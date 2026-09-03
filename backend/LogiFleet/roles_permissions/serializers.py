from .models import Roles, Permissions
from rest_framework import serializers

class PermissionReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['id', 'name']
        
class PermissionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permissions
        fields = ['name']
        
class RoleReadSerializer(serializers.ModelSerializer):
    permissions = PermissionReadSerializer(read_only=True, many=True)
    
    class Meta:
        model = Roles
        fields = ['id', 'name', 'permissions']
        
class RoleWriteSerializer(serializers.ModelSerializer):
    permissions = serializers.SlugRelatedField(queryset = Permissions.objects.all(), slug_field='name', many=True)
    
    class Meta:
        model = Roles
        fields = ['name', 'permissions']