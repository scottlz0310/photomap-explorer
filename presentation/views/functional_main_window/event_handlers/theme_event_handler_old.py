"""
テーマ切り替えイベント処理を担当するハンドラ

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
            if not self.theme_manager:
                self.main_window.show_status_message("❌ テーママネージャーが利用できません")
                return
            
            # テーマ適用
            success = self._apply_theme(theme_name)
            
            if success:
                self.current_theme = theme_name
                self.main_window.show_status_message(f"🎨 テーマ変更: {theme_name}")
                
                # 画面の再描画をトリガー
                self._refresh_ui()
                
                # ナビゲーションコントロールに直接テーマ適用
                self._apply_navigation_theme(theme_name)
                
            else:
                self.main_window.show_status_message(f"❌ テーマ変更に失敗: {theme_name}")
                
        except Exception as e:
            self.logger.error(f"テーマ変更エラー: {e}")
            self.main_window.show_status_message(f"❌ テーマ変更エラー: {e}")
    
    def _apply_theme(self, theme_name):
        """テーマを適用"""
        try:
            if hasattr(self.theme_manager, 'apply_theme'):
                return self.theme_manager.apply_theme(theme_name)  # type: ignore
            elif hasattr(self.theme_manager, 'set_theme'):
                return self.theme_manager.set_theme(theme_name)  # type: ignore
            else:
                # 基本的なテーマ適用（フォールバック）
                return self._apply_basic_theme(theme_name)
                
        except Exception as e:
            self.logger.error(f"テーマ適用エラー: {e}")
            return False
    
    def _apply_basic_theme(self, theme_name):
        """基本的なテーマ適用（フォールバック）"""
        try:
            # 基本的なテーマカラーの定義
            themes = {
                "default": {
                    "background": "#ffffff",
                    "foreground": "#000000",
                    "accent": "#007ACC",
                    "secondary": "#f0f0f0"
                },
                "dark": {
                    "background": "#2d2d2d",
                    "foreground": "#ffffff", 
                    "accent": "#007ACC",
                    "secondary": "#4d4d4d"
                },
                "blue": {
                    "background": "#1e3a8a",
                    "foreground": "#ffffff",
                    "accent": "#60a5fa",
                    "secondary": "#3b82f6"
                }
            }
            
            if theme_name not in themes:
                return False
            
            theme_colors = themes[theme_name]
            
            # 全てのUIコンポーネントにテーマを適用
            self._apply_theme_to_all_components(theme_colors)
            
            return True
            
        except Exception as e:
            self.logger.error(f"基本テーマ適用エラー: {e}")
            return False
    
    def _apply_theme_to_all_components(self, theme_colors):
        """すべてのUIコンポーネントにテーマを適用"""
        try:
            # アプリケーション全体のスタイルシートを設定
            app_stylesheet = f"""
                QWidget {{
                    background-color: {theme_colors['background']};
                    color: {theme_colors['foreground']};
                }}
                QGroupBox {{
                    background-color: {theme_colors['background']};
                    color: {theme_colors['foreground']};
                    border: 1px solid {theme_colors['secondary']};
                    margin-top: 10px;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    color: {theme_colors['foreground']};
                    font-weight: bold;
                }}
                QLabel {{
                    color: {theme_colors['foreground']};
                }}
                QListWidget {{
                    background-color: {theme_colors['background']};
                    color: {theme_colors['foreground']};
                    border: 1px solid {theme_colors['secondary']};
                }}
                QPushButton {{
                    background-color: {theme_colors['secondary']};
                    color: {theme_colors['foreground']};
                    border: 1px solid {theme_colors['accent']};
                    padding: 5px;
                }}
                QPushButton:hover {{
                    background-color: {theme_colors['accent']};
                }}
            """
            
            # メインウィンドウにスタイルシートを設定
            if self.main_window:
                self.main_window.setStyleSheet(app_stylesheet)
                self.logger.debug(f"テーマ適用完了: {theme_colors}")
                return True
                
        except Exception as e:
            self.logger.error(f"全コンポーネントテーマ適用エラー: {e}")
            
            # フォールバック: 基本的なスタイルシートを適用
            try:
                stylesheet = f"""
                    QMainWindow {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                    }}
                    QLabel {{
                        color: {theme_colors['foreground']};
                    }}
                    QPushButton {{
                        background-color: {theme_colors['accent']};
                        color: {theme_colors['foreground']};
                        border: 1px solid {theme_colors['accent']};
                        padding: 5px;
                        border-radius: 3px;
                    }}
                    QPushButton:hover {{
                        background-color: {theme_colors['secondary']};
                    }}
                    QListWidget {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: 1px solid {theme_colors['secondary']};
                    }}
                """
                
                self.main_window.setStyleSheet(stylesheet)
                return True
                
            except Exception as fallback_error:
                self.logger.error(f"フォールバックテーマ適用エラー: {fallback_error}")
                return False
    
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
        return self.current_theme
    
    def get_available_themes(self):
        """利用可能なテーマ一覧を取得"""
        try:
            if self.theme_manager and hasattr(self.theme_manager, 'get_available_themes'):
                return self.theme_manager.get_available_themes()
            else:
                # デフォルトテーマ一覧
                return ["default", "dark", "blue"]
                
        except Exception as e:
            self.logger.error(f"テーマ一覧取得エラー: {e}")
            return ["default"]
    
    def save_theme_preference(self, theme_name):
        """テーマ設定を保存"""
        try:
            if self.theme_manager and hasattr(self.theme_manager, 'save_preference'):
                self.theme_manager.save_preference(theme_name)
            else:
                # 設定ファイルに保存（簡易版）
                self._save_basic_preference(theme_name)
                
        except Exception as e:
            self.logger.error(f"テーマ設定保存エラー: {e}")
    
    def _save_basic_preference(self, theme_name):
        """基本的なテーマ設定保存"""
        try:
            import json
            import os
            
            # 設定ディレクトリの作成
            config_dir = os.path.join(os.path.expanduser("~"), ".photomap-explorer")
            os.makedirs(config_dir, exist_ok=True)
            
            # 設定ファイルパス
            config_file = os.path.join(config_dir, "theme_config.json")
            
            # 設定データ
            from datetime import datetime
            config_data = {
                "current_theme": theme_name,
                "saved_at": str(datetime.now())
            }
            
            # JSONファイルに保存
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"基本テーマ設定保存エラー: {e}")
    
    def load_theme_preference(self):
        """保存されたテーマ設定を読み込み"""
        try:
            if self.theme_manager and hasattr(self.theme_manager, 'load_preference'):
                return self.theme_manager.load_preference()
            else:
                # 設定ファイルから読み込み（簡易版）
                return self._load_basic_preference()
                
        except Exception as e:
            self.logger.error(f"テーマ設定読み込みエラー: {e}")
            return "default"
    
    def _load_basic_preference(self):
        """基本的なテーマ設定読み込み"""
        try:
            import json
            import os
            
            # 設定ファイルパス
            config_file = os.path.join(os.path.expanduser("~"), ".photomap-explorer", "theme_config.json")
            
            if not os.path.exists(config_file):
                return "default"
            
            # JSONファイルから読み込み
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
                
            return config_data.get("current_theme", "default")
            
        except Exception as e:
            self.logger.error(f"基本テーマ設定読み込みエラー: {e}")
            return "default"
    
    def initialize_theme(self):
        """テーマの初期化"""
        try:
            if self.theme_manager and hasattr(self.theme_manager, 'get_current_theme'):
                # 新しい統合テーママネージャーから現在のテーマを取得
                current_theme = self.theme_manager.get_current_theme()
                self.logger.verbose(f"保存されたテーマで初期化: {current_theme}")
                
                # テーマを適用（統合テーママネージャーでは自動的に適用される）
                self.current_theme = current_theme
                self._apply_theme(current_theme)
                return
                
            # フォールバック処理
            self.logger.warning("保存されたテーマの適用に失敗、ダークテーマにフォールバック")
            self.on_theme_changed("dark")
            
        except Exception as e:
            self.logger.error(f"テーマ初期化エラー: {e}")
            # デフォルトテーマにフォールバック
            self.on_theme_changed("dark")
    
    def toggle_theme(self):
        """テーマを切り替え（サイクル）"""
        try:
            if self.theme_manager and hasattr(self.theme_manager, 'cycle_theme'):
                # 新しい統合テーママネージャーのサイクル機能を使用
                new_theme = self.theme_manager.cycle_theme()
                self.current_theme = new_theme
                
                # UIに統合テーママネージャーのスタイルシートを適用
                if hasattr(self.theme_manager, 'get_theme_stylesheet'):
                    stylesheet = self.theme_manager.get_theme_stylesheet()
                    if stylesheet:
                        self.main_window.setStyleSheet(stylesheet)
                
                self.main_window.show_status_message(f"🎨 テーマ切り替え: {new_theme}")
                self._refresh_ui()
                
            elif self.theme_manager and hasattr(self.theme_manager, 'get_theme_names'):
                # 手動でサイクル処理
                available_themes = self.theme_manager.get_theme_names()
                if available_themes:
                    current_index = 0
                    try:
                        current_index = available_themes.index(self.current_theme)
                    except ValueError:
                        pass
                    
                    next_index = (current_index + 1) % len(available_themes)
                    next_theme = available_themes[next_index]
                    
                    success = self.theme_manager.set_theme(next_theme)
                    if success:
                        self.current_theme = next_theme
                        self.main_window.show_status_message(f"🎨 テーマ切り替え: {next_theme}")
                        self._refresh_ui()
                
            else:
                # フォールバック: 従来の方法
                if self.current_theme == "dark":
                    self.on_theme_changed("light")
                    self._update_theme_button_text("🌙 ダーク")
                else:
                    self.on_theme_changed("dark")
                    self._update_theme_button_text("☀️ ライト")
                
        except Exception as e:
            self.logger.error(f"テーマ切り替えエラー: {e}")
            self.main_window.show_status_message(f"❌ テーマ切り替えエラー: {e}")
    
    def _update_theme_button_text(self, text):
        """テーマボタンのテキストを更新"""
        try:
            if hasattr(self.main_window, 'theme_toggle_btn') and self.main_window.theme_toggle_btn:
                self.main_window.theme_toggle_btn.setText(text)
        except Exception as e:
            self.logger.error(f"テーマボタンテキスト更新エラー: {e}")
    
    def apply_theme_to_component(self, component, theme_name=None):
        """特定のコンポーネントにテーマを適用"""
        try:
            if not theme_name:
                theme_name = self.current_theme
                
            if self.theme_manager and hasattr(self.theme_manager, 'apply_to_component'):
                self.theme_manager.apply_to_component(component, theme_name)
            else:
                # 基本的なテーマ適用
                self._apply_basic_component_theme(component, theme_name)
                
        except Exception as e:
            self.logger.error(f"コンポーネントテーマ適用エラー: {e}")
    
    def _apply_basic_component_theme(self, component, theme_name):
        """基本的なコンポーネントテーマ適用"""
        try:
            # 基本的なテーマスタイルをコンポーネントに適用
            if hasattr(component, 'setStyleSheet') and theme_name == "dark":
                component.setStyleSheet("""
                    QWidget {
                        background-color: #2d2d2d;
                        color: #ffffff;
                    }
                    QLabel {
                        color: #ffffff;
                    }
                """)
                
        except Exception as e:
            self.logger.error(f"基本コンポーネントテーマ適用エラー: {e}")
    
    def _apply_navigation_theme(self, theme_name):
        """ナビゲーションコントロールにテーマを適用"""
        try:
            if hasattr(self.main_window, 'controls_widget') and self.main_window.controls_widget:
                from ui.controls.toolbar.navigation_controls import NavigationControls
                for nav_control in self.main_window.controls_widget.findChildren(NavigationControls):
                    if hasattr(nav_control, 'apply_theme'):
                        nav_control.apply_theme(theme_name)
                        self.logger.debug(f"ナビゲーションコントロールにテーマ適用: {theme_name}")
        except Exception as e:
            self.logger.error(f"ナビゲーションテーマ適用エラー: {e}")
