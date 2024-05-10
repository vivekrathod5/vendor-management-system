from django.urls import path
from .views import PurchaseOrderListCreateAPIView, PurchaseOrderDetailAPIView

urlpatterns = [
    path('api/purchase_orders', PurchaseOrderListCreateAPIView.as_view(), name='purchase-order-list'),
    path('api/purchase_orders/<str:po_id>', PurchaseOrderDetailAPIView.as_view(), name='purchase-order-detail'),
]
