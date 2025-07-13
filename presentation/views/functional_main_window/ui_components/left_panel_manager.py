"""
Left Panel Manager

フォルダ内容表示、サムネイル表示、詳細情報表示を管理
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListWidget, QLabel, QAbstractItemView, QSplitter, QScrollArea
from PyQt5.QtCore import Qt
from utils.debug_logger import debug, info, warning, error, verbose


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
        self.panel.setVisible(True)  # 明示的に表示
        self.panel.setMinimumSize(400, 600)  # 最小サイズを設定
        layout = QVBoxLayout(self.panel)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)
        
        # 左パネル内の縦分割スプリッター
        left_splitter = QSplitter()
        left_splitter.setOrientation(2)  # Qt.Vertical = 2 # type: ignore
        left_splitter.setChildrenCollapsible(False)  # スプリッター要素を完全に隠せないように
        
        # フォルダ内容パネル
        folder_widget = QWidget()
        self._create_folder_panel(QVBoxLayout(folder_widget))
        left_splitter.addWidget(folder_widget)
        
        # サムネイルパネル
        thumbnail_widget = QWidget()
        self._create_thumbnail_panel(QVBoxLayout(thumbnail_widget))
        left_splitter.addWidget(thumbnail_widget)
        
        # ステータスパネル
        status_widget = QWidget()
        self._create_status_panel(QVBoxLayout(status_widget))
        left_splitter.addWidget(status_widget)
        
        # スプリッターサイズを設定
        left_splitter.setSizes([150, 250, 150])  # フォルダ:サムネイル:ステータス
        left_splitter.setStretchFactor(0, 0)  # フォルダ部分は固定的
        left_splitter.setStretchFactor(1, 1)  # サムネイル部分は可変
        left_splitter.setStretchFactor(2, 0)  # ステータス部分は固定的
        
        layout.addWidget(left_splitter)
        
        # テーマコンポーネント登録
        self._register_theme_components()
        
        # 各コンポーネントを明示的に表示
        if self.folder_group:
            self.folder_group.setVisible(True)
        if self.thumbnail_group:
            self.thumbnail_group.setVisible(True)
        if self.status_group:
            self.status_group.setVisible(True)
        
        # 左パネル用スプリッターをメインウィンドウに参照保存
        self.main_window.left_splitter = left_splitter
        
        debug("左パネル最終作成: panel={self.panel}, visible={self.panel.isVisible()}")
        debug("左パネルスプリッター作成: splitter={left_splitter}")
        
        return self.panel
    
    def _create_folder_panel(self, layout):
        """フォルダ内容パネルを作成"""
        self.folder_group = QGroupBox("📁 フォルダ内容")
        folder_layout = QVBoxLayout(self.folder_group)
        
        # フォルダ内容リスト
        self.folder_content_list = QListWidget()
        self.folder_content_list.setMinimumHeight(150)
        self.folder_content_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.folder_content_list.setEnabled(True)  # 初期状態から選択可能に
        
        # 選択表示を確実にするためのスタイル設定
        self.folder_content_list.setStyleSheet("""
            QListWidget {
                selection-background-color: #0078d4;
                selection-color: white;
                alternate-background-color: #f0f0f0;
            }
            QListWidget::item {
                padding: 4px;
                border-bottom: 1px solid #e0e0e0;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #e6f3ff;
            }
        """)
        
        # 選択を確実に有効にする
        self.folder_content_list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.folder_content_list.setCurrentRow(-1)  # 初期選択なし
        
        # テスト用のデータを追加（実際のフォルダが選択されるまでの暫定）
        try:
            self.folder_content_list.addItem("フォルダを選択してください...")
            debug("フォルダ内容リスト作成成功")
        except Exception as e:
            error("フォルダ内容リスト作成エラー: {e}")
        
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
            # サムネイルクリック時のコールバック関数を作成
            def thumbnail_item_clicked(item):
                """サムネイルクリック時のコールバック"""
                try:
                    # QListWidgetItemから画像パスを取得
                    image_path = item.data(256)  # Qt.UserRole = 256
                    verbose(f"サムネイルクリック: {image_path}")
                    if hasattr(self.main_window, 'image_event_handler') and self.main_window.image_event_handler:
                        self.main_window.image_event_handler.on_image_selected(item)
                except Exception as e:
                    error(f"サムネイルクリックエラー: {e}")
            
            self.thumbnail_list = create_thumbnail_list(thumbnail_item_clicked)
            self.thumbnail_layout.addWidget(self.thumbnail_list)
            debug("サムネイルリスト作成成功")
        except Exception as e:
            error("サムネイルエラー: {e}")
            error_label = QLabel(f"サムネイルエラー: {e}")
            error_label.setStyleSheet("color: red;")
            self.thumbnail_layout.addWidget(error_label)
        
        layout.addWidget(self.thumbnail_group)
        
        # メインウィンドウに参照を設定
        debug("サムネイルリスト参照設定: {self.thumbnail_list}")
        self.main_window.thumbnail_list = self.thumbnail_list
        self.main_window.thumbnail_group = self.thumbnail_group
        self.main_window.thumbnail_layout = self.thumbnail_layout
        debug("メインウィンドウにサムネイルリスト設定完了: {getattr(self.main_window, 'thumbnail_list', 'Not Found')}")
    
    def _create_status_panel(self, layout):
        """ステータス情報パネルを作成"""
        self.status_group = QGroupBox("📋 詳細情報")
        status_layout = QVBoxLayout(self.status_group)
        
        # スクロール可能なステータス表示エリアを作成
        self.status_scroll = QScrollArea()
        self.status_scroll.setWidgetResizable(True)
        self.status_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.status_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.status_scroll.setMinimumHeight(150)  # 最小高さ
        self.status_scroll.setMaximumHeight(300)  # 最大高さ
        
        # ステータス表示ラベル
        self.status_info = QLabel("画像を選択すると詳細情報が表示されます")
        self.status_info.setWordWrap(True)
        # ラベルの高さ制限を削除（スクロールエリアが制御）
        # 上寄せで表示するため
        try:
            self.status_info.setAlignment(1)  # type: ignore # Qt.AlignTop = 1
        except:
            pass
        
        # ラベルをスクロールエリアに設定
        self.status_scroll.setWidget(self.status_info)
        
        # スクロールエリアをレイアウトに追加
        status_layout.addWidget(self.status_scroll)
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
