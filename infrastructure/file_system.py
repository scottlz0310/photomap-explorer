"""
ファイルシステムアクセスインフラストラクチャ

画像ファイルの検索と管理を行う具象実装
"""

import os
from pathlib import Path
from typing import List, Set, Optional, Iterator
import asyncio

from ..utils.helpers import is_image_file, normalize_path
from ..utils.constants import SUPPORTED_IMAGE_EXTENSIONS
from ..utils.exceptions import InfrastructureError


class FileSystemService:
    """
    ファイルシステムサービス
    
    画像ファイルの検索、フィルタリング、ソート機能を提供
    """
    
    def __init__(self, supported_extensions: Optional[Set[str]] = None):
        """
        初期化
        
        Args:
            supported_extensions: サポートするファイル拡張子のセット
        """
        self.supported_extensions = supported_extensions or SUPPORTED_IMAGE_EXTENSIONS
    
    async def find_images_in_directory(
        self, 
        directory_path: Path, 
        recursive: bool = False,
        sort_by: str = 'name'
    ) -> List[Path]:
        """
        ディレクトリ内の画像ファイルを検索
        
        Args:
            directory_path: 検索対象のディレクトリ
            recursive: サブディレクトリも検索するか
            sort_by: ソート方法 ('name', 'date', 'size')
            
        Returns:
            List[Path]: 見つかった画像ファイルのパスリスト
        """
        if not directory_path.exists() or not directory_path.is_dir():
            return []
        
        try:
            image_paths = []
            
            if recursive:
                # 再帰的検索
                for root, _, files in os.walk(directory_path):
                    root_path = Path(root)
                    for file in files:
                        file_path = root_path / file
                        if self._is_supported_image(file_path):
                            image_paths.append(file_path)
            else:
                # 単一ディレクトリ検索
                for item in directory_path.iterdir():
                    if item.is_file() and self._is_supported_image(item):
                        image_paths.append(item)
            
            # ソート
            return self._sort_image_paths(image_paths, sort_by)
            
        except Exception as e:
            raise InfrastructureError(f"画像ファイル検索エラー: {e}") from e
    
    async def find_images_by_pattern(
        self, 
        directory_path: Path, 
        pattern: str,
        recursive: bool = False
    ) -> List[Path]:
        """
        パターンマッチングで画像ファイルを検索
        
        Args:
            directory_path: 検索対象のディレクトリ
            pattern: 検索パターン（ワイルドカード使用可）
            recursive: サブディレクトリも検索するか
            
        Returns:
            List[Path]: マッチした画像ファイルのパスリスト
        """
        if not directory_path.exists():
            return []
        
        try:
            if recursive:
                matched_files = list(directory_path.rglob(pattern))
            else:
                matched_files = list(directory_path.glob(pattern))
            
            # 画像ファイルのみをフィルタ
            image_files = [f for f in matched_files if self._is_supported_image(f)]
            
            return self._sort_image_paths(image_files, 'name')
            
        except Exception as e:
            raise InfrastructureError(f"パターン検索エラー: {e}") from e
    
    async def get_directory_structure(
        self, 
        directory_path: Path,
        max_depth: int = 3
    ) -> dict:
        """
        ディレクトリ構造を取得（画像ファイル数付き）
        
        Args:
            directory_path: 対象ディレクトリ
            max_depth: 最大探索深度
            
        Returns:
            dict: ディレクトリ構造の辞書
        """
        if not directory_path.exists() or not directory_path.is_dir():
            return {}
        
        try:
            return await self._build_directory_tree(directory_path, max_depth, 0)
        except Exception as e:
            raise InfrastructureError(f"ディレクトリ構造取得エラー: {e}") from e
    
    async def get_file_info(self, file_path: Path) -> dict:
        """
        ファイル情報を取得
        
        Args:
            file_path: ファイルパス
            
        Returns:
            dict: ファイル情報
        """
        if not file_path.exists():
            return {}
        
        try:
            stat = file_path.stat()
            return {
                'name': file_path.name,
                'size': stat.st_size,
                'modified_time': stat.st_mtime,
                'created_time': stat.st_ctime,
                'extension': file_path.suffix.lower(),
                'is_image': self._is_supported_image(file_path),
                'absolute_path': str(file_path.absolute())
            }
        except Exception as e:
            raise InfrastructureError(f"ファイル情報取得エラー: {e}") from e
    
    async def count_images_in_directory(
        self, 
        directory_path: Path, 
        recursive: bool = False
    ) -> int:
        """
        ディレクトリ内の画像ファイル数をカウント
        
        Args:
            directory_path: 対象ディレクトリ
            recursive: サブディレクトリも含めるか
            
        Returns:
            int: 画像ファイル数
        """
        if not directory_path.exists() or not directory_path.is_dir():
            return 0
        
        try:
            count = 0
            
            if recursive:
                for root, _, files in os.walk(directory_path):
                    root_path = Path(root)
                    count += sum(1 for file in files 
                               if self._is_supported_image(root_path / file))
            else:
                count = sum(1 for item in directory_path.iterdir() 
                          if item.is_file() and self._is_supported_image(item))
            
            return count
            
        except Exception as e:
            return 0
    
    def create_image_iterator(
        self, 
        directory_path: Path, 
        recursive: bool = False
    ) -> Iterator[Path]:
        """
        画像ファイルのイテレータを作成
        
        Args:
            directory_path: 対象ディレクトリ
            recursive: サブディレクトリも含めるか
            
        Yields:
            Path: 画像ファイルのパス
        """
        if not directory_path.exists() or not directory_path.is_dir():
            return
        
        try:
            if recursive:
                for root, _, files in os.walk(directory_path):
                    root_path = Path(root)
                    for file in files:
                        file_path = root_path / file
                        if self._is_supported_image(file_path):
                            yield file_path
            else:
                for item in directory_path.iterdir():
                    if item.is_file() and self._is_supported_image(item):
                        yield item
        except Exception:
            return
    
    def _is_supported_image(self, file_path: Path) -> bool:
        """
        サポートされている画像ファイルかを判定
        
        Args:
            file_path: ファイルパス
            
        Returns:
            bool: サポートされている場合True
        """
        return is_image_file(file_path)
    
    def _sort_image_paths(self, paths: List[Path], sort_by: str) -> List[Path]:
        """
        画像パスリストをソート
        
        Args:
            paths: パスリスト
            sort_by: ソート方法
            
        Returns:
            List[Path]: ソートされたパスリスト
        """
        if sort_by == 'name':
            return sorted(paths, key=lambda p: p.name.lower())
        elif sort_by == 'date':
            return sorted(paths, key=lambda p: p.stat().st_mtime, reverse=True)
        elif sort_by == 'size':
            return sorted(paths, key=lambda p: p.stat().st_size, reverse=True)
        else:
            return sorted(paths, key=lambda p: p.name.lower())
    
    async def _build_directory_tree(
        self, 
        directory_path: Path, 
        max_depth: int, 
        current_depth: int
    ) -> dict:
        """
        ディレクトリツリーを再帰的に構築
        
        Args:
            directory_path: ディレクトリパス
            max_depth: 最大深度
            current_depth: 現在の深度
            
        Returns:
            dict: ディレクトリツリー
        """
        if current_depth >= max_depth:
            return {}
        
        tree = {
            'name': directory_path.name,
            'path': str(directory_path),
            'image_count': await self.count_images_in_directory(directory_path, False),
            'subdirectories': {}
        }
        
        try:
            for item in directory_path.iterdir():
                if item.is_dir():
                    subtree = await self._build_directory_tree(
                        item, max_depth, current_depth + 1
                    )
                    tree['subdirectories'][item.name] = subtree
        except PermissionError:
            # アクセス権限がない場合はスキップ
            pass
        
        return tree


class ImageFileWatcher:
    """
    画像ファイルの変更監視クラス
    
    ディレクトリ内の画像ファイルの追加、削除、変更を監視します。
    """
    
    def __init__(self, directory_path: Path):
        """
        初期化
        
        Args:
            directory_path: 監視対象のディレクトリ
        """
        self.directory_path = directory_path
        self._file_system = FileSystemService()
        self._last_scan_time = None
        self._cached_files = set()
    
    async def scan_for_changes(self) -> dict:
        """
        変更をスキャン
        
        Returns:
            dict: 変更情報（added, removed, modified）
        """
        try:
            current_files = set(await self._file_system.find_images_in_directory(
                self.directory_path, recursive=True
            ))
            
            if self._cached_files is None:
                # 初回スキャン
                changes = {
                    'added': list(current_files),
                    'removed': [],
                    'modified': []
                }
            else:
                # 変更検出
                added = current_files - self._cached_files
                removed = self._cached_files - current_files
                
                changes = {
                    'added': list(added),
                    'removed': list(removed),
                    'modified': []  # 将来的にファイル変更時刻を監視
                }
            
            self._cached_files = current_files
            return changes
            
        except Exception as e:
            raise InfrastructureError(f"変更スキャンエラー: {e}") from e
    
    async def get_current_state(self) -> dict:
        """
        現在の状態を取得
        
        Returns:
            dict: 現在の状態情報
        """
        try:
            image_count = await self._file_system.count_images_in_directory(
                self.directory_path, recursive=True
            )
            
            return {
                'directory': str(self.directory_path),
                'image_count': image_count,
                'last_scan': self._last_scan_time,
                'is_monitoring': True
            }
            
        except Exception as e:
            raise InfrastructureError(f"状態取得エラー: {e}") from e
