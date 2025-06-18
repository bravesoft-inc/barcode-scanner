import json
from typing import Dict, Any, Optional
from .constants import CORS_HEADERS, HTTP_STATUS

def create_response(status_code: int, body: Dict[str, Any], cors: bool = True) -> Dict[str, Any]:
    """
    標準的なAPIレスポンスを生成
    
    Args:
        status_code: HTTPステータスコード
        body: レスポンスボディ
        cors: CORSヘッダーを含めるかどうか
    
    Returns:
        API Gateway形式のレスポンス
    """
    headers = {}
    
    if cors:
        headers.update(CORS_HEADERS)
    
    headers['Content-Type'] = 'application/json'
    
    return {
        'statusCode': status_code,
        'headers': headers,
        'body': json.dumps(body, ensure_ascii=False, default=str)
    }

def create_error_response(status_code: int, message: str, 
                         error_code: Optional[str] = None, 
                         details: Optional[Dict[str, Any]] = None,
                         cors: bool = True) -> Dict[str, Any]:
    """
    エラーレスポンスを生成
    
    Args:
        status_code: HTTPステータスコード
        message: エラーメッセージ
        error_code: エラーコード（オプション）
        details: 詳細情報（オプション）
        cors: CORSヘッダーを含めるかどうか
    
    Returns:
        API Gateway形式のエラーレスポンス
    """
    error_body = {
        'success': False,
        'error': {
            'message': message,
            'code': error_code or f'HTTP_{status_code}'
        }
    }
    
    if details:
        error_body['error']['details'] = details
    
    return create_response(status_code, error_body, cors)

def create_success_response(data: Dict[str, Any], 
                           message: Optional[str] = None,
                           cors: bool = True) -> Dict[str, Any]:
    """
    成功レスポンスを生成
    
    Args:
        data: レスポンスデータ
        message: 成功メッセージ（オプション）
        cors: CORSヘッダーを含めるかどうか
    
    Returns:
        API Gateway形式の成功レスポンス
    """
    body = {
        'success': True,
        'data': data
    }
    
    if message:
        body['message'] = message
    
    return create_response(HTTP_STATUS['OK'], body, cors)

def create_cors_response() -> Dict[str, Any]:
    """
    CORSプリフライトリクエスト用のレスポンスを生成
    
    Returns:
        CORS対応レスポンス
    """
    return create_response(HTTP_STATUS['OK'], {}, cors=True)

def create_timeout_response(cors: bool = True) -> Dict[str, Any]:
    """
    タイムアウトエラーレスポンスを生成
    
    Args:
        cors: CORSヘッダーを含めるかどうか
    
    Returns:
        タイムアウトエラーレスポンス
    """
    return create_error_response(
        HTTP_STATUS['TIMEOUT'],
        'Request timeout - processing took too long',
        'TIMEOUT_ERROR',
        cors=cors
    )

def create_validation_error_response(field: str, message: str, cors: bool = True) -> Dict[str, Any]:
    """
    バリデーションエラーレスポンスを生成
    
    Args:
        field: エラーが発生したフィールド名
        message: エラーメッセージ
        cors: CORSヘッダーを含めるかどうか
    
    Returns:
        バリデーションエラーレスポンス
    """
    return create_error_response(
        HTTP_STATUS['BAD_REQUEST'],
        f'Validation error in field "{field}": {message}',
        'VALIDATION_ERROR',
        {'field': field},
        cors=cors
    ) 