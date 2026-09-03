from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

class GoogleAuthService:
    
    @staticmethod
    @transaction.atomic
    def authenticate(google_token):
        
        payload = id_token.verify_oauth2_token(
            google_token,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID,
        )
        
        if not payload.get('email_verified', False):
            raise AuthenticationFailed('Email not found')
        
        email = payload['email']
        first_name = payload.get('given_name', '')
        last_name = payload.get('family_name', '')
        picture = payload.get('picture', '')
        
        user, created = User.objects.get_or_create(
            email=email,
            defaults = {
                'first_name': first_name,
                'last_name': last_name,
                'is_email_verified': True
            },
        )
        
        if not created:
            
            updated = False
            
            if not user.is_email_verified:
                user.is_email_verified = True
                updated = True
            
            if first_name and user.first_name != first_name:
                user.first_name = first_name
                updated = True
                
            if last_name and user.last_name != last_name:
                user.last_name = last_name
                updated = True
                
            if updated:
                user.save(
                    update_fields=[
                        'is_email_verified',
                        'first_name',
                        'last_name',
                    ]
                )
                
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        
        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": str(refresh_token),
            "data": {
                "message": "Google login successful.",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "picture": picture,
                },
            },
        }