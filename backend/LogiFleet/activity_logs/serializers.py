from rest_framework import serializers
from .models import ActivityLogs


class ActivityLogReadSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = ActivityLogs
        fields = [
            'id',
            'user',
            'username',
            'action',
            'model_name',
            'object_id',
            'description',
            'timestamp',
        ]


class ActivityLogWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ActivityLogs
        fields = [
            'action',
            'model_name',
            'object_id',
            'description',
        ]