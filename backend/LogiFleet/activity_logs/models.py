from django.db import models
from accounts.models import User
from django.db.models import DateTimeField

# Create your models here.

class ActivityLogs(models.Model):
    
    ACTION_STATUS = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('view', 'View'),
        ('assign', 'Assign'),
        ('change status', 'Change Status'),
        ('confirm delivery', 'Confirm Delivery'),
        ('failure', 'Failure'),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('restore', 'Restore'),
        ('payment', 'Payment'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activityLogs')
    action = models.CharField(max_length=20, choices=ACTION_STATUS, null=True, blank=True)
    model_name = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    object_id = models.CharField(max_length=20, null=True, blank=True, db_index=True)
    description = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['-id']