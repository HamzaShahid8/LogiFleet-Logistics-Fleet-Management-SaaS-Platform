from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ActivityLogsViewSet

router = DefaultRouter()

router.register('activity_logs', ActivityLogsViewSet, basename='activity_logs')

urlpatterns = router.urls