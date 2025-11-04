from rest_framework import permissions
from .models import User, Permission, RolePermission


class IsAdmin(permissions.BasePermission):
    """检查用户是否为管理员"""
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsOwnerOrAdmin(permissions.BasePermission):
    """检查用户是否为对象所有者或管理员"""
    
    def has_object_permission(self, request, view, obj):
        # 管理员有所有权限
        if request.user.is_admin:
            return True
        
        # 检查对象是否有user属性
        if hasattr(obj, 'user'):
            return obj.user == request.user
        
        # 检查对象是否有owner属性
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # 检查对象是否有created_by属性
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        
        return False


class HasPermission(permissions.BasePermission):
    """检查用户是否具有特定权限"""
    
    def __init__(self, permission_code):
        self.permission_code = permission_code
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 管理员拥有所有权限
        if request.user.is_admin:
            return True
        
        try:
            # 获取权限对象
            permission = Permission.objects.get(code=self.permission_code)
            # 检查用户角色是否有此权限
            return RolePermission.objects.filter(
                role=request.user.role,
                permission=permission
            ).exists()
        except Permission.DoesNotExist:
            return False


class IsViewerReadOnly(permissions.BasePermission):
    """只读用户只能进行GET请求"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # 只读用户只能进行安全方法（GET, HEAD, OPTIONS）
        if request.user.is_viewer:
            return request.method in permissions.SAFE_METHODS
        
        return True


# 预定义的权限代码
class PermissionCodes:
    """权限代码常量"""
    USER_READ = 'user_read'
    USER_WRITE = 'user_write'
    USER_DELETE = 'user_delete'
    DATA_READ = 'data_read'
    DATA_WRITE = 'data_write'
    DATA_DELETE = 'data_delete'
    SYSTEM_CONFIG = 'system_config'


# 便捷的权限类
class CanReadUsers(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.USER_READ)


class CanWriteUsers(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.USER_WRITE)


class CanDeleteUsers(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.USER_DELETE)


class CanReadData(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.DATA_READ)


class CanWriteData(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.DATA_WRITE)


class CanDeleteData(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.DATA_DELETE)


class CanConfigSystem(HasPermission):
    def __init__(self):
        super().__init__(PermissionCodes.SYSTEM_CONFIG)
