from django.shortcuts import render
from .services import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import viewsets
from .models import Invoice
from rest_framework.permissions import IsAuthenticated
from roles_permissions.services import *
from roles_permissions.permissions import *
from .serializers import InvoiceReadSerializer, InvoiceWriteSerializer
from .services import *
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.

class SoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        invoice = Invoice.all_objects.get(pk=pk)
        
        InvoiceService.soft_delete(invoice)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Invoice',
            object_id=invoice.id,
            description=f"Invoice {invoice.invoice_number} soft deleted successfully"
        )
        
        return Response({'message': 'Invoice soft delete successfully'}, status=status.HTTP_200_OK)
    
class RestoreView(APIView):
    
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        
        invoice = Invoice.deleted_objects.get(pk=pk)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Invoice',
            object_id=invoice.id,
            description=f"Invoice {invoice.invoice_number} restored successfully"
        )
        
        InvoiceService.restore(invoice)
        
        return Response({
            'message': 'Invoice restored successfully'
        }, status=status.HTTP_200_OK)
        
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('customer', 'shipment')
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return InvoiceReadSerializer
        return InvoiceWriteSerializer
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_invoice'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_invoice'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_invoice'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_invoice'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):
        
        serializer = InvoiceWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        shipment = serializer.validated_data['shipment']
        
        invoice = InvoiceService.calculate_invoice(shipment)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Invoice',
            object_id=invoice.id,
            description=f"Invoice {invoice.invoice_number} created successfully"
        )
        
        response = InvoiceReadSerializer(invoice)
        
        return Response(response.data, status=status.HTTP_200_OK)
    
    def perform_update(self, serializer):
        invoice = serializer.save()
        
        create_logs(
            user=self.request.user,
            action='update',
            model_name='Invoice',
            object_id=invoice.id,
            description=f"Invoice {invoice.invoice_number} updated successfully"
        )
        
        InvoiceService.update_invoice(invoice)
        
    def list(self, request, *args, **kwargs):
        
        response = super().list(request, *args, **kwargs)
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Invoice',
            description='Invoice list viewed successfully'
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        
        response = super().retrieve(request, *args, **kwargs)
        
        invoice = self.get_object()
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Invoice',
            object_id=invoice.id,
            description=f"Invoice {invoice.invoice_number} viewed successfully"
        )
        
        return response