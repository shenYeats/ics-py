from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Permission, RolePermission
from .permissions import IsAdmin, IsOwnerOrAdmin, HasPermission, PermissionCodes
from .serializers import UserSerializer, UserCreateSerializer, PermissionSerializer, RolePermissionSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """用户登录接口"""
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response(
            {'error': '邮箱和密码不能为空'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # 使用自定义用户管理器进行认证
    try:
        user = User.objects.get(email=email)
        if user.check_password(password) and user.is_active:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        else:
            return Response(
                {'error': '无效的凭据或用户未激活'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
    except User.DoesNotExist:
        return Response(
            {'error': '用户不存在'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """用户登出接口"""
    # 简化登出逻辑，直接返回成功
    # 前端会清除本地存储的token，使token自然过期
    return Response({'message': '成功登出'})


class UserListView(generics.ListCreateAPIView):
    """用户列表和创建接口"""
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        # 管理员可以看到所有用户，普通用户只能看到自己
        if self.request.user.is_admin:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """用户详情接口"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerOrAdmin]
    
    def get_object(self):
        # 普通用户只能获取自己的信息
        if not self.request.user.is_admin:
            return self.request.user
        return super().get_object()


class PermissionListView(generics.ListAPIView):
    """权限列表接口"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdmin]


class RolePermissionListView(generics.ListCreateAPIView):
    """角色权限管理接口"""
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAdmin]


class RolePermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """角色权限详情接口"""
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [IsAdmin]


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    """获取当前用户信息"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def check_permission(request, permission_code):
    """检查用户是否具有特定权限"""
    has_perm = HasPermission(permission_code).has_permission(request, None)
    return Response({'has_permission': has_perm})


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_permissions(request):
    """获取当前用户的所有权限"""
    user = request.user
    
    if user.is_admin:
        # 管理员拥有所有权限
        permissions_list = Permission.objects.all().values_list('code', flat=True)
    else:
        # 获取用户角色对应的权限
        permissions_list = Permission.objects.filter(
            rolepermission__role=user.role
        ).values_list('code', flat=True)
    
    return Response({'permissions': list(permissions_list)})
