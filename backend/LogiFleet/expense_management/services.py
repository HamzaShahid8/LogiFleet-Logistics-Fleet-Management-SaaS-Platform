from django.utils import timezone

class ExpenseService:
    
    @staticmethod
    def soft_delete(expense):
        expense.is_deleted = True
        expense.save(update_fields = ['is_deleted'])
        return expense
    
    @staticmethod
    def restore(expense):
        expense.is_deleted = False
        expense.save(update_fields = ['is_deleted'])
        return expense