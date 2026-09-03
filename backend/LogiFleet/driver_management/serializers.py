from rest_framework import serializers
from .models import Driver

class DriverReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'code', 'full_name', 'email', 'phone', 'license_number', 'license_type', 'license_expiry', 'joining_date', 'status', 'address', 'emergency_contact', 'created_at', 'updated_at']
        
class DriverWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['full_name', 'email', 'phone', 'license_number', 'license_type', 'license_expiry', 'joining_date', 'status', 'address', 'emergency_contact']
        
        
    def validate_full_name(self, value):
        if not value or  not value.strip():
            raise serializers.ValidationError('Full name is required')
        
        return value
    
    def validate_license_number(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError('License number is required')
        
        return value