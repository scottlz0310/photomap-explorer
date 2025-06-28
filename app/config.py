# Configuration management for PhotoMap Explorer
import os
from typing import Dict, Any
from enum import Enum

class ThumbnailSize(Enum):
    """サムネイルサイズの列挙型"""
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class WindowState(Enum):
    """ウィンドウ状態の列挙型"""
    NORMAL = "normal"
    MAXIMIZED_IMAGE = "maximized_image"
    MAXIMIZED_MAP = "maximized_map"

class AppConfig:
    """アプリケーション設定を管理するクラス"""
    
    # デフォルト設定
    DEFAULT_SETTINGS = {
        # ウィンドウ設定
        "window": {
            "width": 1400,
            "height": 900,
            "x": 100,
            "y": 100,
            "state": WindowState.NORMAL.value
        },
        # UI設定
        "ui": {
            "thumbnail_size": ThumbnailSize.MEDIUM.value,
            "splitter_sizes": [700, 200, 700],
            "thumbnail_icon_sizes": {
                ThumbnailSize.SMALL.value: {"width": 64, "height": 64, "panel_width": 124},
                ThumbnailSize.MEDIUM.value: {"width": 128, "height": 128, "panel_width": 188},
                ThumbnailSize.LARGE.value: {"width": 192, "height": 192, "panel_width": 252}
            }
        },
        # ファイル設定
        "files": {
            "supported_extensions": [".jpg", ".jpeg", ".png", ".bmp", ".gif"],
            "last_folder": "",
            "recent_folders": []
        },
        # 地図設定
        "map": {
            "default_zoom": 15,
            "marker_tooltip": "画像の位置"
        }
    }
    
    def __init__(self):
        self._settings = self.DEFAULT_SETTINGS.copy()
        self._config_file = os.path.join(os.path.expanduser("~"), ".photomap_explorer_config.json")
    
    def get(self, key_path: str, default=None) -> Any:
        """
        設定値を取得する
        
        Args:
            key_path: ドット記法のキーパス (例: "ui.thumbnail_size")
            default: デフォルト値
            
        Returns:
            設定値
        """
        keys = key_path.split('.')
        value = self._settings
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key_path: str, value: Any) -> None:
        """
        設定値を更新する
        
        Args:
            key_path: ドット記法のキーパス
            value: 設定値
        """
        keys = key_path.split('.')
        target = self._settings
        
        # 最後のキー以外のパスを辿る
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        # 最後のキーに値を設定
        target[keys[-1]] = value
    
    def get_thumbnail_config(self, size: ThumbnailSize) -> Dict[str, int]:
        """サムネイルサイズ設定を取得"""
        return self.get(f"ui.thumbnail_icon_sizes.{size.value}", {})
    
    def get_window_geometry(self) -> Dict[str, int]:
        """ウィンドウジオメトリを取得"""
        return self.get("window", {})
    
    def get_supported_extensions(self) -> list:
        """サポートされているファイル拡張子を取得"""
        return self.get("files.supported_extensions", [])
    
    def save_config(self) -> None:
        """設定をファイルに保存する（将来の実装用）"""
        # TODO: JSON形式で設定ファイルに保存
        pass
    
    def load_config(self) -> None:
        """設定をファイルから読み込む（将来の実装用）"""
        # TODO: JSON形式の設定ファイルから読み込み
        pass

# グローバル設定インスタンス
config = AppConfig()
