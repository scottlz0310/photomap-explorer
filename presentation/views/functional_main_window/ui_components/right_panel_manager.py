"""
Right Panel Manager

プレビューパネルとマップパネルの管理
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QSplitter, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from utils.debug_logger import debug, info, warning, error, verbose


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
        """右パネルを作成（レイアウト優先・アンカリング最適化）"""
        # メインパネル作成（親ウィジェット明示的設定で独立ウィンドウ問題解決）
        self.panel = QWidget(self.main_window)
        from PyQt5.QtWidgets import QSizePolicy
        from PyQt5.QtCore import Qt
        self.panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # ウィンドウフラグを埋め込み用に設定（独立ウィンドウ完全防止）
        # Qt.Widget が存在しない場合は、埋め込み用の適切なフラグを設定
        try:
            # 埋め込みウィジェット用フラグ (0x0 = no flags = 埋め込み)
            self.panel.setWindowFlags(Qt.WindowType(0))
            debug("右パネルウィンドウフラグ設定完了")
        except AttributeError:
            # フラグ設定が失敗した場合は親設定で制御
            debug("右パネル親設定による埋め込み制御")
        debug("右パネルウィンドウフラグ確認: {self.panel.windowFlags()}")
        
        # レイアウト設定（手動サイズ指定を削除）
        layout = QVBoxLayout(self.panel)
        layout.setContentsMargins(2, 2, 2, 2)  # 最小限のマージン
        layout.setSpacing(2)
        
        # 縦分割スプリッター作成（親を明示的に設定）
        self.right_splitter = QSplitter(self.panel)
        try:
            self.right_splitter.setOrientation(2)  # type: ignore # 2 = Qt.Vertical
        except:
            pass
        self.right_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # スプリッター設定
        self.right_splitter.setChildrenCollapsible(False)
        self.right_splitter.setHandleWidth(8)
        
        # レイアウトにスプリッターを追加（setParent不要）
        layout.addWidget(self.right_splitter)
        
        # 子パネル作成
        self._create_preview_panel()
        self._create_map_panel()
        
        # 子パネルの即座表示設定（参照実装の改良点）
        if self.preview_group:
            self.preview_group.show()
        if self.map_group:
            self.map_group.show()
        
        # スプリッターサイズ初期設定（右パネル表示確保）
        self.right_splitter.setSizes([400, 300])  # プレビュー：マップ = 400:300
        self.right_splitter.setStretchFactor(0, 2)  # プレビューパネルを少し大きく
        self.right_splitter.setStretchFactor(1, 1)  # マップパネル
        
        # テーマ登録
        self._register_theme_components()
        
        # メインウィンドウ参照設定
        self.main_window.right_splitter = self.right_splitter
        
        # 明示的な表示設定（親があっても show() は必要）
        self.panel.show()
        
        # 強制更新（参照実装の改良点）
        self.right_splitter.update()
        self.panel.update()
        
        # 詳細デバッグ情報（参照実装のデバッグ強化）
        verbose("右パネル詳細デバッグ情報:")
        debug(f"  - panel parent: {self.panel.parent()}")
        debug(f"  - panel visible: {self.panel.isVisible()}")
        debug(f"  - panel geometry: {self.panel.geometry()}")
        debug(f"  - panel windowFlags: {self.panel.windowFlags()}")
        debug(f"  - right_splitter count: {self.right_splitter.count()}")
        debug(f"  - right_splitter sizes: {self.right_splitter.sizes()}")
        for i in range(self.right_splitter.count()):
            widget = self.right_splitter.widget(i)
            visible = widget.isVisible() if widget else False
            geometry = widget.geometry() if widget else None
            debug(f"  - splitter widget[{i}]: {widget}, visible: {visible}, geometry: {geometry}")
        
        # ウィジェット階層確認
        if self.preview_panel:
            debug(f"  - preview_panel parent: {self.preview_panel.parent()}")
            debug(f"  - preview_panel visible: {self.preview_panel.isVisible()}")
        if self.map_panel:
            debug(f"  - map_panel parent: {self.map_panel.parent()}")
            debug(f"  - map_panel visible: {self.map_panel.isVisible()}")
        
        debug("右パネル作成完了（表示最適化・アンカリング統合）")
        return self.panel
    
    def _create_preview_panel(self):
        """プレビューパネルを作成（レイアウト優先）"""
        # プレビューグループボックス（親を明示的に設定）
        self.preview_group = QGroupBox("🖼️ プレビュー", self.right_splitter)
        from PyQt5.QtWidgets import QSizePolicy
        self.preview_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        preview_layout = QVBoxLayout(self.preview_group)
        preview_layout.setContentsMargins(4, 4, 4, 4)
        preview_layout.setSpacing(2)
        
        # プレビューヘッダー
        preview_header = QHBoxLayout()
        preview_title = QLabel("画像プレビュー")
        preview_title.setStyleSheet("font-weight: normal; color: #666; font-size: 11px;")
        preview_header.addWidget(preview_title)
        preview_header.addStretch()
        
        # 最大化ボタン
        self.maximize_image_btn = QPushButton("⛶")
        self.maximize_image_btn.setToolTip("画像を最大化表示（ダブルクリックでも可能）")
        self.maximize_image_btn.setMaximumSize(40, 30)  # 戻るボタンサイズに合わせて拡大
        self.maximize_image_btn.setMinimumSize(40, 30)
        self.maximize_image_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                border: 2px solid #007ACC;
                background-color: rgba(0, 122, 204, 0.1);
            }
        """)
        preview_header.addWidget(self.maximize_image_btn)
        
        preview_header_widget = QWidget()
        preview_header_widget.setLayout(preview_header)
        preview_header_widget.setMaximumHeight(36)  # ボタンサイズに合わせて高さ調整
        preview_layout.addWidget(preview_header_widget)
        
        # プレビューパネル本体
        try:
            from ui.image_preview import create_image_preview
            # 適切な親を設定してレイアウト管理を確実にする
            self.preview_panel = create_image_preview(parent=self.preview_group)
            if self.preview_panel:
                self.preview_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                preview_layout.addWidget(self.preview_panel)
                debug("プレビューパネル作成成功: {self.preview_panel}")
                debug("プレビューパネル親: {self.preview_panel.parent()}")
            else:
                raise Exception("create_image_preview returned None")
        except Exception as e:
            error("プレビューエラー: {e}")
            error_label = QLabel(f"プレビューエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            preview_layout.addWidget(error_label)
        
        # スプリッターに追加（存在チェック）
        if self.right_splitter:
            self.right_splitter.addWidget(self.preview_group)
            # 子パネル即座表示（参照実装の改良点）
            self.preview_group.show()
            # QGroupBox の親がスプリッターに設定されることを確認
            debug("プレビューグループスプリッター追加後親: {self.preview_group.parent()}")
        
        # プレビューパネル強制更新（参照実装の改良点）
        if self.preview_panel:
            self.preview_panel.show()
            self.preview_panel.update()
            # 子ウィジェットの埋め込み確保
            try:
                self.preview_panel.setWindowFlags(Qt.WindowType(0))
                debug("プレビューパネル埋め込みフラグ設定完了")
            except AttributeError:
                debug("プレビューパネル親設定による埋め込み制御")
        
        # メインウィンドウ参照設定
        self.main_window.preview_panel = self.preview_panel
        self.main_window.image_preview = self.preview_panel
        self.main_window.maximize_image_btn = self.maximize_image_btn
    
    def _create_map_panel(self):
        """マップパネルを作成（レイアウト優先）"""
        # マップグループボックス（親を明示的に設定）
        self.map_group = QGroupBox("🗺️ マップ", self.right_splitter)
        from PyQt5.QtWidgets import QSizePolicy
        self.map_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        map_layout = QVBoxLayout(self.map_group)
        map_layout.setContentsMargins(4, 4, 4, 4)
        map_layout.setSpacing(2)
        
        # マップヘッダー
        map_header = QHBoxLayout()
        map_title = QLabel("撮影場所マップ")
        map_title.setStyleSheet("font-weight: normal; color: #666; font-size: 11px;")
        map_header.addWidget(map_title)
        map_header.addStretch()
        
        # 最大化ボタン
        self.maximize_map_btn = QPushButton("⛶")
        self.maximize_map_btn.setToolTip("マップを最大化表示（ダブルクリックでも可能）")
        self.maximize_map_btn.setMaximumSize(40, 30)  # 戻るボタンサイズに合わせて拡大
        self.maximize_map_btn.setMinimumSize(40, 30)
        self.maximize_map_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                border: 1px solid #666;
                border-radius: 4px;
                padding: 2px;
            }
            QPushButton:hover {
                border: 2px solid #007ACC;
                background-color: rgba(0, 122, 204, 0.1);
            }
        """)
        map_header.addWidget(self.maximize_map_btn)
        
        map_header_widget = QWidget()
        map_header_widget.setLayout(map_header)
        map_header_widget.setMaximumHeight(36)  # ボタンサイズに合わせて高さ調整
        map_layout.addWidget(map_header_widget)
        
        # マップパネル本体
        try:
            from ui.map_panel import MapPanel
            # 適切な親を設定してレイアウト管理を確実にする
            self.map_panel = MapPanel(parent=self.map_group)
            if self.map_panel:
                self.map_panel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                map_layout.addWidget(self.map_panel)
                verbose("マップパネル作成成功: {self.map_panel}")
                debug("マップパネル親: {self.map_panel.parent()}")
            else:
                raise Exception("MapPanel creation returned None")
        except Exception as e:
            error(f"マップエラー: {e}")
            error_label = QLabel(f"マップエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            map_layout.addWidget(error_label)
        
        # スプリッターに追加（存在チェック）
        if self.right_splitter:
            self.right_splitter.addWidget(self.map_group)
            # 子パネル即座表示（参照実装の改良点）
            self.map_group.show()
            # QGroupBox の親がスプリッターに設定されることを確認
            debug("マップグループスプリッター追加後親: {self.map_group.parent()}")
        
        # マップパネル強制更新（参照実装の改良点）
        if self.map_panel:
            self.map_panel.show()
            self.map_panel.update()
            # 子ウィジェットの埋め込み確保
            try:
                self.map_panel.setWindowFlags(Qt.WindowType(0))
                debug("マップパネル埋め込みフラグ設定完了")
            except AttributeError:
                debug("マップパネル親設定による埋め込み制御")
        
        # メインウィンドウ参照設定
        self.main_window.map_panel = self.map_panel
        self.main_window.map_view = self.map_panel
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
    
    def debug_widget_hierarchy(self):
        """ウィジェット階層をデバッグ出力"""
        from utils.debug_logger import debug
        debug("\n🔍 右パネルウィジェット階層デバッグ:")
        debug(f"panel: {self.panel}, parent: {self.panel.parent() if self.panel else None}")
        debug(f"right_splitter: {self.right_splitter}, parent: {self.right_splitter.parent() if self.right_splitter else None}")
        debug(f"preview_group: {self.preview_group}, parent: {self.preview_group.parent() if self.preview_group else None}")
        debug(f"preview_panel: {self.preview_panel}, parent: {self.preview_panel.parent() if self.preview_panel else None}")
        debug(f"map_group: {self.map_group}, parent: {self.map_group.parent() if self.map_group else None}")
        debug(f"map_panel: {self.map_panel}, parent: {self.map_panel.parent() if self.map_panel else None}")
        
        if self.panel:
            debug(f"panel window flags: {self.panel.windowFlags()}")
            debug(f"panel visible: {self.panel.isVisible()}")
            debug(f"panel geometry: {self.panel.geometry()}")
        
        if self.preview_panel and hasattr(self.preview_panel, 'windowFlags'):
            debug(f"preview_panel window flags: {self.preview_panel.windowFlags()}")
            print(f"preview_panel visible: {self.preview_panel.isVisible()}")
        
        if self.map_panel and hasattr(self.map_panel, 'windowFlags'):
            print(f"map_panel window flags: {self.map_panel.windowFlags()}")
            print(f"map_panel visible: {self.map_panel.isVisible()}")

    def ensure_embedded_widgets(self):
        """ウィジェットが確実に埋め込まれるようにする（強化版）"""
        try:
            print("\n🔧 ウィジェット埋め込み修正開始...")
            
            # プレビューパネルの修正
            if self.preview_panel and self.preview_group:
                print(f"プレビューパネル修正前: parent={self.preview_panel.parent()}")
                
                # 親を明示的に再設定
                self.preview_panel.setParent(self.preview_group)
                
                # ウィンドウフラグを埋め込み専用に設定（スキップ）
                # from PyQt5.QtCore import Qt
                # フラグ設定はスキップして親設定に集中
                
                # レイアウトに確実に追加
                layout = self.preview_group.layout()
                if layout:
                    # 既存のウィジェットを削除してから再追加
                    layout.removeWidget(self.preview_panel)
                    layout.addWidget(self.preview_panel)
                
                # 表示設定を強制
                self.preview_panel.setVisible(True)
                self.preview_panel.show()
                
                print(f"プレビューパネル修正後: parent={self.preview_panel.parent()}")
            
            # マップパネルの修正
            if self.map_panel and self.map_group:
                print(f"マップパネル修正前: parent={self.map_panel.parent()}")
                
                # 親を明示的に再設定
                self.map_panel.setParent(self.map_group)
                
                # ウィンドウフラグを埋め込み専用に設定（スキップ）
                # from PyQt5.QtCore import Qt
                # フラグ設定はスキップして親設定に集中
                
                # レイアウトに確実に追加
                layout = self.map_group.layout()
                if layout:
                    # 既存のウィジェットを削除してから再追加
                    layout.removeWidget(self.map_panel)
                    layout.addWidget(self.map_panel)
                
                # 表示設定を強制
                self.map_panel.setVisible(True)
                self.map_panel.show()
                
                print(f"マップパネル修正後: parent={self.map_panel.parent()}")
            
            # 右スプリッターの強制更新
            if self.right_splitter:
                self.right_splitter.update()
                info("右スプリッター更新完了")
            
            # パネル全体の強制更新
            if self.panel:
                self.panel.update()
                info("右パネル全体更新完了")
            
            info("ウィジェット埋め込み修正完了（強化版）")
            
        except Exception as e:
            error("ウィジェット埋め込み修正エラー: {e}")
            import traceback
            traceback.print_exc()
