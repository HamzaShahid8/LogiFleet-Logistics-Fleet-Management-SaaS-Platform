from django.contrib import admin
from django.utils import timezone
from django.contrib import messages
from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        "code",
        "expense_type",
        "shipment",
        "driver",
        "vehicle",
        "amount",
        "payment_method",
        "expense_date",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        'id',
        "code",
        "receipt_number",
        "description",
        "shipment__shipment_number",
        "driver__full_name",
        "vehicle__registration_number",
    )

    list_filter = (
        "expense_type",
        "payment_method",
        "is_deleted",
        "expense_date",
        "created_at",
    )

    date_hierarchy = "expense_date"


    ordering = ("-expense_date",)

   
    list_per_page = 25

   
    list_select_related = (
        "shipment",
        "driver",
        "vehicle",
    )

    
    readonly_fields = (
        'id',
        "code",
        "created_at",
        "updated_at",
    )

    
    fieldsets = (
        (
            "Expense Information",
            {
                "fields": (
                    'id',
                    "code",
                    "expense_type",
                    "amount",
                    "payment_method",
                    "expense_date",
                )
            },
        ),
        (
            "Relations",
            {
                "fields": (
                    "shipment",
                    "driver",
                    "vehicle",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "description",
                    "receipt_number",
                )
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "is_deleted",
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    
    actions = [
        "soft_delete_expenses",
        "restore_expenses",
    ]

    @admin.action(description="Soft delete selected expenses")
    def soft_delete_expenses(self, request, queryset):
        queryset.update(is_deleted = True)

    @admin.action(description="Restore selected expenses")
    def restore_expenses(self, request, queryset):
        queryset.update(is_deleted = False)