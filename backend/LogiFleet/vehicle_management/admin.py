from django.contrib import admin

from .models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):

    list_display = [
        'code',
        'registration_number',
        'vin',
        'make',
        'model',
        'vehicle_type',
        'fuel_type',
        'capacity',
        'current_mileage',
        'status',
        'is_deleted',
        'created_at',
    ]

    list_filter = [
        'vehicle_type',
        'fuel_type',
        'status',
        'is_deleted',
        'purchase_date',
    ]

    search_fields = [
        'code',
        'registration_number',
        'vin',
        'make',
        'model',
    ]

    ordering = [
        '-created_at',
    ]

    readonly_fields = [
        'code',
        'created_at',
        'updated_at',
    ]

    list_per_page = 25

    fieldsets = (
        (
            'Vehicle Information',
            {
                'fields': (
                    'code',
                    'registration_number',
                    'vin',
                    'vehicle_type',
                    'make',
                    'model',
                    'year',
                )
            },
        ),
        (
            'Vehicle Specifications',
            {
                'fields': (
                    'capacity',
                    'fuel_type',
                    'current_mileage',
                )
            },
        ),
        (
            'Status & Purchase',
            {
                'fields': (
                    'status',
                    'purchase_date',
                )
            },
        ),
        (
            'Soft Delete',
            {
                'fields': (
                    'is_deleted',
                )
            },
        ),
        (
            'Timestamps',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )
    
    actions = ['soft_delete', 'restore']
    
    def get_queryset(self, request):
        return Vehicle.all_objects.all()
    
    @admin.action(description='Soft delete vehicle')
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted = True)
        
    @admin.action(description='Restore vehicle')
    def restore(self, request, queryset):
        queryset.update(is_deleted = False)