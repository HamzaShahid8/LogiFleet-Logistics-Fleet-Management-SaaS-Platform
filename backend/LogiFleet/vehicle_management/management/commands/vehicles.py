from django.core.management import BaseCommand
from vehicle_management.models import Vehicle

class Command(BaseCommand):
    help = 'Create vehicles.'
    
    def handle(self, *args, **kwargs):
        VEHICLES = [
            ("LEA-1234", "1HGCM82633A123456", "car", "Toyota", "Corolla", 2023, 5.00, "petrol", 15000, "available", "2023-05-10"),
            ("LEB-5678", "1HGCM82633A234567", "car", "Honda", "Civic", 2022, 5.00, "petrol", 22000, "available", "2022-08-15"),
            ("LEC-9012", "1HGCM82633A345678", "van", "Toyota", "HiAce", 2021, 1200.00, "diesel", 45000, "assigned", "2021-03-20"),
            ("LED-3456", "1HGCM82633A456789", "truck", "Isuzu", "NPR", 2020, 3000.00, "diesel", 68000, "maintenance", "2020-07-12"),
            ("LEE-7890", "1HGCM82633A567890", "bike", "Honda", "CB 150F", 2024, 1.50, "petrol", 5000, "available", "2024-02-18"),
            ("LEF-2345", "1HGCM82633A678901", "car", "Suzuki", "Swift", 2023, 5.00, "petrol", 12000, "available", "2023-09-05"),
            ("LEG-6789", "1HGCM82633A789012", "trailer", "Hino", "Trailer X", 2019, 5000.00, "diesel", 90000, "inactive", "2019-04-25"),
            ("LEH-0123", "1HGCM82633A890123", "car", "KIA", "Sportage", 2022, 7.00, "hybrid", 18000, "assigned", "2022-11-10"),
            ("LEI-4567", "1HGCM82633A901234", "van", "Nissan", "NV200", 2021, 800.00, "petrol", 35000, "available", "2021-06-15"),
            ("LEJ-8901", "1HGCM82633A012345", "truck", "Mitsubishi", "Fuso", 2020, 4000.00, "diesel", 72000, "available", "2020-10-20"),
        ]
        
        for registration_number, vin, vehicle_type, make, model, year, capacity, fuel_type, current_mileage, status, purchase_date in VEHICLES:
            Vehicle.objects.get_or_create(
                registration_number=registration_number,
                defaults = {
                    'vin': vin,
                    'vehicle_type': vehicle_type,
                    'make': make,
                    'model': model,
                    'year': year,
                    'capacity': capacity,
                    'fuel_type': fuel_type,
                    'current_mileage': current_mileage,
                    'status': status,
                    'purchase_date': purchase_date,
                }
            )
            self.stdout.write(self.style.SUCCESS('Vehicles created succesfully.'))