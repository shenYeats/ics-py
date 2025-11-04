// Material-UI 全局组件导出
// 统一导出常用的Material-UI组件，避免在每个文件中重复导入

// 布局组件
export {
  Container,
  Paper,
  Box,
  Grid,
  AppBar,
  Toolbar,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Card,
  CardContent,
} from '@mui/material';

// 表单组件
export {
  TextField,
  Button,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  Radio,
  Switch,
} from '@mui/material';

// 数据展示组件
export {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Avatar,
  Typography,
  Alert,
  CircularProgress,
  LinearProgress,
} from '@mui/material';

// 反馈组件
export {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Backdrop,
} from '@mui/material';

// 导航组件
export {
  Breadcrumbs,
  Link,
  Tabs,
  Tab,
  Stepper,
  Step,
  StepLabel,
} from '@mui/material';

// Material-UI图标
export {
  Add,
  Edit,
  Delete,
  Person,
  Security,
  Settings,
  ExitToApp,
  Dashboard,
  People,
  Menu,
  Visibility,
  VisibilityOff,
  Email,
  Lock,
} from '@mui/icons-material';

// 主题相关
export { ThemeProvider, createTheme } from '@mui/material/styles';
export { default as CssBaseline } from '@mui/material/CssBaseline';
