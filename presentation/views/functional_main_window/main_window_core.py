"""
Main Window Core

メインウィンドウの基本構成と初期化を担当
"""

import os
import logging
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QSplitter, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

# コントロールのインポート  
from ui.controls import create_controls

# テーマシステム
from presentation.themes import ThemeAwareMixin

# デバッグロガー
from utils.debug_logger import debug, info, warning, error, verbose


class MainWindowCore(QMainWindow, ThemeAwareMixin):
    """
    メインウィンドウのコア機能
    
    基本的なウィンドウ構成、初期化、メイン制御を担当
    """
    
    def __init__(self):
        QMainWindow.__init__(self)
        try:
            ThemeAwareMixin.__init__(self)
        except Exception as e:
            warning(f"ThemeAwareMixin初期化エラー: {e}")
        
        # ウィンドウ基本設定
        self.setWindowTitle("PhotoMap Explorer - 新UI (Clean Architecture) v2.2.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # 状態管理
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        
        # UI状態管理
        self.maximized_state = None  # 'image', 'map', None
        self.main_splitter = None
        self.right_splitter = None
        self.maximize_container = None
        self.original_preview_parent = None
        self.original_map_parent = None
        
        # UIコンポーネント参照
        self.thumbnail_list = None
        self.preview_panel = None
        self.map_panel = None
        self.folder_panel = None
        self.address_bar = None
        
        # 管理クラス参照（setup_managersで設定される）
        self.left_panel_manager = None
        self.right_panel_manager = None
        self.address_bar_manager = None
        self.maximize_handler = None
        self.folder_event_handler = None
        self.image_event_handler = None
        self.theme_event_handler = None
        self.image_display_manager = None
        self.map_display_manager = None
        self.status_display_manager = None
        
        # 初期化
        self._setup_icon()
        self._setup_basic_ui()
    
    def _setup_icon(self):
        """アイコン設定"""
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_basic_ui(self):
        """基本UI構成の設定"""
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 中央ウィジェットのサイズポリシーを設定
        from PyQt5.QtWidgets import QSizePolicy
        central_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.main_layout = QVBoxLayout(central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)  # マージン削除
        self.main_layout.setSpacing(0)  # スペーシング削除
        
        # ツールバーエリアの準備（詳細は後で設定）
        self._setup_toolbar_area()
        
        # メインスプリッターの準備
        self.main_splitter = QSplitter()
        self.main_splitter.setOrientation(Qt.Horizontal)  # type: ignore
        self.main_splitter.setChildrenCollapsible(False)  # スプリッター要素を完全に隠せないように
        
        # メインスプリッターのサイズポリシー設定
        self.main_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        # メインレイアウトにストレッチファクターを設定
        self.main_layout.addWidget(self.main_splitter, 1)  # ストレッチファクター1で追加
        
        # 最大化コンテナの準備
        self._setup_maximize_container()
        
        # レイアウト構造をデバッグ表示
        verbose("レイアウト構造確認:")
        verbose(f"  - main_layout子要素数: {self.main_layout.count()}")
        for i in range(self.main_layout.count()):
            item = self.main_layout.itemAt(i)
            widget = item.widget() if item else None
            verbose(f"  - 要素[{i}]: {widget}")
        
        # ステータスバー設定
        status_bar = self.statusBar()
        if status_bar:
            # status_bar.hide()  # HOTFIX: ステータスバーを復帰
            status_bar.showMessage("初期化中...")
    
    def _setup_toolbar_area(self):
        """ツールバーエリアの基本設定"""
        # ツールバーレイアウト
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        
        # フォルダ選択ボタン
        self.folder_btn = QPushButton("📁 フォルダ選択")
        self.folder_btn.setMaximumHeight(30)
        toolbar_layout.addWidget(self.folder_btn)
        
        # アドレスバーエリア（実際のコールバックを設定）
        def on_address_changed_callback(path):
            """アドレスバーのパス変更時のコールバック"""
            if hasattr(self, 'address_bar_manager') and self.address_bar_manager:
                self.address_bar_manager.on_address_changed(path)
        
        def on_parent_button_callback():
            """親フォルダボタンクリック時のコールバック"""
            if hasattr(self, 'address_bar_manager') and self.address_bar_manager:
                self.address_bar_manager.go_to_parent_folder()
        
        self.controls_widget, self.address_bar, self.parent_button = create_controls(
            on_address_changed_callback,
            on_parent_button_callback
        )
        
        # create_controls内で既に初期化済みのため、追加の設定のみ
        if self.controls_widget:
            self.controls_widget.setMaximumHeight(55)  # 横並びに対応して高さを調整（少し余裕を持たせる）
        
        toolbar_layout.addWidget(self.controls_widget, 1)
        
        # ナビゲーションコントロールの参照を取得
        from ui.controls.toolbar.navigation_controls import NavigationControls
        nav_controls_list = self.controls_widget.findChildren(NavigationControls)
        if nav_controls_list:
            self.navigation_controls = nav_controls_list[0]
            verbose(f"ナビゲーションコントロール参照取得: {self.navigation_controls}")
        else:
            self.navigation_controls = None
            warning("ナビゲーションコントロールが見つかりません")
        
        # テーマ切り替えボタン
        self.theme_toggle_btn = QPushButton("🌙 ダーク")
        self.theme_toggle_btn.setMaximumHeight(30)
        self.theme_toggle_btn.setMaximumWidth(80)
        self.theme_toggle_btn.setToolTip("ダークモード・ライトモード切り替え")
        toolbar_layout.addWidget(self.theme_toggle_btn)
        
        # ツールバーウィジェット
        self.toolbar_widget = QWidget()
        self.toolbar_widget.setLayout(toolbar_layout)
        self.toolbar_widget.setMaximumHeight(40)
        # ツールバーを確実に表示
        self.toolbar_widget.setVisible(True)
        self.toolbar_widget.show()
        debug(f"ツールバーウィジェット表示設定: visible={self.toolbar_widget.isVisible()}")
        self.main_layout.addWidget(self.toolbar_widget)
    
    def _setup_maximize_container(self):
        """最大化コンテナの準備"""
        from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy
        
        self.maximize_container = QWidget()
        # 最大化コンテナのサイズポリシーを設定
        self.maximize_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        self.maximized_content_layout = QVBoxLayout(self.maximize_container)
        self.maximized_content_layout.setContentsMargins(0, 0, 0, 0)
        
        # 最大化コンテナを追加（初期は非表示）
        self.main_layout.addWidget(self.maximize_container, 1)  # ストレッチファクター1で追加
        self.maximize_container.hide()
        self.maximize_container.setVisible(False)  # 明示的に非表示に設定
        
        # デバッグ用スタイル設定（本番ではコメントアウト）
        # self.maximize_container.setStyleSheet("""
        #     QWidget {
        #         background-color: #1e1e1e;
        #         border: 2px solid #007ACC;
        #     }
        # """)
    
    def setup_managers(self, left_panel_mgr, right_panel_mgr, address_bar_mgr, maximize_hdlr,
                      folder_event_hdlr, image_event_hdlr, theme_event_hdlr,
                      image_display_mgr, map_display_mgr, status_display_mgr):
        """
        各種管理クラスを設定
        """
        debug("setup_managers メソッド開始")
        
        self.left_panel_manager = left_panel_mgr
        self.right_panel_manager = right_panel_mgr
        self.address_bar_manager = address_bar_mgr
        self.maximize_handler = maximize_hdlr
        self.folder_event_handler = folder_event_hdlr
        self.image_event_handler = image_event_hdlr
        self.theme_event_handler = theme_event_hdlr
        self.image_display_manager = image_display_mgr
        self.map_display_manager = map_display_mgr
        self.status_display_manager = status_display_mgr
        
        verbose("設定された管理クラス:")
        verbose(f"   左パネル: {self.left_panel_manager}")
        verbose(f"   右パネル: {self.right_panel_manager}")
        
        # 各管理クラスに参照を渡す
        verbose("_setup_manager_references 呼び出し")
        self._setup_manager_references()
        
        # イベントハンドラの接続
        verbose("_connect_event_handlers 呼び出し")
        self._connect_event_handlers()
    
    def _setup_manager_references(self):
        """管理クラス間の参照を設定"""
        debug("_setup_manager_references 開始")
        verbose("self.left_panel_manager = {self.left_panel_manager}")
        verbose("self.right_panel_manager = {self.right_panel_manager}")
        verbose("self.main_splitter = {self.main_splitter}")
        verbose("hasattr(self, 'main_splitter') = {hasattr(self, 'main_splitter')}")
        
        # 左パネル作成
        condition1 = bool(self.left_panel_manager)
        condition2 = hasattr(self, 'main_splitter')
        condition3 = (self.main_splitter is not None) if hasattr(self, 'main_splitter') else False
        verbose("左パネル条件: manager={condition1}, has_attr={condition2}, splitter_not_none={condition3}")
        
        if self.left_panel_manager and hasattr(self, 'main_splitter') and self.main_splitter is not None:
            try:
                verbose("左パネル作成開始...")
                left_panel = self.left_panel_manager.create_panel()
                debug("左パネル作成成功: {left_panel}")
                self.main_splitter.addWidget(left_panel)
                debug("左パネルをスプリッターに追加完了")
            except Exception as e:
                error("左パネル作成エラー: {e}")
                import traceback
                traceback.print_exc()
        else:
            warning("左パネル作成スキップ: manager={bool(self.left_panel_manager)}, splitter_exists={hasattr(self, 'main_splitter')}, splitter_value={getattr(self, 'main_splitter', None)}")
        
        # 右パネル作成
        condition1_r = bool(self.right_panel_manager)
        condition2_r = hasattr(self, 'main_splitter')
        condition3_r = (self.main_splitter is not None) if hasattr(self, 'main_splitter') else False
        verbose("右パネル条件: manager={condition1_r}, has_attr={condition2_r}, splitter_not_none={condition3_r}")
        
        if self.right_panel_manager and hasattr(self, 'main_splitter') and self.main_splitter is not None:
            try:
                verbose("右パネル作成開始...")
                # 左パネルと同じパターンに統一
                right_panel = self.right_panel_manager.create_panel()
                debug("右パネル作成成功: {right_panel}")
                self.main_splitter.addWidget(right_panel)
                debug("右パネルをスプリッターに追加完了")
            except Exception as e:
                error("右パネル作成エラー: {e}")
                import traceback
                traceback.print_exc()
        else:
            warning("右パネル作成スキップ: manager={bool(self.right_panel_manager)}, splitter_exists={hasattr(self, 'main_splitter')}, splitter_value={getattr(self, 'main_splitter', None)}")
        
        # スプリッターサイズ調整
        if hasattr(self, 'main_splitter') and self.main_splitter is not None:
            # スプリッター自体のサイズポリシーを設定
            from PyQt5.QtWidgets import QSizePolicy
            self.main_splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            
            # より適切なサイズ比率を設定
            self.main_splitter.setSizes([350, 1050])  # 左パネル350px、右パネル1050px（右パネル表示確保）
            self.main_splitter.setVisible(True)  # 明示的に表示する
            
            # スプリッターの最小サイズを設定
            self.main_splitter.setMinimumSize(800, 600)
            
            # 子要素の折りたたみを無効化（アンカリング改善）
            self.main_splitter.setChildrenCollapsible(False)
            
            # ストレッチファクターを設定（右パネルがウィンドウサイズに追従）
            self.main_splitter.setStretchFactor(0, 0)  # 左パネルは固定的
            self.main_splitter.setStretchFactor(1, 3)  # 右パネルは強可変（ウィンドウサイズに強く追従）
            
            # ハンドル幅を大きくしてリサイズしやすく
            self.main_splitter.setHandleWidth(8)
            
            verbose("スプリッターサイズ設定: [350, 1050] - 右パネル表示確保・アンカリング改善")
            verbose("スプリッター子要素数: {self.main_splitter.count()}")
            
            # 各子要素の詳細を確認
            for i in range(self.main_splitter.count()):
                widget = self.main_splitter.widget(i)
                if widget:
                    widget.setVisible(True)  # 明示的に表示
                    widget.show()  # show()も呼び出し
                    widget.raise_()  # ウィジェットを前面に
                verbose("子要素[{i}]: {widget}, 表示状態: {widget.isVisible() if widget else 'None'}, サイズ: {widget.size() if widget else 'None'}")
            
            # メインレイアウトの子要素も強制表示
            if hasattr(self, 'main_layout'):
                for i in range(self.main_layout.count()):
                    item = self.main_layout.itemAt(i)
                    widget = item.widget() if item else None
                    if widget:
                        widget.setVisible(True)
                        widget.show()
                        widget.raise_()
                    verbose("レイアウト子要素[{i}]: {widget}, 表示状態: {widget.isVisible() if widget else 'None'}")
            
            # スプリッター自体の表示を確認
            verbose("スプリッター親ウィジェット: {self.main_splitter.parent()}")
            
            # スプリッター自体を明示的に表示
            self.main_splitter.show()
            self.main_splitter.raise_()
            verbose("スプリッター show() 後表示状態: {self.main_splitter.isVisible()}")
            
            # メインウィンドウの表示を確実にする
            self.show()  # メインウィンドウを表示
            self.raise_()  # 前面に
            
            # 表示後に子要素の状態を再確認・修正
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(100, self._ensure_panels_visible)
            
            # スプリッターの可視性確認
            verbose("スプリッター表示状態: {self.main_splitter.isVisible()}")
            verbose("スプリッターサイズ: {self.main_splitter.size()}")
            verbose("スプリッター実際のサイズ: {self.main_splitter.sizes()}")
        else:
            error("main_splitterが利用できません")
        
        # アドレスバーマネージャーにコンポーネントを設定
        if self.address_bar_manager and hasattr(self, 'address_bar') and self.address_bar:
            try:
                # フォルダハンドラーの参照を取得
                folder_handler = self.folder_event_handler if hasattr(self, 'folder_event_handler') else None
                
                # アドレスバーマネージャーにコンポーネントを設定
                self.address_bar_manager.set_components(self.address_bar, folder_handler)
                debug(f"✅ アドレスバーマネージャーにコンポーネント設定完了: address_bar={self.address_bar}, folder_handler={folder_handler}")
                
                # アドレスバーにプレースホルダーテキストを設定
                self.address_bar_manager.set_placeholder_text("フォルダパスを入力または選択...")
                
            except Exception as e:
                error(f"アドレスバーマネージャー設定エラー: {e}")
                import traceback
                traceback.print_exc()
        else:
            warning(f"アドレスバーマネージャー設定スキップ: manager={bool(self.address_bar_manager if hasattr(self, 'address_bar_manager') else False)}, address_bar={bool(getattr(self, 'address_bar', None))}")
    
    def _connect_event_handlers(self):
        """イベントハンドラの接続"""
        # フォルダ選択ボタン
        if self.folder_event_handler:
            self.folder_btn.clicked.connect(self.folder_event_handler.select_folder)
            
            # フォルダイベントハンドラーにUIコンポーネント参照を設定
            thumbnail_list_ref = getattr(self, 'thumbnail_list', None)
            folder_content_list_ref = getattr(self, 'folder_content_list', None)
            address_bar_ref = getattr(self, 'address_bar', None)
            
            debug("コンポーネント参照取得:")
            debug(f"  - address_bar: {address_bar_ref}")
            debug(f"  - folder_content_list: {folder_content_list_ref}")
            debug(f"  - thumbnail_list: {thumbnail_list_ref}")
            
            # ナビゲーションコントロールを取得
            navigation_controls_ref = getattr(self, 'navigation_controls', None)
            if navigation_controls_ref:
                debug("ナビゲーションコントロール参照取得成功: {navigation_controls_ref}")
                
                # ナビゲーション信号の直接接続
                try:
                    navigation_controls_ref.back_requested.connect(self.go_back)
                    navigation_controls_ref.forward_requested.connect(self.go_forward)
                    navigation_controls_ref.parent_folder_requested.connect(self.folder_event_handler.go_to_parent_folder)
                    navigation_controls_ref.home_folder_requested.connect(self.go_to_home_folder)
                    navigation_controls_ref.refresh_requested.connect(self.refresh_current_folder)
                    debug("ナビゲーション信号接続完了")
                except Exception as e:
                    error("ナビゲーション信号接続エラー: {e}")
                    import traceback
                    traceback.print_exc()
            else:
                warning("ナビゲーションコントロール参照取得失敗")
            
            # 正しいシグネチャでコンポーネントを設定
            self.folder_event_handler.set_components(
                address_bar=address_bar_ref,
                folder_content_list=folder_content_list_ref,
                thumbnail_list=thumbnail_list_ref,
                navigation_controls=navigation_controls_ref
            )
            debug("フォルダイベントハンドラーにUIコンポーネント参照を設定")
        
        # テーマ切り替えボタン
        if self.theme_event_handler:
            self.theme_toggle_btn.clicked.connect(self.theme_event_handler.toggle_theme)
        
        # アドレスバー関連
        if self.address_bar_manager and self.folder_event_handler and address_bar_ref:
            # アドレスバーマネージャーにコンポーネントを設定
            self.address_bar_manager.set_components(
                address_bar=address_bar_ref,
                folder_handler=self.folder_event_handler
            )
            debug(f"アドレスバーマネージャーにUIコンポーネント参照を設定: {address_bar_ref}")
        else:
            warning(f"アドレスバー設定スキップ: manager={bool(self.address_bar_manager)}, folder_handler={bool(self.folder_event_handler)}, address_bar={bool(address_bar_ref)}")
        
        # ナビゲーションコントロールのシグナル接続
        if hasattr(self, 'address_bar_manager') and self.address_bar_manager and hasattr(self.address_bar_manager, 'navigation_controls'):
            nav_controls = self.address_bar_manager.navigation_controls
            if nav_controls and self.folder_event_handler:
                try:
                    # 戻るボタン
                    if hasattr(nav_controls, 'back_button'):
                        nav_controls.back_button.clicked.connect(self.go_back)
                    
                    # 進むボタン
                    if hasattr(nav_controls, 'forward_button'):
                        nav_controls.forward_button.clicked.connect(self.go_forward)
                    
                    # 上へボタン（親フォルダ）
                    if hasattr(nav_controls, 'up_button'):
                        nav_controls.up_button.clicked.connect(self.folder_event_handler.go_to_parent_folder)
                    
                    # リフレッシュボタン
                    if hasattr(nav_controls, 'refresh_button'):
                        nav_controls.refresh_button.clicked.connect(self.refresh_current_folder)
                    
                    verbose("ナビゲーションコントロールのシグナル接続完了")
                except Exception as e:
                    error("ナビゲーションコントロールシグナル接続エラー: {e}")
                    import traceback
                    traceback.print_exc()
        
        # 画像イベントハンドラーにUIコンポーネント参照を設定
        if self.image_event_handler:
            try:
                # 正しいコンポーネント名で参照を取得
                image_preview = getattr(self, 'image_preview', None) or getattr(self, 'preview_panel', None)
                map_view = getattr(self, 'map_view', None) or getattr(self, 'map_panel', None)
                status_display = getattr(self, 'status_display_manager', None)
                
                debug("画像イベントハンドラー用コンポーネント検索:")
                debug(f"  - image_preview候補: {image_preview}")
                debug(f"  - map_view候補: {map_view}")
                debug(f"  - status_display: {status_display}")
                
                # 右パネルマネージャーから直接取得を試行
                if not image_preview and hasattr(self, 'right_panel_manager'):
                    image_preview = getattr(self.right_panel_manager, 'preview_panel', None)
                    debug(f"  - 右パネルマネージャーからpreview_panel: {image_preview}")
                
                if not map_view and hasattr(self, 'right_panel_manager'):
                    map_view = getattr(self.right_panel_manager, 'map_panel', None)
                    debug(f"  - 右パネルマネージャーからmap_panel: {map_view}")
                
                self.image_event_handler.set_components(
                    image_preview=image_preview,
                    map_view=map_view,
                    status_display=status_display
                )
                debug("画像イベントハンドラーにUIコンポーネント参照を設定")
            except Exception as e:
                error("画像イベントハンドラーコンポーネント設定エラー: {e}")
                import traceback
                traceback.print_exc()
        
        # 左パネルのイベントハンドラを設定
        if self.left_panel_manager and self.folder_event_handler:
            try:
                self.left_panel_manager.set_event_handlers(
                    self.folder_event_handler.on_folder_item_clicked,
                    self.folder_event_handler.on_folder_item_clicked,  # ダブルクリックも同じ処理
                    self.image_event_handler.on_image_selected if self.image_event_handler else None
                )
                debug("左パネルイベントハンドラを設定")
            except Exception as e:
                error("左パネルイベントハンドラ設定エラー: {e}")
        
        # 右パネルのイベントハンドラを設定
        verbose("右パネル設定条件: right_panel_manager={bool(self.right_panel_manager)}, maximize_handler={bool(self.maximize_handler)}")
        if self.right_panel_manager and self.maximize_handler:
            try:
                # 右パネルマネージャーからコンポーネント参照を取得
                preview_panel = getattr(self.right_panel_manager, 'preview_panel', None)
                map_panel = getattr(self.right_panel_manager, 'map_panel', None)
                
                debug("最大化ハンドラー設定: preview_panel={preview_panel}, map_panel={map_panel}")
                
                if preview_panel and map_panel:
                    self.maximize_handler.set_components(
                        self.main_splitter,
                        preview_panel,
                        map_panel
                    )
                    verbose("最大化ハンドラにコンポーネント参照を設定")
                    
                    # 最大化コンテナを設定
                    maximize_container = self.maximize_handler.create_maximize_container()
                    if maximize_container and hasattr(self, 'maximize_container'):
                        # 既存のコンテナと置き換え
                        old_container = self.maximize_container
                        self.maximize_container = maximize_container
                        if old_container:
                            self.main_layout.removeWidget(old_container)
                            old_container.deleteLater()
                        self.main_layout.addWidget(self.maximize_container)
                        verbose("最大化コンテナを設定")
                    
                    # 右パネルマネージャーにイベントハンドラを設定
                    self.right_panel_manager.set_event_handlers(
                        self.maximize_handler.toggle_image_maximize,
                        self.maximize_handler.toggle_map_maximize
                    )
                    verbose("右パネルイベントハンドラを設定")
                else:
                    warning("プレビューパネルまたはマップパネルが見つかりません: preview={preview_panel}, map={map_panel}")
                    
            except Exception as e:
                error("右パネルイベントハンドラ設定エラー: {e}")
                import traceback
                traceback.print_exc()
        else:
            warning("右パネルイベントハンドラー設定スキップ: right_panel_manager={bool(getattr(self, 'right_panel_manager', None))}, maximize_handler={bool(getattr(self, 'maximize_handler', None))}")
    
    def show_status_message(self, message, timeout=0):
        """ステータスバーにメッセージを表示"""
        try:
            status_bar = self.statusBar()
            if status_bar:
                status_bar.showMessage(message, timeout)
            else:
                pass  # ステータスバーが無い場合は何もしない
        except Exception as e:
            import logging
            logging.error(f"ステータス表示エラー: {e}, メッセージ: {message}")
    
    def finalize_setup(self):
        """セットアップの最終処理"""
        # テーマコンポーネント登録（一時的にスキップ）
        try:
            if hasattr(self, 'register_theme_component'):
                self.register_theme_component(self.folder_btn, "button")
                self.register_theme_component(self.theme_toggle_btn, "button") 
                self.register_theme_component(self.parent_button, "button")
                self.register_theme_component(self.toolbar_widget, "panel")
                
                # ナビゲーションコントロールをテーマシステムに登録
                if hasattr(self, 'controls_widget') and self.controls_widget:
                    # controls_widgetの子要素からNavigationControlsを探す
                    from ui.controls.toolbar.navigation_controls import NavigationControls
                    for child in self.controls_widget.findChildren(NavigationControls):
                        self.register_theme_component(child, "navigation_controls")
                        verbose("ナビゲーションコントロールをテーマシステムに登録: {child}")
                        # 個別のボタンも登録
                        if hasattr(child, 'back_button') and child.back_button:
                            self.register_theme_component(child.back_button, "button")
                        if hasattr(child, 'forward_button') and child.forward_button:
                            self.register_theme_component(child.forward_button, "button")
                        if hasattr(child, 'parent_button') and child.parent_button:
                            self.register_theme_component(child.parent_button, "button")
                        break
        except Exception as e:
            error(f"テーマコンポーネント登録エラー: {e}")
        
        # 初期テーマ設定
        try:
            if hasattr(self, 'theme_event_hdlr') and self.theme_event_hdlr:
                # テーマの初期化を実行
                self.theme_event_hdlr.initialize_theme()
            elif hasattr(self, 'theme_event_handler') and self.theme_event_handler:
                # レガシー属性名
                self.theme_event_handler.initialize_theme()
        except Exception as e:
            error(f"テーマイベントハンドラーエラー: {e}")
        
        try:
            if hasattr(self, 'apply_theme'):
                self.apply_theme()
        except Exception as e:
            error(f"テーマ適用エラー: {e}")
        
        # ステータス更新
        self.show_status_message("新UI (Clean Architecture) v2.2.0 で起動しました")
        
        # StatusDisplayManagerにステータスラベルを設定
        if self.status_display_manager and hasattr(self, 'status_info'):
            try:
                self.status_display_manager.set_components(status_info=self.status_info)
                verbose("StatusDisplayManagerにステータスラベルを設定完了")
            except Exception as e:
                error(f"StatusDisplayManagerのステータスラベル設定エラー: {e}")
                import traceback
                traceback.print_exc()
        
        # ImageEventHandlerにStatusDisplayManagerを設定
        if self.image_event_handler and self.status_display_manager:
            try:
                # ImageEventHandlerにEXIF表示用のコールバックを設定
                self.image_event_handler.status_display_manager = self.status_display_manager
                verbose("ImageEventHandlerにStatusDisplayManagerを設定完了")
            except Exception as e:
                error("ImageEventHandlerのStatusDisplayManager設定エラー: {e}")
    
    # ナビゲーション機能
    def go_back(self):
        """戻る機能"""
        try:
            debug("戻るボタンがクリックされました")
            if self.folder_event_handler:
                self.folder_event_handler.go_back()
                verbose("戻る処理を実行しました")
            else:
                self.show_status_message("❌ フォルダイベントハンドラが見つかりません")
                error("フォルダイベントハンドラが見つかりません")
        except Exception as e:
            self.show_status_message(f"❌ 戻る機能エラー: {e}")
            logging.error(f"戻る機能エラー: {e}")
            error("戻る機能エラー: {e}")
    
    def go_forward(self):
        """進む機能"""
        try:
            debug("進むボタンがクリックされました")
            if self.folder_event_handler:
                self.folder_event_handler.go_forward()
                verbose("進む処理を実行しました")
            else:
                self.show_status_message("❌ フォルダイベントハンドラが見つかりません")
                error("フォルダイベントハンドラが見つかりません")
        except Exception as e:
            self.show_status_message(f"❌ 進む機能エラー: {e}")
            logging.error(f"進む機能エラー: {e}")
            error("進む機能エラー: {e}")
    
    def refresh_current_folder(self):
        """現在のフォルダをリフレッシュ"""
        try:
            if self.folder_event_handler:
                self.folder_event_handler.refresh_current_folder()
            else:
                self.show_status_message("❌ フォルダイベントハンドラが見つかりません")
                error("フォルダイベントハンドラが見つかりません")
        except Exception as e:
            self.show_status_message(f"❌ リフレッシュエラー: {e}")
            logging.error(f"リフレッシュエラー: {e}")
    
    def resizeEvent(self, event):
        """ウィンドウリサイズイベント - 右パネルのアンカリングを維持"""
        super().resizeEvent(event)
        
        try:
            # メインスプリッターが存在する場合
            if hasattr(self, 'main_splitter') and self.main_splitter:
                # ウィンドウサイズに応じてスプリッターサイズを動的調整
                total_width = self.width()
                left_width = min(450, total_width * 0.3)  # 左パネルは最大450px、全体の30%まで
                right_width = total_width - left_width - 20  # 右パネルは残り（マージン考慮）
                
                # 最小サイズを保証
                if right_width < 600:
                    left_width = max(300, total_width - 600)
                    right_width = total_width - left_width
                
                self.main_splitter.setSizes([int(left_width), int(right_width)])
                
                # 右スプリッターも同様に調整
                if hasattr(self, 'right_splitter') and self.right_splitter:
                    total_height = self.height() - 100  # ツールバー等を除く
                    preview_height = total_height * 0.55  # プレビューは55%
                    map_height = total_height * 0.45     # マップは45%
                    self.right_splitter.setSizes([int(preview_height), int(map_height)])
                
        except Exception as e:
            warning("リサイズイベントエラー（無視）: {e}")
    
    def _ensure_panels_visible(self):
        """メインウィンドウ表示後にパネルの表示状態を確認・修正"""
        debug("パネル表示状態の最終確認・修正開始")
        
        if hasattr(self, 'main_splitter') and self.main_splitter:
            # スプリッター子要素の強制表示
            for i in range(self.main_splitter.count()):
                widget = self.main_splitter.widget(i)
                if widget:
                    widget.show()
                    widget.setVisible(True)
                    widget.update()
                    debug("強制表示後 子要素[{i}]: 表示状態={widget.isVisible()}")
            
            # スプリッター自体の状態確認
            self.main_splitter.show()
            self.main_splitter.update()
            debug("最終スプリッター表示状態: {self.main_splitter.isVisible()}")
            debug("最終スプリッター実際サイズ: {self.main_splitter.sizes()}")
        
        debug("パネル表示状態確認完了")
    
    def go_to_home_folder(self):
        """ホームフォルダに移動"""
        try:
            debug("ホームボタンがクリックされました")
            if self.folder_event_handler:
                # ホームフォルダのパスを取得
                import os
                home_path = os.path.expanduser("~")
                debug(f"ホームフォルダパス: {home_path}")
                
                # フォルダイベントハンドラーでフォルダを開く
                self.folder_event_handler.load_folder(home_path)
                self.show_status_message(f"🏠 ホームフォルダに移動: {home_path}")
                verbose("ホームフォルダ移動処理を実行しました")
            else:
                self.show_status_message("❌ フォルダイベントハンドラが見つかりません")
                error("フォルダイベントハンドラが見つかりません")
        except Exception as e:
            self.show_status_message(f"❌ ホームフォルダ移動エラー: {e}")
            logging.error(f"ホームフォルダ移動エラー: {e}")
            error(f"ホームフォルダ移動エラー: {e}")
