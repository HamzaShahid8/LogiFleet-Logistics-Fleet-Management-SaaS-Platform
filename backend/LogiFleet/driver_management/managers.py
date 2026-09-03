from django.db import models

class ActiveDriverManagement(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedDriverManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllDriverManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()