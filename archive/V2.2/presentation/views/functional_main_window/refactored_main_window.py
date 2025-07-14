"""
Refactored Functional Main Window

リファクタリング後の新UIメインウィンドウ
"""

from .main_window_core import MainWindowCore
from .ui_components.left_panel_manager import LeftPanelManager
from .ui_components.right_panel_manager import RightPanelManager


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
        self.maximize_hdlr = None    # MaximizeHandler(self)
        
        # イベントハンドラ
        self.folder_event_hdlr = None    # FolderEventHandler(self)
        self.image_event_hdlr = None     # ImageEventHandler(self)
        self.theme_event_hdlr = None     # ThemeEventHandler(self)
        
        # 表示管理
        self.image_display_mgr = None    # ImageDisplayManager(self)
        self.map_display_mgr = None      # MapDisplayManager(self)
        self.status_display_mgr = None   # StatusDisplayManager(self)
    
    def _setup_managers_complete(self):
        """管理クラスの完全設定"""
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
        
        # 暫定的なイベントハンドラ設定（完全版まで）
        self._setup_temporary_handlers()
    
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
        
        # 初期データの読み込み
        # TODO: 初期フォルダ読み込み
        # TODO: 初期マップ画面表示
    
    # 暫定的なイベントハンドラメソッド（後で専用クラスに移動）
    def _on_folder_item_clicked(self, item):
        """フォルダ項目クリック（暫定）"""
        print(f"フォルダ項目クリック: {item.text()}")
    
    def _on_folder_item_double_clicked(self, item):
        """フォルダ項目ダブルクリック（暫定）"""
        print(f"フォルダ項目ダブルクリック: {item.text()}")
    
    def _on_image_selected(self, image_path):
        """画像選択（暫定）"""
        print(f"画像選択: {image_path}")
    
    def _toggle_image_maximize(self):
        """画像最大化切り替え（暫定）"""
        print("画像最大化切り替え")
    
    def _toggle_map_maximize(self):
        """マップ最大化切り替え（暫定）"""
        print("マップ最大化切り替え")
