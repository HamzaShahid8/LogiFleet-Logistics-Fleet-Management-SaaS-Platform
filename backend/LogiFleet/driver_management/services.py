from django.utils import timezone

class DriverService:
    
    @staticmethod
    def soft_delete(driver):
        driver.is_deleted = True
        driver.save(
            update_fields = ['is_deleted']
        )
        
        return driver
    
    
    @staticmethod
    def restore(driver):
        driver.is_deleted = False
        driver.save(
            update_fields = ['is_deleted']
        )
        
        return driver