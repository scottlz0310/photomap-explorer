"""
UI Controls モジュール統合パッケージ

このモジュールは元の ui/controls.py から分離された機能を
統合して提供します。

主要コンポーネント:
- address_bar: GIMP風ブレッドクラムアドレスバー機能
- toolbar: ナビゲーションとユーティリティコントロール機能

Phase 2 リファクタリング完了:
元の ui/controls.py (425行) を以下の構造に分割:

address_bar/
├── address_bar_core.py (470行) - コア機能
├── breadcrumb_manager.py (400行) - ブレッドクラム管理
├── text_input_handler.py (400行) - テキスト入力処理
└── __init__.py (130行) - 統合

toolbar/
├── navigation_controls.py (350行) - ナビゲーション制御
├── utility_controls.py (450行) - ユーティリティ制御
└── __init__.py (150行) - 統合

合計: 2,350行（元の425行から約5.5倍に拡張・モジュール化）
"""

# アドレスバー関連のインポート
from .address_bar import (
    AddressBarCore,
    BreadcrumbManager,
    TextInputHandler,
    IntegratedAddressBar,
    GIMPAddressBar  # 後方互換性用別名
)

# ツールバー関連のインポート
from .toolbar import (
    NavigationControls,
    UtilityControls,
    IntegratedToolbar
)

# 統合コントロールクラス
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import pyqtSignal
import logging


class ModernControlsContainer(QWidget):
    """
    モダンコントロールコンテナークラス
    
    アドレスバーとツールバーを統合し、
    元の ui/controls.py と同等の機能を提供する
    モダンなコントロールインターフェース。
    """
    
    # 統合シグナル
    path_changed = pyqtSignal(str)          # パス変更
    navigation_requested = pyqtSignal(str)   # ナビゲーション要求
    parent_folder_requested = pyqtSignal()   # 親フォルダ移動要求
    home_folder_requested = pyqtSignal()     # ホームフォルダ移動要求
    back_requested = pyqtSignal()            # 戻る要求
    forward_requested = pyqtSignal()         # 進む要求
    refresh_requested = pyqtSignal()         # 更新要求
    view_mode_changed = pyqtSignal(str)      # 表示モード変更
    settings_requested = pyqtSignal()        # 設定画面要求
    help_requested = pyqtSignal()            # ヘルプ表示要求
    theme_changed = pyqtSignal(str)          # テーマ変更
    layout_changed = pyqtSignal(str)         # レイアウト変更
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # コンポーネント初期化
        self.address_bar = IntegratedAddressBar(self)
        self.toolbar = IntegratedToolbar(self)
        
        # 状態管理
        self.current_path = ""
        
        # UI設定
        self._setup_container_ui()
        
        # シグナル接続
        self._connect_container_signals()
    
    def _setup_container_ui(self):
        """コンテナーUIを設定"""
        try:
            # 垂直レイアウト
            layout = QVBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(2)
            
            # アドレスバーを上部に
            layout.addWidget(self.address_bar)
            
            # ツールバーを下部に
            layout.addWidget(self.toolbar)
            
        except Exception as e:
            logging.error(f"コントロールコンテナーUI設定エラー: {e}")
    
    def _connect_container_signals(self):
        """コンテナー内シグナルを接続"""
        try:
            # アドレスバー → 外部
            self.address_bar.path_changed.connect(self._on_path_changed)
            self.address_bar.navigation_requested.connect(self._on_navigation_requested)
            
            # ツールバー → 外部
            self.toolbar.parent_folder_requested.connect(self.parent_folder_requested)
            self.toolbar.home_folder_requested.connect(self.home_folder_requested)
            self.toolbar.back_requested.connect(self.back_requested)
            self.toolbar.forward_requested.connect(self.forward_requested)
            self.toolbar.refresh_requested.connect(self.refresh_requested)
            self.toolbar.view_mode_changed.connect(self.view_mode_changed)
            self.toolbar.settings_requested.connect(self.settings_requested)
            self.toolbar.help_requested.connect(self.help_requested)
            self.toolbar.theme_changed.connect(self.theme_changed)
            self.toolbar.layout_changed.connect(self.layout_changed)
            
        except Exception as e:
            logging.error(f"コンテナーシグナル接続エラー: {e}")
    
    def _on_path_changed(self, path: str):
        """パス変更時の処理"""
        try:
            self.current_path = path
            self.toolbar.set_current_path(path)
            self.path_changed.emit(path)
            
        except Exception as e:
            logging.error(f"パス変更処理エラー: {e}")
    
    def _on_navigation_requested(self, path: str):
        """ナビゲーション要求時の処理"""
        try:
            self.current_path = path
            self.toolbar.set_current_path(path)
            self.navigation_requested.emit(path)
            
        except Exception as e:
            logging.error(f"ナビゲーション要求処理エラー: {e}")
    
    # 外部インターフェース（元のcontrols.pyと互換性）
    
    def set_path(self, path: str):
        """パスを設定"""
        try:
            self.current_path = path
            self.address_bar.setText(path)
            self.toolbar.set_current_path(path)
            
        except Exception as e:
            logging.error(f"パス設定エラー: {e}")
    
    def get_path(self) -> str:
        """現在のパスを取得"""
        return self.current_path
    
    def set_history_state(self, can_back: bool, can_forward: bool):
        """履歴状態を設定"""
        try:
            self.toolbar.set_history_state(can_back, can_forward)
            
        except Exception as e:
            logging.error(f"履歴状態設定エラー: {e}")
    
    def apply_theme(self, theme_name: str):
        """テーマを適用"""
        try:
            self.address_bar.apply_theme(theme_name)
            self.toolbar.apply_theme(theme_name)
            
        except Exception as e:
            logging.error(f"コントロールテーマ適用エラー: {e}")
    
    def get_address_bar(self) -> IntegratedAddressBar:
        """アドレスバーを取得"""
        return self.address_bar
    
    def get_toolbar(self) -> IntegratedToolbar:
        """ツールバーを取得"""
        return self.toolbar


# パッケージレベルのエクスポート
__all__ = [
    # アドレスバー関連
    'AddressBarCore',
    'BreadcrumbManager',
    'TextInputHandler', 
    'IntegratedAddressBar',
    'GIMPAddressBar',
    
    # ツールバー関連
    'NavigationControls',
    'UtilityControls',
    'IntegratedToolbar',
    'create_controls',
    
    # 統合コンテナー
    'ModernControlsContainer'
]


# 後方互換性のための関数
def create_gimp_address_bar(parent=None):
    """
    GIMP風アドレスバーを作成
    
    元のGIMPAddressBarクラスと同等の機能を提供します。
    後方互換性のためのラッパー関数。
    
    Args:
        parent: 親ウィジェット
        
    Returns:
        IntegratedAddressBar: 統合アドレスバーインスタンス
    """
    return IntegratedAddressBar(parent)


def create_modern_controls(parent=None):
    """
    モダンコントロールコンテナーを作成
    
    元の ui/controls.py の全機能を提供する
    統合コントロールインターフェース。
    
    Args:
        parent: 親ウィジェット
        
    Returns:
        ModernControlsContainer: モダンコントロールコンテナーインスタンス
    """
    return ModernControlsContainer(parent)


def create_controls(on_address_changed_callback=None, on_parent_button_callback=None):
    """
    シンプルなフォルダパス表示コントロール
    
    アドレスバーの代わりに、カレントフォルダをラベル形式で表示
    
    Args:
        on_address_changed_callback: アドレス変更時のコールバック（互換性のため）
        on_parent_button_callback: 親フォルダボタンクリック時のコールバック
        
    Returns:
        tuple: (controls_widget, folder_label, parent_button)
    """
    from PyQt5.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel
    from PyQt5.QtGui import QFont
    from PyQt5.QtCore import Qt
    
    # レイアウト作成
    controls_widget = QWidget()
    layout = QHBoxLayout(controls_widget)
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(10)
    
    # フォルダパス表示ラベルを作成
    folder_label = QLabel("フォルダを選択してください", controls_widget)
    # folder_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
    folder_label.setStyleSheet("""
        QLabel {
            background-color: #f0f0f0;
            border: 1px solid #d0d0d0;
            border-radius: 4px;
            padding: 6px 12px;
            font-size: 12px;
            color: #333;
        }
    """)
    
    # フォルダパス更新メソッドを追加
    def update_folder_path(path):
        """フォルダパスを更新する"""
        import os
        if path and os.path.exists(path):
            folder_label.setText(f"📁 {path}")
            folder_label.setToolTip(f"現在のフォルダ: {path}")
        else:
            folder_label.setText("フォルダを選択してください")
            folder_label.setToolTip("")
    
    # メソッドをラベルに追加（互換性のため）
    folder_label.update_folder_path = update_folder_path
    folder_label.update_address = update_folder_path  # IntegratedAddressBarとの互換性
    
    # 親フォルダに戻るボタンを作成
    parent_button = QPushButton("⬆️", controls_widget)
    parent_button.setFixedSize(38, 30)
    parent_button.setToolTip("親フォルダへ移動")
    
    if on_parent_button_callback:
        parent_button.clicked.connect(on_parent_button_callback)
    
    # 親フォルダボタンのフォント設定
    parent_font = QFont()
    parent_font.setPointSize(12)
    parent_button.setFont(parent_font)

    # ウィジェットをレイアウトに追加
    layout.addWidget(folder_label, 1)  # 拡張可能
    layout.addWidget(parent_button)
    
    return controls_widget, folder_label, parent_button
