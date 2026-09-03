from django.shortcuts import render
from .services import *
from .models import Driver
from .serializers import DriverReadSerializer, DriverWriteSerializer
from rest_framework import viewsets
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.

class DriverViewSet(viewsets.ModelViewSet):
    
    queryset = Driver.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DriverReadSerializer
        return DriverWriteSerializer
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_driver'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_driver'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_driver'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_driver'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        driver = serializer.save()
        
        response = DriverReadSerializer(driver)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Driver',
            object_id=driver.id,
            description=f"Driver {driver.full_name} created successfully"
        )
        
        return Response(response.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        
        driver = serializer.save()
        
        create_logs(
            user=self.request.user,
            action='update',
            model_name='Driver',
            object_id=driver.id,
            description=f"Driver {driver.full_name} updated successfully"
        )
        
    def list(self, request, *args, **kwargs):
        
        response = super().list(request, *args, **kwargs)
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Driver',
            description='User viewd driver list'
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        
        response = super().retrieve(request, *args, **kwargs)
        
        driver = self.get_object()
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Driver',
            object_id=driver.id,
            description=f"User view driver {driver.full_name} details"
        )
        
        return response

class DeleteDriver(APIView):
    def post(self, request, pk):
        driver = Driver.objects.get(pk=pk)
    
        DriverService.soft_delete(driver)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Driver',
            object_id=driver.id,
            description=f"Driver {driver.full_name} deleted successfully"
        )
    
        return Response({
            'message': 'Driver deleted successfully'
        }, status=status.HTTP_200_OK)
    
class RestoreDriver(APIView):
    def post(self, request, pk):
        driver = Driver.deleted_objects.get(pk=pk)
        
        DriverService.restore(driver)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Driver',
            object_id=driver.id,
            description=f"Driver {driver.full_name} restored successfully"
        )
        
        return Response({
            'message': 'Driver restored successfully'
        }, status=status.HTTP_200_OK)