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
            
            # 初期表示状態設定
            if self.breadcrumb_widget:
                self.breadcrumb_widget.setVisible(True)  # ブレッドクラムを表示
                # テーマに適応したスタイルを適用
                self.breadcrumb_widget.setStyleSheet("""
                    QWidget {
                        background-color: #2d3748;
                        border: 1px solid #4a5568;
                        border-radius: 3px;
                        min-height: 30px;
                        padding: 2px;
                    }
                """)
            if self.text_edit:
                self.text_edit.setVisible(False)  # テキスト編集は非表示
            
            # 編集ボタンを強制表示
            if self.edit_button:
                self.edit_button.setVisible(True)
                self.edit_button.show()
                debug(f"🔧 🔧 🔧 編集ボタン強制表示: visible={self.edit_button.isVisible()}, size={self.edit_button.size()}")
            
            # 初期パスは設定しない - メインウィンドウからの設定を待つ
            # （重複処理を避けるため、refactored_main_window.pyがassetsフォルダを設定する）
            debug(f"🔧 🔧 🔧 初期パス設定をスキップ - メインウィンドウからの設定を待機")
            
            # ブレッドクラムウィジェットの最小サイズ設定（0幅にならないように）
            if self.breadcrumb_widget:
                self.breadcrumb_widget.setMinimumWidth(350)  # 幅を拡大してボタンが見切れないように
                debug(f"🔧 🔧 🔧 ブレッドクラム最小幅設定: size={self.breadcrumb_widget.size()}")
            
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
            debug(f"🔧 🔧 🔧 _create_breadcrumb_widget開始")
            
            # 重要: 親ウィジェット(self)を明示的に指定
            self.breadcrumb_widget = QWidget(self)
            debug(f"🔧 🔧 🔧 QWidget作成成功(parent={self}): {self.breadcrumb_widget}")
            
            self.breadcrumb_widget.setMaximumHeight(34)
            self.breadcrumb_widget.setMinimumHeight(30)
            debug(f"🔧 🔧 🔧 breadcrumb_widget高さ設定完了")
            
            self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_widget)
            debug(f"🔧 🔧 🔧 QHBoxLayout作成成功: {self.breadcrumb_layout}")
            
            self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)
            self.breadcrumb_layout.setSpacing(1)
            debug(f"🔧 🔧 🔧 レイアウト設定完了")
            
            debug(f"🔧 🔧 🔧 _create_breadcrumb_widget成功完了")
            
        except Exception as e:
            logging.error(f"ブレッドクラムウィジェット作成エラー: {e}")
            debug(f"🔧 🔧 🔧 _create_breadcrumb_widget例外: {e}")
            raise e
    
    def _recreate_breadcrumb_widget(self):
        """ブレッドクラムウィジェットを再作成"""
        try:
            debug(f"🔧 🔧 🔧 ブレッドクラムウィジェット再作成開始")
            
            # 古いウィジェットとレイアウトを完全にクリーンアップ
            if hasattr(self, 'breadcrumb_widget') and self.breadcrumb_widget:
                try:
                    # まず、レイアウトから削除
                    if self.main_layout:
                        for i in range(self.main_layout.count()):
                            item = self.main_layout.itemAt(i)
                            if item and item.widget() == self.breadcrumb_widget:
                                self.main_layout.removeWidget(self.breadcrumb_widget)
                                break
                    
                    # ウィジェットの親を削除（deleteLater()は使用しない）
                    self.breadcrumb_widget.setParent(None)
                    debug(f"🔧 🔧 🔧 古いbreadcrumb_widget削除完了")
                except Exception as e:
                    debug(f"🔧 🔧 🔧 古いbreadcrumb_widget削除エラー: {e}")
            
            # breadcrumb_layoutの参照をクリア
            self.breadcrumb_layout = None
            self.breadcrumb_widget = None
            
            # 新しいウィジェットを作成
            debug(f"🔧 🔧 🔧 新しいbreadcrumb_widget作成開始")
            self._create_breadcrumb_widget()
            
            # 作成結果の詳細確認
            widget_created = self.breadcrumb_widget is not None
            layout_created = self.breadcrumb_layout is not None
            debug(f"🔧 🔧 🔧 作成結果: widget={widget_created}, layout={layout_created}")
            debug(f"🔧 🔧 🔧 作成されたwidget: {self.breadcrumb_widget}")
            debug(f"🔧 🔧 🔧 作成されたlayout: {self.breadcrumb_layout}")
            
            # PyQt C++オブジェクトの有効性も確認
            widget_valid = False
            layout_valid = False
            
            if widget_created and self.breadcrumb_widget:
                try:
                    # C++オブジェクトが有効かテスト
                    _ = self.breadcrumb_widget.isVisible()
                    widget_valid = True
                    debug(f"🔧 🔧 🔧 breadcrumb_widget C++オブジェクト有効")
                except Exception as e:
                    debug(f"🔧 🔧 🔧 breadcrumb_widget C++オブジェクト無効: {e}")
            
            if layout_created and self.breadcrumb_layout:
                try:
                    # C++オブジェクトが有効かテスト - 直接メソッド呼び出し
                    test_count = self.breadcrumb_layout.count()
                    layout_valid = True
                    debug(f"🔧 🔧 🔧 breadcrumb_layout C++オブジェクト有効 (count={test_count})")
                except RuntimeError as e:
                    debug(f"🔧 🔧 🔧 breadcrumb_layout C++オブジェクト削除済み: {e}")
                except Exception as e:
                    debug(f"🔧 🔧 🔧 breadcrumb_layout C++オブジェクト無効: {e}")
            
            if not widget_valid or not layout_valid:
                error(f"🔧 🔧 🔧 新しいbreadcrumb_widget作成失敗: widget_valid={widget_valid}, layout_valid={layout_valid}")
                return False
            
            # ウィジェットの基本設定
            if self.breadcrumb_widget:
                self.breadcrumb_widget.setVisible(True)
                self.breadcrumb_widget.setMinimumWidth(350)  # 同じ幅に統一
            
            # メインレイアウトに適切な位置に追加
            if self.main_layout and self.breadcrumb_widget:
                # ブレッドクラムを最初の位置（インデックス0）に挿入
                self.main_layout.insertWidget(0, self.breadcrumb_widget, 1)
                debug(f"🔧 🔧 🔧 新しいbreadcrumb_widgetをレイアウトに追加完了")
            
            # 表示状態確認
            if self.breadcrumb_widget and self.breadcrumb_layout:
                debug(f"🔧 🔧 🔧 再作成後のbreadcrumb_widget: visible={self.breadcrumb_widget.isVisible()}, size={self.breadcrumb_widget.size()}")
                debug(f"🔧 🔧 🔧 再作成後のbreadcrumb_layout: count={self.breadcrumb_layout.count()}")
            
            return True
            
        except Exception as e:
            logging.error(f"ブレッドクラムウィジェット再作成エラー: {e}")
            debug(f"🔧 🔧 🔧 ブレッドクラムウィジェット再作成失敗: {e}")
            return False
    
    def _create_text_edit(self):
        """テキスト入力フィールドを作成"""
        try:
            # 重要: 親ウィジェット(self)を明示的に指定
            self.text_edit = QLineEdit(self)
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
            # 重要: 親ウィジェット(self)を明示的に指定
            self.edit_button = QPushButton("📝", self)
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
            debug(f"🔧 🔧 🔧 setText呼び出し: path='{path}', is_edit_mode={self.is_edit_mode}")
            self.current_path = path
            if self.is_edit_mode:
                if self.text_edit:
                    self.text_edit.setText(path)
            else:
                debug(f"🔧 🔧 🔧 ブレッドクラム更新開始: path='{path}'")
                self._update_breadcrumb(path)
                debug(f"🔧 🔧 🔧 ブレッドクラム更新完了")
                
        except Exception as e:
            logging.error(f"パス設定エラー: {e}")
    
    def text(self):
        """現在のパスを取得"""
        return self.current_path
    
    def _update_breadcrumb(self, path):
        """ブレッドクラム表示を更新"""
        try:
            debug(f"🔧 🔧 🔧 _update_breadcrumb開始: path='{path}', breadcrumb_layout={self.breadcrumb_layout}")
            debug(f"🔧 🔧 🔧 breadcrumb_layout型: {type(self.breadcrumb_layout)}")
            debug(f"🔧 🔧 🔧 breadcrumb_layout is None: {self.breadcrumb_layout is None}")
            
            # 最も安全なチェック方法
            layout_valid = False
            try:
                if hasattr(self, 'breadcrumb_layout') and self.breadcrumb_layout is not None:
                    # C++オブジェクトが有効かテスト
                    try:
                        test_count = self.breadcrumb_layout.count()
                        layout_valid = True
                        debug(f"🔧 🔧 🔧 breadcrumb_layout有効性チェック: 有効 (count={test_count})")
                    except RuntimeError as runtime_error:
                        debug(f"⚠️ breadcrumb_layout RuntimeError: {runtime_error}")
                        layout_valid = False
                    except Exception as layout_error:
                        debug(f"⚠️ breadcrumb_layout例外: {layout_error}")
                        layout_valid = False
                else:
                    debug(f"🔧 🔧 🔧 breadcrumb_layout属性なしまたはNone")
                    layout_valid = False
            except Exception as check_error:
                debug(f"⚠️ breadcrumb_layout存在チェックエラー: {check_error}")
                layout_valid = False
            
            if not layout_valid:
                debug(f"⚠️ breadcrumb_layoutが無効 - パス更新をスキップ")
                return
            
            # 既存のボタンを安全にクリア
            debug(f"🔧 🔧 🔧 既存ボタンクリア開始")
            try:
                self._safe_clear_breadcrumb_buttons()
            except Exception as clear_error:
                debug(f"⚠️ ボタンクリア中にエラー: {clear_error}")
                return
            debug(f"🔧 🔧 🔧 既存ボタンクリア完了")
            
            # 新しいボタンを作成
            debug(f"🔧 🔧 🔧 ブレッドクラムボタン作成開始")
            try:
                self._create_breadcrumb_buttons(path)
            except Exception as create_error:
                debug(f"⚠️ ボタン作成中にエラー: {create_error}")
                return
            debug(f"🔧 🔧 🔧 ブレッドクラムボタン作成完了")
            
            # デバッグ情報表示
            try:
                final_count = self.breadcrumb_layout.count()
                debug(f"🔧 🔧 🔧 最終的なボタン数: {final_count}")
                for i in range(final_count):
                    item = self.breadcrumb_layout.itemAt(i)
                    if item and item.widget():
                        button = item.widget()
                        debug(f"🔧 🔧 🔧 ボタン[{i}]: text='{button.text()}', visible={button.isVisible()}")
            except Exception as debug_error:
                debug(f"⚠️ デバッグ情報表示エラー: {debug_error}")
            
            debug(f"🔧 🔧 🔧 ブレッドクラム更新完了")
            
        except Exception as e:
            debug(f"⚠️ ブレッドクラム更新中にエラー: {e}")
            import traceback
            debug(f"⚠️ トレースバック: {traceback.format_exc()}")
    
    def _safe_clear_breadcrumb_buttons(self):
        """ブレッドクラムボタンを安全にクリア"""
        try:
            if not hasattr(self, 'breadcrumb_layout') or not self.breadcrumb_layout:
                return
                
            # 削除対象のウィジェットを事前に収集
            widgets_to_remove = []
            try:
                for i in range(self.breadcrumb_layout.count()):
                    item = self.breadcrumb_layout.itemAt(i)
                    if item and item.widget():
                        widgets_to_remove.append(item.widget())
            except Exception as collection_error:
                debug(f"⚠️ ウィジェット収集エラー: {collection_error}")
                return
            
            # レイアウトから安全に削除
            try:
                while self.breadcrumb_layout.count() > 0:
                    item = self.breadcrumb_layout.takeAt(0)
                    # アイテムはtakeAt()で自動的に管理される
            except Exception as layout_error:
                debug(f"⚠️ レイアウトクリアエラー: {layout_error}")
            
            # ウィジェットを安全に削除
            for widget in widgets_to_remove:
                try:
                    if widget:
                        widget.hide()
                        widget.setParent(None)
                except Exception as widget_error:
                    debug(f"⚠️ 個別ウィジェット削除エラー（無視）: {widget_error}")
            
        except Exception as e:
            debug(f"⚠️ ブレッドクラムボタンクリア中にエラー: {e}")
    
    def _clear_breadcrumb_buttons(self):
        """既存のブレッドクラムボタンをクリア - 後方互換性のため残存"""
        return self._safe_clear_breadcrumb_buttons()
    
    def _create_breadcrumb_buttons(self, path):
        """パスからブレッドクラムボタンを作成"""
        try:
            debug(f"🔧 🔧 🔧 _create_breadcrumb_buttons開始: path='{path}'")
            # パスを正規化
            path = os.path.normpath(path)
            debug(f"🔧 🔧 🔧 パス正規化後: '{path}'")
            parts = self._split_path(path)
            debug(f"🔧 🔧 🔧 パス分割結果: {parts}")
            
            # ボタンを作成
            all_buttons = []
            current_path = ""
            
            for i, part in enumerate(parts):
                debug(f"🔧 🔧 🔧 パス要素[{i}]: '{part}'")
                if not part and i != 0:  # 空の部分をスキップ（ルート以外）
                    debug(f"🔧 🔧 🔧 空のパス要素をスキップ: index={i}")
                    continue
                
                # パス構築
                current_path = self._build_current_path(current_path, part, i)
                debug(f"🔧 🔧 🔧 構築されたパス[{i}]: '{current_path}'")
                
                # ボタン作成
                button = self._create_path_button(part, current_path)
                if button:
                    debug(f"🔧 🔧 🔧 ボタン作成成功[{i}]: text='{button.text()}', path='{current_path}'")
                    all_buttons.append(button)
                else:
                    warning(f"🔧 🔧 🔧 ボタン作成失敗[{i}]: part='{part}', path='{current_path}'")
            
            debug(f"🔧 🔧 🔧 作成されたボタン数: {len(all_buttons)}")
            
            # ボタンレイアウト
            debug(f"🔧 🔧 🔧 ボタンレイアウト開始")
            self._layout_buttons_with_priority(all_buttons)
            debug(f"🔧 🔧 🔧 ボタンレイアウト完了")
            
        except Exception as e:
            logging.error(f"ブレッドクラムボタン作成エラー: {e}")
            debug(f"🔧 🔧 🔧 _create_breadcrumb_buttons例外: {e}")
    
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
            debug(f"🔧 🔧 🔧 _create_path_button開始: part='{part}', path='{path}'")
            # 重要: 親ウィジェット(self.breadcrumb_widget)を明示的に指定
            button = QPushButton(part if part else '/', self.breadcrumb_widget)
            button.setProperty('path', path)
            button.clicked.connect(lambda checked, p=path: self._on_button_clicked(p))
            
            # フォント設定
            font = QFont()
            font.setPointSize(10)
            font.setWeight(QFont.Medium)
            button.setFont(font)
            
            # スタイル設定
            button.setStyleSheet(self._get_button_style())
            
            # 表示設定を追加
            button.setVisible(True)
            button.show()
            
            debug(f"🔧 🔧 🔧 ボタン作成成功: text='{button.text()}', size={button.size()}")
            return button
            
        except Exception as e:
            logging.error(f"パスボタン作成エラー: {e}")
            debug(f"🔧 🔧 🔧 _create_path_button例外: {e}")
            return None
    
    def _layout_buttons_with_priority(self, all_buttons):
        """カレント側を優先してボタンを配置"""
        try:
            debug(f"🔧 🔧 🔧 _layout_buttons_with_priority開始: ボタン数={len(all_buttons)}")
            if not all_buttons or not self.breadcrumb_widget:
                warning(f"🔧 🔧 🔧 ボタンまたはウィジェットなし: buttons={len(all_buttons) if all_buttons else 0}, widget={bool(self.breadcrumb_widget)}")
                return
            
            # 利用可能な幅を計算
            available_width = self.breadcrumb_widget.width() - 30  # マージンを拡大
            debug(f"🔧 🔧 🔧 利用可能幅計算: widget_width={self.breadcrumb_widget.width()}, available_width={available_width}")
            if available_width <= 0:
                available_width = 300  # より広いデフォルト値
                debug(f"🔧 🔧 🔧 幅不足のためデフォルト値使用: {available_width}")
            
            # ボタン幅を計算
            total_width = sum(self._estimate_button_width(btn) for btn in all_buttons)
            debug(f"🔧 🔧 🔧 総ボタン幅: {total_width}, 利用可能幅: {available_width}")
            
            # 全てのボタンが収まる場合
            if total_width <= available_width:
                debug(f"🔧 🔧 🔧 全ボタン表示可能 - 通常レイアウト実行")
                debug(f"🔧 🔧 🔧 self.breadcrumb_layoutチェック: {self.breadcrumb_layout}, None={self.breadcrumb_layout is None}, bool={bool(self.breadcrumb_layout) if hasattr(self, 'breadcrumb_layout') else 'NoAttr'}")
                
                if hasattr(self, 'breadcrumb_layout') and self.breadcrumb_layout is not None:
                    for i, button in enumerate(all_buttons):
                        button.setVisible(True)  # ボタンを明示的に表示
                        button.show()  # 追加の表示設定
                        self.breadcrumb_layout.addWidget(button)
                        debug(f"🔧 🔧 🔧 ボタン追加[{i}]: text='{button.text()}', visible={button.isVisible()}")
                    
                    self.breadcrumb_layout.addStretch()
                    debug(f"🔧 🔧 🔧 ストレッチ追加完了")
                    
                    # 通常レイアウトでも最終状態を確認
                    debug(f"🔧 🔧 🔧 通常レイアウト アイテム数: {self.breadcrumb_layout.count()}")
                    for i in range(self.breadcrumb_layout.count()):
                        item = self.breadcrumb_layout.itemAt(i)
                        if item and item.widget():
                            widget = item.widget()
                            debug(f"🔧 🔧 🔧 通常レイアウト[{i}]: {widget}, text='{getattr(widget, 'text', lambda: 'N/A')()}', visible={getattr(widget, 'isVisible', lambda: False)()}")
                else:
                    debug(f"🔧 🔧 🔧 breadcrumb_layoutが無効（通常レイアウト）: hasattr={hasattr(self, 'breadcrumb_layout')}, is_none={self.breadcrumb_layout is None if hasattr(self, 'breadcrumb_layout') else 'NoAttr'}")
                return
            
            # 幅が足りない場合の処理
            debug(f"🔧 🔧 🔧 🔧 幅不足 - 省略記号レイアウト実行開始")
            debug(f"🔧 🔧 🔧 🔧 breadcrumb_layoutチェック: {self.breadcrumb_layout}, None={self.breadcrumb_layout is None}")
            debug(f"🔧 🔧 🔧 🔧 breadcrumb_layout型: {type(self.breadcrumb_layout)}")
            debug(f"🔧 🔧 🔧 🔧 hasattr(self, 'breadcrumb_layout'): {hasattr(self, 'breadcrumb_layout')}")
            debug(f"🔧 🔧 🔧 🔧 bool(self.breadcrumb_layout): {bool(self.breadcrumb_layout) if hasattr(self, 'breadcrumb_layout') else 'No attr'}")
            
            if hasattr(self, 'breadcrumb_layout') and self.breadcrumb_layout is not None:
                debug(f"🔧 🔧 🔧 🔧 省略記号レイアウト実行開始 - レイアウト有効")
                self._layout_with_ellipsis(all_buttons, available_width, self.breadcrumb_layout)
                debug(f"🔧 🔧 🔧 🔧 省略記号レイアウト実行完了")
            else:
                debug(f"🔧 🔧 🔧 🔧 breadcrumb_layoutがない/Noneのため省略記号レイアウトをスキップ")
            
        except Exception as e:
            logging.error(f"ボタンレイアウトエラー: {e}")
            debug(f"🔧 🔧 🔧 _layout_buttons_with_priority例外: {e}")
    
    def _estimate_button_width(self, button):
        """ボタン幅を推定"""
        try:
            text = button.text()
            return len(text) * 8 + 24 + 2  # 文字幅 + パディング + マージン
            
        except Exception as e:
            logging.error(f"ボタン幅推定エラー: {e}")
            return 50  # デフォルト幅
    
    def _layout_with_ellipsis(self, all_buttons, available_width, breadcrumb_layout):
        """省略記号を使用してボタンを配置"""
        try:
            debug(f"🔧 🔧 🔧 🔧 🔧 _layout_with_ellipsis開始: ボタン数={len(all_buttons)}, 利用可能幅={available_width}")
            debug(f"🔧 🔧 🔧 🔧 🔧 受け取ったbreadcrumb_layout: {breadcrumb_layout}")
            debug(f"🔧 🔧 🔧 🔧 🔧 breadcrumb_layout型: {type(breadcrumb_layout)}")
            debug(f"🔧 🔧 🔧 🔧 🔧 breadcrumb_layout is None: {breadcrumb_layout is None}")
            debug(f"🔧 🔧 🔧 🔧 🔧 bool(breadcrumb_layout): {bool(breadcrumb_layout)}")
            
            if breadcrumb_layout is None:
                debug(f"🔧 🔧 🔧 🔧 🔧 breadcrumb_layoutがNoneです")
                return
                
            # PyQtオブジェクトの有効性をチェック
            try:
                # レイアウトが有効かどうかをアイテム数をチェックして確認
                item_count = breadcrumb_layout.count()
                debug(f"🔧 🔧 🔧 🔧 🔧 breadcrumb_layout有効性確認: count={item_count}")
            except Exception as e:
                debug(f"🔧 🔧 🔧 🔧 🔧 breadcrumb_layout無効: {e}")
                return
            
            debug(f"🔧 🔧 🔧 🔧 🔧 breadcrumb_layout確認完了: {breadcrumb_layout}")
                
            ellipsis_width = 30
            used_width = 0
            visible_buttons = []
            
            debug(f"🔧 🔧 🔧 🔧 🔧 省略記号計算開始: ellipsis_width={ellipsis_width}")
            
            # 後ろから順に追加
            for i in reversed(range(len(all_buttons))):
                button = all_buttons[i]
                button_width = self._estimate_button_width(button)
                debug(f"🔧 🔧 🔧 🔧 🔧 ボタン[{i}]幅計算: text='{button.text()}', width={button_width}")
                
                needed_width = used_width + button_width
                if len(visible_buttons) > 0:  # 省略記号が必要
                    needed_width += ellipsis_width
                
                debug(f"🔧 🔧 🔧 🔧 🔧 幅チェック[{i}]: needed={needed_width}, available={available_width}")
                
                if needed_width <= available_width:
                    visible_buttons.insert(0, button)
                    used_width += button_width
                    debug(f"🔧 🔧 🔧 🔧 🔧 ボタン[{i}]追加: text='{button.text()}', used_width={used_width}")
                else:
                    debug(f"🔧 🔧 🔧 🔧 🔧 ボタン[{i}]スキップ（幅不足）: text='{button.text()}'")
                    break
            
            debug(f"🔧 🔧 🔧 🔧 🔧 表示ボタン決定完了: {len(visible_buttons)}/{len(all_buttons)}個表示")
            
            # 省略記号を追加（必要な場合）
            if len(visible_buttons) < len(all_buttons):
                debug(f"🔧 🔧 🔧 🔧 🔧 省略記号ボタン作成開始")
                # 重要: 親ウィジェット(self.breadcrumb_widget)を明示的に指定
                ellipsis_btn = QPushButton("...", self.breadcrumb_widget)
                ellipsis_btn.setFixedSize(ellipsis_width, 30)
                ellipsis_btn.setToolTip("省略されたパス要素")
                ellipsis_btn.setStyleSheet(self._get_button_style())  # スタイル適用
                ellipsis_btn.setVisible(True)  # 省略記号ボタンを明示的に表示
                ellipsis_btn.show()  # 追加の表示設定

                breadcrumb_layout.addWidget(ellipsis_btn)
                debug(f"🔧 🔧 🔧 🔧 🔧 省略記号ボタン追加完了: visible={ellipsis_btn.isVisible()}")
            else:
                debug(f"🔧 🔧 🔧 🔧 🔧 省略記号不要（全ボタン表示可能）")
            
            # 表示するボタンを追加
            for i, button in enumerate(visible_buttons):
                button.setVisible(True)  # ボタンを明示的に表示
                button.show()  # 追加の表示設定
                breadcrumb_layout.addWidget(button)
                debug(f"🔧 🔧 🔧 🔧 省略レイアウト - ボタン追加[{i}]: text='{button.text()}', visible={button.isVisible()}")
            
            # 右端にスペーサー
            breadcrumb_layout.addStretch()
            debug(f"🔧 🔧 🔧 🔧 省略レイアウト完了 - 表示ボタン数: {len(visible_buttons)}/{len(all_buttons)}")
            
            # 最終的なレイアウト状態を確認
            if breadcrumb_layout:
                debug(f"🔧 🔧 🔧 🔧 breadcrumb_layout アイテム数: {breadcrumb_layout.count()}")
                for i in range(breadcrumb_layout.count()):
                    item = breadcrumb_layout.itemAt(i)
                    if item and item.widget():
                        widget = item.widget()
                        debug(f"🔧 🔧 🔧 🔧 レイアウト[{i}]: {widget}, text='{getattr(widget, 'text', lambda: 'N/A')()}', visible={getattr(widget, 'isVisible', lambda: False)()}")
            
            # ブレッドクラムウィジェット自体の状態確認
            if self.breadcrumb_widget:
                debug(f"🔧 🔧 🔧 🔧 breadcrumb_widget: visible={self.breadcrumb_widget.isVisible()}, size={self.breadcrumb_widget.size()}")
                debug(f"🔧 🔧 🔧 🔧 breadcrumb_widget 親: {self.breadcrumb_widget.parent()}")
            
        except Exception as e:
            logging.error(f"省略記号レイアウトエラー: {e}")
    
    def _force_create_breadcrumb_buttons(self, path):
        """PyQtオブジェクト問題を回避してブレッドクラムボタンを強制作成"""
        try:
            debug(f"🔧 🔧 🔧 🔧 🔧 強制ブレッドクラムボタン作成開始: path='{path}'")
            debug(f"🔧 🔧 🔧 🔧 🔧 hasattr(self, 'main_layout'): {hasattr(self, 'main_layout')}")
            if hasattr(self, 'main_layout'):
                debug(f"🔧 🔧 🔧 🔧 🔧 self.main_layout: {self.main_layout}")
                debug(f"🔧 🔧 🔧 🔧 🔧 self.main_layout is not None: {self.main_layout is not None}")
            
            # main_layoutの有効性チェック
            if not hasattr(self, 'main_layout') or not self.main_layout:
                debug(f"🔧 🔧 🔧 🔧 🔧 main_layoutが存在しないため強制作成をスキップ")
                return
            
            # 既存のブレッドクラムウィジェットを完全に破棄して新規作成
            debug(f"🔧 🔧 🔧 🔧 main_layoutが存在: count={self.main_layout.count()}")
            
            # レイアウトから古いブレッドクラムウィジェットを削除
            removed_count = 0
            widgets_to_remove = []
            
            # 削除対象のウィジェットを安全に特定
            for i in range(self.main_layout.count()):
                item = self.main_layout.itemAt(i)
                if item and item.widget():
                    widget = item.widget()
                    if widget == self.breadcrumb_widget:
                        widgets_to_remove.append(widget)
                        debug(f"🔧 🔧 🔧 🔧 削除対象ウィジェット特定: {widget}")
            
            # 安全にウィジェットを削除
            for widget in widgets_to_remove:
                try:
                    debug(f"🔧 🔧 🔧 🔧 ウィジェット削除開始: {widget}")
                    self.main_layout.removeWidget(widget)
                    widget.setParent(None)
                    # deleteLater()を使わず、即座に削除せずに参照をクリア
                    removed_count += 1
                    debug(f"🔧 🔧 🔧 🔧 ウィジェット削除完了: {widget}")
                except Exception as e:
                    debug(f"🔧 🔧 🔧 🔧 ウィジェット削除エラー: {e}")
            
            debug(f"🔧 🔧 🔧 🔧 削除されたウィジェット数: {removed_count}")
            
            # 新しいブレッドクラムウィジェットを作成
            new_breadcrumb = QWidget()
            new_breadcrumb.setObjectName('breadcrumb_widget_forced')
            new_breadcrumb.setMaximumHeight(34)
            new_breadcrumb.setMinimumHeight(30)
            new_breadcrumb.setMinimumWidth(200)
            debug(f"🔧 🔧 🔧 🔧 新しいブレッドクラムウィジェット作成: {new_breadcrumb}")
            
            # スタイル設定
            new_breadcrumb.setStyleSheet("""
                QWidget {
                    background-color: #2d3748;
                    border: 1px solid #4a5568;
                    border-radius: 3px;
                    min-height: 30px;
                    padding: 2px;
                }
            """)
            debug(f"🔧 🔧 🔧 🔧 スタイル設定完了")
            
            # 新しいレイアウトを作成
            new_layout = QHBoxLayout(new_breadcrumb)
            new_layout.setContentsMargins(0, 0, 0, 0)
            new_layout.setSpacing(1)
            debug(f"🔧 🔧 🔧 🔧 新しいレイアウト作成: {new_layout}")
            
            # パスからボタンを作成
            parts = self._split_path(path)
            current_path = ""
            debug(f"🔧 🔧 🔧 🔧 パス分割結果: {parts}")
            
            button_count = 0
            for i, part in enumerate(parts):
                if not part and i != 0:  # 空の部分をスキップ（ルート以外）
                    continue
                
                # パス構築
                current_path = self._build_current_path(current_path, part, i)
                debug(f"🔧 🔧 🔧 🔧 ボタン[{i}]作成: part='{part}', path='{current_path}'")
                
                # ボタン作成
                button = QPushButton(part if part else '/')
                button.setProperty('path', current_path)
                button.clicked.connect(lambda checked, p=current_path: self._on_button_clicked(p))
                button.setStyleSheet(self._get_button_style())
                
                # フォント設定
                font = QFont()
                font.setPointSize(10)
                font.setWeight(QFont.Medium)
                button.setFont(font)
                
                new_layout.addWidget(button)
                button_count += 1
                debug(f"🔧 🔧 🔧 🔧 ボタン[{i}]追加完了: text='{button.text()}'")
            
            # 右端にスペーサー
            new_layout.addStretch()
            debug(f"🔧 🔧 🔧 🔧 ストレッチ追加完了, 合計ボタン数: {button_count}")
            
            # メインレイアウトに追加（最初の位置）
            self.main_layout.insertWidget(0, new_breadcrumb, 1)
            debug(f"🔧 🔧 🔧 🔧 メインレイアウトに追加完了: position=0, stretch=1")
            
            # 参照を更新
            self.breadcrumb_widget = new_breadcrumb
            self.breadcrumb_layout = new_layout
            debug(f"🔧 🔧 🔧 🔧 参照更新完了: widget={self.breadcrumb_widget}, layout={self.breadcrumb_layout}")
            
            # ブレッドクラムウィジェットを強制表示
            new_breadcrumb.setVisible(True)
            new_breadcrumb.show()
            debug(f"🔧 🔧 🔧 🔧 強制表示設定完了: setVisible=True, show()実行")
            
            # 最終確認
            debug(f"🔧 🔧 🔧 🔧 強制ブレッドクラムボタン作成成功: パス='{path}', ボタン数={button_count}")
            debug(f"🔧 🔧 🔧 🔧 強制作成後のブレッドクラム状態: visible={new_breadcrumb.isVisible()}, size={new_breadcrumb.size()}")
            debug(f"🔧 🔧 🔧 🔧 レイアウト最終状態: count={self.main_layout.count()}")
            
        except Exception as e:
            logging.error(f"強制ブレッドクラムボタン作成エラー: {e}")
            debug(f"🔧 🔧 🔧 🔧 強制ブレッドクラムボタン作成失敗: {e}")
            raise e
    
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
                background-color: #4a5568;
                border: 1px solid #718096;
                border-radius: 3px;
                padding: 2px 8px;
                margin: 1px;
                font-weight: 500;
                color: #ffffff;
            }
            QPushButton:hover {
                background-color: #5a6470;
                border-color: #00adb5;
            }
            QPushButton:pressed {
                background-color: #2d3748;
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
