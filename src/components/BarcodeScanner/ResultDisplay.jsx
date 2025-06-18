import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Chip,
  Button,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Alert
} from '@mui/material';
import {
  QrCode,
  CheckCircle,
  Error,
  ContentCopy,
  Clear
} from '@mui/icons-material';
import LoadingSpinner from '../common/LoadingSpinner';

const ResultDisplay = ({ result, isScanning, onClear }) => {
  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
  };

  const formatBarcodeData = (data) => {
    if (!data) return '';
    
    // 長いバーコードデータを整形
    if (data.length > 20) {
      return `${data.substring(0, 10)}...${data.substring(data.length - 10)}`;
    }
    return data;
  };

  if (isScanning) {
    return <LoadingSpinner message="バーコードをスキャン中..." />;
  }

  if (!result) {
    return (
      <Box
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'text.secondary'
        }}
      >
        <QrCode sx={{ fontSize: 64, mb: 2, opacity: 0.5 }} />
        <Typography variant="h6" gutterBottom>
          スキャン結果
        </Typography>
        <Typography variant="body2" textAlign="center">
          カメラまたはファイルからバーコードをスキャンしてください
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6">スキャン結果</Typography>
        <Button
          size="small"
          startIcon={<Clear />}
          onClick={onClear}
        >
          クリア
        </Button>
      </Box>

      <Paper elevation={1} sx={{ p: 2, mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          {result.success ? (
            <CheckCircle color="success" sx={{ mr: 1 }} />
          ) : (
            <Error color="error" sx={{ mr: 1 }} />
          )}
          <Typography variant="subtitle1" color={result.success ? 'success.main' : 'error.main'}>
            {result.success ? 'スキャン成功' : 'スキャン失敗'}
          </Typography>
        </Box>

        {result.success && (
          <>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                バーコードデータ
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Typography variant="body1" fontFamily="monospace" sx={{ flex: 1 }}>
                  {formatBarcodeData(result.barcode_data)}
                </Typography>
                <Button
                  size="small"
                  startIcon={<ContentCopy />}
                  onClick={() => handleCopy(result.barcode_data)}
                >
                  コピー
                </Button>
              </Box>
            </Box>

            <Divider sx={{ my: 2 }} />

            <List dense>
              {result.format && (
                <ListItem>
                  <ListItemIcon>
                    <QrCode fontSize="small" />
                  </ListItemIcon>
                  <ListItemText
                    primary="形式"
                    secondary={result.format}
                  />
                </ListItem>
              )}
              
              {result.provider && (
                <ListItem>
                  <ListItemIcon>
                    <QrCode fontSize="small" />
                  </ListItemIcon>
                  <ListItemText
                    primary="プロバイダー"
                    secondary={result.provider}
                  />
                </ListItem>
              )}

              {result.confidence && (
                <ListItem>
                  <ListItemIcon>
                    <QrCode fontSize="small" />
                  </ListItemIcon>
                  <ListItemText
                    primary="信頼度"
                    secondary={`${(result.confidence * 100).toFixed(1)}%`}
                  />
                </ListItem>
              )}
            </List>

            {result.ticket_info && (
              <>
                <Divider sx={{ my: 2 }} />
                <Typography variant="subtitle2" gutterBottom>
                  チケット情報
                </Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                  {result.ticket_info.event_name && (
                    <Chip
                      label={result.ticket_info.event_name}
                      size="small"
                      color="primary"
                    />
                  )}
                  {result.ticket_info.venue && (
                    <Chip
                      label={result.ticket_info.venue}
                      size="small"
                      variant="outlined"
                    />
                  )}
                </Box>
              </>
            )}
          </>
        )}

        {!result.success && result.error && (
          <Alert severity="error" sx={{ mt: 1 }}>
            {result.error}
          </Alert>
        )}
      </Paper>

      {result.metadata && (
        <Paper elevation={1} sx={{ p: 2, flex: 1 }}>
          <Typography variant="subtitle2" gutterBottom>
            メタデータ
          </Typography>
          <Typography variant="body2" fontFamily="monospace" sx={{ fontSize: '0.75rem' }}>
            {JSON.stringify(result.metadata, null, 2)}
          </Typography>
        </Paper>
      )}
    </Box>
  );
};

export default ResultDisplay; 