"""
リファクタリング統合テスト用の更新版メインウィンドウ

Phase 1 で作成した各種マネージャークラスとイベントハンドラを統合し、
実際に動作するバージョンを作成します。
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

# メインウィンドウコア
from presentation.views.functional_main_window.main_window_core import MainWindowCore

# UIマネージャー
from presentation.views.functional_main_window.ui_components.left_panel_manager import LeftPanelManager
from presentation.views.functional_main_window.ui_components.right_panel_manager import RightPanelManager

# イベントハンドラ
from presentation.views.functional_main_window.event_handlers.folder_event_handler import FolderEventHandler
from presentation.views.functional_main_window.event_handlers.image_event_handler import ImageEventHandler
from presentation.views.functional_main_window.event_handlers.theme_event_handler import ThemeEventHandler


class RefactoredMainWindowV2(MainWindowCore):
    """リファクタリング済みメインウィンドウ（実装版）"""
    
    def __init__(self):
        """リファクタリング済みメインウィンドウを初期化"""
        super().__init__()
        
        # 状態管理
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        self.maximized_state = None
        
        # コンポーネント管理
        self.ui_components = {}
        self.event_handlers = {}
        
        # 初期化
        self._initialize_components()
        self._setup_event_handlers()
        self._connect_signals()
        
        # ウィンドウ設定
        self.setWindowTitle("PhotoMap Explorer v2.2.0 (Refactored)")
        self.setGeometry(100, 100, 1200, 800)
        
        # 初期テーマ適用
        self._initialize_theme()
    
    def _initialize_components(self):
        """コンポーネントを初期化"""
        try:
            # UIマネージャーの初期化
            self.ui_components['left_panel'] = LeftPanelManager(self)
            self.ui_components['right_panel'] = RightPanelManager(self)
            
            # レイアウト構築
            self._build_layout()
            
        except Exception as e:
            print(f"コンポーネント初期化エラー: {e}")
    
    def _build_layout(self):
        """レイアウトを構築"""
        try:
            # 中央ウィジェット作成
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # メインレイアウト（水平）
            main_layout = QHBoxLayout(central_widget)
            main_layout.setContentsMargins(5, 5, 5, 5)
            main_layout.setSpacing(5)
            
            # 左パネル作成・追加
            left_panel = self.ui_components['left_panel'].create_panel()
            main_layout.addWidget(left_panel, 1)  # 比率1
            
            # 右パネル作成・追加
            right_panel = self.ui_components['right_panel'].create_panel()
            main_layout.addWidget(right_panel, 2)  # 比率2
            
        except Exception as e:
            print(f"レイアウト構築エラー: {e}")
    
    def _setup_event_handlers(self):
        """イベントハンドラを設定"""
        try:
            # イベントハンドラの初期化
            self.event_handlers['folder'] = FolderEventHandler(self)
            self.event_handlers['image'] = ImageEventHandler(self)
            self.event_handlers['theme'] = ThemeEventHandler(self)
            
            # コンポーネント参照を設定
            self._setup_handler_references()
            
        except Exception as e:
            print(f"イベントハンドラ設定エラー: {e}")
    
    def _setup_handler_references(self):
        """ハンドラにコンポーネント参照を設定"""
        try:
            # フォルダハンドラ
            folder_handler = self.event_handlers['folder']
            left_panel_mgr = self.ui_components['left_panel']
            
            if hasattr(left_panel_mgr, 'address_bar'):
                folder_handler.set_components(
                    left_panel_mgr.address_bar,
                    left_panel_mgr.folder_content_list,
                    left_panel_mgr.thumbnail_list
                )
            
            # 画像ハンドラ
            image_handler = self.event_handlers['image']
            right_panel_mgr = self.ui_components['right_panel']
            
            if hasattr(right_panel_mgr, 'preview_panel'):
                image_handler.set_components(
                    right_panel_mgr.preview_panel,
                    right_panel_mgr.map_panel
                )
            
            # テーマハンドラ（テーママネージャーは後で設定）
            # theme_handler = self.event_handlers['theme']
            # theme_handler.set_components(theme_manager)
            
        except Exception as e:
            print(f"ハンドラ参照設定エラー: {e}")
    
    def _connect_signals(self):
        """シグナルとスロットを接続"""
        try:
            # フォルダ関連のシグナル接続
            self._connect_folder_signals()
            
            # 画像関連のシグナル接続
            self._connect_image_signals()
            
            # UI関連のシグナル接続
            self._connect_ui_signals()
            
        except Exception as e:
            print(f"シグナル接続エラー: {e}")
    
    def _connect_folder_signals(self):
        """フォルダ関連のシグナルを接続"""
        try:
            left_panel_mgr = self.ui_components['left_panel']
            folder_handler = self.event_handlers['folder']
            
            # フォルダ選択ボタン
            if hasattr(left_panel_mgr, 'folder_button'):
                left_panel_mgr.folder_button.clicked.connect(folder_handler.select_folder)
            
            # フォルダ内容リスト
            if hasattr(left_panel_mgr, 'folder_content_list'):
                left_panel_mgr.folder_content_list.itemClicked.connect(
                    self.event_handlers['image'].on_folder_item_clicked
                )
                left_panel_mgr.folder_content_list.itemDoubleClicked.connect(
                    self.event_handlers['image'].on_folder_item_double_clicked
                )
            
            # サムネイルリスト
            if hasattr(left_panel_mgr, 'thumbnail_list'):
                if hasattr(left_panel_mgr.thumbnail_list, 'itemClicked'):
                    left_panel_mgr.thumbnail_list.itemClicked.connect(
                        self.event_handlers['image'].on_image_selected
                    )
            
        except Exception as e:
            print(f"フォルダシグナル接続エラー: {e}")
    
    def _connect_image_signals(self):
        """画像関連のシグナルを接続"""
        try:
            right_panel_mgr = self.ui_components['right_panel']
            
            # プレビューパネルのダブルクリック
            if hasattr(right_panel_mgr, 'preview_panel') and hasattr(right_panel_mgr.preview_panel, 'mouseDoubleClickEvent'):
                # ダブルクリックハンドラを設定（実装が必要）
                pass
            
            # マップパネルのダブルクリック
            if hasattr(right_panel_mgr, 'map_panel') and hasattr(right_panel_mgr.map_panel, 'mouseDoubleClickEvent'):
                # ダブルクリックハンドラを設定（実装が必要）
                pass
            
        except Exception as e:
            print(f"画像シグナル接続エラー: {e}")
    
    def _connect_ui_signals(self):
        """UI関連のシグナルを接続"""
        try:
            # テーマ切り替えやその他のUIイベント
            # TODO: テーマ切り替えボタンなどがあれば接続
            pass
            
        except Exception as e:
            print(f"UIシグナル接続エラー: {e}")
    
    def _initialize_theme(self):
        """テーマの初期化"""
        try:
            theme_handler = self.event_handlers['theme']
            theme_handler.initialize_theme()
            
        except Exception as e:
            print(f"テーマ初期化エラー: {e}")
    
    def show_status_message(self, message):
        """ステータスメッセージを表示"""
        try:
            print(f"[STATUS] {message}")
            
            # ステータスバーがあれば表示
            if hasattr(self, 'statusBar'):
                status_bar = self.statusBar()
                if status_bar:
                    status_bar.showMessage(message, 3000)  # type: ignore
            
        except Exception as e:
            print(f"ステータス表示エラー: {e}")
    
    # 公開メソッド（互換性のため）
    def select_folder(self):
        """フォルダ選択（外部から呼び出し可能）"""
        if 'folder' in self.event_handlers:
            self.event_handlers['folder'].select_folder()
    
    def load_folder(self, folder_path):
        """フォルダ読み込み（外部から呼び出し可能）"""
        if 'folder' in self.event_handlers:
            self.event_handlers['folder'].load_folder(folder_path)
    
    def display_image(self, image_path):
        """画像表示（外部から呼び出し可能）"""
        if 'image' in self.event_handlers:
            self.event_handlers['image'].display_image(image_path)
    
    def change_theme(self, theme_name):
        """テーマ変更（外部から呼び出し可能）"""
        if 'theme' in self.event_handlers:
            self.event_handlers['theme'].on_theme_changed(theme_name)


def main():
    """テストアプリケーション実行"""
    try:
        # アプリケーション作成
        app = QApplication(sys.argv)
        
        # メインウィンドウ作成・表示
        window = RefactoredMainWindowV2()
        window.show()
        
        # ログ出力
        print("RefactoredMainWindowV2 が正常に起動しました")
        print("フォルダ選択、画像表示、テーマ変更などの機能をテストしてください")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
