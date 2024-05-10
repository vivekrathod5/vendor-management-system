

from rest_framework import serializers
from .models import PurchaseOrder


class PurchaseOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status']

    def to_representation(self, instance):
        """
        Serialize all fields of the instance.
        """
        representation = {}
        for field in self.Meta.model._meta.fields:
            value = getattr(instance, field.attname)
            representation[field.attname] = value
        return representation


class PurchaseOrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['order_date', 'delivery_date', 'items', 'quantity', 'status', 'acknowledgment_date']

    def to_representation(self, instance):
        """
        Serialize all fields of the instance.
        """
        representation = {}
        for field in self.Meta.model._meta.fields:
            value = getattr(instance, field.attname)
            representation[field.attname] = value
        return representation
