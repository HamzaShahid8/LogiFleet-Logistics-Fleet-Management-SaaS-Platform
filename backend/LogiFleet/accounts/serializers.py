from rest_framework import serializers
from .models import User
from roles_permissions.models import Roles

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SlugRelatedField(queryset = Roles.objects.all(), slug_field='name')
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_email_verified', 'role']
        read_only_fields = ['password']
        
    def validate_email(self, email):
        if not email.endswith('@gmail.com'):
            raise serializers.ValidationError('Only gmail account allow')
        return email
        
    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        
        user = User.objects.create(
            **validated_data,
            role=role,
            is_email_verified=False,
        )
        user.set_password(password)
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class GoogleLoginSerializer(serializers.Serializer):
    token = serializers.CharField()