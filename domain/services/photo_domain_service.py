"""
写真ドメインサービス

複数のエンティティにまたがるビジネスロジックや、
エンティティ単体では表現しきれない複雑な操作を提供します。
"""

from typing import List, Optional, Dict, Tuple, Set
from datetime import datetime, timedelta
from pathlib import Path
import asyncio

from ..models.photo import Photo, GPSCoordinates, PhotoMetadata
from ..models.photo_collection import PhotoCollection
from ..repositories.photo_repository import PhotoRepository, PhotoCollectionRepository
from utils.exceptions import DomainError, ValidationError
from utils.helpers import is_image_file, normalize_path


class PhotoDomainService:
    """
    写真ドメインサービス
    
    写真に関する複雑なビジネスロジックを提供します。
    """
    
    def __init__(
        self, 
        photo_repository: PhotoRepository,
        collection_repository: PhotoCollectionRepository
    ):
        self._photo_repository = photo_repository
        self._collection_repository = collection_repository
    
    async def find_duplicate_photos(
        self, 
        photos: List[Photo],
        similarity_threshold: float = 0.95
    ) -> List[List[Photo]]:
        """
        重複写真を検出
        
        Args:
            photos: 対象の写真リスト
            similarity_threshold: 類似度の閾値（0.0-1.0）
            
        Returns:
            List[List[Photo]]: 重複グループのリスト
            
        Note:
            現在の実装はファイル名とサイズによる単純な比較。
            将来的には画像の内容による比較を追加予定。
        """
        if not photos:
            return []
        
        # ファイル名とサイズでグループ化
        groups: Dict[Tuple[str, int], List[Photo]] = {}
        
        for photo in photos:
            if not photo.metadata:
                continue
            
            key = (photo.file_name.lower(), photo.metadata.file_size)
            if key not in groups:
                groups[key] = []
            groups[key].append(photo)
        
        # 重複がある（2つ以上の写真を持つ）グループのみを返す
        duplicates = [group for group in groups.values() if len(group) > 1]
        
        return duplicates
    
    async def analyze_photo_journey(
        self, 
        photos: List[Photo]
    ) -> Optional[List[Photo]]:
        """
        写真から旅行ルートを分析
        
        GPS情報と撮影時刻から時系列順に並べて、
        移動ルートを推定します。
        
        Args:
            photos: 分析対象の写真
            
        Returns:
            Optional[List[Photo]]: 時系列順に並べられた写真、または None
        """
        # GPS情報と撮影時刻の両方を持つ写真をフィルタ
        valid_photos = [
            photo for photo in photos 
            if photo.has_gps_data and photo.taken_date
        ]
        
        if len(valid_photos) < 2:
            return None
        
        # 撮影時刻でソート
        valid_photos.sort(key=lambda photo: photo.taken_date)
        
        # 異常な移動（高速移動など）を検出して除外
        filtered_photos = [valid_photos[0]]
        
        for i in range(1, len(valid_photos)):
            prev_photo = filtered_photos[-1]
            current_photo = valid_photos[i]
            
            # 時間差を計算
            time_diff = current_photo.taken_date - prev_photo.taken_date
            time_diff_hours = time_diff.total_seconds() / 3600
            
            # 距離を計算
            distance_km = prev_photo.distance_to_photo(current_photo)
            
            if distance_km is not None and time_diff_hours > 0:
                # 移動速度を計算（km/h）
                speed_kmh = distance_km / time_diff_hours
                
                # 異常に高速な移動（500km/h以上）は除外
                if speed_kmh < 500:
                    filtered_photos.append(current_photo)
            else:
                # 距離や時間が計算できない場合は含める
                filtered_photos.append(current_photo)
        
        return filtered_photos
    
    async def suggest_photo_clusters(
        self, 
        photos: List[Photo],
        time_threshold_hours: int = 24,
        distance_threshold_km: float = 10.0
    ) -> List[PhotoCollection]:
        """
        写真のクラスタリングを提案
        
        時間と位置の近さに基づいて、写真を自動的にグループ化します。
        
        Args:
            photos: 対象の写真
            time_threshold_hours: 時間の閾値（時間）
            distance_threshold_km: 距離の閾値（km）
            
        Returns:
            List[PhotoCollection]: 提案されたコレクション
        """
        if not photos:
            return []
        
        # GPS情報と撮影時刻の両方を持つ写真のみを対象
        valid_photos = [
            photo for photo in photos 
            if photo.has_gps_data and photo.taken_date
        ]
        
        if not valid_photos:
            return []
        
        # 撮影時刻でソート
        valid_photos.sort(key=lambda photo: photo.taken_date)
        
        clusters: List[List[Photo]] = []
        used_photos: Set[Photo] = set()
        
        for photo in valid_photos:
            if photo in used_photos:
                continue
            
            # 新しいクラスターを開始
            cluster = [photo]
            used_photos.add(photo)
            
            # 時間と位置が近い写真を追加
            for other_photo in valid_photos:
                if other_photo in used_photos:
                    continue
                
                # 時間差をチェック
                time_diff = abs((photo.taken_date - other_photo.taken_date).total_seconds())
                time_diff_hours = time_diff / 3600
                
                if time_diff_hours > time_threshold_hours:
                    continue
                
                # 距離をチェック
                distance = photo.distance_to_photo(other_photo)
                if distance is None or distance > distance_threshold_km:
                    continue
                
                cluster.append(other_photo)
                used_photos.add(other_photo)
            
            if len(cluster) > 1:  # 2枚以上の写真があるクラスターのみ保持
                clusters.append(cluster)
        
        # クラスターをPhotoCollectionに変換
        collections = []
        for i, cluster in enumerate(clusters, 1):
            # クラスター名を生成
            first_photo = min(cluster, key=lambda p: p.taken_date)
            date_str = first_photo.taken_date.strftime('%Y年%m月%d日')
            name = f"クラスター {i} - {date_str}"
            
            collection = PhotoCollection(name=name)
            for photo in cluster:
                collection.add_photo(photo)
            
            collections.append(collection)
        
        return collections
    
    async def calculate_photo_statistics(
        self, 
        photos: List[Photo]
    ) -> Dict[str, any]:
        """
        写真統計を計算
        
        Args:
            photos: 分析対象の写真
            
        Returns:
            Dict[str, any]: 統計情報
        """
        if not photos:
            return {
                'total_count': 0,
                'with_gps_count': 0,
                'without_gps_count': 0,
                'gps_coverage': 0.0,
                'date_range': None,
                'geographic_bounds': None,
                'file_formats': {},
                'total_size_mb': 0.0
            }
        
        # 基本統計
        photos_with_gps = [p for p in photos if p.has_gps_data]
        photos_with_date = [p for p in photos if p.taken_date]
        
        # 日付範囲
        date_range = None
        if photos_with_date:
            dates = [p.taken_date for p in photos_with_date]
            date_range = (min(dates), max(dates))
        
        # 地理的境界
        geographic_bounds = None
        if photos_with_gps:
            latitudes = [float(p.gps_coordinates.latitude) for p in photos_with_gps]
            longitudes = [float(p.gps_coordinates.longitude) for p in photos_with_gps]
            
            from decimal import Decimal
            min_lat, max_lat = min(latitudes), max(latitudes)
            min_lon, max_lon = min(longitudes), max(longitudes)
            
            sw = GPSCoordinates(Decimal(str(min_lat)), Decimal(str(min_lon)))
            ne = GPSCoordinates(Decimal(str(max_lat)), Decimal(str(max_lon)))
            geographic_bounds = (sw, ne)
        
        # ファイル形式統計
        file_formats = {}
        total_size = 0
        
        for photo in photos:
            ext = photo.file_extension
            file_formats[ext] = file_formats.get(ext, 0) + 1
            
            if photo.metadata:
                total_size += photo.metadata.file_size
        
        return {
            'total_count': len(photos),
            'with_gps_count': len(photos_with_gps),
            'without_gps_count': len(photos) - len(photos_with_gps),
            'gps_coverage': len(photos_with_gps) / len(photos) if photos else 0.0,
            'date_range': date_range,
            'geographic_bounds': geographic_bounds,
            'file_formats': file_formats,
            'total_size_mb': total_size / (1024 * 1024)
        }
    
    async def validate_photo_collection(
        self, 
        collection: PhotoCollection
    ) -> List[str]:
        """
        写真コレクションを検証
        
        Args:
            collection: 検証するコレクション
            
        Returns:
            List[str]: 検証エラーのリスト（空の場合は正常）
        """
        errors = []
        
        # コレクション名の検証
        if not collection.name or not collection.name.strip():
            errors.append("コレクション名が空です")
        
        # 写真の検証
        for i, photo in enumerate(collection.photos):
            try:
                # ファイルの存在確認
                if not photo.file_path.exists():
                    errors.append(f"写真 {i+1}: ファイルが存在しません - {photo.file_path}")
                
                # 画像ファイルの確認
                if not is_image_file(photo.file_path):
                    errors.append(f"写真 {i+1}: サポートされていないファイル形式 - {photo.file_extension}")
                
                # GPS座標の検証
                if photo.gps_coordinates:
                    lat = float(photo.gps_coordinates.latitude)
                    lon = float(photo.gps_coordinates.longitude)
                    
                    if not (-90 <= lat <= 90):
                        errors.append(f"写真 {i+1}: 無効な緯度 - {lat}")
                    
                    if not (-180 <= lon <= 180):
                        errors.append(f"写真 {i+1}: 無効な経度 - {lon}")
                
            except Exception as e:
                errors.append(f"写真 {i+1}: 検証エラー - {str(e)}")
        
        return errors
    
    async def optimize_collection_order(
        self, 
        collection: PhotoCollection,
        strategy: str = 'date'
    ) -> PhotoCollection:
        """
        コレクション内の写真順序を最適化
        
        Args:
            collection: 最適化するコレクション
            strategy: 最適化戦略 ('date', 'location', 'name')
            
        Returns:
            PhotoCollection: 最適化されたコレクション
        """
        if strategy == 'date':
            collection.sort_by_date()
        elif strategy == 'name':
            collection.sort_by_name()
        elif strategy == 'location':
            # 位置による最適化（travelling salesman problem の簡単な近似）
            await self._optimize_by_location(collection)
        else:
            raise ValidationError(f"未知の最適化戦略です: {strategy}")
        
        return collection
    
    async def _optimize_by_location(self, collection: PhotoCollection) -> None:
        """
        位置情報による最適化（簡単な最近傍法）
        """
        photos_with_gps = collection.photos_with_gps
        if len(photos_with_gps) < 2:
            return
        
        # GPS情報のない写真は最後に配置
        photos_without_gps = collection.photos_without_gps
        
        # 最近傍法で順序を最適化
        optimized = [photos_with_gps[0]]
        remaining = photos_with_gps[1:]
        
        while remaining:
            current = optimized[-1]
            nearest = min(remaining, key=lambda p: current.distance_to_photo(p) or float('inf'))
            optimized.append(nearest)
            remaining.remove(nearest)
        
        # 最適化された順序でコレクションを更新
        collection.clear()
        for photo in optimized + photos_without_gps:
            collection.add_photo(photo)
