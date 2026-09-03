from .models import Roles, Permissions

def has_permission(user, permission_name):
    
    if not user.is_authenticated:
        return False
    
    if user.is_superuser:
        return True
    
    role = user.role
    
    if role is None:
        return False
    
    return role.permissions.filter(name = permission_name).exists()