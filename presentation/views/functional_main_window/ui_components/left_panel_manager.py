"""
Left Panel Manager

フォルダ内容表示、サムネイル表示、詳細情報表示を管理
"""

import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QListWidget, QLabel, QListWidgetItem
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
        try:
            from utils.debug_logger import debug, info, error
            info("左パネル作成開始")
            
            self.panel = QWidget()
            layout = QVBoxLayout(self.panel)
            
            # フォルダ内容パネル
            info("フォルダ内容パネル作成中...")
            self._create_folder_panel(layout)
            
            # サムネイルパネル
            info("サムネイルパネル作成中...")
            self._create_thumbnail_panel(layout)
            
            # ステータスパネル
            info("ステータスパネル作成中...")
            self._create_status_panel(layout)
            
            # テーマコンポーネント登録
            info("テーマコンポーネント登録中...")
            self._register_theme_components()
            
            info("左パネル作成完了")
            return self.panel
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"左パネル作成エラー: {e}")
            import traceback
            traceback.print_exc()
            return QWidget()  # 空のウィジェットを返す
    
    def _create_folder_panel(self, layout):
        """フォルダ内容パネルを作成"""
        self.folder_group = QGroupBox("📁 フォルダ内容")
        folder_layout = QVBoxLayout(self.folder_group)
        
        # フォルダ内容リスト
        self.folder_content_list = QListWidget()
        self.folder_content_list.setMinimumHeight(150)
        
        # イベントハンドラの接続（ダミーイベント）
        def folder_item_clicked(item):
            from utils.debug_logger import info
            if item:
                item_path = item.data(Qt.ItemDataRole.UserRole)
                item_type = item.data(Qt.ItemDataRole.UserRole + 1)
                info(f"フォルダアイテムクリック: {item.text()}, パス: {item_path}, タイプ: {item_type}")
                
                # フォルダの場合は中身を表示
                if item_type == "folder":
                    self.update_folder_content(item_path)
                    # サムネイル更新
                    image_files = self._get_image_files_from_folder(item_path)
                    self.update_thumbnails(image_files)
                # 画像の場合はEXIF情報を表示
                elif item_type == "image":
                    self._show_image_info(item_path)
        
        def folder_item_double_clicked(item):
            from utils.debug_logger import info
            if item:
                item_path = item.data(Qt.ItemDataRole.UserRole)
                item_type = item.data(Qt.ItemDataRole.UserRole + 1)
                info(f"フォルダアイテムダブルクリック: {item.text()}")
        
        self.folder_content_list.itemClicked.connect(folder_item_clicked)
        self.folder_content_list.itemDoubleClicked.connect(folder_item_double_clicked)
        
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
            # サムネイルリストを作成（コールバックは後で set_event_handlers で設定）
            self.thumbnail_list = create_thumbnail_list()  # コールバック引数を削除
            self.thumbnail_layout.addWidget(self.thumbnail_list)
            from utils.debug_logger import info
            info("サムネイルリスト作成成功")
        except Exception as e:
            from utils.debug_logger import error
            error(f"サムネイル作成エラー: {e}")
            error_label = QLabel(f"サムネイルエラー: {e}")
            error_label.setStyleSheet("color: red;")
            self.thumbnail_layout.addWidget(error_label)
            self.thumbnail_list = None
        
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
        if self.folder_content_list is not None:
            self.folder_content_list.itemClicked.connect(folder_item_clicked)
            self.folder_content_list.itemDoubleClicked.connect(folder_item_double_clicked)
        
        from utils.debug_logger import info, error
        info(f"🔍 サムネイルリスト状態チェック: self.thumbnail_list={self.thumbnail_list}")
        info(f"🔍 サムネイルリスト型: {type(self.thumbnail_list)}")
        info(f"🔍 サムネイルリストNone確認: {self.thumbnail_list is None}")
        
        if self.thumbnail_list is not None:
            # 既存の接続をすべて切断（より確実に）
            try:
                # 全ての接続を確実に切断
                self.thumbnail_list.itemClicked.disconnect()
                from utils.debug_logger import info
                info("🔍 既存のサムネイル接続を切断しました")
            except TypeError:
                # 接続がない場合はTypeErrorが発生
                from utils.debug_logger import info
                info("🔍 サムネイル接続がありませんでした（正常）")
            except Exception as e:
                from utils.debug_logger import warning
                warning(f"🔍 接続切断エラー: {e}")
            
            # サムネイルクリック時の処理
            def thumbnail_item_clicked(item):
                from utils.debug_logger import debug, info
                info(f"🔍 thumbnail_item_clicked開始: {item}")
                if item:
                    image_path = item.data(Qt.ItemDataRole.UserRole)
                    info(f"🔍 取得したimage_path: {image_path}")
                    if image_path:
                        debug(f"サムネイルクリック: {image_path}")
                        info(f"🔍 image_selected呼び出し開始: {image_selected}")
                        image_selected(image_path)
                        info(f"🔍 image_selected呼び出し完了")
                    else:
                        debug("サムネイルアイテムからパスを取得できませんでした")
                else:
                    info("🔍 thumbnail_item_clicked: itemがNone")
            
            # 新しい接続を設定
            self.thumbnail_list.itemClicked.connect(thumbnail_item_clicked)
            from utils.debug_logger import info
            info("🔍 新しいサムネイルイベントハンドラーを設定しました")
        else:
            from utils.debug_logger import error
            error("🚨 サムネイルリストがNullまたは無効です - イベントハンドラーを設定できません")
    
    def _show_image_in_preview(self, image_path):
        """画像をプレビューパネルに表示"""
        try:
            from utils.debug_logger import debug, info, error
            debug(f"プレビュー表示要求: {image_path}")
            
            if not image_path or not os.path.exists(image_path):
                error(f"無効な画像パス: {image_path}")
                return
                
            # メインウィンドウのプレビューパネルを使用
            if hasattr(self.main_window, 'preview_panel') and self.main_window.preview_panel:
                if hasattr(self.main_window.preview_panel, 'display_image'):
                    self.main_window.preview_panel.display_image(image_path)
                    info(f"プレビュー表示完了: {os.path.basename(image_path)}")
                else:
                    error("プレビューパネルにdisplay_imageメソッドがありません")
            else:
                error("プレビューパネルが見つかりません")
                
        except Exception as e:
            from utils.debug_logger import error
            error(f"画像プレビュー表示エラー: {e}")
    
    def update_folder_content(self, folder_path):
        """フォルダ内容を更新"""
        try:
            from utils.debug_logger import info, error
            if self.folder_content_list is None:
                error("フォルダ内容リストが初期化されていません")
                return
                
            info(f"フォルダ内容を更新中: {folder_path}")
            self.folder_content_list.clear()
            
            if not folder_path or not os.path.exists(folder_path):
                error(f"無効なフォルダパス: {folder_path}")
                return
            
            try:
                # フォルダ内のファイル・フォルダを取得
                items = []
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        items.append(("📁 " + item, item_path, "folder"))
                    elif os.path.isfile(item_path) and item.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')):
                        items.append(("🖼️ " + item, item_path, "image"))
                
                # フォルダを先頭、ファイルを後に並べてソート
                items.sort(key=lambda x: (x[2] != "folder", x[0].lower()))
                
                # リストに追加
                for display_name, full_path, item_type in items:
                    item = QListWidgetItem(display_name)
                    item.setData(Qt.ItemDataRole.UserRole, full_path)  # フルパスを保存
                    item.setData(Qt.ItemDataRole.UserRole + 1, item_type)  # タイプを保存
                    self.folder_content_list.addItem(item)
                
                info(f"フォルダ内容更新完了: {len(items)}件")
                
            except PermissionError:
                error(f"フォルダアクセス権限なし: {folder_path}")
            except Exception as e:
                error(f"フォルダ読み込みエラー: {e}")
                
        except Exception as e:
            from utils.debug_logger import error
            error(f"フォルダ内容更新エラー: {e}")
    
    def update_thumbnails(self, image_files):
        """サムネイルを更新"""
        try:
            from utils.debug_logger import info, error
            if self.thumbnail_list is None:
                error("サムネイルリストが初期化されていません")
                return
                
            info(f"サムネイル更新中: {len(image_files)}件")
            self.thumbnail_list.clear()
            
            if not image_files:
                info("画像ファイルがありません")
                return
            
            try:
                from ui.thumbnail_list import add_thumbnail
                for image_path in image_files:
                    if os.path.exists(image_path):
                        add_thumbnail(self.thumbnail_list, image_path)
                
                info(f"サムネイル更新完了: {self.thumbnail_list.count()}件")
                
            except Exception as e:
                error(f"サムネイル追加エラー: {e}")
                
        except Exception as e:
            from utils.debug_logger import error
            error(f"サムネイル更新エラー: {e}")
    
    def update_status_info(self, message):
        """ステータス情報を更新"""
        if self.status_info is not None:
            self.status_info.setText(message)
    
    def clear_status_info(self):
        """ステータス情報をクリア"""
        if self.status_info is not None:
            self.status_info.setText("画像を選択すると詳細情報が表示されます")
    
    def _get_image_files_from_folder(self, folder_path):
        """フォルダから画像ファイルのリストを取得"""
        try:
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
            image_files = []
            
            if os.path.exists(folder_path) and os.path.isdir(folder_path):
                for item in os.listdir(folder_path):
                    item_path = os.path.join(folder_path, item)
                    if os.path.isfile(item_path):
                        _, ext = os.path.splitext(item.lower())
                        if ext in image_extensions:
                            image_files.append(item_path)
            
            return sorted(image_files)
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"画像ファイル取得エラー: {e}")
            return []
    
    def _show_image_info(self, image_path):
        """画像のEXIF情報を表示（exifreadライブラリ使用）"""
        try:
            from utils.debug_logger import info, error
            import os
            from datetime import datetime
            
            # 基本ファイル情報
            file_size = os.path.getsize(image_path)
            file_size_mb = file_size / (1024 * 1024)
            file_modified = datetime.fromtimestamp(os.path.getmtime(image_path))
            
            info_text = f"📁 ファイル: {os.path.basename(image_path)}\n"
            info_text += f"📏 サイズ: {file_size_mb:.2f} MB\n"
            info_text += f"📅 更新日: {file_modified.strftime('%Y-%m-%d %H:%M:%S')}\n"
            
            # logic/image_utils.pyを使用してEXIF情報取得
            try:
                # 画像サイズ取得（PyQt5で取得）
                from PyQt5.QtGui import QPixmap
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    info_text += f"🖼️ サイズ: {pixmap.width()} x {pixmap.height()} px\n"
                
                # EXIF情報取得
                try:
                    import exifread
                    with open(image_path, 'rb') as f:
                        tags = exifread.process_file(f)
                        
                    if tags:
                        info_text += "\n📸 EXIF情報:\n"
                        
                        # 重要なEXIF情報を抽出
                        important_tags = {
                            'EXIF DateTime': '撮影日時',
                            'EXIF DateTimeOriginal': '撮影日時（元）', 
                            'Image Make': 'カメラメーカー',
                            'Image Model': 'カメラモデル',
                            'EXIF Software': 'ソフトウェア',
                            'EXIF FocalLength': '焦点距離',
                            'EXIF ISOSpeedRatings': 'ISO感度'
                        }
                        
                        for tag_key, display_name in important_tags.items():
                            if tag_key in tags:
                                value = str(tags[tag_key])
                                info_text += f"  {display_name}: {value}\n"
                        
                        # GPS情報チェック
                        gps_tags = [tag for tag in tags.keys() if 'GPS' in str(tag)]
                        if gps_tags:
                            info_text += "  🗺️ GPS情報: あり\n"
                        else:
                            info_text += "  🗺️ GPS情報: なし\n"
                    else:
                        info_text += "\n📸 EXIF情報: なし\n"
                        
                except ImportError:
                    info_text += "\n📸 EXIF読み込み: exifreadライブラリが必要です\n"
                except Exception as exif_error:
                    info_text += f"\n📸 EXIF読み込みエラー: {exif_error}\n"
                    
            except Exception as img_error:
                info_text += f"\n�️ 画像読み込みエラー: {img_error}\n"
            
            # ステータス情報に表示
            self.update_status_info(info_text)
            
        except Exception as e:
            from utils.debug_logger import error
            error(f"画像情報表示エラー: {e}")
            self.update_status_info(f"❌ 画像情報取得エラー: {e}")
