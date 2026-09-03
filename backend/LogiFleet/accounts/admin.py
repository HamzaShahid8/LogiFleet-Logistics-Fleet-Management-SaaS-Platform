from django.contrib import admin
from .models import User


@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'is_email_verified',
        'created_at',
        'updated_at',
    )

    list_display_links = (
        'id',
        'username',
        'email',
    )

    list_filter = (
        'role',
        'is_email_verified',
        'created_at',
    )

    search_fields = (
        'username',
        'email',
        'role__name',
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Account Information', {
            'fields': (
                'username',
                'email',
                'password',
                'role',
            )
        }),

        ('Email Verification', {
            'fields': (
                'is_email_verified',
            )
        }),

        ('Timestamps', {
            'fields': (
                'created_at',
                'updated_at',
            )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'role',
                'is_email_verified',
            ),
        }),
    )