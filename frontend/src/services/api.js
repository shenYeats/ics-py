import axios from 'axios';

// 创建axios实例
const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
});

// 请求拦截器 - 添加认证token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器 - 处理token过期
api.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const originalRequest = error.config;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const response = await axios.post('http://localhost:8000/api/auth/token/refresh/', {
            refresh: refreshToken
          });
          
          const { access } = response.data;
          localStorage.setItem('access_token', access);
          originalRequest.headers.Authorization = `Bearer ${access}`;
          
          return api(originalRequest);
        }
      } catch (refreshError) {
        // 刷新token失败，清除本地存储并跳转到登录页
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

// 认证相关API
export const authAPI = {
  // 用户登录
  login: (email, password) => 
    api.post('/auth/login/', { email, password }),
  
  // 用户登出
  logout: (refreshToken) => 
    api.post('/auth/logout/', { refresh_token: refreshToken }),
  
  // 刷新token
  refreshToken: (refreshToken) => 
    api.post('/auth/token/refresh/', { refresh: refreshToken }),
  
  // 获取当前用户信息
  getProfile: () => 
    api.get('/auth/profile/'),
  
  // 检查权限
  checkPermission: (permissionCode) => 
    api.get(`/auth/check-permission/${permissionCode}/`),
  
  // 获取用户所有权限
  getUserPermissions: () => 
    api.get('/auth/user-permissions/'),
};

// 用户管理API
export const userAPI = {
  // 获取用户列表
  getUsers: () => 
    api.get('/auth/users/'),
  
  // 创建用户
  createUser: (userData) => 
    api.post('/auth/users/', userData),
  
  // 获取用户详情
  getUser: (id) => 
    api.get(`/auth/users/${id}/`),
  
  // 更新用户
  updateUser: (id, userData) => 
    api.put(`/auth/users/${id}/`, userData),
  
  // 删除用户
  deleteUser: (id) => 
    api.delete(`/auth/users/${id}/`),
};

// 权限管理API
export const permissionAPI = {
  // 获取权限列表
  getPermissions: () => 
    api.get('/auth/permissions/'),
  
  // 获取角色权限
  getRolePermissions: () => 
    api.get('/auth/role-permissions/'),
  
  // 创建角色权限
  createRolePermission: (data) => 
    api.post('/auth/role-permissions/', data),
  
  // 更新角色权限
  updateRolePermission: (id, data) => 
    api.put(`/auth/role-permissions/${id}/`, data),
  
  // 删除角色权限
  deleteRolePermission: (id) => 
    api.delete(`/auth/role-permissions/${id}/`),
};

export default api;
