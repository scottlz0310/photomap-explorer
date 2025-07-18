"""
画像情報抽出ユーティリティ

PILLOW + exifreadを使用した高機能な画像情報取得
"""

import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class ImageInfoExtractor:
    """画像情報抽出クラス"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # ライブラリ可用性をチェック
        self.pillow_available = self._check_pillow()
        self.exifread_available = self._check_exifread()
        
        self.logger.info(f"ImageInfoExtractor初期化完了 - PILLOW:{self.pillow_available}, exifread:{self.exifread_available}")
    
    def _check_pillow(self) -> bool:
        """PILLOWライブラリの可用性をチェック"""
        try:
            from PIL import Image
            return True
        except ImportError:
            self.logger.warning("PILLOWライブラリが利用できません")
            return False
    
    def _check_exifread(self) -> bool:
        """exifreadライブラリの可用性をチェック"""
        try:
            import exifread
            return True
        except ImportError:
            self.logger.warning("exifreadライブラリが利用できません")
            return False
    
    def extract_basic_info(self, image_path: str) -> Dict[str, Any]:
        """基本ファイル情報の抽出"""
        try:
            file_path = Path(image_path)
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # 更新日時
            modification_time = file_path.stat().st_mtime
            modified_date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
            
            return {
                'filename': file_path.name,
                'file_size_mb': file_size_mb,
                'modified_date': modified_date,
                'format_guess': file_path.suffix.upper().replace('.', ''),
                'folder_name': file_path.parent.name,
                'full_path': str(file_path.parent)
            }
            
        except Exception as e:
            self.logger.error(f"基本情報取得エラー: {e}")
            return {'error': str(e)}
    
    def extract_image_info(self, image_path: str) -> Dict[str, Any]:
        """PILLOW使用画像情報の抽出"""
        if not self.pillow_available:
            return {'error': 'PILLOWライブラリが必要'}
        
        try:
            from PIL import Image
            
            with Image.open(image_path) as img:
                info = {
                    'width': img.size[0],
                    'height': img.size[1],
                    'format': img.format,
                    'mode': img.mode,
                    'color_profile': 'あり' if 'icc_profile' in img.info else 'なし'
                }
                
                # 追加情報
                if hasattr(img, 'info') and img.info:
                    info['additional_info'] = len(img.info)
                
                return info
                
        except Exception as e:
            self.logger.error(f"PILLOW画像情報取得エラー: {e}")
            return {'error': str(e)}
    
    def extract_exif_info(self, image_path: str) -> Dict[str, Any]:
        """exifread使用EXIF情報の抽出"""
        if not self.exifread_available:
            return {'error': 'exifreadライブラリが必要'}
        
        try:
            import exifread
            
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False)
                
                exif_info = {}
                
                # 重要なEXIF情報を抽出
                exif_mappings = {
                    'EXIF DateTimeOriginal': '撮影日時',
                    'Image Make': 'カメラメーカー',
                    'Image Model': 'カメラモデル',
                    'EXIF ExposureTime': '露出時間',
                    'EXIF FNumber': 'F値',
                    'EXIF ISOSpeedRatings': 'ISO感度',
                    'EXIF FocalLength': '焦点距離',
                    'EXIF Flash': 'フラッシュ',
                    'EXIF WhiteBalance': 'ホワイトバランス',
                    'EXIF ExposureMode': '露出モード',
                    'EXIF SceneCaptureType': '撮影シーン',
                    'Image Orientation': '画像方向'
                }
                
                for tag_name, display_name in exif_mappings.items():
                    if tag_name in tags:
                        exif_info[display_name] = str(tags[tag_name])
                
                # GPS情報の処理
                if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                    lat = tags['GPS GPSLatitude']
                    lon = tags['GPS GPSLongitude']
                    lat_ref = tags.get('GPS GPSLatitudeRef', 'N')
                    lon_ref = tags.get('GPS GPSLongitudeRef', 'E')
                    exif_info['GPS位置'] = f"緯度:{lat} {lat_ref}, 経度:{lon} {lon_ref}"
                
                # レンズ情報
                if 'EXIF LensModel' in tags:
                    exif_info['レンズモデル'] = str(tags['EXIF LensModel'])
                
                return exif_info if exif_info else {'info': 'EXIF情報なし'}
                
        except Exception as e:
            self.logger.error(f"EXIF情報取得エラー: {e}")
            return {'error': str(e)}
    
    def extract_all_info(self, image_path: str) -> Dict[str, Any]:
        """すべての画像情報を抽出"""
        return {
            'basic': self.extract_basic_info(image_path),
            'image': self.extract_image_info(image_path),
            'exif': self.extract_exif_info(image_path)
        }
    
    def format_info_text(self, image_path: str) -> str:
        """情報をフォーマットされたテキストとして返す"""
        all_info = self.extract_all_info(image_path)
        
        lines = []
        
        # 基本情報
        basic = all_info['basic']
        if 'error' not in basic:
            lines.extend([
                f"📁 ファイル名: {basic['filename']}",
                f"💾 ファイルサイズ: {basic['file_size_mb']:.2f} MB",
                f"📅 更新日時: {basic['modified_date']}",
                ""
            ])
        else:
            lines.extend([
                f"📁 基本情報エラー: {basic['error']}",
                ""
            ])
        
        # PILLOW画像情報
        image_info = all_info['image']
        if 'error' not in image_info:
            lines.extend([
                "🖼️ 画像情報:",
                f"  📏 サイズ: {image_info['width']} × {image_info['height']} px",
                f"  🎨 形式: {image_info['format']}",
                f"  🌈 モード: {image_info['mode']}",
                f"  🎭 カラープロファイル: {image_info['color_profile']}",
                ""
            ])
        else:
            lines.extend([
                f"🖼️ 画像情報: {image_info['error']}",
                ""
            ])
        
        # EXIF情報
        exif_info = all_info['exif']
        if 'error' not in exif_info:
            if 'info' in exif_info:
                lines.extend([
                    f"📸 EXIF情報: {exif_info['info']}",
                    ""
                ])
            else:
                lines.append("📸 EXIF情報:")
                for key, value in exif_info.items():
                    lines.append(f"  {key}: {value}")
                lines.append("")
        else:
            lines.extend([
                f"📸 EXIF情報: {exif_info['error']}",
                ""
            ])
        
        # フォルダ情報
        if 'error' not in basic:
            lines.extend([
                f"📂 フォルダ: {basic['folder_name']}",
                f"📍 フルパス: {basic['full_path']}"
            ])
        
        return '\n'.join(lines)
