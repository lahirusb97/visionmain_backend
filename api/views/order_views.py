from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Order, OrderItem, OrderPayment, LensStock, LensCleanerStock, FrameStock,RefractionDetails,Refraction
from ..serializers import OrderSerializer, OrderItemSerializer, OrderPaymentSerializer
from ..services.order_payment_service import OrderPaymentService
from ..services.stock_validation_service import StockValidationService
from ..services.order_service import OrderService
from ..services.patient_service import PatientService
from ..services.Invoice_service import InvoiceService
from ..services.refraction_details_service import RefractionDetailsService
from django.utils import timezone

class OrderCreateView(APIView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            # Start transaction
            with transaction.atomic():
                
                # 🔹 Step 1: Validate & Create/Update Patient
                patient_data = request.data.get("patient")
                if not patient_data:
                    return Response({"error": "Patient details are required."}, status=status.HTTP_400_BAD_REQUEST)

                patient = PatientService.create_or_update_patient(patient_data)

                # 🔹 Step 2: Update Refraction linkage if provided
                refraction_id = patient_data.get("refraction_id")
                if refraction_id:
                    try:
                        refraction = Refraction.objects.get(id=refraction_id)
                        refraction.patient = patient
                        refraction.save()
                    except Refraction.DoesNotExist:
                        return Response({"error": "Refraction record not found."}, status=status.HTTP_400_BAD_REQUEST)

                # 🔹 Step 3: Create Refraction Details if provided
                refraction_details_data = request.data.get("refraction_details")
                if refraction_details_data:
                    refraction_details_data["patient"] = patient.id
                    RefractionDetailsService.create_refraction_details(refraction_details_data)
                else:
                    if patient.refraction_id:
                        try:
                            refraction_details = RefractionDetails.objects.get(refraction_id=patient.refraction_id)
                            refraction_details.patient_id = patient.id
                            refraction_details.save()
                        except RefractionDetails.DoesNotExist:
                            pass  # No existing refraction details, continue

                # 🔹 Step 4: Extract Order Data
                order_data = request.data.get('order')
                if not order_data:
                    return Response({"error": "The 'order' field is required."}, status=status.HTTP_400_BAD_REQUEST)
                
                # ✅ Ensure order_date is set
                if not order_data.get('user_date'):
                    order_data['user_date'] = timezone.now().date()

                # 🔹 Step 5: Extract On-Hold status
                on_hold = order_data.get('on_hold', False)

                # 🔹 Step 6: If not on_hold, validate stocks
                stock_updates = []
                if not on_hold:
                    branch_id = order_data.get("branch_id")
                    if not branch_id:
                        return Response({"error": "Branch ID is required for stock validation."}, status=status.HTTP_400_BAD_REQUEST)

                    order_items_data = request.data.get('order_items', [])
                    stock_items = [item for item in order_items_data if not item.get('is_non_stock', False)]

                    stock_updates = StockValidationService.validate_stocks(stock_items, branch_id) if stock_items else []
                else:
                    order_items_data = request.data.get('order_items', [])

                # 🔹 Step 7: Create Order + Items
                order_data["customer"] = patient.id
                order = OrderService.create_order(order_data, order_items_data)

                # 🔹 Step 8: Generate Invoice
                InvoiceService.create_invoice(order)

                # 🔹 Step 9: Create Payments
                payments_data = request.data.get('order_payments', [])
                if not payments_data:
                    raise ValueError("At least one order payment is required.")

                total_payment = OrderPaymentService.process_payments(order, payments_data)

                # 🔹 Step 10: Validate payment amount
                if total_payment > order.total_price:
                    raise ValueError("Total payments exceed the order total price.")

                # 🔹 Step 11: Adjust Stocks if not on_hold
                if not on_hold and stock_updates:
                    StockValidationService.adjust_stocks(stock_updates)

                # 🔹 Step 12: Return Success
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        except ValueError as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)