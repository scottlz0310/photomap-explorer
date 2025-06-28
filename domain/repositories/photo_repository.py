"""
写真リポジトリインターフェース

写真データのCRUD操作とクエリ機能を定義する抽象インターフェース
Clean Architectureにおけるリポジトリパターンの実装
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models.photo import Photo, GPSCoordinates
from ..models.photo_collection import PhotoCollection


class PhotoRepository(ABC):
    """
    写真リポジトリの抽象基底クラス
    
    データアクセス層の抽象化により、具体的な実装（ファイルシステム、データベースなど）
    から独立したドメインロジックを実現します。
    """
    
    @abstractmethod
    async def find_by_path(self, file_path: Path) -> Optional[Photo]:
        """
        ファイルパスで写真を検索
        
        Args:
            file_path: 写真ファイルのパス
            
        Returns:
            Optional[Photo]: 見つかった写真、または None
        """
        pass
    
    @abstractmethod
    async def find_by_directory(self, directory_path: Path, recursive: bool = True) -> List[Photo]:
        """
        ディレクトリ内の写真を検索
        
        Args:
            directory_path: 検索対象のディレクトリ
            recursive: サブディレクトリも検索するか
            
        Returns:
            List[Photo]: 見つかった写真のリスト
        """
        pass
    
    @abstractmethod
    async def find_by_date_range(
        self, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Photo]:
        """
        撮影日時の範囲で写真を検索
        
        Args:
            start_date: 開始日時
            end_date: 終了日時
            
        Returns:
            List[Photo]: 条件に合う写真のリスト
        """
        pass
    
    @abstractmethod
    async def find_by_location(
        self, 
        center: GPSCoordinates,
        radius_km: float
    ) -> List[Photo]:
        """
        位置情報で写真を検索
        
        Args:
            center: 中心座標
            radius_km: 検索半径（km）
            
        Returns:
            List[Photo]: 条件に合う写真のリスト
        """
        pass
    
    @abstractmethod
    async def find_photos_with_gps(self) -> List[Photo]:
        """
        GPS情報を持つ写真を全て取得
        
        Returns:
            List[Photo]: GPS情報を持つ写真のリスト
        """
        pass
    
    @abstractmethod
    async def find_photos_without_gps(self) -> List[Photo]:
        """
        GPS情報を持たない写真を全て取得
        
        Returns:
            List[Photo]: GPS情報を持たない写真のリスト
        """
        pass
    
    @abstractmethod
    async def save(self, photo: Photo) -> Photo:
        """
        写真を保存（作成または更新）
        
        Args:
            photo: 保存する写真
            
        Returns:
            Photo: 保存された写真
        """
        pass
    
    @abstractmethod
    async def save_many(self, photos: List[Photo]) -> List[Photo]:
        """
        複数の写真を一括保存
        
        Args:
            photos: 保存する写真のリスト
            
        Returns:
            List[Photo]: 保存された写真のリスト
        """
        pass
    
    @abstractmethod
    async def delete(self, photo: Photo) -> bool:
        """
        写真を削除
        
        Args:
            photo: 削除する写真
            
        Returns:
            bool: 削除成功した場合True
        """
        pass
    
    @abstractmethod
    async def exists(self, file_path: Path) -> bool:
        """
        写真が存在するかを確認
        
        Args:
            file_path: 確認するファイルパス
            
        Returns:
            bool: 存在する場合True
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        管理されている写真の総数を取得
        
        Returns:
            int: 写真の総数
        """
        pass
    
    @abstractmethod
    async def count_with_gps(self) -> int:
        """
        GPS情報を持つ写真の数を取得
        
        Returns:
            int: GPS情報を持つ写真の数
        """
        pass


class PhotoCollectionRepository(ABC):
    """
    写真コレクションリポジトリの抽象基底クラス
    
    写真コレクションの永続化と取得を管理します。
    """
    
    @abstractmethod
    async def find_by_name(self, name: str) -> Optional[PhotoCollection]:
        """
        名前でコレクションを検索
        
        Args:
            name: コレクション名
            
        Returns:
            Optional[PhotoCollection]: 見つかったコレクション、または None
        """
        pass
    
    @abstractmethod
    async def find_all(self) -> List[PhotoCollection]:
        """
        全てのコレクションを取得
        
        Returns:
            List[PhotoCollection]: コレクションのリスト
        """
        pass
    
    @abstractmethod
    async def save(self, collection: PhotoCollection) -> PhotoCollection:
        """
        コレクションを保存
        
        Args:
            collection: 保存するコレクション
            
        Returns:
            PhotoCollection: 保存されたコレクション
        """
        pass
    
    @abstractmethod
    async def delete(self, collection: PhotoCollection) -> bool:
        """
        コレクションを削除
        
        Args:
            collection: 削除するコレクション
            
        Returns:
            bool: 削除成功した場合True
        """
        pass
    
    @abstractmethod
    async def exists(self, name: str) -> bool:
        """
        コレクションが存在するかを確認
        
        Args:
            name: コレクション名
            
        Returns:
            bool: 存在する場合True
        """
        pass
    
    @abstractmethod
    async def count(self) -> int:
        """
        コレクションの総数を取得
        
        Returns:
            int: コレクションの総数
        """
        pass


class CacheRepository(ABC):
    """
    キャッシュリポジトリの抽象基底クラス
    
    写真のメタデータやサムネイルなどのキャッシュデータを管理します。
    """
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """
        キャッシュからデータを取得
        
        Args:
            key: キャッシュキー
            
        Returns:
            Optional[Any]: キャッシュされたデータ、または None
        """
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """
        データをキャッシュに保存
        
        Args:
            key: キャッシュキー
            value: 保存するデータ
            ttl_seconds: 有効期限（秒）、Noneの場合は無期限
        """
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """
        キャッシュからデータを削除
        
        Args:
            key: キャッシュキー
            
        Returns:
            bool: 削除成功した場合True
        """
        pass
    
    @abstractmethod
    async def clear(self) -> None:
        """
        キャッシュを全てクリア
        """
        pass
    
    @abstractmethod
    async def exists(self, key: str) -> bool:
        """
        キャッシュにデータが存在するかを確認
        
        Args:
            key: キャッシュキー
            
        Returns:
            bool: 存在する場合True
        """
        pass
    
    @abstractmethod
    async def get_size(self) -> int:
        """
        キャッシュのサイズを取得
        
        Returns:
            int: キャッシュのアイテム数
        """
        pass
