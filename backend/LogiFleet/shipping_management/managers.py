from django.db import models

class ActiveShipmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedShipmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllShipmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
class ActiveShipmentChargeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedShipmentChargeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllShipmentChargeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()