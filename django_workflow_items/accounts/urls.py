from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileView, UpdateUserStatusView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # 用户注册
    path('login/', LoginView.as_view(), name='login'), # 用户登录
    path('logout/', LogoutView.as_view(), name='logout'), # 用户登出
    path('profile/', UserProfileView.as_view(), name='user-profile'), # 获取用户信息
    path('update-status/<int:pk>/', UpdateUserStatusView.as_view(), name='update-user-status'), # 更新用户状态
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # 刷新访问令牌
]