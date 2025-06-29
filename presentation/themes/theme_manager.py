"""
テーマ管理システム - PhotoMap Explorer

ダークモード・ライトモードの切り替えとスタイル管理
"""

from enum import Enum
from typing import Dict, Any
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
import json
import os


class ThemeMode(Enum):
    """テーマモード"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"  # システム設定に従う


class ThemeManager(QObject):
    """
    テーマ管理クラス
    
    ダークモード・ライトモードの切り替えと
    アプリケーション全体のスタイル管理
    """
    
    # テーマ変更シグナル
    theme_changed = pyqtSignal(str)  # theme_name
    
    def __init__(self):
        super().__init__()
        self.current_theme = ThemeMode.LIGHT
        self.settings_file = self._get_settings_path()
        
        # テーマ定義
        self.themes = {
            ThemeMode.LIGHT: self._create_light_theme(),
            ThemeMode.DARK: self._create_dark_theme()
        }
        
        # 設定読み込み
        self._load_settings()
    
    def _get_settings_path(self) -> str:
        """設定ファイルパス取得"""
        app_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        settings_dir = os.path.join(app_dir, "settings")
        os.makedirs(settings_dir, exist_ok=True)
        return os.path.join(settings_dir, "theme_settings.json")
    
    def _create_light_theme(self) -> Dict[str, Any]:
        """ライトテーマ定義"""
        return {
            "name": "light",
            "display_name": "ライトモード",
            "colors": {
                "background": "#ffffff",
                "foreground": "#000000",
                "primary": "#007acc",
                "secondary": "#f8f8f8",
                "accent": "#0078d4",
                "border": "#ddd",
                "error": "#e74c3c",
                "warning": "#f39c12",
                "success": "#27ae60",
                "info": "#3498db",
                "muted": "#666",
                "hover": "#e6f3ff",
                "selection": "#cce8ff",
                "button_bg": "#f0f0f0",
                "button_hover": "#e0e0e0",
                "input_bg": "#ffffff",
                "input_border": "#ccc",
                "group_bg": "#f8f8f8",
                "status_bg": "#f8f8f8"
            },
            "styles": {
                "main_window": """
QMainWindow {{
    background-color: {background};
    color: {foreground};
}}
                """,
                "group_box": """
QGroupBox {{
    font-size: 12px;
    font-weight: bold;
    background-color: {background};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 5px;
    margin: 5px 0;
    padding-top: 10px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
}}
                """,
                "button": """
QPushButton {{
    background-color: {button_bg};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 11px;
}}
QPushButton:hover {{
    background-color: {button_hover};
    border-color: {accent};
}}
QPushButton:pressed {{
    background-color: {selection};
}}
                """,
                "maximize_button": """
QPushButton {{
    background: rgba(255, 255, 255, 0.9);
    color: #333;
    border: 1px solid #ccc;
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
    padding: 0;
    width: 30px;
    height: 30px;
}}
QPushButton:hover {{
    background: rgba(0, 120, 212, 0.9);
    color: white;
    border-color: #0078d4;
}}
                """,
                "status_info": """
QLabel {{
    padding: 10px;
    background: {status_bg};
    border: 1px solid {border};
    border-radius: 5px;
    font-size: 11px;
    line-height: 1.4;
    color: {foreground};
}}
                """,
                "list_widget": """
QListWidget {{
    background-color: {background};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 3px;
    selection-background-color: {selection};
    alternate-background-color: {secondary};
}}
QListWidget::item {{
    padding: 5px;
    border-bottom: 1px solid {border};
}}
QListWidget::item:hover {{
    background-color: {hover};
}}
QListWidget::item:selected {{
    background-color: {selection};
    color: {foreground};
}}
                """,
                "panel": """
QWidget {{
    background-color: {background};
    color: {foreground};
}}
                """
            }
        }
    
    def _create_dark_theme(self) -> Dict[str, Any]:
        """ダークテーマ定義"""
        return {
            "name": "dark",
            "display_name": "ダークモード",
            "colors": {
                "background": "#2b2b2b",
                "foreground": "#ffffff",
                "primary": "#4fc3f7",
                "secondary": "#3c3c3c",
                "accent": "#29b6f6",
                "border": "#555",
                "error": "#f44336",
                "warning": "#ff9800",
                "success": "#4caf50",
                "info": "#2196f3",
                "muted": "#aaa",
                "hover": "#404040",
                "selection": "#1e88e5",
                "button_bg": "#3c3c3c",
                "button_hover": "#484848",
                "input_bg": "#2b2b2b",
                "input_border": "#555",
                "group_bg": "#353535",
                "status_bg": "#353535"
            },
            "styles": {
                "main_window": """
QMainWindow {{
    background-color: {background};
    color: {foreground};
}}
                """,
                "group_box": """
QGroupBox {{
    font-size: 12px;
    font-weight: bold;
    background-color: {background};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 5px;
    margin: 5px 0;
    padding-top: 10px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px 0 5px;
    color: {foreground};
}}
                """,
                "button": """
QPushButton {{
    background-color: {button_bg};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 11px;
}}
QPushButton:hover {{
    background-color: {button_hover};
    border-color: {accent};
}}
QPushButton:pressed {{
    background-color: {selection};
}}
                """,
                "maximize_button": """
QPushButton {{
    background: rgba(60, 60, 60, 0.9);
    color: #fff;
    border: 1px solid #666;
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
    padding: 0;
    width: 30px;
    height: 30px;
}}
QPushButton:hover {{
    background: rgba(41, 182, 246, 0.9);
    color: white;
    border-color: #29b6f6;
}}
                """,
                "status_info": """
QLabel {{
    padding: 10px;
    background: {status_bg};
    border: 1px solid {border};
    border-radius: 5px;
    font-size: 11px;
    line-height: 1.4;
    color: {foreground};
}}
                """,
                "list_widget": """
QListWidget {{
    background-color: {background};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 3px;
    selection-background-color: {selection};
    alternate-background-color: {secondary};
}}
QListWidget::item {{
    padding: 5px;
    border-bottom: 1px solid {border};
    color: {foreground};
}}
QListWidget::item:hover {{
    background-color: {hover};
}}
QListWidget::item:selected {{
    background-color: {selection};
    color: white;
}}
                """,
                "panel": """
QWidget {{
    background-color: {background};
    color: {foreground};
}}
                """
            }
        }
    
    def get_current_theme(self) -> ThemeMode:
        """現在のテーマを取得"""
        return self.current_theme
    
    def set_theme(self, theme: ThemeMode):
        """テーマを設定"""
        if theme != self.current_theme:
            self.current_theme = theme
            self._save_settings()
            self.theme_changed.emit(theme.value)
    
    def toggle_theme(self):
        """テーマを切り替え"""
        if self.current_theme == ThemeMode.LIGHT:
            self.set_theme(ThemeMode.DARK)
        else:
            self.set_theme(ThemeMode.LIGHT)
    
    def get_theme_data(self, theme: ThemeMode = None) -> Dict[str, Any]:
        """テーマデータ取得"""
        theme = theme or self.current_theme
        return self.themes.get(theme, self.themes[ThemeMode.LIGHT])
    
    def get_style(self, component: str, theme: ThemeMode = None) -> str:
        """コンポーネントのスタイル取得"""
        theme_data = self.get_theme_data(theme)
        style_template = theme_data["styles"].get(component, "")
        colors = theme_data["colors"]
        
        # カラー変数を置換
        try:
            return style_template.format(**colors)
        except KeyError as e:
            print(f"テーマスタイル警告: {component} で未定義カラー {e}")
            return style_template
    
    def get_color(self, color_name: str, theme: ThemeMode = None) -> str:
        """カラー値取得"""
        theme_data = self.get_theme_data(theme)
        return theme_data["colors"].get(color_name, "#000000")
    
    def _load_settings(self):
        """設定読み込み"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    theme_name = settings.get("theme", "light")
                    try:
                        self.current_theme = ThemeMode(theme_name)
                    except ValueError:
                        self.current_theme = ThemeMode.LIGHT
        except Exception as e:
            print(f"テーマ設定読み込みエラー: {e}")
            self.current_theme = ThemeMode.LIGHT
    
    def _save_settings(self):
        """設定保存"""
        try:
            settings = {
                "theme": self.current_theme.value,
                "version": "2.1.0"
            }
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"テーマ設定保存エラー: {e}")
    
    def detect_system_theme(self) -> ThemeMode:
        """
        Windowsシステム設定からテーマモードを検出
        
        Returns:
            ThemeMode: システム設定に基づくテーマモード
        """
        try:
            import sys
            if sys.platform == "win32":
                # Windowsレジストリからダークモード設定を読み取り
                try:
                    import winreg
                    
                    # システムのダークモード設定を確認
                    key_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                    
                    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:
                        # AppsUseLightTheme: 0=ダーク, 1=ライト
                        apps_light_theme = winreg.QueryValueEx(key, "AppsUseLightTheme")[0]
                        
                        if apps_light_theme == 0:
                            return ThemeMode.DARK
                        else:
                            return ThemeMode.LIGHT
                            
                except (ImportError, OSError, FileNotFoundError, winreg.error) as e:
                    print(f"Windows設定読み取りエラー: {e}")
                    return ThemeMode.LIGHT  # フォールバック
            else:
                # Windows以外のOSの場合
                return ThemeMode.LIGHT
                
        except Exception as e:
            print(f"システムテーマ検出エラー: {e}")
            return ThemeMode.LIGHT
    
    def set_theme_with_system_detection(self, theme_mode: ThemeMode = None):
        """
        システム設定を考慮したテーマ設定
        
        Args:
            theme_mode: 明示的なテーマモード（Noneの場合はシステム設定を使用）
        """
        if theme_mode is None:
            # システム設定から自動検出
            detected_theme = self.detect_system_theme()
            self.set_theme(detected_theme)
        else:
            self.set_theme(theme_mode)


# グローバルテーママネージャー
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """グローバルテーママネージャー取得"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
