from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ShipmentViewSet,
    ShipmentAssignView,
    ChangeStatusView,
    ConfirmDeliveryView,
    FailureView,
    SoftDeleteView,
    RestoreView,
)


router = DefaultRouter()

router.register(
    "shipments",
    ShipmentViewSet,
    basename="shipments"
)


urlpatterns = [
    
    # Shipment CRUD
    path(
        "",
        include(router.urls)
    ),

    # Assign shipment
    path(
        "shipments/<int:pk>/assign/",
        ShipmentAssignView.as_view(),
        name="shipment-assign"
    ),

    # Change shipment status
    path(
        "shipments/<int:pk>/status/",
        ChangeStatusView.as_view(),
        name="shipment-status"
    ),

    # Confirm delivery
    path(
        "shipments/<int:pk>/delivery/",
        ConfirmDeliveryView.as_view(),
        name="shipment-delivery"
    ),

    # Mark shipment as failed
    path(
        "shipments/<int:pk>/fail/",
        FailureView.as_view(),
        name="shipment-fail"
    ),

    # Soft delete
    path(
        "shipments/<int:pk>/delete/",
        SoftDeleteView.as_view(),
        name="shipment-delete"
    ),

    # Restore
    path(
        "shipments/<int:pk>/restore/",
        RestoreView.as_view(),
        name="shipment-restore"
    ),
]