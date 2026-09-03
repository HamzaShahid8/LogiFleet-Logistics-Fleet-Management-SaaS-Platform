from django.core.management import BaseCommand
from roles_permissions.models import Roles

class Command(BaseCommand):
    help = 'Create roles'
    
    def handle(self, *args, **kwargs):
        
        names = [
            'Company_Admin',
            'Operations_Manager',
            'Fleet_Manager',
            'Accountant',
            'Dispatcher',
            'Driver',
        ]
        
        for name in names:
            role, created = Roles.objects.get_or_create(name=name)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f"Role: { name} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Role: {name} already exists"))