from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthenticationMiddleware:
    
    # yay app chlny pr shuru hoga
    def __init__(self, get_response):
        self.get_response = get_response
        
        self.public_paths = [
            '/register/',
            '/login/',
        ]
        
        # har request pr run hogi
        def __call__(self, request):
            
            if request.path in self.public_paths:
                request.user = AnonymousUser()
                return get_response(request)
            
            access_token = request.COOKIES.get('access_token')
            
            if access_token:
                try:
                    # token access token e h
                    validate_token = AccessToken(access_token)
                
                    # token may sy user id nikalygy
                    user_id = validate_token['user_id']
                
                    # database sy actual user nikalygy
                    user = User.objects.get(id=user_id)
                
                    # request ko user k sth attach krdengy
                    request.user = user
                
                except Exception as e:
                    # if token not found
                        request.user = AnonymousUser()
                        
            else:
                request.user = AnonymousUser()
                
            response = get_response(request)
            return response