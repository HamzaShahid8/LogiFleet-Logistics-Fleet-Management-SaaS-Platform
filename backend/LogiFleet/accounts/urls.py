from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    ChangePasswordView,
    LogoutView,
    VerifyEmailView,
    DashboardView,
    GoogleLoginView,
    HealthyChecks,
)


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('healthy_check/', HealthyChecks.as_view(), name = 'healthy_check'),
]