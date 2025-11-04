from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # 认证相关
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # 用户相关
    path('users/', views.UserListView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
    path('profile/', views.user_profile, name='user-profile'),
    
    # 权限相关
    path('permissions/', views.PermissionListView.as_view(), name='permission-list'),
    path('role-permissions/', views.RolePermissionListView.as_view(), name='role-permission-list'),
    path('role-permissions/<int:pk>/', views.RolePermissionDetailView.as_view(), name='role-permission-detail'),
    
    # 权限检查
    path('check-permission/<str:permission_code>/', views.check_permission, name='check-permission'),
    path('user-permissions/', views.user_permissions, name='user-permissions'),
]
