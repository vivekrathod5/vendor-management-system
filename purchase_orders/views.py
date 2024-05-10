from .models import PurchaseOrder
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from .serializers import PurchaseOrderCreateSerializer, PurchaseOrderUpdateSerializer


class PurchaseOrderListCreateAPIView(APIView):

    def get(self, request):
        """
        List all purchase orders.

        Response:
        - Returns a list of all purchase orders.
        """
        purchase_orders = PurchaseOrder.objects.all()
        if purchase_orders:
            serializer = PurchaseOrderCreateSerializer(purchase_orders, many=True)
            data = {'message': 'Records fetched successfully.', "data":serializer.data}
            return Response(data, status=200)
        else:
            data = {'message': 'Orders not found', "data":[]}
            return Response(data, status=400)

    @swagger_auto_schema(
        operation_description="Endpoint for create a new purchase order.",
        request_body=PurchaseOrderCreateSerializer
    )
    def post(self, request):
        """
        Create a new purchase order.

        Request Body:
        - po_number: Purchase order number (required)
        - vendor: Vendor ID (required)
        - order_date: Order date
        - delivery_date: Expected or actual delivery date
        - items: Details of items ordered
        - quantity: Total quantity of items in the purchase order
        - status: Current status of the purchase order (e.g., pending, completed, canceled)

        Response:
        - Returns the created purchase order data if successful.
        """
        serializer = PurchaseOrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'message': 'Purchase order successful.', "data":serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderDetailAPIView(APIView):
    def get_object(self, po_id):
        """
        Get purchase order object by ID.

        Returns:
        - Purchase order object if found, otherwise None.
        """
        try:
            return PurchaseOrder.objects.get(pk=po_id)
        except PurchaseOrder.DoesNotExist:
            return None

    def get(self, request, po_id):
        """
        Retrieve details of a specific purchase order.

        Parameters:
        - po_id: ID of the purchase order to retrieve.

        Response:
        - Returns the purchase order details if found, otherwise returns an error.
        """
        purchase_order = self.get_object(po_id)
        if purchase_order:
            serializer = PurchaseOrderUpdateSerializer(purchase_order)
            data = {'message': 'Record fetch successful.', "data":serializer.data}
            return Response(data)
        return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Endpoint for create a new purchase order.",
        request_body=PurchaseOrderUpdateSerializer
    )
    def put(self, request, po_id):
        """
        Update a purchase order's details.

        Parameters:
        - po_id: ID of the purchase order to update.

        Request Body:
        - po_number: Purchase order number
        - vendor: Vendor ID
        - order_date: Order date
        - delivery_date: Expected or actual delivery date
        - items: Details of items ordered
        - quantity: Total quantity of items in the purchase order
        - status: Current status of the purchase order (e.g., pending, completed, canceled)

        Response:
        - Returns the updated purchase order data if successful.
        """
        purchase_order = self.get_object(po_id)
        if purchase_order:
            serializer = PurchaseOrderUpdateSerializer(purchase_order, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {'message': 'Order updated successfully.', "data":serializer.data}
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, po_id):
        """
        Delete a purchase order.

        Parameters:
        - po_id: ID of the purchase order to delete.

        Response:
        - Returns a success message if the purchase order is deleted successfully.
        """
        purchase_order = self.get_object(po_id)
        if purchase_order:
            purchase_order.delete()
            return Response({"message": "Purchase order deleted successfully"})
        return Response({"error": "Purchase order not found"}, status=status.HTTP_404_NOT_FOUND)
