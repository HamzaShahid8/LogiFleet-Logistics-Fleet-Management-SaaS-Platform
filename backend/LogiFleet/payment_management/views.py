from django.shortcuts import render
from .services import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Payment
from rest_framework import viewsets
from roles_permissions.services import *
from roles_permissions.permissions import *
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.

class SoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        payment = Payment.all_objects.get(pk=pk)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Payment',
            object_id=payment.id,
            description=f"Payment {payment.payment_number} soft deleted successfully"
        )
        
        PaymentService.soft_delete(payment)
        
        return Response({
            'message': 'Payment soft deleted'
        }, status=status.HTTP_200_OK)
        
class RestoreView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        payment = Payment.deleted_objects.get(pk=pk)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Payment',
            object_id=payment.id,
            description=f"Payment {payment.payment_number} restored successfully"
        )
        
        PaymentService.restore(payment)
        
        return Response({
            'message': 'Payment restored successfully'
        }, status=status.HTTP_200_OK)
        
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice', 'customer')
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PaymentReadSerializer
        return PaymentWriteSerializer
    
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_payment'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_payment'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_payment'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_payment'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):
        
        idempotency_key = request.headers.get('idempotency_key')
        
        if not idempotency_key:
            return Response({
                'message': 'Idempotency-key header is required'
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        response_data, status_code = PaymentService.create_payment(serializer.validated_data, request.user, idempotency_key)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Payment',
            object_id=response_data['id'],
            description=f"Payment {response_data['payment_number']} created successfully"
        )
        
        return Response(response_data, status=status_code)
    
    def list(self, request, *args, **kwargs):
        
        response = super().list(request, *args, **kwargs)
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Payment',
            description="Payment list viewed successfully"
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        
        response = super().retrieve(request, *args, **kwargs)
        
        payment = self.get_object()
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Payment',
            object_id=payment.id,
            description=f"Payment {payment.payment_number} viewed successfully"
        )
        
        return response