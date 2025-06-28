"""
写真モデル

GPS情報を含む写真データを表現するドメインモデル
"""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
from decimal import Decimal


@dataclass(frozen=True)
class GPSCoordinates:
    """
    GPS座標を表すバリューオブジェクト
    
    不変性を保証し、GPS座標の有効性を検証します。
    """
    latitude: Decimal
    longitude: Decimal
    
    def __post_init__(self):
        """座標の有効性を検証"""
        if not isinstance(self.latitude, Decimal):
            object.__setattr__(self, 'latitude', Decimal(str(self.latitude)))
        if not isinstance(self.longitude, Decimal):
            object.__setattr__(self, 'longitude', Decimal(str(self.longitude)))
            
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"緯度が範囲外です: {self.latitude} (有効範囲: -90 to 90)")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"経度が範囲外です: {self.longitude} (有効範囲: -180 to 180)")
    
    def to_tuple(self) -> Tuple[float, float]:
        """座標をタプル形式で返す"""
        return (float(self.latitude), float(self.longitude))
    
    def distance_to(self, other: 'GPSCoordinates') -> float:
        """
        他の座標との距離を計算（ハーバーサイン公式）
        
        Args:
            other: 比較対象の座標
            
        Returns:
            float: 距離（km）
        """
        import math
        
        # 度をラジアンに変換
        lat1_rad = math.radians(float(self.latitude))
        lon1_rad = math.radians(float(self.longitude))
        lat2_rad = math.radians(float(other.latitude))
        lon2_rad = math.radians(float(other.longitude))
        
        # ハーバーサイン公式
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = (math.sin(dlat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))
        
        # 地球の半径（km）
        earth_radius = 6371.0
        
        return earth_radius * c


@dataclass(frozen=True)
class PhotoMetadata:
    """
    写真のメタデータを表すバリューオブジェクト
    """
    file_size: int  # バイト
    width: Optional[int] = None
    height: Optional[int] = None
    camera_make: Optional[str] = None
    camera_model: Optional[str] = None
    iso: Optional[int] = None
    aperture: Optional[str] = None
    shutter_speed: Optional[str] = None
    focal_length: Optional[str] = None
    
    def __post_init__(self):
        """メタデータの有効性を検証"""
        if self.file_size < 0:
            raise ValueError("ファイルサイズは0以上である必要があります")
        
        if self.width is not None and self.width <= 0:
            raise ValueError("幅は正の値である必要があります")
        
        if self.height is not None and self.height <= 0:
            raise ValueError("高さは正の値である必要があります")
    
    @property
    def aspect_ratio(self) -> Optional[float]:
        """アスペクト比を計算"""
        if self.width and self.height:
            return self.width / self.height
        return None
    
    @property
    def megapixels(self) -> Optional[float]:
        """メガピクセル数を計算"""
        if self.width and self.height:
            return (self.width * self.height) / 1_000_000
        return None


@dataclass
class Photo:
    """
    写真エンティティ
    
    GPS情報を含む写真データの集約ルート
    """
    file_path: Path
    taken_date: Optional[datetime] = None
    gps_coordinates: Optional[GPSCoordinates] = None
    metadata: Optional[PhotoMetadata] = None
    
    def __post_init__(self):
        """写真の有効性を検証"""
        if not isinstance(self.file_path, Path):
            object.__setattr__(self, 'file_path', Path(self.file_path))
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"写真ファイルが存在しません: {self.file_path}")
        
        # サポートされているファイル形式の確認
        supported_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp'}
        if self.file_path.suffix.lower() not in supported_extensions:
            raise ValueError(
                f"サポートされていないファイル形式です: {self.file_path.suffix}"
            )
    
    @property
    def file_name(self) -> str:
        """ファイル名を取得"""
        return self.file_path.name
    
    @property
    def file_extension(self) -> str:
        """ファイル拡張子を取得"""
        return self.file_path.suffix.lower()
    
    @property
    def has_gps_data(self) -> bool:
        """GPS情報を持っているかを確認"""
        return self.gps_coordinates is not None
    
    @property
    def display_name(self) -> str:
        """表示用の名前を生成"""
        if self.taken_date:
            date_str = self.taken_date.strftime("%Y-%m-%d %H:%M:%S")
            return f"{self.file_name} ({date_str})"
        return self.file_name
    
    def distance_to_photo(self, other: 'Photo') -> Optional[float]:
        """
        他の写真との距離を計算
        
        Args:
            other: 比較対象の写真
            
        Returns:
            Optional[float]: 距離（km）、GPS情報がない場合はNone
        """
        if self.gps_coordinates and other.gps_coordinates:
            return self.gps_coordinates.distance_to(other.gps_coordinates)
        return None
    
    def is_nearby(self, other: 'Photo', max_distance_km: float = 1.0) -> bool:
        """
        他の写真が近くにあるかを判定
        
        Args:
            other: 比較対象の写真
            max_distance_km: 最大距離（km）
            
        Returns:
            bool: 近くにある場合True
        """
        distance = self.distance_to_photo(other)
        return distance is not None and distance <= max_distance_km
    
    def update_metadata(self, metadata: PhotoMetadata) -> None:
        """メタデータを更新"""
        self.metadata = metadata
    
    def update_gps_coordinates(self, coordinates: GPSCoordinates) -> None:
        """GPS座標を更新"""
        self.gps_coordinates = coordinates
    
    def update_taken_date(self, taken_date: datetime) -> None:
        """撮影日時を更新"""
        self.taken_date = taken_date
    
    def __str__(self) -> str:
        """文字列表現"""
        return f"Photo({self.display_name})"
    
    def __repr__(self) -> str:
        """デバッグ用の文字列表現"""
        return (f"Photo(file_path={self.file_path}, "
                f"taken_date={self.taken_date}, "
                f"has_gps={self.has_gps_data})")
