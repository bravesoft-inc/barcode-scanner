import re
import mimetypes
from typing import Optional, Dict, Any
from .constants import MAX_FILE_SIZE, SUPPORTED_IMAGE_TYPES, PROVIDERS, SUPPORTED_FORMATS

def validate_image_file(image_data: bytes, max_size: int = MAX_FILE_SIZE) -> Optional[str]:
    """
    画像ファイルのバリデーション
    
    Args:
        image_data: 画像データ（バイト）
        max_size: 最大ファイルサイズ
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    if not image_data:
        return "No image data provided"
    
    if len(image_data) > max_size:
        return f"File size exceeds maximum limit of {max_size // (1024*1024)}MB"
    
    # 画像形式の検証（簡易版）
    if len(image_data) < 10:
        return "Invalid image file - too small"
    
    # JPEG, PNG, GIFのマジックナンバーをチェック
    magic_numbers = {
        b'\xff\xd8\xff': 'image/jpeg',
        b'\x89PNG\r\n\x1a\n': 'image/png',
        b'GIF87a': 'image/gif',
        b'GIF89a': 'image/gif'
    }
    
    is_valid_image = False
    for magic, mime_type in magic_numbers.items():
        if image_data.startswith(magic):
            is_valid_image = True
            break
    
    if not is_valid_image:
        return "Unsupported image format. Please use JPEG, PNG, or GIF"
    
    return None

def validate_barcode_data(data: str) -> Optional[str]:
    """
    バーコードデータのバリデーション
    
    Args:
        data: バーコードデータ
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    if not data:
        return "Barcode data is required"
    
    if len(data) < 3:
        return "Barcode data too short"
    
    if len(data) > 100:
        return "Barcode data too long"
    
    # 印刷可能文字のみ許可
    if not data.isprintable():
        return "Barcode data contains non-printable characters"
    
    return None

def validate_format(format_name: str) -> Optional[str]:
    """
    バーコード形式のバリデーション
    
    Args:
        format_name: バーコード形式名
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    if not format_name:
        return None  # 形式指定はオプション
    
    if format_name not in SUPPORTED_FORMATS:
        return f"Unsupported format: {format_name}. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
    
    return None

def validate_provider(provider: str) -> Optional[str]:
    """
    プロバイダーのバリデーション
    
    Args:
        provider: プロバイダー名
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    if not provider:
        return None  # プロバイダー指定はオプション
    
    if provider not in PROVIDERS:
        return f"Unsupported provider: {provider}. Supported providers: {', '.join(PROVIDERS.keys())}"
    
    return None

def validate_scan_params(params: Dict[str, Any]) -> Optional[str]:
    """
    スキャンパラメータの包括的バリデーション
    
    Args:
        params: スキャンパラメータ
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    # プロバイダーヒントの検証
    provider_hint = params.get('provider_hint')
    if provider_hint:
        error = validate_provider(provider_hint)
        if error:
            return error
    
    # フォーマットヒントの検証
    format_hint = params.get('format_hint')
    if format_hint:
        error = validate_format(format_hint)
        if error:
            return error
    
    # enable_mlパラメータの検証
    enable_ml = params.get('enable_ml', 'true')
    if enable_ml not in ['true', 'false']:
        return "enable_ml must be 'true' or 'false'"
    
    return None

def validate_multipart_content_type(content_type: str) -> Optional[str]:
    """
    マルチパートContent-Typeのバリデーション
    
    Args:
        content_type: Content-Typeヘッダー
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    if not content_type:
        return "Content-Type header is required"
    
    if 'multipart/form-data' not in content_type:
        return "Content-Type must be multipart/form-data"
    
    if 'boundary=' not in content_type:
        return "multipart/form-data must include boundary parameter"
    
    return None

def validate_batch_request(images_data: list, max_images: int = 10) -> Optional[str]:
    """
    バッチリクエストのバリデーション
    
    Args:
        images_data: 画像データのリスト
        max_images: 最大画像数
    
    Returns:
        エラーメッセージ（バリデーション成功時はNone）
    """
    if not images_data:
        return "No images provided"
    
    if len(images_data) > max_images:
        return f"Too many images. Maximum allowed: {max_images}"
    
    # 各画像のバリデーション
    for i, image_data in enumerate(images_data):
        error = validate_image_file(image_data)
        if error:
            return f"Image {i+1}: {error}"
    
    return None

def sanitize_barcode_data(data: str) -> str:
    """
    バーコードデータのサニタイゼーション
    
    Args:
        data: 生のバーコードデータ
    
    Returns:
        サニタイズされたデータ
    """
    if not data:
        return ""
    
    # 前後の空白を削除
    data = data.strip()
    
    # 制御文字を削除
    data = ''.join(char for char in data if char.isprintable())
    
    # 連続する空白を単一の空白に置換
    data = re.sub(r'\s+', ' ', data)
    
    return data

def extract_boundary(content_type: str) -> Optional[str]:
    """
    Content-Typeからboundaryを抽出
    
    Args:
        content_type: Content-Typeヘッダー
    
    Returns:
        boundary文字列（見つからない場合はNone）
    """
    if 'boundary=' not in content_type:
        return None
    
    boundary_match = re.search(r'boundary=([^;]+)', content_type)
    if boundary_match:
        return boundary_match.group(1).strip('"')
    
    return None 