from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True


class User(AbstractUser, BaseModel):
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    role = models.ForeignKey('roles_permissions.Roles', on_delete=models.CASCADE, null=True, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.username} - {self.email}"