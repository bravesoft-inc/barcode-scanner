import apiClient from './apiClient';

export const scanBarcode = async (imageBlob, options = {}) => {
  const formData = new FormData();
  formData.append('image', imageBlob, 'capture.jpg');
  
  if (options.providerHint) {
    formData.append('provider_hint', options.providerHint);
  }
  
  if (options.formatHint) {
    formData.append('format_hint', options.formatHint);
  }
  
  formData.append('enable_ml', 'true');

  const response = await apiClient.post('/scan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const scanBarcodeFile = async (file, options = {}) => {
  const formData = new FormData();
  formData.append('image', file);
  
  if (options.providerHint) {
    formData.append('provider_hint', options.providerHint);
  }
  
  if (options.formatHint) {
    formData.append('format_hint', options.formatHint);
  }
  
  formData.append('enable_ml', 'true');

  const response = await apiClient.post('/scan', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });

  return response.data;
};

export const validateBarcode = async (barcodeData, format, provider) => {
  const response = await apiClient.post(`/validate/${format}`, {
    barcode_data: barcodeData,
    provider: provider
  });

  return response.data;
};

export const getTicketInfo = async (barcodeData) => {
  const response = await apiClient.get(`/tickets/${encodeURIComponent(barcodeData)}`);
  return response.data;
}; 