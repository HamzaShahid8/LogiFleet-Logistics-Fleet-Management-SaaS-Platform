from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, PermissionViewSet

router = DefaultRouter()

router.register('roles', RoleViewSet, basename='roles')
router.register('permissions', PermissionViewSet, basename='permissions')

urlpatterns = router.urls