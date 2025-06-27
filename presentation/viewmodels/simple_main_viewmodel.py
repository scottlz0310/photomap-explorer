"""
シンプルなメインViewModelクラス
Clean Architecture - プレゼンテーション層
"""
from .base_viewmodel import BaseViewModel


class SimpleMainViewModel(BaseViewModel):
    """
    シンプルなメインViewModel（Phase 3テスト用）
    """
    
    def __init__(self):
        super().__init__()
        self._current_folder_path = ""
        self._image_paths = []
        self._selected_image_path = ""
    
    @property
    def current_folder_path(self):
        """現在のフォルダパス"""
        return self._current_folder_path
    
    @current_folder_path.setter
    def current_folder_path(self, value):
        if self._current_folder_path != value:
            old_value = self._current_folder_path
            self._current_folder_path = value
            self.property_changed.emit("current_folder_path", old_value, value)
    
    @property
    def image_paths(self):
        """画像ファイルパスのリスト"""
        return self._image_paths.copy()  # 防御的コピー
    
    @image_paths.setter
    def image_paths(self, value):
        old_value = self._image_paths.copy()
        self._image_paths = value.copy() if value else []
        self.property_changed.emit("image_paths", old_value, self._image_paths.copy())
    
    @property
    def selected_image_path(self):
        """選択された画像のパス"""
        return self._selected_image_path
    
    @selected_image_path.setter
    def selected_image_path(self, value):
        if self._selected_image_path != value:
            old_value = self._selected_image_path
            self._selected_image_path = value
            self.property_changed.emit("selected_image_path", old_value, value)
    
    @property
    def loading(self):
        """ローディング状態（デフォルトはFalse）"""
        return False
    
    def get_image_count(self):
        """画像の総数を取得"""
        return len(self._image_paths)
    
    def has_images(self):
        """画像があるかどうか"""
        return len(self._image_paths) > 0
    
    def has_selected_image(self):
        """画像が選択されているかどうか"""
        return bool(self._selected_image_path)
