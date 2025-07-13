"""
シンプルなテーマ切り替えイベント処理ハンドラ

統一されたテーマシステムを使用してシンプルなテーマ切り替えを提供します。
"""

from PyQt5.QtWidgets import QMessageBox
from utils.logging_bridge import get_theme_logger
from presentation.themes.theme_init import get_theme_initializer


class ThemeEventHandler:
    """テーマ切り替えイベント処理を担当するハンドラ"""
    
    def __init__(self, main_window):
        """
        テーマイベントハンドラを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.logger = get_theme_logger("EventHandler")
        self.theme_initializer = get_theme_initializer()
        self.current_theme = self.theme_initializer.get_current_theme()
        
    def set_components(self, theme_manager=None):
        """互換性のためのメソッド（新システムでは不要）"""
        pass
    
    def on_theme_changed(self, theme_name):
        """テーマ変更時の処理"""
        try:
            success = self._apply_theme(theme_name)
            
            if success:
                self.current_theme = theme_name
                self.main_window.show_status_message(f"🎨 テーマ変更: {theme_name}")
                self._refresh_ui()
                
            else:
                self.main_window.show_status_message(f"❌ テーマ変更に失敗: {theme_name}")
                
        except Exception as e:
            self.logger.error(f"テーマ変更エラー: {e}")
            self.main_window.show_status_message(f"❌ テーマ変更エラー: {e}")
    
    def _apply_theme(self, theme_name):
        """テーマを適用"""
        try:
            # テーマを設定
            success = self.theme_initializer.set_current_theme(theme_name)
            if not success:
                return False
            
            # スタイルシートを生成・適用
            stylesheet = self.theme_initializer.create_theme_stylesheet(theme_name)
            self.main_window.setStyleSheet(stylesheet)
            
            # ナビゲーションボタンのスタイルを更新
            self._update_navigation_controls(theme_name)
            
            self.logger.info(f"テーマ適用完了: {theme_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"テーマ適用エラー: {e}")
            return False
    
    def _update_navigation_controls(self, theme_name):
        """ナビゲーションコントロールのテーマを更新"""
        try:
            # ナビゲーションコントロールを検索して更新
            if hasattr(self.main_window, 'navigation_controls') and self.main_window.navigation_controls:
                self.main_window.navigation_controls.apply_theme(theme_name)
                self.logger.debug(f"ナビゲーションコントロールテーマ更新: {theme_name}")
            
            # アドレスバーも更新
            if hasattr(self.main_window, 'address_bar') and self.main_window.address_bar:
                if hasattr(self.main_window.address_bar, 'apply_theme'):
                    self.main_window.address_bar.apply_theme(theme_name)
                    self.logger.debug(f"アドレスバーテーマ更新: {theme_name}")
                    
        except Exception as e:
            self.logger.error(f"ナビゲーションコントロールテーマ更新エラー: {e}")
    
    def _refresh_ui(self):
        """UI全体の再描画"""
        try:
            # メインウィンドウの更新
            self.main_window.update()
            self.main_window.repaint()
            
            # 子ウィジェットの更新
            for child in self.main_window.findChildren(object):
                if hasattr(child, 'update'):
                    try:
                        child.update()
                    except:
                        pass
                        
        except Exception as e:
            self.logger.error(f"UI再描画エラー: {e}")
    
    def get_current_theme(self):
        """現在のテーマ名を取得"""
        return self.theme_initializer.get_current_theme()
    
    def get_available_themes(self):
        """利用可能なテーマ一覧を取得"""
        try:
            return self.theme_initializer.get_available_theme_names()
        except Exception as e:
            self.logger.error(f"テーマ一覧取得エラー: {e}")
            return ["light"]
    
    def save_theme_preference(self, theme_name):
        """テーマ設定を保存（自動的に行われるため互換性用）"""
        try:
            self.theme_initializer.set_current_theme(theme_name)
        except Exception as e:
            self.logger.error(f"テーマ設定保存エラー: {e}")
    
    def load_theme_preference(self):
        """保存されたテーマ設定を読み込み"""
        try:
            return self.theme_initializer.get_current_theme()
        except Exception as e:
            self.logger.error(f"テーマ設定読み込みエラー: {e}")
            return "light"
    
    def initialize_theme(self):
        """テーマの初期化"""
        try:
            current_theme = self.theme_initializer.get_current_theme()
            self.logger.verbose(f"保存されたテーマで初期化: {current_theme}")
            
            # テーマを適用
            self.current_theme = current_theme
            self._apply_theme(current_theme)
            
            # 初期化完了後にナビゲーションコントロールのテーマも更新
            # 少し遅延させてコンポーネントが完全に初期化されるのを待つ
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, lambda: self._update_navigation_controls(current_theme))
            
        except Exception as e:
            self.logger.error(f"テーマ初期化エラー: {e}")
            # デフォルトテーマにフォールバック
            self.on_theme_changed("light")
    
    def toggle_theme(self):
        """テーマを切り替え（サイクル）"""
        try:
            new_theme = self.theme_initializer.cycle_theme()
            self.current_theme = new_theme
            
            # UIにスタイルシートを適用
            stylesheet = self.theme_initializer.create_theme_stylesheet(new_theme)
            self.main_window.setStyleSheet(stylesheet)
            
            self.main_window.show_status_message(f"🎨 テーマ切り替え: {new_theme}")
            self._refresh_ui()
            
            # テーマボタンのテキストを更新
            self._update_theme_button_text(new_theme)
            
        except Exception as e:
            self.logger.error(f"テーマ切り替えエラー: {e}")
            self.main_window.show_status_message(f"❌ テーマ切り替えエラー: {e}")
    
    def _update_theme_button_text(self, theme_name):
        """テーマボタンのテキストを更新"""
        try:
            if hasattr(self.main_window, 'theme_toggle_btn') and self.main_window.theme_toggle_btn:
                # テーマ表示名を取得
                theme_def = self.theme_initializer.get_theme_definition(theme_name)
                if theme_def:
                    display_name = theme_def.get('display_name', theme_name)
                    self.main_window.theme_toggle_btn.setText(f"🎨 {display_name}")
                else:
                    self.main_window.theme_toggle_btn.setText(f"🎨 {theme_name}")
                    
        except Exception as e:
            self.logger.error(f"テーマボタンテキスト更新エラー: {e}")
    
    def apply_theme_to_component(self, component, theme_name=None):
        """特定のコンポーネントにテーマを適用"""
        try:
            if not theme_name:
                theme_name = self.current_theme
            
            stylesheet = self.theme_initializer.create_theme_stylesheet(theme_name)
            if hasattr(component, 'setStyleSheet'):
                component.setStyleSheet(stylesheet)
                
        except Exception as e:
            self.logger.error(f"コンポーネントテーマ適用エラー: {e}")
    
    def _apply_navigation_theme(self, theme_name):
        """ナビゲーションコントロールにテーマを適用（互換性用）"""
        try:
            # 新システムでは自動的に適用されるため、何もしない
            self.logger.debug(f"ナビゲーションテーマ適用（自動）: {theme_name}")
        except Exception as e:
            self.logger.error(f"ナビゲーションテーマ適用エラー: {e}")
