import React from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  Avatar,
  Divider,
  Person,
  Security,
  Settings,
  ExitToApp,
} from '../utils/mui';
import { authAPI } from '../services/api';

const Dashboard = ({ user, onLogout }) => {
  const handleLogout = async () => {
    try {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        await authAPI.logout(refreshToken);
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      // 清除本地存储
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      
      // 调用登出回调
      if (onLogout) {
        onLogout();
      }
    }
  };

  const getRoleColor = (role) => {
    switch (role) {
      case 'admin':
        return 'success';
      case 'user':
        return 'primary';
      case 'viewer':
        return 'secondary';
      default:
        return 'default';
    }
  };

  const getRoleText = (role) => {
    switch (role) {
      case 'admin':
        return '管理员';
      case 'user':
        return '普通用户';
      case 'viewer':
        return '只读用户';
      default:
        return role;
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" component="h1">
          系统仪表板
        </Typography>
        <Button
          variant="outlined"
          startIcon={<ExitToApp />}
          onClick={handleLogout}
          color="error"
        >
          退出登录
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* 用户信息卡片 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <Person />
                </Avatar>
                <Box>
                  <Typography variant="h6" component="div">
                    {user.email}
                  </Typography>
                  <Chip
                    label={getRoleText(user.role)}
                    color={getRoleColor(user.role)}
                    size="small"
                  />
                </Box>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  姓名: {user.first_name || '未设置'} {user.last_name || ''}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  邮箱: {user.email}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  角色: {getRoleText(user.role)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  状态: {user.is_active ? '激活' : '未激活'}
                </Typography>
                {user.last_login && (
                  <Typography variant="body2" color="text.secondary">
                    最后登录: {new Date(user.last_login).toLocaleString()}
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 系统信息卡片 */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <Security />
                </Avatar>
                <Typography variant="h6" component="div">
                  系统信息
                </Typography>
              </Box>
              <Divider sx={{ my: 2 }} />
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                <Typography variant="body2">
                  • 基于 Django + React 的全栈应用
                </Typography>
                <Typography variant="body2">
                  • 使用 JWT 进行身份认证
                </Typography>
                <Typography variant="body2">
                  • 支持角色权限管理
                </Typography>
                <Typography variant="body2">
                  • 响应式 Material-UI 设计
                </Typography>
                <Typography variant="body2">
                  • PostgreSQL 数据库支持
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* 功能卡片 */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              可用功能
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'primary.light', color: 'white' }}>
                  <Typography variant="h6">用户管理</Typography>
                  <Typography variant="body2">
                    {user.role === 'admin' ? '完全访问' : '受限访问'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'secondary.light', color: 'white' }}>
                  <Typography variant="h6">数据管理</Typography>
                  <Typography variant="body2">
                    {user.role === 'viewer' ? '只读' : '读写访问'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'success.light', color: 'white' }}>
                  <Typography variant="h6">权限管理</Typography>
                  <Typography variant="body2">
                    {user.role === 'admin' ? '完全访问' : '无访问权限'}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={6} md={3}>
                <Paper sx={{ p: 2, textAlign: 'center', bgcolor: 'warning.light', color: 'white' }}>
                  <Typography variant="h6">系统设置</Typography>
                  <Typography variant="body2">
                    {user.role === 'admin' ? '完全访问' : '无访问权限'}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
