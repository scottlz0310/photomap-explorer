"""
メインウィンドウViewModel

アプリケーションのメイン画面を制御するViewModel
写真の読み込み、表示、フィルタリングなどの機能を管理
"""

import asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
from PyQt5.QtCore import pyqtSignal

from .base_viewmodel import BaseViewModel, ObservableProperty, Command, AsyncCommand
from domain.models.photo import Photo
from domain.models.photo_collection import PhotoCollection
from domain.services.photo_domain_service import PhotoDomainService
from infrastructure.repositories import FileSystemPhotoRepository, InMemoryPhotoCollectionRepository
from infrastructure.file_system import FileSystemService
from infrastructure.map_generator import MapGenerator
from utils.exceptions import RepositoryError, DomainError


class MainWindowViewModel(BaseViewModel):
    """
    メインウィンドウのViewModel
    
    アプリケーションの中核となる機能を管理:
    - フォルダ選択と画像読み込み
    - 写真リストの管理
    - 選択された写真の管理
    - 地図生成
    - フィルタリング
    """
    
    # 追加のシグナル
    photos_loaded = pyqtSignal(list)  # 写真が読み込まれた時
    photo_selected = pyqtSignal(object)  # 写真が選択された時
    folder_changed = pyqtSignal(str)  # フォルダが変更された時
    map_generated = pyqtSignal(str)  # 地図が生成された時
    statistics_updated = pyqtSignal(dict)  # 統計情報が更新された時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # サービスとリポジトリの初期化
        self._photo_repository = FileSystemPhotoRepository()
        self._collection_repository = InMemoryPhotoCollectionRepository()
        self._domain_service = PhotoDomainService(
            self._photo_repository, 
            self._collection_repository
        )
        self._file_system_service = FileSystemService()
        self._map_generator = MapGenerator()
        
        # プロパティの初期化
        self._current_folder_path: Optional[Path] = None
        self._photos: List[Photo] = []
        self._filtered_photos: List[Photo] = []
        self._selected_photo: Optional[Photo] = None
        self._selected_photos: List[Photo] = []
        self._current_collection: Optional[PhotoCollection] = None
        self._search_text: str = ""
        self._show_gps_only: bool = False
        self._sort_by: str = "name"  # "name", "date", "size"
        self._sort_ascending: bool = True
        self._thumbnail_size: str = "medium"  # "small", "medium", "large"
        self._statistics: Dict[str, Any] = {}
        
        # コマンドの設定
        self._setup_commands()
        
        # 初期状態の設定
        self._update_filtered_photos()
    
    # ===== プロパティ =====
    
    @property
    def current_folder_path(self) -> Optional[Path]:
        """現在のフォルダパス"""
        return self._current_folder_path
    
    @current_folder_path.setter
    def current_folder_path(self, value: Optional[Path]):
        if self._current_folder_path != value:
            self._current_folder_path = value
            if value:
                self.folder_changed.emit(str(value))
                # 新しいフォルダの写真を非同期で読み込み
                asyncio.create_task(self.load_photos_from_folder(value))
    
    @property
    def photos(self) -> List[Photo]:
        """全写真リスト"""
        return self._photos.copy()
    
    @property
    def filtered_photos(self) -> List[Photo]:
        """フィルタリングされた写真リスト"""
        return self._filtered_photos.copy()
    
    @property
    def selected_photo(self) -> Optional[Photo]:
        """選択された写真"""
        return self._selected_photo
    
    @selected_photo.setter
    def selected_photo(self, value: Optional[Photo]):
        if self._selected_photo != value:
            self._selected_photo = value
            if value:
                self.photo_selected.emit(value)
                self.log_info(f"Photo selected: {value.file_name}")
    
    @property
    def selected_photos(self) -> List[Photo]:
        """複数選択された写真リスト"""
        return self._selected_photos.copy()
    
    @property
    def search_text(self) -> str:
        """検索テキスト"""
        return self._search_text
    
    @search_text.setter
    def search_text(self, value: str):
        if self._search_text != value:
            self._search_text = value
            self._update_filtered_photos()
    
    @property
    def show_gps_only(self) -> bool:
        """GPS情報のみ表示フラグ"""
        return self._show_gps_only
    
    @show_gps_only.setter
    def show_gps_only(self, value: bool):
        if self._show_gps_only != value:
            self._show_gps_only = value
            self._update_filtered_photos()
    
    @property
    def sort_by(self) -> str:
        """ソート基準"""
        return self._sort_by
    
    @sort_by.setter
    def sort_by(self, value: str):
        if self._sort_by != value and value in ["name", "date", "size"]:
            self._sort_by = value
            self._update_filtered_photos()
    
    @property
    def sort_ascending(self) -> bool:
        """昇順ソートフラグ"""
        return self._sort_ascending
    
    @sort_ascending.setter
    def sort_ascending(self, value: bool):
        if self._sort_ascending != value:
            self._sort_ascending = value
            self._update_filtered_photos()
    
    @property
    def thumbnail_size(self) -> str:
        """サムネイルサイズ"""
        return self._thumbnail_size
    
    @thumbnail_size.setter
    def thumbnail_size(self, value: str):
        if self._thumbnail_size != value and value in ["small", "medium", "large"]:
            self._thumbnail_size = value
    
    @property
    def statistics(self) -> Dict[str, Any]:
        """統計情報"""
        return self._statistics.copy()
    
    @property
    def photo_count(self) -> int:
        """写真総数"""
        return len(self._photos)
    
    @property
    def filtered_photo_count(self) -> int:
        """フィルタリング後の写真数"""
        return len(self._filtered_photos)
    
    @property
    def gps_photo_count(self) -> int:
        """GPS情報付き写真数"""
        return len([p for p in self._photos if p.has_gps_data])
    
    @property
    def selected_photo_count(self) -> int:
        """選択された写真数"""
        return len(self._selected_photos)
    
    # ===== コマンド設定 =====
    
    def _setup_commands(self):
        """コマンドを設定"""
        # フォルダ選択コマンド
        self.add_command("select_folder", AsyncCommand(
            self._execute_select_folder,
            lambda: not self.is_busy
        ))
        
        # 写真読み込みコマンド
        self.add_command("load_photos", AsyncCommand(
            self._execute_load_photos,
            lambda: not self.is_busy and self._current_folder_path is not None
        ))
        
        # 地図生成コマンド
        self.add_command("generate_map", AsyncCommand(
            self._execute_generate_map,
            lambda: not self.is_busy and self.gps_photo_count > 0
        ))
        
        # 統計情報更新コマンド
        self.add_command("update_statistics", AsyncCommand(
            self._execute_update_statistics,
            lambda: not self.is_busy and self.photo_count > 0
        ))
        
        # 写真選択クリアコマンド
        self.add_command("clear_selection", Command(
            self._execute_clear_selection,
            lambda: self.selected_photo_count > 0
        ))
        
        # コレクション作成コマンド
        self.add_command("create_collection", AsyncCommand(
            self._execute_create_collection,
            lambda: not self.is_busy and self.selected_photo_count > 0
        ))
    
    # ===== コマンド実行メソッド =====
    
    async def _execute_select_folder(self, folder_path: str = None):
        """フォルダ選択を実行"""
        try:
            self.is_busy = True
            
            if folder_path:
                path = Path(folder_path)
            else:
                # UI側でフォルダ選択ダイアログを表示
                # 実際の実装ではQFileDialogなどを使用
                return
            
            if path.exists() and path.is_dir():
                self.current_folder_path = path
                self.log_info(f"Folder selected: {path}")
            else:
                self.add_error(f"Invalid folder path: {path}")
        
        except Exception as e:
            self.handle_exception(e, "Select folder")
        finally:
            self.is_busy = False
    
    async def _execute_load_photos(self):
        """写真読み込みを実行"""
        try:
            self.is_busy = True
            self.clear_errors()
            
            if not self._current_folder_path:
                return
            
            # 写真を読み込み
            photos = await self._photo_repository.find_by_directory(
                self._current_folder_path, recursive=True
            )
            
            self._photos = photos
            self._update_filtered_photos()
            
            # 統計情報を更新
            await self._update_statistics()
            
            self.photos_loaded.emit(photos)
            self.log_info(f"Loaded {len(photos)} photos from {self._current_folder_path}")
        
        except Exception as e:
            self.handle_exception(e, "Load photos")
        finally:
            self.is_busy = False
    
    async def _execute_generate_map(self):
        """地図生成を実行"""
        try:
            self.is_busy = True
            
            # GPS情報付きの写真を取得
            gps_photos = [p for p in self._filtered_photos if p.has_gps_data]
            
            if not gps_photos:
                self.add_error("GPS情報付きの写真がありません")
                return
            
            # 地図を生成
            if len(gps_photos) == 1:
                map_path = self._map_generator.generate_single_photo_map(gps_photos[0])
            else:
                map_path = self._map_generator.generate_multi_photo_map(gps_photos)
            
            self.map_generated.emit(str(map_path))
            self.log_info(f"Map generated: {map_path}")
        
        except Exception as e:
            self.handle_exception(e, "Generate map")
        finally:
            self.is_busy = False
    
    async def _execute_update_statistics(self):
        """統計情報更新を実行"""
        try:
            self.is_busy = True
            
            # 統計情報を計算
            stats = await self._domain_service.calculate_photo_statistics(self._photos)
            self._statistics = stats
            
            self.statistics_updated.emit(stats)
            self.log_info("Statistics updated")
        
        except Exception as e:
            self.handle_exception(e, "Update statistics")
        finally:
            self.is_busy = False
    
    def _execute_clear_selection(self):
        """選択クリアを実行"""
        self._selected_photos.clear()
        self.selected_photo = None
        self.log_info("Selection cleared")
    
    async def _execute_create_collection(self, collection_name: str = "新しいコレクション"):
        """コレクション作成を実行"""
        try:
            self.is_busy = True
            
            # コレクションを作成
            collection = PhotoCollection(name=collection_name)
            for photo in self._selected_photos:
                collection.add_photo(photo)
            
            # リポジトリに保存
            await self._collection_repository.save(collection)
            
            self._current_collection = collection
            self.log_info(f"Collection created: {collection_name} with {len(self._selected_photos)} photos")
        
        except Exception as e:
            self.handle_exception(e, "Create collection")
        finally:
            self.is_busy = False
    
    # ===== パブリックメソッド =====
    
    async def load_photos_from_folder(self, folder_path: Path):
        """指定されたフォルダから写真を読み込み"""
        self.current_folder_path = folder_path
        command = self.get_command("load_photos")
        if command and command.can_execute():
            await command.execute()
    
    def add_photo_to_selection(self, photo: Photo):
        """写真を選択に追加"""
        if photo not in self._selected_photos:
            self._selected_photos.append(photo)
            self.selected_photo = photo
    
    def remove_photo_from_selection(self, photo: Photo):
        """写真を選択から削除"""
        if photo in self._selected_photos:
            self._selected_photos.remove(photo)
            if self.selected_photo == photo:
                self.selected_photo = self._selected_photos[0] if self._selected_photos else None
    
    def toggle_photo_selection(self, photo: Photo):
        """写真選択をトグル"""
        if photo in self._selected_photos:
            self.remove_photo_from_selection(photo)
        else:
            self.add_photo_to_selection(photo)
    
    def get_photo_at_index(self, index: int) -> Optional[Photo]:
        """インデックス指定で写真を取得"""
        if 0 <= index < len(self._filtered_photos):
            return self._filtered_photos[index]
        return None
    
    def get_photo_index(self, photo: Photo) -> int:
        """写真のインデックスを取得"""
        try:
            return self._filtered_photos.index(photo)
        except ValueError:
            return -1
    
    async def refresh_current_folder(self):
        """現在のフォルダを再読み込み"""
        if self._current_folder_path:
            await self.load_photos_from_folder(self._current_folder_path)
    
    # ===== プライベートメソッド =====
    
    def _update_filtered_photos(self):
        """フィルタリングされた写真リストを更新"""
        filtered = self._photos.copy()
        
        # GPS情報フィルタ
        if self._show_gps_only:
            filtered = [p for p in filtered if p.has_gps_data]
        
        # 検索テキストフィルタ
        if self._search_text:
            search_lower = self._search_text.lower()
            filtered = [p for p in filtered if search_lower in p.file_name.lower()]
        
        # ソート
        if self._sort_by == "name":
            filtered.sort(key=lambda p: p.file_name.lower(), reverse=not self._sort_ascending)
        elif self._sort_by == "date":
            filtered.sort(
                key=lambda p: p.taken_date or Path(p.file_path).stat().st_mtime,
                reverse=not self._sort_ascending
            )
        elif self._sort_by == "size":
            filtered.sort(
                key=lambda p: p.metadata.file_size if p.metadata else 0,
                reverse=not self._sort_ascending
            )
        
        self._filtered_photos = filtered
        self.log_debug(f"Filtered photos updated: {len(filtered)} photos")
    
    async def _update_statistics(self):
        """統計情報を更新"""
        command = self.get_command("update_statistics")
        if command and command.can_execute():
            await command.execute()
    
    # ===== オーバーライドメソッド =====
    
    def validate(self) -> bool:
        """状態検証"""
        return True
    
    def reset(self):
        """状態リセット"""
        super().reset()
        self._photos.clear()
        self._filtered_photos.clear()
        self._selected_photos.clear()
        self.selected_photo = None
        self._current_collection = None
        self._statistics.clear()
        self._search_text = ""
        self._show_gps_only = False
    
    def dispose(self):
        """リソース解放"""
        super().dispose()
        self._map_generator.cleanup_temp_files()
        self._photo_repository.clear_cache()
