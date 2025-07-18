"""
GIMP風アドレスバー制御機能を担当するマネージャー

このモジュールは functional_new_main_view.py から分離された
アドレスバー関連の機能を担当します。
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import QMessageBox
import logging


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
        if self.address_bar and hasattr(self.address_bar, 'path_changed'):
            self.address_bar.path_changed.connect(self.on_address_changed)
        
        # アドレスバーの初期設定
        self._initialize_address_bar()
    
    def _initialize_address_bar(self):
        """アドレスバーの初期設定"""
        try:
            if not self.address_bar:
                logging.warning("アドレスバーコンポーネントが設定されていません")
                return
            
            # 表示状態を確保
            if hasattr(self.address_bar, 'setVisible'):
                self.address_bar.setVisible(True)
            
            # プレースホルダーを設定（フォルダラベルの場合は不要）
            # self.set_placeholder_text("パスを入力してください...")
            
            # ホームディレクトリをデフォルトパスとして設定
            import os
            home_path = os.path.expanduser("~")
            self.update_address_bar(home_path)
            
            logging.debug("フォルダパス表示初期化完了")
            
        except Exception as e:
            logging.error(f"アドレスバー初期化エラー: {e}")
    
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
            else:
                # フォールバック：メインウィンドウのメソッド呼び出し
                if hasattr(self.main_window, 'load_folder'):
                    self.main_window.load_folder(folder_path)
                    
        except Exception as e:
            logging.error(f"アドレスバー経由フォルダ読み込みエラー: {e}")
            self.main_window.show_status_message(f"❌ フォルダ読み込みエラー: {e}")
    
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
            else:
                # 現在のパスがない場合は空にする
                if self.address_bar:
                    self.address_bar.setText("")
                    
        except Exception as e:
            logging.error(f"無効パス処理エラー: {e}")
    
    def update_address_bar(self, folder_path):
        """フォルダパス表示ラベルを更新"""
        try:
            logging.debug(f"=== AddressBarManager.update_address_bar呼び出し ===")
            logging.debug(f"folder_path: {folder_path}")
            logging.debug(f"self.address_bar: {self.address_bar}")
            logging.debug(f"self.address_bar type: {type(self.address_bar) if self.address_bar else None}")
            
            if not self.address_bar:
                logging.warning("フォルダパス表示更新: フォルダラベルが設定されていません")
                return
            
            # パスを正規化
            normalized_path = os.path.normpath(folder_path) if folder_path else ""
            
            # 現在のパスを更新
            self.current_path = normalized_path
            
            # フォルダラベルを更新
            if hasattr(self.address_bar, 'update_folder_path'):
                # 新しいフォルダラベルの場合
                logging.debug("新しいフォルダラベルのupdate_folder_pathメソッドを呼び出し")
                self.address_bar.update_folder_path(normalized_path)
            elif hasattr(self.address_bar, 'setText'):
                # 旧来のQLineEdit/QLabelの場合（後方互換性）
                logging.debug("setTextメソッドを呼び出し")
                self.address_bar.setText(normalized_path)
            elif hasattr(self.address_bar, 'set_path'):
                # IntegratedAddressBarの場合（後方互換性）
                logging.debug("set_pathメソッドを呼び出し")
                self.address_bar.set_path(normalized_path)
            else:
                logging.warning(f"フォルダラベルに適切な設定メソッドが見つかりません: {type(self.address_bar)}")
                logging.debug(f"利用可能なメソッド: {[attr for attr in dir(self.address_bar) if not attr.startswith('_')]}")
            
            logging.debug(f"フォルダパス表示更新完了: {normalized_path}")
            
        except Exception as e:
            logging.error(f"フォルダパス表示更新エラー: {e}")
    
    def clear_address_bar(self):
        """フォルダパス表示をクリア"""
        try:
            if self.address_bar:
                if hasattr(self.address_bar, 'update_folder_path'):
                    # 新しいフォルダラベルの場合
                    self.address_bar.update_folder_path("")
                elif hasattr(self.address_bar, 'setText'):
                    # 旧来のQLineEdit/QLabel の場合
                    self.address_bar.setText("")
            self.current_path = None
            
        except Exception as e:
            logging.error(f"フォルダパス表示クリアエラー: {e}")
    
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
            if self.address_bar:
                # IntegratedAddressBarの場合
                if hasattr(self.address_bar, 'text_input_handler'):
                    handler = self.address_bar.text_input_handler
                    if handler and hasattr(handler, 'text_edit') and handler.text_edit:
                        handler.text_edit.setPlaceholderText(placeholder)
                        logging.debug(f"統合アドレスバーのプレースホルダーを設定: {placeholder}")
                        return
                
                # 標準QLineEditの場合
                if hasattr(self.address_bar, 'setPlaceholderText'):
                    self.address_bar.setPlaceholderText(placeholder)
                    logging.debug(f"アドレスバーのプレースホルダーを設定: {placeholder}")
                    return
                
                # カスタムメソッドの場合
                if hasattr(self.address_bar, 'set_placeholder_text'):
                    self.address_bar.set_placeholder_text(placeholder)
                    logging.debug(f"カスタムアドレスバーのプレースホルダーを設定: {placeholder}")
                    return
                
                logging.debug(f"アドレスバーにプレースホルダー設定機能が見つかりません - タイプ: {type(self.address_bar)}")
            else:
                logging.debug("アドレスバーが設定されていません")
                
        except Exception as e:
            logging.error(f"プレースホルダー設定エラー: {e}")
    
    def apply_delayed_theme(self):
        """遅延テーマ適用"""
        try:
            # 現在のテーマを取得して適用
            if hasattr(self.main_window, 'theme_manager'):
                current_theme = self.main_window.theme_manager.get_current_theme()
                theme_name = current_theme.value if hasattr(current_theme, 'value') else str(current_theme)
                self.apply_theme(theme_name)
            else:
                # フォールバック：デフォルトテーマを適用
                self.apply_theme("light")
                
        except Exception as e:
            logging.error(f"遅延テーマ適用エラー: {e}")
