"""
テキスト入力処理ハンドラーモジュール

このモジュールは ui/controls.py から分離された
アドレスバーのテキスト入力、補完、履歴機能を提供します。
"""

from PyQt5.QtWidgets import QLineEdit, QCompleter, QFileSystemModel
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QStringListModel
from PyQt5.QtGui import QFont, QKeySequence
import os
import logging
from typing import List, Optional


class TextInputHandler(QObject):
    """
    アドレスバーテキスト入力処理クラス
    
    パス入力、自動補完、履歴管理、バリデーション機能を提供
    """
    
    # シグナル
    path_entered = pyqtSignal(str)  # パス入力完了
    path_changed = pyqtSignal(str)  # パス変更
    edit_mode_requested = pyqtSignal(bool)  # 編集モード切り替え要求
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 設定
        self.max_history = 50
        self.enable_completion = True
        
        # 状態管理
        self.path_history: List[str] = []
        self.current_text = ""
        self.is_completion_active = False
        
        # コンポーネント
        self.text_edit: Optional[QLineEdit] = None
        self.completer: Optional[QCompleter] = None
        self.filesystem_model: Optional[QFileSystemModel] = None
        
    def setup_text_input(self, line_edit: QLineEdit):
        """
        テキスト入力フィールドを設定
        
        Args:
            line_edit: 設定対象のQLineEdit
        """
        try:
            self.text_edit = line_edit
            
            # 基本設定
            self._setup_basic_properties()
            
            # 自動補完設定
            if self.enable_completion:
                self._setup_completion()
            
            # イベント接続
            self._connect_events()
            
            # フォント設定
            self._setup_font()
            
        except Exception as e:
            logging.error(f"テキスト入力設定エラー: {e}")
    
    def _setup_basic_properties(self):
        """基本プロパティを設定"""
        try:
            if not self.text_edit:
                return
            
            self.text_edit.setMinimumHeight(28)
            self.text_edit.setMaximumHeight(34)
            self.text_edit.setPlaceholderText("パスを入力してください...")
            
            # 初期状態は非表示
            self.text_edit.setVisible(False)
            
        except Exception as e:
            logging.error(f"基本プロパティ設定エラー: {e}")
    
    def _setup_completion(self):
        """自動補完機能を設定"""
        try:
            if not self.text_edit:
                return
            
            # ファイルシステムモデル
            self.filesystem_model = QFileSystemModel()
            self.filesystem_model.setRootPath("")
            
            # コンプリーター
            self.completer = QCompleter()
            self.completer.setModel(self.filesystem_model)
            self.completer.setCaseSensitivity(Qt.CaseInsensitive)  # type: ignore
            self.completer.setCompletionMode(QCompleter.PopupCompletion)  # type: ignore
            
            # テキストエディットに設定
            self.text_edit.setCompleter(self.completer)
            
            # 補完関連イベント
            if self.completer:
                self.completer.activated.connect(self._on_completion_activated)
            
        except Exception as e:
            logging.error(f"自動補完設定エラー: {e}")
    
    def _connect_events(self):
        """イベントを接続"""
        try:
            if not self.text_edit:
                return
            
            # 基本イベント
            self.text_edit.returnPressed.connect(self._on_return_pressed)
            self.text_edit.editingFinished.connect(self._on_editing_finished)
            self.text_edit.textChanged.connect(self._on_text_changed)
            
            # キーイベント（カスタム処理用）
            self.text_edit.installEventFilter(self)
            
        except Exception as e:
            logging.error(f"イベント接続エラー: {e}")
    
    def _setup_font(self):
        """フォントを設定"""
        try:
            if not self.text_edit:
                return
            
            font = QFont()
            font.setFamily("Consolas, Monaco, monospace")  # 等幅フォント
            font.setPointSize(10)
            font.setWeight(QFont.Normal)
            
            self.text_edit.setFont(font)
            
        except Exception as e:
            logging.error(f"フォント設定エラー: {e}")
    
    def enter_edit_mode(self, current_path: str = ""):
        """編集モードに入る"""
        try:
            if not self.text_edit:
                return
            
            # テキスト設定
            self.text_edit.setText(current_path)
            self.current_text = current_path
            
            # 表示・フォーカス
            self.text_edit.setVisible(True)
            self.text_edit.setFocus()
            self.text_edit.selectAll()
            
            # 補完モデル更新
            self._update_completion_model(current_path)
            
        except Exception as e:
            logging.error(f"編集モード開始エラー: {e}")
    
    def exit_edit_mode(self):
        """編集モードを終了"""
        try:
            if not self.text_edit:
                return
            
            self.text_edit.setVisible(False)
            self.text_edit.clearFocus()
            
            # 補完を閉じる
            if self.completer:
                self.completer.popup().hide()  # type: ignore
            
        except Exception as e:
            logging.error(f"編集モード終了エラー: {e}")
    
    def _update_completion_model(self, path: str):
        """補完モデルを更新"""
        try:
            if not self.filesystem_model or not path:
                return
            
            # ディレクトリ部分を取得
            dir_path = os.path.dirname(path) if os.path.isfile(path) else path
            
            if os.path.isdir(dir_path):
                self.filesystem_model.setRootPath(dir_path)
            
        except Exception as e:
            logging.error(f"補完モデル更新エラー: {e}")
    
    def _on_return_pressed(self):
        """Enterキー押下時の処理"""
        try:
            if not self.text_edit:
                return
            
            entered_path = self.text_edit.text().strip()
            
            # パス検証
            if self._validate_input_path(entered_path):
                # 履歴に追加
                self._add_to_history(entered_path)
                
                # パス確定シグナル
                self.path_entered.emit(entered_path)
                
                # 編集モード終了
                self.edit_mode_requested.emit(False)
            else:
                # 無効なパスの場合の処理
                self._handle_invalid_path(entered_path)
            
        except Exception as e:
            logging.error(f"Enter処理エラー: {e}")
    
    def _on_editing_finished(self):
        """編集終了時の処理"""
        try:
            # フォーカスが外れた場合の処理
            self.edit_mode_requested.emit(False)
            
        except Exception as e:
            logging.error(f"編集終了処理エラー: {e}")
    
    def _on_text_changed(self, text: str):
        """テキスト変更時の処理"""
        try:
            self.current_text = text
            
            # リアルタイム補完モデル更新
            if self.enable_completion and len(text) > 2:
                self._update_completion_model(text)
            
            # パス変更シグナル（リアルタイム）
            self.path_changed.emit(text)
            
        except Exception as e:
            logging.error(f"テキスト変更処理エラー: {e}")
    
    def _on_completion_activated(self, text: str):
        """補完選択時の処理"""
        try:
            if not self.text_edit:
                return
            
            # 補完されたパスを設定
            self.text_edit.setText(text)
            
            # フォーカスを維持
            self.text_edit.setFocus()
            
        except Exception as e:
            logging.error(f"補完選択処理エラー: {e}")
    
    def _validate_input_path(self, path: str) -> bool:
        """入力パスの妥当性を検証"""
        try:
            if not path:
                return False
            
            # パスの正規化
            normalized_path = os.path.normpath(path)
            
            # 存在確認
            if os.path.exists(normalized_path):
                return True
            
            # 部分パスの場合の処理
            if self._is_partial_path(normalized_path):
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"パス検証エラー: {e}")
            return False
    
    def _is_partial_path(self, path: str) -> bool:
        """部分パス（入力途中）かどうかを判定"""
        try:
            # 親ディレクトリが存在する場合は有効とみなす
            parent = os.path.dirname(path)
            return os.path.exists(parent) if parent != path else False
            
        except Exception as e:
            logging.error(f"部分パス判定エラー: {e}")
            return False
    
    def _handle_invalid_path(self, path: str):
        """無効なパス入力時の処理"""
        try:
            if not self.text_edit:
                return
            
            # エラー表示（背景色変更など）
            self.text_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #fff0f0;
                    border: 2px solid #ff6666;
                }
            """)
            
            # 一定時間後に元に戻す
            # TODO: QTimerを使用して背景色をリセット
            
            logging.warning(f"無効なパス入力: {path}")
            
        except Exception as e:
            logging.error(f"無効パス処理エラー: {e}")
    
    def _add_to_history(self, path: str):
        """パス履歴に追加"""
        try:
            # 重複を除去
            if path in self.path_history:
                self.path_history.remove(path)
            
            # 先頭に追加
            self.path_history.insert(0, path)
            
            # 履歴サイズ制限
            if len(self.path_history) > self.max_history:
                self.path_history = self.path_history[:self.max_history]
            
        except Exception as e:
            logging.error(f"履歴追加エラー: {e}")
    
    def get_history(self) -> List[str]:
        """パス履歴を取得"""
        return self.path_history.copy()
    
    def clear_history(self):
        """履歴をクリア"""
        self.path_history.clear()
    
    def set_completion_enabled(self, enabled: bool):
        """補完機能の有効/無効を設定"""
        try:
            self.enable_completion = enabled
            
            if self.text_edit and self.completer:
                if enabled:
                    self.text_edit.setCompleter(self.completer)
                else:
                    self.text_edit.setCompleter(None)
            
        except Exception as e:
            logging.error(f"補完設定エラー: {e}")
    
    def eventFilter(self, obj, event):
        """イベントフィルター（カスタムキー処理）"""
        try:
            if obj == self.text_edit and event.type() == event.KeyPress:
                # Escapeキー: 編集モード終了
                if event.key() == Qt.Key_Escape:  # type: ignore
                    self.edit_mode_requested.emit(False)
                    return True
                
                # Ctrl+L: テキスト全選択
                elif event.matches(QKeySequence.SelectAll):  # type: ignore
                    if self.text_edit:
                        self.text_edit.selectAll()
                    return True
            
            return super().eventFilter(obj, event)
            
        except Exception as e:
            logging.error(f"イベントフィルターエラー: {e}")
            return False
    
    def apply_theme_style(self, theme_name: str):
        """テーマスタイルを適用"""
        try:
            if not self.text_edit:
                return
            
            if theme_name == "dark":
                style = self._get_dark_theme_style()
            else:
                style = self._get_light_theme_style()
            
            self.text_edit.setStyleSheet(style)
            
        except Exception as e:
            logging.error(f"テーマスタイル適用エラー: {e}")
    
    def _get_light_theme_style(self) -> str:
        """ライトテーマスタイル"""
        return """
            QLineEdit {
                background-color: white;
                border: 2px solid #d0d0d0;
                border-radius: 4px;
                padding: 4px 8px;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
                selection-background-color: #3399ff;
            }
            QLineEdit:focus {
                border-color: #0078d4;
                background-color: #fff;
            }
            QLineEdit:hover {
                border-color: #b0b0b0;
            }
        """
    
    def _get_dark_theme_style(self) -> str:
        """ダークテーマスタイル"""
        return """
            QLineEdit {
                background-color: #2d2d30;
                border: 2px solid #464647;
                border-radius: 4px;
                padding: 4px 8px;
                color: #f0f0f0;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 10pt;
                selection-background-color: #264f78;
            }
            QLineEdit:focus {
                border-color: #007acc;
                background-color: #1e1e1e;
            }
            QLineEdit:hover {
                border-color: #6a6a6b;
            }
        """
    
    def get_current_text(self) -> str:
        """現在のテキストを取得"""
        return self.current_text
    
    def set_text(self, text: str):
        """テキストを設定"""
        try:
            if self.text_edit:
                self.text_edit.setText(text)
            self.current_text = text
            
        except Exception as e:
            logging.error(f"テキスト設定エラー: {e}")
    
    def reset_style(self):
        """スタイルをリセット（エラー表示解除など）"""
        try:
            if self.text_edit:
                # 現在のテーマスタイルを再適用
                # テーマ名は外部から管理されているため、デフォルトスタイルを適用
                self.apply_theme_style("light")
            
        except Exception as e:
            logging.error(f"スタイルリセットエラー: {e}")
