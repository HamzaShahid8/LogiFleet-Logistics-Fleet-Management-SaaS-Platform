from django.utils import timezone

class VehicleService:
    
    @staticmethod
    def soft_delete(vehicle):
        vehicle.is_deleted = True
        vehicle.save(
            update_fields = ['is_deleted']
        )
        
        return vehicle
    
    @staticmethod
    def restore(vehicle):
        vehicle.is_deleted = False
        vehicle.save(
            update_fields = ['is_deleted']
        )
        return vehicle