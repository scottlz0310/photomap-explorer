"""
フォルダ選択・ナビゲーション機能を担当するイベントハンドラ

このモジュールは functional_new_main_view.py から分離された
フォルダ関連のイベント処理機能を担当します。
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt
from utils.debug_logger import debug, info, warning, error, verbose
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
        
        # ナビゲーション履歴
        self.history = []
        self.history_index = -1
        self.navigation_controls = None
        
        # コンポーネント参照
        self.address_bar = None
        self.folder_content_list = None
        self.thumbnail_list = None
        
    def set_components(self, address_bar=None, folder_content_list=None, thumbnail_list=None, navigation_controls=None):
        """UIコンポーネントの参照を設定"""
        debug("フォルダイベントハンドラーコンポーネント設定:")
        debug(f"  - address_bar: {address_bar}")
        debug(f"  - folder_content_list: {folder_content_list}")
        debug(f"  - thumbnail_list: {thumbnail_list}")
        debug(f"  - navigation_controls: {navigation_controls}")
        
        self.address_bar = address_bar
        self.folder_content_list = folder_content_list
        self.thumbnail_list = thumbnail_list
        self.navigation_controls = navigation_controls
        
        # thumbnail_listの型チェックを強化
        if self.thumbnail_list is not None:
            actual_type = type(self.thumbnail_list)
            debug("設定されたサムネイルリストの詳細型: {actual_type}")
            debug("サムネイルリストの属性: {dir(self.thumbnail_list)}")
        
        debug("設定完了:")
        debug(f"  - self.address_bar: {self.address_bar}")
        debug(f"  - self.folder_content_list: {self.folder_content_list}")
        debug(f"  - self.thumbnail_list: {self.thumbnail_list}")
        debug(f"  - self.thumbnail_list type: {type(self.thumbnail_list) if self.thumbnail_list else 'None'}")
    
    def _get_thumbnail_widget(self):
        """サムネイルウィジェットを確実に取得"""
        # 1. 直接設定されたものを確認
        if self.thumbnail_list is not None:
            return self.thumbnail_list
        
        # 2. メインウィンドウから取得
        if hasattr(self.main_window, 'thumbnail_list') and self.main_window.thumbnail_list is not None:
            self.thumbnail_list = self.main_window.thumbnail_list
            return self.thumbnail_list
        
        # 3. 左パネルマネージャーから取得
        if hasattr(self.main_window, 'left_panel_manager'):
            left_panel = self.main_window.left_panel_manager
            if hasattr(left_panel, 'thumbnail_list') and left_panel.thumbnail_list is not None:
                self.thumbnail_list = left_panel.thumbnail_list
                return self.thumbnail_list
            if hasattr(left_panel, 'working_thumbnail_list') and left_panel.working_thumbnail_list is not None:
                self.thumbnail_list = left_panel.working_thumbnail_list
                return self.thumbnail_list
        
        return None
    
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
            
            # 履歴に追加（履歴ナビゲーション時以外）
            self._add_to_history(folder_path)
            
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
            
            # ナビゲーションボタンの状態を更新
            self._update_navigation_buttons()
            
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
            
            # フォルダが選択されたらリストを有効化
            self.folder_content_list.setEnabled(True)
            
            folder = Path(folder_path)
            
            # 親フォルダへのリンク（ルートでない場合）
            if folder.parent != folder:
                parent_item = QListWidgetItem("📁 .. (親フォルダ)")
                parent_item.setData(256, str(folder.parent))  # Qt.UserRole = 256
                parent_item.setToolTip(str(folder.parent))
                self.folder_content_list.addItem(parent_item)
            
            # フォルダとファイルを取得
            items = []
            
            try:
                for item_path in folder.iterdir():
                    if item_path.is_dir():
                        # フォルダ
                        folder_item = QListWidgetItem(f"📁 {item_path.name}")
                        folder_item.setData(256, str(item_path))  # Qt.UserRole = 256
                        folder_item.setToolTip(str(item_path))
                        items.append((folder_item, 0))  # フォルダは先頭
                    elif item_path.is_file():
                        # ファイル（画像ファイルを優先表示）
                        file_ext = item_path.suffix.lower()
                        if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                            file_item = QListWidgetItem(f"🖼️ {item_path.name}")
                            file_item.setData(256, str(item_path))  # Qt.UserRole = 256
                            file_item.setToolTip(str(item_path))
                            items.append((file_item, 1))  # 画像ファイルは2番目
                        else:
                            file_item = QListWidgetItem(f"📄 {item_path.name}")
                            file_item.setData(256, str(item_path))  # Qt.UserRole = 256
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
            verbose(f"🖼️ サムネイル更新開始: {len(image_files)}枚")
            
            # サムネイルリストの確実な取得
            thumbnail_widget = self._get_thumbnail_widget()
            if thumbnail_widget is None:
                error("サムネイルリストが取得できません")
                return
                
            info("サムネイルリスト取得成功: {type(thumbnail_widget)}")
            
            # サムネイル表示をクリア
            thumbnail_widget.clear()
            
            added_count = 0
            max_thumbnails = 50  # 表示上限
            
            for i, image_file in enumerate(image_files[:max_thumbnails]):
                if i % 10 == 0:
                    debug(f"🔄 サムネイル処理進捗: {i}/{min(len(image_files), max_thumbnails)}")
                
                try:
                    # サムネイル画像を作成
                    pixmap = self._create_thumbnail(image_file)
                    if pixmap is None:
                        continue
                        
                    # リストアイテムを作成
                    from PyQt5.QtWidgets import QListWidgetItem
                    from PyQt5.QtCore import Qt
                    from PyQt5.QtGui import QIcon
                    
                    item = QListWidgetItem()
                    item.setIcon(QIcon(pixmap))
                    item.setText(os.path.basename(image_file))
                    item.setData(256, image_file)  # Qt.UserRole = 256, フルパスを保存
                    item.setToolTip(f"ファイル: {os.path.basename(image_file)}\nパス: {image_file}")
                    
                    # リストに追加
                    thumbnail_widget.addItem(item)
                    added_count += 1
                    
                except Exception as e:
                    error("サムネイル作成エラー {image_file}: {e}")
                    continue
            
            verbose("サムネイル追加完了: {added_count}/{len(image_files[:max_thumbnails])}")
            self.main_window.show_status_message(
                f"📁 {len(image_files)}枚発見、{added_count}枚のサムネイル表示: {self.current_folder}"
            )
            
            # 最初の画像を選択してナビゲーションボタンを初期化
            if added_count > 0:
                thumbnail_widget.setCurrentRow(0)
                info("最初のサムネイルを選択")
                
                # 画像選択イベントを発火して連携を確実にする
                first_item = thumbnail_widget.item(0)
                if first_item:
                    thumbnail_widget.itemClicked.emit(first_item)
                    info("最初の画像選択イベント発火")
                
                # ナビゲーションボタンの状態を即座に更新
                self._update_navigation_buttons()
                debug("ナビゲーションボタンの初期化完了")
                
                # メインウィンドウの画像選択状態も更新
                if hasattr(self.main_window, 'selected_image'):
                    first_image_path = first_item.data(256)  # Qt.UserRole = 256
                    self.main_window.selected_image = first_image_path
                    debug("メインウィンドウ選択画像設定: {first_image_path}")
            
        except Exception as e:
            logging.error(f"サムネイル更新エラー: {e}")
            self.main_window.show_status_message(f"❌ サムネイル更新エラー: {e}")
            self.main_window.show_status_message(f"❌ サムネイル更新エラー: {e}")
    
    def _create_thumbnail(self, image_path):
        """サムネイル画像を作成"""
        try:
            from PyQt5.QtGui import QPixmap
            from PyQt5.QtCore import Qt
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                return None
            
            # 128x128のサムネイルに縮小
            scaled_pixmap = pixmap.scaled(128, 128)
            return scaled_pixmap
        except Exception as e:
            print(f"サムネイル作成エラー {image_path}: {e}")
            return None
    
    def on_folder_changed(self, folder_path):
        """フォルダ変更時の処理"""
        self.load_folder(folder_path)
    
    def on_folder_item_clicked(self, item):
        """フォルダアイテムクリック時の処理"""
        try:
            print(f"フォルダ項目クリック: {item.text()}")
            item_path = item.data(256)  # Qt.UserRole = 256
            print(f"アイテムパス: {item_path}")
            print(f"パス存在確認: {os.path.exists(item_path) if item_path else 'パスがNone'}")
            
            if item_path and os.path.exists(item_path):
                print(f"ディレクトリ判定: {os.path.isdir(item_path)}")
                print(f"ファイル判定: {os.path.isfile(item_path)}")
                
                if os.path.isdir(item_path):
                    # フォルダの場合は移動
                    print(f"フォルダに移動: {item_path}")
                    self.load_folder(item_path)
                    self.main_window.show_status_message(f"📁 フォルダ移動: {os.path.basename(item_path)}")
                elif os.path.isfile(item_path):
                    # ファイルの場合は画像選択処理
                    print(f"ファイル選択: {item_path}")
                    
                    # メインウィンドウに選択された画像を設定（最大化ハンドラー用）
                    if hasattr(self.main_window, 'selected_image'):
                        self.main_window.selected_image = item_path
                    else:
                        setattr(self.main_window, 'selected_image', item_path)
                    
                    if hasattr(self.main_window, 'image_event_handler') and self.main_window.image_event_handler:
                        self.main_window.image_event_handler.on_image_selected(item)
                        self.main_window.show_status_message(f"🖼️ 画像選択: {os.path.basename(item_path)}")
                    else:
                        self.main_window.show_status_message("❌ 画像処理ハンドラが見つかりません")
            else:
                warning("パスが存在しないか無効: {item_path}")
                self.main_window.show_status_message(f"⚠️ パスが見つかりません: {item_path}")
                        
        except Exception as e:
            import logging
            import traceback
            logging.error(f"フォルダアイテムクリックエラー: {e}")
            traceback.print_exc()
            self.main_window.show_status_message(f"❌ アイテム選択エラー: {e}")
    
    def go_to_parent_folder(self):
        """親フォルダに移動"""
        try:
            if not self.current_folder:
                self.main_window.show_status_message("❌ 現在のフォルダが設定されていません")
                return
            
            parent_folder = os.path.dirname(self.current_folder)
            if parent_folder and parent_folder != self.current_folder:
                self.load_folder(parent_folder)
                self.main_window.show_status_message(f"📁 親フォルダに移動: {os.path.basename(parent_folder)}")
            else:
                self.main_window.show_status_message("❌ 親フォルダがありません")
        except Exception as e:
            logging.error(f"親フォルダ移動エラー: {e}")
            self.main_window.show_status_message(f"❌ 親フォルダ移動エラー: {e}")
    
    def go_back(self):
        """前の画像に移動（ループ化対応）"""
        try:
            if not self.thumbnail_list:
                error("サムネイルリストが見つかりません")
                return
            
            total_count = self.thumbnail_list.count()
            if total_count == 0:
                self.main_window.show_status_message("❌ 画像がありません")
                return
            elif total_count == 1:
                self.main_window.show_status_message("ℹ️ 画像が1枚のみです")
                return
            
            current_row = self.thumbnail_list.currentRow()
            # ループ化: 最初の画像の場合は最後の画像に移動
            new_row = current_row - 1 if current_row > 0 else total_count - 1
            
            # 新しい画像に移動
            self.thumbnail_list.setCurrentRow(new_row)
            # 画像選択イベントを発生させる
            item = self.thumbnail_list.item(new_row)
            if item:
                self.thumbnail_list.itemClicked.emit(item)
                if new_row == total_count - 1:
                    self.main_window.show_status_message(f"🔄 ループ: 最後の画像 {total_count}/{total_count}")
                    info("ループして最後の画像に移動: {new_row}")
                else:
                    self.main_window.show_status_message(f"⬅️ 前の画像: {new_row + 1}/{total_count}")
                    info("前の画像に移動: {new_row}")
        except Exception as e:
            logging.error(f"前の画像移動エラー: {e}")
            self.main_window.show_status_message(f"❌ 前の画像移動エラー: {e}")
    
    def go_forward(self):
        """次の画像に移動（ループ化対応）"""
        try:
            if not self.thumbnail_list:
                error("サムネイルリストが見つかりません")
                return
            
            total_count = self.thumbnail_list.count()
            if total_count == 0:
                self.main_window.show_status_message("❌ 画像がありません")
                return
            elif total_count == 1:
                self.main_window.show_status_message("ℹ️ 画像が1枚のみです")
                return
            
            current_row = self.thumbnail_list.currentRow()
            max_row = total_count - 1
            # ループ化: 最後の画像の場合は最初の画像に移動
            new_row = current_row + 1 if current_row < max_row else 0
            
            # 新しい画像に移動
            self.thumbnail_list.setCurrentRow(new_row)
            # 画像選択イベントを発生させる
            item = self.thumbnail_list.item(new_row)
            if item:
                self.thumbnail_list.itemClicked.emit(item)
                if new_row == 0:
                    self.main_window.show_status_message(f"🔄 ループ: 最初の画像 1/{total_count}")
                    info("ループして最初の画像に移動: {new_row}")
                else:
                    self.main_window.show_status_message(f"➡️ 次の画像: {new_row + 1}/{total_count}")
                    info("次の画像に移動: {new_row}")
        except Exception as e:
            logging.error(f"次の画像移動エラー: {e}")
            self.main_window.show_status_message(f"❌ 次の画像移動エラー: {e}")
    
    def refresh_current_folder(self):
        """現在のフォルダを更新"""
        try:
            if self.current_folder:
                self._load_folder_from_history(self.current_folder)
                self.main_window.show_status_message(f"🔄 フォルダ更新: {os.path.basename(self.current_folder)}")
                info("フォルダ更新実行: {self.current_folder}")
            else:
                self.main_window.show_status_message("❌ 現在のフォルダが設定されていません")
                error("現在のフォルダが設定されていません")
        except Exception as e:
            logging.error(f"フォルダ更新エラー: {e}")
            self.main_window.show_status_message(f"❌ フォルダ更新エラー: {e}")
    
    def _add_to_history(self, folder_path):
        """履歴に追加"""
        try:
            # 現在位置より後の履歴を削除
            if self.history_index >= 0:
                self.history = self.history[:self.history_index + 1]
            
            # 同じパスの重複を避ける
            if not self.history or self.history[-1] != folder_path:
                self.history.append(folder_path)
                self.history_index = len(self.history) - 1
                info("履歴追加: {folder_path} (インデックス: {self.history_index})")
            
            # 履歴の最大数を制限（例：50個）
            if len(self.history) > 50:
                self.history = self.history[-50:]
                self.history_index = len(self.history) - 1
            
            # ナビゲーションボタンの状態を更新
            self._update_navigation_buttons()
                
        except Exception as e:
            logging.error(f"履歴追加エラー: {e}")
    
    def _update_navigation_buttons(self):
        """ナビゲーションボタンの状態を更新（サムネイル間移動用）"""
        try:
            if self.navigation_controls and self.thumbnail_list:
                current_row = self.thumbnail_list.currentRow()
                total_count = self.thumbnail_list.count()
                
                # ループ化対応: 画像が2枚以上あれば常に両方向のナビゲーションが可能
                can_back = total_count > 1
                can_forward = total_count > 1
                
                # ナビゲーションコントロールに状態設定
                if hasattr(self.navigation_controls, 'set_history_state'):
                    self.navigation_controls.set_history_state(can_back, can_forward)
                
                # 直接ボタンに状態設定
                if hasattr(self.navigation_controls, 'back_button'):
                    self.navigation_controls.back_button.setEnabled(can_back)
                if hasattr(self.navigation_controls, 'forward_button'):
                    self.navigation_controls.forward_button.setEnabled(can_forward)
                
                debug("ループナビゲーション状態更新: 戻る={can_back}, 進む={can_forward}, 現在={current_row + 1}/{total_count} (ループ対応)")
                
                # パスの設定
                if hasattr(self.navigation_controls, 'set_current_path'):
                    self.navigation_controls.set_current_path(self.current_folder or "")
                
                # 親フォルダボタンの状態も更新
                if hasattr(self.navigation_controls, 'update_button_states'):
                    self.navigation_controls.update_button_states()
            else:
                warning("navigation_controlsまたはthumbnail_listが設定されていません")
        except Exception as e:
            logging.error(f"ナビゲーションボタン更新エラー: {e}")
            error("ナビゲーションボタン更新エラー: {e}")
    
    def _load_folder_from_history(self, folder_path):
        """履歴からフォルダを読み込み（履歴に追加しない）"""
        try:
            # 一時的に履歴追加を無効にして通常の読み込みを実行
            old_history = self.history.copy()
            old_index = self.history_index
            
            self.load_folder(folder_path)
            
            # 履歴を復元（履歴ナビゲーション時は履歴を変更しない）
            self.history = old_history
            self.history_index = old_index
            
        except Exception as e:
            logging.error(f"履歴フォルダ読み込みエラー: {e}")
            self.main_window.show_status_message(f"❌ 履歴フォルダ読み込みエラー: {e}")
