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
        import logging
        logger = logging.getLogger(__name__)
        
        self.folder_group = QGroupBox("📁 フォルダ内容")
        folder_layout = QVBoxLayout(self.folder_group)
        
        # フォルダ内容リスト
        self.folder_content_list = QListWidget()
        self.folder_content_list.setMinimumHeight(120)  # SVGレイアウトに合わせて調整
        self.folder_content_list.setMaximumHeight(180)  # 最大高さを設定
        
        logger.debug(f"フォルダ内容リスト作成: {self.folder_content_list}")
        
        # イベントハンドラの接続（後で設定）
        # self.folder_content_list.itemClicked.connect(...)
        # self.folder_content_list.itemDoubleClicked.connect(...)
        
        folder_layout.addWidget(self.folder_content_list)
        layout.addWidget(self.folder_group)
        
        # メインウィンドウに参照を設定
        self.main_window.folder_content_list = self.folder_content_list
        logger.debug(f"メインウィンドウに参照設定: {self.main_window.folder_content_list}")
    
    def _create_thumbnail_panel(self, layout):
        """サムネイルパネルを作成"""
        self.thumbnail_group = QGroupBox("🖼️ サムネイル")
        self.thumbnail_layout = QVBoxLayout(self.thumbnail_group)
        
        try:
            from ui.thumbnail_list import create_thumbnail_list
            self.thumbnail_list = create_thumbnail_list(None)  # コールバックは後で設定
            self.thumbnail_list.setMinimumHeight(200)  # SVGレイアウトに合わせて調整
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
        self.status_info.setMinimumHeight(100)  # SVGレイアウトに合わせて調整
        self.status_info.setMaximumHeight(150)  # 最大高さを調整
        
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
        import logging
        import os
        from pathlib import Path
        from PyQt5.QtWidgets import QListWidgetItem
        from PyQt5.QtCore import Qt
        
        logger = logging.getLogger(__name__)
        
        try:
            # デバッグ情報を追加
            logger.debug(f"update_folder_content 呼び出し: folder_path={folder_path}")
            logger.debug(f"self.folder_content_list = {self.folder_content_list}")
            logger.debug(f"self.folder_content_list type: {type(self.folder_content_list)}")
            
            if self.folder_content_list is None:
                logger.warning("フォルダ内容リストが見つかりません")
                
                # メインウィンドウから参照を取得する試行
                if hasattr(self.main_window, 'folder_content_list'):
                    self.folder_content_list = self.main_window.folder_content_list
                    logger.info(f"メインウィンドウから参照を復旧: {self.folder_content_list}")
                else:
                    logger.error("メインウィンドウにもfolder_content_listが見つかりません")
                    return
            
            self.folder_content_list.clear()
            
            if not folder_path or not os.path.exists(folder_path):
                logger.warning(f"無効なフォルダパス: {folder_path}")
                return
            
            folder = Path(folder_path)
            
            # 親フォルダへのリンク（ルートでない場合）
            if folder.parent != folder:
                parent_item = QListWidgetItem("📁 .. (親フォルダ)")
                parent_item.setData(Qt.ItemDataRole.UserRole, str(folder.parent))  # type: ignore
                parent_item.setToolTip(str(folder.parent))
                self.folder_content_list.addItem(parent_item)
            
            # フォルダとファイルを取得
            items = []
            
            try:
                for item_path in folder.iterdir():
                    if item_path.is_dir():
                        # フォルダ
                        folder_item = QListWidgetItem(f"📁 {item_path.name}")
                        folder_item.setData(Qt.ItemDataRole.UserRole, str(item_path))  # type: ignore
                        folder_item.setToolTip(str(item_path))
                        items.append((folder_item, 0))  # フォルダは先頭
                    elif item_path.is_file():
                        # ファイル（画像ファイルを優先表示）
                        file_ext = item_path.suffix.lower()
                        if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                            file_item = QListWidgetItem(f"🖼️ {item_path.name}")
                            file_item.setData(Qt.ItemDataRole.UserRole, str(item_path))  # type: ignore
                            file_item.setToolTip(str(item_path))
                            items.append((file_item, 1))  # 画像ファイルは2番目
                        else:
                            file_item = QListWidgetItem(f"📄 {item_path.name}")
                            file_item.setData(Qt.ItemDataRole.UserRole, str(item_path))  # type: ignore
                            file_item.setToolTip(str(item_path))
                            items.append((file_item, 2))  # その他ファイルは最後
            
            except PermissionError:
                error_item = QListWidgetItem("❌ アクセス権限がありません")
                self.folder_content_list.addItem(error_item)
                return
            
            # ソートして追加（フォルダ→画像→その他ファイル）
            items.sort(key=lambda x: (x[1], x[0].text()))
            
            for item, _ in items:
                self.folder_content_list.addItem(item)
            
            # ステータス更新
            folder_count = len([i for i, t in items if t == 0])
            image_count = len([i for i, t in items if t == 1])
            other_count = len([i for i, t in items if t == 2])
            
            self.main_window.show_status_message(
                f"📁 フォルダ: {folder_count}, 🖼️ 画像: {image_count}, 📄 その他: {other_count}"
            )
            
            logger.info(f"フォルダ内容更新完了: {folder_path}")
            
        except Exception as e:
            logger.error(f"フォルダ内容更新エラー: {e}")
            self.main_window.show_status_message(f"❌ フォルダ内容更新エラー: {e}")
    
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

    def refresh_folder_content(self, folder_path=None):
        """フォルダ内容を更新・リフレッシュ
        
        Args:
            folder_path (str, optional): 更新するフォルダパス
        """
        import logging
        logger = logging.getLogger(__name__)
        
        try:
            if folder_path:
                logger.info(f"フォルダ内容更新: {folder_path}")
                self.update_folder_content(folder_path)
            else:
                logger.info("フォルダ内容リフレッシュ")
                # 現在のフォルダ内容をリフレッシュ
                if hasattr(self.main_window, 'current_folder') and self.main_window.current_folder:
                    self.update_folder_content(self.main_window.current_folder)
                    
            # ステータス更新
            self.main_window.show_status_message("📁 フォルダ内容を更新しました")
            
        except Exception as e:
            logger.error(f"フォルダ内容更新エラー: {e}")
            self.main_window.show_status_message(f"❌ フォルダ内容更新エラー: {e}")
