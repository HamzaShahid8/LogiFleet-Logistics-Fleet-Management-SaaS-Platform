from django.db import models


class ActiveInvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = False)
    
class DeletedInvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted = True)
    
class AllInvoiceManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()