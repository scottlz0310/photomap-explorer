"""
フォルダ選択・ナビゲーション機能を担当するイベントハンドラ

このモジュールは functional_new_main_view.py から分離された
フォルダ関連のイベント処理機能を担当します。
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt
import logging


class FolderEventHandler:
    """フォルダ選択・ナビゲーション機能を担当するイベントハンドラ"""
    
    def __init__(self, main_window):
        """
        フォルダイベントハンドラを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.current_folder = None
        self.current_images = []
        
        # コンポーネント参照
        self.address_bar = None
        self.folder_content_list = None
        self.thumbnail_list = None
        
    def set_components(self, address_bar, folder_content_list, thumbnail_list):
        """UIコンポーネントの参照を設定"""
        self.address_bar = address_bar
        self.folder_content_list = folder_content_list
        self.thumbnail_list = thumbnail_list
    
    def select_folder(self):
        """フォルダ選択ダイアログ（標準的なフォルダ選択）"""
        try:
            folder = QFileDialog.getExistingDirectory(
                self.main_window,
                "フォルダを選択してください",
                self.current_folder if self.current_folder else os.path.expanduser("~"),
                QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
            )
            
            if folder:
                folder = os.path.normpath(folder)
                self.load_folder(folder)
                self.main_window.show_status_message(f"📁 フォルダ選択: {folder}")
                
        except Exception as e:
            logging.error(f"フォルダ選択ダイアログエラー: {e}")
            self.main_window.show_status_message("❌ フォルダ選択に失敗しました")
    
    def load_initial_folder(self):
        """初期フォルダ読み込み（空の状態で開始）"""
        # アドレスバーを空に設定
        if self.address_bar:
            self.address_bar.setText("")
        
        # 初期状態では何も読み込まない
        self.current_folder = None
        self.current_images = []
    
    def load_folder(self, folder_path):
        """
        フォルダ読み込み処理
        
        Args:
            folder_path (str): 読み込むフォルダパス
        """
        try:
            # パスを正規化
            folder_path = os.path.normpath(folder_path)
            self.current_folder = folder_path
            
            # アドレスバーを更新
            if self.address_bar:
                self.address_bar.setText("")
                self.address_bar.setText(folder_path)
            
            # 画像ファイル検索
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
            image_files = []
            
            folder = Path(folder_path)
            for file_path in folder.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    image_files.append(str(file_path))
            
            self.current_images = image_files
            
            # フォルダ内容表示を更新
            self._update_folder_content(folder_path)
            
            # サムネイル更新
            self._update_thumbnails(image_files)
            
        except Exception as e:
            QMessageBox.warning(self.main_window, "エラー", f"フォルダ読み込みエラー: {e}")
            self.main_window.show_status_message(f"❌ フォルダ読み込みエラー: {e}")
            logging.error(f"フォルダ読み込みエラー: {e}")
    
    def _update_folder_content(self, folder_path):
        """フォルダ内容を更新表示"""
        try:
            if not self.folder_content_list:
                return
            
            self.folder_content_list.clear()
            
            if not folder_path or not os.path.exists(folder_path):
                return
            
            folder = Path(folder_path)
            
            # 親フォルダへのリンク（ルートでない場合）
            if folder.parent != folder:
                parent_item = QListWidgetItem("📁 .. (親フォルダ)")
                parent_item.setData(Qt.UserRole, str(folder.parent))  # type: ignore
                parent_item.setToolTip(str(folder.parent))
                self.folder_content_list.addItem(parent_item)
            
            # フォルダとファイルを取得
            items = []
            
            try:
                for item_path in folder.iterdir():
                    if item_path.is_dir():
                        # フォルダ
                        folder_item = QListWidgetItem(f"📁 {item_path.name}")
                        folder_item.setData(Qt.UserRole, str(item_path))  # type: ignore
                        folder_item.setToolTip(str(item_path))
                        items.append((folder_item, 0))  # フォルダは先頭
                    elif item_path.is_file():
                        # ファイル（画像ファイルを優先表示）
                        file_ext = item_path.suffix.lower()
                        if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                            file_item = QListWidgetItem(f"🖼️ {item_path.name}")
                            file_item.setData(Qt.UserRole, str(item_path))  # type: ignore
                            file_item.setToolTip(str(item_path))
                            items.append((file_item, 1))  # 画像ファイルは2番目
                        else:
                            file_item = QListWidgetItem(f"📄 {item_path.name}")
                            file_item.setData(Qt.UserRole, str(item_path))  # type: ignore
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
            
        except Exception as e:
            self.main_window.show_status_message(f"❌ フォルダ内容表示エラー: {e}")
            logging.error(f"フォルダ内容表示詳細エラー: {e}")
    
    def _update_thumbnails(self, image_files):
        """サムネイル表示を更新"""
        try:
            if not self.thumbnail_list:
                return
            
            self.thumbnail_list.clear()
            
            # 画像ファイルを一つずつ追加
            added_count = 0
            for image_path in image_files[:50]:  # 最初の50枚まで
                try:
                    # ThumbnailListWidgetの場合
                    if hasattr(self.thumbnail_list, 'add_thumbnail'):
                        success = self.thumbnail_list.add_thumbnail(image_path)
                        if success:
                            added_count += 1
                    else:
                        # レガシー関数の場合
                        from ui.thumbnail_list import add_thumbnail
                        add_thumbnail(self.thumbnail_list, image_path)
                        added_count += 1
                except Exception as e:
                    logging.warning(f"サムネイル追加エラー({image_path}): {e}")
                    continue
            
            # 追加結果を表示
            self.main_window.show_status_message(
                f"📁 {len(image_files)}枚発見、{added_count}枚のサムネイル表示: {self.current_folder}"
            )
            
        except Exception as e:
            logging.error(f"サムネイル更新エラー: {e}")
            self.main_window.show_status_message(f"❌ サムネイル更新エラー: {e}")
    
    def on_folder_changed(self, folder_path):
        """フォルダ変更時の処理"""
        self.load_folder(folder_path)
    
    def on_folder_item_clicked(self, item):
        """フォルダアイテムクリック時の処理"""
        try:
            item_path = item.data(Qt.UserRole)  # type: ignore
            if item_path and os.path.exists(item_path):
                if os.path.isdir(item_path):
                    # フォルダの場合は移動
                    self.load_folder(item_path)
                elif os.path.isfile(item_path):
                    # ファイルの場合は選択通知
                    if hasattr(self.main_window, 'on_image_selected'):
                        self.main_window.on_image_selected(item)
                        
        except Exception as e:
            logging.error(f"フォルダアイテムクリックエラー: {e}")
            self.main_window.show_status_message(f"❌ アイテム選択エラー: {e}")
    
    def on_folder_item_double_clicked(self, item):
        """フォルダアイテムダブルクリック時の処理"""
        try:
            item_path = item.data(Qt.UserRole)  # type: ignore
            if item_path and os.path.exists(item_path):
                if os.path.isdir(item_path):
                    # フォルダの場合は移動
                    self.load_folder(item_path)
                    self.main_window.show_status_message(f"📁 フォルダ移動: {os.path.basename(item_path)}")
                elif os.path.isfile(item_path):
                    # 画像ファイルの場合は画像表示管理に委譲
                    if self.main_window.image_event_hdlr:
                        self.main_window.image_event_hdlr.on_image_selected(item)
                        
        except Exception as e:
            logging.error(f"フォルダアイテムダブルクリックエラー: {e}")
            self.main_window.show_status_message(f"❌ アイテムダブルクリックエラー: {e}")
