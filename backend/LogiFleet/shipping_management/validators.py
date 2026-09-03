from django.core.exceptions import ValidationError


ALLOWED_STATUS_TRANSITIONS = {
    "pending": ["assigned", "cancelled"],
    "assigned": ["picked_up", "cancelled"],
    "picked_up": ["in_transit", "failed"],
    "in_transit": ["out_for_delivery", "failed"],
    "out_for_delivery": ["delivered", "failed"],
    "delivered": [],
    "failed": [],
    "cancelled": [],
}


def validate_status_transition(old_status, new_status):

    if old_status == new_status:
        raise ValidationError(
            "Shipment is already in this status."
        )

    allowed_statuses = ALLOWED_STATUS_TRANSITIONS.get(
        old_status,
        []
    )

    if new_status not in allowed_statuses:
        raise ValidationError(
            f"Invalid status transition: "
            f"{old_status} → {new_status}."
        )


def validate_weight(weight):

    if weight <= 0:
        raise ValidationError(
            "Weight must be greater than zero."
        )


def validate_quantity(quantity):

    if quantity < 1:
        raise ValidationError(
            "Quantity must be at least 1."
        )


def validate_shipment_dates(
    pickup_date,
    estimated_delivery_date
):

    if estimated_delivery_date < pickup_date:
        raise ValidationError(
            "Estimated delivery date cannot be "
            "before pickup date."
        )


def validate_delivery_confirmation(shipment):

    if shipment.status != "out_for_delivery":
        raise ValidationError(
            "Only out-for-delivery shipments "
            "can be delivered."
        )


def validate_failure_reason(reason):

    if not reason or not reason.strip():
        raise ValidationError(
            "Failure reason is required."
        )