from django.core.management.base import BaseCommand
from auth_app.models import Permission, RolePermission
from auth_app.permissions import PermissionCodes


class Command(BaseCommand):
    help = '初始化权限数据'

    def handle(self, *args, **options):
        self.stdout.write('开始初始化权限数据...')
        
        # 定义权限数据
        permissions_data = [
            {
                'name': '用户读取权限',
                'code': PermissionCodes.USER_READ,
                'description': '允许读取用户信息'
            },
            {
                'name': '用户写入权限',
                'code': PermissionCodes.USER_WRITE,
                'description': '允许创建和修改用户信息'
            },
            {
                'name': '用户删除权限',
                'code': PermissionCodes.USER_DELETE,
                'description': '允许删除用户'
            },
            {
                'name': '数据读取权限',
                'code': PermissionCodes.DATA_READ,
                'description': '允许读取数据'
            },
            {
                'name': '数据写入权限',
                'code': PermissionCodes.DATA_WRITE,
                'description': '允许创建和修改数据'
            },
            {
                'name': '数据删除权限',
                'code': PermissionCodes.DATA_DELETE,
                'description': '允许删除数据'
            },
            {
                'name': '系统配置权限',
                'code': PermissionCodes.SYSTEM_CONFIG,
                'description': '允许修改系统配置'
            },
        ]

        # 创建权限
        created_count = 0
        for perm_data in permissions_data:
            permission, created = Permission.objects.get_or_create(
                code=perm_data['code'],
                defaults={
                    'name': perm_data['name'],
                    'description': perm_data['description']
                }
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'创建权限: {permission.name} ({permission.code})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'权限已存在: {permission.name} ({permission.code})')
                )

        # 定义角色权限映射
        role_permissions = {
            'admin': [
                PermissionCodes.USER_READ,
                PermissionCodes.USER_WRITE,
                PermissionCodes.USER_DELETE,
                PermissionCodes.DATA_READ,
                PermissionCodes.DATA_WRITE,
                PermissionCodes.DATA_DELETE,
                PermissionCodes.SYSTEM_CONFIG,
            ],
            'user': [
                PermissionCodes.USER_READ,
                PermissionCodes.DATA_READ,
                PermissionCodes.DATA_WRITE,
            ],
            'viewer': [
                PermissionCodes.USER_READ,
                PermissionCodes.DATA_READ,
            ],
        }

        # 创建角色权限关联
        role_perm_count = 0
        for role, perm_codes in role_permissions.items():
            for perm_code in perm_codes:
                try:
                    permission = Permission.objects.get(code=perm_code)
                    role_perm, created = RolePermission.objects.get_or_create(
                        role=role,
                        permission=permission
                    )
                    if created:
                        role_perm_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'为角色 {role} 分配权限: {permission.name}')
                        )
                except Permission.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'权限不存在: {perm_code}')
                    )

        self.stdout.write(
            self.style.SUCCESS(
                f'权限初始化完成！创建了 {created_count} 个权限，分配了 {role_perm_count} 个角色权限'
            )
        )
