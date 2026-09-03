from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('invoice', InvoiceViewSet, basename='invoice')

urlpatterns = router.urls