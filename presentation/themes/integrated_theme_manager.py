"""
統合テーママネージャー

テーマの作成、管理、設定の永続化を統合管理します。
"""

from typing import Dict, Any, Optional, List
from PyQt5.QtCore import QObject, pyqtSignal

from .theme_init import ThemeInitializer
from .core.theme_engine import ThemeEngine, ThemeMode
from .theme_settings_manager import ThemeSettingsManager
from utils.logging_bridge import get_theme_logger


class IntegratedThemeManager(QObject):
    """統合テーマ管理クラス"""
    
    # シグナル
    theme_changed = pyqtSignal(str)  # テーマ変更通知
    theme_saved = pyqtSignal(str)    # テーマ設定保存通知
    theme_error = pyqtSignal(str, str)  # エラー通知 (theme_name, error_message)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # ログブリッジ初期化
        self.logger = get_theme_logger("IntegratedManager")
        
        # コンポーネント初期化
        self.theme_init = ThemeInitializer()
        self.engine = ThemeEngine(self)
        self.settings_manager = ThemeSettingsManager()
        
        # シグナル接続
        self.engine.theme_changed.connect(self._on_theme_changed)
        self.engine.theme_error.connect(self._on_theme_error)
        
        # 初期化
        self._initialize_themes()
        self._load_saved_theme()
    
    def _initialize_themes(self):
        """テーマを初期化"""
        try:
            # 利用可能なテーマを登録
            available_themes = self.theme_init.get_available_theme_names()
            
            for theme_name in available_themes:
                theme_data = self.theme_init.get_theme_definition(theme_name)
                if theme_data:
                    # テーマエンジンへの登録は一時的にスキップ（新形式対応まで）
                    # self.engine.register_theme(theme_name, theme_data)
                    self.logger.verbose(f"テーマ準備: {theme_name}")
                else:
                    self.logger.warning(f"テーマ作成失敗: {theme_name}")
            
            self.logger.info(f"テーマ初期化完了: {len(available_themes)}個のテーマが利用可能")
            
        except Exception as e:
            self.logger.error(f"テーマ初期化エラー: {e}")
    
    def _load_saved_theme(self):
        """保存されたテーマを読み込み"""
        try:
            if self.settings_manager.is_theme_remembering_enabled():
                saved_theme = self.settings_manager.get_last_selected_theme()
                self.logger.verbose(f"保存されたテーマを復元: {saved_theme}")
                self.set_theme(saved_theme, save_settings=False)
            else:
                # 記憶機能が無効の場合はデフォルトテーマ
                self.set_theme('dark', save_settings=False)
                self.logger.verbose("デフォルトテーマを適用")
                
        except Exception as e:
            self.logger.error(f"保存テーマ読み込みエラー: {e}")
            self.set_theme('dark', save_settings=False)
    
    def set_theme(self, theme_name: str, save_settings: bool = True) -> bool:
        """
        テーマを設定
        
        Args:
            theme_name: テーマ名
            save_settings: 設定を保存するかどうか
            
        Returns:
            bool: 成功した場合True
        """
        try:
            # テーマが存在するかチェック
            if not self.is_theme_available(theme_name):
                self.logger.warning(f"未知のテーマ: {theme_name}")
                return False
            
            # 新しいテーマシステムを使用してスタイルシートを取得
            stylesheet = self.theme_init.create_theme_stylesheet(theme_name)
            
            # 親ウィジェットに適用（テーマエンジンを迂回）
            if hasattr(self, 'parent') and self.parent():
                self.parent().setStyleSheet(stylesheet)
                success = True
            else:
                success = False
            
            if success and save_settings:
                # 設定を保存
                self.settings_manager.set_current_theme(theme_name)
                self.logger.verbose(f"テーマ設定を保存: {theme_name}")
                self.theme_saved.emit(theme_name)
            
            return success
            
        except Exception as e:
            self.logger.error(f"テーマ設定エラー: {e}")
            self.theme_error.emit(theme_name, str(e))
            return False
    
    def get_current_theme(self) -> str:
        """現在のテーマ名を取得"""
        current = self.engine.get_current_theme()
        if isinstance(current, str):
            return current
        elif hasattr(current, 'value'):
            return current.value
        else:
            return str(current)
    
    def get_available_themes(self) -> List[str]:
        """利用可能なテーマ名のリストを取得"""
        return self.theme_init.get_available_theme_names()
    
    def get_theme_display_names(self) -> List[str]:
        """テーマの表示名リストを取得"""
        themes = []
        for theme_name in self.get_available_themes():
            theme_def = self.theme_init.get_theme_definition(theme_name)
            if theme_def:
                themes.append(theme_def.get('display_name', theme_name))
        return themes
    
    def get_theme_info(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """特定のテーマの情報を取得"""
        return self.theme_init.get_theme_definition(theme_name)
    
    def is_theme_available(self, theme_name: str) -> bool:
        """テーマが利用可能かチェック"""
        return theme_name in self.get_available_themes()
    
    def is_theme_remembering_enabled(self) -> bool:
        """テーマ記憶機能が有効かどうか"""
        return self.settings_manager.is_theme_remembering_enabled()
    
    def set_theme_remembering(self, enabled: bool) -> bool:
        """テーマ記憶機能の有効/無効を設定"""
        return self.settings_manager.set_theme_remembering(enabled)
    
    def get_theme_stylesheet(self, theme_name: Optional[str] = None) -> str:
        """
        テーマのスタイルシートを取得
        
        Args:
            theme_name: テーマ名（省略時は現在のテーマ）
            
        Returns:
            str: スタイルシート文字列
        """
        if not theme_name:
            theme_name = self.get_current_theme()
        
        # テーマ初期化システムからテーマデータを取得
        theme_data = self.theme_init.get_theme_definition(theme_name)
        if theme_data:
            # スタイルシートを生成
            stylesheet = self.theme_init.create_theme_stylesheet(theme_name)
            return stylesheet
        
        return ""
    
    def get_theme_color(self, color_key: str, theme_name: Optional[str] = None) -> str:
        """
        テーマから特定の色を取得
        
        Args:
            color_key: 色のキー
            theme_name: テーマ名（省略時は現在のテーマ）
            
        Returns:
            str: 色の値
        """
        if not theme_name:
            theme_name = self.get_current_theme()
        
        # テーマ初期化システムからテーマデータを取得
        theme_data = self.theme_init.get_theme_definition(theme_name)
        if theme_data:
            # 色の値を取得
            return theme_data.get(color_key, "#000000")
        
        return "#000000"
    
    def refresh_current_theme(self):
        """現在のテーマを再読み込み"""
        current = self.get_current_theme()
        self.set_theme(current, save_settings=False)
    
    def reset_to_default(self) -> bool:
        """テーマ設定をデフォルトにリセット"""
        try:
            success = self.settings_manager.reset_to_defaults()
            if success:
                self._initialize_themes()
                self.set_theme('dark', save_settings=False)
                self.logger.info("テーマ設定をデフォルトにリセット")
            
            return success
            
        except Exception as e:
            self.logger.error(f"テーマリセットエラー: {e}")
            return False
    
    def create_custom_theme(self, theme_name: str, base_theme: str, 
                          customizations: Dict[str, Any]) -> bool:
        """
        カスタムテーマを作成
        
        Args:
            theme_name: 新しいテーマ名
            base_theme: ベースとなるテーマ名
            customizations: カスタマイズ内容
            
        Returns:
            bool: 成功した場合True
        """
        try:
            # ベーステーマから作成
            base_theme_data = self.theme_init.get_theme_definition(base_theme)
            if not base_theme_data:
                self.logger.warning(f"ベーステーマが見つかりません: {base_theme}")
                return False
            
            # カスタマイズを適用（簡略化）
            custom_theme = base_theme_data.copy()
            for key, value in customizations.items():
                custom_theme[key] = value
            
            # エンジンに登録（必要に応じて）
            # self.engine.register_theme(theme_name, custom_theme)
            
            # 設定に保存
            theme_definition = {
                'name': theme_name,
                'display_name': theme_name,
                'description': f'{base_theme}ベースのカスタムテーマ',
                'base_theme': base_theme,
                'customizations': customizations
            }
            
            success = self.settings_manager.add_custom_theme(theme_name, theme_definition)
            
            if success:
                self.logger.info(f"カスタムテーマを作成: {theme_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"カスタムテーマ作成エラー: {e}")
            return False
    
    def remove_custom_theme(self, theme_name: str) -> bool:
        """カスタムテーマを削除"""
        try:
            # カスタムテーマのレジストリから削除
            if theme_name in self.engine.custom_themes:
                del self.engine.custom_themes[theme_name]
            
            if theme_name in self.engine.theme_registry:
                del self.engine.theme_registry[theme_name]
            
            # 設定から削除
            success = self.settings_manager.remove_theme(theme_name)
            
            if success:
                self.logger.info(f"カスタムテーマを削除: {theme_name}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"カスタムテーマ削除エラー: {e}")
            return False
    
    def export_theme_settings(self, file_path: str) -> bool:
        """テーマ設定をエクスポート"""
        return self.settings_manager.backup_settings(file_path)
    
    def import_theme_settings(self, file_path: str) -> bool:
        """テーマ設定をインポート"""
        success = self.settings_manager.restore_settings(file_path)
        if success:
            self._initialize_themes()
            self._load_saved_theme()
        
        return success
    
    def get_breadcrumb_settings(self) -> Dict[str, Any]:
        """パンくずリスト設定を取得"""
        return self.settings_manager.get_breadcrumb_settings()
    
    def set_breadcrumb_settings(self, settings: Dict[str, Any]) -> bool:
        """パンくずリスト設定を保存"""
        return self.settings_manager.set_breadcrumb_settings(settings)
    
    def cycle_theme(self) -> str:
        """
        テーマを順次切り替え
        
        Returns:
            str: 新しく設定されたテーマ名
        """
        try:
            available_themes = self.get_available_themes()
            current_theme = self.get_current_theme()
            
            if not available_themes:
                self.logger.warning("利用可能なテーマがありません")
                return current_theme
            
            # 現在のテーマのインデックスを取得
            try:
                current_index = available_themes.index(current_theme)
            except ValueError:
                # 現在のテーマが見つからない場合は最初のテーマから開始
                current_index = -1
            
            # 次のテーマのインデックスを計算
            next_index = (current_index + 1) % len(available_themes)
            next_theme = available_themes[next_index]
            
            # テーマを切り替え
            success = self.set_theme(next_theme)
            if success:
                self.logger.info(f"テーマサイクル: {current_theme} -> {next_theme}")
                return next_theme
            else:
                self.logger.error(f"テーマ切り替えに失敗: {next_theme}")
                return current_theme
                
        except Exception as e:
            self.logger.error(f"テーマサイクルエラー: {e}")
            return self.get_current_theme()

    def _on_theme_changed(self, theme_name: str):
        """テーマ変更イベントハンドラ"""
        self.logger.debug(f"テーマ変更イベント: {theme_name}")
        self.theme_changed.emit(theme_name)
    
    def _on_theme_error(self, theme_name: str, error_message: str):
        """テーマエラーイベントハンドラ"""
        self.logger.error(f"テーマエラー {theme_name}: {error_message}")
        self.theme_error.emit(theme_name, error_message)


# 共有インスタンス（シングルトンパターン）
_theme_manager_instance = None

def get_theme_manager() -> IntegratedThemeManager:
    """テーママネージャーのシングルトンインスタンスを取得"""
    global _theme_manager_instance
    if _theme_manager_instance is None:
        _theme_manager_instance = IntegratedThemeManager()
    return _theme_manager_instance
