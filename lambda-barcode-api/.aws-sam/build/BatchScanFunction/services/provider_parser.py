import re
from typing import Dict, Any, Optional
from ..utils.constants import PROVIDERS

class ProviderParser:
    """
    チケットプロバイダー固有のデータ解析を行うクラス
    """
    
    def __init__(self):
        self.providers = PROVIDERS
    
    def detect_provider(self, barcode_data: str) -> Optional[str]:
        """
        バーコードデータからプロバイダーを自動検出
        
        Args:
            barcode_data: バーコードデータ
        
        Returns:
            検出されたプロバイダーID（検出できない場合はNone）
        """
        if not barcode_data:
            return None
        
        # 各プロバイダーのパターンでマッチング
        for provider_id, provider_info in self.providers.items():
            patterns = provider_info['patterns']
            
            for pattern in patterns:
                if re.match(pattern, barcode_data):
                    return provider_id
        
        return None
    
    def parse(self, barcode_data: str, provider: Optional[str] = None) -> Dict[str, Any]:
        """
        バーコードデータを解析して構造化データを生成
        
        Args:
            barcode_data: バーコードデータ
            provider: プロバイダーID（Noneの場合は自動検出）
        
        Returns:
            解析されたデータ
        """
        if not barcode_data:
            return {}
        
        # プロバイダーが指定されていない場合は自動検出
        if not provider:
            provider = self.detect_provider(barcode_data)
        
        if not provider:
            return self._parse_generic(barcode_data)
        
        # プロバイダー固有の解析
        parser_method = getattr(self, f'_parse_{provider}', None)
        if parser_method:
            return parser_method(barcode_data)
        else:
            return self._parse_generic(barcode_data)
    
    def _parse_seven_ticket(self, data: str) -> Dict[str, Any]:
        """
        セブンチケットのデータ解析
        形式: "23XXXXXX XXXXXXXX XXX" または "XXXXXX XXXXXXXX XXX"
        """
        parsed = {
            'provider': 'seven_ticket',
            'provider_name': 'セブンチケット',
            'raw_data': data
        }
        
        # スペースで分割
        parts = data.split()
        
        if len(parts) >= 3:
            parsed['ticket_number'] = parts[0]
            parsed['serial_number'] = parts[1]
            parsed['check_digit'] = parts[2]
            
            # 店舗コードの抽出（最初の部分が23で始まる場合）
            if parts[0].startswith('23'):
                parsed['store_code'] = parts[0]
                parsed['ticket_id'] = parts[1]
            else:
                parsed['ticket_id'] = parts[0]
                parsed['serial_id'] = parts[1]
        
        return parsed
    
    def _parse_ticket_pia(self, data: str) -> Dict[str, Any]:
        """
        チケットぴあのデータ解析
        形式: "64XXXXXXXXXXX" または "640032XXXXXXX"
        """
        parsed = {
            'provider': 'ticket_pia',
            'provider_name': 'チケットぴあ',
            'raw_data': data
        }
        
        if data.startswith('640032'):
            parsed['prefix'] = '640032'
            parsed['ticket_number'] = data[6:]
        else:
            parsed['prefix'] = '64'
            parsed['ticket_number'] = data[2:]
        
        return parsed
    
    def _parse_lawson_ticket(self, data: str) -> Dict[str, Any]:
        """
        ローソンチケットのデータ解析
        形式: "30XXXXXXXXXXX" または "LXXXXXXXXXX"
        """
        parsed = {
            'provider': 'lawson_ticket',
            'provider_name': 'ローソンチケット',
            'raw_data': data
        }
        
        if data.startswith('30'):
            parsed['prefix'] = '30'
            parsed['ticket_number'] = data[2:]
        elif data.startswith('L'):
            parsed['prefix'] = 'L'
            parsed['ticket_number'] = data[1:]
        
        return parsed
    
    def _parse_eplus(self, data: str) -> Dict[str, Any]:
        """
        イープラスのデータ解析
        形式: "EPXXXXXXXXXX"
        """
        parsed = {
            'provider': 'eplus',
            'provider_name': 'イープラス',
            'raw_data': data
        }
        
        parsed['prefix'] = 'EP'
        parsed['ticket_number'] = data[2:]
        
        return parsed
    
    def _parse_cnplayguide(self, data: str) -> Dict[str, Any]:
        """
        CNプレイガイドのデータ解析
        形式: "CNXXXXXXXXXX"
        """
        parsed = {
            'provider': 'cnplayguide',
            'provider_name': 'CNプレイガイド',
            'raw_data': data
        }
        
        parsed['prefix'] = 'CN'
        parsed['ticket_number'] = data[2:]
        
        return parsed
    
    def _parse_generic(self, data: str) -> Dict[str, Any]:
        """
        一般的なバーコードデータの解析
        """
        parsed = {
            'provider': 'unknown',
            'provider_name': 'Unknown',
            'raw_data': data
        }
        
        # 基本的な情報を抽出
        parsed['length'] = len(data)
        parsed['is_numeric'] = data.isdigit()
        parsed['has_spaces'] = ' ' in data
        parsed['has_letters'] = any(c.isalpha() for c in data)
        
        # スペースで分割された場合
        if ' ' in data:
            parts = data.split()
            parsed['parts'] = parts
            parsed['part_count'] = len(parts)
        
        return parsed
    
    def validate_provider_data(self, data: str, provider: str) -> Dict[str, Any]:
        """
        プロバイダー固有のデータ検証
        
        Args:
            data: バーコードデータ
            provider: プロバイダーID
        
        Returns:
            検証結果
        """
        if provider not in self.providers:
            return {
                'valid': False,
                'error': f'Unknown provider: {provider}'
            }
        
        provider_info = self.providers[provider]
        patterns = provider_info['patterns']
        
        for pattern in patterns:
            if re.match(pattern, data):
                return {
                    'valid': True,
                    'provider': provider,
                    'provider_name': provider_info['name']
                }
        
        return {
            'valid': False,
            'error': f'Data does not match {provider_info["name"]} pattern',
            'expected_patterns': patterns
        }
    
    def get_provider_info(self, provider: str) -> Optional[Dict[str, Any]]:
        """
        プロバイダー情報を取得
        
        Args:
            provider: プロバイダーID
        
        Returns:
            プロバイダー情報（存在しない場合はNone）
        """
        return self.providers.get(provider)
    
    def list_providers(self) -> Dict[str, str]:
        """
        利用可能なプロバイダーのリストを取得
        
        Returns:
            プロバイダーIDと名前の辞書
        """
        return {pid: info['name'] for pid, info in self.providers.items()} 