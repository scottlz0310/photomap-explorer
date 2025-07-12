"""
テーマシステム統合モジュール

presentation/themes/theme_manager.py の機能を提供する統合インターフェース
"""

import logging
from typing import Dict, Any, Optional, List, Callable

# 各モジュールのインポート
from .core.theme_engine import ThemeEngine, ThemeMode
from .core.theme_factory import ThemeFactory, ThemePresetManager
from .system.system_theme_detector import SystemThemeDetector, SystemThemeSync
from .system.theme_settings import ThemeSettingsManager, ThemeSettings
from .definitions.light_theme import create_light_theme, create_light_theme_variant
from .definitions.dark_theme import create_dark_theme, create_dark_theme_variant


class ThemeManager:
    """
    統合テーマ管理クラス
    
    元の theme_manager.py の機能を提供する後方互換インターフェース
    """
    
    def __init__(self, settings_file: Optional[str] = None):
        """
        テーママネージャーの初期化
        
        Args:
            settings_file: 設定ファイルパス（オプション）
        """
        try:
            # 各コンポーネントの初期化
            self._theme_engine = ThemeEngine()
            self._theme_factory = ThemeFactory()
            self._preset_manager = ThemePresetManager()
            self._settings_manager = ThemeSettingsManager(settings_file)
            self._system_detector = SystemThemeDetector()
            self._system_sync = SystemThemeSync(self._system_detector)
            
            # 初期設定
            self._initialize_themes()
            self._setup_system_sync()
            
            logging.info("テーママネージャー初期化完了")
            
        except Exception as e:
            logging.error(f"テーママネージャー初期化エラー: {e}")
            raise
    
    def _initialize_themes(self):
        """デフォルトテーマの登録"""
        try:
            # 基本テーマの登録
            themes_to_register = [
                ("light", self._theme_factory.create_theme("light")),
                ("dark", self._theme_factory.create_theme("dark"))
            ]
            
            for theme_name, theme_data in themes_to_register:
                if theme_data:
                    self._theme_engine.register_theme(theme_name, theme_data)
            
            # バリエーションテーマの登録
            variations = self._theme_factory.get_theme_variations("light") + \
                        self._theme_factory.get_theme_variations("dark")
            
            for variant in variations:
                theme_data = self._theme_factory.create_theme(variant)
                if theme_data:
                    self._theme_engine.register_theme(variant, theme_data)
            
            logging.debug("デフォルトテーマ登録完了")
            
        except Exception as e:
            logging.error(f"テーマ初期化エラー: {e}")
    
    def _setup_system_sync(self):
        """システムテーマ同期の設定"""
        try:
            if self._settings_manager.get_auto_detect_system():
                # システムテーマ変更のコールバック設定
                def on_system_theme_change(is_dark: bool):
                    if self._settings_manager.get_theme_mode() == ThemeMode.AUTO:
                        new_theme = "dark" if is_dark else "light"
                        self.set_current_theme(new_theme)
                
                self._system_sync.add_callback(on_system_theme_change)
                self._system_sync.start_monitoring()
                
                logging.debug("システムテーマ同期設定完了")
                
        except Exception as e:
            logging.error(f"システム同期設定エラー: {e}")
    
    # ========== 公開API - テーマ操作 ==========
    
    def get_current_theme(self) -> str:
        """現在のテーマ名を取得"""
        return self._settings_manager.get_current_theme()
    
    def set_current_theme(self, theme_name: str) -> bool:
        """
        現在のテーマを設定
        
        Args:
            theme_name: テーマ名
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            # テーマの存在確認
            if not self._theme_engine.has_theme(theme_name):
                logging.warning(f"テーマが見つかりません: {theme_name}")
                return False
            
            # テーマ切り替え
            success = self._theme_engine.switch_theme(theme_name)
            if success:
                self._settings_manager.set_current_theme(theme_name)
                logging.info(f"テーマ変更: {theme_name}")
            
            return success
            
        except Exception as e:
            logging.error(f"テーマ設定エラー: {e}")
            return False
    
    def get_available_themes(self) -> List[str]:
        """利用可能なテーマ一覧を取得"""
        return self._theme_engine.get_available_themes()
    
    def get_theme_data(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """
        テーマデータを取得
        
        Args:
            theme_name: テーマ名
            
        Returns:
            Optional[Dict[str, Any]]: テーマデータ
        """
        return self._theme_engine.get_theme_data(theme_name)
    
    def apply_theme_to_widget(self, widget, theme_name: Optional[str] = None):
        """
        ウィジェットにテーマを適用
        
        Args:
            widget: 対象ウィジェット
            theme_name: テーマ名（None時は現在のテーマ）
        """
        try:
            target_theme = theme_name or self.get_current_theme()
            self._theme_engine.apply_theme_to_widget(widget, target_theme)
            
        except Exception as e:
            logging.error(f"テーマ適用エラー: {e}")
    
    # ========== 公開API - モード管理 ==========
    
    def get_theme_mode(self) -> ThemeMode:
        """テーマモードを取得"""
        return self._settings_manager.get_theme_mode()
    
    def set_theme_mode(self, mode: ThemeMode) -> bool:
        """
        テーマモードを設定
        
        Args:
            mode: テーマモード
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            success = self._settings_manager.set_theme_mode(mode)
            
            if success and mode == ThemeMode.AUTO:
                # 自動モード時はシステムテーマに従う
                is_system_dark = self._system_detector.is_dark_theme()
                auto_theme = "dark" if is_system_dark else "light"
                self.set_current_theme(auto_theme)
            
            return success
            
        except Exception as e:
            logging.error(f"テーマモード設定エラー: {e}")
            return False
    
    def toggle_theme_mode(self) -> bool:
        """テーマモードを切り替え（light ⇄ dark）"""
        try:
            current_mode = self.get_theme_mode()
            
            if current_mode == ThemeMode.LIGHT:
                return self.set_theme_mode(ThemeMode.DARK) and self.set_current_theme("dark")
            elif current_mode == ThemeMode.DARK:
                return self.set_theme_mode(ThemeMode.LIGHT) and self.set_current_theme("light")
            else:  # AUTO mode
                # 現在のテーマを反転
                current_theme = self.get_current_theme()
                new_theme = "light" if current_theme == "dark" else "dark"
                new_mode = ThemeMode.LIGHT if new_theme == "light" else ThemeMode.DARK
                return self.set_theme_mode(new_mode) and self.set_current_theme(new_theme)
                
        except Exception as e:
            logging.error(f"テーマ切り替えエラー: {e}")
            return False
    
    def get_system_theme(self) -> str:
        """システムテーマを取得"""
        try:
            is_dark = self._system_detector.is_dark_theme()
            return "dark" if is_dark else "light"
            
        except Exception as e:
            logging.error(f"システムテーマ取得エラー: {e}")
            return "light"
    
    def cleanup(self):
        """リソースのクリーンアップ"""
        try:
            if self._system_sync:
                self._system_sync.stop_monitoring()
            
            if self._theme_engine:
                self._theme_engine.clear_cache()
            
            logging.debug("テーママネージャークリーンアップ完了")
            
        except Exception as e:
            logging.error(f"クリーンアップエラー: {e}")


# 後方互換性のための関数
def create_theme_manager(settings_file: Optional[str] = None) -> ThemeManager:
    """テーママネージャーを作成"""
    return ThemeManager(settings_file)


def get_theme_manager() -> Optional[ThemeManager]:
    """グローバルテーママネージャーを取得（後方互換）"""
    # 必要に応じて実装
    return None


# 後方互換性のためのクラス
class ThemeAwareMixin:
    """テーマ対応Mixin（後方互換）"""
    pass


class ThemedWidget:
    """テーマ対応ウィジェット（後方互換）"""
    pass


def apply_theme_to_widget(widget, theme_name: Optional[str] = None):
    """ウィジェットにテーマを適用（後方互換）"""
    pass


def get_themed_style(style_name: str) -> str:
    """テーマスタイルを取得（後方互換）"""
    return ""


def get_themed_color(color_name: str) -> str:
    """テーマカラーを取得（後方互換）"""
    return "#000000"


# モジュールレベルでのエクスポート
__all__ = [
    'ThemeManager',
    'ThemeEngine', 
    'ThemeMode',
    'ThemeFactory',
    'ThemePresetManager',
    'SystemThemeDetector',
    'ThemeSettingsManager',
    'create_theme_manager',
    'get_theme_manager',
    'ThemeAwareMixin',
    'ThemedWidget',
    'apply_theme_to_widget',
    'get_themed_style', 
    'get_themed_color',
    'create_light_theme',
    'create_dark_theme'
]

__all__ = [
    'ThemeManager',
    'ThemeMode', 
    'get_theme_manager',
    'ThemeAwareMixin',
    'ThemedWidget',
    'apply_theme_to_widget',
    'get_themed_style',
    'get_themed_color'
]
