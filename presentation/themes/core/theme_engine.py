"""
テーマエンジンコアモジュール

このモジュールは presentation/themes/theme_manager.py から分離された
テーマシステムのコア機能を提供します。
"""

from enum import Enum
from typing import Dict, Any, Optional, List
from PyQt5.QtCore import QObject, pyqtSignal
import logging


class ThemeMode(Enum):
    """テーマモード定義"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"  # システム設定に従う
    CUSTOM = "custom"  # カスタムテーマ


class ThemeEngine(QObject):
    """
    テーマエンジンコアクラス
    
    テーマの基本管理、切り替え、変更通知を担当
    テーマ定義やシステム連携とは独立したコア機能
    """
    
    # シグナル
    theme_changed = pyqtSignal(str)  # テーマ変更通知
    theme_loading = pyqtSignal(str)  # テーマ読み込み開始
    theme_loaded = pyqtSignal(str)   # テーマ読み込み完了
    theme_error = pyqtSignal(str, str)  # エラー発生 (theme_name, error_message)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 状態管理
        self.current_theme = ThemeMode.LIGHT
        self.previous_theme = ThemeMode.LIGHT
        self.is_loading = False
        
        # テーマデータストレージ
        self.theme_registry: Dict[str, Dict[str, Any]] = {}
        self.custom_themes: Dict[str, Dict[str, Any]] = {}
        
        # キャッシュ設定
        self.enable_caching = True
        self.style_cache: Dict[str, str] = {}
        self.color_cache: Dict[str, str] = {}
        
        # 設定
        self.enable_caching = True
        self.enable_transitions = True
        
    def register_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """
        テーマをエンジンに登録
        
        Args:
            theme_name: テーマ名（文字列）
            theme_data: テーマ定義データ
            
        Returns:
            bool: 登録成功可否
        """
        try:
            # テーマデータの基本検証
            if not self._validate_theme_data(theme_data):
                logging.error(f"テーマデータ検証失敗: {theme_name}")
                return False
            
            # テーマ登録
            self.theme_registry[theme_name] = theme_data.copy()
            
            logging.info(f"テーマ登録完了: {theme_name}")
            return True
            
        except Exception as e:
            logging.error(f"テーマ登録エラー: {theme_name} - {e}")
            return False
    
    def register_custom_theme(self, theme_name: str, theme_data: Dict[str, Any]) -> bool:
        """
        カスタムテーマを登録
        
        Args:
            theme_name: カスタムテーマ名
            theme_data: テーマ定義データ
            
        Returns:
            bool: 登録成功可否
        """
        try:
            if not self._validate_theme_data(theme_data):
                logging.error(f"カスタムテーマデータ検証失敗: {theme_name}")
                return False
            
            self.custom_themes[theme_name] = theme_data.copy()
            
            logging.info(f"カスタムテーマ登録完了: {theme_name}")
            return True
            
        except Exception as e:
            logging.error(f"カスタムテーマ登録エラー: {theme_name} - {e}")
            return False
    
    def _validate_theme_data(self, theme_data: Dict[str, Any]) -> bool:
        """テーマデータの妥当性を検証"""
        try:
            # 必須フィールドチェック
            required_fields = ["name", "colors", "styles"]
            for field in required_fields:
                if field not in theme_data:
                    logging.error(f"必須フィールド不足: {field}")
                    return False
            
            # colors構造チェック
            colors = theme_data.get("colors", {})
            if not isinstance(colors, dict):
                logging.error("colors フィールドは辞書である必要があります")
                return False
            
            # styles構造チェック
            styles = theme_data.get("styles", {})
            if not isinstance(styles, dict):
                logging.error("styles フィールドは辞書である必要があります")
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"テーマデータ検証エラー: {e}")
            return False
    
    def get_current_theme(self) -> ThemeMode:
        """現在のテーマモードを取得"""
        return self.current_theme
    
    def get_available_themes(self) -> List[str]:
        """利用可能なテーマモード一覧を取得"""
        return list(self.theme_registry.keys())
    
    def get_custom_themes(self) -> List[str]:
        """利用可能なカスタムテーマ一覧を取得"""
        return list(self.custom_themes.keys())
    
    def set_theme(self, theme_mode) -> bool:
        """
        テーマを設定
        
        Args:
            theme_mode: 設定するテーマモード（ThemeModeまたは文字列）
            
        Returns:
            bool: 設定成功可否
        """
        try:
            # 文字列の場合はそのまま使用、ThemeModeの場合は.valueを使用
            if isinstance(theme_mode, str):
                theme_key = theme_mode
                theme_emit_value = theme_mode
            elif hasattr(theme_mode, 'value'):
                theme_key = theme_mode.value
                theme_emit_value = theme_mode.value
            else:
                theme_key = str(theme_mode)
                theme_emit_value = str(theme_mode)
            
            # 同じテーマの場合はスキップ
            current_key = getattr(self.current_theme, 'value', str(self.current_theme))
            if theme_key == current_key and not self.is_loading:
                return True
            
            # テーマ存在確認
            if theme_key not in self.theme_registry:
                logging.error(f"テーマが登録されていません: {theme_key}")
                return False
            
            # ローディング開始
            self.is_loading = True
            self.theme_loading.emit(theme_key)
            
            # 前のテーマを保存
            self.previous_theme = self.current_theme
            
            # テーマ変更
            self.current_theme = theme_mode
            
            # キャッシュクリア
            if hasattr(self, 'enable_caching') and self.enable_caching:
                self._clear_cache()
            
            # テーマ変更通知
            self.theme_changed.emit(theme_emit_value)
            
            # ローディング完了
            self.is_loading = False
            self.theme_loaded.emit(theme_emit_value)
            
            logging.info(f"テーマ変更完了: {getattr(self.previous_theme, 'value', str(self.previous_theme))} → {theme_emit_value}")
            return True
            
        except Exception as e:
            self.is_loading = False
            error_msg = f"テーマ設定エラー: {e}"
            logging.error(error_msg)
            try:
                self.theme_error.emit(theme_emit_value, str(e))
            except:
                pass
            return False
    
    def set_custom_theme(self, theme_name: str) -> bool:
        """
        カスタムテーマを設定
        
        Args:
            theme_name: カスタムテーマ名
            
        Returns:
            bool: 設定成功可否
        """
        try:
            if theme_name not in self.custom_themes:
                logging.error(f"カスタムテーマが見つかりません: {theme_name}")
                return False
            
            # カスタムテーマを一時的にCUSTOMモードとして登録
            custom_data = self.custom_themes[theme_name]
            self.theme_registry[ThemeMode.CUSTOM] = custom_data
            
            return self.set_theme(ThemeMode.CUSTOM)
            
        except Exception as e:
            logging.error(f"カスタムテーマ設定エラー: {theme_name} - {e}")
            return False
    
    def toggle_theme(self) -> bool:
        """
        テーマを切り替え（LIGHT ⇔ DARK）
        
        Returns:
            bool: 切り替え成功可否
        """
        try:
            if self.current_theme == ThemeMode.LIGHT:
                return self.set_theme(ThemeMode.DARK)
            elif self.current_theme == ThemeMode.DARK:
                return self.set_theme(ThemeMode.LIGHT)
            else:
                # CUSTOM、AUTOの場合はLIGHTに切り替え
                return self.set_theme(ThemeMode.LIGHT)
                
        except Exception as e:
            logging.error(f"テーマ切り替えエラー: {e}")
            return False
    
    def revert_theme(self) -> bool:
        """
        前のテーマに戻す
        
        Returns:
            bool: 復元成功可否
        """
        try:
            return self.set_theme(self.previous_theme)
            
        except Exception as e:
            logging.error(f"テーマ復元エラー: {e}")
            return False
    
    def get_theme_data(self, theme_name: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        テーマデータを取得
        
        Args:
            theme_name: テーマ名（省略時は現在のテーマ）
            
        Returns:
            Optional[Dict[str, Any]]: テーマデータ
        """
        try:
            if not theme_name:
                if isinstance(self.current_theme, str):
                    theme_name = self.current_theme
                elif hasattr(self.current_theme, 'value'):
                    theme_name = self.current_theme.value
                else:
                    theme_name = str(self.current_theme)
            
            # 登録されたテーマから検索
            if theme_name in self.theme_registry:
                return self.theme_registry[theme_name]
            
            # カスタムテーマから検索
            if theme_name in self.custom_themes:
                return self.custom_themes[theme_name]
            
            return None
            
        except Exception as e:
            logging.error(f"テーマデータ取得エラー: {e}")
            return None
    
    def get_color(self, color_key: str, theme_name: Optional[str] = None) -> str:
        """
        テーマから色を取得
        
        Args:
            color_key: 色のキー
            theme_name: テーマ名（省略時は現在のテーマ）
            
        Returns:
            str: 色の値（見つからない場合は空文字列）
        """
        try:
            theme_data = self.get_theme_data(theme_name)
            if theme_data and 'colors' in theme_data:
                colors = theme_data['colors']
                return colors.get(color_key, "")
            
            return ""
            
        except Exception as e:
            logging.error(f"色取得エラー: {e}")
            return ""
    
    def get_style(self, component: str, theme_mode: Optional[ThemeMode] = None) -> str:
        """
        コンポーネントのスタイルを取得
        
        Args:
            component: コンポーネント名
            theme_mode: 対象テーマモード
            
        Returns:
            str: スタイル文字列
        """
        try:
            target_theme = theme_mode or self.current_theme
            
            # キャッシュチェック
            cache_key = f"{target_theme.value}:{component}"
            if self.enable_caching and cache_key in self.style_cache:
                return self.style_cache[cache_key]
            
            # テーマデータ取得
            theme_data = self.get_theme_data(target_theme)
            if not theme_data:
                logging.warning(f"テーマデータが見つかりません: {target_theme}")
                return ""
            
            # スタイルテンプレート取得
            style_template = theme_data.get("styles", {}).get(component, "")
            if not style_template:
                logging.warning(f"コンポーネントスタイルが見つかりません: {component}")
                return ""
            
            # カラー変数を置換
            colors = theme_data.get("colors", {})
            try:
                style = style_template.format(**colors)
                
                # キャッシュに保存
                if self.enable_caching:
                    self.style_cache[cache_key] = style
                
                return style
                
            except KeyError as e:
                logging.warning(f"スタイル変数置換エラー - {component}: 未定義カラー {e}")
                return style_template
            
        except Exception as e:
            logging.error(f"スタイル取得エラー - {component}: {e}")
            return ""
    
    def get_color(self, color_name: str, theme_mode: Optional[ThemeMode] = None) -> str:
        """
        カラー値を取得
        
        Args:
            color_name: カラー名
            theme_mode: 対象テーマモード
            
        Returns:
            str: カラー値（16進数形式）
        """
        try:
            target_theme = theme_mode or self.current_theme
            
            # キャッシュチェック
            cache_key = f"{target_theme.value}:{color_name}"
            if self.enable_caching and cache_key in self.color_cache:
                return self.color_cache[cache_key]
            
            # テーマデータ取得
            theme_data = self.get_theme_data(target_theme)
            if not theme_data:
                logging.warning(f"テーマデータが見つかりません: {target_theme}")
                return "#000000"  # デフォルト黒
            
            # カラー取得
            color = theme_data.get("colors", {}).get(color_name, "#000000")
            
            # キャッシュに保存
            if self.enable_caching:
                self.color_cache[cache_key] = color
            
            return color
            
        except Exception as e:
            logging.error(f"カラー取得エラー - {color_name}: {e}")
            return "#000000"
    
    def get_theme_info(self, theme_mode: Optional[ThemeMode] = None) -> Dict[str, Any]:
        """
        テーマ情報を取得
        
        Args:
            theme_mode: 対象テーマモード
            
        Returns:
            Dict[str, Any]: テーマ情報
        """
        try:
            target_theme = theme_mode or self.current_theme
            theme_data = self.get_theme_data(target_theme)
            
            if not theme_data:
                return {"name": "unknown", "display_name": "不明"}
            
            return {
                "name": theme_data.get("name", "unknown"),
                "display_name": theme_data.get("display_name", "不明"),
                "description": theme_data.get("description", ""),
                "version": theme_data.get("version", "1.0"),
                "author": theme_data.get("author", ""),
                "color_count": len(theme_data.get("colors", {})),
                "style_count": len(theme_data.get("styles", {}))
            }
            
        except Exception as e:
            logging.error(f"テーマ情報取得エラー: {e}")
            return {"name": "error", "display_name": "エラー"}
    
    def _clear_cache(self):
        """キャッシュをクリア"""
        try:
            self.style_cache.clear()
            self.color_cache.clear()
            logging.debug("テーマキャッシュクリア完了")
            
        except Exception as e:
            logging.error(f"キャッシュクリアエラー: {e}")
    
    def set_caching_enabled(self, enabled: bool):
        """キャッシュ機能の有効/無効を設定"""
        try:
            self.enable_caching = enabled
            if not enabled:
                self._clear_cache()
            
            logging.info(f"テーマキャッシュ: {'有効' if enabled else '無効'}")
            
        except Exception as e:
            logging.error(f"キャッシュ設定エラー: {e}")
    
    def set_transitions_enabled(self, enabled: bool):
        """テーマ遷移効果の有効/無効を設定"""
        try:
            self.enable_transitions = enabled
            logging.info(f"テーマ遷移効果: {'有効' if enabled else '無効'}")
            
        except Exception as e:
            logging.error(f"遷移効果設定エラー: {e}")
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """エンジンの統計情報を取得"""
        try:
            return {
                "current_theme": self.current_theme.value,
                "previous_theme": self.previous_theme.value,
                "registered_themes": len(self.theme_registry),
                "custom_themes": len(self.custom_themes),
                "style_cache_size": len(self.style_cache),
                "color_cache_size": len(self.color_cache),
                "caching_enabled": self.enable_caching,
                "transitions_enabled": self.enable_transitions,
                "is_loading": self.is_loading
            }
            
        except Exception as e:
            logging.error(f"エンジン統計取得エラー: {e}")
            return {}
