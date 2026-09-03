from django.contrib import admin
from .models import Invoice


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):

    list_display = [
        "code",
        "invoice_number",
        "customer",
        "shipment",
        "issue_date",
        "due_date",
        "subtotal",
        "total_amount",
        "paid_amount",
        "status",
        "is_deleted",
        "created_at",
    ]

    list_filter = [
        "status",
        "is_deleted",
        "issue_date",
        "due_date",
        "created_at",
    ]

    search_fields = [
        "invoice_number",
        "code",
        "customer__name",
        "shipment__shipment_number",
    ]

    ordering = [
        "-created_at",
    ]

    readonly_fields = [
        "code",
        "invoice_number",
        "customer",
        "shipment",
        "issue_date",
        "subtotal",
        "total_amount",
        "paid_amount",
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Invoice Information",
            {
                "fields": (
                    "code",
                    "invoice_number",
                    "customer",
                    "shipment",
                )
            },
        ),
        (
            "Billing",
            {
                "fields": (
                    "issue_date",
                    "due_date",
                    "subtotal",
                    "total_amount",
                    "paid_amount",
                )
            },
        ),
        (
            "Status",
            {
                "fields": (
                    "status",
                    "is_deleted",
                )
            },
        ),
        (
            "Additional Information",
            {
                "fields": (
                    "notes",
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

    actions = [
        "soft_delete_invoices",
        "restore_invoices",
    ]

    @admin.action(description="Soft delete selected invoices")
    def soft_delete_invoices(self, request, queryset):
        queryset.update(is_deleted = True)

    @admin.action(description="Restore selected invoices")
    def restore_invoices(self, request, queryset):
        queryset.update(is_deleted = False)