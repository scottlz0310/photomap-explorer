"""
テーマ対応Mixin - PhotoMap Explorer

ウィジェットにテーマ機能を追加するMixin
"""

from PyQt5.QtCore import QObject
from .theme_init import get_theme_initializer


class ThemeAwareMixin:
    """
    テーマ対応Mixin
    
    ウィジェットにテーマ機能を追加
    """
    
    def __init__(self):
        try:
            self.theme_initializer = get_theme_initializer()
            self.theme_components = []
            
        except Exception as e:
            import logging
            logging.error(f"ThemeAwareMixin初期化エラー: {e}")
            # フォールバック
            self.theme_initializer = None
            self.theme_components = []
    
    def register_theme_component(self, widget, component_type="widget"):
        """テーマコンポーネントを登録"""
        self.theme_components.append((widget, component_type))
    
    def apply_theme(self):
        """テーマを適用"""
        if not self.theme_initializer:
            return
        current_theme = self.theme_initializer.get_current_theme()
        self._apply_custom_theme(current_theme)
    
    def _apply_custom_theme(self, theme_name: str):
        """カスタムテーマ適用（サブクラスでオーバーライド）"""
        pass
    
    def on_theme_changed(self, theme_name: str):
        """テーマ変更時のハンドラ"""
        self.apply_theme()
    
    def get_theme_color(self, color_key: str) -> str:
        """テーマカラーを取得"""
        if not self.theme_initializer:
            return "#000000"  # フォールバック
        # ThemeInitializerにはget_colorメソッドがないため、テーマデータから直接取得
        theme_data = self._get_theme_data()
        return self._extract_color_from_theme_data(theme_data, color_key)
    
    def get_theme_style(self, style_key: str) -> str:
        """テーマスタイルを取得"""
        if not self.theme_initializer:
            return ""  # フォールバック
        # ThemeInitializerにはget_styleメソッドがないため、テーマデータから直接取得
        theme_data = self._get_theme_data()
        return self._extract_style_from_theme_data(theme_data, style_key)
    
    def _get_theme_data(self, theme_name = None):
        """テーマデータを取得"""
        try:
            if not self.theme_initializer:
                return None
            if theme_name:
                return self.theme_initializer.get_theme_data(theme_name)
            else:
                return self.theme_initializer.get_current_theme_data()
        except Exception as e:
            import logging
            logging.error(f"テーマデータ取得エラー: {e}")
            return None
    
    def _extract_color_from_theme_data(self, theme_data, color_key: str) -> str:
        """テーマデータから色を抽出"""
        if not theme_data:
            return "#000000"
        # 色キーの形式: "button.background", "text.primary" など
        keys = color_key.split('.')
        current = theme_data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return "#000000"
        return str(current) if current else "#000000"
    
    def _extract_style_from_theme_data(self, theme_data, style_key: str) -> str:
        """テーマデータからスタイルを抽出"""
        if not theme_data:
            return ""
        # スタイルキーの処理（今のところ基本的な対応のみ）
        return ""


# ダミー関数（互換性のため）
class ThemedWidget:
    pass

def apply_theme_to_widget(widget, theme):
    pass

def get_themed_style(style_key):
    return ""

def get_themed_color(color_key):
    return "#000000"
