"""
Main Window Core

メインウィンドウの基本構成と初期化を担当
"""

import os
import logging
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

# コントロールのインポート  
from ui.controls import create_controls

# テーマシステム
from presentation.themes import ThemeAwareMixin


class MainWindowCore(QMainWindow, ThemeAwareMixin):
    """
    メインウィンドウのコア機能
    
    基本的なウィンドウ構成、初期化、メイン制御を担当
    """
    
    def __init__(self):
        super().__init__()  # QMainWindow の初期化
        
        # テーマ関連属性を手動で初期化（ThemeAwareMixin の属性）
        from presentation.themes.core.theme_engine import ThemeEngine
        self.theme_engine = ThemeEngine()
        self.theme_components = []
        
        # ログの設定
        logger = logging.getLogger(__name__)
        logger.debug("MainWindowCore 初期化開始")
        
        # テーマ変更シグナルに接続
        try:
            self.theme_engine.theme_changed.connect(self.on_theme_changed)
        except Exception as e:
            logger.warning(f"テーマシグナル接続失敗: {e}")
        
        logger.debug("MainWindowCore 初期化完了")
        
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
        
        # アドレスバーエリア（イベントハンドラを適切に設定）
        self.controls_widget, self.address_bar, self.parent_button = create_controls(
            self._on_address_changed,  # アドレス変更時のコールバック
            self._on_parent_button_clicked   # 親フォルダボタンクリック時のコールバック
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
        logger = logging.getLogger(__name__)
        logger.debug("=== _setup_manager_references開始 ===")
        
        # 左パネル作成
        logger.debug(f"left_panel_manager: {self.left_panel_manager}")
        logger.debug(f"main_splitter: {self.main_splitter}")
        
        if self.left_panel_manager is not None and self.main_splitter is not None:
            logger.debug("左パネル作成開始")
            left_panel = self.left_panel_manager.create_panel()
            logger.debug(f"左パネル作成完了: {left_panel}")
            self.main_splitter.addWidget(left_panel)
            logger.debug("左パネルをスプリッターに追加完了")
        else:
            logger.warning(f"左パネル作成スキップ - left_panel_manager: {self.left_panel_manager is not None}, main_splitter: {self.main_splitter is not None}")
        
        # 右パネル作成
        if self.right_panel_manager is not None and self.main_splitter is not None:
            logger.debug("右パネル作成開始")
            right_panel = self.right_panel_manager.create_panel()
            logger.debug(f"右パネル作成完了: {right_panel}")
            self.main_splitter.addWidget(right_panel)
            logger.debug("右パネルをスプリッターに追加完了")
        else:
            logger.warning(f"右パネル作成スキップ - right_panel_manager: {self.right_panel_manager is not None}, main_splitter: {self.main_splitter is not None}")
        
        # スプリッターサイズ調整
        if self.main_splitter is not None:
            logger.debug(f"スプリッター子要素数（設定前）: {self.main_splitter.count()}")
            self.main_splitter.setSizes([600, 800])
            logger.debug(f"スプリッター子要素数（設定後）: {self.main_splitter.count()}")
        
        logger.debug("=== _setup_manager_references完了 ===")
    
    def _connect_event_handlers(self):
        """イベントハンドラの接続"""
        # フォルダ選択ボタン
        if self.folder_event_handler:
            self.folder_btn.clicked.connect(self.folder_event_handler.select_folder)
        
        # テーマ切り替えボタン
        if self.theme_event_handler:
            self.theme_toggle_btn.clicked.connect(self.theme_event_handler.toggle_theme)
        
        # アドレスバー関連
        if self.address_bar_manager and self.folder_event_handler:
            # アドレスバーマネージャーのコンポーネント設定
            if hasattr(self, 'address_bar'):
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
            self.theme_event_handler.update_theme_button()
        
        self.apply_theme()
        
        # アドレスバーの遅延テーマ適用
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self._apply_delayed_theme)
        
        # ステータス更新
        self.show_status_message("新UI (Clean Architecture) v2.2.0 で起動しました")
    
    def _apply_delayed_theme(self):
        """遅延テーマ適用"""
        logger = logging.getLogger(__name__)
        if self.address_bar_manager:
            # AddressBarManagerに遅延テーマ適用メソッドがない場合はスキップ
            if hasattr(self.address_bar_manager, 'apply_delayed_theme'):
                self.address_bar_manager.apply_delayed_theme()
            else:
                logger.debug("AddressBarManager: apply_delayed_theme メソッドなし（スキップ）")
    
    # テーマ関連メソッド（ThemeAwareMixin からの機能）
    def register_theme_component(self, widget, component_type="widget"):
        """テーマコンポーネントを登録"""
        logger = logging.getLogger(__name__)
        try:
            self.theme_components.append((widget, component_type))
            logger.debug(f"テーマコンポーネント登録: {widget.__class__.__name__} - {component_type}")
        except Exception as e:
            logger.error(f"テーマコンポーネント登録エラー: {e}")
    
    def apply_theme(self):
        """テーマを適用"""
        logger = logging.getLogger(__name__)
        try:
            current_theme = self.theme_engine.get_current_theme()
            self._apply_custom_theme(current_theme)
            logger.debug("テーマ適用完了")
        except Exception as e:
            logger.error(f"テーマ適用エラー: {e}")
    
    def _apply_custom_theme(self, theme):
        """カスタムテーマ適用（サブクラスでオーバーライド）"""
        pass
    
    def on_theme_changed(self, theme_name):
        """テーマ変更時のハンドラ"""
        logger = logging.getLogger(__name__)
        logger.debug(f"テーマ変更: {theme_name}")
        self.apply_theme()
    
    def get_theme_color(self, color_key):
        """テーマカラーを取得"""
        try:
            return self.theme_engine.get_color(color_key)
        except Exception as e:
            logging.getLogger(__name__).error(f"テーマカラー取得エラー: {e}")
            return "#000000"  # デフォルト色
    
    def get_theme_style(self, style_key):
        """テーマスタイルを取得"""
        try:
            return self.theme_engine.get_style(style_key)
        except Exception as e:
            logging.getLogger(__name__).error(f"テーマスタイル取得エラー: {e}")
            return ""  # デフォルトスタイル
    
    # イベントハンドラメソッド（管理クラス連携実装）
    def _on_address_changed(self, new_path):
        """アドレスバーでパスが変更された時の処理"""
        logger = logging.getLogger(__name__)
        try:
            logger.debug(f"アドレス変更: {new_path}")
            
            # フォルダイベントハンドラがあれば委譲
            if self.folder_event_handler:
                self.folder_event_handler.on_address_changed(new_path)
            else:
                # 直接処理（フォルダハンドラ未設定時のフォールバック）
                logger.info(f"新しいパス: {new_path}")
                self.show_status_message(f"パス変更: {new_path}")
                
        except Exception as e:
            logger.error(f"アドレス変更処理エラー: {e}")
    
    def _on_parent_button_clicked(self):
        """親フォルダボタンがクリックされた時の処理"""
        logger = logging.getLogger(__name__)
        try:
            logger.debug("親フォルダボタンクリック")
            
            # フォルダイベントハンドラがあれば委譲
            if self.folder_event_handler:
                self.folder_event_handler.go_to_parent_folder()
            else:
                # 直接処理（フォルダハンドラ未設定時のフォールバック）
                logger.info("親フォルダへ移動")
                self.show_status_message("親フォルダへ移動")
                
        except Exception as e:
            logger.error(f"親フォルダボタン処理エラー: {e}")
