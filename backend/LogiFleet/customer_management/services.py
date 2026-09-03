from django.utils import timezone

class CustomerService:
    
    @staticmethod
    def soft_delete(customer):
        customer.is_deleted = True
        
        customer.save(
            update_fields=[
                'is_deleted'
            ]
        )
        return customer
    
    @staticmethod
    def restore(customer):
        customer.is_deleted = False
        
        customer.save(
            update_fields=['is_deleted']
        )
        return customer