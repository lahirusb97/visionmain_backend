from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status,generics
from ..services.Invoice_service import InvoiceService
from ..serializers import InvoiceSerializer,InvoiceSearchSerializer,ExternalLensOrderItemSerializer
from rest_framework.pagination import PageNumberPagination
from ..models import OrderItem,Invoice,OrderItemWhatsAppLog
from ..services.pagination_service import PaginationService
from django.db.models import Exists, OuterRef

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = 'page_size'  # Allow client to override
    max_page_size = 100  # Maximum limit

class FactoryInvoiceSearchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    def get(self, request):
        invoice_number = request.query_params.get('invoice_number')
        mobile = request.query_params.get('mobile')
        nic = request.query_params.get('nic')
        branch_id = request.query_params.get('branch_id')
        progress_status = request.query_params.get('progress_status')

        if not any([invoice_number, mobile, nic,branch_id,progress_status]):
            return Response(
                {"error": "Please provide at least one search parameter: invoice_number, mobile, or nic."},
                status=status.HTTP_400_BAD_REQUEST
            )

        invoices = InvoiceService.search_factory_invoices(
            user=request.user,
            invoice_number=invoice_number,
            mobile=mobile,
            nic=nic,
            branch_id=branch_id,
            progress_status=progress_status
        )
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(invoices, request)
        if page is not None:
            serializer = InvoiceSearchSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        #InvoiceSearchSerializer provide only nesasry info for the checkin module
        serializer = InvoiceSearchSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FactoryInvoiceExternalLenseSearchView(generics.ListAPIView):
    serializer_class = ExternalLensOrderItemSerializer
    pagination_class = PaginationService

    def get_queryset(self):
        queryset = OrderItem.objects.filter(
            external_lens__isnull=False,
            is_deleted=False,
            order__is_deleted=False
        ).select_related(
            'order__invoice', 'order__branch'
        ).filter(
            order__invoice__is_deleted=False
        )

        invoice_number = self.request.query_params.get('invoice_number')
        whatsapp_sent = self.request.query_params.get('whatsapp_sent')
        order_status = self.request.query_params.get('order_status')
        branch_id = self.request.query_params.get('branch_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if invoice_number:
            queryset = queryset.filter(order__invoice__invoice_number__icontains=invoice_number)

        # --- Only apply annotation/filter if param is present ---
        if whatsapp_sent in ['sent', 'not_sent']:
            queryset = queryset.annotate(
                has_whatsapp_log=Exists(
                    OrderItemWhatsAppLog.objects.filter(order=OuterRef('order_id'))
                )
            )
            if whatsapp_sent == 'sent':
                queryset = queryset.filter(has_whatsapp_log=True)
            elif whatsapp_sent == 'not_sent':
                queryset = queryset.filter(has_whatsapp_log=False)

        if order_status:
            queryset = queryset.filter(order__status=order_status)

        if branch_id:
            queryset = queryset.filter(order__branch_id=branch_id)

        if start_date and end_date:
            try:
                from datetime import datetime, timedelta
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
                queryset = queryset.filter(order__order_date__gte=start, order__order_date__lt=end)
            except ValueError:
                pass

        return queryset

class InvoiceNumberSearchView(APIView):
    """
    Search for a single invoice by its invoice_number.
    If not found, returns {"error": "Invoice not found"} with 404 status.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        invoice_number = request.query_params.get('invoice_number')
        if not invoice_number:
            return Response(
                {"error": "invoice_number query parameter is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        invoice = Invoice.objects.filter(
            invoice_number=invoice_number,
            is_deleted=False
        ).first()

        if not invoice:
            return Response(
                {"error": "Invoice not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = InvoiceSearchSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)