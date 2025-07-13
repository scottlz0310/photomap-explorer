"""
Refactored Functional Main Window

リファクタリング後の新UIメインウィンドウ
"""

from .main_window_core import MainWindowCore
from .ui_components.left_panel_manager import LeftPanelManager
from .ui_components.right_panel_manager import RightPanelManager
from .event_handlers.folder_event_handler import FolderEventHandler
from .event_handlers.theme_event_handler import ThemeEventHandler
from .event_handlers.image_event_handler import ImageEventHandler
from utils.debug_logger import debug, info, warning, error, verbose


class RefactoredFunctionalMainWindow(MainWindowCore):
    """
    リファクタリング後の機能的メインウィンドウ
    
    各種管理クラスを組み合わせて完全な機能を提供
    """
    
    def __init__(self):
        super().__init__()
        
        # 管理クラスの初期化
        self._initialize_managers()
        
        # 管理クラスの設定
        self._setup_managers_complete()
        
        # 初期化の完了
        self._finalize_initialization()
    
    def _initialize_managers(self):
        """管理クラスを初期化"""
        # UI コンポーネント管理
        self.left_panel_mgr = LeftPanelManager(self)
        self.right_panel_mgr = RightPanelManager(self)
        
        # TODO: 以下の管理クラスを後で実装
        self.address_bar_mgr = None  # AddressBarManager(self)
        # MaximizeHandler（最大化機能）
        from .ui_components.maximize_handler import MaximizeHandler
        self.maximize_hdlr = MaximizeHandler(self)
        
        # イベントハンドラ（実装済みを使用）
        try:
            self.folder_event_hdlr = FolderEventHandler(self)
            self.theme_event_hdlr = ThemeEventHandler(self)
            self.image_event_hdlr = ImageEventHandler(self)
            
            # テーマエンジンを設定（新しい統合テーママネージャー使用）
            from presentation.themes.integrated_theme_manager import get_theme_manager
            
            debug("テーマエンジン初期化開始")
            
            # 統合テーママネージャーを取得
            self.theme_manager = get_theme_manager()
            
            # テーマイベントハンドラーに設定
            self.theme_event_hdlr.set_components(self.theme_manager)
            debug("テーマエンジン初期化完了")
            
        except Exception as e:
            error(f"イベントハンドラー初期化エラー: {e}")
            # フォールバック: None設定
            self.folder_event_hdlr = None
            self.theme_event_hdlr = None
            self.image_event_hdlr = None
        
        # 表示管理
        self.image_display_mgr = None    # ImageDisplayManager(self)
        
        # MapDisplayManagerを実際に初期化
        try:
            from .display_managers.map_display_manager import MapDisplayManager
            self.map_display_mgr = MapDisplayManager(self)
            verbose("MapDisplayManager初期化成功")
        except Exception as e:
            error(f"MapDisplayManager初期化エラー: {e}")
            self.map_display_mgr = None
        
        # StatusDisplayManagerを実際に初期化
        try:
            from .display_managers.status_display_manager import StatusDisplayManager
            self.status_display_mgr = StatusDisplayManager(self)
            verbose("StatusDisplayManager初期化成功")
        except Exception as e:
            error(f"StatusDisplayManager初期化エラー: {e}")
            import traceback
            traceback.print_exc()
            self.status_display_mgr = None
    
    def _setup_managers_complete(self):
        """管理クラスの完全設定"""
        debug("_setup_managers_complete 開始")
        
        # 基本的なUI構築
        self.setup_managers(
            self.left_panel_mgr,
            self.right_panel_mgr,
            self.address_bar_mgr,
            self.maximize_hdlr,
            self.folder_event_hdlr,
            self.image_event_hdlr,
            self.theme_event_hdlr,
            self.image_display_mgr,
            self.map_display_mgr,
            self.status_display_mgr
        )
        
        debug("setup_managers 完了")
        
        # 暫定的なイベントハンドラ設定（完全版まで）
        # self._setup_temporary_handlers()  # コメントアウト：main_window_coreで設定される
    
    def _setup_temporary_handlers(self):
        """暫定的なイベントハンドラ設定"""
        # TODO: 完全なイベントハンドラが実装されるまでの暫定処理
        
        # 左パネルのイベント
        if self.left_panel_mgr:
            self.left_panel_mgr.set_event_handlers(
                self._on_folder_item_clicked,
                self._on_folder_item_double_clicked,
                self._on_image_selected
            )
        
        # 右パネルのイベント  
        if self.right_panel_mgr:
            self.right_panel_mgr.set_event_handlers(
                self._toggle_image_maximize,
                self._toggle_map_maximize
            )
    
    def _setup_temporary_handlers(self):
        """暫定的なイベントハンドラ設定"""
        # TODO: 完全なイベントハンドラが実装されるまでの暫定処理
        
        # 左パネルのイベント
        if self.left_panel_mgr:
            self.left_panel_mgr.set_event_handlers(
                self._on_folder_item_clicked,
                self._on_folder_item_double_clicked,
                self._on_image_selected
            )
        
        # 右パネルのイベント  
        if self.right_panel_mgr:
            self.right_panel_mgr.set_event_handlers(
                self._toggle_image_maximize,
                self._toggle_map_maximize
            )
    
    def _finalize_initialization(self):
        """初期化の最終処理"""
        # テーマ設定の完了
        self.finalize_setup()
        
        # メインウィンドウ表示は main_window_core.py で処理される
        debug("メインウィンドウ表示完了")
        
        # 初期データの読み込み
        # TODO: 初期フォルダ読み込み
        # TODO: 初期マップ画面表示
    
    # 暫定的なイベントハンドラメソッド（後で専用クラスに移動）
    def _on_folder_item_clicked(self, item):
        """フォルダ項目クリック（暫定）"""
        verbose(f"フォルダ項目クリック: {item.text()}")
        # 実際の処理: フォルダイベントハンドラーに委譲
        if self.folder_event_hdlr:
            try:
                # アイテムのデータを取得してフォルダ変更を実行
                folder_path = item.data(256)  # Qt.UserRole = 256
                if folder_path and folder_path != item.text():
                    self.folder_event_hdlr.load_folder(folder_path)
            except Exception as e:
                error(f"フォルダ項目クリック処理エラー: {e}")
    
    def _on_folder_item_double_clicked(self, item):
        """フォルダ項目ダブルクリック（暫定）"""
        verbose(f"フォルダ項目ダブルクリック: {item.text()}")
        # 実際の処理: フォルダイベントハンドラーに委譲
        if self.folder_event_hdlr:
            try:
                # アイテムのデータを取得してフォルダ変更を実行
                folder_path = item.data(256)  # Qt.UserRole = 256
                if folder_path:
                    self.folder_event_hdlr.load_folder(folder_path)
            except Exception as e:
                error(f"フォルダ項目ダブルクリック処理エラー: {e}")
    
    def _on_image_selected(self, image_path):
        """画像選択（暫定）"""
        verbose(f"画像選択: {image_path}")
        # 実際の処理: 画像イベントハンドラーに委譲
        if self.image_event_hdlr:
            try:
                # 画像パスが文字列の場合はQListWidgetItemオブジェクトを作る必要がある
                if isinstance(image_path, str):
                    from PyQt5.QtWidgets import QListWidgetItem
                    item = QListWidgetItem()
                    item.setData(256, image_path)  # Qt.UserRole = 256
                    self.image_event_hdlr.on_image_selected(item)
                else:
                    # 既にQListWidgetItemの場合
                    self.image_event_hdlr.on_image_selected(image_path)
            except Exception as e:
                error(f"画像選択処理エラー: {e}")
    
    def _toggle_image_maximize(self):
        """画像最大化切り替え（暫定）"""
        debug("画像最大化切り替え")
        if self.maximize_hdlr:
            self.maximize_hdlr.toggle_image_maximize()
        else:
            warning("MaximizeHandlerが初期化されていません")
    
    def _toggle_map_maximize(self):
        """マップ最大化切り替え（暫定）"""
        debug("マップ最大化切り替え")
        if self.maximize_hdlr:
            self.maximize_hdlr.toggle_map_maximize()
        else:
            warning("MaximizeHandlerが初期化されていません")
