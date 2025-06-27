"""
写真リポジトリの具象実装

ファイルシステムベースの写真データアクセス実装
"""

from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import asyncio

from domain.models.photo import Photo, GPSCoordinates
from domain.models.photo_collection import PhotoCollection
from domain.repositories.photo_repository import PhotoRepository, PhotoCollectionRepository
from .file_system import FileSystemService
from .exif_reader import ExifReader
from utils.exceptions import RepositoryError, InfrastructureError


class FileSystemPhotoRepository(PhotoRepository):
    """
    ファイルシステムベースの写真リポジトリ実装
    
    ファイルシステム上の画像ファイルを対象とした
    写真データのCRUD操作を提供
    """
    
    def __init__(self):
        self._file_system = FileSystemService()
        self._exif_reader = ExifReader()
        self._cache = {}  # 簡単なメモリキャッシュ
    
    async def find_by_path(self, file_path: Path) -> Optional[Photo]:
        """
        ファイルパスで写真を検索
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Optional[Photo]: 見つかった写真、または None
        """
        try:
            # キャッシュをチェック
            cache_key = str(file_path.absolute())
            if cache_key in self._cache:
                return self._cache[cache_key]
            
            if not file_path.exists() or not self._file_system._is_supported_image(file_path):
                return None
            
            # 写真オブジェクトを作成
            photo = await self._create_photo_from_file(file_path)
            
            # キャッシュに保存
            if photo:
                self._cache[cache_key] = photo
            
            return photo
            
        except Exception as e:
            raise RepositoryError(f"写真検索エラー: {e}") from e
    
    async def find_by_directory(self, directory_path: Path, recursive: bool = True) -> List[Photo]:
        """
        ディレクトリ内の写真を検索
        
        Args:
            directory_path: 検索対象のディレクトリ
            recursive: サブディレクトリも検索するか
            
        Returns:
            List[Photo]: 見つかった写真のリスト
        """
        try:
            # 画像ファイルを検索
            image_paths = await self._file_system.find_images_in_directory(
                directory_path, recursive, sort_by='name'
            )
            
            # 写真オブジェクトを並列作成
            photos = []
            for image_path in image_paths:
                photo = await self.find_by_path(image_path)
                if photo:
                    photos.append(photo)
            
            return photos
            
        except Exception as e:
            raise RepositoryError(f"ディレクトリ写真検索エラー: {e}") from e
    
    async def find_by_date_range(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Photo]:
        """
        撮影日時の範囲で写真を検索
        
        Note: この実装では全ファイルをスキャンするため効率が悪い
        実際のプロダクションではデータベースやインデックスを使用することを推奨
        """
        # TODO: 効率的な実装のためにはインデックスが必要
        raise NotImplementedError("日付範囲検索は将来実装予定")
    
    async def find_by_location(
        self, 
        center: GPSCoordinates,
        radius_km: float
    ) -> List[Photo]:
        """
        位置情報で写真を検索
        
        Note: この実装では全ファイルをスキャンするため効率が悪い
        """
        # TODO: 効率的な実装のためにはインデックスが必要
        raise NotImplementedError("位置検索は将来実装予定")
    
    async def find_photos_with_gps(self) -> List[Photo]:
        """
        GPS情報を持つ写真を全て取得
        
        Note: この実装では全ファイルをスキャンするため効率が悪い
        """
        # TODO: 効率的な実装のためにはインデックスが必要
        raise NotImplementedError("GPS写真検索は将来実装予定")
    
    async def find_photos_without_gps(self) -> List[Photo]:
        """
        GPS情報を持たない写真を全て取得
        
        Note: この実装では全ファイルをスキャンするため効率が悪い
        """
        # TODO: 効率的な実装のためにはインデックスが必要
        raise NotImplementedError("非GPS写真検索は将来実装予定")
    
    async def save(self, photo: Photo) -> Photo:
        """
        写真を保存（作成または更新）
        
        Note: ファイルシステムベースのリポジトリでは、
        写真ファイル自体は変更せず、メタデータのキャッシュのみ更新
        """
        try:
            cache_key = str(photo.file_path.absolute())
            self._cache[cache_key] = photo
            return photo
            
        except Exception as e:
            raise RepositoryError(f"写真保存エラー: {e}") from e
    
    async def save_many(self, photos: List[Photo]) -> List[Photo]:
        """
        複数の写真を一括保存
        """
        try:
            saved_photos = []
            for photo in photos:
                saved_photo = await self.save(photo)
                saved_photos.append(saved_photo)
            return saved_photos
            
        except Exception as e:
            raise RepositoryError(f"一括保存エラー: {e}") from e
    
    async def delete(self, photo: Photo) -> bool:
        """
        写真を削除
        
        Note: この実装ではキャッシュからのみ削除
        実際のファイル削除は別の操作として扱う
        """
        try:
            cache_key = str(photo.file_path.absolute())
            if cache_key in self._cache:
                del self._cache[cache_key]
            return True
            
        except Exception as e:
            raise RepositoryError(f"写真削除エラー: {e}") from e
    
    async def exists(self, file_path: Path) -> bool:
        """
        写真が存在するかを確認
        """
        try:
            return (file_path.exists() and 
                    self._file_system._is_supported_image(file_path))
        except Exception:
            return False
    
    async def count(self) -> int:
        """
        管理されている写真の総数を取得
        
        Note: この実装では正確な数を返せない
        """
        return len(self._cache)
    
    async def count_with_gps(self) -> int:
        """
        GPS情報を持つ写真の数を取得
        """
        count = 0
        for photo in self._cache.values():
            if photo.has_gps_data:
                count += 1
        return count
    
    async def _create_photo_from_file(self, file_path: Path) -> Optional[Photo]:
        """
        ファイルから写真オブジェクトを作成
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Optional[Photo]: 作成された写真オブジェクト
        """
        try:
            # EXIF情報を抽出
            exif_info = self._exif_reader.extract_all_info(file_path)
            
            # 写真オブジェクトを作成
            photo = Photo(
                file_path=file_path,
                taken_date=exif_info['taken_date'],
                gps_coordinates=exif_info['gps_coordinates'],
                metadata=exif_info['metadata']
            )
            
            return photo
            
        except Exception as e:
            # エラーが発生した場合は基本的な写真オブジェクトを作成
            try:
                return Photo(file_path=file_path)
            except:
                return None
    
    def clear_cache(self) -> None:
        """キャッシュをクリア"""
        self._cache.clear()
    
    def get_cache_size(self) -> int:
        """キャッシュサイズを取得"""
        return len(self._cache)


class InMemoryPhotoCollectionRepository(PhotoCollectionRepository):
    """
    インメモリ写真コレクションリポジトリ実装
    
    簡単な実装として、メモリ内でコレクションを管理
    将来的にはJSONファイルやデータベースに永続化することを想定
    """
    
    def __init__(self):
        self._collections: Dict[str, PhotoCollection] = {}
    
    async def find_by_name(self, name: str) -> Optional[PhotoCollection]:
        """
        名前でコレクションを検索
        """
        return self._collections.get(name)
    
    async def find_all(self) -> List[PhotoCollection]:
        """
        全てのコレクションを取得
        """
        return list(self._collections.values())
    
    async def save(self, collection: PhotoCollection) -> PhotoCollection:
        """
        コレクションを保存
        """
        try:
            self._collections[collection.name] = collection
            collection.updated_at = datetime.now()
            return collection
        except Exception as e:
            raise RepositoryError(f"コレクション保存エラー: {e}") from e
    
    async def delete(self, collection: PhotoCollection) -> bool:
        """
        コレクションを削除
        """
        try:
            if collection.name in self._collections:
                del self._collections[collection.name]
                return True
            return False
        except Exception as e:
            raise RepositoryError(f"コレクション削除エラー: {e}") from e
    
    async def exists(self, name: str) -> bool:
        """
        コレクションが存在するかを確認
        """
        return name in self._collections
    
    async def count(self) -> int:
        """
        コレクションの総数を取得
        """
        return len(self._collections)
    
    def clear(self) -> None:
        """全コレクションを削除"""
        self._collections.clear()


class SimpleCache:
    """
    簡単なメモリキャッシュ実装
    """
    
    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
    
    async def get(self, key: str) -> Optional[Any]:
        """キャッシュからデータを取得"""
        return self._cache.get(key)
    
    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """データをキャッシュに保存"""
        # 簡単な実装：TTLは無視、最大サイズチェックのみ
        if len(self._cache) >= self._max_size:
            # 最も古いアイテムを削除（簡単な実装）
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[key] = value
    
    async def delete(self, key: str) -> bool:
        """キャッシュからデータを削除"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def clear(self) -> None:
        """キャッシュを全てクリア"""
        self._cache.clear()
    
    async def exists(self, key: str) -> bool:
        """キャッシュにデータが存在するかを確認"""
        return key in self._cache
    
    async def get_size(self) -> int:
        """キャッシュのサイズを取得"""
        return len(self._cache)
