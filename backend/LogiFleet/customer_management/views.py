from django.shortcuts import render
from rest_framework import viewsets
from .models import Customer
from .serializers import CustomerReadSerializer, CustomerWriteSerializer
from roles_permissions.services import *
from roles_permissions.permissions import *
from rest_framework.permissions import IsAuthenticated
from .services import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs

# Create your views here.


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, HasPermission]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['id', 'code', 'name', 'email', 'phone', 'address', 'city', 'country', 'tax_number', 'credit_limit']
    search_fields = ['id', 'code', 'name', 'email', 'phone', 'address', 'tax_number', 'credit_limit']
    ordering_fields = ['name', 'email']
    ordering = ['-id', '-created_at']
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CustomerReadSerializer
        return CustomerWriteSerializer

    
    def get_permissions(self):
        permission = HasPermission()
        
        if self.action == 'create':
            permission.required_permission = 'create_customer'
            
        elif self.action in ['list', 'retrieve']:
            permission.required_permission = 'view_customer'
            
        elif self.action in ['update', 'partial_update']:
            permission.required_permission = 'update_customer'
            
        elif self.action == 'destroy':
            permission.required_permission = 'delete_customer'
            
        return [IsAuthenticated(), permission]
    
    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        customer = serializer.save()

        response_serializer = CustomerReadSerializer(customer)
        
        create_logs(
            user=self.request.user,
            action='create',
            model_name='Customer',
            object_id=customer.id,
            description=f"Customer {customer.name} created successfully"
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )
        
    def perform_update(self, serializer):
        
        customer = serializer.save()
        
        create_logs(
            user=self.request.user,
            action='update',
            model_name='Customer',
            object_id=customer.id,
            description=f"Customer {customer.name} updated successfully"
        )
        
    def list(self, request, *args, **kwargs):
        
        response = super().list(request, *args, **kwargs)
        
        create_logs(
            user=self.request.user,
            action='list',
            model_name='Customer',
            description="Customer list viewe successfully"
        )
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        
        response = super().retrieve(request, *args, **kwargs)
        
        customer = self.get_object()
        
        create_logs(
            user=self.request.user,
            action='retrieve',
            model_name='Customer',
            object_id=customer.id,
            description=f"Customer {customer.name} details viewed successfully"
        )
        
        return response

class DeleteCustomerView(APIView):
    def post(self, request, pk):
        customer = Customer.objects.get(pk=pk)
        
        CustomerService.soft_delete(customer)
        
        create_logs(
            user=self.request.user,
            action='delete',
            model_name='Customer',
            object_id=customer.id,
            description=f"Customer {customer.name} deleted successfully"
        )
        
        return Response({
            'message': 'Customer deleted successfully'
        }, status=status.HTTP_200_OK)
        
class RestoreCustomerView(APIView):
    def post(self, request, pk):
        
        customer = Customer.deleted_objects.get(pk=pk)
        
        CustomerService.restore(customer)
        
        create_logs(
            user=self.request.user,
            action='restore',
            model_name='Customer',
            object_id=customer.id,
            description=f"Customer {customer.name} restored successfully"
        )
        
        return Response({
            'message': 'Customer restored successfully'
        }, status=status.HTTP_200_OK)