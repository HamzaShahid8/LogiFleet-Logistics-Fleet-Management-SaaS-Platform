from django.shortcuts import render
from .models import ActivityLogs
from rest_framework import viewsets
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from .serializers import ActivityLogReadSerializer, ActivityLogWriteSerializer

# Create your views here.

class ActivityLogsViewSet(viewsets.ModelViewSet):
    
    queryset = ActivityLogs.objects.select_related('user')
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ActivityLogReadSerializer
        return ActivityLogWriteSerializer
    
    def get_permissions(self):
        
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_activity_logs'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_activity_logs'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_activity_logs'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_activity_logs'
            
        return [IsAuthenticated(), permission]