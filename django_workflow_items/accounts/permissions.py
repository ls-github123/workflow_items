# 创建自定义权限类
from rest_framework import permissions

class IsAdminUserOrReadOnly(permissions.BasePermission):
    """
    允许管理员用户进行任何操作, 其他用户仅能进行读取操作。
    """
    def has_permission(self, request, view):
        # 安全方法(GET, HEAD, OPTIONS)允许所有认证用户
        if request.method in permissions.SAFE_METHODS:
            return True
        # 非安全方法 仅允许管理员用户
        return request.user and request.user.is_staff