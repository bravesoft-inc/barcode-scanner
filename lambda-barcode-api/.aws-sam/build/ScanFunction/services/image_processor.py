import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import io
from typing import List, Dict, Any
from ..utils.constants import IMAGE_PROCESSING

class ImageProcessor:
    """
    画像の前処理とバリエーション生成を行うクラス
    """
    
    def __init__(self):
        self.max_width = IMAGE_PROCESSING['max_width']
        self.max_height = IMAGE_PROCESSING['max_height']
        self.quality = IMAGE_PROCESSING['quality']
    
    def create_variants(self, image_data: bytes) -> List[Dict[str, Any]]:
        """
        画像データから複数のバリエーションを生成
        
        Args:
            image_data: 元の画像データ（バイト）
        
        Returns:
            処理済み画像バリエーションのリスト
        """
        variants = []
        
        try:
            # PIL Imageに変換
            pil_image = Image.open(io.BytesIO(image_data))
            
            # リサイズ
            pil_image = self._resize_image(pil_image)
            
            # 標準バリエーション
            variants.append({
                'name': 'standard',
                'image': self._pil_to_cv2(pil_image),
                'description': 'Original image with basic preprocessing'
            })
            
            # 高コントラストバリエーション
            high_contrast = self._enhance_contrast(pil_image)
            variants.append({
                'name': 'high_contrast',
                'image': self._pil_to_cv2(high_contrast),
                'description': 'Enhanced contrast for better barcode detection'
            })
            
            # エッジ強調バリエーション
            edge_enhanced = self._enhance_edges(pil_image)
            variants.append({
                'name': 'edge_enhanced',
                'image': self._pil_to_cv2(edge_enhanced),
                'description': 'Edge enhanced for pattern recognition'
            })
            
            # ノイズ除去バリエーション
            noise_reduced = self._reduce_noise(pil_image)
            variants.append({
                'name': 'noise_reduced',
                'image': self._pil_to_cv2(noise_reduced),
                'description': 'Noise reduced for cleaner barcode lines'
            })
            
            # ブラー除去バリエーション
            blur_reduced = self._reduce_blur(pil_image)
            variants.append({
                'name': 'blur_reduced',
                'image': self._pil_to_cv2(blur_reduced),
                'description': 'Blur reduction for sharper barcode edges'
            })
            
            # グレースケールバリエーション
            grayscale = self._convert_grayscale(pil_image)
            variants.append({
                'name': 'grayscale',
                'image': self._pil_to_cv2(grayscale),
                'description': 'Grayscale conversion for monochrome processing'
            })
            
            # 二値化バリエーション
            binary = self._binarize_image(pil_image)
            variants.append({
                'name': 'binary',
                'image': self._pil_to_cv2(binary),
                'description': 'Binary threshold for clear black/white separation'
            })
            
        except Exception as e:
            print(f"Error creating image variants: {e}")
            # エラーが発生した場合は元画像のみを返す
            try:
                pil_image = Image.open(io.BytesIO(image_data))
                pil_image = self._resize_image(pil_image)
                variants.append({
                    'name': 'standard',
                    'image': self._pil_to_cv2(pil_image),
                    'description': 'Original image (fallback)'
                })
            except:
                pass
        
        return variants
    
    def _resize_image(self, image: Image.Image) -> Image.Image:
        """
        画像を適切なサイズにリサイズ
        
        Args:
            image: PIL Image
        
        Returns:
            リサイズされた画像
        """
        width, height = image.size
        
        # 最大サイズを超える場合のみリサイズ
        if width > self.max_width or height > self.max_height:
            # アスペクト比を保持してリサイズ
            ratio = min(self.max_width / width, self.max_height / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    def _enhance_contrast(self, image: Image.Image) -> Image.Image:
        """
        コントラストを強調
        
        Args:
            image: PIL Image
        
        Returns:
            コントラスト強調された画像
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)  # コントラストを2倍に
    
    def _enhance_edges(self, image: Image.Image) -> Image.Image:
        """
        エッジを強調
        
        Args:
            image: PIL Image
        
        Returns:
            エッジ強調された画像
        """
        # エッジ検出フィルターを適用
        edge_enhanced = image.filter(ImageFilter.EDGE_ENHANCE)
        return edge_enhanced
    
    def _reduce_noise(self, image: Image.Image) -> Image.Image:
        """
        ノイズを除去
        
        Args:
            image: PIL Image
        
        Returns:
            ノイズ除去された画像
        """
        # メディアンフィルターでノイズ除去
        denoised = image.filter(ImageFilter.MedianFilter(size=3))
        return denoised
    
    def _reduce_blur(self, image: Image.Image) -> Image.Image:
        """
        ブラーを軽減
        
        Args:
            image: PIL Image
        
        Returns:
            ブラー軽減された画像
        """
        # アンシャープマスクフィルターを適用
        sharpened = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
        return sharpened
    
    def _convert_grayscale(self, image: Image.Image) -> Image.Image:
        """
        グレースケールに変換
        
        Args:
            image: PIL Image
        
        Returns:
            グレースケール画像
        """
        if image.mode != 'L':
            return image.convert('L')
        return image
    
    def _binarize_image(self, image: Image.Image) -> Image.Image:
        """
        画像を二値化
        
        Args:
            image: PIL Image
        
        Returns:
            二値化された画像
        """
        # グレースケールに変換
        gray = self._convert_grayscale(image)
        
        # 適応的閾値処理
        gray_array = np.array(gray)
        
        # OpenCVの適応的閾値処理を使用
        binary = cv2.adaptiveThreshold(
            gray_array, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        return Image.fromarray(binary)
    
    def _pil_to_cv2(self, pil_image: Image.Image) -> np.ndarray:
        """
        PIL ImageをOpenCV形式（numpy配列）に変換
        
        Args:
            pil_image: PIL Image
        
        Returns:
            OpenCV形式の画像配列
        """
        # RGBに変換（OpenCVはBGR形式）
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # numpy配列に変換
        cv2_image = np.array(pil_image)
        
        # BGRに変換（OpenCVの標準形式）
        cv2_image = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2BGR)
        
        return cv2_image
    
    def cv2_to_pil(self, cv2_image: np.ndarray) -> Image.Image:
        """
        OpenCV形式の画像をPIL Imageに変換
        
        Args:
            cv2_image: OpenCV形式の画像配列
        
        Returns:
            PIL Image
        """
        # BGRからRGBに変換
        rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
        
        # PIL Imageに変換
        pil_image = Image.fromarray(rgb_image)
        
        return pil_image
    
    def save_variant(self, variant: Dict[str, Any], filename: str) -> bool:
        """
        バリエーションをファイルに保存（デバッグ用）
        
        Args:
            variant: 画像バリエーション
            filename: 保存するファイル名
        
        Returns:
            保存成功時True
        """
        try:
            cv2_image = variant['image']
            pil_image = self.cv2_to_pil(cv2_image)
            pil_image.save(filename, quality=self.quality)
            return True
        except Exception as e:
            print(f"Error saving variant {filename}: {e}")
            return False 