from django.shortcuts import render
from .models import Roles, Permissions
from .serializers import (
    PermissionReadSerializer, PermissionWriteSerializer,
    RoleReadSerializer, RoleWriteSerializer
)
from rest_framework import viewsets
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permissions.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PermissionReadSerializer
        return PermissionWriteSerializer
    
    def perform_create(self, serializer):
        
        permission = serializer.save()
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Permission',
            object_id=permission.id,
            description=f"Permission {permission.name} created successfully"
        )
        
    def perform_update(self, serializer):
        
        permission = serializer.save()
        
        create_logs(
            user=self.request.user,
            action='update',
            model_name='Permission',
            object_id=permission.id,
            description=f"Permission {permission.name} updated successfully"
        )
        
    def perform_destroy(self, instance):
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Permission',
            object_id=instance.id,
            description=f"Permission {instance.name} deleted successfully"
        )
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_permission'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_permission'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_permission'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_permission'
            
        return [IsAuthenticated(), permission]
            
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Roles.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return RoleReadSerializer
        return RoleWriteSerializer
    
    def perform_create(self, serializer):
        role = serializer.save()
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Role',
            object_id=role.id,
            description=f"Role {role.name} created successfully"
        )

    def perform_update(self, serializer):
        role = serializer.save()
        create_logs(
            user=self.request.user,
            action='update',
            model_name='Role',
            object_id=role.id,
            description=f"Role {role.name} updated successfully"
        )

    def perform_destroy(self, instance):
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Role',
            object_id=instance.id,
            description=f"Role {instance.name} deleted successfully"
        )

    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_role'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_role'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_role'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_role'
            
        return [IsAuthenticated(), permission]