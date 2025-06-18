import cv2
import numpy as np
from typing import List, Dict, Any, Optional
import re
import time

try:
    from pyzbar import pyzbar
    PYZBAR_AVAILABLE = True
except ImportError:
    PYZBAR_AVAILABLE = False

try:
    import zxing
    ZXING_AVAILABLE = True
except ImportError:
    ZXING_AVAILABLE = False

class MultiFormatBarcodeScanner:
    """
    マルチフォーマット対応バーコードスキャナー
    """
    
    def __init__(self):
        self.engines = self._init_engines()
        self.ml_model = None  # 必要に応じてML Kitモデルを読み込み
    
    def _init_engines(self) -> List[Dict[str, Any]]:
        """
        利用可能なエンジンを初期化
        """
        engines = []
        
        if PYZBAR_AVAILABLE:
            engines.append({
                'name': 'pyzbar',
                'function': self._scan_with_pyzbar,
                'priority': 1,
                'formats': ['CODE128', 'CODE39', 'EAN13', 'ITF', 'CODABAR']
            })
        
        if ZXING_AVAILABLE:
            engines.append({
                'name': 'zxing',
                'function': self._scan_with_zxing,
                'priority': 2,
                'formats': ['CODE128', 'CODE39', 'EAN13', 'ITF', 'CODE93']
            })
        
        # OpenCVカスタム実装
        engines.append({
            'name': 'opencv',
            'function': self._scan_with_opencv,
            'priority': 3,
            'formats': ['CODE128']
        })
        
        return sorted(engines, key=lambda x: x['priority'])
    
    def scan_multiple_variants(self, variants: List[Dict[str, Any]], 
                              provider_hint: Optional[str] = None,
                              format_hint: Optional[str] = None,
                              enable_ml: bool = True) -> List[Dict[str, Any]]:
        """
        複数の前処理バリエーションでスキャンを実行
        """
        all_results = []
        
        for variant in variants:
            image = variant['image']
            variant_name = variant['name']
            
            for engine in self.engines:
                # フォーマットヒントがある場合は対応エンジンのみ実行
                if format_hint and format_hint not in engine['formats']:
                    continue
                
                try:
                    results = engine['function'](image, format_hint)
                    
                    for result in results:
                        if self._validate_result(result, provider_hint):
                            confidence = self._calculate_confidence(
                                result, variant_name, engine['name'], provider_hint
                            )
                            
                            all_results.append({
                                'data': result,
                                'format': self._detect_format(result),
                                'engine': engine['name'],
                                'variant': variant_name,
                                'confidence': confidence,
                                'timestamp': time.time()
                            })
                            
                except Exception as e:
                    print(f"Engine {engine['name']} failed on variant {variant_name}: {e}")
                    continue
        
        # 重複除去
        unique_results = self._remove_duplicates(all_results)
        
        # ML による精度向上（有効な場合）
        if enable_ml and len(unique_results) > 1 and self.ml_model:
            unique_results = self._apply_ml_ranking(unique_results)
        
        return sorted(unique_results, key=lambda x: x['confidence'], reverse=True)
    
    def _scan_with_pyzbar(self, image: np.ndarray, format_hint: Optional[str] = None) -> List[str]:
        """
        PyZBarを使用したスキャン
        """
        if not PYZBAR_AVAILABLE:
            return []
        
        try:
            # 全フォーマットでスキャン
            barcodes = pyzbar.decode(image)
            results = []
            
            for barcode in barcodes:
                try:
                    data = barcode.data.decode('utf-8')
                    if data and len(data) > 2:
                        results.append(data)
                except UnicodeDecodeError:
                    # バイナリデータの場合は16進数で保存
                    data = barcode.data.hex()
                    results.append(data)
            
            return results
            
        except Exception as e:
            print(f"PyZBar scan error: {e}")
            return []
    
    def _scan_with_zxing(self, image: np.ndarray, format_hint: Optional[str] = None) -> List[str]:
        """
        ZXingを使用したスキャン（仮実装）
        """
        # 実際の環境ではzxing-cppまたはpython-zxingを使用
        return []
    
    def _scan_with_opencv(self, image: np.ndarray, format_hint: Optional[str] = None) -> List[str]:
        """
        OpenCVカスタム実装（基本的なパターンマッチング）
        """
        try:
            # エッジ検出
            edges = cv2.Canny(image, 50, 150)
            
            # 水平線検出
            horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
            horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, horizontal_kernel)
            
            # バーコード領域の抽出（簡易版）
            contours, _ = cv2.findContours(horizontal_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            results = []
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                
                # バーコードらしい領域のみ処理
                if w > 100 and h > 10 and w/h > 5:
                    roi = image[y:y+h, x:x+w]
                    # ここで実際のバーコード解析を実装
                    # 現在は空の実装
                    pass
            
            return results
            
        except Exception as e:
            print(f"OpenCV scan error: {e}")
            return []
    
    def _validate_result(self, data: str, provider_hint: Optional[str] = None) -> bool:
        """
        スキャン結果の妥当性検証
        """
        if not data or len(data) < 3:
            return False
        
        # 印刷可能文字チェック
        if not data.isprintable():
            return False
        
        # プロバイダーヒントがある場合の検証
        if provider_hint:
            return self._validate_provider_pattern(data, provider_hint)
        
        # 一般的なパターンチェック
        patterns = [
            r'^\d{6,20}$',           # 数字のみ
            r'^[A-Z]{2}\d{8,15}$',   # アルファベット+数字
            r'^\d{2,3}\s\d{3,15}$',  # スペース区切り数字
            r'^[A-Z0-9\-]{6,25}$'    # 英数字+ハイフン
        ]
        
        return any(re.match(pattern, data) for pattern in patterns)
    
    def _validate_provider_pattern(self, data: str, provider: str) -> bool:
        """
        プロバイダー固有パターンの検証
        """
        provider_patterns = {
            'seven_ticket': [r'^23\d{6}\s\d{8}\s\d{3}$', r'^\d{6}\s\d{8}\s\d{3}$'],
            'ticket_pia': [r'^64\d{11}$', r'^640032\d{7}$'],
            'lawson_ticket': [r'^30\d{11}$', r'^L\d{10}$'],
            'eplus': [r'^EP\d{10}$'],
            'cnplayguide': [r'^CN\d{10}$']
        }
        
        patterns = provider_patterns.get(provider, [])
        return any(re.match(pattern, data) for pattern in patterns)
    
    def _detect_format(self, data: str) -> str:
        """
        データからバーコード形式を推定
        """
        # 長さと文字種別から推定
        if len(data) == 13 and data.isdigit():
            return 'EAN13'
        elif re.match(r'^[A-Z0-9\-\.\s\$\/\+%]+$', data):
            if len(data) <= 43:
                return 'CODE39'
            else:
                return 'CODE128'
        elif data.isdigit() and len(data) % 2 == 0:
            return 'ITF'
        else:
            return 'CODE128'  # デフォルト
    
    def _calculate_confidence(self, data: str, variant: str, engine: str, provider_hint: Optional[str] = None) -> float:
        """
        信頼度スコアの計算
        """
        base_score = 0.5
        
        # エンジン重み
        engine_weights = {'pyzbar': 0.3, 'zxing': 0.25, 'opencv': 0.1}
        base_score += engine_weights.get(engine, 0.1)
        
        # バリアント重み
        variant_weights = {'standard': 0.2, 'high_contrast': 0.15, 'edge_enhanced': 0.1}
        base_score += variant_weights.get(variant, 0.05)
        
        # プロバイダー一致ボーナス
        if provider_hint and self._validate_provider_pattern(data, provider_hint):
            base_score += 0.2
        
        # データ品質ボーナス
        if data.isdigit() or re.match(r'^[A-Z0-9\s]+$', data):
            base_score += 0.1
        
        return min(base_score, 1.0)
    
    def _remove_duplicates(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        重複結果の除去
        """
        seen = set()
        unique_results = []
        
        for result in results:
            data = result['data']
            if data not in seen:
                seen.add(data)
                unique_results.append(result)
        
        return unique_results
    
    def select_best_result(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        最適な結果を選択
        """
        if not results:
            return None
        
        # 信頼度順でソート済みのため、最初の要素を返す
        return results[0]
    
    def _apply_ml_ranking(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        MLモデルを使用して結果を再ランク付け（将来の拡張用）
        """
        # 現在は実装なし。将来的にMLモデルを統合
        return results 