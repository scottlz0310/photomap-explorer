"""
EXIF読み取りインフラストラクチャ

exifreadライブラリを使用してEXIF情報を読み取る具象実装
"""

import exifread
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

from ..domain.models.photo import GPSCoordinates, PhotoMetadata
from ..utils.exceptions import InfrastructureError


class ExifReader:
    """
    EXIF情報読み取りクラス
    
    exifreadライブラリを使用してEXIF情報を抽出し、
    ドメインモデルに変換します。
    """
    
    def __init__(self):
        self._supported_extensions = {'.jpg', '.jpeg', '.tiff', '.tif'}
    
    def can_read_exif(self, file_path: Path) -> bool:
        """
        ファイルがEXIF読み取り対象かを判定
        
        Args:
            file_path: ファイルパス
            
        Returns:
            bool: EXIF読み取り可能な場合True
        """
        return file_path.suffix.lower() in self._supported_extensions
    
    def extract_metadata(self, file_path: Path) -> Optional[PhotoMetadata]:
        """
        写真のメタデータを抽出
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Optional[PhotoMetadata]: 抽出されたメタデータ、失敗時はNone
        """
        if not file_path.exists():
            return None
        
        try:
            # ファイルサイズを取得
            file_size = file_path.stat().st_size
            
            # EXIF読み取り可能でない場合は基本情報のみ
            if not self.can_read_exif(file_path):
                return PhotoMetadata(file_size=file_size)
            
            # EXIF情報を読み取り
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, details=False, strict=True)
            
            if not tags:
                return PhotoMetadata(file_size=file_size)
            
            # メタデータを抽出
            width = self._extract_image_width(tags)
            height = self._extract_image_height(tags)
            camera_make = self._extract_camera_make(tags)
            camera_model = self._extract_camera_model(tags)
            iso = self._extract_iso(tags)
            aperture = self._extract_aperture(tags)
            shutter_speed = self._extract_shutter_speed(tags)
            focal_length = self._extract_focal_length(tags)
            
            return PhotoMetadata(
                file_size=file_size,
                width=width,
                height=height,
                camera_make=camera_make,
                camera_model=camera_model,
                iso=iso,
                aperture=aperture,
                shutter_speed=shutter_speed,
                focal_length=focal_length
            )
            
        except Exception as e:
            # エラーが発生した場合は基本情報のみ返す
            try:
                file_size = file_path.stat().st_size
                return PhotoMetadata(file_size=file_size)
            except:
                return None
    
    def extract_gps_coordinates(self, file_path: Path) -> Optional[GPSCoordinates]:
        """
        GPS座標を抽出
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Optional[GPSCoordinates]: GPS座標、見つからない場合はNone
        """
        if not file_path.exists() or not self.can_read_exif(file_path):
            return None
        
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, details=False, strict=True)
            
            if not tags:
                return None
            
            # GPS情報を取得
            gps_latitude = tags.get('GPS GPSLatitude')
            gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
            gps_longitude = tags.get('GPS GPSLongitude')
            gps_longitude_ref = tags.get('GPS GPSLongitudeRef')
            
            if not all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
                return None
            
            # 座標を度数法に変換
            lat = self._convert_to_degrees(gps_latitude)
            lon = self._convert_to_degrees(gps_longitude)
            
            # 方位に基づいて符号を調整
            if gps_latitude_ref.values[0] != 'N':
                lat = -lat
            if gps_longitude_ref.values[0] != 'E':
                lon = -lon
            
            return GPSCoordinates(
                latitude=Decimal(str(lat)),
                longitude=Decimal(str(lon))
            )
            
        except Exception as e:
            return None
    
    def extract_taken_date(self, file_path: Path) -> Optional[datetime]:
        """
        撮影日時を抽出
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Optional[datetime]: 撮影日時、見つからない場合はNone
        """
        if not file_path.exists() or not self.can_read_exif(file_path):
            return None
        
        try:
            with open(file_path, 'rb') as f:
                tags = exifread.process_file(f, details=False, strict=True)
            
            if not tags:
                return None
            
            # 撮影日時を取得（優先順位順）
            date_tags = [
                'EXIF DateTimeOriginal',
                'EXIF DateTime',
                'Image DateTime'
            ]
            
            for tag_name in date_tags:
                date_tag = tags.get(tag_name)
                if date_tag:
                    try:
                        # EXIFの日時形式: "2023:12:31 12:34:56"
                        date_str = str(date_tag).strip()
                        if date_str and date_str != "":
                            return datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    except ValueError:
                        continue
            
            return None
            
        except Exception as e:
            return None
    
    def extract_all_info(self, file_path: Path) -> Dict[str, Any]:
        """
        すべての情報を一括抽出
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Dict[str, Any]: 抽出された情報
        """
        return {
            'metadata': self.extract_metadata(file_path),
            'gps_coordinates': self.extract_gps_coordinates(file_path),
            'taken_date': self.extract_taken_date(file_path)
        }
    
    def _convert_to_degrees(self, gps_coord) -> float:
        """
        GPS座標を度数法に変換
        
        Args:
            gps_coord: GPS座標（度分秒形式）
            
        Returns:
            float: 度数法の座標
        """
        d, m, s = [float(x.num) / float(x.den) for x in gps_coord.values]
        return d + (m / 60.0) + (s / 3600.0)
    
    def _extract_image_width(self, tags) -> Optional[int]:
        """画像の幅を抽出"""
        width_tag = tags.get('EXIF ExifImageWidth') or tags.get('Image ImageWidth')
        if width_tag:
            try:
                return int(width_tag.values[0])
            except:
                pass
        return None
    
    def _extract_image_height(self, tags) -> Optional[int]:
        """画像の高さを抽出"""
        height_tag = tags.get('EXIF ExifImageLength') or tags.get('Image ImageLength')
        if height_tag:
            try:
                return int(height_tag.values[0])
            except:
                pass
        return None
    
    def _extract_camera_make(self, tags) -> Optional[str]:
        """カメラメーカーを抽出"""
        make_tag = tags.get('Image Make')
        if make_tag:
            return str(make_tag).strip()
        return None
    
    def _extract_camera_model(self, tags) -> Optional[str]:
        """カメラモデルを抽出"""
        model_tag = tags.get('Image Model')
        if model_tag:
            return str(model_tag).strip()
        return None
    
    def _extract_iso(self, tags) -> Optional[int]:
        """ISO感度を抽出"""
        iso_tag = tags.get('EXIF ISOSpeedRatings')
        if iso_tag:
            try:
                return int(iso_tag.values[0])
            except:
                pass
        return None
    
    def _extract_aperture(self, tags) -> Optional[str]:
        """絞り値を抽出"""
        aperture_tag = tags.get('EXIF FNumber')
        if aperture_tag:
            try:
                f_num = float(aperture_tag.values[0].num) / float(aperture_tag.values[0].den)
                return f"f/{f_num:.1f}"
            except:
                pass
        return None
    
    def _extract_shutter_speed(self, tags) -> Optional[str]:
        """シャッタースピードを抽出"""
        shutter_tag = tags.get('EXIF ExposureTime')
        if shutter_tag:
            try:
                num = shutter_tag.values[0].num
                den = shutter_tag.values[0].den
                if num == 1:
                    return f"1/{den}"
                else:
                    return f"{num}/{den}"
            except:
                pass
        return None
    
    def _extract_focal_length(self, tags) -> Optional[str]:
        """焦点距離を抽出"""
        focal_tag = tags.get('EXIF FocalLength')
        if focal_tag:
            try:
                focal = float(focal_tag.values[0].num) / float(focal_tag.values[0].den)
                return f"{focal:.0f}mm"
            except:
                pass
        return None
