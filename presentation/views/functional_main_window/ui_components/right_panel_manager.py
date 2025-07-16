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
        try:
            from utils.debug_logger import debug, info, error
            info("右パネル作成開始")
            
            self.panel = QWidget()
            layout = QVBoxLayout(self.panel)
            
            # デバッグ: パネルの可視性とサイズを確認
            debug(f"右パネル作成: サイズ={self.panel.size()}, 可視={self.panel.isVisible()}")
            
            # 上下スプリッター
            info("右パネルスプリッター作成中...")
            self.right_splitter = QSplitter(Qt.Orientation.Vertical)
            debug(f"右スプリッター作成直後: {self.right_splitter}, None確認: {self.right_splitter is not None}")
            
            if self.right_splitter is not None:
                layout.addWidget(self.right_splitter)
                debug(f"右スプリッター作成: サイズ={self.right_splitter.size()}, 可視={self.right_splitter.isVisible()}")
            else:
                error("右スプリッター作成に失敗")
            
            # プレビューパネル
            info("プレビューパネル作成中...")
            self._create_preview_panel()
            
            # マップパネル
            info("マップパネル作成中...")
            self._create_map_panel()
            
            # スプリッターサイズ調整
            info("スプリッターサイズ調整中...")
            # プレビュー:マップ = 1:1の比率で設定、最小サイズも確保
            self.right_splitter.setSizes([400, 400])
            debug(f"右スプリッターサイズ設定後: サイズ配分={self.right_splitter.sizes()}, 子要素数={self.right_splitter.count()}")
            
            # 地図パネルの最小サイズを強制設定
            if self.map_group:
                self.map_group.setMinimumHeight(300)
                debug(f"地図グループ最小サイズ設定: {self.map_group.minimumHeight()}px")
            if hasattr(self, 'map_panel') and self.map_panel:
                self.map_panel.setMinimumHeight(250)
                debug(f"地図パネル最小サイズ設定: {self.map_panel.minimumHeight()}px")
            
            # テーマコンポーネント登録
            info("右パネルテーマコンポーネント登録中...")
            self._register_theme_components()
            
            # メインウィンドウに参照を設定
            self.main_window.right_splitter = self.right_splitter
            
            # 強制的にパネルを表示
            self.panel.show()
            self.right_splitter.show()
            if self.preview_group:
                self.preview_group.show()
            if self.map_group:
                self.map_group.show()
            if self.preview_panel:
                self.preview_panel.show()
            if self.map_panel:
                self.map_panel.show()
            
            debug(f"右パネル最終状態: パネルサイズ={self.panel.size()}, スプリッターサイズ={self.right_splitter.size()}")
            debug(f"強制表示後可視性: パネル={self.panel.isVisible()}, スプリッター={self.right_splitter.isVisible()}")
            
            info("右パネル作成完了")
            return self.panel
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"右パネル作成エラー: {e}")
            import traceback
            traceback.print_exc()
            return QWidget()  # 空のウィジェットを返す
    
    def _create_preview_panel(self):
        """プレビューパネルを作成"""
        from utils.debug_logger import debug, info, error
        debug("プレビューパネル作成開始")
        
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
            debug("プレビューパネル本体作成開始")
            from ui.image_preview import create_image_preview
            debug("image_previewインポート成功")
            self.preview_panel = create_image_preview()
            debug(f"プレビューパネル作成成功: {self.preview_panel}")
            preview_layout.addWidget(self.preview_panel)
            debug("プレビューパネルをレイアウトに追加完了")
        except Exception as e:
            error(f"プレビューパネル作成エラー: {e}")
            import traceback
            traceback.print_exc()
            error_label = QLabel(f"プレビューエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            preview_layout.addWidget(error_label)
            self.preview_panel = error_label  # エラーラベルを設定
        
        debug(f"右スプリッター存在確認: {self.right_splitter is not None}")
        if self.right_splitter is not None:
            debug("プレビューグループを右スプリッターに追加中...")
            self.right_splitter.addWidget(self.preview_group)
            debug(f"プレビューグループ追加後の右スプリッター子要素数: {self.right_splitter.count()}")
        else:
            error("右スプリッターが存在しません")
        
        # メインウィンドウに参照を設定
        self.main_window.preview_panel = self.preview_panel
        self.main_window.maximize_image_btn = self.maximize_image_btn
        debug("プレビューパネル作成完了")
    
    def _create_map_panel(self):
        """マップパネルを作成"""
        from utils.debug_logger import debug, info, error
        debug("マップパネル作成開始")
        
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
            debug("マップパネル本体作成開始")
            from ui.map_panel import create_map_panel
            debug("map_panelインポート成功")
            self.map_panel = create_map_panel()
            debug(f"マップパネル作成成功: {self.map_panel}")
            map_layout.addWidget(self.map_panel)
            debug("マップパネルをレイアウトに追加完了")
        except Exception as e:
            error(f"マップパネル作成エラー: {e}")
            import traceback
            traceback.print_exc()
            error_label = QLabel(f"マップエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            map_layout.addWidget(error_label)
            self.map_panel = error_label  # エラーラベルを設定
        
        debug(f"右スプリッター存在確認: {self.right_splitter is not None}")
        if self.right_splitter is not None:
            debug("マップグループを右スプリッターに追加中...")
            self.right_splitter.addWidget(self.map_group)
            debug(f"マップグループ追加後の右スプリッター子要素数: {self.right_splitter.count()}")
        else:
            error("右スプリッターが存在しません")
        
        # メインウィンドウに参照を設定
        self.main_window.map_panel = self.map_panel
        self.main_window.maximize_map_btn = self.maximize_map_btn
        debug("マップパネル作成完了")
    
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
