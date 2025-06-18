import { useState, useCallback } from 'react';
import { scanBarcode, scanBarcodeFile } from '../services/barcodeService';

const useBarcodeScanner = () => {
  const [scanResult, setScanResult] = useState(null);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState(null);

  const scanFromCamera = useCallback(async (imageBlob, options = {}) => {
    try {
      setIsScanning(true);
      setError(null);
      
      const result = await scanBarcode(imageBlob, options);
      setScanResult(result);
      
    } catch (err) {
      setError(err.message || 'スキャンに失敗しました');
      setScanResult(null);
    } finally {
      setIsScanning(false);
    }
  }, []);

  const scanFromFile = useCallback(async (file, options = {}) => {
    try {
      setIsScanning(true);
      setError(null);
      
      const result = await scanBarcodeFile(file, options);
      setScanResult(result);
      
    } catch (err) {
      setError(err.message || 'ファイルのスキャンに失敗しました');
      setScanResult(null);
    } finally {
      setIsScanning(false);
    }
  }, []);

  const clearResult = useCallback(() => {
    setScanResult(null);
    setError(null);
  }, []);

  return {
    scanResult,
    isScanning,
    error,
    scanFromCamera,
    scanFromFile,
    clearResult
  };
};

export default useBarcodeScanner; 