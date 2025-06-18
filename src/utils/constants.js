export const PROVIDERS = [
  { id: 'seven_ticket', name: 'セブンチケット' },
  { id: 'ticket_pia', name: 'チケットぴあ' },
  { id: 'lawson_ticket', name: 'ローソンチケット' },
  { id: 'eplus', name: 'イープラス' },
  { id: 'cnplayguide', name: 'CNプレイガイド' }
];

export const BARCODE_FORMATS = [
  'CODE128',
  'CODE39',
  'EAN13',
  'ITF',
  'CODABAR',
  'CODE93'
];

export const SCAN_MODES = {
  CAMERA: 'camera',
  UPLOAD: 'upload'
};

export const API_ENDPOINTS = {
  SCAN: '/scan',
  VALIDATE: '/validate',
  TICKETS: '/tickets',
  FORMATS: '/formats',
  PROVIDERS: '/providers'
}; 