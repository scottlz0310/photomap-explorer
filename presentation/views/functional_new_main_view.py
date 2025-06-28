"""
修正版新UIメインビュー

実際の機能を持つ新UIメインウィンドウ
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QSplitter, QWidget, 
                            QStatusBar, QHBoxLayout, QPushButton, QLabel,
                            QGroupBox, QFileDialog, QMessageBox, QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon


class FunctionalNewMainWindow(QMainWindow):
    """
    機能的な新UIメインウィンドウ
    
    実際にフォルダ選択、画像表示、マップ表示が動作します。
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - 新UI (Clean Architecture)")
        self.setGeometry(100, 100, 1400, 900)
        
        # 現在の状態
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        
        # コンポーネント参照
        self.thumbnail_list = None
        self.preview_panel = None
        self.map_panel = None
        self.folder_panel = None
        
        # アイコン設定
        self._setup_icon()
        
        # UI構築
        self._setup_ui()
        
        # 初期フォルダ設定
        self._load_initial_folder()
        
        # ステータス表示
        self.show_status_message("新UI (Clean Architecture) で起動しました")
    
    def show_status_message(self, message, timeout=0):
        """ステータスバーにメッセージを表示"""
        try:
            if hasattr(self, 'statusBar') and self.statusBar():
                self.statusBar().showMessage(message, timeout)
                print(f"Status: {message}")  # デバッグ用
            else:
                print(f"Status (fallback): {message}")
        except Exception as e:
            print(f"ステータス表示エラー: {e}, メッセージ: {message}")
    
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
        
        # ツールバー（高さを最小に調整）
        toolbar_layout = QHBoxLayout()
        toolbar_layout.setContentsMargins(5, 2, 5, 2)  # マージンを最小に
        
        # フォルダ選択ボタン（高さを制限）
        folder_btn = QPushButton("📁 フォルダ選択")
        folder_btn.setMaximumHeight(30)  # 高さを制限
        folder_btn.clicked.connect(self._select_folder)
        toolbar_layout.addWidget(folder_btn)
        
        # 現在のフォルダ表示（高さを制限）
        self.folder_label = QLabel("フォルダが選択されていません")
        self.folder_label.setStyleSheet("color: #666; margin: 2px; font-size: 11px;")
        self.folder_label.setMaximumHeight(30)  # 高さを制限
        toolbar_layout.addWidget(self.folder_label)
        
        toolbar_layout.addStretch()
        
        # ツールバーウィジェットを作成して高さを制限
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar_layout)
        toolbar_widget.setMaximumHeight(35)  # ツールバー全体の高さを制限
        layout.addWidget(toolbar_widget)
        
        # メインスプリッター
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # 左パネル：フォルダとサムネイル
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右パネル：プレビューとマップ
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # ステータスバー
        self.statusBar().showMessage("準備完了")
        
        # スプリッターサイズ調整
        main_splitter.setSizes([600, 800])
    
    def _create_left_panel(self):
        """左パネル作成"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # フォルダパネル（現在のフォルダ内容表示）
        folder_group = QGroupBox("📁 フォルダ内容")
        folder_group.setStyleSheet("QGroupBox { font-size: 12px; font-weight: bold; }")
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
        thumbnail_group.setStyleSheet("QGroupBox { font-size: 12px; font-weight: bold; }")
        thumbnail_layout = QVBoxLayout(thumbnail_group)
        
        try:
            from ui.thumbnail_list import create_thumbnail_list
            self.thumbnail_list = create_thumbnail_list(self._on_image_selected)
            thumbnail_layout.addWidget(self.thumbnail_list)
        except Exception as e:
            error_label = QLabel(f"サムネイルエラー: {e}")
            error_label.setStyleSheet("color: red;")
            thumbnail_layout.addWidget(error_label)
        
        layout.addWidget(thumbnail_group)
        
        return panel
    
    def _create_right_panel(self):
        """右パネル作成"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 上下スプリッター
        splitter = QSplitter(Qt.Vertical)
        layout.addWidget(splitter)
        
        # プレビューパネル
        preview_group = QGroupBox("🖼️ プレビュー")
        preview_group.setStyleSheet("QGroupBox { font-size: 12px; font-weight: bold; }")
        preview_layout = QVBoxLayout(preview_group)
        
        try:
            from ui.image_preview import create_image_preview
            self.preview_panel = create_image_preview()
            preview_layout.addWidget(self.preview_panel)
        except Exception as e:
            error_label = QLabel(f"プレビューエラー: {e}")
            error_label.setStyleSheet("color: red;")
            preview_layout.addWidget(error_label)
        
        splitter.addWidget(preview_group)
        
        # マップパネル
        map_group = QGroupBox("🗺️ マップ")
        map_group.setStyleSheet("QGroupBox { font-size: 12px; font-weight: bold; }")
        map_layout = QVBoxLayout(map_group)
        
        try:
            from ui.map_panel import create_map_panel
            self.map_panel = create_map_panel()
            map_layout.addWidget(self.map_panel)
        except Exception as e:
            error_label = QLabel(f"マップエラー: {e}")
            error_label.setStyleSheet("color: red;")
            map_layout.addWidget(error_label)
        
        splitter.addWidget(map_group)
        
        # スプリッターサイズ調整
        splitter.setSizes([400, 400])
        
        return panel
    
    def _select_folder(self):
        """フォルダ選択ダイアログ"""
        folder = QFileDialog.getExistingDirectory(
            self, 
            "画像フォルダを選択", 
            os.path.expanduser("~")
        )
        
        if folder:
            self._load_folder(folder)
    
    def _load_initial_folder(self):
        """初期フォルダ読み込み"""
        # デスクトップまたはピクチャフォルダから開始
        initial_paths = [
            os.path.join(os.path.expanduser("~"), "Pictures"),
            os.path.join(os.path.expanduser("~"), "Desktop"),
            os.path.expanduser("~")
        ]
        
        for path in initial_paths:
            if os.path.exists(path):
                self._load_folder(path)
                break
    
    def _load_folder(self, folder_path):
        """フォルダ読み込み"""
        try:
            self.current_folder = folder_path
            self.folder_label.setText(f"📁 {folder_path}")
            
            # 画像ファイル検索
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
                        print(f"サムネイル追加エラー({image_path}): {e}")
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
                        folder_content_list = list_widgets[0]  # 最初のQListWidgetを使用
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
            print(f"フォルダ内容表示詳細エラー: {e}")
    
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
            print(f"画像選択詳細エラー: {e}")
            import traceback
            traceback.print_exc()
    
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
            
            # GPS情報取得してマップ表示
            self._update_map(image_path)
            
        except Exception as e:
            self.show_status_message(f"❌ 画像表示エラー: {e}")
            print(f"画像表示詳細エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_map(self, image_path):
        """マップ更新"""
        try:
            if not self.map_panel:
                return
                
            # GPS情報抽出
            try:
                from logic.image_utils import extract_gps_coords
                gps_info = extract_gps_coords(image_path)
                
                if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                    lat, lon = gps_info["latitude"], gps_info["longitude"]
                    
                    # マップパネルのupdate_locationメソッドを使用
                    if hasattr(self.map_panel, 'update_location'):
                        success = self.map_panel.update_location(lat, lon)
                        if success:
                            self.show_status_message(f"📍 GPS座標: {lat:.6f}, {lon:.6f}")
                        else:
                            self.show_status_message("📍 マップ表示に失敗しました")
                    else:
                        self.show_status_message("📍 マップ機能が利用できません")
                else:
                    # GPS情報がない場合はデフォルトメッセージを表示
                    self.map_panel.view.setHtml("""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                        <h3>📍 GPS情報がありません</h3>
                        <p>この画像にはGPS座標が含まれていません。</p>
                    </body>
                    </html>
                    """)
                    self.show_status_message("📍 GPS情報が見つかりません")
                    
            except ImportError:
                self.show_status_message("📍 GPS機能が利用できません")
                
        except Exception as e:
            # エラーログを静かに記録し、ユーザーには簡潔なメッセージを表示
            self.show_status_message("❌ マップ更新に失敗しました")
    
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
            print(f"ダブルクリック詳細エラー: {e}")
