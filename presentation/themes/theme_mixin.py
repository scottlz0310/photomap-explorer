"""
テーマ対応Mixin - PhotoMap Explorer

ウィジェットにテーマ機能を追加するMixin
"""

from PyQt5.QtCore import QObject
from .core.theme_engine import ThemeEngine
from .system.theme_settings import ThemeMode


class ThemeAwareMixin:
    """
    テーマ対応Mixin
    
    ウィジェットにテーマ機能を追加
    """
    
    def __init__(self):
        self.theme_engine = ThemeEngine()
        self.theme_components = []
        
        # テーマ変更シグナルに接続
        self.theme_engine.theme_changed.connect(self.on_theme_changed)
    
    def register_theme_component(self, widget, component_type="widget"):
        """テーマコンポーネントを登録"""
        self.theme_components.append((widget, component_type))
    
    def apply_theme(self):
        """テーマを適用"""
        current_theme = self.theme_engine.get_current_theme()
        self._apply_custom_theme(current_theme)
    
    def _apply_custom_theme(self, theme: ThemeMode):
        """カスタムテーマ適用（サブクラスでオーバーライド）"""
        pass
    
    def on_theme_changed(self, theme_name: str):
        """テーマ変更時のハンドラ"""
        self.apply_theme()
    
    def get_theme_color(self, color_key: str) -> str:
        """テーマカラーを取得"""
        return self.theme_engine.get_color(color_key)
    
    def get_theme_style(self, style_key: str) -> str:
        """テーマスタイルを取得"""
        return self.theme_engine.get_style(style_key)


# 後方互換性のためのクラスと関数
class ThemedWidget:
    """後方互換性のための空のクラス"""
    def __init__(self):
        pass

def apply_theme_to_widget(widget, theme):
    """ウィジェットにテーマを適用（後方互換性）"""
    try:
        if hasattr(widget, 'setStyleSheet') and theme:
            # 基本的なテーマ適用
            if hasattr(theme, 'get_style'):
                style = theme.get_style('default')
                widget.setStyleSheet(style)
    except Exception:
        pass  # エラーを無視

def get_themed_style(style_key):
    """テーマスタイルを取得（後方互換性）"""
    try:
        # デフォルトスタイルを返す
        return ""
    except Exception:
        return ""

def get_themed_color(color_key):
    return "#000000"
