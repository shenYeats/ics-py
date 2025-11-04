from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Permission, RolePermission


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    
    class Meta:
        model = User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'role', 
            'is_active', 'created_at', 'updated_at', 'last_login'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'last_login')


class UserCreateSerializer(serializers.ModelSerializer):
    """用户创建序列化器"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "密码确认不匹配"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """用户更新序列化器"""
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'role', 'is_active')
    
    def update(self, instance, validated_data):
        # 普通用户不能修改自己的角色
        if not self.context['request'].user.is_admin:
            validated_data.pop('role', None)
            validated_data.pop('is_active', None)
        return super().update(instance, validated_data)


class PasswordChangeSerializer(serializers.Serializer):
    """密码修改序列化器"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password_confirm = serializers.CharField(required=True)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("原密码不正确")
        return value
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "新密码确认不匹配"})
        return attrs
    
    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class PermissionSerializer(serializers.ModelSerializer):
    """权限序列化器"""
    
    class Meta:
        model = Permission
        fields = '__all__'
        read_only_fields = ('created_at',)


class RolePermissionSerializer(serializers.ModelSerializer):
    """角色权限序列化器"""
    permission_name = serializers.CharField(source='permission.name', read_only=True)
    permission_code = serializers.CharField(source='permission.code', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = '__all__'
        read_only_fields = ('created_at',)
    
    def validate(self, attrs):
        # 检查是否已存在相同的角色权限组合
        role = attrs.get('role')
        permission = attrs.get('permission')
        
        if RolePermission.objects.filter(role=role, permission=permission).exists():
            raise serializers.ValidationError("该角色已拥有此权限")
        
        return attrs


class UserLoginSerializer(serializers.Serializer):
    """用户登录序列化器"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            try:
                user = User.objects.get(email=email)
                if user.check_password(password) and user.is_active:
                    attrs['user'] = user
                else:
                    raise serializers.ValidationError("无效的凭据或用户未激活")
            except User.DoesNotExist:
                raise serializers.ValidationError("用户不存在")
        else:
            raise serializers.ValidationError("邮箱和密码不能为空")
        
        return attrs
