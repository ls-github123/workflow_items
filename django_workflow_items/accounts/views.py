from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers.auth_serializers import RegisterSerializer, LoginSerializer
from .serializers.user_serializer import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import logout as django_logout
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from .models import CustomUser

class RegisterView(APIView):
    """
    用户注册视图, 处理 POST 请求以创建新用户。
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save() # 创建用户
            user_serializer = UserSerializer(user, context={'request': request}) # 序列化用户信息
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    用户登录视图, 处理 POST 请求以验证用户凭据并返回 JWT 令牌。
    """
    permission_classes = [AllowAny]  # 允许任何用户
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # 生成 JWT 刷新令牌和访问令牌
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            response = Response({
                'access': access_token,
                'user': serializer.validated_data['user']
            }, status=status.HTTP_200_OK)
            
            # 设置 refresh_token 为 HttpOnly Cookie
            response.set_cookie(
                key = 'refresh_token',
                value = refresh_token,
                httponly = True,
                secure = False, # 生成环境中设置为True
                samesite='Lax', # 根据需求设置
                max_age = 7*24*60*60 # 7天
            )
            
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    """
    用户登出视图, 处理 POST 请求以注销用户并将刷新令牌加入黑名单。
    """
    permission_classes = [IsAuthenticated] # 仅允许已认证用户访问
    
    def post(self, request):
        """
        处理用户登出请求。
        """
        try:
            # 从 cookei 中获取刷新令牌
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token is None:
                return Response({"error": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist() # 将刷新令牌加入黑名单
            django_logout(request) # 注销当前用户会话
            
            # 删除 Cookie
            response = Response({"detail": "退出成功!"}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response({"error": "Invalid token or token already blacklisted."}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    """
    用户信息视图, 处理 GET 请求以获取当前认证用户的详细信息。
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """
        获取当前用户的详细信息。
        """
        serializer = UserSerializer(request.user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateUserStatusView(generics.UpdateAPIView):
    """
    允许管理员更新用户的工作状态和当前去向。
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, permissions.IsAdminUser] # 仅管理员用户可访问
    parser_classes = [MultiPartParser, FormParser] # 支持文件上传
    
    def get_serializer(self, *args, **kwargs):
        kwargs['partial'] = True # 支持部分更新
        return super().get_serializer(*args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        自定义更新逻辑, 进一步限制可更新字段。
        """
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        # 仅允许更新特定字段
        allowed_fields = ['work_status', 'current_destination', 'position', 'department_id', 'date_of_leaving', 'avatar']
        data = {field: request.data.get(field) for field in allowed_fields if field in request.data}
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)