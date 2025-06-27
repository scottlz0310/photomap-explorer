"""
メインウィンドウコントローラー

ViewModelとViewの間の調整を行うコントローラー
UIイベントの処理とViewModelへの委譲を管理
"""

from pathlib import Path
from typing import Optional, List, Callable, Any
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QInputDialog
import logging

from ..viewmodels.main_viewmodel import MainWindowViewModel
from domain.models.photo import Photo
from utils.exceptions import PhotoMapExplorerError


class MainWindowController(QObject):
    """
    メインウィンドウのコントローラー
    
    ViewとViewModelの間の調整を行い、
    UIイベントをビジネスロジックに変換する
    """
    
    def __init__(self, viewmodel: MainWindowViewModel, parent=None):
        super().__init__(parent)
        self._viewmodel = viewmodel
        self._logger = logging.getLogger(self.__class__.__name__)
        self._view = None  # Viewは後で設定
        
        # ViewModelのシグナルに接続
        self._connect_viewmodel_signals()
    
    def set_view(self, view):
        """Viewを設定"""
        self._view = view
        self._logger.info("View set to controller")
    
    def _connect_viewmodel_signals(self):
        """ViewModelのシグナルに接続"""
        self._viewmodel.photos_loaded.connect(self._on_photos_loaded)
        self._viewmodel.photo_selected.connect(self._on_photo_selected)
        self._viewmodel.folder_changed.connect(self._on_folder_changed)
        self._viewmodel.map_generated.connect(self._on_map_generated)
        self._viewmodel.statistics_updated.connect(self._on_statistics_updated)
        self._viewmodel.error_occurred.connect(self._on_error_occurred)
        self._viewmodel.busy_state_changed.connect(self._on_busy_state_changed)
    
    # ===== ViewModelシグナルハンドラー =====
    
    @pyqtSlot(list)
    def _on_photos_loaded(self, photos: List[Photo]):
        """写真読み込み完了時の処理"""
        self._logger.info(f"Photos loaded: {len(photos)} photos")
        if self._view and hasattr(self._view, 'update_photo_list'):
            self._view.update_photo_list(photos)
    
    @pyqtSlot(object)
    def _on_photo_selected(self, photo: Photo):
        """写真選択時の処理"""
        self._logger.debug(f"Photo selected: {photo.file_name}")
        if self._view and hasattr(self._view, 'update_photo_selection'):
            self._view.update_photo_selection(photo)
    
    @pyqtSlot(str)
    def _on_folder_changed(self, folder_path: str):
        """フォルダ変更時の処理"""
        self._logger.info(f"Folder changed: {folder_path}")
        if self._view and hasattr(self._view, 'update_folder_display'):
            self._view.update_folder_display(folder_path)
    
    @pyqtSlot(str)
    def _on_map_generated(self, map_path: str):
        """地図生成完了時の処理"""
        self._logger.info(f"Map generated: {map_path}")
        if self._view and hasattr(self._view, 'display_map'):
            self._view.display_map(map_path)
    
    @pyqtSlot(dict)
    def _on_statistics_updated(self, statistics: dict):
        """統計情報更新時の処理"""
        self._logger.debug("Statistics updated")
        if self._view and hasattr(self._view, 'update_statistics_display'):
            self._view.update_statistics_display(statistics)
    
    @pyqtSlot(str, str)
    def _on_error_occurred(self, error_type: str, error_message: str):
        """エラー発生時の処理"""
        self._logger.error(f"{error_type}: {error_message}")
        if self._view:
            self._show_error_message(error_type, error_message)
    
    @pyqtSlot(bool)
    def _on_busy_state_changed(self, is_busy: bool):
        """ビジー状態変更時の処理"""
        if self._view and hasattr(self._view, 'set_busy_state'):
            self._view.set_busy_state(is_busy)
    
    # ===== パブリックメソッド（UIから呼び出される） =====
    
    def select_folder(self):
        """フォルダ選択ダイアログを表示"""
        try:
            # フォルダ選択ダイアログ
            folder_path = QFileDialog.getExistingDirectory(
                self._view,
                "フォルダを選択",
                str(Path.home()),
                QFileDialog.ShowDirsOnly
            )
            
            if folder_path:
                command = self._viewmodel.get_command("select_folder")
                if command and command.can_execute():
                    command.execute(folder_path)
                
        except Exception as e:
            self._logger.error(f"Error in select_folder: {e}")
            self._show_error_message("フォルダ選択エラー", str(e))
    
    def load_photos(self):
        """写真読み込みを実行"""
        try:
            command = self._viewmodel.get_command("load_photos")
            if command and command.can_execute():
                command.execute()
            else:
                self._show_warning_message("写真読み込み", "フォルダが選択されていません")
        except Exception as e:
            self._logger.error(f"Error in load_photos: {e}")
            self._show_error_message("写真読み込みエラー", str(e))
    
    def generate_map(self):
        """地図生成を実行"""
        try:
            command = self._viewmodel.get_command("generate_map")
            if command and command.can_execute():
                command.execute()
            else:
                self._show_warning_message("地図生成", "GPS情報付きの写真がありません")
        except Exception as e:
            self._logger.error(f"Error in generate_map: {e}")
            self._show_error_message("地図生成エラー", str(e))
    
    def select_photo(self, photo: Photo):
        """写真を選択"""
        try:
            self._viewmodel.selected_photo = photo
        except Exception as e:
            self._logger.error(f"Error in select_photo: {e}")
    
    def toggle_photo_selection(self, photo: Photo):
        """写真選択をトグル"""
        try:
            self._viewmodel.toggle_photo_selection(photo)
        except Exception as e:
            self._logger.error(f"Error in toggle_photo_selection: {e}")
    
    def clear_selection(self):
        """選択をクリア"""
        try:
            command = self._viewmodel.get_command("clear_selection")
            if command and command.can_execute():
                command.execute()
        except Exception as e:
            self._logger.error(f"Error in clear_selection: {e}")
    
    def create_collection(self):
        """コレクション作成ダイアログを表示"""
        try:
            if self._viewmodel.selected_photo_count == 0:
                self._show_warning_message("コレクション作成", "写真が選択されていません")
                return
            
            # コレクション名の入力ダイアログ
            collection_name, ok = QInputDialog.getText(
                self._view,
                "コレクション作成",
                f"コレクション名を入力してください\\n({self._viewmodel.selected_photo_count}枚の写真)",
                text="新しいコレクション"
            )
            
            if ok and collection_name.strip():
                command = self._viewmodel.get_command("create_collection")
                if command and command.can_execute():
                    command.execute(collection_name.strip())
                    
        except Exception as e:
            self._logger.error(f"Error in create_collection: {e}")
            self._show_error_message("コレクション作成エラー", str(e))
    
    def set_search_text(self, text: str):
        """検索テキストを設定"""
        try:
            self._viewmodel.search_text = text
        except Exception as e:
            self._logger.error(f"Error in set_search_text: {e}")
    
    def set_gps_filter(self, show_gps_only: bool):
        """GPSフィルターを設定"""
        try:
            self._viewmodel.show_gps_only = show_gps_only
        except Exception as e:
            self._logger.error(f"Error in set_gps_filter: {e}")
    
    def set_sort_options(self, sort_by: str, ascending: bool = True):
        """ソートオプションを設定"""
        try:
            self._viewmodel.sort_by = sort_by
            self._viewmodel.sort_ascending = ascending
        except Exception as e:
            self._logger.error(f"Error in set_sort_options: {e}")
    
    def set_thumbnail_size(self, size: str):
        """サムネイルサイズを設定"""
        try:
            self._viewmodel.thumbnail_size = size
        except Exception as e:
            self._logger.error(f"Error in set_thumbnail_size: {e}")
    
    def refresh_photos(self):
        """写真リストを更新"""
        try:
            # ViewModelの非同期メソッドを呼び出し
            import asyncio
            try:
                loop = asyncio.get_running_loop()
                loop.create_task(self._viewmodel.refresh_current_folder())
            except RuntimeError:
                # イベントループがない場合
                asyncio.run(self._viewmodel.refresh_current_folder())
        except Exception as e:
            self._logger.error(f"Error in refresh_photos: {e}")
            self._show_error_message("更新エラー", str(e))
    
    def navigate_to_parent_folder(self):
        """親フォルダに移動"""
        try:
            if self._viewmodel.current_folder_path:
                parent_path = self._viewmodel.current_folder_path.parent
                if parent_path.exists():
                    command = self._viewmodel.get_command("select_folder")
                    if command and command.can_execute():
                        command.execute(str(parent_path))
        except Exception as e:
            self._logger.error(f"Error in navigate_to_parent_folder: {e}")
    
    def open_folder_in_explorer(self):
        """フォルダをエクスプローラーで開く"""
        try:
            if self._viewmodel.current_folder_path:
                import os
                import platform
                
                path_str = str(self._viewmodel.current_folder_path)
                
                if platform.system() == "Windows":
                    os.startfile(path_str)
                elif platform.system() == "Darwin":  # macOS
                    os.system(f"open '{path_str}'")
                else:  # Linux
                    os.system(f"xdg-open '{path_str}'")
                    
        except Exception as e:
            self._logger.error(f"Error in open_folder_in_explorer: {e}")
            self._show_error_message("フォルダを開くエラー", str(e))
    
    # ===== プロパティアクセス =====
    
    @property
    def viewmodel(self) -> MainWindowViewModel:
        """ViewModelを取得"""
        return self._viewmodel
    
    def get_current_photos(self) -> List[Photo]:
        """現在の写真リストを取得"""
        return self._viewmodel.filtered_photos
    
    def get_selected_photo(self) -> Optional[Photo]:
        """選択された写真を取得"""
        return self._viewmodel.selected_photo
    
    def get_selected_photos(self) -> List[Photo]:
        """選択された写真リストを取得"""
        return self._viewmodel.selected_photos
    
    def get_statistics(self) -> dict:
        """統計情報を取得"""
        return self._viewmodel.statistics
    
    # ===== プライベートメソッド =====
    
    def _show_error_message(self, title: str, message: str):
        """エラーメッセージを表示"""
        if self._view:
            try:
                QMessageBox.critical(self._view, title, message)
            except Exception as e:
                self._logger.error(f"Error showing message box: {e}")
    
    def _show_warning_message(self, title: str, message: str):
        """警告メッセージを表示"""
        if self._view:
            try:
                QMessageBox.warning(self._view, title, message)
            except Exception as e:
                self._logger.error(f"Error showing warning box: {e}")
    
    def _show_info_message(self, title: str, message: str):
        """情報メッセージを表示"""
        if self._view:
            try:
                QMessageBox.information(self._view, title, message)
            except Exception as e:
                self._logger.error(f"Error showing info box: {e}")
    
    def cleanup(self):
        """クリーンアップ"""
        try:
            if self._viewmodel:
                self._viewmodel.dispose()
            self._logger.info("Controller cleanup completed")
        except Exception as e:
            self._logger.error(f"Error during cleanup: {e}")


class ControllerFactory:
    """
    コントローラーファクトリー
    
    コントローラーとViewModelの作成を管理
    """
    
    @staticmethod
    def create_main_controller() -> MainWindowController:
        """メインウィンドウコントローラーを作成"""
        try:
            viewmodel = MainWindowViewModel()
            controller = MainWindowController(viewmodel)
            return controller
        except Exception as e:
            logging.error(f"Error creating main controller: {e}")
            raise
    
    @staticmethod
    def create_main_controller_with_folder(folder_path: str) -> MainWindowController:
        """指定されたフォルダでメインウィンドウコントローラーを作成"""
        try:
            controller = ControllerFactory.create_main_controller()
            
            # フォルダを設定
            path = Path(folder_path)
            if path.exists() and path.is_dir():
                controller.viewmodel.current_folder_path = path
            
            return controller
        except Exception as e:
            logging.error(f"Error creating controller with folder: {e}")
            raise
