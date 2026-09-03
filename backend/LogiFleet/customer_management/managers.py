from django.db import models

class ActiveCustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedCustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllCustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()