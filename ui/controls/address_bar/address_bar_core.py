"""
アドレスバーのメイン機能を提供するコアモジュール

このモジュールは ui/controls.py から分離された
GIMP風アドレスバーのコア機能を提供します。
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from presentation.themes.theme_mixin import ThemeAwareMixin
from utils.debug_logger import debug, info, warning, error, verbose
import os
import logging
from typing import Optional


class AddressBarCore(QWidget, ThemeAwareMixin):
    """
    GIMP風ブレッドクラムアドレスバーのコア機能
    
    パスをボタン形式で表示し、クリックで移動可能
    テキスト入力モードとの切り替えも対応
    """
    
    path_changed = pyqtSignal(str)  # パス変更シグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # ThemeAwareMixinの初期化を明示的に呼び出し
        ThemeAwareMixin.__init__(self)
        
        self.current_path = ""
        self.is_edit_mode = False
        
        # コンポーネント
        self.breadcrumb_widget: Optional[QWidget] = None
        self.breadcrumb_layout: Optional[QHBoxLayout] = None
        self.text_edit: Optional[QLineEdit] = None
        self.edit_button: Optional[QPushButton] = None
        self.main_layout: Optional[QHBoxLayout] = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI初期化"""
        try:
            self.main_layout = QHBoxLayout(self)
            self.main_layout.setContentsMargins(2, 2, 2, 2)
            self.main_layout.setSpacing(2)
            
            # ブレッドクラムコンテナ
            self._create_breadcrumb_widget()
            
            # テキスト入力フィールド
            self._create_text_edit()
            
            # 編集ボタン
            self._create_edit_button()
            
            # レイアウト追加
            if self.main_layout and self.breadcrumb_widget:
                self.main_layout.addWidget(self.breadcrumb_widget, 1)  # 拡張可能
            if self.main_layout and self.text_edit:
                self.main_layout.addWidget(self.text_edit, 1)    # 編集モード時
            if self.main_layout and self.edit_button:
                self.main_layout.addWidget(self.edit_button)
            
            # 初期表示
            self.setText("")  # 初期パス
            
            # 初期テーマを適用
            self._apply_edit_button_theme()
            
            # テーマエンジンが遅延初期化される場合に備えて遅延適用も設定
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(500, self._delayed_theme_update)
            
        except Exception as e:
            logging.error(f"アドレスバーUI初期化エラー: {e}")
    
    def _delayed_theme_update(self):
        """遅延テーマ更新（テーマエンジンの初期化完了後）"""
        try:
            debug("アドレスバー遅延テーマ更新を実行")
            self._apply_edit_button_theme()
        except Exception as e:
            logging.error(f"アドレスバー遅延テーマ更新エラー: {e}")
    
    def _create_breadcrumb_widget(self):
        """ブレッドクラムウィジェットを作成"""
        try:
            self.breadcrumb_widget = QWidget()
            self.breadcrumb_widget.setMaximumHeight(34)
            self.breadcrumb_widget.setMinimumHeight(30)
            self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_widget)
            self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)
            self.breadcrumb_layout.setSpacing(1)
            
        except Exception as e:
            logging.error(f"ブレッドクラムウィジェット作成エラー: {e}")
    
    def _create_text_edit(self):
        """テキスト入力フィールドを作成"""
        try:
            self.text_edit = QLineEdit()
            self.text_edit.setVisible(False)
            self.text_edit.setMinimumHeight(28)
            self.text_edit.returnPressed.connect(self._on_text_entered)
            self.text_edit.editingFinished.connect(self._exit_edit_mode)
            
            # フォント設定
            text_font = QFont()
            text_font.setPointSize(10)
            self.text_edit.setFont(text_font)
            
        except Exception as e:
            logging.error(f"テキスト入力フィールド作成エラー: {e}")
    
    def _create_edit_button(self):
        """編集ボタンを作成"""
        try:
            self.edit_button = QPushButton("📝")
            self.edit_button.setFixedSize(35, 30)
            self.edit_button.setToolTip("テキスト入力モードに切り替え")
            self.edit_button.clicked.connect(self._toggle_edit_mode)
            
            # フォント設定
            edit_font = QFont()
            edit_font.setPointSize(12)
            self.edit_button.setFont(edit_font)
            
            # テーマスタイルを適用
            self._apply_edit_button_theme()
            
        except Exception as e:
            logging.error(f"編集ボタン作成エラー: {e}")
    
    def _apply_edit_button_theme(self):
        """編集ボタンにテーマスタイルを適用"""
        try:
            if not self.edit_button:
                return
                
            theme_data = self._get_theme_data()
            if not theme_data:
                # フォールバック用のデフォルトスタイル
                self.edit_button.setStyleSheet(self._get_fallback_edit_button_style())
                return
            
            button_config = theme_data.get('button', {})
            style = f"""
                QPushButton {{
                    background-color: {button_config.get('background', '#f0f0f0')};
                    color: {button_config.get('text', '#000000')};
                    border: 1px solid {button_config.get('border', '#d0d0d0')};
                    border-radius: 4px;
                    font-weight: 500;
                    padding: 2px;
                }}
                QPushButton:hover {{
                    background-color: {button_config.get('hover', '#e0e0e0')};
                    border-color: {button_config.get('border', '#d0d0d0')};
                }}
                QPushButton:pressed {{
                    background-color: {button_config.get('pressed', '#d0d0d0')};
                }}
                QPushButton:disabled {{
                    background-color: {theme_data.get('background', {}).get('secondary', '#f8f8f8')};
                    border-color: {theme_data.get('border', {}).get('color', '#e0e0e0')};
                    color: {theme_data.get('text', {}).get('muted', '#a0a0a0')};
                }}
            """
            self.edit_button.setStyleSheet(style)
            
        except Exception as e:
            logging.error(f"編集ボタンテーマ適用エラー: {e}")
            if self.edit_button:
                self.edit_button.setStyleSheet(self._get_fallback_edit_button_style())
    
    def _get_fallback_edit_button_style(self) -> str:
        """フォールバック用の編集ボタンスタイル"""
        return """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                font-weight: 500;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #b0b0b0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
    
    def setText(self, path):
        """パスを設定（外部から呼び出し可能）"""
        try:
            self.current_path = path
            if self.is_edit_mode:
                if self.text_edit:
                    self.text_edit.setText(path)
            else:
                self._update_breadcrumb(path)
                
        except Exception as e:
            logging.error(f"パス設定エラー: {e}")
    
    def text(self):
        """現在のパスを取得"""
        return self.current_path
    
    def _update_breadcrumb(self, path):
        """ブレッドクラム表示を更新"""
        try:
            if not self.breadcrumb_layout:
                return
            
            # 既存のボタンをクリア
            self._clear_breadcrumb_buttons()
            
            # 空のパスの場合は全ドライブ表示（Windows）
            if not path:
                if os.name == 'nt':  # Windows
                    self._show_all_drives()
                return
            
            # パスを分割して処理
            self._create_breadcrumb_buttons(path)
            
        except Exception as e:
            logging.error(f"ブレッドクラム更新エラー: {e}")
    
    def _clear_breadcrumb_buttons(self):
        """既存のブレッドクラムボタンをクリア"""
        try:
            if not self.breadcrumb_layout:
                return
            
            for i in reversed(range(self.breadcrumb_layout.count())):
                item = self.breadcrumb_layout.takeAt(i)
                if item and item.widget():
                    item.widget().deleteLater()  # type: ignore
                    
        except Exception as e:
            logging.error(f"ブレッドクラムボタンクリアエラー: {e}")
    
    def _create_breadcrumb_buttons(self, path):
        """パスからブレッドクラムボタンを作成"""
        try:
            # パスを正規化
            path = os.path.normpath(path)
            parts = self._split_path(path)
            
            # ボタンを作成
            all_buttons = []
            current_path = ""
            
            for i, part in enumerate(parts):
                if not part and i != 0:  # 空の部分をスキップ（ルート以外）
                    continue
                
                # パス構築
                current_path = self._build_current_path(current_path, part, i)
                
                # ボタン作成
                button = self._create_path_button(part, current_path)
                all_buttons.append(button)
            
            # ボタンレイアウト
            self._layout_buttons_with_priority(all_buttons)
            
        except Exception as e:
            logging.error(f"ブレッドクラムボタン作成エラー: {e}")
    
    def _split_path(self, path):
        """パスを分割"""
        try:
            parts = []
            
            if os.name == 'nt':  # Windows
                if ':' in path:
                    drive, rest = path.split(':', 1)
                    parts.append(drive + ':')
                    if rest and rest.strip('\\'):
                        folders = rest.strip('\\').split('\\')
                        parts.extend([folder for folder in folders if folder])
                else:
                    path_parts = path.strip('\\').split('\\')
                    parts = [part for part in path_parts if part]
            else:  # Unix系
                parts = path.strip('/').split('/')
                if path.startswith('/'):
                    parts.insert(0, '/')
            
            return parts
            
        except Exception as e:
            logging.error(f"パス分割エラー: {e}")
            return []
    
    def _build_current_path(self, current_path, part, index):
        """現在のパスを構築"""
        try:
            if os.name == 'nt':
                if index == 0:
                    # ドライブ部分
                    if part.endswith(':'):
                        return part + '\\\\'
                    else:
                        return part
                else:
                    return os.path.join(current_path, part)
            else:
                if part == '/':
                    return '/'
                else:
                    return os.path.join(current_path, part)
                    
        except Exception as e:
            logging.error(f"パス構築エラー: {e}")
            return current_path
    
    def _create_path_button(self, part, path):
        """パスボタンを作成"""
        try:
            button = QPushButton(part if part else '/')
            button.setProperty('path', path)
            button.clicked.connect(lambda checked, p=path: self._on_button_clicked(p))
            
            # フォント設定
            font = QFont()
            font.setPointSize(10)
            font.setWeight(QFont.Medium)
            button.setFont(font)
            
            # スタイル設定
            button.setStyleSheet(self._get_button_style())
            
            return button
            
        except Exception as e:
            logging.error(f"パスボタン作成エラー: {e}")
            return None
    
    def _layout_buttons_with_priority(self, all_buttons):
        """カレント側を優先してボタンを配置"""
        try:
            if not all_buttons or not self.breadcrumb_widget:
                return
            
            # 利用可能な幅を計算
            available_width = self.breadcrumb_widget.width() - 20  # type: ignore
            if available_width <= 0:
                available_width = 400
            
            # ボタン幅を計算
            total_width = sum(self._estimate_button_width(btn) for btn in all_buttons)
            
            # 全てのボタンが収まる場合
            if total_width <= available_width:
                for button in all_buttons:
                    if self.breadcrumb_layout:
                        self.breadcrumb_layout.addWidget(button)
                if self.breadcrumb_layout:
                    self.breadcrumb_layout.addStretch()
                return
            
            # 幅が足りない場合の処理
            self._layout_with_ellipsis(all_buttons, available_width)
            
        except Exception as e:
            logging.error(f"ボタンレイアウトエラー: {e}")
    
    def _estimate_button_width(self, button):
        """ボタン幅を推定"""
        try:
            text = button.text()
            return len(text) * 8 + 24 + 2  # 文字幅 + パディング + マージン
            
        except Exception as e:
            logging.error(f"ボタン幅推定エラー: {e}")
            return 50  # デフォルト幅
    
    def _layout_with_ellipsis(self, all_buttons, available_width):
        """省略記号を使用してボタンを配置"""
        try:
            if not self.breadcrumb_layout:
                return
                
            ellipsis_width = 30
            used_width = 0
            visible_buttons = []
            
            # 後ろから順に追加
            for i in reversed(range(len(all_buttons))):
                button = all_buttons[i]
                button_width = self._estimate_button_width(button)
                
                needed_width = used_width + button_width
                if len(visible_buttons) > 0:  # 省略記号が必要
                    needed_width += ellipsis_width
                
                if needed_width <= available_width:
                    visible_buttons.insert(0, button)
                    used_width += button_width
                else:
                    break
            
            # 省略記号を追加（必要な場合）
            if len(visible_buttons) < len(all_buttons):
                ellipsis_btn = QPushButton("...")
                ellipsis_btn.setFixedSize(ellipsis_width, 30)
                ellipsis_btn.setToolTip("省略されたパス要素")
                self.breadcrumb_layout.addWidget(ellipsis_btn)
            
            # 表示するボタンを追加
            for button in visible_buttons:
                self.breadcrumb_layout.addWidget(button)
            
            # 右端にスペーサー
            self.breadcrumb_layout.addStretch()
            
        except Exception as e:
            logging.error(f"省略記号レイアウトエラー: {e}")
    
    def _show_all_drives(self):
        """全ドライブを表示（Windows用）"""
        try:
            if not self.breadcrumb_layout:
                return
                
            import string
            from pathlib import Path
            
            for drive in string.ascii_uppercase:
                drive_path = f"{drive}:\\\\"
                if Path(drive_path).exists():
                    button = QPushButton(f"{drive}:")
                    button.setProperty('path', drive_path)
                    button.clicked.connect(lambda checked, p=drive_path: self._on_button_clicked(p))
                    button.setStyleSheet(self._get_button_style())
                    self.breadcrumb_layout.addWidget(button)
            
            self.breadcrumb_layout.addStretch()
            
        except Exception as e:
            logging.error(f"全ドライブ表示エラー: {e}")
    
    def _get_button_style(self):
        """ボタンスタイルを取得"""
        return """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 2px 8px;
                margin: 1px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #b0b0b0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
    
    def _on_button_clicked(self, path):
        """ボタンクリック時の処理"""
        try:
            self.current_path = path
            self.path_changed.emit(path)
            
        except Exception as e:
            logging.error(f"ボタンクリック処理エラー: {e}")
    
    def _toggle_edit_mode(self):
        """編集モードの切り替え"""
        try:
            if self.is_edit_mode:
                self._exit_edit_mode()
            else:
                self._enter_edit_mode()
                
        except Exception as e:
            logging.error(f"編集モード切り替えエラー: {e}")
    
    def _enter_edit_mode(self):
        """編集モードに入る"""
        try:
            self.is_edit_mode = True
            if self.breadcrumb_widget:
                self.breadcrumb_widget.setVisible(False)
            if self.text_edit:
                self.text_edit.setText(self.current_path)
                self.text_edit.setVisible(True)
                self.text_edit.setFocus()
                self.text_edit.selectAll()
            if self.edit_button:
                self.edit_button.setText("✓")
                self.edit_button.setToolTip("確定してブレッドクラムモードに戻る")
                
        except Exception as e:
            logging.error(f"編集モード開始エラー: {e}")
    
    def _exit_edit_mode(self):
        """編集モードを終了"""
        try:
            self.is_edit_mode = False
            if self.text_edit:
                self.text_edit.setVisible(False)
            if self.breadcrumb_widget:
                self.breadcrumb_widget.setVisible(True)
            if self.edit_button:
                self.edit_button.setText("📝")
                self.edit_button.setToolTip("テキスト入力モードに切り替え")
                
        except Exception as e:
            logging.error(f"編集モード終了エラー: {e}")
    
    def _on_text_entered(self):
        """テキスト入力確定時の処理"""
        try:
            if self.text_edit:
                new_path = self.text_edit.text().strip()
                if new_path != self.current_path:
                    self.current_path = new_path
                    self.path_changed.emit(new_path)
                    self._update_breadcrumb(new_path)
            
            self._exit_edit_mode()
            
        except Exception as e:
            logging.error(f"テキスト入力処理エラー: {e}")
    
    def keyPressEvent(self, event):
        """キーイベント処理"""
        try:
            if event.key() == Qt.Key_Escape:  # type: ignore
                if self.is_edit_mode:
                    if self.text_edit:
                        self.text_edit.setText(self.current_path)  # 元に戻す
                    self._exit_edit_mode()
            super().keyPressEvent(event)
            
        except Exception as e:
            logging.error(f"キーイベント処理エラー: {e}")
    
    def apply_theme(self, theme_name):
        """テーマを適用"""
        try:
            # 編集ボタンのテーマスタイルを更新
            self._apply_edit_button_theme()
            
            # テーマに応じたスタイル更新
            if theme_name == "dark":
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
                
        except Exception as e:
            logging.error(f"テーマ適用エラー: {e}")
    
    def _apply_dark_theme(self):
        """ダークテーマを適用"""
        try:
            # ダークテーマのスタイルを適用
            pass
            
        except Exception as e:
            logging.error(f"ダークテーマ適用エラー: {e}")
    
    def _apply_light_theme(self):
        """ライトテーマを適用"""
        try:
            # ライトテーマのスタイルを適用
            pass
            
        except Exception as e:
            logging.error(f"ライトテーマ適用エラー: {e}")
