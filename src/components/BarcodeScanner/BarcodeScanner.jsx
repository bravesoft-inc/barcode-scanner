import React, { useState, useCallback, useRef } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Grid,
  Alert,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { PhotoCamera, Upload } from '@mui/icons-material';
import CameraView from './CameraView';
import ResultDisplay from './ResultDisplay';
import useBarcodeScanner from '../../hooks/useBarcodeScanner';
import { PROVIDERS, BARCODE_FORMATS } from '../../utils/constants';

const BarcodeScanner = () => {
  const [mode, setMode] = useState('camera'); // 'camera' or 'upload'
  const [selectedProvider, setSelectedProvider] = useState('');
  const [selectedFormat, setSelectedFormat] = useState('');
  const fileInputRef = useRef(null);

  const {
    scanResult,
    isScanning,
    error,
    scanFromCamera,
    scanFromFile,
    clearResult
  } = useBarcodeScanner();

  const handleCameraScan = useCallback(async (imageData) => {
    await scanFromCamera(imageData, {
      providerHint: selectedProvider,
      formatHint: selectedFormat
    });
  }, [scanFromCamera, selectedProvider, selectedFormat]);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (file) {
      await scanFromFile(file, {
        providerHint: selectedProvider,
        formatHint: selectedFormat
      });
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  return (
    <Box sx={{ maxWidth: 1200, mx: 'auto', p: 3 }}>
      <Typography variant="h4" gutterBottom align="center">
        マルチフォーマットバーコードスキャナー
      </Typography>

      {/* 設定パネル */}
      <Paper elevation={2} sx={{ p: 3, mb: 3 }}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={4}>
            <FormControl fullWidth>
              <InputLabel>チケット会社</InputLabel>
              <Select
                value={selectedProvider}
                label="チケット会社"
                onChange={(e) => setSelectedProvider(e.target.value)}
              >
                <MenuItem value="">自動検出</MenuItem>
                {PROVIDERS.map((provider) => (
                  <MenuItem key={provider.id} value={provider.id}>
                    {provider.name}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} sm={4}>
            <FormControl fullWidth>
              <InputLabel>バーコード形式</InputLabel>
              <Select
                value={selectedFormat}
                label="バーコード形式"
                onChange={(e) => setSelectedFormat(e.target.value)}
              >
                <MenuItem value="">自動検出</MenuItem>
                {BARCODE_FORMATS.map((format) => (
                  <MenuItem key={format} value={format}>
                    {format}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={4}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button
                variant={mode === 'camera' ? 'contained' : 'outlined'}
                startIcon={<PhotoCamera />}
                onClick={() => setMode('camera')}
                size="small"
              >
                カメラ
              </Button>
              <Button
                variant={mode === 'upload' ? 'contained' : 'outlined'}
                startIcon={<Upload />}
                onClick={() => setMode('upload')}
                size="small"
              >
                ファイル
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      {/* エラー表示 */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={clearResult}>
          {error}
        </Alert>
      )}

      {/* スキャン領域 */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 2, height: 400 }}>
            {mode === 'camera' ? (
              <CameraView
                onScan={handleCameraScan}
                isScanning={isScanning}
              />
            ) : (
              <Box
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  border: '2px dashed #ccc',
                  borderRadius: 1,
                  cursor: 'pointer'
                }}
                onClick={handleUploadClick}
              >
                <Upload sx={{ fontSize: 48, color: 'gray', mb: 2 }} />
                <Typography variant="h6" color="textSecondary">
                  ファイルをクリックして選択
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  JPG, PNG, GIF対応
                </Typography>
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileUpload}
                  accept="image/*"
                  style={{ display: 'none' }}
                />
              </Box>
            )}
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 2, height: 400 }}>
            <ResultDisplay 
              result={scanResult}
              isScanning={isScanning}
              onClear={clearResult}
            />
          </Paper>
        </Grid>
      </Grid>

      {/* ステータス表示 */}
      {isScanning && (
        <Box sx={{ mt: 2, textAlign: 'center' }}>
          <Chip 
            label="スキャン中..." 
            color="primary" 
            variant="outlined"
          />
        </Box>
      )}
    </Box>
  );
};

export default BarcodeScanner; 