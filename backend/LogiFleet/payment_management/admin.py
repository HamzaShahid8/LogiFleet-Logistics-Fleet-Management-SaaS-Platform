from django.contrib import admin
from .models import Payment, IdempotancyKey


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "code",
        "payment_number",
        "invoice__invoice_number",
        "customer__name",
        "amount",
        "payment_method",
        "payment_date",
        "status",
        "is_deleted",
        "created_at",
    ]

    list_display_links = [
        "id",
        "payment_number",
    ]

    list_filter = [
        "payment_method",
        "status",
        "is_deleted",
        "payment_date",
        "created_at",
    ]

    search_fields = [
        "payment_number",
        "invoice__invoice_number",
        "customer__name",
        "customer__email",
        "reference_number",
    ]

    ordering = [
        "-created_at",
    ]

    date_hierarchy = "payment_date"

    readonly_fields = [
        "id",
        "code",
        "payment_number",
        "payment_date",
        "created_at",
        "updated_at",
    ]

    autocomplete_fields = [
        "invoice",
        "customer",
    ]

    list_select_related = [
        "invoice",
        "customer",
    ]

    list_per_page = 25
    
    actions = ['soft_delete', 'restore']
    
    @admin.action(description='Soft delete')
    def soft_delete(self, request, queryset):
        queryset.update(is_deleted = True)
        
    @admin.action(description='Restore')
    def restore(self, request, queryset):
        queryset.update(is_deleted = False)


@admin.register(IdempotancyKey)
class IdempotancyKeyAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "key",
        "user",
        "status_code",
        "created_at",
    ]

    list_display_links = [
        "id",
        "key",
    ]

    list_filter = [
        "status_code",
        "created_at",
    ]

    search_fields = [
        "key",
        "user__email",
    ]

    ordering = [
        "-created_at",
    ]

    date_hierarchy = "created_at"

    readonly_fields = [
        "id",
        "key",
        "user",
        "response_data",
        "status_code",
        "created_at",
    ]

    list_select_related = [
        "user",
    ]

    list_per_page = 25