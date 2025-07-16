"""
テーマ対応Mixin - PhotoMap Explorer

ウィジェットにテーマ機能を追加するMixin
"""

from PyQt5.QtCore import QObject
from .core.theme_engine import ThemeMode

# 一時的なダミー実装
class DummySignal:
    def connect(self, func):
        pass

class DummyThemeManager:
    def __init__(self):
        self.theme_changed = DummySignal()
    
    def get_theme_definition(self, name):
        return {}
    
    def get_current_theme_name(self):
        return "light"
    
    def get_current_theme(self):
        return {}
    
    def get_color(self, color_key):
        return "#000000"
    
    def get_style(self, style_key):
        return ""

def get_theme_manager():
    return DummyThemeManager()


class ThemeAwareMixin:
    """
    テーマ対応Mixin
    
    ウィジェットにテーマ機能を追加
    """
    
    def __init__(self):
        self.theme_manager = get_theme_manager()
        self.theme_components = []
        
        # テーマ変更シグナルに接続
        self.theme_manager.theme_changed.connect(self.on_theme_changed)
    
    def register_theme_component(self, widget, component_type="widget"):
        """テーマコンポーネントを登録"""
        self.theme_components.append((widget, component_type))
    
    def apply_theme(self):
        """テーマを適用"""
        current_theme = self.theme_manager.get_current_theme()
        self._apply_custom_theme(current_theme)
    
    def _apply_custom_theme(self, theme: ThemeMode):
        """カスタムテーマ適用（サブクラスでオーバーライド）"""
        pass
    
    def on_theme_changed(self, theme_name: str):
        """テーマ変更時のハンドラ"""
        self.apply_theme()
    
    def get_theme_color(self, color_key: str) -> str:
        """テーマカラーを取得"""
        return self.theme_manager.get_color(color_key)
    
    def get_theme_style(self, style_key: str) -> str:
        """テーマスタイルを取得"""
        return self.theme_manager.get_style(style_key)


# ダミー関数（互換性のため）
class ThemedWidget:
    pass

def apply_theme_to_widget(widget, theme):
    pass

def get_themed_style(style_key):
    return ""

def get_themed_color(color_key):
    return "#000000"
