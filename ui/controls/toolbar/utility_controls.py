"""
ユーティリティコントロールモジュール

このモジュールは ui/controls.py から分離された
その他のユーティリティボタンや制御機能を提供します。
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon, QCursor
from presentation.themes.theme_mixin import ThemeAwareMixin
import logging
from typing import Optional, List


class UtilityControls(QWidget, ThemeAwareMixin):
    """
    ユーティリティコントロールクラス
    
    設定、表示オプション、ヘルプなどの
    ユーティリティ機能UIを提供
    """
    
    # シグナル
    view_mode_changed = pyqtSignal(str)     # 表示モード変更
    settings_requested = pyqtSignal()       # 設定画面要求
    help_requested = pyqtSignal()           # ヘルプ表示要求
    theme_changed = pyqtSignal(str)         # テーマ変更
    layout_changed = pyqtSignal(str)        # レイアウト変更
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 状態管理
        self.current_view_mode = "grid"     # grid, list, details
        self.current_theme = "light"        # light, dark
        self.current_layout = "standard"    # standard, compact, wide
        
        # コンポーネント
        self.view_mode_button: Optional[QPushButton] = None
        self.settings_button: Optional[QPushButton] = None
        self.theme_button: Optional[QPushButton] = None
        self.layout_button: Optional[QPushButton] = None
        self.help_button: Optional[QPushButton] = None
        
        # メニュー
        self.view_mode_menu: Optional[QMenu] = None
        self.theme_menu: Optional[QMenu] = None
        self.layout_menu: Optional[QMenu] = None
        
        # UI設定
        self.setup_ui()
    
    def setup_ui(self):
        """UI初期化"""
        try:
            # メインレイアウト
            layout = QHBoxLayout(self)
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setSpacing(2)
            
            # 左端にスペーサー
            layout.addStretch()
            
            # 表示モードボタン
            self._create_view_mode_button(layout)
            
            # レイアウトボタン
            self._create_layout_button(layout)
            
            # テーマボタン
            self._create_theme_button(layout)
            
            # 設定ボタン
            self._create_settings_button(layout)
            
            # ヘルプボタン
            self._create_help_button(layout)
            
        except Exception as e:
            logging.error(f"ユーティリティコントロールUI初期化エラー: {e}")
    
    def _create_view_mode_button(self, layout: QHBoxLayout):
        """表示モードボタンを作成"""
        try:
            self.view_mode_button = QPushButton("⊞")
            self.view_mode_button.setFixedSize(35, 30)
            self.view_mode_button.setToolTip("表示モード切り替え")
            self.view_mode_button.clicked.connect(self._show_view_mode_menu)
            
            # フォント設定
            font = QFont()
            font.setPointSize(12)
            font.setWeight(QFont.Bold)
            self.view_mode_button.setFont(font)
            
            # スタイル
            self.view_mode_button.setStyleSheet(self._get_utility_button_style())
            
            # メニュー作成
            self._create_view_mode_menu()
            
            layout.addWidget(self.view_mode_button)
            
        except Exception as e:
            logging.error(f"表示モードボタン作成エラー: {e}")
    
    def _create_view_mode_menu(self):
        """表示モードメニューを作成"""
        try:
            self.view_mode_menu = QMenu(self)
            
            # メニュー項目
            modes = [
                ("グリッド表示", "grid", "⊞"),
                ("リスト表示", "list", "☰"),
                ("詳細表示", "details", "▤")
            ]
            
            for name, mode, icon in modes:
                action = QAction(f"{icon} {name}", self)
                action.triggered.connect(lambda checked, m=mode: self._on_view_mode_selected(m))
                if mode == self.current_view_mode:
                    action.setCheckable(True)
                    action.setChecked(True)
                self.view_mode_menu.addAction(action)
            
        except Exception as e:
            logging.error(f"表示モードメニュー作成エラー: {e}")
    
    def _create_layout_button(self, layout: QHBoxLayout):
        """レイアウトボタンを作成"""
        try:
            self.layout_button = QPushButton("⊞")
            self.layout_button.setFixedSize(35, 30)
            self.layout_button.setToolTip("レイアウト変更")
            self.layout_button.clicked.connect(self._show_layout_menu)
            
            # フォント設定
            font = QFont()
            font.setPointSize(11)
            self.layout_button.setFont(font)
            
            # スタイル
            self.layout_button.setStyleSheet(self._get_utility_button_style())
            
            # メニュー作成
            self._create_layout_menu()
            
            layout.addWidget(self.layout_button)
            
        except Exception as e:
            logging.error(f"レイアウトボタン作成エラー: {e}")
    
    def _create_layout_menu(self):
        """レイアウトメニューを作成"""
        try:
            self.layout_menu = QMenu(self)
            
            # メニュー項目
            layouts = [
                ("標準レイアウト", "standard", "⊞"),
                ("コンパクト", "compact", "▦"),
                ("ワイド", "wide", "▬")
            ]
            
            for name, layout_type, icon in layouts:
                action = QAction(f"{icon} {name}", self)
                action.triggered.connect(lambda checked, l=layout_type: self._on_layout_selected(l))
                if layout_type == self.current_layout:
                    action.setCheckable(True)
                    action.setChecked(True)
                self.layout_menu.addAction(action)
            
        except Exception as e:
            logging.error(f"レイアウトメニュー作成エラー: {e}")
    
    def _create_theme_button(self, layout: QHBoxLayout):
        """テーマボタンを作成"""
        try:
            self.theme_button = QPushButton("🌓")
            self.theme_button.setFixedSize(35, 30)
            self.theme_button.setToolTip("テーマ切り替え")
            self.theme_button.clicked.connect(self._show_theme_menu)
            
            # フォント設定
            font = QFont()
            font.setPointSize(11)
            self.theme_button.setFont(font)
            
            # スタイル
            self.theme_button.setStyleSheet(self._get_utility_button_style())
            
            # メニュー作成
            self._create_theme_menu()
            
            layout.addWidget(self.theme_button)
            
        except Exception as e:
            logging.error(f"テーマボタン作成エラー: {e}")
    
    def _create_theme_menu(self):
        """テーマメニューを作成"""
        try:
            self.theme_menu = QMenu(self)
            
            # メニュー項目
            themes = [
                ("ライトテーマ", "light", "☀"),
                ("ダークテーマ", "dark", "🌙"),
                ("自動切り替え", "auto", "🌓")
            ]
            
            for name, theme, icon in themes:
                action = QAction(f"{icon} {name}", self)
                action.triggered.connect(lambda checked, t=theme: self._on_theme_selected(t))
                if theme == self.current_theme:
                    action.setCheckable(True)
                    action.setChecked(True)
                self.theme_menu.addAction(action)
            
        except Exception as e:
            logging.error(f"テーマメニュー作成エラー: {e}")
    
    def _create_settings_button(self, layout: QHBoxLayout):
        """設定ボタンを作成"""
        try:
            self.settings_button = QPushButton("⚙")
            self.settings_button.setFixedSize(35, 30)
            self.settings_button.setToolTip("設定")
            self.settings_button.clicked.connect(self._on_settings_clicked)
            
            # フォント設定
            font = QFont()
            font.setPointSize(12)
            self.settings_button.setFont(font)
            
            # スタイル
            self.settings_button.setStyleSheet(self._get_utility_button_style())
            
            layout.addWidget(self.settings_button)
            
        except Exception as e:
            logging.error(f"設定ボタン作成エラー: {e}")
    
    def _create_help_button(self, layout: QHBoxLayout):
        """ヘルプボタンを作成"""
        try:
            self.help_button = QPushButton("?")
            self.help_button.setFixedSize(35, 30)
            self.help_button.setToolTip("ヘルプ")
            self.help_button.clicked.connect(self._on_help_clicked)
            
            # フォント設定
            font = QFont()
            font.setPointSize(12)
            font.setWeight(QFont.Bold)
            self.help_button.setFont(font)
            
            # スタイル
            self.help_button.setStyleSheet(self._get_utility_button_style())
            
            layout.addWidget(self.help_button)
            
        except Exception as e:
            logging.error(f"ヘルプボタン作成エラー: {e}")
    
    def _get_utility_button_style(self) -> str:
        """ユーティリティボタンのスタイル"""
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
        """
    
    def _show_view_mode_menu(self):
        """表示モードメニューを表示"""
        try:
            if self.view_mode_menu and self.view_mode_button:
                # ボタンの下に表示
                button_pos = self.view_mode_button.mapToGlobal(self.view_mode_button.rect().bottomLeft())
                self.view_mode_menu.exec_(button_pos)
            
        except Exception as e:
            logging.error(f"表示モードメニュー表示エラー: {e}")
    
    def _show_layout_menu(self):
        """レイアウトメニューを表示"""
        try:
            if self.layout_menu and self.layout_button:
                # ボタンの下に表示
                button_pos = self.layout_button.mapToGlobal(self.layout_button.rect().bottomLeft())
                self.layout_menu.exec_(button_pos)
            
        except Exception as e:
            logging.error(f"レイアウトメニュー表示エラー: {e}")
    
    def _show_theme_menu(self):
        """テーマメニューを表示"""
        try:
            if self.theme_menu and self.theme_button:
                # ボタンの下に表示
                button_pos = self.theme_button.mapToGlobal(self.theme_button.rect().bottomLeft())
                self.theme_menu.exec_(button_pos)
            
        except Exception as e:
            logging.error(f"テーマメニュー表示エラー: {e}")
    
    def _on_view_mode_selected(self, mode: str):
        """表示モード選択時の処理"""
        try:
            if mode != self.current_view_mode:
                self.current_view_mode = mode
                self._update_view_mode_button()
                self.view_mode_changed.emit(mode)
            
        except Exception as e:
            logging.error(f"表示モード選択処理エラー: {e}")
    
    def _on_layout_selected(self, layout_type: str):
        """レイアウト選択時の処理"""
        try:
            if layout_type != self.current_layout:
                self.current_layout = layout_type
                self._update_layout_button()
                self.layout_changed.emit(layout_type)
            
        except Exception as e:
            logging.error(f"レイアウト選択処理エラー: {e}")
    
    def _on_theme_selected(self, theme: str):
        """テーマ選択時の処理"""
        try:
            if theme != self.current_theme:
                self.current_theme = theme
                self._update_theme_button()
                self.theme_changed.emit(theme)
            
        except Exception as e:
            logging.error(f"テーマ選択処理エラー: {e}")
    
    def _on_settings_clicked(self):
        """設定ボタンクリック時の処理"""
        try:
            self.settings_requested.emit()
            
        except Exception as e:
            logging.error(f"設定ボタン処理エラー: {e}")
    
    def _on_help_clicked(self):
        """ヘルプボタンクリック時の処理"""
        try:
            self.help_requested.emit()
            
        except Exception as e:
            logging.error(f"ヘルプボタン処理エラー: {e}")
    
    def _update_view_mode_button(self):
        """表示モードボタンのアイコンを更新"""
        try:
            if not self.view_mode_button:
                return
            
            icons = {
                "grid": "⊞",
                "list": "☰", 
                "details": "▤"
            }
            
            icon = icons.get(self.current_view_mode, "⊞")
            self.view_mode_button.setText(icon)
            
            # メニューの選択状態も更新
            self._update_view_mode_menu()
            
        except Exception as e:
            logging.error(f"表示モードボタン更新エラー: {e}")
    
    def _update_layout_button(self):
        """レイアウトボタンのアイコンを更新"""
        try:
            if not self.layout_button:
                return
            
            icons = {
                "standard": "⊞",
                "compact": "▦",
                "wide": "▬"
            }
            
            icon = icons.get(self.current_layout, "⊞")
            self.layout_button.setText(icon)
            
            # メニューの選択状態も更新
            self._update_layout_menu()
            
        except Exception as e:
            logging.error(f"レイアウトボタン更新エラー: {e}")
    
    def _update_theme_button(self):
        """テーマボタンのアイコンを更新"""
        try:
            if not self.theme_button:
                return
            
            icons = {
                "light": "☀",
                "dark": "🌙",
                "auto": "🌓"
            }
            
            icon = icons.get(self.current_theme, "🌓")
            self.theme_button.setText(icon)
            
            # メニューの選択状態も更新
            self._update_theme_menu()
            
        except Exception as e:
            logging.error(f"テーマボタン更新エラー: {e}")
    
    def _update_view_mode_menu(self):
        """表示モードメニューの選択状態を更新"""
        try:
            if not self.view_mode_menu:
                return
            
            # 全アクションのチェック状態をリセット
            for action in self.view_mode_menu.actions():
                action.setChecked(False)
                action.setCheckable(False)
            
            # 現在のモードに対応するアクションをチェック
            # TODO: アクションとモードの対応付けを改善
            
        except Exception as e:
            logging.error(f"表示モードメニュー更新エラー: {e}")
    
    def _update_layout_menu(self):
        """レイアウトメニューの選択状態を更新"""
        try:
            if not self.layout_menu:
                return
            
            # 全アクションのチェック状態をリセット
            for action in self.layout_menu.actions():
                action.setChecked(False)
                action.setCheckable(False)
            
        except Exception as e:
            logging.error(f"レイアウトメニュー更新エラー: {e}")
    
    def _update_theme_menu(self):
        """テーマメニューの選択状態を更新"""
        try:
            if not self.theme_menu:
                return
            
            # 全アクションのチェック状態をリセット
            for action in self.theme_menu.actions():
                action.setChecked(False)
                action.setCheckable(False)
            
        except Exception as e:
            logging.error(f"テーマメニュー更新エラー: {e}")
    
    def set_view_mode(self, mode: str):
        """表示モードを設定"""
        try:
            if mode in ["grid", "list", "details"]:
                self.current_view_mode = mode
                self._update_view_mode_button()
            
        except Exception as e:
            logging.error(f"表示モード設定エラー: {e}")
    
    def set_theme(self, theme: str):
        """テーマを設定"""
        try:
            if theme in ["light", "dark", "auto"]:
                self.current_theme = theme
                self._update_theme_button()
            
        except Exception as e:
            logging.error(f"テーマ設定エラー: {e}")
    
    def set_layout(self, layout_type: str):
        """レイアウトを設定"""
        try:
            if layout_type in ["standard", "compact", "wide"]:
                self.current_layout = layout_type
                self._update_layout_button()
            
        except Exception as e:
            logging.error(f"レイアウト設定エラー: {e}")
    
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
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #505050;
                    border-color: #777;
                }
                QPushButton:pressed {
                    background-color: #2a2a2a;
                }
            """
            
            # 全ボタンに適用
            for button in [self.view_mode_button, self.theme_button, self.layout_button,
                          self.settings_button, self.help_button]:
                if button:
                    button.setStyleSheet(dark_style)
            
        except Exception as e:
            logging.error(f"ダークテーマ適用エラー: {e}")
    
    def _apply_light_theme(self):
        """ライトテーマを適用"""
        try:
            # 元のスタイルに戻す
            light_style = self._get_utility_button_style()
            
            for button in [self.view_mode_button, self.theme_button, self.layout_button,
                          self.settings_button, self.help_button]:
                if button:
                    button.setStyleSheet(light_style)
            
        except Exception as e:
            logging.error(f"ライトテーマ適用エラー: {e}")
