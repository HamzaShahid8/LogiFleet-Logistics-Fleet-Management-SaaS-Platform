from rest_framework import serializers
from .models import Vehicle


class VehicleReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            'id',
            'code',
            'registration_number',
            'vin',
            'vehicle_type',
            'make',
            'model',
            'year',
            'capacity',
            'fuel_type',
            'current_mileage',
            'status',
            'purchase_date',
            'is_deleted',
            'created_at',
            'updated_at',
        ]

        read_only_fields = [
            'id',
            'code',
            'created_at',
            'updated_at',
            'vehicle_type_display',
            'fuel_type_display',
            'status_display',
        ]


class VehicleWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = [
            'registration_number',
            'vin',
            'vehicle_type',
            'make',
            'model',
            'year',
            'capacity',
            'fuel_type',
            'current_mileage',
            'status',
            'purchase_date',
        ]
        
    def validate_registration_number(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Registration number is required')
        
        return value
    
    def validate_vin(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('VIN is required')

        return value
    
    def validate_vehicle_type(self, value):
        if not value:
            raise serializers.ValidationError('Vehicle type is required')

        return value
    
    def validate_make(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Make is required')

        return value
    
    def validate_model(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('Model is required')

        return value
    
    def validate_year(self, value):
        if not value:
            raise serializers.ValidationError('Year is required')

        return value
    
    def validate_capacity(self, value):
        if not value:
            raise serializers.ValidationError('Capacity is required')

        if value <= 0:
            raise serializers.ValidationError('Capacity must be greater than 0')

        return value
    
    def validate_fuel_type(self, value):
        if not value:
            raise serializers.ValidationError('Fuel type is required')

        return value


    def validate_current_mileage(self, value):
        if value is None:
            raise serializers.ValidationError('Current mileage is required')

        if value < 0:
            raise serializers.ValidationError('Current mileage cannot be negative')

        return value


    def validate_purchase_date(self, value):
        if not value:
            raise serializers.ValidationError('Purchase date is required')

        return value