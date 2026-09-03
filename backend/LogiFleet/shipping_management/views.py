from django.shortcuts import render
from rest_framework import status
from .services import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Shipment, ShipmentStatusHistory
from rest_framework.response import Response
from rest_framework import viewsets
from roles_permissions.permissions import *
from roles_permissions.services import *
from .services import *
from .serializers import ShipmentReadSerializer, ShipmentWriteSerializer, ShipmentAssignSerializer, ShipmentStatusChangeSerializer, DeliveryConfirmationSerializer, ShipmentFailureSerializer
from driver_management.models import Driver
from vehicle_management.models import Vehicle
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.

class SoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        shipping = Shipment.objects.get(pk=pk)
        
        ShippingService.soft_delete(shipping)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Shipment',
            object_id=shipping.id,
            description=f"Shipment {shipping.shipment_number} soft deleted successfully"
        )
        
        return Response({
            'message': 'Soft deleted successfully'
        }, status=status.HTTP_200_OK)
        
class RestoreView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        shipping = Shipment.deleted_objects.get(pk=pk)
        
        ShippingService.restore(shipping)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Shipment',
            object_id=shipping.id,
            description=f"Shipment {shipping.shipment_number} restored successfully"
        )
        
        return Response({
            'message': 'Restored successfully'
        }, status=status.HTTP_200_OK)
        
class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.select_related('customer', 'driver', 'vehicle')
    permission_classes = [IsAuthenticated, HasPermission]

    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ShipmentReadSerializer
        return ShipmentWriteSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "id",
        "code",
        "shipment_number",
        "customer",
        "driver",
        "vehicle",
        "status",
        "priority",
        "pickup_city",
        "delivery_city",
        "is_deleted",
    ]

    search_fields = [
        "shipment_number",
        "customer__name",
        "driver__full_name",
        "vehicle__registration_number",
        "pickup_address",
        "delivery_address",
        "pickup_city",
        "delivery_city",
        "receiver_name",
        "receiver_phone",
        "failure_reason",
    ]

    ordering_fields = [
        "shipment_number",
        "status",
        "priority",
        "pickup_date",
        "estimated_delivery_date",
        "actual_delivery_date",
        "created_at",
        "updated_at",
    ]

    ordering = [
        "-created_at"
    ]
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_shipment'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_shipment'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_shipment'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_shipment'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):
        
        idempotency_key = request.headers.get('idempotency_key')
        
        if not idempotency_key:
            return Response({
                'message': 'Idempotency header is required'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ShipmentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        response_data, status_code = ShippingService.create_shipment(serializer.validated_data, request.user, idempotency_key)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Shipment',
            object_id=response_data.id,
            description=f"Shipment {response_data.shipment_number} created successfully"
        )
        
        return Response(
            response_data,
            status=status_code
        )
    
class ShipmentAssignView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        shipment = Shipment.objects.get(pk=pk)
        
        serializer = ShipmentAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        driver = serializer.validated_data['driver']
        
        vehicle = serializer.validated_data['vehicle']
        
        shipment = ShippingService.assign_shipment(shipment, driver, vehicle, user=request.user)
        
        create_logs(
            user=self.request.user,
            action='assign',
            model_name='Shipment',
            object_id=shipment.id,
            description=f"Shipment {shipment.shipment_number} assigned to driver {driver.full_name} and vehicle {vehicle.registration_number} successfully"
        )
        
        response = ShipmentReadSerializer(shipment)
        
        return Response(response.data, status=status.HTTP_200_OK)
    
class ChangeStatusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        shipment = Shipment.objects.get(pk=pk)
        
        serializer = ShipmentStatusChangeSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        status = serializer.validated_data['status']
        note = serializer.validated_data.get('note', '')
        
        shipment = ShippingService.change_status(shipment=shipment, new_status=status, user=request.user, note=note)
        
        response = ShipmentReadSerializer(shipment)
        
        create_logs(
            user=self.request.user,
            action='status_change',
            model_name='Shipment',
            object_id=shipment.id,
            description=f"Shipment {shipment.shipment_number} status changed to {status}"
        )
        
        return Response(response.data)
    
class ConfirmDeliveryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        shipment = Shipment.objects.get(pk=pk)
        
        serializer = DeliveryConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        shipment = ShippingService.confirm_delivery(
            shipment,
            request.user,
            serializer.validated_data['receiver_name'],
            serializer.validated_data.get('receiverphone', ''),
            serializer.validated_data.get('delivery_notes', '')
        )
        
        response = ShipmentReadSerializer(shipment)
        
        create_logs(
            user=self.request.user,
            action='confirm_delivery',
            model_name='Shipment',
            object_id=shipment.id,
            description=f"Shipment {shipment.shipment_number} delivery confirmed"
        )
        
        return Response(response.data, status=status.HTTP_200_OK)
    
class FailureView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        shipment = Shipment.objects.get(pk=pk)
        
        serializer = ShipmentFailureSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        shipment = ShippingService.fail_shipment(
            shipment,
            request.user,
            serializer.validated_data['failure_reason']
        )
        
        response = ShipmentReadSerializer(shipment)
        
        create_logs(
            user=self.request.user,
            action='fail_shipment',
            model_name='Shipment',
            object_id=shipment.id,
            description=f"Shipment {shipment.shipment_number} failed"
        )
        
        return Response(response.data, status=status.HTTP_200_OK)