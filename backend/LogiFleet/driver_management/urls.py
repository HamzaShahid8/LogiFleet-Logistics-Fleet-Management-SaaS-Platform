from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include

router = DefaultRouter()

router.register('drivers', DriverViewSet, basename='drivers')

urlpatterns = router.urls