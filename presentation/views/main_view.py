"""
メインビュー（メインウィンドウのビュー層）
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QSplitter, QWidget, 
                            QStatusBar, QHBoxLayout, QPushButton, QStackedLayout)
from PyQt5.QtCore import Qt, QDir, pyqtSignal
from PyQt5.QtGui import QIcon

# 新しいプレゼンテーション層のコンポーネント
from .panels.folder_panel import FolderPanel
from .panels.preview_panel import PreviewPanel
from .panels.map_panel import MapPanel
from .controls.address_bar import NavigationControls
from .controls.thumbnail_list import ThumbnailPanel

# ViewModelとController
from ..viewmodels.simple_main_viewmodel import SimpleMainViewModel
from ..controllers.main_controller import MainWindowController


class MaximizeControls(QWidget):
    """
    最大化コントロール（画像最大化、地図最大化、復元ボタン）
    """
    # シグナル
    image_maximize_requested = pyqtSignal()
    map_maximize_requested = pyqtSignal()
    restore_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 画像最大化ボタン
        self.maximize_image_btn = QPushButton("画像最大化")
        self.maximize_image_btn.setFixedWidth(90)
        self.maximize_image_btn.clicked.connect(self.image_maximize_requested.emit)
        layout.addWidget(self.maximize_image_btn)
        
        # 地図最大化ボタン
        self.maximize_map_btn = QPushButton("地図最大化")
        self.maximize_map_btn.setFixedWidth(90)
        self.maximize_map_btn.clicked.connect(self.map_maximize_requested.emit)
        layout.addWidget(self.maximize_map_btn)
        
        # 復元ボタン
        self.restore_btn = QPushButton("元に戻す")
        self.restore_btn.setFixedWidth(90)
        self.restore_btn.setFixedHeight(30)
        self.restore_btn.clicked.connect(self.restore_requested.emit)
        self.restore_btn.hide()  # 初期状態では非表示
        layout.addWidget(self.restore_btn)
        
        layout.addStretch()  # 右側に余白
    
    def show_restore_button(self):
        """復元ボタンを表示"""
        self.restore_btn.show()
        self.maximize_image_btn.hide()
        self.maximize_map_btn.hide()
    
    def hide_restore_button(self):
        """復元ボタンを非表示"""
        self.restore_btn.hide()
        self.maximize_image_btn.show()
        self.maximize_map_btn.show()


class MainView(QMainWindow):
    """
    メインビュー（Clean Architecture対応）
    MVVM/MVCパターンでの実装
    """
    # シグナル
    folder_changed = pyqtSignal(str)  # フォルダ変更時
    thumbnail_clicked = pyqtSignal(str)  # サムネイルクリック時
    address_changed = pyqtSignal(str)  # アドレス変更時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._setup_mvvm()
        self._connect_signals()
        
        # 状態管理
        self.is_fullscreen = False
        self.is_preview_fullscreen = False
        self._original_central_widget = None
    
    def _setup_ui(self):
        """UIセットアップ"""
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        
        # アイコン設定
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # コントロール部分
        self._setup_controls(main_layout)
        
        # メインコンテンツ部分
        self._setup_main_content(main_layout)
        
        # ステータスバー
        self.setStatusBar(QStatusBar())
        self.statusBar().showMessage("準備完了")
    
    def _setup_controls(self, parent_layout):
        """コントロール部分のセットアップ"""
        controls_layout = QHBoxLayout()
        
        # ナビゲーションコントロール（アドレスバー）
        self.navigation_controls = NavigationControls()
        controls_layout.addWidget(self.navigation_controls)
        
        # 最大化コントロール
        self.maximize_controls = MaximizeControls()
        controls_layout.addWidget(self.maximize_controls)
        
        parent_layout.addLayout(controls_layout)
    
    def _setup_main_content(self, parent_layout):
        """メインコンテンツ部分のセットアップ"""
        # メインスプリッター（水平分割）
        main_splitter = QSplitter(Qt.Horizontal)
        
        # 左側パネル（フォルダー + サムネイル）
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右側パネル（プレビュー + 地図）
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # スプリッターの比率設定
        main_splitter.setSizes([400, 1000])  # 左:右 = 400:1000
        
        parent_layout.addWidget(main_splitter)
    
    def _create_left_panel(self):
        """左側パネル（フォルダー + サムネイル）を作成"""
        left_splitter = QSplitter(Qt.Vertical)
        
        # フォルダパネル
        self.folder_panel = FolderPanel()
        left_splitter.addWidget(self.folder_panel)
        
        # サムネイルパネル
        self.thumbnail_panel = ThumbnailPanel()
        left_splitter.addWidget(self.thumbnail_panel)
        
        # スプリッターの比率設定
        left_splitter.setSizes([300, 400])  # フォルダ:サムネイル = 300:400
        
        return left_splitter
    
    def _create_right_panel(self):
        """右側パネル（プレビュー + 地図）を作成"""
        right_splitter = QSplitter(Qt.Vertical)
        
        # プレビューパネル
        self.preview_panel = PreviewPanel()
        right_splitter.addWidget(self.preview_panel)
        
        # 地図パネル
        self.map_panel = MapPanel()
        right_splitter.addWidget(self.map_panel)
        
        # スプリッターの比率設定
        right_splitter.setSizes([400, 300])  # プレビュー:地図 = 400:300
        
        return right_splitter
    
    def _setup_mvvm(self):
        """MVVM/MVCセットアップ"""
        # ViewModelとControllerの初期化
        self.view_model = SimpleMainViewModel()
        self.controller = MainWindowController(self.view_model, self)
        
        # 初期パス設定
        self.navigation_controls.set_path(QDir.rootPath())
    
    def _connect_signals(self):
        """シグナル接続"""
        # ナビゲーションコントロール
        self.navigation_controls.path_changed.connect(self.address_changed.emit)
        self.navigation_controls.parent_requested.connect(self._go_to_parent)
        
        # フォルダパネル
        self.folder_panel.folder_changed.connect(self.folder_changed.emit)
        
        # サムネイルパネル
        self.thumbnail_panel.thumbnail_clicked.connect(self.thumbnail_clicked.emit)
        
        # 最大化コントロール
        self.maximize_controls.image_maximize_requested.connect(self._toggle_image_maximize)
        self.maximize_controls.map_maximize_requested.connect(self._toggle_map_maximize)
        self.maximize_controls.restore_requested.connect(self._restore_normal_view)
    
    def _go_to_parent(self):
        """親フォルダへ移動"""
        current_path = self.navigation_controls.get_path()
        if current_path:
            parent_dir = QDir(current_path)
            if parent_dir.cdUp():
                parent_path = parent_dir.absolutePath()
                self.address_changed.emit(parent_path)
    
    def _toggle_image_maximize(self):
        """画像の最大化/復元を切り替え"""
        if not self.is_preview_fullscreen:
            self._maximize_preview()
        else:
            self._restore_normal_view()
    
    def _toggle_map_maximize(self):
        """地図の最大化/復元を切り替え"""
        if not self.is_preview_fullscreen:
            self._maximize_map()
        else:
            self._restore_normal_view()
    
    def _maximize_preview(self):
        """プレビューを最大化"""
        if self.is_preview_fullscreen:
            return
        
        self._original_central_widget = self.centralWidget()
        
        # プレビューパネルのみを中央ウィジェットに設定
        self.setCentralWidget(self.preview_panel)
        self.is_preview_fullscreen = True
        self.maximize_controls.show_restore_button()
        
        self.statusBar().showMessage("プレビュー最大化中 - 「元に戻す」ボタンで復元")
    
    def _maximize_map(self):
        """地図を最大化"""
        if self.is_preview_fullscreen:
            return
        
        self._original_central_widget = self.centralWidget()
        
        # 地図パネルのみを中央ウィジェットに設定
        self.setCentralWidget(self.map_panel)
        self.is_preview_fullscreen = True
        self.maximize_controls.show_restore_button()
        
        self.statusBar().showMessage("地図最大化中 - 「元に戻す」ボタンで復元")
    
    def _restore_normal_view(self):
        """通常表示に復元"""
        if not self.is_preview_fullscreen or not self._original_central_widget:
            return
        
        # 元の中央ウィジェットを復元
        self.setCentralWidget(self._original_central_widget)
        self.is_preview_fullscreen = False
        self.maximize_controls.hide_restore_button()
        
        self.statusBar().showMessage("通常表示に復元しました")
        self._original_central_widget = None
    
    # パブリックメソッド（Controllerから呼び出される）
    
    def update_folder_path(self, path):
        """フォルダパスを更新"""
        self.navigation_controls.set_path(path)
        self.folder_panel.set_root(path)
    
    def update_thumbnails(self, image_paths):
        """サムネイル一覧を更新"""
        self.thumbnail_panel.update_thumbnails(image_paths)
    
    def update_preview(self, image_path):
        """プレビュー画像を更新"""
        if image_path and os.path.exists(image_path):
            success = self.preview_panel.set_image(image_path)
            if success:
                self.statusBar().showMessage(f"画像を表示: {os.path.basename(image_path)}")
            else:
                self.statusBar().showMessage("画像の読み込みに失敗しました")
        else:
            self.preview_panel.clear_image()
            self.statusBar().showMessage("画像を選択してください")
    
    def update_map(self, map_file_path=None):
        """地図を更新"""
        if map_file_path and os.path.exists(map_file_path):
            self.map_panel.load_map(map_file_path)
            self.statusBar().showMessage("地図を更新しました")
        else:
            self.map_panel.show_no_gps_data()
            self.statusBar().showMessage("GPS情報が含まれていません")
    
    def select_thumbnail(self, image_path):
        """サムネイルを選択"""
        self.thumbnail_panel.select_thumbnail(image_path, center=True)
    
    def show_loading_map(self):
        """地図ローディング表示"""
        self.map_panel.show_loading()
        self.statusBar().showMessage("地図を生成中...")
    
    def show_status_message(self, message):
        """ステータスメッセージを表示"""
        self.statusBar().showMessage(message)


# 後方互換性のための関数（既存コードとの互換性維持）
def create_main_window():
    """
    レガシー関数：メインウィンドウを作成
    新しいMainViewクラスを使用して実装
    """
    return MainView()
