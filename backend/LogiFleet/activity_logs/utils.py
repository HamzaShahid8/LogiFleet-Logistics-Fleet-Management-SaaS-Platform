from .models import ActivityLogs

def create_logs(user, action, model_name=None, object_id=None, description=None):
    
    if not user or not user.is_authenticated:
        return None
    
    return ActivityLogs.objects.create(
        user=user,
        action=action,
        model_name=model_name,
        object_id=str(object_id) if object_id else None,
        description=description
    )