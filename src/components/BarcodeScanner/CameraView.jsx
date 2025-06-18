import React, { useRef, useCallback, useEffect, useState } from 'react';
import { Box, Button, Typography, Alert } from '@mui/material';
import { CameraAlt, FlipCameraAndroid } from '@mui/icons-material';
import useCamera from '../../hooks/useCamera';

const CameraView = ({ onScan, isScanning }) => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [facingMode, setFacingMode] = useState('environment'); // 'user' or 'environment'
  
  const {
    stream,
    isActive,
    error: cameraError,
    startCamera,
    stopCamera,
    switchCamera
  } = useCamera(facingMode);

  useEffect(() => {
    if (stream && videoRef.current) {
      videoRef.current.srcObject = stream;
    }
  }, [stream]);

  const captureImage = useCallback(() => {
    if (!videoRef.current || !canvasRef.current) return;

    const video = videoRef.current;
    const canvas = canvasRef.current;
    const context = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0);

    // Canvas を Blob に変換
    canvas.toBlob((blob) => {
      if (blob && onScan) {
        onScan(blob);
      }
    }, 'image/jpeg', 0.8);
  }, [onScan]);

  const handleSwitchCamera = async () => {
    const newFacingMode = facingMode === 'environment' ? 'user' : 'environment';
    setFacingMode(newFacingMode);
    await switchCamera(newFacingMode);
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {cameraError && (
        <Alert severity="error" sx={{ mb: 1 }}>
          カメラエラー: {cameraError}
        </Alert>
      )}

      <Box sx={{ flex: 1, position: 'relative', mb: 2 }}>
        {isActive ? (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              style={{
                width: '100%',
                height: '100%',
                objectFit: 'cover',
                borderRadius: 8
              }}
            />
            <canvas
              ref={canvasRef}
              style={{ display: 'none' }}
            />
            
            {/* バーコード読み取りガイドライン */}
            <Box
              sx={{
                position: 'absolute',
                top: '30%',
                left: '10%',
                right: '10%',
                height: '40%',
                border: '2px solid #ff0000',
                borderRadius: 1,
                pointerEvents: 'none',
                '&::before': {
                  content: '""',
                  position: 'absolute',
                  top: '50%',
                  left: 0,
                  right: 0,
                  height: '2px',
                  backgroundColor: '#ff0000',
                  opacity: 0.7
                }
              }}
            />
          </>
        ) : (
          <Box
            sx={{
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: '#f5f5f5',
              borderRadius: 1
            }}
          >
            <CameraAlt sx={{ fontSize: 64, color: 'gray', mb: 2 }} />
            <Typography variant="h6" color="textSecondary" gutterBottom>
              カメラが停止中
            </Typography>
            <Button
              variant="contained"
              onClick={startCamera}
              startIcon={<CameraAlt />}
            >
              カメラを開始
            </Button>
          </Box>
        )}
      </Box>

      {/* カメラコントロール */}
      <Box sx={{ display: 'flex', gap: 1, justifyContent: 'center' }}>
        {isActive && (
          <>
            <Button
              variant="contained"
              onClick={captureImage}
              disabled={isScanning}
              size="large"
              sx={{ flex: 1 }}
            >
              {isScanning ? 'スキャン中...' : 'スキャン'}
            </Button>
            <Button
              variant="outlined"
              onClick={handleSwitchCamera}
              disabled={isScanning}
            >
              <FlipCameraAndroid />
            </Button>
            <Button
              variant="outlined"
              onClick={stopCamera}
              disabled={isScanning}
              color="error"
            >
              停止
            </Button>
          </>
        )}
      </Box>
    </Box>
  );
};

export default CameraView; 