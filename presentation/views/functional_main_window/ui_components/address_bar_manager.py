"""
GIMP風アドレスバー制御機能を担当するマネージャー

このモジュールは functional_new_main_view.py から分離された
アドレスバー関連の機能を担当します。
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
import logging
from utils.debug_logger import debug, info, warning, error, verbose


class AddressBarManager:
    """GIMP風アドレスバー制御機能を担当するマネージャー"""
    
    def __init__(self, main_window):
        """
        アドレスバーマネージャーを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.current_path = None
        
        # コンポーネント参照
        self.address_bar = None
        self.folder_handler = None
        
    def set_components(self, address_bar, folder_handler):
        """コンポーネントの参照を設定"""
        self.address_bar = address_bar
        self.folder_handler = folder_handler
        
        # アドレスバーのシグナル接続
        if self.address_bar:
            if hasattr(self.address_bar, 'path_changed'):
                self.address_bar.path_changed.connect(self.on_address_changed)
            if hasattr(self.address_bar, 'navigation_requested'):
                self.address_bar.navigation_requested.connect(self.on_navigation_requested)
    
    def on_address_changed(self, new_path):
        """GIMP風アドレスバーでパスが変更された時の処理"""
        try:
            # パスを正規化
            new_path = os.path.normpath(new_path) if new_path else ""
            
            if new_path and os.path.exists(new_path) and os.path.isdir(new_path):
                # 現在のパスと異なる場合のみロード
                if new_path != self.current_path:
                    self._load_folder_via_address_bar(new_path)
                else:
                    # 同じパスの場合はリフレッシュ
                    self.main_window.show_status_message(f"📁 現在のフォルダ: {new_path}")
            elif not new_path:
                # 空パスの場合は全ドライブ表示状態
                self._show_drives_view()
            else:
                # 無効なパス
                self._handle_invalid_path(new_path)
                
        except Exception as e:
            QMessageBox.warning(self.main_window, "エラー", f"パス変更エラー: {e}")
            self.main_window.show_status_message(f"❌ パス変更エラー: {e}")
            logging.error(f"アドレスバーパス変更エラー: {e}")
    
    def _load_folder_via_address_bar(self, folder_path):
        """アドレスバー経由でフォルダを読み込み"""
        try:
            self.current_path = folder_path
            
            # フォルダハンドラに処理を委譲
            if self.folder_handler:
                self.folder_handler.load_folder(folder_path)
            elif hasattr(self.main_window, 'folder_event_handler') and self.main_window.folder_event_handler:
                # 正しいフォルダイベントハンドラを使用
                self.main_window.folder_event_handler.load_folder(folder_path)
            else:
                self.main_window.show_status_message("❌ フォルダハンドラが見つかりません")
                    
        except Exception as e:
            logging.error(f"アドレスバー経由フォルダ読み込みエラー: {e}")
            self.main_window.show_status_message(f"❌ フォルダ読み込みエラー: {e}")
    
    def on_navigation_requested(self, path):
        """パンくずリストのナビゲーション要求時の処理"""
        try:
            # パスを正規化
            path = os.path.normpath(path) if path else ""
            
            if path and os.path.exists(path) and os.path.isdir(path):
                self._load_folder_via_address_bar(path)
                verbose(f"パンくずリストナビゲーション: {path}")
            else:
                warning(f"無効なパス: {path}")
                self._handle_invalid_path(path)
                
        except Exception as e:
            error(f"パンくずリストナビゲーションエラー: {e}")
            self.main_window.show_status_message(f"❌ ナビゲーションエラー: {e}")
    
    def _show_drives_view(self):
        """全ドライブ表示状態"""
        try:
            self.main_window.show_status_message("💻 全ドライブ表示")
            
            # フォルダハンドラがあれば、ルートディレクトリ表示を委譲
            if self.folder_handler and hasattr(self.folder_handler, 'show_drives'):
                self.folder_handler.show_drives()
            else:
                # フォールバック：ホームディレクトリを表示
                home_dir = os.path.expanduser("~")
                self._load_folder_via_address_bar(home_dir)
                
        except Exception as e:
            logging.error(f"ドライブ表示エラー: {e}")
    
    def _handle_invalid_path(self, invalid_path):
        """無効なパスの処理"""
        try:
            QMessageBox.warning(self.main_window, "パスエラー", f"無効なパス: {invalid_path}")
            
            # アドレスバーを現在のパスに戻す
            if self.address_bar and self.current_path:
                self.address_bar.setText(self.current_path)
            # 現在のパスがない場合は何もしない（空文字列設定を避ける）
                    
        except Exception as e:
            logging.error(f"無効パス処理エラー: {e}")
    
    def update_address_bar(self, folder_path):
        """アドレスバーの表示を更新"""
        try:
            if not self.address_bar:
                return
            
            # パスを正規化
            normalized_path = os.path.normpath(folder_path) if folder_path else ""
            
            # 現在のパスを更新
            self.current_path = normalized_path
            
            # アドレスバーを直接更新（不要な空文字列設定を削除）
            self.address_bar.setText(normalized_path)
            
        except Exception as e:
            logging.error(f"アドレスバー更新エラー: {e}")
    
    def clear_address_bar(self):
        """アドレスバーをクリア（必要な場合のみ使用）"""
        try:
            # 通常は空文字列設定を避ける
            # この関数は特別な場合（エラー処理等）のみ使用
            if self.address_bar:
                self.address_bar.setText("")
            self.current_path = None
            
        except Exception as e:
            logging.error(f"アドレスバークリアエラー: {e}")
    
    def go_to_parent_folder(self):
        """親フォルダへ移動"""
        try:
            if not self.current_path:
                return
            
            parent_path = str(Path(self.current_path).parent)
            
            # ルートディレクトリの場合は移動しない
            if parent_path == self.current_path:
                self.main_window.show_status_message("📁 すでにルートディレクトリです")
                return
            
            # 親ディレクトリに移動
            self.on_address_changed(parent_path)
            
        except Exception as e:
            logging.error(f"親フォルダ移動エラー: {e}")
            self.main_window.show_status_message(f"❌ 親フォルダ移動エラー: {e}")
    
    def go_to_home_folder(self):
        """ホームフォルダへ移動"""
        try:
            home_path = os.path.expanduser("~")
            self.on_address_changed(home_path)
            
        except Exception as e:
            logging.error(f"ホームフォルダ移動エラー: {e}")
            self.main_window.show_status_message(f"❌ ホームフォルダ移動エラー: {e}")
    
    def navigate_to_path(self, path):
        """指定パスに移動"""
        try:
            if not path:
                return
            
            # パスの存在確認
            if not os.path.exists(path):
                QMessageBox.warning(self.main_window, "パスエラー", f"パスが存在しません: {path}")
                return
            
            # ディレクトリ確認
            if not os.path.isdir(path):
                QMessageBox.warning(self.main_window, "パスエラー", f"指定パスはディレクトリではありません: {path}")
                return
            
            # アドレスバー経由で移動
            self.on_address_changed(path)
            
        except Exception as e:
            logging.error(f"パス移動エラー: {e}")
            self.main_window.show_status_message(f"❌ パス移動エラー: {e}")
    
    def get_current_path(self):
        """現在のパスを取得"""
        return self.current_path
    
    def validate_path(self, path):
        """パスの妥当性を検証"""
        try:
            if not path:
                return False, "パスが空です"
            
            if not os.path.exists(path):
                return False, "パスが存在しません"
            
            if not os.path.isdir(path):
                return False, "ディレクトリではありません"
            
            # アクセス権限チェック
            if not os.access(path, os.R_OK):
                return False, "読み取り権限がありません"
            
            return True, "パスは有効です"
            
        except Exception as e:
            return False, f"パス検証エラー: {e}"
    
    def get_path_components(self, path=None):
        """パスの構成要素を取得（ブレッドクラム用）"""
        try:
            target_path = path or self.current_path
            if not target_path:
                return []
            
            components = []
            path_obj = Path(target_path)
            
            # ルートから現在のパスまでの各ディレクトリを取得
            for parent in reversed(path_obj.parents):
                components.append({
                    'name': parent.name or str(parent),  # ルートの場合は"/"など
                    'path': str(parent)
                })
            
            # 現在のディレクトリを追加
            components.append({
                'name': path_obj.name or str(path_obj),
                'path': str(path_obj)
            })
            
            return components
            
        except Exception as e:
            logging.error(f"パス構成要素取得エラー: {e}")
            return []
    
    def apply_theme(self, theme_name):
        """アドレスバーにテーマを適用"""
        try:
            if not self.address_bar:
                return
            
            # テーマに応じたスタイルを適用
            if hasattr(self.address_bar, 'apply_theme'):
                self.address_bar.apply_theme(theme_name)
            elif hasattr(self.address_bar, 'setStyleSheet'):
                # 基本的なテーマスタイル適用
                self._apply_basic_theme_style(theme_name)
                
        except Exception as e:
            logging.error(f"アドレスバーテーマ適用エラー: {e}")
    
    def _apply_basic_theme_style(self, theme_name):
        """基本的なテーマスタイル適用"""
        try:
            if theme_name == "dark":
                style = """
                    QLineEdit {
                        background-color: #2d2d2d;
                        color: #ffffff;
                        border: 1px solid #404040;
                        border-radius: 4px;
                        padding: 4px;
                    }
                    QLineEdit:focus {
                        border-color: #007ACC;
                    }
                """
            else:
                style = """
                    QLineEdit {
                        background-color: #ffffff;
                        color: #000000;
                        border: 1px solid #cccccc;
                        border-radius: 4px;
                        padding: 4px;
                    }
                    QLineEdit:focus {
                        border-color: #007ACC;
                    }
                """
            
            self.address_bar.setStyleSheet(style)  # type: ignore
            
        except Exception as e:
            logging.error(f"基本テーマスタイル適用エラー: {e}")
    
    def set_read_only(self, read_only=True):
        """アドレスバーの読み取り専用設定"""
        try:
            if self.address_bar and hasattr(self.address_bar, 'setReadOnly'):
                self.address_bar.setReadOnly(read_only)
                
        except Exception as e:
            logging.error(f"読み取り専用設定エラー: {e}")
    
    def set_placeholder_text(self, placeholder):
        """プレースホルダーテキストを設定"""
        try:
            if self.address_bar and hasattr(self.address_bar, 'setPlaceholderText'):
                self.address_bar.setPlaceholderText(placeholder)
                
        except Exception as e:
            logging.error(f"プレースホルダー設定エラー: {e}")
