"""
Refactored Functional Main Window

リファクタリング後の新UIメインウィンドウ
"""

import os
import logging
from .main_window_core import MainWindowCore
from .ui_components.left_panel_manager import LeftPanelManager
from .ui_components.right_panel_manager import RightPanelManager
from .ui_components.address_bar_manager import AddressBarManager
from .ui_components.maximize_handler import MaximizeHandler
from .event_handlers.folder_event_handler import FolderEventHandler
from .event_handlers.image_event_handler import ImageEventHandler
from .event_handlers.theme_event_handler import ThemeEventHandler
from .display_managers.image_display_manager import ImageDisplayManager
from .display_managers.map_display_manager import MapDisplayManager
from .display_managers.status_display_manager import StatusDisplayManager


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
        try:
            # UI コンポーネント管理
            self.left_panel_mgr = LeftPanelManager(self)
            self.right_panel_mgr = RightPanelManager(self)
            self.address_bar_mgr = AddressBarManager(self)
            self.maximize_hdlr = MaximizeHandler(self)
            
            # イベントハンドラ
            self.folder_event_hdlr = FolderEventHandler(self)
            self.image_event_hdlr = ImageEventHandler(self)
            self.theme_event_hdlr = ThemeEventHandler(self)
            
            # 表示管理
            self.image_display_mgr = ImageDisplayManager(self)
            self.map_display_mgr = MapDisplayManager(self)
            self.status_display_mgr = StatusDisplayManager(self)
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"管理クラス初期化エラー: {e}")
            # フォールバック: 最小構成
            self.left_panel_mgr = LeftPanelManager(self)
            self.right_panel_mgr = RightPanelManager(self)
            self.address_bar_mgr = None
            self.maximize_hdlr = None
            self.folder_event_hdlr = None
            self.image_event_hdlr = None
            self.theme_event_hdlr = None
            self.image_display_mgr = None
            self.map_display_mgr = None
            self.status_display_mgr = None
    
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
        
        # イベントハンドラの設定
        self._setup_event_handlers()
    
    def _setup_event_handlers(self):
        """イベントハンドラを設定"""
        # 左パネルのイベント（適切なハンドラに委譲）
        if self.left_panel_mgr and self.folder_event_hdlr and self.image_event_hdlr:
            logging.info(f"🔍 set_event_handlers呼び出し開始")
            logging.info(f"🔍 image_event_hdlr.on_image_selected: {self.image_event_hdlr.on_image_selected}")
            self.left_panel_mgr.set_event_handlers(
                self.folder_event_hdlr.on_folder_item_clicked,
                self.folder_event_hdlr.on_folder_item_double_clicked,
                self.image_event_hdlr.on_image_selected
            )
            logging.info(f"🔍 set_event_handlers呼び出し完了")
        
        # イベントハンドラにコンポーネント参照を設定
        if self.folder_event_hdlr:
            self.folder_event_hdlr.set_components(
                getattr(self, 'address_bar', None),
                getattr(self, 'folder_content_list', None),
                getattr(self.left_panel_mgr, 'thumbnail_list', None) if self.left_panel_mgr else None
            )
        
        if self.image_event_hdlr:
            self.image_event_hdlr.set_components(
                getattr(self, 'preview_panel', None),
                getattr(self, 'map_panel', None)
            )
        
        # 右パネルのイベント（適切なハンドラに委譲）
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
        # TODO: 初期フォルダ読み込み
        # TODO: 初期マップ画面表示
    
    # 暫定的なイベントハンドラメソッド（後で専用クラスに移動）
    def _on_folder_item_clicked(self, item):
        """フォルダ項目クリック（暫定）"""
        from utils.debug_logger import debug
        debug(f"フォルダ項目クリック: {item.text()}")
    
    def _on_folder_item_double_clicked(self, item):
        """フォルダ項目ダブルクリック（暫定）"""
        from utils.debug_logger import debug
        debug(f"フォルダ項目ダブルクリック: {item.text()}")
    
    def _on_image_selected(self, image_path):
        """画像選択時の処理"""
        try:
            from utils.debug_logger import debug, info, error
            debug(f"画像選択処理開始: {image_path}")
            
            if not image_path or not os.path.exists(image_path):
                error(f"無効な画像パス: {image_path}")
                return
            
            # 画像プレビューを更新
            if hasattr(self, 'preview_panel') and self.preview_panel:
                debug("プレビューパネル更新中...")
                if hasattr(self.preview_panel, 'display_image'):
                    self.preview_panel.display_image(image_path)
                    info(f"プレビュー更新完了: {os.path.basename(image_path)}")
                else:
                    debug("プレビューパネルにdisplay_imageメソッドがありません")
            else:
                error("プレビューパネルが見つかりません")
            
            # マップ表示を更新
            if hasattr(self, 'map_panel') and self.map_panel:
                debug("マップパネル更新中...")
                self._update_map_display(image_path)
            else:
                error("マップパネルが見つかりません")
                
            # ステータス情報を更新
            if hasattr(self, 'status_info') and self.status_info:
                debug("ステータス情報更新中...")
                self._update_image_status(image_path)
            
            info(f"画像選択処理完了: {os.path.basename(image_path)}")
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"画像選択エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_map_display(self, image_path):
        """マップ表示を更新"""
        try:
            from utils.debug_logger import debug, info, error
            from logic.image_utils import extract_gps_coords
            
            debug(f"GPS情報取得中: {image_path}")
            gps_info = extract_gps_coords(image_path)
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                debug(f"GPS座標取得: {lat}, {lon}")
                
                # マップパネルの更新
                if self.map_panel and hasattr(self.map_panel, 'update_location'):
                    success = self.map_panel.update_location(lat, lon)
                    if success:
                        info(f"マップ更新成功: {lat:.6f}, {lon:.6f}")
                    else:
                        error("マップ更新に失敗")
                elif self.map_panel and hasattr(self.map_panel, 'setHtml'):
                    # WebViewの場合
                    html_content = self._generate_map_html(lat, lon, image_path)
                    self.map_panel.setHtml(html_content)
                    info(f"マップHTML更新: {lat:.6f}, {lon:.6f}")
                else:
                    error("マップパネルに更新メソッドがありません")
            else:
                debug("GPS情報が見つかりません")
                # GPS情報がない場合の表示
                if self.map_panel and hasattr(self.map_panel, 'setHtml'):
                    no_gps_html = self._generate_no_gps_html(image_path)
                    self.map_panel.setHtml(no_gps_html)
                    info("GPS情報なしのマップ表示")
                    
        except Exception as e:
            from utils.debug_logger import error
            error(f"マップ表示更新エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _generate_map_html(self, lat, lon, image_path):
        """マップ表示用のHTMLを生成"""
        import os
        filename = os.path.basename(image_path)
        return f"""
        <html>
        <body style="margin: 0; padding: 20px; font-family: Arial;">
            <div style="text-align: center;">
                <h3 style="color: #2196F3; margin-top: 0;">📍 GPS座標情報</h3>
                <p style="margin: 10px 0;"><strong>緯度:</strong> {lat:.6f}</p>
                <p style="margin: 10px 0;"><strong>経度:</strong> {lon:.6f}</p>
                <p style="margin: 10px 0; color: #666;"><strong>画像:</strong> {filename}</p>
                <div style="margin-top: 15px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
                    <small style="color: #666;">GPS座標が含まれています</small>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _generate_no_gps_html(self, image_path):
        """GPS情報なし表示用のHTMLを生成"""
        import os
        filename = os.path.basename(image_path)
        return f"""
        <html>
        <body style="margin: 0; padding: 20px; font-family: Arial;">
            <div style="text-align: center;">
                <h3 style="color: #666; margin-top: 0;">📍 位置情報</h3>
                <p style="color: #999; margin: 15px 0;">この画像にはGPS座標が含まれていません。</p>
                <p style="margin: 10px 0; color: #666;"><strong>画像:</strong> {filename}</p>
                <div style="margin-top: 20px; padding: 10px; background: #f5f5f5; border-radius: 5px;">
                    <small style="color: #999;">位置情報付きの画像を選択してください</small>
                </div>
            </div>
        </body>
        </html>
        """
    
    def _update_image_status(self, image_path):
        """画像ステータス情報を更新"""
        try:
            from utils.debug_logger import debug
            import os
            from datetime import datetime
            from PyQt5.QtGui import QPixmap
            
            if not os.path.exists(image_path):
                return
                
            # ファイル情報取得
            stat = os.stat(image_path)
            file_size = stat.st_size
            modified_time = datetime.fromtimestamp(stat.st_mtime)
            
            # 画像サイズ取得
            try:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    dimensions_str = f"{pixmap.width()} x {pixmap.height()}"
                else:
                    dimensions_str = "不明"
            except:
                dimensions_str = "不明"
            
            # ステータス文字列作成
            status_text = f"""📋 画像詳細情報

📁 ファイル名: {os.path.basename(image_path)}
📏 サイズ: {file_size:,} bytes
📐 解像度: {dimensions_str}
📅 更新日時: {modified_time.strftime('%Y-%m-%d %H:%M:%S')}
📂 フォルダ: {os.path.dirname(image_path)}"""

            self.status_info.setText(status_text)
            debug("ステータス情報更新完了")
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"ステータス情報更新エラー: {e}")
    
    def _toggle_image_maximize(self):
        """画像最大化切り替え（暫定）"""
        from utils.debug_logger import debug
        debug("画像最大化切り替え")
    
    def _toggle_map_maximize(self):
        """マップ最大化切り替え（暫定）"""
        from utils.debug_logger import debug
        debug("マップ最大化切り替え")
    
    def load_folder(self, folder_path):
        """フォルダを読み込み"""
        if hasattr(self, 'folder_event_hdlr') and self.folder_event_hdlr:
            self.folder_event_hdlr.load_folder(folder_path)
        else:
            from utils.debug_logger import warning
            warning(f"フォルダイベントハンドラが見つかりません: {folder_path}")
