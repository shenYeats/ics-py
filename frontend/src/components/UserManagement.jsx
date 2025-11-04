import React, { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  Chip,
  CircularProgress,
  Grid,
  Card,
  CardContent,
  Add,
  Edit,
  Delete,
  Person,
  Visibility,
  VisibilityOff,
} from '../utils/mui';
import { userAPI } from '../services/api';

const UserManagement = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [openDialog, setOpenDialog] = useState(false);
  const [editingUser, setEditingUser] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);

  const [formData, setFormData] = useState({
    email: '',
    password: '',
    password_confirm: '',
    first_name: '',
    last_name: '',
    role: 'user',
    is_active: true,
  });

  // 获取用户列表
  const fetchUsers = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await userAPI.getUsers();
      setUsers(response.data);
    } catch (err) {
      console.error('获取用户列表失败:', err);
      setError('获取用户列表失败，请检查权限或网络连接');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // 重置表单
  const resetForm = () => {
    setFormData({
      email: '',
      password: '',
      password_confirm: '',
      first_name: '',
      last_name: '',
      role: 'user',
      is_active: true,
    });
    setEditingUser(null);
    setError('');
    setSuccess('');
  };

  // 打开创建用户对话框
  const handleCreateUser = () => {
    resetForm();
    setOpenDialog(true);
  };

  // 打开编辑用户对话框
  const handleEditUser = (user) => {
    setFormData({
      email: user.email,
      password: '',
      password_confirm: '',
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      role: user.role,
      is_active: user.is_active,
    });
    setEditingUser(user);
    setOpenDialog(true);
  };

  // 删除用户
  const handleDeleteUser = async (user) => {
    if (!window.confirm(`确定要删除用户 ${user.email} 吗？`)) {
      return;
    }

    try {
      await userAPI.deleteUser(user.id);
      setSuccess('用户删除成功');
      fetchUsers();
    } catch (err) {
      console.error('删除用户失败:', err);
      setError('删除用户失败，请检查权限');
    }
  };

  // 提交表单
  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // 验证表单
    if (!formData.email) {
      setError('邮箱不能为空');
      return;
    }

    if (!editingUser && (!formData.password || !formData.password_confirm)) {
      setError('密码不能为空');
      return;
    }

    if (formData.password !== formData.password_confirm) {
      setError('两次输入的密码不一致');
      return;
    }

    try {
      if (editingUser) {
        // 更新用户
        const updateData = { ...formData };
        if (!updateData.password) {
          delete updateData.password;
          delete updateData.password_confirm;
        }
        await userAPI.updateUser(editingUser.id, updateData);
        setSuccess('用户更新成功');
      } else {
        // 创建用户
        await userAPI.createUser(formData);
        setSuccess('用户创建成功');
      }
      
      setOpenDialog(false);
      resetForm();
      fetchUsers();
    } catch (err) {
      console.error('操作失败:', err);
      setError(err.response?.data?.error || '操作失败，请检查输入信息');
    }
  };

  // 获取角色颜色
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

  // 获取角色文本
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
          用户管理
        </Typography>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={handleCreateUser}
        >
          创建用户
        </Button>
      </Box>

      {/* 统计卡片 */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                总用户数
              </Typography>
              <Typography variant="h5" component="div">
                {users.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                管理员
              </Typography>
              <Typography variant="h5" component="div">
                {users.filter(u => u.role === 'admin').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                普通用户
              </Typography>
              <Typography variant="h5" component="div">
                {users.filter(u => u.role === 'user').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                只读用户
              </Typography>
              <Typography variant="h5" component="div">
                {users.filter(u => u.role === 'viewer').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 消息提示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}
      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

      {/* 用户列表 */}
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>邮箱</TableCell>
                <TableCell>姓名</TableCell>
                <TableCell>角色</TableCell>
                <TableCell>状态</TableCell>
                <TableCell>最后登录</TableCell>
                <TableCell>操作</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {loading ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    <CircularProgress />
                  </TableCell>
                </TableRow>
              ) : users.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} align="center">
                    暂无用户数据
                  </TableCell>
                </TableRow>
              ) : (
                users.map((user) => (
                  <TableRow key={user.id}>
                    <TableCell>{user.email}</TableCell>
                    <TableCell>
                      {user.first_name || '未设置'} {user.last_name || ''}
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={getRoleText(user.role)}
                        color={getRoleColor(user.role)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={user.is_active ? '激活' : '未激活'}
                        color={user.is_active ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {user.last_login 
                        ? new Date(user.last_login).toLocaleString()
                        : '从未登录'
                      }
                    </TableCell>
                    <TableCell>
                      <IconButton
                        color="primary"
                        onClick={() => handleEditUser(user)}
                        size="small"
                      >
                        <Edit />
                      </IconButton>
                      <IconButton
                        color="error"
                        onClick={() => handleDeleteUser(user)}
                        size="small"
                      >
                        <Delete />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* 创建/编辑用户对话框 */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingUser ? '编辑用户' : '创建用户'}
        </DialogTitle>
        <form onSubmit={handleSubmit}>
          <DialogContent>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="邮箱地址"
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                  disabled={!!editingUser}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="密码"
                  type={showPassword ? 'text' : 'password'}
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required={!editingUser}
                  InputProps={{
                    endAdornment: (
                      <IconButton
                        onClick={() => setShowPassword(!showPassword)}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="确认密码"
                  type={showConfirmPassword ? 'text' : 'password'}
                  value={formData.password_confirm}
                  onChange={(e) => setFormData({ ...formData, password_confirm: e.target.value })}
                  required={!editingUser}
                  InputProps={{
                    endAdornment: (
                      <IconButton
                        onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                        edge="end"
                      >
                        {showConfirmPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    ),
                  }}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="名字"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  fullWidth
                  label="姓氏"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                />
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>角色</InputLabel>
                  <Select
                    value={formData.role}
                    label="角色"
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                  >
                    <MenuItem value="admin">管理员</MenuItem>
                    <MenuItem value="user">普通用户</MenuItem>
                    <MenuItem value="viewer">只读用户</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12}>
                <FormControl fullWidth>
                  <InputLabel>状态</InputLabel>
                  <Select
                    value={formData.is_active}
                    label="状态"
                    onChange={(e) => setFormData({ ...formData, is_active: e.target.value })}
                  >
                    <MenuItem value={true}>激活</MenuItem>
                    <MenuItem value={false}>未激活</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setOpenDialog(false)}>取消</Button>
            <Button type="submit" variant="contained">
              {editingUser ? '更新' : '创建'}
            </Button>
          </DialogActions>
        </form>
      </Dialog>
    </Container>
  );
};

export default UserManagement;
