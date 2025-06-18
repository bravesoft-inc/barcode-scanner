import json
import base64
import io
import time
import re
from typing import Dict, Any, List
import boto3
from PIL import Image

from services.barcode_scanner import MultiFormatBarcodeScanner
from services.image_processor import ImageProcessor
from services.provider_parser import ProviderParser
from utils.response import create_response, create_error_response
from utils.validation import validate_image_file, validate_scan_params
from utils.constants import MAX_FILE_SIZE, SUPPORTED_FORMATS

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    単一画像のバーコードスキャン
    """
    try:
        start_time = time.time()
        
        # CORS対応
        if event.get('httpMethod') == 'OPTIONS':
            return create_response(200, {}, cors=True)
        
        # リクエスト解析
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        if is_base64:
            body = base64.b64decode(body)
        
        # マルチパートデータ解析
        content_type = event.get('headers', {}).get('content-type', '')
        
        if 'multipart/form-data' not in content_type:
            return create_error_response(400, "Content-Type must be multipart/form-data")
        
        # 画像とパラメータの抽出
        image_data, params = extract_multipart_data(body, content_type)
        
        if not image_data:
            return create_error_response(400, "No image data found")
        
        # 画像検証
        validation_error = validate_image_file(image_data, MAX_FILE_SIZE)
        if validation_error:
            return create_error_response(400, validation_error)
        
        # パラメータ検証
        param_error = validate_scan_params(params)
        if param_error:
            return create_error_response(400, param_error)
        
        # 画像処理
        processor = ImageProcessor()
        variants = processor.create_variants(image_data)
        
        # バーコードスキャン
        scanner = MultiFormatBarcodeScanner()
        results = scanner.scan_multiple_variants(
            variants,
            provider_hint=params.get('provider_hint'),
            format_hint=params.get('format_hint'),
            enable_ml=params.get('enable_ml', 'true').lower() == 'true'
        )
        
        if not results:
            return create_error_response(404, "No barcode detected")
        
        # 最適結果選択
        best_result = scanner.select_best_result(results)
        
        # プロバイダー固有解析
        parser = ProviderParser()
        provider = parser.detect_provider(best_result['data'])
        parsed_data = parser.parse(best_result['data'], provider)
        
        # レスポンス構築
        processing_time = int((time.time() - start_time) * 1000)
        
        response_data = {
            "success": True,
            "barcode_data": best_result['data'],
            "detected_format": best_result['format'],
            "confidence": best_result['confidence'],
            "provider": provider,
            "parsed_data": parsed_data,
            "candidates": results[:5],
            "processing_info": {
                "total_time_ms": processing_time,
                "preprocessing_variants": [v['name'] for v in variants],
                "engines_tried": list(set(r['engine'] for r in results)),
                "ml_prediction_used": len(results) > 1 and params.get('enable_ml', 'true').lower() == 'true'
            }
        }
        
        # DynamoDBに保存（オプション）
        save_scan_result(best_result, provider, parsed_data)
        
        return create_response(200, response_data, cors=True)
        
    except Exception as e:
        import traceback
        print(f"Error in scan handler: {str(e)}")
        print(traceback.format_exc())
        return create_error_response(500, f"Internal server error: {str(e)}", cors=True)

def batch_lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    複数画像のバッチスキャン
    """
    try:
        start_time = time.time()
        
        # CORS対応
        if event.get('httpMethod') == 'OPTIONS':
            return create_response(200, {}, cors=True)
        
        # リクエスト解析（複数画像）
        body = event.get('body', '')
        is_base64 = event.get('isBase64Encoded', False)
        
        if is_base64:
            body = base64.b64decode(body)
        
        content_type = event.get('headers', {}).get('content-type', '')
        images_data, params = extract_multiple_images(body, content_type)
        
        if not images_data:
            return create_error_response(400, "No images found")
        
        if len(images_data) > 10:
            return create_error_response(400, "Maximum 10 images allowed")
        
        # 並列処理でスキャン
        scanner = MultiFormatBarcodeScanner()
        processor = ImageProcessor()
        
        results = []
        successful = 0
        
        for idx, image_data in enumerate(images_data):
            try:
                # 画像検証
                validation_error = validate_image_file(image_data, MAX_FILE_SIZE)
                if validation_error:
                    results.append({
                        "image_index": idx,
                        "success": False,
                        "error": validation_error
                    })
                    continue
                
                # 処理実行
                variants = processor.create_variants(image_data)
                scan_results = scanner.scan_multiple_variants(
                    variants,
                    provider_hint=params.get('provider_hint'),
                    format_hint=params.get('format_hint')
                )
                
                if scan_results:
                    best_result = scanner.select_best_result(scan_results)
                    parser = ProviderParser()
                    provider = parser.detect_provider(best_result['data'])
                    parsed_data = parser.parse(best_result['data'], provider)
                    
                    results.append({
                        "image_index": idx,
                        "success": True,
                        "barcode_data": best_result['data'],
                        "detected_format": best_result['format'],
                        "confidence": best_result['confidence'],
                        "provider": provider,
                        "parsed_data": parsed_data
                    })
                    successful += 1
                else:
                    results.append({
                        "image_index": idx,
                        "success": False,
                        "error": "No barcode detected"
                    })
                    
            except Exception as e:
                results.append({
                    "image_index": idx,
                    "success": False,
                    "error": str(e)
                })
        
        processing_time = int((time.time() - start_time) * 1000)
        
        response_data = {
            "results": results,
            "summary": {
                "total_processed": len(images_data),
                "successful": successful,
                "failed": len(images_data) - successful,
                "processing_time_ms": processing_time
            }
        }
        
        return create_response(200, response_data, cors=True)
        
    except Exception as e:
        print(f"Error in batch scan handler: {str(e)}")
        return create_error_response(500, f"Internal server error: {str(e)}", cors=True)

def extract_multipart_data(body: bytes, content_type: str) -> tuple:
    """
    マルチパートデータから画像とパラメータを抽出
    """
    import email
    from email.mime.multipart import MIMEMultipart
    from io import BytesIO
    
    # boundary抽出
    boundary = content_type.split('boundary=')[1].strip()
    
    # email.parserを使用してマルチパートデータを解析
    msg_str = f"Content-Type: {content_type}\r\n\r\n".encode() + body
    msg = email.message_from_bytes(msg_str)
    
    image_data = None
    params = {}
    
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get('Content-Disposition', '')
            
            if 'name="image"' in content_disposition:
                image_data = part.get_payload(decode=True)
            else:
                # その他のパラメータ
                name_match = re.search(r'name="([^"]+)"', content_disposition)
                if name_match:
                    param_name = name_match.group(1)
                    params[param_name] = part.get_payload(decode=True).decode('utf-8')
    
    return image_data, params

def extract_multiple_images(body: bytes, content_type: str) -> tuple:
    """
    複数画像のマルチパートデータを解析
    """
    import email
    
    # boundary抽出
    boundary = content_type.split('boundary=')[1].strip()
    
    # email.parserを使用してマルチパートデータを解析
    msg_str = f"Content-Type: {content_type}\r\n\r\n".encode() + body
    msg = email.message_from_bytes(msg_str)
    
    images_data = []
    params = {}
    
    if msg.is_multipart():
        for part in msg.walk():
            content_disposition = part.get('Content-Disposition', '')
            
            if 'name="images"' in content_disposition:
                images_data.append(part.get_payload(decode=True))
            elif 'name="image_' in content_disposition:
                # 個別の画像ファイル
                images_data.append(part.get_payload(decode=True))
            else:
                # その他のパラメータ
                name_match = re.search(r'name="([^"]+)"', content_disposition)
                if name_match:
                    param_name = name_match.group(1)
                    params[param_name] = part.get_payload(decode=True).decode('utf-8')
    
    return images_data, params

def save_scan_result(result: Dict[str, Any], provider: str, parsed_data: Dict[str, Any]):
    """
    スキャン結果をDynamoDBに保存
    """
    try:
        import os
        import boto3
        from datetime import datetime
        
        table_name = os.environ.get('DYNAMODB_TABLE')
        if not table_name:
            return
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(table_name)
        
        item = {
            'barcode_data': result['data'],
            'barcode_format': result['format'],
            'provider': provider,
            'parsed_data': parsed_data,
            'confidence': result['confidence'],
            'engine_used': result['engine'],
            'created_at': datetime.utcnow().isoformat(),
            'status': 'scanned'
        }
        
        table.put_item(Item=item)
        
    except Exception as e:
        print(f"Error saving to DynamoDB: {e}")
        # エラーは記録するが、メイン処理は継続 