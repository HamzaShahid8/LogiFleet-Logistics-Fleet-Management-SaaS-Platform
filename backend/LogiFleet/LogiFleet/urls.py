"""
URL configuration for LogiFleet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # apps
    path('api/accounts/', include('accounts.urls')),
    path('api/roles_permissions/', include('roles_permissions.urls')),
    path('api/customers/', include('customer_management.urls')),
    path('api/drivers/', include('driver_management.urls')),
    path('api/vehicles/', include('vehicle_management.urls')),
    path('api/shipping/', include('shipping_management.urls')),
    path('api/expense/', include('expense_management.urls')),
    path('api/invoice/', include('invoice_management.urls')),
    path('api/payment/', include('payment_management.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('api/activity_logs/', include('activity_logs.urls')),
    
    # swagger
    path('api/schema/', SpectacularAPIView.as_view(), name = 'schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name = 'schema'), name = 'swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name = 'schema'), name = 'redoc-ui'),
]