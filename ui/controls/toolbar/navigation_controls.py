"""
ナビゲーションコントロールモジュール

このモジュールは ui/controls.py から分離された
親フォルダボタンなどのナビゲーション制御機能を提供します。
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon
from presentation.themes.theme_mixin import ThemeAwareMixin
import os
import logging
from typing import Optional


class NavigationControls(QWidget, ThemeAwareMixin):
    """
    ナビゲーションコントロールクラス
    
    親フォルダボタン、ホームボタン、履歴ボタンなどの
    ナビゲーション制御UIを提供
    """
    
    # シグナル
    parent_folder_requested = pyqtSignal()  # 親フォルダ移動要求
    home_folder_requested = pyqtSignal()    # ホームフォルダ移動要求
    back_requested = pyqtSignal()           # 戻る要求
    forward_requested = pyqtSignal()        # 進む要求
    refresh_requested = pyqtSignal()        # 更新要求
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 状態管理
        self.current_path = ""
        self.can_go_back = False
        self.can_go_forward = False
        
        # コンポーネント
        self.parent_button: Optional[QPushButton] = None
        self.home_button: Optional[QPushButton] = None
        self.back_button: Optional[QPushButton] = None
        self.forward_button: Optional[QPushButton] = None
        self.refresh_button: Optional[QPushButton] = None
        self.separator_label: Optional[QLabel] = None
        
        # UI設定
        self.setup_ui()
    
    def setup_ui(self):
        """UI初期化"""
        try:
            # メインレイアウト
            layout = QHBoxLayout(self)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(2)
            
            # 戻る/進むボタン
            self._create_history_buttons(layout)
            
            # セパレーター
            self._create_separator(layout)
            
            # 親フォルダボタン
            self._create_parent_button(layout)
            
            # ホームボタン
            self._create_home_button(layout)
            
            # 更新ボタン
            self._create_refresh_button(layout)
            
            # 右端にスペーサー
            layout.addStretch()
            
        except Exception as e:
            logging.error(f"ナビゲーションコントロールUI初期化エラー: {e}")
    
    def _create_history_buttons(self, layout: QHBoxLayout):
        """履歴ボタン（戻る/進む）を作成"""
        try:
            # 戻るボタン
            self.back_button = QPushButton("◀")
            self.back_button.setFixedSize(32, 30)
            self.back_button.setToolTip("戻る")
            self.back_button.setEnabled(False)
            self.back_button.clicked.connect(self._on_back_clicked)
            
            # 進むボタン
            self.forward_button = QPushButton("▶")
            self.forward_button.setFixedSize(32, 30)
            self.forward_button.setToolTip("進む")
            self.forward_button.setEnabled(False)
            self.forward_button.clicked.connect(self._on_forward_clicked)
            
            # フォント設定
            for button in [self.back_button, self.forward_button]:
                if button:
                    font = QFont()
                    font.setPointSize(10)
                    font.setWeight(QFont.Bold)
                    button.setFont(font)
                    button.setStyleSheet(self._get_history_button_style())
            
            # レイアウトに追加
            if self.back_button:
                layout.addWidget(self.back_button)
            if self.forward_button:
                layout.addWidget(self.forward_button)
            
        except Exception as e:
            logging.error(f"履歴ボタン作成エラー: {e}")
    
    def _create_separator(self, layout: QHBoxLayout):
        """セパレーターを作成"""
        try:
            self.separator_label = QLabel("|")
            self.separator_label.setFixedWidth(10)
            self.separator_label.setAlignment(Qt.AlignCenter)  # type: ignore
            self.separator_label.setStyleSheet("""
                QLabel {
                    color: #c0c0c0;
                    font-weight: bold;
                }
            """)
            
            layout.addWidget(self.separator_label)
            
        except Exception as e:
            logging.error(f"セパレーター作成エラー: {e}")
    
    def _create_parent_button(self, layout: QHBoxLayout):
        """親フォルダボタンを作成"""
        try:
            self.parent_button = QPushButton("⬆")
            self.parent_button.setFixedSize(35, 30)
            self.parent_button.setToolTip("親フォルダに移動")
            self.parent_button.clicked.connect(self._on_parent_clicked)
            
            # フォント設定
            font = QFont()
            font.setPointSize(12)
            font.setWeight(QFont.Bold)
            self.parent_button.setFont(font)
            
            # スタイル
            self.parent_button.setStyleSheet(self._get_navigation_button_style())
            
            layout.addWidget(self.parent_button)
            
        except Exception as e:
            logging.error(f"親フォルダボタン作成エラー: {e}")
    
    def _create_home_button(self, layout: QHBoxLayout):
        """ホームボタンを作成"""
        try:
            self.home_button = QPushButton("🏠")
            self.home_button.setFixedSize(35, 30)
            self.home_button.setToolTip("ホームフォルダに移動")
            self.home_button.clicked.connect(self._on_home_clicked)
            
            # フォント設定
            font = QFont()
            font.setPointSize(11)
            self.home_button.setFont(font)
            
            # スタイル
            self.home_button.setStyleSheet(self._get_navigation_button_style())
            
            layout.addWidget(self.home_button)
            
        except Exception as e:
            logging.error(f"ホームボタン作成エラー: {e}")
    
    def _create_refresh_button(self, layout: QHBoxLayout):
        """更新ボタンを作成"""
        try:
            self.refresh_button = QPushButton("🔄")
            self.refresh_button.setFixedSize(35, 30)
            self.refresh_button.setToolTip("現在のフォルダを更新")
            self.refresh_button.clicked.connect(self._on_refresh_clicked)
            
            # フォント設定
            font = QFont()
            font.setPointSize(10)
            self.refresh_button.setFont(font)
            
            # スタイル
            self.refresh_button.setStyleSheet(self._get_navigation_button_style())
            
            layout.addWidget(self.refresh_button)
            
        except Exception as e:
            logging.error(f"更新ボタン作成エラー: {e}")
    
    def _get_history_button_style(self) -> str:
        """履歴ボタンのスタイル"""
        return """
            QPushButton {
                background-color: #f8f8f8;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                font-weight: bold;
                color: #333;
            }
            QPushButton:hover:enabled {
                background-color: #e8e8e8;
                border-color: #b0b0b0;
            }
            QPushButton:pressed:enabled {
                background-color: #d8d8d8;
            }
            QPushButton:disabled {
                background-color: #f0f0f0;
                border-color: #e0e0e0;
                color: #a0a0a0;
            }
        """
    
    def _get_navigation_button_style(self) -> str:
        """ナビゲーションボタンのスタイル"""
        return """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #b0b0b0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
            QPushButton:disabled {
                background-color: #f8f8f8;
                border-color: #e0e0e0;
                color: #a0a0a0;
            }
        """
    
    def _on_back_clicked(self):
        """戻るボタンクリック時の処理"""
        try:
            self.back_requested.emit()
            
        except Exception as e:
            logging.error(f"戻るボタン処理エラー: {e}")
    
    def _on_forward_clicked(self):
        """進むボタンクリック時の処理"""
        try:
            self.forward_requested.emit()
            
        except Exception as e:
            logging.error(f"進むボタン処理エラー: {e}")
    
    def _on_parent_clicked(self):
        """親フォルダボタンクリック時の処理"""
        try:
            self.parent_folder_requested.emit()
            
        except Exception as e:
            logging.error(f"親フォルダボタン処理エラー: {e}")
    
    def _on_home_clicked(self):
        """ホームボタンクリック時の処理"""
        try:
            self.home_folder_requested.emit()
            
        except Exception as e:
            logging.error(f"ホームボタン処理エラー: {e}")
    
    def _on_refresh_clicked(self):
        """更新ボタンクリック時の処理"""
        try:
            self.refresh_requested.emit()
            
        except Exception as e:
            logging.error(f"更新ボタン処理エラー: {e}")
    
    def set_current_path(self, path: str):
        """現在のパスを設定"""
        try:
            self.current_path = path
            self._update_button_states()
            
        except Exception as e:
            logging.error(f"現在パス設定エラー: {e}")
    
    def _update_button_states(self):
        """ボタンの有効/無効状態を更新"""
        try:
            # 親フォルダボタンの状態
            has_parent = self._has_parent_folder()
            if self.parent_button:
                self.parent_button.setEnabled(has_parent)
            
        except Exception as e:
            logging.error(f"ボタン状態更新エラー: {e}")
    
    def _has_parent_folder(self) -> bool:
        """親フォルダが存在するかチェック"""
        try:
            if not self.current_path:
                return False
            
            parent = os.path.dirname(self.current_path)
            return parent != self.current_path and os.path.exists(parent)
            
        except Exception as e:
            logging.error(f"親フォルダ存在チェックエラー: {e}")
            return False
    
    def set_history_state(self, can_back: bool, can_forward: bool):
        """履歴ボタンの状態を設定"""
        try:
            self.can_go_back = can_back
            self.can_go_forward = can_forward
            
            if self.back_button:
                self.back_button.setEnabled(can_back)
            if self.forward_button:
                self.forward_button.setEnabled(can_forward)
            
        except Exception as e:
            logging.error(f"履歴状態設定エラー: {e}")
    
    def apply_theme(self, theme_name: str):
        """テーマを適用"""
        try:
            if theme_name == "dark":
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
                
        except Exception as e:
            logging.error(f"テーマ適用エラー: {e}")
    
    def _apply_dark_theme(self):
        """ダークテーマを適用"""
        try:
            dark_style = """
                QPushButton {
                    background-color: #3c3c3c;
                    border: 1px solid #555;
                    border-radius: 4px;
                    color: #fff;
                }
                QPushButton:hover:enabled {
                    background-color: #505050;
                    border-color: #777;
                }
                QPushButton:pressed:enabled {
                    background-color: #2a2a2a;
                }
                QPushButton:disabled {
                    background-color: #2a2a2a;
                    border-color: #444;
                    color: #666;
                }
            """
            
            # 全ボタンに適用
            for button in [self.parent_button, self.home_button, self.refresh_button, 
                          self.back_button, self.forward_button]:
                if button:
                    button.setStyleSheet(dark_style)
            
            # セパレーター
            if self.separator_label:
                self.separator_label.setStyleSheet("""
                    QLabel {
                        color: #666;
                        font-weight: bold;
                    }
                """)
            
        except Exception as e:
            logging.error(f"ダークテーマ適用エラー: {e}")
    
    def _apply_light_theme(self):
        """ライトテーマを適用"""
        try:
            # 元のスタイルに戻す
            if self.parent_button:
                self.parent_button.setStyleSheet(self._get_navigation_button_style())
            if self.home_button:
                self.home_button.setStyleSheet(self._get_navigation_button_style())
            if self.refresh_button:
                self.refresh_button.setStyleSheet(self._get_navigation_button_style())
            
            for button in [self.back_button, self.forward_button]:
                if button:
                    button.setStyleSheet(self._get_history_button_style())
            
            # セパレーター
            if self.separator_label:
                self.separator_label.setStyleSheet("""
                    QLabel {
                        color: #c0c0c0;
                        font-weight: bold;
                    }
                """)
            
        except Exception as e:
            logging.error(f"ライトテーマ適用エラー: {e}")
