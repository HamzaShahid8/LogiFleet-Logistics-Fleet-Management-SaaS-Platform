from django.db import models

class ActiveExpenseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedExpenseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllExpenseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()