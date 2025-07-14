"""
Right Panel Manager

プレビューパネルとマップパネルの管理
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QSplitter, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt


class RightPanelManager:
    """
    右パネルの管理クラス
    
    プレビューパネルとマップパネルの表示を担当
    """
    
    def __init__(self, main_window):
        self.main_window = main_window
        self.panel = None
        
        # UI要素
        self.right_splitter = None
        self.preview_panel = None
        self.map_panel = None
        self.maximize_image_btn = None
        self.maximize_map_btn = None
        self.preview_group = None
        self.map_group = None
    
    def create_panel(self):
        """右パネルを作成"""
        self.panel = QWidget()
        layout = QVBoxLayout(self.panel)
        
        # 上下スプリッター
        self.right_splitter = QSplitter(Qt.Vertical)
        if self.right_splitter:
            layout.addWidget(self.right_splitter)
        
        # プレビューパネル
        self._create_preview_panel()
        
        # マップパネル
        self._create_map_panel()
        
        # スプリッターサイズ調整
        self.right_splitter.setSizes([400, 400])
        
        # テーマコンポーネント登録
        self._register_theme_components()
        
        # メインウィンドウに参照を設定
        self.main_window.right_splitter = self.right_splitter
        
        return self.panel
    
    def _create_preview_panel(self):
        """プレビューパネルを作成"""
        self.preview_group = QGroupBox("🖼️ プレビュー")
        preview_layout = QVBoxLayout(self.preview_group)
        
        # プレビューヘッダー（タイトル + 最大化ボタン）
        preview_header = QHBoxLayout()
        preview_title = QLabel("画像プレビュー")
        preview_title.setStyleSheet("font-weight: normal; color: #666; font-size: 11px;")
        preview_header.addWidget(preview_title)
        preview_header.addStretch()  # 右寄せ
        
        # 最大化ボタン
        self.maximize_image_btn = QPushButton("⛶")
        self.maximize_image_btn.setToolTip("画像を最大化表示（ダブルクリックでも可能）")
        self.maximize_image_btn.setMaximumSize(28, 28)
        # イベントハンドラは後で設定
        preview_header.addWidget(self.maximize_image_btn)
        
        preview_header_widget = QWidget()
        preview_header_widget.setLayout(preview_header)
        preview_header_widget.setMaximumHeight(32)
        preview_layout.addWidget(preview_header_widget)
        
        # プレビューパネル本体
        try:
            from ui.image_preview import create_image_preview
            self.preview_panel = create_image_preview()
            preview_layout.addWidget(self.preview_panel)
        except Exception as e:
            error_label = QLabel(f"プレビューエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            preview_layout.addWidget(error_label)
        
        if self.right_splitter:
            self.right_splitter.addWidget(self.preview_group)
        
        # メインウィンドウに参照を設定
        self.main_window.preview_panel = self.preview_panel
        self.main_window.maximize_image_btn = self.maximize_image_btn
    
    def _create_map_panel(self):
        """マップパネルを作成"""
        self.map_group = QGroupBox("🗺️ マップ")
        map_layout = QVBoxLayout(self.map_group)
        
        # マップヘッダー（タイトル + 最大化ボタン）
        map_header = QHBoxLayout()
        map_title = QLabel("撮影場所マップ")
        map_title.setStyleSheet("font-weight: normal; color: #666; font-size: 11px;")
        map_header.addWidget(map_title)
        map_header.addStretch()  # 右寄せ
        
        # 最大化ボタン
        self.maximize_map_btn = QPushButton("⛶")
        self.maximize_map_btn.setToolTip("マップを最大化表示（ダブルクリックでも可能）")
        self.maximize_map_btn.setMaximumSize(28, 28)
        # イベントハンドラは後で設定
        map_header.addWidget(self.maximize_map_btn)
        
        map_header_widget = QWidget()
        map_header_widget.setLayout(map_header)
        map_header_widget.setMaximumHeight(32)
        map_layout.addWidget(map_header_widget)
        
        # マップパネル本体
        try:
            from ui.map_panel import create_map_panel
            self.map_panel = create_map_panel()
            map_layout.addWidget(self.map_panel)
        except Exception as e:
            error_label = QLabel(f"マップエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            map_layout.addWidget(error_label)
        
        if self.right_splitter:
            self.right_splitter.addWidget(self.map_group)
        
        # メインウィンドウに参照を設定
        self.main_window.map_panel = self.map_panel
        self.main_window.maximize_map_btn = self.maximize_map_btn
    
    def _register_theme_components(self):
        """テーマコンポーネントを登録"""
        if self.main_window and hasattr(self.main_window, 'register_theme_component'):
            self.main_window.register_theme_component(self.preview_group, "group_box")
            self.main_window.register_theme_component(self.maximize_image_btn, "maximize_button")
            self.main_window.register_theme_component(self.map_group, "group_box")
            self.main_window.register_theme_component(self.maximize_map_btn, "maximize_button")
            self.main_window.register_theme_component(self.panel, "panel")
    
    def set_event_handlers(self, toggle_image_maximize, toggle_map_maximize):
        """イベントハンドラを設定"""
        if self.maximize_image_btn:
            self.maximize_image_btn.clicked.connect(toggle_image_maximize)
        
        if self.maximize_map_btn:
            self.maximize_map_btn.clicked.connect(toggle_map_maximize)
        
        # ダブルクリックイベントの設定
        self._setup_double_click_events(toggle_image_maximize, toggle_map_maximize)
    
    def _setup_double_click_events(self, toggle_image_maximize, toggle_map_maximize):
        """ダブルクリックイベントを設定"""
        # プレビューパネルのダブルクリック
        if self.preview_panel and hasattr(self.preview_panel, 'mouseDoubleClickEvent'):
            original_preview_double_click = getattr(self.preview_panel, 'mouseDoubleClickEvent', None)
            def enhanced_preview_double_click(a0):
                toggle_image_maximize()
                if original_preview_double_click:
                    original_preview_double_click(a0)
            # 型チェック回避のため条件付きで設定
            try:
                self.preview_panel.mouseDoubleClickEvent = enhanced_preview_double_click  # type: ignore
            except (AttributeError, TypeError):
                pass  # 設定できない場合はスキップ
        
        # マップパネルのダブルクリック
        if self.map_panel and hasattr(self.map_panel, 'mouseDoubleClickEvent'):
            original_map_double_click = getattr(self.map_panel, 'mouseDoubleClickEvent', None)
            def enhanced_map_double_click(a0):
                toggle_map_maximize()
                if original_map_double_click:
                    original_map_double_click(a0)
            # 型チェック回避のため条件付きで設定
            try:
                self.map_panel.mouseDoubleClickEvent = enhanced_map_double_click  # type: ignore
            except (AttributeError, TypeError):
                pass  # 設定できない場合はスキップ
