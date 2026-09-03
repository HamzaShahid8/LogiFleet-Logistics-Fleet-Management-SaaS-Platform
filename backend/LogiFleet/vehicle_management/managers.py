from django.db import models

class ActiveVehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedVehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllVehicleManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()