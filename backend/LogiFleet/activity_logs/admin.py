from django.contrib import admin
from .models import ActivityLogs


@admin.register(ActivityLogs)
class ActivityLogsAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'action',
        'model_name',
        'object_id',
        'description_short',
        'timestamp',
    )

    list_filter = (
        'action',
        'model_name',
        'timestamp',
    )

    search_fields = (
        'user__email',
        'user__username',
        'model_name',
        'object_id',
        'description',
    )

    readonly_fields = (
        'user',
        'action',
        'model_name',
        'object_id',
        'description',
        'timestamp',
    )

    date_hierarchy = 'timestamp'

    ordering = (
        '-timestamp',
        '-id',
    )

    list_per_page = 50

    list_select_related = (
        'user',
    )

    def description_short(self, obj):
        if not obj.description:
            return '-'

        return (
            obj.description[:80] + '...'
            if len(obj.description) > 80
            else obj.description
        )

    description_short.short_description = 'Description'