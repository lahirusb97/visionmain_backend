from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Frame, FrameStock
from ..serializers import FrameSerializer, FrameStockSerializer
from django.db import transaction
from ..services.branch_protection_service import BranchProtectionsService
# List and Create Frames (with stock)
class FrameListCreateView(generics.ListCreateAPIView):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer

    def list(self, request, *args, **kwargs):
        """
        List frames with optional status filter (?status=active|inactive|all).
        Includes stock information for the branch.
        """
        branch = BranchProtectionsService.validate_branch_id(request)
        status_filter = request.query_params.get("status", "active").lower()

        frames = self.get_queryset()

        if status_filter == "active":
            frames = frames.filter(is_active=True)
        elif status_filter == "inactive":
            frames = frames.filter(is_active=False)
        elif status_filter == "all":
            pass  # no filter
        else:
            return Response(
                {"error": "Invalid status filter. Use 'active', 'inactive', or 'all'."},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = []

        for frame in frames:
            stocks = frame.stocks.filter(branch_id=branch.id)  # ✅ Get all stock entries for this frame
            stock_data = FrameStockSerializer(stocks, many=True).data  # ✅ Ensure many=True

            frame_data = FrameSerializer(frame).data
            frame_data["stock"] = stock_data  # ✅ Store all stock records as a list

            data.append(frame_data)

        return Response(data, status=status.HTTP_200_OK)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create a frame and optionally add stock. Supports multiple stocks for different branches.
        """
        frame_data = request.data.get("frame")
        stock_data_list = request.data.get("stock", [])  # ✅ Default to an empty list if stock is missing

        # ✅ Create the frame
        frame_serializer = self.get_serializer(data=frame_data)
        frame_serializer.is_valid(raise_exception=True)
        frame = frame_serializer.save()

        stock_entries = []

        # ✅ If stock data is provided, process it
        if stock_data_list and isinstance(stock_data_list, list):
            for stock_data in stock_data_list:
                if "initial_count" not in stock_data:
                    return Response(
                        {"error": "initial_count is required for all stock entries."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                stock_data["frame"] = frame.id  # Assign frame ID
                stock_serializer = FrameStockSerializer(data=stock_data)
                stock_serializer.is_valid(raise_exception=True)
                stock_entries.append(stock_serializer.save())

        # ✅ Prepare response
        response_data = frame_serializer.data
        response_data["stocks"] = FrameStockSerializer(stock_entries, many=True).data if stock_entries else []

        return Response(response_data, status=status.HTTP_201_CREATED)

# Retrieve, Update, and Delete Frames (with stock details)
class FrameRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Frame.objects.all()
    serializer_class = FrameSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a frame along with its stock details.
        """
        branch=BranchProtectionsService.validate_branch_id(request)
        frame = self.get_object()
        stock = frame.stocks.filter(branch_id=branch.id)
        frame_data = FrameSerializer(frame).data
        frame_data["stock"] = FrameStockSerializer(stock, many=True).data 
        return Response(frame_data)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        """
        Update frame details and optionally update stock details.
        """
        frame = self.get_object()
        frame_serializer = self.get_serializer(frame, data=request.data, partial=True)
        frame_serializer.is_valid(raise_exception=True)
        frame_serializer.save()

        stock_data_list = request.data.get("stock", [])  # ✅ Default to empty list if no stock data

        stock_entries = []

        # ✅ Process stock updates if provided
        if stock_data_list and isinstance(stock_data_list, list):
            for stock_data in stock_data_list:
                if "initial_count" not in stock_data:
                    return Response(
                        {"error": "initial_count is required for all stock entries."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                branch_id = stock_data.get("branch_id")
                if not branch_id:
                    return Response(
                        {"error": "branch_id is required for stock updates."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # ✅ Check if stock entry exists for the frame & branch
                stock_instance = frame.stocks.filter(branch_id=branch_id).first()

                if stock_instance:
                    # ✅ Update existing stock
                    stock_serializer = FrameStockSerializer(stock_instance, data=stock_data, partial=True)
                else:
                    # ✅ Create new stock entry if it doesn't exist
                    stock_data["frame"] = frame.id
                    stock_serializer = FrameStockSerializer(data=stock_data)

                stock_serializer.is_valid(raise_exception=True)
                stock_entries.append(stock_serializer.save())

        # ✅ Prepare response
        response_data = frame_serializer.data
        response_data["stocks"] = FrameStockSerializer(stock_entries, many=True).data if stock_entries else []

        return Response(response_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: Mark the frame as inactive instead of deleting it.
        """
        frame = self.get_object()
        frame.is_active = False
        frame.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

