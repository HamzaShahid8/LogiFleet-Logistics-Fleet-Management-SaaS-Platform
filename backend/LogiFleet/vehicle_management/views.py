from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vehicle
from rest_framework import viewsets
from rest_framework import status
from .serializers import *
from roles_permissions.permissions import *
from roles_permissions.services import *
from rest_framework.permissions import IsAuthenticated
from .services import *
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.


class VehicleViewSet(viewsets.ModelViewSet):
    
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return VehicleReadSerializer
        return VehicleWriteSerializer
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_vehicle'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_vehicle'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_vehicle'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_vehicle'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):
        
        serializer = VehicleWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        vehicle = serializer.save()
        
        response = VehicleReadSerializer(vehicle)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Vehicle',
            object_id=vehicle.id,
            description=f"Vehicle {vehicle.registration_number} created successfully"
        )
        
        return Response(response.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        
        vehicle = serializer.save()
        
        create_logs(
            user=self.request.user,
            action='update',
            model_name='Vehicle',
            object_id=vehicle.id,
            description=f"Vehicle {vehicle.registration_number} updated successfully"
        )
        
    def list(self, request, *args, **kwargs):
        
        response = super().list(request, *args, **kwargs)
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Vehicle',
            description="Vehicle list viewed successfully"
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        
        response = super().retrieve(request, *args, **kwargs)
        
        vehicle = self.get_object()
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Vehicle',
            object_id=vehicle.id,
            description=f"Vehicle {vehicle.registration_number} viewed successfully"
        )
        return response
    
class SoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        vehicle = Vehicle.objects.get(pk=pk)
        
        VehicleService.soft_delete(vehicle)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Vehicle',
            object_id=vehicle.id,
            description=f"Vehicle {vehicle.registration_number} soft deleted successfully"
        )

        return Response({
            'message': "Vehicle soft deleted successfully"
        }, status=status.HTTP_200_OK)
        
class RestoreView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        vehicle = Vehicle.deleted_objects.get(pk=pk)
        
        VehicleService.restore(vehicle)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Vehicle',
            object_id=vehicle.id,
            description=f"Vehicle {vehicle.registration_number} restored successfully"
        )
        
        return Response({
            'message': 'Vehicle restored successfully'
        }, status=status.HTTP_200_OK)