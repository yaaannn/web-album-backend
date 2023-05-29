from rest_framework.permissions import BasePermission


class IsAuthPermission(BasePermission):
    """检查必须登录权限"""

    def has_permission(self, request, view):
        return bool(request.auth)
