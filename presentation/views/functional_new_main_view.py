"""
修正版新UIメインビュー

実際の機能を持つ新UIメインウィンドウ
v2.1.0: ダークモード・ライトモード切り替え対応
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QSplitter, QWidget, 
                            QStatusBar, QHBoxLayout, QPushButton, QLabel,
                            QGroupBox, QFileDialog, QMessageBox, QListWidget, QListWidgetItem, QLineEdit, QApplication)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

# コントロールのインポート
from ui.controls import create_controls

# テーマシステム
from presentation.themes import ThemeAwareMixin, get_theme_manager, ThemeMode


class FunctionalNewMainWindow(QMainWindow, ThemeAwareMixin):
    """
    機能的な新UIメインウィンドウ
    
    実際にフォルダ選択、画像表示、マップ表示が動作します。
    v2.1.0: ダークモード・テーマ切り替え対応
    """
    
    def __init__(self):
        QMainWindow.__init__(self)
        ThemeAwareMixin.__init__(self)
        
        self.setWindowTitle("PhotoMap Explorer - 新UI (Clean Architecture) v2.1.2")
        self.setGeometry(100, 100, 1400, 900)
        
        # 現在の状態
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        
        # 最大化状態管理
        self.maximized_state = None  # 'image', 'map', None
        self.main_splitter = None
        self.right_splitter = None
        self.maximize_container = None
        self.original_preview_parent = None
        self.original_map_parent = None
        
        # コンポーネント参照
        self.thumbnail_list = None
        self.preview_panel = None
        self.map_panel = None
        self.folder_panel = None
        self.address_bar = None  # GIMP風アドレスバー
        
        # アイコン設定
        self._setup_icon()
        
        # UI構築
        self._setup_ui()
        
        # 初期フォルダ設定
        self._load_initial_folder()
        
        # 初期マップ画面表示
        self._show_initial_map_screen()
        
        # ステータス表示
        self.show_status_message("新UI (Clean Architecture) で起動しました")
    
    def show_status_message(self, message, timeout=0):
        """ステータスバーにメッセージを表示"""
        try:
            if hasattr(self, 'statusBar') and self.statusBar():
                self.statusBar().showMessage(message, timeout)
                # 正常稼働時の標準出力は抑制
            else:
                # ステータスバーが無い場合のみフォールバック出力
                pass
        except Exception as e:
            # エラー時のみログ出力（デバッグ目的）
            import logging
            logging.error(f"ステータス表示エラー: {e}, メッセージ: {message}")
    
    def _setup_icon(self):
        """アイコン設定"""
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # ツールバーとGIMP風アドレスバー
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(5, 2, 5, 2)
        
        # フォルダ選択ボタン
        folder_btn = QPushButton("📁 フォルダ選択")
        folder_btn.setMaximumHeight(30)
        folder_btn.clicked.connect(self._select_folder)
        toolbar_layout.addWidget(folder_btn)
        
        # GIMP風アドレスバーコントロール
        controls_widget, self.address_bar, parent_button = create_controls(
            self._on_address_changed, 
            self._go_to_parent_folder
        )
        controls_widget.setMaximumHeight(35)
        toolbar_layout.addWidget(controls_widget, 1)  # アドレスバーを拡張
        
        # ダークモード切り替えボタン
        self.theme_toggle_btn = QPushButton("🌙 ダーク")
        self.theme_toggle_btn.setMaximumHeight(30)
        self.theme_toggle_btn.setMaximumWidth(80)
        self.theme_toggle_btn.setToolTip("ダークモード・ライトモード切り替え")
        self.theme_toggle_btn.clicked.connect(self._toggle_theme)
        toolbar_layout.addWidget(self.theme_toggle_btn)
        
        # テーマコンポーネント登録
        self.register_theme_component(folder_btn, "button")
        self.register_theme_component(self.theme_toggle_btn, "button")
        self.register_theme_component(parent_button, "button")  # 親フォルダボタンも登録
        
        # アドレスバーとツールバーの参照保存（後でテーマ適用）
        self.folder_btn = folder_btn
        self.controls_widget = controls_widget
        
        # ツールバーウィジェットを作成
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setMaximumHeight(40)
        layout.addWidget(toolbar_widget)
        
        # ツールバーのテーマコンポーネント登録
        self.toolbar_widget = toolbar_widget
        self.register_theme_component(toolbar_widget, "panel")
        
        # メインスプリッター
        self.main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(self.main_splitter)
        
        # 左パネル：フォルダとサムネイル
        left_panel = self._create_left_panel()
        self.left_panel = left_panel  # 参照を保存
        self.main_splitter.addWidget(left_panel)
        
        # 右パネル：プレビューとマップ
        right_panel = self._create_right_panel()
        self.main_splitter.addWidget(right_panel)
        
        # 最大化用コンテナ（初期は非表示）
        self._create_maximize_container()
        layout.addWidget(self.maximize_container)
        self.maximize_container.hide()
        
        # ステータスバー
        self.statusBar().showMessage("準備完了")
        
        # スプリッターサイズ調整
        self.main_splitter.setSizes([600, 800])
        
        # 初期テーマ設定（Windowsシステム設定に連動）
        self._update_theme_button()
        self.apply_theme()
        
        # アドレスバーの初期テーマ適用を遅延実行
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(100, self._apply_delayed_theme)
    
    def _create_left_panel(self):
        """左パネル作成"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # フォルダパネル（現在のフォルダ内容表示）
        folder_group = QGroupBox("📁 フォルダ内容")
        folder_layout = QVBoxLayout(folder_group)
        
        # フォルダ内容リスト（ツリー表示廃止）
        self.folder_content_list = QListWidget()
        self.folder_content_list.setMinimumHeight(150)
        
        # クリック・ダブルクリックイベント
        self.folder_content_list.itemClicked.connect(self._on_folder_item_clicked)
        self.folder_content_list.itemDoubleClicked.connect(self._on_folder_item_double_clicked)
        
        folder_layout.addWidget(self.folder_content_list)
        layout.addWidget(folder_group)
        
        # サムネイルパネル
        thumbnail_group = QGroupBox("🖼️ サムネイル")
        thumbnail_layout = QVBoxLayout(thumbnail_group)
        
        try:
            from ui.thumbnail_list import create_thumbnail_list
            self.thumbnail_list = create_thumbnail_list(self._on_image_selected)
            thumbnail_layout.addWidget(self.thumbnail_list)
        except Exception as e:
            error_label = QLabel(f"サムネイルエラー: {e}")
            error_label.setStyleSheet("color: red;")
            thumbnail_layout.addWidget(error_label)
        
        # サムネイル関連の参照を保存（テーマ適用用）
        self.thumbnail_group = thumbnail_group
        self.thumbnail_layout = thumbnail_layout
        
        layout.addWidget(thumbnail_group)
        
        # 詳細ステータスパネル
        status_group = QGroupBox("📋 詳細情報")
        status_layout = QVBoxLayout(status_group)
        
        # ステータス表示ラベル
        self.status_info = QLabel("画像を選択すると詳細情報が表示されます")
        self.status_info.setWordWrap(True)
        self.status_info.setMinimumHeight(120)
        self.status_info.setMaximumHeight(180)
        
        status_layout.addWidget(self.status_info)
        layout.addWidget(status_group)
        
        # テーマコンポーネント登録
        self.register_theme_component(folder_group, "group_box")
        self.register_theme_component(self.folder_content_list, "list_widget")
        self.register_theme_component(thumbnail_group, "group_box")
        self.register_theme_component(status_group, "group_box")
        self.register_theme_component(self.status_info, "status_info")
        self.register_theme_component(panel, "panel")  # 左パネル全体
        
        return panel
    
    def _create_right_panel(self):
        """右パネル作成"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 上下スプリッター
        self.right_splitter = QSplitter(Qt.Vertical)
        layout.addWidget(self.right_splitter)
        
        # プレビューパネル
        preview_group = QGroupBox("🖼️ プレビュー")
        # 初期スタイルは apply_theme で設定される
        preview_layout = QVBoxLayout(preview_group)
        
        # プレビューヘッダー（タイトル + 最大化ボタン）
        preview_header = QHBoxLayout()
        preview_title = QLabel("画像プレビュー")
        preview_title.setStyleSheet("font-weight: normal; color: #666; font-size: 11px;")
        preview_header.addWidget(preview_title)
        preview_header.addStretch()  # 右寄せ
        
        # 最大化ボタン（改良版）
        self.maximize_image_btn = QPushButton("⛶")
        self.maximize_image_btn.setToolTip("画像を最大化表示（ダブルクリックでも可能）")
        self.maximize_image_btn.setMaximumSize(28, 28)
        self.maximize_image_btn.clicked.connect(self.toggle_image_maximize)
        preview_header.addWidget(self.maximize_image_btn)
        
        preview_header_widget = QWidget()
        preview_header_widget.setLayout(preview_header)
        preview_header_widget.setMaximumHeight(32)
        preview_layout.addWidget(preview_header_widget)
        
        try:
            from ui.image_preview import create_image_preview
            self.preview_panel = create_image_preview()
            # ダブルクリック最大化イベント追加（改良版）
            if hasattr(self.preview_panel, 'mouseDoubleClickEvent'):
                original_double_click = getattr(self.preview_panel, 'mouseDoubleClickEvent', None)
                def enhanced_double_click(event):
                    self.toggle_image_maximize()
                    if original_double_click:
                        original_double_click(event)
                self.preview_panel.mouseDoubleClickEvent = enhanced_double_click
            else:
                self.preview_panel.mouseDoubleClickEvent = self._on_preview_double_click
            preview_layout.addWidget(self.preview_panel)
        except Exception as e:
            error_label = QLabel(f"プレビューエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            preview_layout.addWidget(error_label)
        
        self.right_splitter.addWidget(preview_group)
        
        # マップパネル
        map_group = QGroupBox("🗺️ マップ")
        # 初期スタイルは apply_theme で設定される
        map_layout = QVBoxLayout(map_group)
        
        # マップヘッダー（タイトル + 最大化ボタン）
        map_header = QHBoxLayout()
        map_title = QLabel("撮影場所マップ")
        map_title.setStyleSheet("font-weight: normal; color: #666; font-size: 11px;")
        map_header.addWidget(map_title)
        map_header.addStretch()  # 右寄せ
        
        # 最大化ボタン（改良版）
        self.maximize_map_btn = QPushButton("⛶")
        self.maximize_map_btn.setToolTip("マップを最大化表示（ダブルクリックでも可能）")
        self.maximize_map_btn.setMaximumSize(28, 28)
        self.maximize_map_btn.clicked.connect(self.toggle_map_maximize)
        map_header.addWidget(self.maximize_map_btn)
        
        map_header_widget = QWidget()
        map_header_widget.setLayout(map_header)
        map_header_widget.setMaximumHeight(32)
        map_layout.addWidget(map_header_widget)
        
        try:
            from ui.map_panel import create_map_panel
            self.map_panel = create_map_panel()
            # ダブルクリック最大化イベント追加（改良版）
            if hasattr(self.map_panel, 'mouseDoubleClickEvent'):
                original_double_click = getattr(self.map_panel, 'mouseDoubleClickEvent', None)
                def enhanced_double_click(event):
                    self.toggle_map_maximize()
                    if original_double_click:
                        original_double_click(event)
                self.map_panel.mouseDoubleClickEvent = enhanced_double_click
            else:
                self.map_panel.mouseDoubleClickEvent = self._on_map_double_click
            map_layout.addWidget(self.map_panel)
        except Exception as e:
            error_label = QLabel(f"マップエラー: {e}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            map_layout.addWidget(error_label)
        
        self.right_splitter.addWidget(map_group)
        
        # スプリッターサイズ調整
        self.right_splitter.setSizes([400, 400])
        
        # テーマコンポーネント登録
        self.register_theme_component(preview_group, "group_box")
        self.register_theme_component(self.maximize_image_btn, "maximize_button")
        self.register_theme_component(map_group, "group_box")
        self.register_theme_component(self.maximize_map_btn, "maximize_button")
        self.register_theme_component(panel, "panel")  # 右パネル全体
        
        return panel
    
    def _create_maximize_container(self):
        """最大化表示用のコンテナ作成"""
        self.maximize_container = QWidget()
        maximize_layout = QVBoxLayout(self.maximize_container)
        
        # 最大化時のトップバー
        topbar = QHBoxLayout()
        
        # 復元ボタン（サイズを大きくしてフォントが潰れないようにする）
        self.restore_btn = QPushButton("◱ 通常表示に戻る")
        self.restore_btn.setToolTip("通常表示に戻る")
        self.restore_btn.setMinimumSize(120, 35)  # 最小サイズを指定
        self.restore_btn.setMaximumHeight(35)
        self.restore_btn.clicked.connect(self.restore_normal_view)
        
        topbar.addStretch()
        topbar.addWidget(self.restore_btn)
        
        topbar_widget = QWidget()
        topbar_widget.setLayout(topbar)
        topbar_widget.setMaximumHeight(40)  # 高さを少し増やす
        
        maximize_layout.addWidget(topbar_widget)
        
        # 最大化されたコンテンツエリア
        self.maximized_content_area = QWidget()
        self.maximized_content_layout = QVBoxLayout(self.maximized_content_area)
        maximize_layout.addWidget(self.maximized_content_area)
        
        # テーマコンポーネント登録
        self.register_theme_component(self.restore_btn, "button")
        self.register_theme_component(self.maximize_container, "panel")
        self.register_theme_component(topbar_widget, "panel")
        self.register_theme_component(self.maximized_content_area, "panel")
    
    def toggle_image_maximize(self):
        """画像最大化の切り替え"""
        if self.maximized_state == 'image':
            self.restore_normal_view()
        else:
            self._maximize_preview()
    
    def toggle_map_maximize(self):
        """マップ最大化の切り替え"""
        if self.maximized_state == 'map':
            self.restore_normal_view()
        else:
            self._maximize_map()
    
    def _maximize_preview(self):
        """プレビューを最大化"""
        if not self.preview_panel:
            return
        
        # 現在の親を記録
        self.original_preview_parent = self.preview_panel.parent()
        
        # プレビューパネルを最大化エリアに移動
        self.preview_panel.setParent(None)
        self.maximized_content_layout.addWidget(self.preview_panel)
        
        # UIの切り替え
        self.main_splitter.hide()
        self.maximize_container.show()
        
        self.maximized_state = 'image'
        
        # 最大化状態での画像表示更新
        self._refresh_maximized_content()
    
    def _maximize_map(self):
        """マップを最大化"""
        if not self.map_panel:
            return
        
        # 現在の親を記録
        self.original_map_parent = self.map_panel.parent()
        
        # マップパネルを最大化エリアに移動
        self.map_panel.setParent(None)
        self.maximized_content_layout.addWidget(self.map_panel)
        
        # UIの切り替え
        self.main_splitter.hide()
        self.maximize_container.show()
        
        self.maximized_state = 'map'
        
        # 最大化状態での表示更新
        self._refresh_maximized_content()
    
    def restore_normal_view(self):
        """通常表示に復元"""
        if self.maximized_state == 'image' and self.preview_panel:
            # プレビューパネルを元の場所に戻す
            self.maximized_content_layout.removeWidget(self.preview_panel)
            self.original_preview_parent.layout().addWidget(self.preview_panel)
            
        elif self.maximized_state == 'map' and self.map_panel:
            # マップパネルを元の場所に戻す
            self.maximized_content_layout.removeWidget(self.map_panel)
            self.original_map_parent.layout().addWidget(self.map_panel)
        
        # UIの切り替え
        self.maximize_container.hide()
        self.main_splitter.show()
        
        self.maximized_state = None
        
        # 通常表示での内容更新
        self._refresh_normal_content()
    
    def _refresh_maximized_content(self):
        """最大化状態でのコンテンツ更新"""
        if self.selected_image:
            if self.maximized_state == 'image':
                self._update_preview_display(self.selected_image)
            elif self.maximized_state == 'map':
                self._update_map_display(self.selected_image)
    
    def _refresh_normal_content(self):
        """通常表示でのコンテンツ更新"""
        if self.selected_image:
            self._update_preview_display(self.selected_image)
            self._update_map_display(self.selected_image)
    
    def _on_preview_double_click(self, event):
        """プレビューエリアのダブルクリックイベント"""
        self.toggle_image_maximize()
    
    def _on_map_double_click(self, event):
        """マップエリアのダブルクリックイベント"""
        self.toggle_map_maximize()
    
    def _select_folder(self):
        """フォルダ選択ダイアログ（標準的なフォルダ選択）"""
        try:
            folder = QFileDialog.getExistingDirectory(
                self,
                "フォルダを選択してください",
                self.current_folder if self.current_folder else os.path.expanduser("~"),
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            
            if folder:
                folder = os.path.normpath(folder)
                self._load_folder(folder)
                self.show_status_message(f"📁 フォルダ選択: {folder}")
                
        except Exception as e:
            print(f"フォルダ選択ダイアログエラー: {e}")
            self.show_status_message("❌ フォルダ選択に失敗しました")
            
            if folder:
                folder = os.path.normpath(folder)
                self._load_folder(folder)
                self.show_status_message(f"📁 フォルダ選択: {folder}")
                
        except Exception as e:
            print(f"フォールバックダイアログエラー: {e}")
            self.show_status_message("❌ フォルダ選択に失敗しました")
    
    def _load_initial_folder(self):
        """初期フォルダ読み込み（空の状態で開始）"""
        # アドレスバーを空に設定
        if self.address_bar:
            self.address_bar.setText("")
        
        # 初期状態では何も読み込まない
        self.current_folder = None
        self.current_images = []
        
        # コメントアウト: 自動的に初期フォルダを読み込まない
        # デスクトップまたはピクチャフォルダから開始
        # initial_paths = [
        #     os.path.join(os.path.expanduser("~"), "Pictures"),
        #     os.path.join(os.path.expanduser("~"), "Desktop"), 
        #     os.path.expanduser("~")
        # ]
        # 
        # for path in initial_paths:
        #     if os.path.exists(path):
        #         self._load_folder(path)
        #         break
    
    def _load_folder(self, folder_path):
        """フォルダ読み込み"""
        try:
            # パスを正規化
            folder_path = os.path.normpath(folder_path)
            self.current_folder = folder_path
            
            # アドレスバーを更新（パス正規化後）
            if self.address_bar:
                # 一度クリアしてから再設定することで正しい分解を保証
                self.address_bar.setText("")
                self.address_bar.setText(folder_path)
            
            # 画像ファイル検索（サムネイル処理用にフィルタリング）
            # フォルダ選択ダイアログでは全ファイル表示、ここで画像のみ抽出
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
            image_files = []
            
            folder = Path(folder_path)
            for file_path in folder.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    image_files.append(str(file_path))
            
            self.current_images = image_files
            
            # フォルダ内容表示を更新（修正版）
            self._update_folder_content(folder_path)
            
            # サムネイル更新（修正版）
            thumbnail_list = self.thumbnail_list
            
            # サムネイルリストの参照が失われている場合、再取得を試行
            if thumbnail_list is None:
                try:
                    from ui.thumbnail_list import ThumbnailListWidget
                    thumbnail_widgets = self.findChildren(ThumbnailListWidget)
                    if thumbnail_widgets:
                        thumbnail_list = thumbnail_widgets[0]
                        self.thumbnail_list = thumbnail_list  # 参照を修復
                except Exception:
                    pass
            
            if thumbnail_list is not None:
                thumbnail_list.clear()
                
                # 画像ファイルを一つずつ追加
                added_count = 0
                for image_path in image_files[:50]:  # 最初の50枚まで
                    try:
                        # ThumbnailListWidgetの場合
                        if hasattr(thumbnail_list, 'add_thumbnail'):
                            success = thumbnail_list.add_thumbnail(image_path)
                            if success:
                                added_count += 1
                        else:
                            # レガシー関数の場合
                            from ui.thumbnail_list import add_thumbnail
                            add_thumbnail(thumbnail_list, image_path)
                            added_count += 1
                    except Exception as e:
                        # エラーログを適切に処理（標準出力ではなくログへ）
                        import logging
                        logging.warning(f"サムネイル追加エラー({image_path}): {e}")
                        continue
                
                # 追加結果を表示
                self.show_status_message(f"📁 {len(image_files)}枚発見、{added_count}枚のサムネイル表示: {folder_path}")
            else:
                self.show_status_message(f"📁 {len(image_files)}枚の画像を読み込みました: {folder_path}")
            
        except Exception as e:
            QMessageBox.warning(self, "エラー", f"フォルダ読み込みエラー: {e}")
            self.show_status_message(f"❌ フォルダ読み込みエラー: {e}")
    
    def _update_folder_content(self, folder_path):
        """フォルダ内容を更新表示"""
        try:
            # フォルダ内容リストの参照を確認・取得
            folder_content_list = self.folder_content_list
            
            # もしNoneの場合、UIから直接取得を試行
            if folder_content_list is None:
                # 親ウィンドウから QListWidget を検索
                try:
                    list_widgets = self.findChildren(QListWidget)
                    if list_widgets:
                        folder_content_list = list_widgets[0]  # まず最初のQListWidgetを使用
                        self.folder_content_list = folder_content_list  # 参照を修復
                    else:
                        return
                except Exception:
                    return
            
            if folder_content_list is None:
                return
            
            # QListWidgetのclearを安全に実行
            try:
                folder_content_list.clear()
            except Exception:
                return
            
            if not folder_path or not os.path.exists(folder_path):
                return
            
            folder = Path(folder_path)
            
            # 親フォルダへのリンク（ルートでない場合）
            if folder.parent != folder:
                parent_item = QListWidgetItem("📁 .. (親フォルダ)")
                parent_item.setData(Qt.UserRole, str(folder.parent))
                parent_item.setToolTip(str(folder.parent))
                try:
                    folder_content_list.addItem(parent_item)
                except Exception:
                    pass
            
            # フォルダとファイルを取得
            items = []
            added_items = 0
            
            try:
                for item_path in folder.iterdir():
                    if item_path.is_dir():
                        # フォルダ
                        folder_item = QListWidgetItem(f"📁 {item_path.name}")
                        folder_item.setData(Qt.UserRole, str(item_path))
                        folder_item.setToolTip(str(item_path))
                        items.append((folder_item, 0))  # フォルダは先頭
                    elif item_path.is_file():
                        # ファイル（画像ファイルを優先表示）
                        file_ext = item_path.suffix.lower()
                        if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                            file_item = QListWidgetItem(f"🖼️ {item_path.name}")
                            file_item.setData(Qt.UserRole, str(item_path))
                            file_item.setToolTip(str(item_path))
                            items.append((file_item, 1))  # 画像ファイルは2番目
                        else:
                            file_item = QListWidgetItem(f"📄 {item_path.name}")
                            file_item.setData(Qt.UserRole, str(item_path))
                            file_item.setToolTip(str(item_path))
                            items.append((file_item, 2))  # その他ファイルは最後
            
            except PermissionError:
                error_item = QListWidgetItem("❌ アクセス権限がありません")
                try:
                    folder_content_list.addItem(error_item)
                except Exception:
                    pass
                return
            
            # ソートして追加（フォルダ→画像→その他ファイル）
            items.sort(key=lambda x: (x[1], x[0].text()))
            
            for item, _ in items:
                try:
                    folder_content_list.addItem(item)
                except Exception:
                    pass
            
            # ステータス更新
            folder_count = len([i for i, t in items if t == 0])
            image_count = len([i for i, t in items if t == 1])
            other_count = len([i for i, t in items if t == 2])
            
            self.show_status_message(
                f"📁 フォルダ: {folder_count}, 🖼️ 画像: {image_count}, 📄 その他: {other_count}"
            )
            
        except Exception as e:
            self.show_status_message(f"❌ フォルダ内容表示エラー: {e}")
            # エラーログを適切に処理
            import logging
            logging.error(f"フォルダ内容表示詳細エラー: {e}")
    
    def _on_folder_changed(self, folder_path):
        """フォルダ変更時の処理"""
        self._load_folder(folder_path)
    
    def _on_image_selected(self, item):
        """画像選択時の処理"""
        try:
            image_path = None
            
            # 複数の方法でパスを取得
            if hasattr(item, 'data') and hasattr(item.data, '__call__'):
                # Qt.UserRoleからパスを取得
                try:
                    image_path = item.data(Qt.UserRole)
                except:
                    pass
            
            # ファイル名から完全パスを構築
            if not image_path and hasattr(item, 'text'):
                filename = item.text()
                if self.current_folder and filename:
                    image_path = os.path.join(self.current_folder, filename)
            
            # 直接テキストからパスを取得
            if not image_path and hasattr(item, 'text'):
                text = item.text()
                if text and os.path.exists(text):
                    image_path = text
            
            # パスが取得できた場合の処理
            if image_path and os.path.exists(image_path):
                self.selected_image = image_path
                self._display_image(image_path)
                self.show_status_message(f"🖼️ 画像選択: {os.path.basename(image_path)}")
            else:
                self.show_status_message(f"❌ 画像パスが取得できません: {item}")
                
        except Exception as e:
            self.show_status_message(f"❌ 画像選択エラー: {e}")
            # エラーログを適切に処理
            import logging
            logging.error(f"画像選択詳細エラー: {e}")
            import traceback
            logging.error(traceback.format_exc())
    
    def _display_image(self, image_path):
        """画像表示"""
        try:
            # プレビュー表示
            if self.preview_panel:
                from PyQt5.QtGui import QPixmap
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    if hasattr(self.preview_panel, 'set_image'):
                        # ImagePreviewViewの場合
                        self.preview_panel.set_image(pixmap)
                    elif hasattr(self.preview_panel, 'setPixmap'):
                        # QLabel等の場合
                        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                        self.preview_panel.setPixmap(scaled_pixmap)
                    elif hasattr(self.preview_panel, 'update_image'):
                        # カスタム関数の場合
                        self.preview_panel.update_image(image_path)
                    
                    self.show_status_message(f"🖼️ プレビュー表示成功: {os.path.basename(image_path)}")
                else:
                    self.show_status_message("❌ 画像読み込み失敗")
            
            # 詳細情報表示
            self._update_image_status(image_path)
            
            # GPS情報取得してマップ表示
            self._update_map(image_path)
            
        except Exception as e:
            self.show_status_message(f"❌ 画像表示エラー: {e}")
            # エラーログを適切に処理
            import logging
            logging.error(f"画像表示詳細エラー: {e}")
            import traceback
            logging.error(traceback.format_exc())
    
    def _update_map(self, image_path):
        """GPS情報を取得してマップを更新"""
        try:
            if not self.map_panel:
                self.show_status_message("📍 マップパネルが利用できません")
                return
            
            # GPS情報抽出
            from logic.image_utils import extract_gps_coords
            gps_info = extract_gps_coords(image_path)
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                
                # マップ更新
                if hasattr(self.map_panel, 'update_location'):
                    success = self.map_panel.update_location(lat, lon)
                    if success:
                        self.show_status_message(f"📍 マップ表示: {lat:.6f}, {lon:.6f}")
                    else:
                        self.show_status_message("📍 マップ更新に失敗")
                elif hasattr(self.map_panel, 'view'):
                    # HTMLベースのマップ表示
                    gps_html = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px; margin: 0; background-color: {self.get_theme_color('background')}; color: {self.get_theme_color('foreground')};">
                        <div style="background: {self.get_theme_color('group_bg')}; border: 2px solid {self.get_theme_color('accent')}; border-radius: 10px; padding: 20px; max-width: 400px; margin: 0 auto;">
                            <h3 style="color: {self.get_theme_color('accent')}; margin-top: 0;">📍 GPS座標情報</h3>
                            <p style="margin: 10px 0;"><strong>緯度:</strong> {lat:.6f}</p>
                            <p style="margin: 10px 0;"><strong>経度:</strong> {lon:.6f}</p>
                            <p style="margin: 10px 0; color: {self.get_theme_color('muted')};"><strong>画像:</strong> {os.path.basename(image_path)}</p>
                            <div style="margin-top: 15px; padding: 10px; background: {self.get_theme_color('secondary')}; border-radius: 5px;">
                                <small style="color: {self.get_theme_color('muted')};">GPS座標が含まれています</small>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    self.map_panel.view.setHtml(gps_html)
                    # HTMLの強制更新
                    self.map_panel.view.update()
                    self.map_panel.view.repaint()
                    self.show_status_message(f"📍 GPS表示: {lat:.6f}, {lon:.6f}")
                else:
                    self.show_status_message("📍 マップ機能が利用できません")
            else:
                # GPS情報なしの場合
                if hasattr(self.map_panel, 'view'):
                    no_gps_html = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; margin: 0; background-color: {self.get_theme_color('background')}; color: {self.get_theme_color('foreground')};">
                        <div style="background: {self.get_theme_color('group_bg')}; border: 2px solid {self.get_theme_color('warning')}; border-radius: 10px; padding: 30px; max-width: 400px; margin: 0 auto;">
                            <h3 style="color: {self.get_theme_color('warning')}; margin-top: 0;">📍 GPS情報なし</h3>
                            <p style="color: {self.get_theme_color('muted')}; margin: 15px 0;">この画像にはGPS座標が含まれていません。</p>
                            <div style="margin-top: 20px; padding: 10px; background: {self.get_theme_color('secondary')}; border-radius: 5px;">
                                <small style="color: {self.get_theme_color('muted')};">位置情報付きの画像を選択してください</small>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    self.map_panel.view.setHtml(no_gps_html)
                    # HTMLの強制更新
                    self.map_panel.view.update()
                    self.map_panel.view.repaint()
                self.show_status_message("📍 GPS情報が見つかりません")
                
        except Exception as e:
            self.show_status_message(f"❌ マップ更新エラー: {e}")
            import logging
            logging.error(f"マップ更新詳細エラー: {e}")
    
    def _update_preview_display(self, image_path):
        """プレビュー表示を更新（最大化状態対応）"""
        try:
            if not self.preview_panel or not image_path:
                return
            
            from PyQt5.QtGui import QPixmap
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                if hasattr(self.preview_panel, 'set_image'):
                    # ImagePreviewViewの場合
                    self.preview_panel.set_image(pixmap)
                elif hasattr(self.preview_panel, 'setPixmap'):
                    # QLabel等の場合 - 最大化状態に応じてサイズを調整
                    if self.maximized_state == 'image':
                        # 最大化時はより大きくスケール
                        available_size = self.maximize_container.size()
                        max_width = max(800, available_size.width() - 50)
                        max_height = max(600, available_size.height() - 100)
                        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    else:
                        # 通常時
                        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                    self.preview_panel.setPixmap(scaled_pixmap)
                elif hasattr(self.preview_panel, 'update_image'):
                    # カスタム関数の場合
                    self.preview_panel.update_image(image_path)
                
                self.show_status_message(f"🖼️ プレビュー更新: {os.path.basename(image_path)}")
            
        except Exception as e:
            self.show_status_message(f"❌ プレビュー更新エラー: {e}")
            import logging
            logging.error(f"プレビュー更新詳細エラー: {e}")

    def _update_map_display(self, image_path):
        """マップ表示を更新（最大化状態対応）"""
        try:
            if not self.map_panel or not image_path:
                return
            
            # GPS情報抽出
            from logic.image_utils import extract_gps_coords
            gps_info = extract_gps_coords(image_path)
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                
                # マップパネルのupdate_locationメソッドを使用
                if hasattr(self.map_panel, 'update_location'):
                    success = self.map_panel.update_location(lat, lon)
                    if success:
                        self.show_status_message(f"📍 マップ更新: {lat:.6f}, {lon:.6f}")
                    else:
                        self.show_status_message("📍 マップ更新に失敗しました")
                elif hasattr(self.map_panel, 'view'):
                    # 最大化状態でも同じHTML表示を使用
                    html_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px; margin: 0; background-color: {self.get_theme_color('background')}; color: {self.get_theme_color('foreground')};">
                        <div style="background: {self.get_theme_color('group_bg')}; border: 2px solid {self.get_theme_color('accent')}; border-radius: 10px; padding: 20px; max-width: 400px; margin: 0 auto;">
                            <h3 style="color: {self.get_theme_color('accent')}; margin-top: 0;">📍 GPS座標情報</h3>
                            <p style="margin: 10px 0;"><strong>緯度:</strong> {lat:.6f}</p>
                            <p style="margin: 10px 0;"><strong>経度:</strong> {lon:.6f}</p>
                            <p style="margin: 10px 0; color: {self.get_theme_color('muted')};"><strong>画像:</strong> {os.path.basename(image_path)}</p>
                            <div style="margin-top: 15px; padding: 10px; background: {self.get_theme_color('secondary')}; border-radius: 5px;">
                                <small style="color: {self.get_theme_color('muted')};">{"最大化表示中" if self.maximized_state == 'map' else "GPS座標が含まれています"}</small>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    self.map_panel.view.setHtml(html_content)
                    self.show_status_message(f"📍 マップ表示: {lat:.6f}, {lon:.6f}")
                else:
                    self.show_status_message("📍 マップ機能が利用できません")
            else:
                # GPS情報がない場合
                if hasattr(self.map_panel, 'view'):
                    self.map_panel.view.setHtml(f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; margin: 0; background-color: {self.get_theme_color('background')}; color: {self.get_theme_color('foreground')};">
                        <div style="background: {self.get_theme_color('group_bg')}; border: 2px solid {self.get_theme_color('warning')}; border-radius: 10px; padding: 30px; max-width: 400px; margin: 0 auto;">
                            <h3 style="color: {self.get_theme_color('warning')}; margin-top: 0;">📍 GPS情報なし</h3>
                            <p style="color: {self.get_theme_color('muted')}; margin: 15px 0;">この画像にはGPS座標が含まれていません。</p>
                            <div style="margin-top: 20px; padding: 10px; background: {self.get_theme_color('secondary')}; border-radius: 5px;">
                                <small style="color: {self.get_theme_color('muted')};">位置情報付きの画像を選択してください</small>
                            </div>
                        </div>
                    </body>
                    </html>
                    """)
                self.show_status_message("📍 GPS情報が見つかりません")
                
        except Exception as e:
            self.show_status_message(f"❌ マップ更新エラー: {e}")
            import logging
            logging.error(f"マップ更新詳細エラー: {e}")
    
    def _on_folder_item_clicked(self, item):
        """フォルダ項目クリック時の処理"""
        try:
            item_path = item.data(Qt.UserRole)
            if not item_path:
                return
            
            # パス情報をステータスバーに表示
            self.show_status_message(f"📌 選択: {item_path}")
            
        except Exception as e:
            self.show_status_message(f"❌ 項目選択エラー: {e}")
    
    def _on_folder_item_double_clicked(self, item):
        """フォルダ項目ダブルクリック時の処理"""
        try:
            item_path = item.data(Qt.UserRole)
            if not item_path or not os.path.exists(item_path):
                self.show_status_message("❌ パスが見つかりません")
                return
            
            if os.path.isdir(item_path):
                # フォルダの場合：移動
                self._load_folder(item_path)
                self.show_status_message(f"📁 フォルダ移動: {item_path}")
            elif os.path.isfile(item_path):
                # ファイルの場合：画像なら表示
                file_ext = Path(item_path).suffix.lower()
                if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                    self.selected_image = item_path
                    self._display_image(item_path)
                    self.show_status_message(f"🖼️ 画像表示: {os.path.basename(item_path)}")
                else:
                    self.show_status_message(f"📄 ファイル選択: {os.path.basename(item_path)}")
            
        except Exception as e:
            self.show_status_message(f"❌ ダブルクリック処理エラー: {e}")
            # エラーログを適切に処理
            import logging
            logging.error(f"ダブルクリック詳細エラー: {e}")
    
    def _on_address_changed(self, new_path):
        """GIMP風アドレスバーでパスが変更された時"""
        try:
            # パスを正規化
            new_path = os.path.normpath(new_path) if new_path else ""
            
            if new_path and os.path.exists(new_path) and os.path.isdir(new_path):
                # 現在のパスと異なる場合のみロード
                if new_path != self.current_folder:
                    self._load_folder(new_path)
                else:
                    # 同じパスの場合はリフレッシュ
                    self.show_status_message(f"📁 現在のフォルダ: {new_path}")
            elif not new_path:
                # 空パスの場合は全ドライブ表示状態
                self.show_status_message("💻 全ドライブ表示")
            else:
                QMessageBox.warning(self, "パスエラー", f"無効なパス: {new_path}")
                # アドレスバーを現在のパスに戻す
                if self.address_bar and self.current_folder:
                    self.address_bar.setText(self.current_folder)
        except Exception as e:
            QMessageBox.warning(self, "エラー", f"パス変更エラー: {e}")
            self.show_status_message(f"❌ パス変更エラー: {e}")
    
    def _go_to_parent_folder(self):
        """親フォルダへ移動"""
        try:
            if self.current_folder:
                parent_path = os.path.dirname(self.current_folder)
                if parent_path != self.current_folder:  # ルートディレクトリでない場合
                    self._load_folder(parent_path)
                else:
                    self.show_status_message("既にルートディレクトリです")
            else:
                self.show_status_message("フォルダが選択されていません")
        except Exception as e:
            QMessageBox.warning(self, "エラー", f"親フォルダ移動エラー: {e}")
            self.show_status_message(f"❌ 親フォルダ移動エラー: {e}")
    
    def _update_image_status(self, image_path):
        """画像の詳細情報を更新表示"""
        try:
            if not hasattr(self, 'status_info') or not self.status_info:
                return
            
            # 基本情報を取得
            filename = os.path.basename(image_path)
            file_size = os.path.getsize(image_path)
            file_size_mb = file_size / (1024 * 1024)
            
            # EXIF情報を取得
            from logic.image_utils import extract_image_info
            image_info = extract_image_info(image_path)
            
            # GPS情報を取得
            from logic.image_utils import extract_gps_coords
            gps_info = extract_gps_coords(image_path)
            
            # ステータス文字列を構築
            status_lines = []
            status_lines.append(f"📄 <b>{filename}</b>")
            
            # ファイルサイズ
            if file_size_mb >= 1:
                status_lines.append(f"📦 <b>サイズ:</b> {file_size_mb:.1f} MB")
            else:
                status_lines.append(f"📦 <b>サイズ:</b> {file_size // 1024} KB")
            
            # 解像度
            if image_info.get('width') and image_info.get('height'):
                width, height = image_info['width'], image_info['height']
                megapixels = (width * height) / 1000000
                status_lines.append(f"🖼️ <b>解像度:</b> {width} × {height} ({megapixels:.1f}MP)")
            
            # 撮影日時
            if image_info.get('datetime') and image_info['datetime'].strip():
                datetime_str = image_info['datetime'].strip()
                try:
                    # 日時フォーマットを整形
                    if ':' in datetime_str and ' ' in datetime_str:
                        date_part, time_part = datetime_str.split(' ', 1)
                        formatted_datetime = f"{date_part.replace(':', '/')} {time_part}"
                        status_lines.append(f"📅 <b>撮影日時:</b> {formatted_datetime}")
                    else:
                        status_lines.append(f"📅 <b>撮影日時:</b> {datetime_str}")
                except:
                    status_lines.append(f"📅 <b>撮影日時:</b> {datetime_str}")
            
            # カメラ情報
            if image_info.get('camera') and image_info['camera'].strip():
                status_lines.append(f"📷 <b>カメラ:</b> {image_info['camera'].strip()}")
            
            # 撮影設定
            shooting_settings = []
            
            # シャッタースピード
            if image_info.get('shutter') and image_info['shutter'].strip():
                shutter_str = image_info['shutter'].strip()
                shooting_settings.append(f"シャッター: {shutter_str}")
            
            # 絞り値
            if image_info.get('aperture') and image_info['aperture'].strip():
                shooting_settings.append(f"絞り: {image_info['aperture'].strip()}")
            elif image_info.get('絞り値') and image_info['絞り値'].strip():
                shooting_settings.append(f"絞り: {image_info['絞り値'].strip()}")
            
            # ISO感度
            if image_info.get('iso') and image_info['iso'].strip():
                shooting_settings.append(f"ISO: {image_info['iso'].strip()}")
            elif image_info.get('ISO感度') and image_info['ISO感度'].strip():
                shooting_settings.append(f"ISO: {image_info['ISO感度'].strip()}")
            
            # 焦点距離
            if image_info.get('focal_length') and image_info['focal_length'].strip():
                shooting_settings.append(f"焦点距離: {image_info['focal_length'].strip()}")
            elif image_info.get('焦点距離') and image_info['焦点距離'].strip():
                shooting_settings.append(f"焦点距離: {image_info['焦点距離'].strip()}")
            
            # 撮影設定を1行にまとめて表示
            if shooting_settings:
                status_lines.append(f"⚙️ <b>設定:</b> {' | '.join(shooting_settings)}")
            
            # GPS情報
            if gps_info and 'latitude' in gps_info and 'longitude' in gps_info:
                lat, lon = gps_info['latitude'], gps_info['longitude']
                status_lines.append(f"🌍 <b>GPS:</b> {lat:.6f}, {lon:.6f}")
            else:
                status_lines.append(f"🌍 <b>GPS:</b> 位置情報なし")
            
            # HTML形式で表示
            status_html = "<br>".join(status_lines)
            self.status_info.setText(status_html)
            
        except Exception as e:
            # エラー時は簡潔な情報のみ表示
            if hasattr(self, 'status_info') and self.status_info:
                filename = os.path.basename(image_path) if image_path else "不明"
                self.status_info.setText(f"📄 <b>{filename}</b><br>❌ 詳細情報の取得に失敗しました")
            
            # エラーログ記録
            import logging
            logging.error(f"画像ステータス更新エラー: {e}")

    def _clear_image_status(self):
        """画像詳細情報をクリア"""
        try:
            if hasattr(self, 'status_info') and self.status_info:
                self.status_info.setText("画像を選択すると詳細情報が表示されます")
        except Exception:
            pass
    
    def _toggle_theme(self):
        """テーマ切り替え"""
        try:
            self.theme_manager.toggle_theme()
            self._update_theme_button()
            
            # 手動テーマスタイル適用（サムネイル、アドレスバーなど）
            current_theme = self.theme_manager.get_current_theme()
            self._apply_manual_theme_styles(current_theme)
            
            # 現在のマップ表示を再描画（GPS情報なし画面を含む）
            self._refresh_map_display()
            
            # サムネイルエリアの強制更新
            if hasattr(self, 'thumbnail_list') and self.thumbnail_list:
                self.thumbnail_list.update()
                self.thumbnail_list.repaint()
            
            self.show_status_message(f"🎨 テーマ切り替え: {self.theme_manager.get_current_theme().value}モード")
        except Exception as e:
            self.show_status_message(f"❌ テーマ切り替えエラー: {e}")
    
    def _refresh_map_display(self):
        """マップ表示を再描画（テーマ切り替え時）"""
        try:
            if self.selected_image:
                # 選択中の画像がある場合は再表示
                self._update_map(self.selected_image)
                if self.maximized_state == 'map':
                    self._update_map_display(self.selected_image)
            else:
                # 選択中の画像がない場合は初期画面を表示
                self._show_initial_map_screen()
        except Exception as e:
            print(f"マップ表示再描画エラー: {e}")
    
    def _show_initial_map_screen(self):
        """起動時の初期マップ画面を表示"""
        try:
            if hasattr(self.map_panel, 'view'):
                initial_html = f"""
                <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; margin: 0; background-color: {self.get_theme_color('background')}; color: {self.get_theme_color('foreground')};">
                    <div style="background: {self.get_theme_color('group_bg')}; border: 2px solid {self.get_theme_color('info')}; border-radius: 10px; padding: 30px; max-width: 400px; margin: 0 auto;">
                        <h3 style="color: {self.get_theme_color('info')}; margin-top: 0;">🗺️ マップビュー</h3>
                        <p style="color: {self.get_theme_color('muted')}; margin: 15px 0;">GPS情報付きの画像を選択すると、ここに地図が表示されます。</p>
                        <div style="margin-top: 20px; padding: 10px; background: {self.get_theme_color('secondary')}; border-radius: 5px;">
                            <small style="color: {self.get_theme_color('muted')};">位置情報付きの画像を選択してください</small>
                        </div>
                    </div>
                </body>
                </html>
                """
                self.map_panel.view.setHtml(initial_html)
                # HTMLの強制更新
                self.map_panel.view.update()
                self.map_panel.view.repaint()
        except Exception as e:
            print(f"初期マップ画面表示エラー: {e}")
    
    def _update_theme_button(self):
        """テーマボタンの表示更新"""
        try:
            current_theme = self.theme_manager.get_current_theme()
            if current_theme == ThemeMode.DARK:
                self.theme_toggle_btn.setText("☀️ ライト")
                self.theme_toggle_btn.setToolTip("ライトモードに切り替え")
            else:
                self.theme_toggle_btn.setText("🌙 ダーク")
                self.theme_toggle_btn.setToolTip("ダークモードに切り替え")
        except Exception as e:
            print(f"テーマボタン更新エラー: {e}")
    
    def _apply_delayed_theme(self):
        """
        遅延テーマ適用
        
        UI構築完了後にアドレスバーなどの外部コンポーネントに
        テーマを適用するための遅延実行メソッド
        """
        try:
            current_theme = self.theme_manager.get_current_theme()
            self._apply_manual_theme_styles(current_theme)
        except Exception as e:
            print(f"遅延テーマ適用エラー: {e}")
    
    def _apply_custom_theme(self, theme: ThemeMode):
        """
        カスタムテーマ適用処理
        
        ThemeAwareMixinのオーバーライドメソッド
        """
        try:
            # メインウィンドウのスタイル適用
            main_style = self.get_theme_style("main_window")
            if main_style:
                self.setStyleSheet(main_style)
            
            # タイトルバー色の変更（Windows固有）
            self._apply_titlebar_theme(theme)
            
            # 個別のスタイル設定が必要な要素
            self._apply_manual_theme_styles(theme)
            
            # 全体的な強制更新（重要：最後に実行）
            self._force_global_theme_refresh()
            
        except Exception as e:
            print(f"カスタムテーマ適用エラー: {e}")
    
    def _apply_titlebar_theme(self, theme: ThemeMode):
        """
        タイトルバーテーマ適用（Windows専用）
        """
        try:
            import sys
            if sys.platform == "win32":
                # Windows APIを使用してタイトルバーをダークモードに変更
                try:
                    import ctypes
                    from ctypes import wintypes
                    
                    # ウィンドウハンドルを取得
                    hwnd = int(self.winId())
                    
                    if theme == ThemeMode.DARK:
                        # ダークモードのタイトルバー
                        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
                        value = ctypes.c_int(1)  # ダークモード有効
                        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
                                           ctypes.byref(value), ctypes.sizeof(value))
                    else:
                        # ライトモードのタイトルバー
                        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                        set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
                        value = ctypes.c_int(0)  # ダークモード無効
                        set_window_attribute(hwnd, DWMWA_USE_IMMERSIVE_DARK_MODE, 
                                           ctypes.byref(value), ctypes.sizeof(value))
                        
                except Exception as api_error:
                    print(f"Windows API タイトルバー変更エラー: {api_error}")
                    
            # フォールバック: パレット変更
            from PyQt5.QtGui import QPalette, QColor
            
            # ダークモードの場合
            if theme == ThemeMode.DARK:
                # ウィンドウの背景色を暗くして、タイトルバーも影響を受けやすくする
                palette = self.palette()
                bg_color = self.get_theme_color("background")
                fg_color = self.get_theme_color("foreground")
                
                # パレットの色を変更
                palette.setColor(QPalette.Window, QColor(bg_color))
                palette.setColor(QPalette.WindowText, QColor(fg_color))
                palette.setColor(QPalette.Base, QColor(bg_color))
                palette.setColor(QPalette.Text, QColor(fg_color))
                
                self.setPalette(palette)
                
                # メインウィンドウのスタイルシート
                self.setStyleSheet(f"""
                    QMainWindow {{
                        background-color: {bg_color};
                        color: {fg_color};
                        border: 1px solid #404040;
                    }}
                    QMenuBar {{
                        background-color: {bg_color};
                        color: {fg_color};
                        border: none;
                    }}
                """)
            else:
                # ライトモードではデフォルトパレットを復元
                self.setPalette(self.style().standardPalette())
                self.setStyleSheet("")  # スタイルシートをクリア
                
        except Exception as e:
            print(f"タイトルバーテーマ適用エラー: {e}")
    
    def _apply_manual_theme_styles(self, theme: ThemeMode):
        """
        手動でスタイルを適用する必要がある要素の処理
        """
        try:
            bg_color = self.get_theme_color("background")
            fg_color = self.get_theme_color("foreground")
            border_color = self.get_theme_color("border")
            button_bg = self.get_theme_color("button_bg")
            
            # 0. メインウィンドウ全体とステータスバーのテーマ適用
            try:
                # メインウィンドウ自体のスタイル設定
                main_window_style = f"""
                    QMainWindow {{
                        background-color: {bg_color};
                        color: {fg_color};
                    }}
                """
                self.setStyleSheet(main_window_style)
                
                # ステータスバーのテーマ適用
                if hasattr(self, 'statusBar') and self.statusBar():
                    status_bar = self.statusBar()
                    status_bar.setStyleSheet(f"""
                        QStatusBar {{
                            background-color: {bg_color};
                            color: {fg_color};
                            border: none;
                            border-top: 1px solid {border_color};
                        }}
                        QStatusBar::item {{
                            border: none;
                        }}
                    """)
                    # ステータスバー内のラベルも更新
                    for label in status_bar.findChildren(QLabel):
                        label.setStyleSheet(f"color: {fg_color}; background-color: {bg_color};")
                        
            except Exception as e:
                print(f"メインウィンドウ・ステータスバーテーマ適用エラー: {e}")

            # 1. ボタン類の一括スタイル適用
            buttons = self.findChildren(QPushButton)
            for btn in buttons:
                if btn != self.theme_toggle_btn:  # テーマ切り替えボタン以外
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {button_bg};
                            color: {fg_color};
                            border: 1px solid {border_color};
                            border-radius: 4px;
                            padding: 4px 8px;
                            font-size: 11px;
                        }}
                        QPushButton:hover {{
                            background-color: {self.get_theme_color("button_hover")};
                            border-color: {self.get_theme_color("accent")};
                        }}
                    """)
                    # 強制スタイル更新
                    btn.style().unpolish(btn)
                    btn.style().polish(btn)
            
            # 1-2. すべてのQGroupBoxを更新
            group_boxes = self.findChildren(QGroupBox)
            for group_box in group_boxes:
                group_box.setStyleSheet(f"""
                    QGroupBox {{
                        background-color: {bg_color};
                        color: {fg_color};
                        border: 2px solid {border_color};
                        border-radius: 5px;
                        margin-top: 10px;
                        padding-top: 10px;
                    }}
                    QGroupBox::title {{
                        subcontrol-origin: margin;
                        left: 10px;
                        padding: 0 5px 0 5px;
                        color: {fg_color};
                    }}
                """)
            
            # 2. サムネイルエリアの手動適用
            if hasattr(self, 'thumbnail_list') and self.thumbnail_list:
                # サムネイルリスト自体
                thumbnail_style = f"""
                    QWidget {{
                        background-color: {bg_color};
                        color: {fg_color};
                        border: 1px solid {border_color};
                    }}
                    QScrollArea {{
                        background-color: {bg_color};
                        border: none;
                    }}
                    QScrollArea > QWidget > QWidget {{
                        background-color: {bg_color};
                    }}
                """
                self.thumbnail_list.setStyleSheet(thumbnail_style)
                
                # サムネイルリスト内の子ウィジェットを再帰的に適用
                self._apply_recursive_theme(self.thumbnail_list, bg_color, fg_color)
            
            # 3. プレビューエリアとマップエリアの余白
            # プレビューパネルとその親を含む全体
            if hasattr(self, 'preview_panel') and self.preview_panel:
                self._apply_panel_theme_recursive(self.preview_panel, bg_color)
            
            # マップパネルとその親を含む全体
            if hasattr(self, 'map_panel') and self.map_panel:
                self._apply_panel_theme_recursive(self.map_panel, bg_color)
                
            # 4. 右スプリッター全体の背景
            if hasattr(self, 'right_splitter'):
                self.right_splitter.setStyleSheet(f"QSplitter {{ background-color: {bg_color}; }}")
                
            # 5. メインスプリッター全体の背景
            if hasattr(self, 'main_splitter'):
                self.main_splitter.setStyleSheet(f"QSplitter {{ background-color: {bg_color}; }}")
                
            # 6. 左パネル全体の背景
            if hasattr(self, 'left_panel') and self.left_panel:
                self.left_panel.setStyleSheet(f"""
                    QWidget {{
                        background-color: {bg_color};
                        color: {fg_color};
                    }}
                """)
                # 左パネルの強制更新
                self.left_panel.update()
                self.left_panel.repaint()
                
            # 7. 最大化コンテナの背景（画像ビュー全画面表示）
            if hasattr(self, 'maximize_container') and self.maximize_container:
                self.maximize_container.setStyleSheet(f"""
                    QWidget {{
                        background-color: {bg_color};
                        color: {fg_color};
                    }}
                """)
                # 最大化コンテナの子要素も更新
                if hasattr(self, 'maximized_content_area') and self.maximized_content_area:
                    self.maximized_content_area.setStyleSheet(f"""
                        QWidget {{
                            background-color: {bg_color};
                            color: {fg_color};
                        }}
                    """)
                # 強制更新
                self.maximize_container.update()
                self.maximize_container.repaint()
                
            # 8. 中央コンテンツエリア全体（スプリッター等）の背景
            try:
                # メインスプリッターの背景
                if hasattr(self, 'main_splitter') and self.main_splitter:
                    self.main_splitter.setStyleSheet(f"""
                        QSplitter {{
                            background-color: {bg_color};
                            border: none;
                        }}
                        QSplitter::handle {{
                            background-color: {border_color};
                        }}
                        QSplitter::handle:horizontal {{
                            width: 3px;
                        }}
                        QSplitter::handle:vertical {{
                            height: 3px;
                        }}
                    """)
                
                # 右パネルスプリッター
                if hasattr(self, 'right_splitter') and self.right_splitter:
                    self.right_splitter.setStyleSheet(f"""
                        QSplitter {{
                            background-color: {bg_color};
                            border: none;
                        }}
                        QSplitter::handle {{
                            background-color: {border_color};
                        }}
                        QSplitter::handle:vertical {{
                            height: 3px;
                        }}
                    """)
                
                # 中央ウィジェット全体
                central_widget = self.centralWidget()
                if central_widget:
                    central_widget.setStyleSheet(f"""
                        QWidget {{
                            background-color: {bg_color};
                            color: {fg_color};
                        }}
                    """)
                    
            except Exception as e:
                print(f"中央エリアテーマ適用エラー: {e}")
            
            # 追加のテーマスタイル適用
            self._apply_additional_theme_styles()
            
        except Exception as e:
            print(f"手動テーマスタイル適用エラー: {e}")
    
    def _apply_recursive_theme(self, widget, bg_color, fg_color):
        """ウィジェットとその子要素に再帰的にテーマ適用"""
        try:
            # 現在のウィジェットに適用
            current_style = widget.styleSheet()
            if not current_style or "background-color" not in current_style:
                widget.setStyleSheet(f"background-color: {bg_color}; color: {fg_color};")
            
            # 子要素に再帰適用
            for child in widget.findChildren(QWidget):
                if not child.styleSheet() or "background-color" not in child.styleSheet():
                    child.setStyleSheet(f"background-color: {bg_color}; color: {fg_color};")
        except Exception as e:
            print(f"再帰テーマ適用エラー: {e}")
    
    def _apply_panel_theme_recursive(self, panel, bg_color):
        """パネルとその親階層に再帰的に背景色適用"""
        try:
            # パネル自体
            if panel:
                current = panel
                # 3階層上まで遡って背景色を適用
                for _ in range(3):
                    if current:
                        parent = current.parent()
                        if parent and hasattr(parent, 'setStyleSheet'):
                            parent.setStyleSheet(f"background-color: {bg_color};")
                            current = parent
                        else:
                            break
        except Exception as e:
            print(f"パネルテーマ適用エラー: {e}")
    
    def _apply_additional_theme_styles(self):
        """追加のテーマスタイル適用"""
        try:
            # 4. プレビューとマップのタイトルラベル
            title_color = self.get_theme_color("muted")
            title_style = f"font-weight: normal; color: {title_color}; font-size: 11px;"
            
            # プレビュータイトル
            preview_titles = self.findChildren(QLabel)
            for label in preview_titles:
                if label.text() in ["画像プレビュー", "撮影場所マップ"]:
                    label.setStyleSheet(title_style)
            
            # 5. QGroupBoxのタイトル色を適用
            fg_color = self.get_theme_color("foreground")
            bg_color = self.get_theme_color("background")
            border_color = self.get_theme_color("border")
            
            group_boxes = self.findChildren(QGroupBox)
            for group_box in group_boxes:
                if group_box.title() in ["🖼️ プレビュー", "🗺️ マップ"]:
                    group_box.setStyleSheet(f"""
                        QGroupBox {{ 
                            font-size: 12px; 
                            font-weight: bold; 
                            color: {fg_color};
                            background-color: {bg_color};
                            border: 2px solid {border_color};
                            border-radius: 5px;
                            margin-top: 1ex;
                        }}
                        QGroupBox::title {{
                            subcontrol-origin: margin;
                            left: 10px;
                            padding: 0 5px 0 5px;
                            color: {fg_color};
                            background-color: {bg_color};
                        }}
                    """)
            
            # 6. エラーラベルのカラー統一
            error_color = self.get_theme_color("error")
            error_labels = self.findChildren(QLabel)
            for label in error_labels:
                if "エラー" in label.text() or "error" in label.text().lower():
                    current_style = label.styleSheet()
                    if "color:" in current_style:
                        # 既存のcolorを新しい色に置換
                        import re
                        new_style = re.sub(r'color:\s*[^;]+;', f'color: {error_color};', current_style)
                        label.setStyleSheet(new_style)
                    else:
                        # colorが設定されていない場合は追加
                        label.setStyleSheet(f"{current_style} color: {error_color};")
                        
        except Exception as e:
            print(f"追加テーマスタイル適用エラー: {e}")
    
    def _force_global_theme_refresh(self):
        """全体的なテーマ強制更新"""
        try:
            # メインウィンドウ全体の強制更新
            self.update()
            self.repaint()
            
            # ステータスバーの強制更新（特別処理）
            if hasattr(self, 'statusBar') and self.statusBar():
                status_bar = self.statusBar()
                status_bar.update()
                status_bar.repaint()
                # ステータスバー内の全ラベルを強制更新
                for label in status_bar.findChildren(QLabel):
                    label.update()
                    label.repaint()
            
            # 中央ウィジェットの強制更新
            central_widget = self.centralWidget()
            if central_widget:
                central_widget.update()
                central_widget.repaint()
                # 中央ウィジェットの子要素も強制更新
                for child in central_widget.findChildren(QWidget):
                    child.update()
            
            # 主要スプリッターの強制更新
            if hasattr(self, 'main_splitter') and self.main_splitter:
                self.main_splitter.update()
                self.main_splitter.repaint()
                
            if hasattr(self, 'right_splitter') and self.right_splitter:
                self.right_splitter.update()
                self.right_splitter.repaint()
                
            # すべての子ウィジェットの強制スタイル更新
            all_widgets = self.findChildren(QWidget)
            for widget in all_widgets:
                try:
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                    widget.update()
                    widget.repaint()
                except:
                    pass  # エラーは無視
                    
            # 最終的な全体更新
            QApplication.instance().processEvents()
            self.update()
            self.repaint()
                    
        except Exception as e:
            print(f"全体テーマ強制更新エラー: {e}")
