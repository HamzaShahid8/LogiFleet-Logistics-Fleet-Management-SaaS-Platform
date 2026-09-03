from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        "code",
        "name",
        "email",
        "phone",
        "city",
        "country",
        "credit_limit",
        "is_deleted",
        "created_at",
    )


    search_fields = (
        'id',
        "code",
        "name",
        "email",
        "phone",
        "tax_number",
    )


    list_filter = (
        "is_deleted",
        "city",
        "country",
        "created_at",
    )


    ordering = (
        "-created_at",
    )


    readonly_fields = (
        'id',
        "code",
        "created_at",
        "updated_at",
    )


    fieldsets = (
        (
            "Customer Information",
            {
                "fields": (
                    'id',
                    "code",
                    "name",
                    "email",
                    "phone",
                )
            },
        ),

        (
            "Address Information",
            {
                "fields": (
                    "address",
                    "city",
                    "country",
                )
            },
        ),

        (
            "Financial Information",
            {
                "fields": (
                    "tax_number",
                    "credit_limit",
                )
            },
        ),

        (
            "Status",
            {
                "fields": (
                    "is_deleted",
                )
            },
        ),

        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    
    actions = ["soft_delete", "restore"]
    
    def get_queryset(self, request):
        return Customer.all_objects.all()

    @admin.action(description="Soft Delete Selected Customers")
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted=True)

    @admin.action(description="Restore Selected Customers")
    def restore(self, request, queryset):
        queryset.update(is_deleted=False)