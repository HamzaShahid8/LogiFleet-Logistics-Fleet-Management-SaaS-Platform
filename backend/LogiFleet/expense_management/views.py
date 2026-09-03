from django.shortcuts import render
from .services import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Expense
from rest_framework.response import Response
from rest_framework import status
from roles_permissions.permissions import *
from roles_permissions.services import *
from .serializers import ExpenseReadSerializer, ExpenseWriteSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.

class SoftDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        expense = Expense.all_objects.get(pk=pk)
        
        ExpenseService.soft_delete(expense)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Expense',
            object_id=expense.id,
            description=f"Expense {expense.shipment} - {expense.driver} - {expense.vehicle} soft deleted successfully"
        )
        
        return Response({
            'message': 'Expense soft deleted successfully'
        }, status=status.HTTP_200_OK)
        
class RestoreView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        expense = Expense.deleted_objects.get(pk=pk)
        
        ExpenseService.restore(expense)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Expense',
            object_id=expense.id,
            description=f"Expense {expense.shipment} - {expense.driver} - {expense.vehicle} restored successfully"
        )

        return Response({
            'message': 'Expense restored successfully'
        }, status=status.HTTP_200_OK)
        
class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('shipment', 'driver', 'vehicle')
    permission_classes = [IsAuthenticated, HasPermission]
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExpenseReadSerializer
        return ExpenseWriteSerializer
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "id",
        "code",
        "expense_type",
        "shipment",
        "driver",
        "vehicle",
        "payment_method",
        "is_deleted",
    ]
    
    search_fields = [
        "code",
        "shipment__shipment_number",
        "driver__full_name",
        "vehicle__registration_number",
        "description",
        "receipt_number",
    ]
    
    ordering_fields = [
        "expense_type",
        "amount",
        "payment_method",
        "expense_date",
        "created_at",
        "updated_at",
    ]
    
    ordering = [
        "-created_at"
    ]
    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_expense'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_expense'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_expense'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_expense'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):
        
        serializer = ExpenseWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        expense = serializer.save()
        
        response = ExpenseReadSerializer(expense)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Expense',
            object_id=expense.id,
            description=f"Expense {expense.shipment} - {expense.driver} - {expense.vehicle} created successfully"
        )
        
        return Response(response.data, status=status.HTTP_201_CREATED)
    
    def list(self, request, *args, **kwargs):
        
        response = super().list(request, *args, **kwargs)
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Expense',
            description="Expense list viewed successfully"
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        
        response = super().retrieve(request, *args, **kwargs)
        
        expense = self.get_object()
        
        create_logs(
            user=self.request.user,
            action='view',
            model_name='Expense',
            object_id=expense.id,
            description=f"Expense {expense.shipment} - {expense.driver} - {expense.vehicle} viewed successfully"
        )
        
        return response