import uuid
from django.db import models
from django.utils import timezone


class Vendor(models.Model):
    class Meta:
        db_table = "vendors"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False, unique=True)
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)


    def calculate_on_time_delivery_rate(self):
        completed_orders = self.purchaseorder_set.filter(status='completed')
        total_completed_orders = completed_orders.count()
        if total_completed_orders == 0:
            return 0
        on_time_orders = completed_orders.filter(delivery_date__lte=timezone.now())
        on_time_delivery_rate = (on_time_orders.count() / total_completed_orders) * 100
        return on_time_delivery_rate

    def calculate_quality_rating_avg(self):
        completed_orders = self.purchaseorder_set.filter(status='completed').exclude(quality_rating__isnull=True)
        if completed_orders.exists():
            return completed_orders.aggregate(avg_rating=models.Avg('quality_rating'))['avg_rating']
        return 0.0

    def calculate_average_response_time(self):
        completed_orders = self.purchaseorder_set.filter(status='completed').exclude(acknowledgment_date__isnull=True)
        if completed_orders.exists():
            response_times = [(po.acknowledgment_date - po.issue_date).total_seconds() for po in completed_orders]
            return sum(response_times) / len(response_times)
        return 0.0

    def calculate_fulfillment_rate(self):
        total_orders = self.purchaseorder_set.count()
        if total_orders == 0:
            return 0
        completed_orders = self.purchaseorder_set.filter(status='completed')
        successful_orders = completed_orders.exclude(quality_rating__lt=3)  # Assuming 3 or above is considered successful
        fulfillment_rate = (successful_orders.count() / total_orders) * 100
        return fulfillment_rate
