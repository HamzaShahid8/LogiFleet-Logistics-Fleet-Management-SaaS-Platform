from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('expenses', ExpenseViewSet, basename='expenses')

urlpatterns = [
    path('', include(router.urls)),
    path('expenses/<int:pk>/delete/', SoftDeleteView.as_view(), name = 'soft_delete'),
    path('expenses/<int:pk>/restore/', RestoreView.as_view(), name = 'restore'),
]