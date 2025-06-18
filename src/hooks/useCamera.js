import { useState, useCallback, useRef, useEffect } from 'react';

const useCamera = (initialFacingMode = 'environment') => {
  const [stream, setStream] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState(null);
  const [facingMode, setFacingMode] = useState(initialFacingMode);
  const streamRef = useRef(null);

  const startCamera = useCallback(async () => {
    try {
      setError(null);
      
      const constraints = {
        video: {
          facingMode: facingMode,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      };

      const mediaStream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = mediaStream;
      setStream(mediaStream);
      setIsActive(true);
      
    } catch (err) {
      console.error('Camera access error:', err);
      setError(err.name === 'NotAllowedError' 
        ? 'カメラのアクセスが拒否されました' 
        : 'カメラを開始できませんでした'
      );
    }
  }, [facingMode]);

  const stopCamera = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
      setStream(null);
      setIsActive(false);
    }
  }, []);

  const switchCamera = useCallback(async (newFacingMode) => {
    stopCamera();
    setFacingMode(newFacingMode);
    // 少し待ってからカメラを再開
    setTimeout(() => {
      startCamera();
    }, 100);
  }, [stopCamera, startCamera]);

  // クリーンアップ
  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, [stopCamera]);

  return {
    stream,
    isActive,
    error,
    facingMode,
    startCamera,
    stopCamera,
    switchCamera
  };
};

export default useCamera; 