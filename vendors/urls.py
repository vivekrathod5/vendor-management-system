from django.urls import path
from .views import VendorListAPIView, VendorDetailAPIView, VendorPerformanceAPIView

urlpatterns = [
    path('api/vendors', VendorListAPIView.as_view(), name='vendor-list'),
    path('api/vendors/<str:vendor_id>', VendorDetailAPIView.as_view(), name='vendor-detail'),
    path('api/vendors/<str:vendor_id>/performance', VendorPerformanceAPIView.as_view(), name='vendor-performance'),
    
]
