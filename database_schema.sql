-- Django PostgreSQL 项目数据库表结构
-- 自动生成的SQL脚本，基于Django模型

-- 创建数据库
CREATE DATABASE ics_db;

-- 连接到数据库
\c ics_db;

-- 设置编码
SET client_encoding = 'UTF8';

-- 创建扩展（如果需要）
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 用户表 (auth_app_user)
CREATE TABLE auth_app_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE NULL,
    is_superuser BOOLEAN NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT true,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'user' CHECK (role IN ('admin', 'user', 'viewer')),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 权限表 (auth_app_permission)
CREATE TABLE auth_app_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 角色权限关联表 (auth_app_rolepermission)
CREATE TABLE auth_app_rolepermission (
    id SERIAL PRIMARY KEY,
    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'user', 'viewer')),
    permission_id INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(role, permission_id),
    FOREIGN KEY (permission_id) REFERENCES auth_app_permission(id) ON DELETE CASCADE
);

-- Django内置表（Django迁移会自动创建）
-- auth_group
-- auth_group_permissions
-- auth_permission
-- auth_user_groups
-- auth_user_user_permissions
-- django_admin_log
-- django_content_type
-- django_migrations
-- django_session

-- 创建索引以提高查询性能
CREATE INDEX idx_user_email ON auth_app_user(email);
CREATE INDEX idx_user_role ON auth_app_user(role);
CREATE INDEX idx_user_created_at ON auth_app_user(created_at);
CREATE INDEX idx_permission_code ON auth_app_permission(code);
CREATE INDEX idx_role_permission_role ON auth_app_rolepermission(role);
CREATE INDEX idx_role_permission_permission ON auth_app_rolepermission(permission_id);

-- 创建触发器自动更新updated_at字段
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_user_updated_at BEFORE UPDATE ON auth_app_user
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 插入初始权限数据
INSERT INTO auth_app_permission (name, code, description) VALUES
('用户读取权限', 'user_read', '允许读取用户信息'),
('用户写入权限', 'user_write', '允许创建和修改用户信息'),
('用户删除权限', 'user_delete', '允许删除用户'),
('数据读取权限', 'data_read', '允许读取数据'),
('数据写入权限', 'data_write', '允许创建和修改数据'),
('数据删除权限', 'data_delete', '允许删除数据'),
('系统配置权限', 'system_config', '允许修改系统配置');

-- 插入角色权限映射
INSERT INTO auth_app_rolepermission (role, permission_id) VALUES
-- 管理员拥有所有权限
('admin', (SELECT id FROM auth_app_permission WHERE code = 'user_read')),
('admin', (SELECT id FROM auth_app_permission WHERE code = 'user_write')),
('admin', (SELECT id FROM auth_app_permission WHERE code = 'user_delete')),
('admin', (SELECT id FROM auth_app_permission WHERE code = 'data_read')),
('admin', (SELECT id FROM auth_app_permission WHERE code = 'data_write')),
('admin', (SELECT id FROM auth_app_permission WHERE code = 'data_delete')),
('admin', (SELECT id FROM auth_app_permission WHERE code = 'system_config')),

-- 普通用户权限
('user', (SELECT id FROM auth_app_permission WHERE code = 'user_read')),
('user', (SELECT id FROM auth_app_permission WHERE code = 'data_read')),
('user', (SELECT id FROM auth_app_permission WHERE code = 'data_write')),

-- 只读用户权限
('viewer', (SELECT id FROM auth_app_permission WHERE code = 'user_read')),
('viewer', (SELECT id FROM auth_app_permission WHERE code = 'data_read'));

-- 创建管理员用户（密码需要加密存储，这里仅为示例）
-- 实际使用时应该通过Django的create_user方法创建
-- INSERT INTO auth_app_user (
--     password, is_superuser, first_name, last_name, is_staff, is_active, date_joined, email, role
-- ) VALUES (
--     'pbkdf2_sha256$600000$...', -- 加密后的密码
--     true, 'Admin', 'User', true, true, CURRENT_TIMESTAMP, 'admin@example.com', 'admin'
-- );

-- 查看表结构
\dt auth_app_*;

-- 查看权限数据
SELECT p.name as permission_name, p.code, rp.role 
FROM auth_app_permission p
JOIN auth_app_rolepermission rp ON p.id = rp.permission_id
ORDER BY rp.role, p.name;

-- 数据库连接池配置建议
-- 在PostgreSQL的postgresql.conf中配置：
-- max_connections = 100
-- shared_buffers = 256MB
-- effective_cache_size = 1GB
-- work_mem = 4MB
-- maintenance_work_mem = 64MB

COMMENT ON TABLE auth_app_user IS '用户表，存储系统用户信息';
COMMENT ON TABLE auth_app_permission IS '权限表，定义系统权限';
COMMENT ON TABLE auth_app_rolepermission IS '角色权限关联表，定义角色拥有的权限';

-- 授予应用用户权限（根据实际情况修改用户名）
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
