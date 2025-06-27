"""
写真コレクションモデル

複数の写真を管理し、検索・フィルタリング機能を提供するドメインモデル
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Iterator, Dict, Set, Tuple
from collections import defaultdict

from .photo import Photo, GPSCoordinates


@dataclass
class PhotoCollection:
    """
    写真コレクションエンティティ
    
    複数の写真を管理し、検索、フィルタリング、グループ化機能を提供
    """
    name: str
    photos: List[Photo] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_photo(self, photo: Photo) -> None:
        """写真を追加"""
        if photo not in self.photos:
            self.photos.append(photo)
            self.updated_at = datetime.now()
    
    def remove_photo(self, photo: Photo) -> bool:
        """
        写真を削除
        
        Returns:
            bool: 削除成功した場合True
        """
        try:
            self.photos.remove(photo)
            self.updated_at = datetime.now()
            return True
        except ValueError:
            return False
    
    def clear(self) -> None:
        """すべての写真を削除"""
        self.photos.clear()
        self.updated_at = datetime.now()
    
    def __len__(self) -> int:
        """写真の数を取得"""
        return len(self.photos)
    
    def __iter__(self) -> Iterator[Photo]:
        """イテレータ"""
        return iter(self.photos)
    
    def __contains__(self, photo: Photo) -> bool:
        """写真が含まれているかを確認"""
        return photo in self.photos
    
    @property
    def has_photos(self) -> bool:
        """写真が存在するかを確認"""
        return len(self.photos) > 0
    
    @property
    def photos_with_gps(self) -> List[Photo]:
        """GPS情報を持つ写真のリストを取得"""
        return [photo for photo in self.photos if photo.has_gps_data]
    
    @property
    def photos_without_gps(self) -> List[Photo]:
        """GPS情報を持たない写真のリストを取得"""
        return [photo for photo in self.photos if not photo.has_gps_data]
    
    @property
    def gps_coverage_ratio(self) -> float:
        """GPS情報を持つ写真の割合を計算"""
        if not self.photos:
            return 0.0
        return len(self.photos_with_gps) / len(self.photos)
    
    def get_date_range(self) -> Optional[Tuple[datetime, datetime]]:
        """
        撮影日時の範囲を取得
        
        Returns:
            Optional[Tuple[datetime, datetime]]: (最古, 最新)の撮影日時
        """
        photos_with_date = [photo for photo in self.photos if photo.taken_date]
        if not photos_with_date:
            return None
        
        dates = [photo.taken_date for photo in photos_with_date]
        return (min(dates), max(dates))
    
    def get_geographic_bounds(self) -> Optional[Tuple[GPSCoordinates, GPSCoordinates]]:
        """
        地理的境界を取得
        
        Returns:
            Optional[Tuple[GPSCoordinates, GPSCoordinates]]: (南西, 北東)の座標
        """
        photos_with_gps = self.photos_with_gps
        if not photos_with_gps:
            return None
        
        latitudes = [float(photo.gps_coordinates.latitude) for photo in photos_with_gps]
        longitudes = [float(photo.gps_coordinates.longitude) for photo in photos_with_gps]
        
        from decimal import Decimal
        min_lat, max_lat = min(latitudes), max(latitudes)
        min_lon, max_lon = min(longitudes), max(longitudes)
        
        sw_corner = GPSCoordinates(Decimal(str(min_lat)), Decimal(str(min_lon)))
        ne_corner = GPSCoordinates(Decimal(str(max_lat)), Decimal(str(max_lon)))
        
        return (sw_corner, ne_corner)
    
    def filter_by_date_range(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Photo]:
        """
        日付範囲でフィルタリング
        
        Args:
            start_date: 開始日時
            end_date: 終了日時
            
        Returns:
            List[Photo]: フィルタリングされた写真リスト
        """
        filtered_photos = []
        
        for photo in self.photos:
            if photo.taken_date is None:
                continue
            
            if start_date and photo.taken_date < start_date:
                continue
            
            if end_date and photo.taken_date > end_date:
                continue
            
            filtered_photos.append(photo)
        
        return filtered_photos
    
    def filter_by_location(
        self, 
        center: GPSCoordinates,
        radius_km: float
    ) -> List[Photo]:
        """
        位置でフィルタリング
        
        Args:
            center: 中心座標
            radius_km: 半径（km）
            
        Returns:
            List[Photo]: フィルタリングされた写真リスト
        """
        filtered_photos = []
        
        for photo in self.photos_with_gps:
            distance = center.distance_to(photo.gps_coordinates)
            if distance <= radius_km:
                filtered_photos.append(photo)
        
        return filtered_photos
    
    def group_by_date(self, group_by: str = 'day') -> Dict[str, List[Photo]]:
        """
        日付でグループ化
        
        Args:
            group_by: グループ化の単位 ('day', 'month', 'year')
            
        Returns:
            Dict[str, List[Photo]]: 日付キーと写真リストの辞書
        """
        if group_by not in ['day', 'month', 'year']:
            raise ValueError("group_byは 'day', 'month', 'year' のいずれかである必要があります")
        
        groups = defaultdict(list)
        
        for photo in self.photos:
            if photo.taken_date is None:
                groups['日付不明'].append(photo)
                continue
            
            if group_by == 'day':
                key = photo.taken_date.strftime('%Y-%m-%d')
            elif group_by == 'month':
                key = photo.taken_date.strftime('%Y-%m')
            else:  # year
                key = photo.taken_date.strftime('%Y')
            
            groups[key].append(photo)
        
        return dict(groups)
    
    def group_by_location(self, cluster_radius_km: float = 1.0) -> Dict[str, List[Photo]]:
        """
        位置でグループ化（簡単なクラスタリング）
        
        Args:
            cluster_radius_km: クラスターの半径（km）
            
        Returns:
            Dict[str, List[Photo]]: 位置名と写真リストの辞書
        """
        groups = defaultdict(list)
        processed: Set[Photo] = set()
        cluster_id = 1
        
        # GPS情報のない写真
        for photo in self.photos_without_gps:
            groups['位置情報なし'].append(photo)
        
        # GPS情報のある写真をクラスタリング
        for photo in self.photos_with_gps:
            if photo in processed:
                continue
            
            # 新しいクラスターを作成
            cluster_name = f"クラスター {cluster_id}"
            cluster_photos = [photo]
            processed.add(photo)
            
            # 同じクラスターに属する写真を検索
            for other_photo in self.photos_with_gps:
                if other_photo in processed:
                    continue
                
                # クラスター内のいずれかの写真から一定距離内にある場合、同じクラスターに追加
                for cluster_photo in cluster_photos:
                    distance = cluster_photo.distance_to_photo(other_photo)
                    if distance and distance <= cluster_radius_km:
                        cluster_photos.append(other_photo)
                        processed.add(other_photo)
                        break
            
            groups[cluster_name] = cluster_photos
            cluster_id += 1
        
        return dict(groups)
    
    def find_photos_near(self, target_photo: Photo, radius_km: float = 1.0) -> List[Photo]:
        """
        指定した写真の近くにある写真を検索
        
        Args:
            target_photo: 対象となる写真
            radius_km: 検索半径（km）
            
        Returns:
            List[Photo]: 近くにある写真のリスト
        """
        if not target_photo.has_gps_data:
            return []
        
        nearby_photos = []
        for photo in self.photos_with_gps:
            if photo == target_photo:
                continue
            
            if target_photo.is_nearby(photo, radius_km):
                nearby_photos.append(photo)
        
        return nearby_photos
    
    def get_statistics(self) -> Dict[str, any]:
        """
        コレクションの統計情報を取得
        
        Returns:
            Dict[str, any]: 統計情報
        """
        stats = {
            'total_photos': len(self.photos),
            'photos_with_gps': len(self.photos_with_gps),
            'photos_without_gps': len(self.photos_without_gps),
            'gps_coverage_ratio': self.gps_coverage_ratio,
            'date_range': self.get_date_range(),
            'geographic_bounds': self.get_geographic_bounds(),
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        # ファイル形式の統計
        extensions = defaultdict(int)
        total_size = 0
        
        for photo in self.photos:
            extensions[photo.file_extension] += 1
            if photo.metadata:
                total_size += photo.metadata.file_size
        
        stats['file_extensions'] = dict(extensions)
        stats['total_file_size'] = total_size
        
        return stats
    
    def sort_by_date(self, reverse: bool = False) -> None:
        """撮影日時でソート"""
        def date_key(photo: Photo):
            return photo.taken_date or datetime.min
        
        self.photos.sort(key=date_key, reverse=reverse)
        self.updated_at = datetime.now()
    
    def sort_by_name(self, reverse: bool = False) -> None:
        """ファイル名でソート"""
        self.photos.sort(key=lambda photo: photo.file_name, reverse=reverse)
        self.updated_at = datetime.now()
    
    def __str__(self) -> str:
        """文字列表現"""
        return f"PhotoCollection('{self.name}', {len(self.photos)} photos)"
    
    def __repr__(self) -> str:
        """デバッグ用の文字列表現"""
        return (f"PhotoCollection(name='{self.name}', "
                f"photos={len(self.photos)}, "
                f"with_gps={len(self.photos_with_gps)})")
