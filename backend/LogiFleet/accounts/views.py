from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, GoogleLoginSerializer
from .models import User
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .tasks import send_verification_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError, AccessToken
from django.contrib.auth.tokens import default_token_generator
from .permissions import *
from .throttles import RegisterRateThrottle, LoginRateThrottle
from .services import *
from activity_logs.models import ActivityLogs
from activity_logs.utils import create_logs
from django.db import connection
from django.core.cache import cache
from celery import current_app

# Create your views here.

class RegisterView(generics.ListCreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    throttle_classes = [RegisterRateThrottle]
    
    def perform_create(self, serializer):
        serializer.save()
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]
    
    def post(self, request):
        
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        user = authenticate(username = email, password = password)
        
        if user is None:
            return Response(
                {
                    'message': 'Invalid Credentials'
                }, status=status.HTTP_404_NOT_FOUND
            )
            
        if not user.is_email_verified:
            send_verification_email.delay(user.id)
            
            return Response({
                'message': 'Email sent'
            }, status=status.HTTP_200_OK)
            
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)
        
        create_logs(
            user=user,
            action='login',
            model_name='User',
            object_id=user.id,
            description=f"User {user.username} Logged in successfully"
        )
        
        response = Response({
            'message': 'Login successfully.',
            'user': {
                'username': user.username,
                'email': user.email
            },
        }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        return response
    
class RefreshTokenView(APIView):
    
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'message': 'Refresh token not found'
            }, status=status.HTTP_404_NOT_FOUND)
            
        refresh = RefreshToken(refresh_token)
        access_token = str(refresh.access_token)
        
        response = Response({
            'message': 'Token refreshed succesfully'
        }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        return response
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        user = self.request.user
        
        if not user.check_password(request.data['old_password']):
            return Response({
                'message': 'Password is incorrect'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        user.set_password(request.data['new_password'])
        user.save()
        return Response({
            'message': 'Password changed succesfully'
        }, status=status.HTTP_200_OK)
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        user = self.request.user
        
        create_logs(
            user=user,
            action='logout',
            model_name='User',
            object_id=user.id,
            description=f"User {user.username} Logged out successfully"
        )
        
        response = Response({
            'message': 'Logout successfully'
        }, status=status.HTTP_200_OK)
        
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        
        return response
    
class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        
        user_id = request.query_params.get('user_id')
        token = request.query_params.get('token')
        
        if not user_id or not token:
            return Response({
                'message': 'Invalid verification link'
            }, status=status.HTTP_404_NOT_FOUND)
            
        user = User.objects.get(id=user_id)
        
        if user.is_email_verified:
            return Response({
                'message': 'Email already verified'
            }, status=status.HTTP_200_OK)
            
        if not default_token_generator.check_token(user, token):
            return Response({
                'message': 'Invalid or expired token'
            }, status=status.HTTP_404_NOT_FOUND)
            
        user.is_email_verified = True
        user.save(update_fields=['is_email_verified'])
        
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        
        response = Response({
            'message': 'Email verified successfully'
        }, status=status.HTTP_200_OK)
        
        response.set_cookie(
            key='access_token',
            value=str(access_token),
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )      
        
        response.set_cookie(
            key='refresh_token',
            value=str(refresh_token),
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        return response
        
        
class DashboardView(APIView):
    permission_classes = [IsAuthenticated, IsEmailVerified]
    
    def get(self, request):
        user = self.request.user
        
        return Response({
            'message': f"Welcome {user.username} to our platform",
            'email': f"your email is: {user.email}"
        }, status=status.HTTP_200_OK)
        
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        result = GoogleAuthService.authenticate(token)
        
        response = Response(result['data'])
        
        response.set_cookie(
            key='access_token',
            value=result['access_token'],
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        response.set_cookie(
            key='refresh_token',
            value=result['refresh_token'],
            httponly=True,
            secure=False,
            samesite='Lax',
            path='/'
        )
        
        return response
    
class HealthyChecks(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        
        health = {
            'database': 'connected',
            'status': 'healthy',
            'redis': 'connected',
            'celery': 'running'
        }
        
        status_code = status.HTTP_200_OK
        
        # database check
        try:
            connection.ensure_connection()
        except Exception as e:
            health['status'] = 'unhealthy'
            health['database'] = str(e)
            
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        # redis check
        try:
            cache.set('health_check', 'ok', timeout=10)
            cache.get('health_check')
        except Exception as e:
            health['status'] = 'unhealthy'
            health['redis'] = str(e)
            
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        # celery check
        try:
            current_app.control.ping(timeout=10)
        except Exception as e:
            health['status'] = 'unhealthy'
            health['celery'] = str(e)
            
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            
        return Response(health, status=status_code)