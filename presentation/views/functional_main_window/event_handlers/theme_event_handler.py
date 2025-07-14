"""
テーマ切り替えイベント処理を担当するハンドラ

このモジュールは functional_new_main_view.py から分離された
テーマ関連のイベント処理機能を担当します。
"""

import logging
from PyQt5.QtWidgets import QMessageBox


class ThemeEventHandler:
    """テーマ切り替えイベント処理を担当するハンドラ"""
    
    def __init__(self, main_window):
        """
        テーマイベントハンドラを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.current_theme = "default"
        
        # コンポーネント参照
        self.theme_manager = None
        
    def set_components(self, theme_manager):
        """テーママネージャーの参照を設定"""
        self.theme_manager = theme_manager
    
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
                
            else:
                self.main_window.show_status_message(f"❌ テーマ変更に失敗: {theme_name}")
                
        except Exception as e:
            logging.error(f"テーマ変更エラー: {e}")
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
            logging.error(f"テーマ適用エラー: {e}")
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
            
            # メインウィンドウにスタイルシートを適用
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
            
        except Exception as e:
            logging.error(f"基本テーマ適用エラー: {e}")
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
            logging.error(f"UI再描画エラー: {e}")
    
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
            logging.error(f"テーマ一覧取得エラー: {e}")
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
            logging.error(f"テーマ設定保存エラー: {e}")
    
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
            logging.error(f"基本テーマ設定保存エラー: {e}")
    
    def load_theme_preference(self):
        """保存されたテーマ設定を読み込み"""
        try:
            if self.theme_manager and hasattr(self.theme_manager, 'load_preference'):
                return self.theme_manager.load_preference()
            else:
                # 設定ファイルから読み込み（簡易版）
                return self._load_basic_preference()
                
        except Exception as e:
            logging.error(f"テーマ設定読み込みエラー: {e}")
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
            logging.error(f"基本テーマ設定読み込みエラー: {e}")
            return "default"
    
    def initialize_theme(self):
        """テーマの初期化"""
        try:
            # 保存されたテーマ設定を読み込み
            saved_theme = self.load_theme_preference()
            
            # テーマを適用
            self.on_theme_changed(saved_theme)
            
        except Exception as e:
            logging.error(f"テーマ初期化エラー: {e}")
            # デフォルトテーマにフォールバック
            self.on_theme_changed("default")
    
    def toggle_theme(self):
        """テーマを切り替え（dark ↔ default）"""
        try:
            if self.current_theme == "dark":
                self.on_theme_changed("default")
            else:
                self.on_theme_changed("dark")
                
        except Exception as e:
            logging.error(f"テーマ切り替えエラー: {e}")
            self.main_window.show_status_message(f"❌ テーマ切り替えエラー: {e}")
    
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
            logging.error(f"コンポーネントテーマ適用エラー: {e}")
    
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
            logging.error(f"基本コンポーネントテーマ適用エラー: {e}")
