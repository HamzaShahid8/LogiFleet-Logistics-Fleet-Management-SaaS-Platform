from django.core.management import BaseCommand
from roles_permissions.models import Roles, Permissions

class Command(BaseCommand):
    help = 'Create permissions'
    
    def handle(self, *args, **kwargs):
        
        names = [
            'create_role',
            'update_role',
            'delete_role',
            'view_role',
            'create_permission',
            'update_permission',
            'delete_permission',
            'view_permission',
            'create_customer',
            'update_customer',
            'delete_customer',
            'view_customer',
            'create_driver',
            'update_driver',
            'delete_driver',
            'view_driver',
            'create_vehicle',
            'update_vehicle',
            'delete_vehicle',
            'view_vehicle',
            'create_shipment',
            'update_shipment',
            'delete_shipment',
            'view_shipment',
            'create_expense',
            'update_expense',
            'delete_expense',
            'view_expense',
            'create_shipment_charges',
            'update_shipment_charges',
            'delete_shipment_charges',
            'view_shipment_charges',
            'create_invoice',
            'update_invoice',
            'delete_invoice',
            'view_invoice',
            'create_payment',
            'update_payment',
            'delete_payment',
            'view_payment',
            'create_activity_logs',
            'update_activity_logs',
            'delete_activity_logs',
            'view_activity_logs',
        ]
        
        for name in names:
            permission, created = Permissions.objects.get_or_create(name=name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Permission: { name} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Permission: {name} already exists"))