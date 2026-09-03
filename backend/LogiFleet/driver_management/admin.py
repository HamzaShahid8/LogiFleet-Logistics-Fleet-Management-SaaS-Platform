from django.contrib import admin
from .models import Driver


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):

    # List page
    list_display = (
        'code',
        'full_name',
        'email',
        'phone',
        'license_number',
        'license_type',
        'license_expiry',
        'joining_date',
        'status',
        'is_deleted',
        'created_at',
    )

    # Sidebar filters
    list_filter = (
        'status',
        'license_type',
        'is_deleted',
        'joining_date',
        'license_expiry',
        'created_at',
    )

    # Search box
    search_fields = (
        'code',
        'full_name',
        'email',
        'phone',
        'license_number',
    )

    # Default ordering
    ordering = ('-created_at',)

    # Pagination
    list_per_page = 25

    # Read-only fields
    readonly_fields = (
        'id',
        'code',
        'created_at',
        'updated_at',
    )

    # Form layout
    fieldsets = (
        (
            'Driver Information',
            {
                'fields': (
                    'full_name',
                    'email',
                    'phone',
                )
            },
        ),
        (
            'License Information',
            {
                'fields': (
                    'license_number',
                    'license_type',
                    'license_expiry',
                )
            },
        ),
        (
            'Employment Information',
            {
                'fields': (
                    'joining_date',
                    'status',
                )
            },
        ),
        (
            'Contact Information',
            {
                'fields': (
                    'address',
                    'emergency_contact',
                )
            },
        ),
        (
            'System Information',
            {
                'fields': (
                    'id',
                    'code',
                    'is_deleted',
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )

    actions = ['soft_delete', 'restore']
    
    def get_queryset(self, request):
        return Driver.all_objects.all()
    
    @admin.action(description='Soft Delete manager')
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted = True)
        
    @admin.action(description='Restore manager')
    def restore(self, request, queryset):
        queryset.update(is_deleted = False)