import React from 'react';
import { Box, Typography, Button, Alert } from '@mui/material';
import { Error as ErrorIcon } from '@mui/icons-material';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // エラーログを送信（本番環境では）
    console.error('Error caught by boundary:', error, errorInfo);
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
  };

  render() {
    if (this.state.hasError) {
      return (
        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '100vh',
            p: 3,
            textAlign: 'center'
          }}
        >
          <ErrorIcon sx={{ fontSize: 64, color: 'error.main', mb: 2 }} />
          <Typography variant="h4" gutterBottom color="error.main">
            エラーが発生しました
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
            予期しないエラーが発生しました。ページを再読み込みしてください。
          </Typography>
          
          <Alert severity="error" sx={{ mb: 3, maxWidth: 600 }}>
            <Typography variant="body2">
              {this.state.error && this.state.error.toString()}
            </Typography>
          </Alert>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              variant="contained"
              onClick={this.handleReset}
              sx={{ mr: 1 }}
            >
              再試行
            </Button>
            <Button
              variant="outlined"
              onClick={() => window.location.reload()}
            >
              ページを再読み込み
            </Button>
          </Box>
        </Box>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary; 