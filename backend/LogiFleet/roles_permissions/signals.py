from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Roles

@receiver(post_migrate)
def assign_panel(sender, **kwargs):
    for role in Roles.objects.filter(name__in=['Company_Admin', 'Operations_Manager', 'Fleet_Manager', 'Accountant',]):
        Group.objects.create(name=role.name)