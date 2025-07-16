"""
画像選択・表示イベント処理を担当するハンドラ

このモジュールは functional_new_main_view.py から分離された
画像関連のイベント処理機能を担当します。
"""

import os
from pathlib import Path
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import logging


class ImageEventHandler:
    """画像選択・表示イベント処理を担当するハンドラ"""
    
    def __init__(self, main_window):
        """
        画像イベントハンドラを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.selected_image = None
        
        # コンポーネント参照
        self.preview_panel = None
        self.map_panel = None
        
    def set_components(self, preview_panel, map_panel):
        """UIコンポーネントの参照を設定"""
        self.preview_panel = preview_panel
        self.map_panel = map_panel
    
    def on_image_selected(self, item_or_path):
        """画像選択時の処理"""
        try:
            logging.info(f"🔍 on_image_selected開始: {item_or_path}")
            logging.info(f"🔍 item_or_path型: {type(item_or_path)}")
            image_path = None
            
            # 文字列パスが直接渡された場合
            if isinstance(item_or_path, str):
                logging.info(f"🔍 文字列パス検出: {item_or_path}")
                if os.path.exists(item_or_path):
                    image_path = item_or_path
                    logging.info(f"🔍 文字列パス有効: {image_path}")
                else:
                    logging.warning(f"🔍 文字列パス無効: {item_or_path}")
            else:
                # QListWidgetItemが渡された場合の従来の処理
                logging.info(f"🔍 QListWidgetItem検出: {item_or_path}")
                item = item_or_path
                
                # 複数の方法でパスを取得
                if hasattr(item, 'data') and hasattr(item.data, '__call__'):
                    # Qt.UserRoleからパスを取得
                    try:
                        image_path = item.data(Qt.UserRole)  # type: ignore
                    except:
                        pass
                
                # ファイル名から完全パスを構築
                if not image_path and hasattr(item, 'text'):
                    filename = item.text()
                    if hasattr(self.main_window, 'current_folder') and self.main_window.current_folder and filename:
                        image_path = os.path.join(self.main_window.current_folder, filename)
                
                # 直接テキストからパスを取得
                if not image_path and hasattr(item, 'text'):
                    text = item.text()
                    if text and os.path.exists(text):
                        image_path = text
            
            # パスが取得できた場合の処理
            if image_path and os.path.exists(image_path):
                logging.info(f"🔍 画像パス確定: {image_path}")
                self.selected_image = image_path
                logging.info(f"🔍 display_image呼び出し直前")
                self.display_image(image_path)
                logging.info(f"🔍 display_image呼び出し完了")
                self.main_window.show_status_message(f"🖼️ 画像選択: {os.path.basename(image_path)}")
            else:
                logging.warning(f"🔍 画像パス取得失敗: {item_or_path}")
                logging.warning(f"🔍 image_path値: {image_path}")
                logging.warning(f"🔍 os.path.exists結果: {os.path.exists(image_path) if image_path else 'image_path is None'}")
                self.main_window.show_status_message(f"❌ 画像パスが取得できません: {item_or_path}")
                
        except Exception as e:
            logging.error(f"🔍 on_image_selected例外: {e}")
            import traceback
            logging.error(f"🔍 on_image_selectedトレースバック: {traceback.format_exc()}")
            self.main_window.show_status_message(f"❌ 画像選択エラー: {e}")
            logging.error(f"画像選択詳細エラー: {e}")
    
    def display_image(self, image_path):
        """画像表示"""
        try:
            logging.info(f"🔍 display_image開始: {image_path}")
            
            # 右パネルを表示（画像選択時に表示）
            logging.info("🔍 右パネル表示処理開始")
            if hasattr(self.main_window, 'right_panel_mgr') and self.main_window.right_panel_mgr:
                if hasattr(self.main_window.right_panel_mgr, 'panel') and self.main_window.right_panel_mgr.panel:
                    self.main_window.right_panel_mgr.panel.show()
                    logging.info("🔍 右パネル表示完了")
                if hasattr(self.main_window.right_panel_mgr, 'right_splitter') and self.main_window.right_panel_mgr.right_splitter:
                    splitter = self.main_window.right_panel_mgr.right_splitter
                    splitter.show()
                    logging.info("🔍 右スプリッター表示完了")
                    
                    # スプリッターの詳細状態確認
                    sizes = splitter.sizes()
                    logging.info(f"🔍 スプリッターサイズ配分: {sizes}")
                    logging.info(f"🔍 スプリッター子要素数: {splitter.count()}")
                    
                    # 子要素の表示状態確認
                    for i in range(splitter.count()):
                        widget = splitter.widget(i)
                        if widget:
                            logging.info(f"🔍 子要素{i}: 型={type(widget).__name__}, 可視={widget.isVisible()}, サイズ={widget.size().width()}x{widget.size().height()}")
                            # 地図関連ウィジェットの詳細確認
                            if hasattr(widget, 'windowTitle') and 'マップ' in str(widget.windowTitle()):
                                logging.info(f"🔍 地図グループ発見: {widget}")
            
            # メインウィンドウの右パネル直接参照も確認
            if hasattr(self.main_window, 'right_panel') and self.main_window.right_panel:
                self.main_window.right_panel.show()
                logging.info("🔍 メイン右パネル表示完了")
            if hasattr(self.main_window, 'right_splitter') and self.main_window.right_splitter:
                self.main_window.right_splitter.show()
                logging.info("🔍 メイン右スプリッター表示完了")
            logging.info("🔍 右パネル表示処理完了")
            
            # プレビュー表示
            if self.preview_panel:
                logging.info("🔍 プレビューパネル表示処理開始")
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    if hasattr(self.preview_panel, 'set_image'):
                        # ImagePreviewViewの場合
                        self.preview_panel.set_image(pixmap)
                    elif hasattr(self.preview_panel, 'setPixmap'):
                        # QLabel等の場合
                        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type: ignore
                        self.preview_panel.setPixmap(scaled_pixmap)
                    elif hasattr(self.preview_panel, 'update_image'):
                        # カスタム関数の場合
                        self.preview_panel.update_image(image_path)
                    
                    self.main_window.show_status_message(f"🖼️ プレビュー表示成功: {os.path.basename(image_path)}")
                    logging.info("🔍 プレビューパネル表示処理完了")
                else:
                    self.main_window.show_status_message("❌ 画像読み込み失敗")
                    logging.error("🔍 画像読み込み失敗")
            
            # 詳細情報表示
            logging.info("🔍 update_image_status呼び出し開始")
            self.update_image_status(image_path)
            logging.info("🔍 update_image_status呼び出し完了")
            
            # GPS情報取得してマップ表示
            logging.info("🔍 update_map呼び出し開始")
            self.update_map(image_path)
            logging.info("🔍 update_map呼び出し完了")
            
        except Exception as e:
            self.main_window.show_status_message(f"❌ 画像表示エラー: {e}")
            logging.error(f"画像表示詳細エラー: {e}")
            import traceback
            logging.error(f"🔍 display_imageトレースバック: {traceback.format_exc()}")
    
    def update_image_status(self, image_path):
        """画像のステータス情報を更新"""
        try:
            # 基本的な画像情報を取得
            file_stat = os.stat(image_path)
            file_size = file_stat.st_size
            
            # ファイルサイズを人間読み取り可能な形式に変換
            if file_size < 1024:
                size_str = f"{file_size} B"
            elif file_size < 1024 * 1024:
                size_str = f"{file_size / 1024:.1f} KB"
            else:
                size_str = f"{file_size / (1024 * 1024):.1f} MB"
            
            # 画像サイズを取得
            try:
                pixmap = QPixmap(image_path)
                width = pixmap.width()
                height = pixmap.height()
                dimensions = f"{width}x{height}"
            except:
                dimensions = "不明"
            
            # ステータス表示
            filename = os.path.basename(image_path)
            status_msg = f"📄 {filename} | 📐 {dimensions} | 💾 {size_str}"
            self.main_window.show_status_message(status_msg)
            
        except Exception as e:
            logging.error(f"画像ステータス更新エラー: {e}")
    
    def update_map(self, image_path):
        """GPS情報を取得してマップを更新"""
        try:
            if not self.map_panel:
                self.main_window.show_status_message("📍 マップパネルが利用できません")
                logging.warning("MapPanel is None")
                return
            
            # デバッグ: MapPanelの型確認
            logging.info(f"🔍 MapPanel type: {type(self.map_panel).__name__}")
            logging.info(f"🔍 MapPanel has update_location: {hasattr(self.map_panel, 'update_location')}")
            logging.info(f"🔍 MapPanel has view: {hasattr(self.map_panel, 'view')}")
            
            # 地図パネルを強制表示
            if hasattr(self.map_panel, 'show'):
                self.map_panel.show()
                logging.info("🔍 地図パネル強制表示完了")
            
            # 地図パネルの親（地図グループ）も強制表示
            if hasattr(self.map_panel, 'parent') and self.map_panel.parent():
                parent = self.map_panel.parent()
                if hasattr(parent, 'show'):
                    parent.show()
                    logging.info(f"🔍 地図親要素強制表示完了: {type(parent).__name__}")
            
            # GPS情報抽出
            from logic.image_utils import extract_gps_coords
            gps_info = extract_gps_coords(image_path)
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                logging.info(f"🔍 GPS extracted: {lat:.6f}, {lon:.6f}")
                
                # マップ更新
                if hasattr(self.map_panel, 'update_location'):
                    logging.info("🔍 Calling map_panel.update_location()")
                    success = self.map_panel.update_location(lat, lon)
                    logging.info(f"🔍 update_location result: {success}")
                    
                    if success:
                        self.main_window.show_status_message(f"📍 マップ表示: {lat:.6f}, {lon:.6f}")
                        logging.info("✅ Map updated successfully")
                        
                        # 地図更新後に追加の強制表示処理
                        from PyQt5.QtCore import QTimer
                        def force_map_visibility():
                            try:
                                if self.map_panel and hasattr(self.map_panel, 'view') and self.map_panel.view:
                                    view = self.map_panel.view
                                    if hasattr(view, 'show'):
                                        view.show()
                                    if hasattr(view, 'setVisible'):
                                        view.setVisible(True)
                                    if hasattr(view, 'raise_'):
                                        view.raise_()
                                    logging.info("🔍 地図ビュー追加強制表示完了")
                            except Exception as e:
                                logging.warning(f"地図ビュー強制表示エラー: {e}")
                        
                        # 300ms後に強制表示
                        QTimer.singleShot(300, force_map_visibility)
                    else:
                        self.main_window.show_status_message("📍 マップ更新に失敗")
                        logging.error("❌ Map update failed")
                elif hasattr(self.map_panel, 'view'):
                    logging.info("🔍 Using fallback GPS HTML display")
                    # HTMLベースのマップ表示
                    self._show_gps_html(lat, lon, image_path)
                    self.main_window.show_status_message(f"📍 GPS表示: {lat:.6f}, {lon:.6f}")
                else:
                    logging.error("🔍 No map display method available")
                    self.main_window.show_status_message("📍 マップ機能が利用できません")
            else:
                logging.info("🔍 No GPS info found in image")
                # GPS情報なしの場合
                if hasattr(self.map_panel, 'view'):
                    self._show_no_gps_html()
                self.main_window.show_status_message("📍 GPS情報が見つかりません")
                
        except Exception as e:
            self.main_window.show_status_message(f"❌ マップ更新エラー: {e}")
            logging.error(f"マップ更新詳細エラー: {e}")
            import traceback
            logging.error(f"Traceback: {traceback.format_exc()}")
    
    def _show_gps_html(self, lat, lon, image_path):
        """GPS情報のHTML表示"""
        try:
            if hasattr(self.map_panel, 'view') and self.map_panel.view:  # type: ignore
                gps_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px; margin: 0; background-color: #2d2d2d; color: #ffffff;">
                <div style="background: #3d3d3d; border: 2px solid #007ACC; border-radius: 10px; padding: 20px; max-width: 400px; margin: 0 auto;">
                    <h3 style="color: #007ACC; margin-top: 0;">📍 GPS座標情報</h3>
                    <p style="margin: 10px 0;"><strong>緯度:</strong> {lat:.6f}</p>
                    <p style="margin: 10px 0;"><strong>経度:</strong> {lon:.6f}</p>
                    <p style="margin: 10px 0; color: #cccccc;"><strong>画像:</strong> {os.path.basename(image_path)}</p>
                    <div style="margin-top: 15px; padding: 10px; background: #4d4d4d; border-radius: 5px;">
                        <small style="color: #cccccc;">GPS座標が含まれています</small>
                    </div>
                </div>
            </body>
            </html>
            """
            self.map_panel.view.setHtml(gps_html)  # type: ignore
            self.map_panel.view.update()  # type: ignore
            self.map_panel.view.repaint()  # type: ignore
        except Exception as e:
            logging.error(f"GPS HTML表示エラー: {e}")
    
    def _show_no_gps_html(self):
        """GPS情報なしのHTML表示"""
        try:
            no_gps_html = """
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; margin: 0; background-color: #2d2d2d; color: #ffffff;">
                <div style="background: #3d3d3d; border: 2px solid #ff6b35; border-radius: 10px; padding: 30px; max-width: 400px; margin: 0 auto;">
                    <h3 style="color: #ff6b35; margin-top: 0;">📍 GPS情報なし</h3>
                    <p style="color: #cccccc; margin: 15px 0;">この画像にはGPS座標が含まれていません。</p>
                    <div style="margin-top: 20px; padding: 10px; background: #4d4d4d; border-radius: 5px;">
                        <small style="color: #cccccc;">位置情報付きの画像を選択してください</small>
                    </div>
                </div>
            </body>
            </html>
            """
            self.map_panel.view.setHtml(no_gps_html)  # type: ignore
            self.map_panel.view.update()  # type: ignore
            self.map_panel.view.repaint()  # type: ignore
        except Exception as e:
            logging.error(f"GPS無し HTML表示エラー: {e}")
    
    def update_preview_display(self, image_path):
        """プレビュー表示を更新（最大化状態対応）"""
        try:
            if not self.preview_panel or not image_path:
                return
            
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                if hasattr(self.preview_panel, 'set_image'):
                    # ImagePreviewViewの場合
                    self.preview_panel.set_image(pixmap)
                elif hasattr(self.preview_panel, 'setPixmap'):
                    # QLabel等の場合 - 最大化状態に応じてサイズを調整
                    maximized_state = getattr(self.main_window, 'maximized_state', None)
                    if maximized_state == 'image':
                        # 最大化時はより大きくスケール
                        maximize_container = getattr(self.main_window, 'maximize_container', None)
                        if maximize_container:
                            available_size = maximize_container.size()
                            max_width = max(800, available_size.width() - 50)
                            max_height = max(600, available_size.height() - 100)
                            scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type: ignore
                        else:
                            scaled_pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type: ignore
                    else:
                        # 通常時
                        scaled_pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type: ignore
                    self.preview_panel.setPixmap(scaled_pixmap)
                elif hasattr(self.preview_panel, 'update_image'):
                    # カスタム関数の場合
                    self.preview_panel.update_image(image_path)
                
                self.main_window.show_status_message(f"🖼️ プレビュー更新: {os.path.basename(image_path)}")
            
        except Exception as e:
            self.main_window.show_status_message(f"❌ プレビュー更新エラー: {e}")
            logging.error(f"プレビュー更新詳細エラー: {e}")
    
    def update_map_display(self, image_path):
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
                        self.main_window.show_status_message(f"📍 マップ更新: {lat:.6f}, {lon:.6f}")
                    else:
                        self.main_window.show_status_message("📍 マップ更新に失敗しました")
                elif hasattr(self.map_panel, 'view'):
                    # 最大化状態でも同じHTML表示を使用
                    maximized_state = getattr(self.main_window, 'maximized_state', None)
                    status_text = "最大化表示中" if maximized_state == 'map' else "GPS座標が含まれています"
                    
                    html_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 20px; margin: 0; background-color: #2d2d2d; color: #ffffff;">
                        <div style="background: #3d3d3d; border: 2px solid #007ACC; border-radius: 10px; padding: 20px; max-width: 400px; margin: 0 auto;">
                            <h3 style="color: #007ACC; margin-top: 0;">📍 GPS座標情報</h3>
                            <p style="margin: 10px 0;"><strong>緯度:</strong> {lat:.6f}</p>
                            <p style="margin: 10px 0;"><strong>経度:</strong> {lon:.6f}</p>
                            <p style="margin: 10px 0; color: #cccccc;"><strong>画像:</strong> {os.path.basename(image_path)}</p>
                            <div style="margin-top: 15px; padding: 10px; background: #4d4d4d; border-radius: 5px;">
                                <small style="color: #cccccc;">{status_text}</small>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    self.map_panel.view.setHtml(html_content)
                    self.main_window.show_status_message(f"📍 マップ表示: {lat:.6f}, {lon:.6f}")
                else:
                    self.main_window.show_status_message("📍 マップ機能が利用できません")
            else:
                # GPS情報がない場合
                if hasattr(self.map_panel, 'view'):
                    self._show_no_gps_html()
                self.main_window.show_status_message("📍 GPS情報が見つかりません")
                
        except Exception as e:
            self.main_window.show_status_message(f"❌ マップ更新エラー: {e}")
            logging.error(f"マップ更新詳細エラー: {e}")
    
    def on_folder_item_clicked(self, item):
        """フォルダ項目クリック時の処理"""
        try:
            item_path = item.data(Qt.UserRole)  # type: ignore
            if not item_path:
                return
            
            # パス情報をステータスバーに表示
            self.main_window.show_status_message(f"📌 選択: {item_path}")
            
        except Exception as e:
            self.main_window.show_status_message(f"❌ 項目選択エラー: {e}")
    
    def on_folder_item_double_clicked(self, item):
        """フォルダ項目ダブルクリック時の処理"""
        try:
            item_path = item.data(Qt.UserRole)  # type: ignore
            if not item_path or not os.path.exists(item_path):
                self.main_window.show_status_message("❌ パスが見つかりません")
                return
            
            if os.path.isdir(item_path):
                # フォルダの場合：移動（フォルダハンドラに委譲）
                if hasattr(self.main_window, 'folder_handler'):
                    self.main_window.folder_handler.load_folder(item_path)
                    self.main_window.show_status_message(f"📁 フォルダ移動: {item_path}")
            elif os.path.isfile(item_path):
                # ファイルの場合：画像なら表示
                file_ext = Path(item_path).suffix.lower()
                if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                    self.selected_image = item_path
                    self.display_image(item_path)
                    self.main_window.show_status_message(f"🖼️ 画像表示: {os.path.basename(item_path)}")
                else:
                    self.main_window.show_status_message(f"📄 ファイル選択: {os.path.basename(item_path)}")
            
        except Exception as e:
            self.main_window.show_status_message(f"❌ ダブルクリック処理エラー: {e}")
            logging.error(f"ダブルクリック処理エラー: {e}")
