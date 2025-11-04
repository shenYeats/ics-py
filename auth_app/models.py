from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """自定义用户管理器"""
    
    def create_user(self, email, password=None, **extra_fields):
        """创建普通用户"""
        if not email:
            raise ValueError('用户必须提供邮箱地址')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """创建超级用户"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置 is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置 is_superuser=True')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """自定义用户模型"""
    username = None
    email = models.EmailField(_('邮箱地址'), unique=True)
    
    # 用户角色
    ROLE_CHOICES = (
        ('admin', '管理员'),
        ('user', '普通用户'),
        ('viewer', '只读用户'),
    )
    role = models.CharField(_('角色'), max_length=20, choices=ROLE_CHOICES, default='user')
    
    # 用户状态
    is_active = models.BooleanField(_('激活状态'), default=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)
    updated_at = models.DateTimeField(_('更新时间'), auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('用户')
        verbose_name_plural = _('用户')

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        """判断是否为管理员"""
        return self.role == 'admin' or self.is_superuser

    @property
    def is_viewer(self):
        """判断是否为只读用户"""
        return self.role == 'viewer'


class Permission(models.Model):
    """权限模型"""
    name = models.CharField(_('权限名称'), max_length=100, unique=True)
    code = models.CharField(_('权限代码'), max_length=50, unique=True)
    description = models.TextField(_('权限描述'), blank=True)
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('权限')
        verbose_name_plural = _('权限')

    def __str__(self):
        return f"{self.name} ({self.code})"


class RolePermission(models.Model):
    """角色权限关联表"""
    role = models.CharField(_('角色'), max_length=20, choices=User.ROLE_CHOICES)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, verbose_name=_('权限'))
    created_at = models.DateTimeField(_('创建时间'), auto_now_add=True)

    class Meta:
        verbose_name = _('角色权限')
        verbose_name_plural = _('角色权限')
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role} - {self.permission.name}"
