import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Typography } from '@mui/material';
import { Login, Dashboard, AdminLayout, UserManagement } from './components';
import { authAPI } from './services/api';

// 创建Material-UI主题
const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
  typography: {
    fontFamily: [
      '-apple-system',
      'BlinkMacSystemFont',
      '"Segoe UI"',
      'Roboto',
      '"Helvetica Neue"',
      'Arial',
      'sans-serif',
    ].join(','),
  },
});

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentPage, setCurrentPage] = useState('dashboard');

  // 检查用户登录状态
  useEffect(() => {
    const checkAuthStatus = async () => {
      try {
        const token = localStorage.getItem('access_token');
        const storedUser = localStorage.getItem('user');
        
        if (token && storedUser) {
          // 验证token是否有效
          try {
            const response = await authAPI.getProfile();
            setUser(response.data);
          } catch (error) {
            // token无效，清除本地存储
            console.error('Token validation failed:', error);
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            setUser(null);
          }
        }
      } catch (error) {
        console.error('Auth check error:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkAuthStatus();
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentPage('dashboard');
  };

  const handlePageChange = (page) => {
    setCurrentPage(page);
  };

  // 渲染当前页面内容
  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard user={user} onLogout={handleLogout} />;
      case 'users':
        return <UserManagement />;
      case 'permissions':
        return (
          <div>
            <Typography variant="h4" gutterBottom>
              权限管理
            </Typography>
            <Typography variant="body1" color="text.secondary">
              权限管理功能开发中...
            </Typography>
          </div>
        );
      case 'settings':
        return (
          <div>
            <Typography variant="h4" gutterBottom>
              系统设置
            </Typography>
            <Typography variant="body1" color="text.secondary">
              系统设置功能开发中...
            </Typography>
          </div>
        );
      default:
        return <Dashboard user={user} onLogout={handleLogout} />;
    }
  };

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div style={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          height: '100vh' 
        }}>
          <div>加载中...</div>
        </div>
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {user ? (
        user.role === 'admin' ? (
          <AdminLayout 
            user={user} 
            onLogout={handleLogout}
            currentPage={currentPage}
            onPageChange={handlePageChange}
          >
            {renderCurrentPage()}
          </AdminLayout>
        ) : (
          <Dashboard user={user} onLogout={handleLogout} />
        )
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </ThemeProvider>
  );
}

export default App;
