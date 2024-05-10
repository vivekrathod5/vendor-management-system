import uuid
from django.db import models
from vendors.models import Vendor

class PurchaseOrder(models.Model):
    class Meta:
        db_table = 'purchase_orders'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    po_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4())
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default="pending")
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.vendor.calculate_on_time_delivery_rate()
        self.vendor.calculate_quality_rating_avg()
        self.vendor.calculate_average_response_time()
        self.vendor.calculate_fulfillment_rate()
        self.vendor.save()