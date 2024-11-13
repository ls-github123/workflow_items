# 自定义令牌的生成和载荷
from typing import Any, Dict
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    自定义 TokenObtainPairSerializer, 添加额外的用户信息到令牌载荷中。
    """
    
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """
        验证用户凭据并生成令牌，同时添加用户信息。
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("用户已被禁用")
                attrs['user'] = user
                data = super().validate(attrs) # 生成令牌
                data.update({'user': UserSerializer(user, context=self.context).data})
                return data
            else:
                raise serializers.ValidationError("提供的凭据无效!")
        else:
            raise serializers.ValidationError("必须包含 'username'和'password'。")
        
    @classmethod
    def get_token(cls, user):
        """
        重写 get_token 方法, 向令牌中添加自定义的声明。
        """
        token = super().get_token(user)
        
        # 添加自定义声明
        