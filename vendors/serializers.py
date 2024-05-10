from .models import Vendor
from rest_framework import serializers
from vendors.helper import generate_vendor_code

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['id', 'name', 'contact_details', 'address']
        

    def create(self, validated_data):
        """
        Create and return a new Vendor instance, given the validated data.
        """
        vendor_code = generate_vendor_code()
        validated_data["vendor_code"] = vendor_code
        return Vendor.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing Vendor instance, given the validated data.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.contact_details = validated_data.get('contact_details', instance.contact_details)
        instance.address = validated_data.get('address', instance.address)
        instance.save()
        return instance
    
    
    def to_representation(self, instance):
        """
        Serialize all fields of the instance.
        """
        representation = {}
        for field in self.Meta.model._meta.fields:
            value = getattr(instance, field.attname)
            representation[field.attname] = value
        return representation
    



class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'
