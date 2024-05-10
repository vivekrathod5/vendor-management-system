from .models import Vendor
from drf_yasg import openapi
from rest_framework import status
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from .serializers import VendorSerializer, VendorPerformanceSerializer



class VendorListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        """
        List all vendors.

        Authentication:
        - Requires authentication.

        Response:
        - Returns a list of all vendors.
        """
        vendors = Vendor.objects.all()
        if vendors:
            serializer = VendorSerializer(vendors, many=True)
            data = {'message': 'Records fetched successfully.', "data":serializer.data}
        else:
            data = {'message': 'Vendors not found.', "data":{}}
        return Response(data)
    

    @swagger_auto_schema(
        operation_description="Endpoint for create a new vendor.",
        request_body=VendorSerializer
    )
    def post(self, request):
        """
        Create a new vendor.

        Authentication:
        - Requires authentication.

        Request Body:
        - name: Vendor's name (required)
        - contact_details: Vendor's contact details
        - address: Vendor's address
        - vendor_code: Unique identifier for the vendor

        Response:
        - Returns the created vendor data if successful.
        """
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = {'message': 'Vendor added successfully.', "data":serializer.data}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorDetailAPIView(APIView):

    def get_object(self, vendor_id):
        """
        Get vendor object by ID.

        Returns:
        - Vendor object if found, otherwise None.
        """
        try:
            return Vendor.objects.get(pk=vendor_id)
        except Vendor.DoesNotExist:
            return None


    def get(self, request, vendor_id):
        """
        Retrieve details of a specific vendor.

        Authentication:
        - Requires authentication.

        Parameters:
        - vendor_id: ID of the vendor to retrieve.

        Response:
        - Returns the vendor details if found, otherwise returns an error.
        """
        vendor = self.get_object(vendor_id)
        if vendor:
            serializer = VendorSerializer(vendor)
            data = {'message': 'Record fetch successful.', "data":serializer.data}
            return Response(data)
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
        operation_description="Endpoint for update vendor.",
        request_body=VendorSerializer
    )
    def put(self, request, vendor_id):
        """
        Update a vendor's details.

        Authentication:
        - Requires authentication.

        Parameters:
        - vendor_id: ID of the vendor to update.

        Request Body:
        - name: Vendor's name
        - contact_details: Vendor's contact details
        - address: Vendor's address
        - vendor_code: Unique identifier for the vendor

        Response:
        - Returns the updated vendor data if successful.
        """
        vendor = self.get_object(vendor_id)
        if vendor:
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {'message': 'Vendor updated successfully.', "data":serializer.data}
                return Response(data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, vendor_id):
        """
        Delete a vendor.

        Authentication:
        - Requires authentication.

        Parameters:
        - vendor_id: ID of the vendor to delete.

        Response:
        - Returns a success message if the vendor is deleted successfully.
        """
        vendor = self.get_object(vendor_id)
        if vendor:
            vendor.delete()
            return Response({"message": "Vendor deleted successfully"})
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)







class VendorPerformanceAPIView(APIView):
    """
    API endpoint to retrieve a vendor's performance metrics.

    Authentication:
        - Requires authentication.

    Parameters:
    - vendor_id: The ID of the vendor whose performance metrics are to be retrieved.

    Response:
    -  Retrieves the performance metrics for the specified vendor.
    """
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VendorPerformanceSerializer(vendor)
        data = {'message': 'Record fetch successful.', "data":serializer.data}
        return Response(data)