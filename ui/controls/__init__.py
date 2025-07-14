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
├── breadcrumb_manager.py (400行) - ブレッドクラム管        # 統合アドレスバーを作成
        controls_container = IntegratedAddressBar()
        if on_address_changed_callback:
            controls_container.path_changed.connect(on_address_changed_callback)
        
        # デバッグ：アドレスバー作成直後の状態確認
        debug(f"🔧 🔧 IntegratedAddressBar作成直後: visible={controls_container.isVisible()}, size={controls_container.size()}")
        
        # より詳細なデバッグ: 親ウィジェットとの関係を確認
        debug(f"🔧 🔧 親ウィジェット確認: parent={controls_container.parent()}")
        debug(f"🔧 🔧 レイアウト追加前のcontrols_widget状態: visible={controls_widget.isVisible()}")
        
        main_layout.addWidget(controls_container)  # 下段に配置
        
        # デバッグ：レイアウト追加後の状態確認
        debug(f"🔧 🔧 IntegratedAddressBarレイアウト追加後: visible={controls_container.isVisible()}, size={controls_container.size()}")
        debug(f"🔧 🔧 親ウィジェット確認（追加後）: parent={controls_container.parent()}")
        debug(f"🔧 🔧 controls_widget状態（追加後）: visible={controls_widget.isVisible()}")
        
        # レイアウト追加後に明示的に表示設定
        controls_container.setVisible(True)
        controls_container.show()
        debug(f"🔧 🔧 IntegratedAddressBar強制表示後: visible={controls_container.isVisible()}, size={controls_container.size()}")
        
        # さらに詳細なデバッグ: ウィジェット階層を確認
        debug(f"🔧 🔧 レイアウト子要素数: {main_layout.count()}")
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                debug(f"🔧 🔧 レイアウト子要素[{i}]: {widget}, visible={widget.isVisible()}, size={widget.size()}")
        
        debug("コントロール全体作成完了（縦配置）: widget={controls_widget}, container={controls_container}, parent_btn={parent_button}")ndler.py (400行) - テキスト入力処理
└── __init__.py (130行) - 統合

toolbar/
├── navigation_controls.py (350行) - ナビゲーション制御
├── utility_controls.py (450行) - ユーティリティ制御
└── __init__.py (150行) - 統合

合計: 2,350行（元の425行から約5.5倍に拡張・モジュール化）
"""

# アドレスバー関連のインポート
import logging
from utils.debug_logger import debug, info, warning, error, verbose
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
    後方互換性のためのcreate_controls関数
    
    元の ui/controls.py の create_controls 関数と同じインターフェースを提供
    
    Args:
        on_address_changed_callback: アドレス変更時のコールバック
        on_parent_button_callback: 親フォルダボタンクリック時のコールバック
        
    Returns:
        tuple: (controls_widget, address_bar, parent_button)
    """
    try:
        # 全体のコンテナを作成（水平レイアウトに変更）
        from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
        controls_widget = QWidget()
        # 明示的に表示状態を設定
        controls_widget.setVisible(True)
        controls_widget.show()
        
        # 最小高さ設定（横並びに最適化）
        controls_widget.setMinimumHeight(45)  # 少し高くして余裕を持たせる
        controls_widget.setMaximumHeight(55)
        
        # 水平レイアウト（横並び）
        main_layout = QHBoxLayout(controls_widget)
        main_layout.setContentsMargins(5, 3, 5, 3)  # 左右に余白を追加
        main_layout.setSpacing(10)  # ボタン間のスペースを拡大
        
        # ナビゲーションコントロールを作成
        nav_controls = None
        parent_button = None
        try:
            from .toolbar.navigation_controls import NavigationControls
            nav_controls = NavigationControls()
            # 最小高さ設定
            nav_controls.setMinimumHeight(30)
            nav_controls.setMaximumHeight(40)
            # 最小幅を設定してボタンが見切れないように
            nav_controls.setMinimumWidth(200)
            nav_controls.setVisible(True)
            nav_controls.show()
            parent_button = nav_controls.parent_button
            if parent_button and on_parent_button_callback:
                parent_button.clicked.connect(on_parent_button_callback)
            main_layout.addWidget(nav_controls, 0)  # 固定幅で左側に配置
            debug("ナビゲーションコントロール作成成功: {nav_controls}")
        except Exception as e:
            warning("ナビゲーションコントロール作成エラー: {e}")
            logging.warning(f"ナビゲーションコントロール設定エラー: {e}")
        
        # 間にスペーサーを追加（調整可能）
        main_layout.addSpacing(5)
        
        # アドレスバー（右側に配置、拡張可能）
        controls_container = IntegratedAddressBar(controls_widget)  # 親ウィジェットを指定
        # アドレスバーの最小幅を確保
        controls_container.setMinimumWidth(300)
        if on_address_changed_callback:
            controls_container.path_changed.connect(on_address_changed_callback)
        
        # デバッグ：アドレスバー作成直後の状態確認
        debug(f"🔧 IntegratedAddressBar作成直後: visible={controls_container.isVisible()}, size={controls_container.size()}")
        debug(f"🔧 🔧 親ウィジェット(controls_widget)の状態: visible={controls_widget.isVisible()}, size={controls_widget.size()}")
        debug(f"🔧 🔧 メインレイアウトの状態: count={main_layout.count()}, parent={main_layout.parent()}")
        
        # レイアウト追加前の詳細確認
        debug(f"🔧 🔧 レイアウト追加前 - address_bar parent: {controls_container.parent()}")
        debug(f"🔧 🔧 レイアウト追加前 - controls_widget visible: {controls_widget.isVisible()}")
        
        main_layout.addWidget(controls_container, 1)  # 右側に配置（拡張可能）
        
        # レイアウト追加後の詳細確認
        debug(f"🔧 IntegratedAddressBarレイアウト追加後: visible={controls_container.isVisible()}, size={controls_container.size()}")
        debug(f"🔧 🔧 レイアウト追加後 - address_bar parent: {controls_container.parent()}")
        debug(f"🔧 🔧 レイアウト追加後 - layout widget count: {main_layout.count()}")
        debug(f"🔧 🔧 レイアウト追加後 - controls_widget visible: {controls_widget.isVisible()}")
        
        # レイアウト内の全ウィジェットの状態確認
        for i in range(main_layout.count()):
            item = main_layout.itemAt(i)
            if item:
                if item.widget():
                    widget = item.widget()
                    if widget:
                        debug(f"🔧 🔧 レイアウト内ウィジェット[{i}]: visible={widget.isVisible()}, size={widget.size()}, type={type(widget)}")
                elif item.layout():
                    layout_item = item.layout()
                    if layout_item:
                        debug(f"🔧 🔧 レイアウト内アイテム[{i}]: count={layout_item.count()}, type={type(layout_item)}")
        
        # 強制表示
        controls_container.setVisible(True)
        controls_container.show()
        debug(f"🔧 IntegratedAddressBar強制表示後: visible={controls_container.isVisible()}, size={controls_container.size()}")
        
        # ナビゲーションコントロールも強制表示
        if nav_controls:
            nav_controls.setVisible(True)
            nav_controls.show()
            debug(f"🔧 🔧 nav_controls強制表示後: visible={nav_controls.isVisible()}, size={nav_controls.size()}")
        
        # 親ウィジェットも強制表示
        controls_widget.setVisible(True)
        controls_widget.show()
        debug(f"🔧 🔧 親ウィジェット強制表示後 - widget: visible={controls_widget.isVisible()}, size={controls_widget.size()}")
        
        # PyQtイベントループ処理後に再度表示状態を確保する遅延処理
        from PyQt5.QtCore import QTimer
        def ensure_visibility():
            try:
                # アドレスバーの表示確保
                if not controls_container.isVisible():
                    debug(f"🔧 🔧 遅延処理: controls_containerが非表示になっているため再表示")
                    controls_container.setVisible(True)
                    controls_container.show()
                
                # ナビゲーションコントロールの表示確保
                if nav_controls and not nav_controls.isVisible():
                    debug(f"🔧 🔧 遅延処理: nav_controlsが非表示になっているため再表示")
                    nav_controls.setVisible(True)
                    nav_controls.show()
                
                # 最終状態をログ
                debug(f"🔧 🔧 遅延処理後最終状態:")
                debug(f"🔧 🔧   - controls_widget: visible={controls_widget.isVisible()}")
                debug(f"🔧 🔧   - controls_container: visible={controls_container.isVisible()}")
                if nav_controls:
                    debug(f"🔧 🔧   - nav_controls: visible={nav_controls.isVisible()}")
                    
            except Exception as e:
                debug(f"🔧 🔧 遅延表示処理エラー: {e}")
        
        # イベントループ処理後に実行
        QTimer.singleShot(100, ensure_visibility)
        
        # 最終状態の確認
        debug(f"🔧 🔧 最終状態確認:")
        debug(f"🔧 🔧   - controls_widget: visible={controls_widget.isVisible()}, size={controls_widget.size()}")
        debug(f"🔧 🔧   - controls_container: visible={controls_container.isVisible()}, size={controls_container.size()}")
        if nav_controls:
            debug(f"🔧 🔧   - nav_controls: visible={nav_controls.isVisible()}, size={nav_controls.size()}")
        
        debug("コントロール全体作成完了（横並び）: widget={controls_widget}, container={controls_container}, parent_btn={parent_button}")
        
        return controls_widget, controls_container, parent_button
        
    except Exception as e:
        error("create_controls エラー: {e}")
        # フォールバック: 統合アドレスバーのみ作成
        controls_container = IntegratedAddressBar()
        if on_address_changed_callback:
            controls_container.path_changed.connect(on_address_changed_callback)
        return controls_container, controls_container, None
