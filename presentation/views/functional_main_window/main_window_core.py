"""
Main Window Core

メインウィンドウの基本構成と初期化を担当
"""

import os
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# コントロールのインポート  
from ui.controls import create_controls

# テーマシステム
from presentation.themes.theme_mixin import ThemeAwareMixin


class MainWindowCore(QMainWindow, ThemeAwareMixin):
    """
    メインウィンドウのコア機能
    
    基本的なウィンドウ構成、初期化、メイン制御を担当
    """
    
    def __init__(self):
        QMainWindow.__init__(self)
        ThemeAwareMixin.__init__(self)
        
        # ウィンドウ基本設定
        self.setWindowTitle("PhotoMap Explorer - 新UI (Clean Architecture) v2.2.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # 状態管理
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        
        # UI状態管理
        self.maximized_state = None  # 'image', 'map', None
        self.main_splitter = None
        self.right_splitter = None
        self.maximize_container = None
        self.original_preview_parent = None
        self.original_map_parent = None
        
        # UIコンポーネント参照
        self.thumbnail_list = None
        self.preview_panel = None
        self.map_panel = None
        self.folder_panel = None
        self.address_bar = None
        
        # 管理クラス参照（後で設定）
        self.left_panel_manager = None
        self.right_panel_manager = None
        self.address_bar_manager = None
        self.maximize_handler = None
        self.folder_event_handler = None
        self.image_event_handler = None
        self.theme_event_handler = None
        self.image_display_manager = None
        self.map_display_manager = None
        self.status_display_manager = None
        
        # 初期化
        self._setup_icon()
        self._setup_basic_ui()
    
    def _setup_icon(self):
        """アイコン設定"""
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_basic_ui(self):
        """基本UI構成の設定"""
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # ツールバーエリアの準備（詳細は後で設定）
        self._setup_toolbar_area()
        
        # メインスプリッターの準備
        self.main_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.main_splitter)
        
        # 最大化コンテナの準備
        self._setup_maximize_container()
        
        # ステータスバー
        status_bar = self.statusBar()
        if status_bar:
            status_bar.showMessage("初期化中...")
    
    def _setup_toolbar_area(self):
        """ツールバーエリアの基本設定"""
        # ツールバーレイアウト
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        
        # フォルダ選択ボタン
        self.folder_btn = QPushButton("📁 フォルダ選択")
        self.folder_btn.setMaximumHeight(30)
        toolbar_layout.addWidget(self.folder_btn)
        
        # アドレスバーエリア（詳細は後で設定）
        def dummy_callback(*args, **kwargs):
            pass  # 暫定的なダミーコールバック
        
        self.controls_widget, self.address_bar, self.parent_button = create_controls(
            dummy_callback,  # 暫定コールバック
            dummy_callback   # 暫定コールバック
        )
        self.controls_widget.setMaximumHeight(35)
        toolbar_layout.addWidget(self.controls_widget, 1)
        
        # テーマ切り替えボタン
        self.theme_toggle_btn = QPushButton("🌙 ダーク")
        self.theme_toggle_btn.setMaximumHeight(30)
        self.theme_toggle_btn.setMaximumWidth(80)
        self.theme_toggle_btn.setToolTip("ダークモード・ライトモード切り替え")
        toolbar_layout.addWidget(self.theme_toggle_btn)
        
        # ツールバーウィジェット
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setLayout(toolbar_layout)
        self.toolbar_widget.setMaximumHeight(40)
        self.main_layout.addWidget(self.toolbar_widget)
    
    def _setup_maximize_container(self):
        """最大化コンテナの準備"""
        from PyQt5.QtWidgets import QVBoxLayout
        
        self.maximize_container = QWidget()
        self.maximized_content_layout = QVBoxLayout(self.maximize_container)
        self.maximized_content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 最大化コンテナを追加（初期は非表示）
        self.main_layout.addWidget(self.maximize_container)
        self.maximize_container.hide()
    
    def setup_managers(self, left_panel_mgr, right_panel_mgr, address_bar_mgr, maximize_hdlr,
                      folder_event_hdlr, image_event_hdlr, theme_event_hdlr,
                      image_display_mgr, map_display_mgr, status_display_mgr):
        """
        各種管理クラスを設定
        """
        self.left_panel_manager = left_panel_mgr
        self.right_panel_manager = right_panel_mgr
        self.address_bar_manager = address_bar_mgr
        self.maximize_handler = maximize_hdlr
        self.folder_event_handler = folder_event_hdlr
        self.image_event_handler = image_event_hdlr
        self.theme_event_handler = theme_event_hdlr
        self.image_display_manager = image_display_mgr
        self.map_display_manager = map_display_mgr
        self.status_display_manager = status_display_mgr
        
        # 各管理クラスに参照を渡す
        self._setup_manager_references()
        
        # イベントハンドラの接続
        self._connect_event_handlers()
    
    def _setup_manager_references(self):
        """管理クラス間の参照を設定"""
        try:
            from utils.debug_logger import debug, info, error
            info("管理クラス間の参照設定開始")
            
            # デバッグ: 詳細な条件確認
            debug(f"self.left_panel_manager: {self.left_panel_manager}")
            debug(f"self.main_splitter: {self.main_splitter}")
            debug(f"self.right_panel_manager: {self.right_panel_manager}")
            
            # 左パネル作成
            debug("左パネル作成条件チェック開始...")
            if self.left_panel_manager is not None and self.main_splitter is not None:
                debug("左パネル作成開始...")
                left_panel = self.left_panel_manager.create_panel()
                debug(f"左パネル作成完了: {left_panel is not None}")
                if left_panel:
                    self.main_splitter.addWidget(left_panel)
                    left_panel.show()  # 左パネルも強制表示
                    info("左パネルをメインスプリッターに追加完了")
                else:
                    error("左パネル作成に失敗")
            else:
                error(f"左パネル作成条件未満: left_panel_manager={self.left_panel_manager is not None}, main_splitter={self.main_splitter is not None}")
            
            # 右パネル作成
            debug("右パネル作成条件チェック開始...")
            if self.right_panel_manager is not None and self.main_splitter is not None:
                debug("右パネル作成開始...")
                right_panel = self.right_panel_manager.create_panel()
                debug(f"右パネル作成完了: {right_panel is not None}")
                if right_panel:
                    self.main_splitter.addWidget(right_panel)
                    info("右パネルをメインスプリッターに追加完了")
                    
                    # 右パネルの詳細デバッグ
                    debug(f"右パネル追加後サイズ: {right_panel.size()}")
                    debug(f"右パネル追加後可視性: {right_panel.isVisible()}")
                    
                    # 強制的に右パネルを表示
                    right_panel.show()
                    debug(f"強制表示後の右パネル可視性: {right_panel.isVisible()}")
                    
                    if hasattr(self.right_panel_manager, 'right_splitter') and self.right_panel_manager.right_splitter:
                        debug(f"右スプリッターサイズ: {self.right_panel_manager.right_splitter.size()}")
                        debug(f"右スプリッター子要素数: {self.right_panel_manager.right_splitter.count()}")
                        debug(f"右スプリッター可視性: {self.right_panel_manager.right_splitter.isVisible()}")
                        self.right_panel_manager.right_splitter.show()
                        debug(f"強制表示後の右スプリッター可視性: {self.right_panel_manager.right_splitter.isVisible()}")
                else:
                    error("右パネル作成に失敗")
            else:
                error(f"右パネル作成条件未満: right_panel_manager={self.right_panel_manager is not None}, main_splitter={self.main_splitter is not None}")
            
            # スプリッターサイズ調整
            if self.main_splitter:
                debug("スプリッターサイズ調整...")
                self.main_splitter.setSizes([600, 800])
                
                # スプリッター調整後のデバッグ
                debug(f"メインスプリッター最終サイズ配分: {self.main_splitter.sizes()}")
                for i in range(self.main_splitter.count()):
                    widget = self.main_splitter.widget(i)
                    if widget:
                        debug(f"子ウィジェット{i}最終サイズ: {widget.size()}, 可視性: {widget.isVisible()}")
                    else:
                        debug(f"子ウィジェット{i}: None")
                
                info(f"スプリッターサイズ調整完了: 子要素数={self.main_splitter.count()}")
                
            info("管理クラス間の参照設定完了")
            
            # 最終的にメインスプリッター全体を強制表示
            debug("メインスプリッター最終強制表示開始...")
            if self.main_splitter:
                self.main_splitter.show()
                debug(f"メインスプリッター強制表示後: 可視性={self.main_splitter.isVisible()}")
                for i in range(self.main_splitter.count()):
                    widget = self.main_splitter.widget(i)
                    if widget:
                        widget.show()
                        debug(f"子ウィジェット{i}強制表示後: 可視性={widget.isVisible()}")
            
            debug("管理クラス間の参照設定と表示設定完了")
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"管理クラス参照設定エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _connect_event_handlers(self):
        """イベントハンドラの接続"""
        # フォルダ選択ボタン
        if self.folder_event_handler:
            self.folder_btn.clicked.connect(self.folder_event_handler.select_folder)
        
        # テーマ切り替えボタン
        if self.theme_event_handler:
            self.theme_toggle_btn.clicked.connect(self.theme_event_handler.toggle_theme)
        
        # アドレスバー関連（set_componentsメソッドを使用）
        if self.address_bar_manager and self.folder_event_handler:
            self.address_bar_manager.set_components(
                self.address_bar,
                self.folder_event_handler
            )
    
    def show_status_message(self, message, timeout=0):
        """ステータスバーにメッセージを表示"""
        try:
            status_bar = self.statusBar()
            if status_bar:
                status_bar.showMessage(message, timeout)
            else:
                pass  # ステータスバーが無い場合は何もしない
        except Exception as e:
            import logging
            logging.error(f"ステータス表示エラー: {e}, メッセージ: {message}")
    
    def finalize_setup(self):
        """セットアップの最終処理"""
        # テーマコンポーネント登録
        self.register_theme_component(self.folder_btn, "button")
        self.register_theme_component(self.theme_toggle_btn, "button") 
        self.register_theme_component(self.parent_button, "button")
        self.register_theme_component(self.toolbar_widget, "panel")
        
        # 初期テーマ設定
        if self.theme_event_handler:
            # self.theme_event_handler.update_theme_button()  # メソッドが存在しない
            self.theme_event_handler.initialize_theme()  # 代替メソッド
        
        self.apply_theme()
        
        # アドレスバーの遅延テーマ適用
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self._apply_delayed_theme)
        
        # ステータス更新
        self.show_status_message("新UI (Clean Architecture) v2.2.0 で起動しました")
        
        # 最終的な表示確認とデバッグ
        from utils.debug_logger import debug, info
        debug("ファイナライズ後の表示状態確認...")
        if self.main_splitter:
            debug(f"ファイナライズ後メインスプリッター可視性: {self.main_splitter.isVisible()}")
            for i in range(self.main_splitter.count()):
                widget = self.main_splitter.widget(i)
                if widget:
                    debug(f"ファイナライズ後子ウィジェット{i}可視性: {widget.isVisible()}")
                    widget.show()  # 再度強制表示
    
    def _apply_delayed_theme(self):
        """遅延テーマ適用"""
        if self.address_bar_manager:
            # self.address_bar_manager.apply_delayed_theme()  # メソッドが存在しない
            pass  # 一時的にスキップ
