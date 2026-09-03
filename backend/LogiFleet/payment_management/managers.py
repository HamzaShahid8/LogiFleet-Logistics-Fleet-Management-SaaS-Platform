from django.db import models

class ActivePaymentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedPaymentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllPaymentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()