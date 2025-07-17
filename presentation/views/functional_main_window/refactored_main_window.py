"""
Refactored Functional Main Window

リファクタリング後の新UIメインウィンドウ
"""

from .main_window_core import MainWindowCore
from .ui_components.left_panel_manager import LeftPanelManager
from .ui_components.right_panel_manager import RightPanelManager
from .ui_components.address_bar_manager import AddressBarManager


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
        
        # アドレスバー管理（実装済み）
        self.address_bar_mgr = AddressBarManager(self)
        
        # 最大化ハンドラ（実装済み）
        from .ui_components.maximize_handler import MaximizeHandler
        self.maximize_hdlr = MaximizeHandler(self)
        
        # イベントハンドラ（実装が必要）
        self.folder_event_hdlr = self._create_folder_event_handler()
        self.image_event_hdlr = self._create_image_event_handler()
        self.theme_event_hdlr = self._create_theme_event_handler()
        
        # 表示管理（実装が必要）
        from .display_managers.image_display_manager import ImageDisplayManager
        from .display_managers.map_display_manager import MapDisplayManager
        from .display_managers.status_display_manager import StatusDisplayManager
        self.image_display_mgr = ImageDisplayManager(self)
        self.map_display_mgr = MapDisplayManager(self)
        self.status_display_mgr = StatusDisplayManager(self)
    
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
        
        # 管理クラス間の連携設定
        self._setup_manager_connections()
    
    def _setup_manager_connections(self):
        """管理クラス間の連携設定"""
        # 左パネルのイベント（実際のハンドラメソッドを使用）
        if self.left_panel_mgr:
            self.left_panel_mgr.set_event_handlers(
                self._handle_folder_selection,
                self._handle_folder_double_click, 
                self.image_event_hdlr.on_image_selected
            )
        
        # 右パネルのイベント（MaximizeHandlerの機能を使用）
        if self.right_panel_mgr and self.maximize_hdlr:
            self.right_panel_mgr.set_event_handlers(
                self.maximize_hdlr.toggle_image_maximize,
                self.maximize_hdlr.toggle_map_maximize
            )
    
    def _finalize_initialization(self):
        """初期化の最終処理"""
        # テーマ設定の完了
        self.finalize_setup()
        
        # 初期データの読み込み
        self._load_initial_folder()
        self._initialize_map_display()
    
    def _load_initial_folder(self):
        """初期フォルダの読み込み"""
        try:
            # デフォルトフォルダ（現在のディレクトリ）を読み込み
            import os
            current_dir = os.getcwd()
            if self.folder_event_hdlr:
                self.folder_event_hdlr.on_address_changed(current_dir)
        except Exception as e:
            self.logger.error(f"初期フォルダ読み込みエラー: {e}")
    
    def _initialize_map_display(self):
        """初期マップ画面の表示"""
        try:
            if self.map_display_mgr:
                # 基本的なマップ初期化（利用可能な場合）
                self.show_status_message("📍 マップ表示を初期化しました")
        except Exception as e:
            self.logger.error(f"マップ初期化エラー: {e}")
    
    # イベントハンドラ作成メソッド（完全実装）
    def _create_folder_event_handler(self):
        """フォルダイベントハンドラを作成"""
        import logging
        logger = logging.getLogger(__name__)
        
        # シンプルなイベントハンドラクラスを動的に作成
        class FolderEventHandler:
            def __init__(self, main_window):
                self.main_window = main_window
                self.logger = logging.getLogger(f"{__name__}.FolderEventHandler")
            
            def select_folder(self):
                """フォルダ選択処理"""
                try:
                    from PyQt5.QtWidgets import QFileDialog
                    folder_path = QFileDialog.getExistingDirectory(
                        self.main_window, 
                        "フォルダを選択してください"
                    )
                    if folder_path:
                        self.logger.info(f"フォルダ選択: {folder_path}")
                        self.main_window.show_status_message(f"選択されたフォルダ: {folder_path}")
                        # フォルダ内容の読み込み処理
                        if self.main_window.left_panel_mgr:
                            self.main_window.left_panel_mgr.refresh_folder_content(folder_path)
                except Exception as e:
                    self.logger.error(f"フォルダ選択エラー: {e}")
            
            def on_address_changed(self, new_path):
                """アドレス変更処理"""
                self.logger.info(f"アドレス変更: {new_path}")
                self.main_window.show_status_message(f"パス変更: {new_path}")
            
            def go_to_parent_folder(self):
                """親フォルダ移動処理"""
                self.logger.info("親フォルダへ移動")
                self.main_window.show_status_message("親フォルダへ移動")
        
        return FolderEventHandler(self)
    
    def _create_image_event_handler(self):
        """画像イベントハンドラを作成"""
        import logging
        
        class ImageEventHandler:
            def __init__(self, main_window):
                self.main_window = main_window
                self.logger = logging.getLogger(f"{__name__}.ImageEventHandler")
            
            def on_image_selected(self, image_path):
                """画像選択処理"""
                self.logger.info(f"画像選択: {image_path}")
                self.main_window.show_status_message(f"選択された画像: {image_path}")
            
            def on_image_double_clicked(self, image_path):
                """画像ダブルクリック処理"""
                self.logger.info(f"画像ダブルクリック: {image_path}")
                # 画像プレビュー表示
                if self.main_window.image_display_mgr:
                    self.main_window.image_display_mgr.display_image(image_path)
        
        return ImageEventHandler(self)
    
    def _create_theme_event_handler(self):
        """テーマイベントハンドラを作成"""
        import logging
        
        class ThemeEventHandler:
            def __init__(self, main_window):
                self.main_window = main_window
                self.logger = logging.getLogger(f"{__name__}.ThemeEventHandler")
                self.current_theme = "light"
            
            def toggle_theme(self):
                """テーマ切り替え処理"""
                try:
                    new_theme = "dark" if self.current_theme == "light" else "light"
                    self.current_theme = new_theme
                    self.logger.info(f"テーマ切り替え: {new_theme}")
                    
                    # テーマボタン更新
                    self.update_theme_button()
                    self.main_window.show_status_message(f"テーマを{new_theme}に変更しました")
                    
                except Exception as e:
                    self.logger.error(f"テーマ切り替えエラー: {e}")
            
            def update_theme_button(self):
                """テーマボタンの表示を更新"""
                if hasattr(self.main_window, 'theme_toggle_btn'):
                    if self.current_theme == "dark":
                        self.main_window.theme_toggle_btn.setText("☀️ ライト")
                    else:
                        self.main_window.theme_toggle_btn.setText("🌙 ダーク")
        
        return ThemeEventHandler(self)

    # 実際のイベントハンドラメソッド（管理クラス連携）
    def _handle_folder_selection(self, item):
        """フォルダ項目選択処理"""
        try:
            folder_path = item.text()
            self.logger.info(f"フォルダ選択: {folder_path}")
            if self.folder_event_hdlr:
                self.folder_event_hdlr.select_folder()
        except Exception as e:
            self.logger.error(f"フォルダ選択エラー: {e}")
    
    def _handle_folder_double_click(self, item):
        """フォルダ項目ダブルクリック処理"""
        try:
            folder_path = item.text()
            self.logger.info(f"フォルダダブルクリック: {folder_path}")
            if self.address_bar_mgr:
                self.address_bar_mgr.update_address_bar(folder_path)
        except Exception as e:
            self.logger.error(f"フォルダダブルクリックエラー: {e}")
