from rest_framework import serializers
from .models import Shipment, ShipmentStatusHistory, ShipmentCharge
from .validators import *
from customer_management.models import Customer
from driver_management.models import Driver
from vehicle_management.models import Vehicle
from invoice_management.serializers import InvoiceReadSerializer

class ShipmentChargeReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentCharge
        fields = ['id', 'code', 'charge_type', 'amount', 'description', 'is_deleted']
        
class ShipmentChargeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShipmentCharge
        fields = ['charge_type', 'amount', 'description']

class ShipmentWriteSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(queryset = Customer.objects.all(), slug_field='name')
    driver = serializers.SlugRelatedField(queryset = Driver.objects.all(), slug_field='full_name', required=False, allow_null=True)
    vehicle = serializers.SlugRelatedField(queryset = Vehicle.objects.all(), slug_field='registration_number', required=False, allow_null=True)
    charges = ShipmentChargeWriteSerializer(write_only=True, many=True)

    class Meta:
        model = Shipment
        fields = [
            "shipment_number",
            "customer",
            "driver",
            "vehicle",
            "pickup_address",
            "delivery_address",
            "pickup_city",
            "delivery_city",
            "package_description",
            "weight",
            "quantity",
            "priority",
            "pickup_date",
            "estimated_delivery_date",
            'charges',
        ]

    def validate_weight(self, value):
        validate_weight(value)
        return value

    def validate_quantity(self, value):
        validate_quantity(value)
        return value

    def validate(self, attrs):
        pickup_date = attrs.get("pickup_date")
        estimated_delivery_date = attrs.get(
            "estimated_delivery_date"
        )

        if pickup_date and estimated_delivery_date:
            validate_shipment_dates(
                pickup_date,
                estimated_delivery_date
            )

        return attrs

class ShipmentReadSerializer(serializers.ModelSerializer):

    customer_name = serializers.CharField(
        source="customer.name",
        read_only=True
    )

    driver_name = serializers.CharField(
        source="driver.full_name",
        read_only=True
    )

    vehicle_registration = serializers.CharField(
        source="vehicle.registration_number",
        read_only=True
    )
    
    charges = ShipmentChargeReadSerializer(read_only=True, many=True)
    
    invoice = InvoiceReadSerializer(read_only=True)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "code",
            "shipment_number",
            "customer",
            "customer_name",
            "driver",
            "driver_name",
            "vehicle",
            "vehicle_registration",
            "pickup_address",
            "delivery_address",
            "pickup_city",
            "delivery_city",
            "package_description",
            "weight",
            "quantity",
            "priority",
            "status",
            "pickup_date",
            "estimated_delivery_date",
            "actual_delivery_date",
            "receiver_name",
            "receiver_phone",
            "delivery_notes",
            "failure_reason",
            "is_deleted",
            "created_at",
            "updated_at",
            'charges',
            'invoice',
        ]
        
class ShipmentAssignSerializer(serializers.Serializer):
    driver = serializers.SlugRelatedField(queryset = Driver.objects.all(), slug_field='full_name')
    vehicle = serializers.SlugRelatedField(queryset = Vehicle.objects.all(), slug_field='registration_number')
    
class ShipmentStatusChangeSerializer(serializers.Serializer):
    status = serializers.CharField()
    note = serializers.CharField(required=False, allow_blank=True)
    
class DeliveryConfirmationSerializer(serializers.Serializer):
    receiver_name = serializers.CharField()
    receiver_phone = serializers.CharField(required=False, allow_blank=True)
    delivery_notes = serializers.CharField(required=False, allow_blank=True)
    
class ShipmentFailureSerializer(serializers.Serializer):
    failure_reason = serializers.CharField()