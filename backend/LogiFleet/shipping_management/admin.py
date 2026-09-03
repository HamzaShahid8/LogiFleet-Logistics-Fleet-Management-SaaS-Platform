from django.contrib import admin

from .models import (
    Shipment,
    ShipmentStatusHistory,
    ShipmentCharge,
    IdempotancyKey,
)


class ShipmentStatusHistoryInline(admin.TabularInline):

    model = ShipmentStatusHistory

    extra = 0
    can_delete = False

    fields = (
        "old_status",
        "new_status",
        "changed_by",
        "note",
        "created_at",
    )

    readonly_fields = (
        "old_status",
        "new_status",
        "changed_by",
        "note",
        "created_at",
    )

    ordering = ("-created_at",)


class ShipmentChargeInline(admin.TabularInline):

    model = ShipmentCharge

    extra = 0

    fields = (
        "code",
        "charge_type",
        "amount",
        "description",
        "is_deleted",
        "created_at",
    )

    readonly_fields = (
        "code",
        "created_at",
    )

    ordering = ("-created_at",)


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'code',
        "shipment_number",
        "customer_name",
        "driver_name",
        "vehicle_name",
        'priority',
        "pickup_city",
        "delivery_city",
        "pickup_date",
        "estimated_delivery_date",
        "created_at",
    )

    list_filter = (
        "status",
        "is_deleted",
        'priority',
        "pickup_city",
        "delivery_city",
        "created_at",
        "pickup_date",
        "estimated_delivery_date",
    )

    search_fields = (
        'id',
        'code',
        "shipment_number",
        "customer__name",
        "driver__full_name",
        "vehicle__registration_number",
        'priority',
        "pickup_address",
        "delivery_address",
        "pickup_city",
        "delivery_city",
        "receiver_name",
        "receiver_phone",
        "failure_reason",
    )

    autocomplete_fields = (
        "customer",
        "driver",
        "vehicle",
    )

    readonly_fields = (
        "id",
        "code",
        "actual_delivery_date",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "customer",
        "driver",
        "vehicle",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_per_page = 25

    save_on_top = True

    inlines = (
        ShipmentStatusHistoryInline,
        ShipmentChargeInline,
    )

    actions = (
        "soft_delete_shipments",
        "restore_shipments",
    )

    fieldsets = (
        (
            "Shipment Information",
            {
                "fields": (
                    "id",
                    "code",
                    "shipment_number",
                    "status",
                    "priority",
                )
            },
        ),

        (
            "Assignment",
            {
                "fields": (
                    "customer",
                    "driver",
                    "vehicle",
                )
            },
        ),

        (
            "Pickup Information",
            {
                "fields": (
                    "pickup_address",
                    "pickup_city",
                    "pickup_date",
                )
            },
        ),

        (
            "Delivery Information",
            {
                "fields": (
                    "delivery_address",
                    "delivery_city",
                    "estimated_delivery_date",
                    "actual_delivery_date",
                )
            },
        ),

        (
            "Package Information",
            {
                "fields": (
                    "package_description",
                    "weight",
                    "quantity",
                )
            },
        ),

        (
            "Receiver Information",
            {
                "fields": (
                    "receiver_name",
                    "receiver_phone",
                    "delivery_notes",
                    "failure_reason",
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
                )
            },
        ),
    )

    @admin.display(
        description="Customer",
        ordering="customer__name"
    )
    def customer_name(self, obj):
        return obj.customer.name

    @admin.display(
        description="Driver",
        ordering="driver__full_name"
    )
    def driver_name(self, obj):

        if obj.driver:
            return obj.driver.full_name

        return "-"

    @admin.display(
        description="Vehicle",
        ordering="vehicle__registration_number"
    )
    def vehicle_name(self, obj):

        if obj.vehicle:
            return obj.vehicle.registration_number

        return "-"

    @admin.action(
        description="Soft delete selected shipments"
    )
    def soft_delete_shipments(self, request, queryset):
        queryset.update(is_deleted = True)

    @admin.action(
        description="Restore selected shipments"
    )
    def restore_shipments(self, request, queryset):
        queryset.update(is_deleted = False)

@admin.register(ShipmentStatusHistory)
class ShipmentStatusHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "shipment_number",
        "old_status",
        "new_status",
        "changed_by",
        "note",
        "created_at",
    )

    list_filter = (
        "old_status",
        "new_status",
        "created_at",
    )

    search_fields = (
        "shipment__shipment_number",
        "changed_by__email",
        "note",
    )

    list_select_related = (
        "shipment",
        "changed_by",
    )

    readonly_fields = (
        "id",
        "code",
        "shipment",
        "old_status",
        "new_status",
        "changed_by",
        "note",
        "created_at",
        "updated_at",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(
        description="Shipment",
        ordering="shipment__shipment_number"
    )
    def shipment_number(self, obj):
        return obj.shipment.shipment_number


@admin.register(ShipmentCharge)
class ShipmentChargeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "code",
        "shipment_number",
        "amount",
        "description",
        "created_at",
    )

    list_filter = (
        "charge_type",
        "is_deleted",
        "created_at",
    )

    search_fields = (
        "id",
        "code",
        "shipment__shipment_number",
        "description",
    )

    autocomplete_fields = (
        "shipment",
    )

    readonly_fields = (
        "id",
        "code",
        "created_at",
        "updated_at",
    )

    list_select_related = (
        "shipment",
    )

    date_hierarchy = "created_at"

    ordering = (
        "-created_at",
    )

    list_per_page = 50

    @admin.display(
        description="Shipment",
        ordering="shipment__shipment_number"
    )
    def shipment_number(self, obj):
        return obj.shipment.shipment_number

    actions = (
        "soft_delete_charges",
        "restore_charges",
    )

    @admin.action(
        description="Soft delete selected charges"
    )
    def soft_delete_charges(self, request, queryset):
        queryset.update(is_deleted = True)

    @admin.action(
        description="Restore selected charges"
    )
    def restore_charges(self, request, queryset):
        queryset.update(is_deleted = False)
        
        
@admin.register(IdempotancyKey)
class IdempotancyKeyAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "key",
        "user",
        "status_code",
        "created_at",
    )

    search_fields = (
        "key",
        "user__email",
    )

    list_filter = (
        "status_code",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "response_data",
    )

    ordering = (
        "-created_at",
    )

    list_per_page = 25