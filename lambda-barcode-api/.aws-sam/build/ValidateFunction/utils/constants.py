# バーコード形式
SUPPORTED_FORMATS = [
    'CODE128',
    'CODE39', 
    'EAN13',
    'ITF',
    'CODABAR',
    'CODE93'
]

# チケットプロバイダー
PROVIDERS = {
    'seven_ticket': {
        'name': 'セブンチケット',
        'patterns': [
            r'^23\d{6}\s\d{8}\s\d{3}$',
            r'^\d{6}\s\d{8}\s\d{3}$'
        ]
    },
    'ticket_pia': {
        'name': 'チケットぴあ',
        'patterns': [
            r'^64\d{11}$',
            r'^640032\d{7}$'
        ]
    },
    'lawson_ticket': {
        'name': 'ローソンチケット',
        'patterns': [
            r'^30\d{11}$',
            r'^L\d{10}$'
        ]
    },
    'eplus': {
        'name': 'イープラス',
        'patterns': [
            r'^EP\d{10}$'
        ]
    },
    'cnplayguide': {
        'name': 'CNプレイガイド',
        'patterns': [
            r'^CN\d{10}$'
        ]
    }
}

# ファイル制限
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
SUPPORTED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/gif']

# 画像処理設定
IMAGE_PROCESSING = {
    'max_width': 1920,
    'max_height': 1080,
    'quality': 85,
    'variants': [
        'standard',
        'high_contrast', 
        'edge_enhanced',
        'blur_reduced',
        'noise_reduced'
    ]
}

# スキャン設定
SCAN_CONFIG = {
    'max_candidates': 10,
    'min_confidence': 0.3,
    'timeout_seconds': 25,
    'retry_attempts': 2
}

# エラーメッセージ
ERROR_MESSAGES = {
    'invalid_image': 'Invalid image format or corrupted file',
    'file_too_large': 'File size exceeds maximum limit of 10MB',
    'no_barcode_found': 'No barcode detected in the image',
    'unsupported_format': 'Unsupported barcode format',
    'processing_timeout': 'Image processing timeout',
    'invalid_provider': 'Invalid ticket provider specified',
    'validation_failed': 'Barcode validation failed'
}

# HTTP ステータスコード
HTTP_STATUS = {
    'OK': 200,
    'BAD_REQUEST': 400,
    'NOT_FOUND': 404,
    'INTERNAL_ERROR': 500,
    'TIMEOUT': 408
}

# CORS設定
CORS_HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
} 