"""
Left Panel Manager

フォルダ内容表示、サムネイル表示、詳細情報表示を管理
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListWidget, QLabel
from PyQt5.QtCore import Qt


class LeftPanelManager:
    """
    左パネルの管理クラス
    
    フォルダ内容、サムネイル、ステータス情報の表示を担当
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.panel = None
        
        # UI要素
        self.folder_content_list = None
        self.thumbnail_list = None
        self.status_info = None
        self.folder_group = None
        self.thumbnail_group = None
        self.status_group = None
        self.thumbnail_layout = None
    
    def create_panel(self):
        """左パネルを作成"""
        self.panel = QWidget()
        layout = QVBoxLayout(self.panel)
        
        # フォルダ内容パネル
        self._create_folder_panel(layout)
        
        # サムネイルパネル
        self._create_thumbnail_panel(layout)
        
        # ステータスパネル
        self._create_status_panel(layout)
        
        # テーマコンポーネント登録
        self._register_theme_components()
        
        return self.panel
    
    def _create_folder_panel(self, layout):
        """フォルダ内容パネルを作成"""
        self.folder_group = QGroupBox("📁 フォルダ内容")
        folder_layout = QVBoxLayout(self.folder_group)
        
        # フォルダ内容リスト
        self.folder_content_list = QListWidget()
        self.folder_content_list.setMinimumHeight(150)
        
        # イベントハンドラの接続（後で設定）
        # self.folder_content_list.itemClicked.connect(...)
        # self.folder_content_list.itemDoubleClicked.connect(...)
        
        folder_layout.addWidget(self.folder_content_list)
        layout.addWidget(self.folder_group)
        
        # メインウィンドウに参照を設定
        self.main_window.folder_content_list = self.folder_content_list
    
    def _create_thumbnail_panel(self, layout):
        """サムネイルパネルを作成"""
        self.thumbnail_group = QGroupBox("🖼️ サムネイル")
        self.thumbnail_layout = QVBoxLayout(self.thumbnail_group)
        
        try:
            from ui.thumbnail_list import create_thumbnail_list
            self.thumbnail_list = create_thumbnail_list(None)  # コールバックは後で設定
            self.thumbnail_layout.addWidget(self.thumbnail_list)
        except Exception as e:
            error_label = QLabel(f"サムネイルエラー: {e}")
            error_label.setStyleSheet("color: red;")
            self.thumbnail_layout.addWidget(error_label)
        
        layout.addWidget(self.thumbnail_group)
        
        # メインウィンドウに参照を設定
        self.main_window.thumbnail_list = self.thumbnail_list
        self.main_window.thumbnail_group = self.thumbnail_group
        self.main_window.thumbnail_layout = self.thumbnail_layout
    
    def _create_status_panel(self, layout):
        """ステータス情報パネルを作成"""
        self.status_group = QGroupBox("📋 詳細情報")
        status_layout = QVBoxLayout(self.status_group)
        
        # ステータス表示ラベル
        self.status_info = QLabel("画像を選択すると詳細情報が表示されます")
        self.status_info.setWordWrap(True)
        self.status_info.setMinimumHeight(120)
        self.status_info.setMaximumHeight(180)
        
        status_layout.addWidget(self.status_info)
        layout.addWidget(self.status_group)
        
        # メインウィンドウに参照を設定
        self.main_window.status_info = self.status_info
    
    def _register_theme_components(self):
        """テーマコンポーネントを登録"""
        if self.main_window and hasattr(self.main_window, 'register_theme_component'):
            self.main_window.register_theme_component(self.folder_group, "group_box")
            self.main_window.register_theme_component(self.folder_content_list, "list_widget")
            self.main_window.register_theme_component(self.thumbnail_group, "group_box")
            self.main_window.register_theme_component(self.status_group, "group_box")
            self.main_window.register_theme_component(self.status_info, "status_info")
            self.main_window.register_theme_component(self.panel, "panel")
    
    def set_event_handlers(self, folder_item_clicked, folder_item_double_clicked, image_selected):
        """イベントハンドラを設定"""
        if self.folder_content_list:
            self.folder_content_list.itemClicked.connect(folder_item_clicked)
            self.folder_content_list.itemDoubleClicked.connect(folder_item_double_clicked)
        
        if self.thumbnail_list and hasattr(self.thumbnail_list, 'set_selection_callback'):
            self.thumbnail_list.set_selection_callback(image_selected)
    
    def update_folder_content(self, folder_path):
        """フォルダ内容を更新"""
        # この機能は別のマネージャーに移譲される予定
        pass
    
    def update_thumbnails(self, image_files):
        """サムネイルを更新"""
        # この機能は別のマネージャーに移譲される予定
        pass
    
    def update_status_info(self, message):
        """ステータス情報を更新"""
        if self.status_info:
            self.status_info.setText(message)
    
    def clear_status_info(self):
        """ステータス情報をクリア"""
        if self.status_info:
            self.status_info.setText("画像を選択すると詳細情報が表示されます")
