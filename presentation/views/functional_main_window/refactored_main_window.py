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
        
        # アドレスバー管理クラスを初期化
        from .ui_components.address_bar_manager import AddressBarManager
        self.address_bar_mgr = AddressBarManager(self)
        
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
        
        # 表示管理マネージャーを初期化
        try:
            from .display_managers.image_display_manager import ImageDisplayManager
            self.image_display_mgr = ImageDisplayManager(self)
            verbose("ImageDisplayManager初期化成功")
        except Exception as e:
            error(f"ImageDisplayManager初期化エラー: {e}")
            self.image_display_mgr = None
        
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
        
        # イベントハンドラの最終設定
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """イベントハンドラーの設定"""
        debug("イベントハンドラー設定開始")
        
        # 左パネルのイベント設定
        if self.left_panel_mgr and hasattr(self.left_panel_mgr, 'set_event_handlers'):
            self.left_panel_mgr.set_event_handlers(
                self._on_folder_item_clicked,
                self._on_folder_item_double_clicked,
                self._on_image_selected
            )
            debug("左パネルイベントハンドラー設定完了")
        
        # 右パネルのイベント設定
        if self.right_panel_mgr and hasattr(self.right_panel_mgr, 'set_event_handlers'):
            self.right_panel_mgr.set_event_handlers(
                self._toggle_image_maximize,
                self._toggle_map_maximize
            )
            debug("右パネルイベントハンドラー設定完了")

    def _finalize_initialization(self):
        """初期化の最終処理"""
        # テーマ設定の完了
        self.finalize_setup()
        
        # メインウィンドウ表示は main_window_core.py で処理される
        debug("メインウィンドウ表示完了")
        
        # 初期データの読み込み
        self._load_initial_data()
    
    def _load_initial_data(self):
        """初期データの読み込み"""
        try:
            # 初期フォルダ読み込み（assets フォルダを使用）
            import os
            assets_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "assets")
            if os.path.exists(assets_path) and self.folder_event_hdlr:
                self.folder_event_hdlr.load_folder(assets_path)
                debug(f"初期フォルダ読み込み完了: {assets_path}")
            else:
                debug("assetsフォルダが見つからないか、フォルダイベントハンドラーが未初期化")
                
        except Exception as e:
            warning(f"初期データ読み込みエラー: {e}")

    # イベントハンドラメソッド
    def _on_folder_item_clicked(self, item):
        """フォルダ項目クリック"""
        try:
            verbose(f"フォルダ項目クリック: {item.text()}")
            
            # Qt のイベント処理を実行
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            # アイテムのデータを取得
            item_path = item.data(256)  # Qt.UserRole = 256
            if not item_path:
                debug("アイテムパスが無効")
                return
            
            import os
            debug(f"アイテムパス: {item_path}")
            debug(f"パス存在確認: {os.path.exists(item_path)}")
            debug(f"ディレクトリ判定: {os.path.isdir(item_path)}")
            debug(f"ファイル判定: {os.path.isfile(item_path)}")
            
            # パスの種類によって処理を分岐
            if os.path.isdir(item_path):
                # ディレクトリの場合：フォルダ読み込み
                debug(f"フォルダに移動: {item_path}")
                if self.folder_event_hdlr:
                    # より長い遅延時間で実行（UI更新とメモリ安全性のため）
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(100, lambda: self._safe_load_folder(item_path))
                else:
                    warning("フォルダイベントハンドラーが未初期化")
                    
            elif os.path.isfile(item_path):
                # ファイルの場合：画像選択処理
                debug(f"ファイル選択: {item_path}")
                # 画像ファイルかどうかチェック
                image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
                file_ext = os.path.splitext(item_path)[1].lower()
                
                if file_ext in image_extensions:
                    # 画像ファイルの場合：画像選択
                    self._on_image_selected(item)
                else:
                    # その他のファイルの場合：何もしない（またはファイル表示）
                    debug(f"非画像ファイル: {item_path}")
                    self.show_status_message(f"📄 ファイル: {os.path.basename(item_path)}")
            else:
                warning(f"不明なパスタイプ: {item_path}")
                
        except Exception as e:
            error(f"フォルダ項目クリック処理エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _safe_load_folder(self, folder_path):
        """安全なフォルダ読み込み"""
        try:
            import os
            # パス検証
            if not folder_path or not os.path.exists(folder_path):
                warning(f"無効なフォルダパス: {folder_path}")
                return
                
            if not os.path.isdir(folder_path):
                warning(f"ディレクトリではありません: {folder_path}")
                return
                
            # 読み取り権限チェック
            if not os.access(folder_path, os.R_OK):
                error(f"読み取り権限がありません: {folder_path}")
                if hasattr(self, 'show_status_message'):
                    self.show_status_message(f"❌ アクセス権限エラー: {os.path.basename(folder_path)}")
                return
            
            debug(f"安全フォルダ読み込み開始: {folder_path}")
            
            # フォルダイベントハンドラーの存在確認
            if not self.folder_event_hdlr:
                error("フォルダイベントハンドラーが初期化されていません")
                return
                
            # UIの安全性のためイベント処理
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            # フォルダ読み込み実行
            self.folder_event_hdlr.load_folder(folder_path)
            debug(f"安全フォルダ読み込み完了: {folder_path}")
            
        except PermissionError as pe:
            error(f"アクセス権限エラー: {pe}")
            if hasattr(self, 'show_status_message'):
                self.show_status_message(f"❌ アクセス権限エラー")
        except OSError as oe:
            error(f"OSエラー: {oe}")
            if hasattr(self, 'show_status_message'):
                self.show_status_message(f"❌ システムエラー")
        except Exception as e:
            error(f"安全フォルダ読み込みエラー: {e}")
            import traceback
            traceback.print_exc()
            # show_status_message メソッドの存在確認
            if hasattr(self, 'show_status_message'):
                self.show_status_message(f"❌ フォルダ読み込みエラー: {e}")
            else:
                warning(f"ステータスメッセージ表示不可: {e}")

    def _on_folder_item_double_clicked(self, item):
        """フォルダ項目ダブルクリック"""
        try:
            verbose(f"フォルダ項目ダブルクリック: {item.text()}")
            
            # Qt のイベント処理を実行
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            # アイテムのデータを取得
            item_path = item.data(256)  # Qt.UserRole = 256
            if not item_path:
                debug("アイテムパスが無効")
                return
            
            import os
            debug(f"ダブルクリック - アイテムパス: {item_path}")
            
            # パスの種類によって処理を分岐
            if os.path.isdir(item_path):
                # ディレクトリの場合：フォルダ読み込み
                debug(f"フォルダに移動（ダブルクリック）: {item_path}")
                if self.folder_event_hdlr:
                    # より長い遅延時間で実行（UI更新とメモリ安全性のため）
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(100, lambda: self._safe_load_folder(item_path))
                else:
                    warning("フォルダイベントハンドラーが未初期化")
                    
            elif os.path.isfile(item_path):
                # ファイルの場合：画像選択処理（ダブルクリックでは最大化も検討）
                debug(f"ファイル選択（ダブルクリック）: {item_path}")
                # 画像ファイルかどうかチェック
                image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
                file_ext = os.path.splitext(item_path)[1].lower()
                
                if file_ext in image_extensions:
                    # 画像ファイルの場合：画像選択 + 最大化
                    self._on_image_selected(item)
                    # ダブルクリックの場合は画像を最大化表示
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(200, self._toggle_image_maximize)
                else:
                    # その他のファイルの場合：何もしない
                    debug(f"非画像ファイル（ダブルクリック）: {item_path}")
            else:
                warning(f"不明なパスタイプ（ダブルクリック）: {item_path}")
                
        except Exception as e:
            error(f"フォルダ項目ダブルクリック処理エラー: {e}")
            import traceback
            traceback.print_exc()
    
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
