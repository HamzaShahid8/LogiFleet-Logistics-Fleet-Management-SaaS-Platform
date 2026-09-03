from django.utils import timezone
from django.db import transaction
from .models import Shipment, ShipmentStatusHistory, ShipmentCharge
from django.core.exceptions import ValidationError
from .validators import *
from invoice_management.services import *
from .models import IdempotancyKey
from .serializers import *

class ShippingService:
    
    @staticmethod
    def soft_delete(shipping):
        shipping.is_deleted = True
        shipping.save(
            update_fields = ['is_deleted']
        )
        return shipping
    
    @staticmethod
    def restore(shipping):
        shipping.is_deleted = False
        shipping.save(update_fields = ['is_deleted'])
        return shipping

    @staticmethod
    @transaction.atomic
    def create_shipment(validated_data, user, idempotency_key):
        
        existing = IdempotancyKey.objects.filter(
            user=user,
            key=idempotency_key
        ).first()
        
        if existing:
            return existing.response_data, existing.status_code
        
        charges = validated_data.pop('charges', [])

        shipment = Shipment.objects.create(
            **validated_data
        )
        
        ShipmentCharge.objects.bulk_create(
            [
                ShipmentCharge(
                    shipment=shipment,
                    **charge
                )
                for charge in charges
            ]
        )

        ShipmentStatusHistory.objects.create(
            shipment=shipment,
            old_status="",
            new_status=shipment.status,
            changed_by=user,
            note="Shipment created."
        )
        
        InvoiceService.calculate_invoice(shipment)
        
        response_data = ShipmentReadSerializer(shipment).data
        
        IdempotancyKey.objects.create(
            user=user,
            key=idempotency_key,
            response_data=response_data,
            status_code=201
        )
        
        return response_data, 201
    
    @staticmethod
    @transaction.atomic
    def assign_shipment(shipment, driver, vehicle, user):
        
        if shipment.status != 'pending':
            raise ValidationError('Only pending shipment can be assigned')
        
        shipment.driver = driver
        shipment.vehicle = vehicle
        shipment.status = 'assigned'
        
        shipment.save(update_fields = [
            'driver',
            'vehicle',
            'status', 
            'updated_at'
        ])
        
        ShipmentStatusHistory.objects.create(
            shipment=shipment,
            old_status='pending',
            new_status='assigned',
            changed_by=user,
            note='Driver and vehicle assigned.'
        )
        
        return shipment
    
    @staticmethod
    @transaction.atomic
    def change_status(shipment, new_status, user, note):
        
        old_status = shipment.status
        
        validate_status_transition(old_status, new_status)
        
        shipment.status = new_status
        
        shipment.save(update_fields = [
            'status',
            'updated_at'
        ])
        
        ShipmentStatusHistory.objects.create(
            shipment=shipment,
            old_status=old_status,
            new_status=new_status,
            changed_by=user,
            note=note
        )
        
        return shipment
    
    @staticmethod
    @transaction.atomic
    def confirm_delivery(shipment, user, receiver_name='', receiver_phone='', delivery_notes=''):
        
        validate_delivery_confirmation(shipment)
        
        old_status = shipment.status
        
        shipment.status = 'delivered'
        shipment.receiver_name = receiver_name
        shipment.receiver_phone = receiver_phone
        shipment.delivery_notes = delivery_notes
        shipment.actual_delivery_date = timezone.now()
        
        
        shipment.save(update_fields = [
            'status',
            'receiver_name',
            'receiver_phone',
            'delivery_notes',
            'actual_delivery_date'
        ])
        
        ShipmentStatusHistory.objects.create(
            shipment=shipment,
            old_status=old_status,
            new_status='delivered',
            changed_by=user,
            note=delivery_notes
        )
        
        return shipment
    
    @staticmethod
    @transaction.atomic
    def fail_shipment(shipment, user, failure_reason):
        
        validate_failure_reason(failure_reason)
        
        old_status = shipment.status
        
        if old_status not in [
            "assigned",
            "picked_up",
            "in_transit",
            "out_for_delivery",
        ]:
            raise ValidationError("Shipment cannot be marked as failed "
            "from its current status.")
        
        shipment.status = 'failed'
        shipment.failure_reason = failure_reason
        
        shipment.save(update_fields = ['status', 'failure_reason', 'updated_at'])
        
        ShipmentStatusHistory.objects.create(
            shipment=shipment,
            old_status=old_status,
            new_status='failed',
            changed_by=user,
            note=failure_reason
        )
        
        return shipment