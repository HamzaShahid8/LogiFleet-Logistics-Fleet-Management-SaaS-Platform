from django.contrib import admin
from .models import Permissions, Roles


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'name',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

    ordering = (
        '-id',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    list_per_page = 25

    fieldsets = (
        ('Permission Information', {
            'fields': (
                'name',
            )
        }),
        ('Audit Information', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )


@admin.register(Roles)
class RolesAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'count_permissions',
        'created_at',
        'updated_at',
    )

    search_fields = (
        'name',
        'permissions__name',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

    filter_horizontal = (
        'permissions',
    )

    ordering = (
        '-id',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    list_per_page = 25

    fieldsets = (
        ('Role Information', {
            'fields': (
                'name',
                'permissions',
            )
        }),
        ('Audit Information', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',),
        }),
    )

    @admin.display(description='Permissions')
    def count_permissions(self, obj):
        return obj.permissions.count()