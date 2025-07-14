"""
画像表示・プレビュー制御を担当するマネージャー

このモジュールは functional_new_main_view.py から分離された
画像表示関連の機能を担当します。
"""

import os
import logging
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ImageDisplayManager:
    """画像表示・プレビュー制御を担当するマネージャー"""
    
    def __init__(self, main_window):
        """
        画像表示マネージャーを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.current_image = None
        self.current_pixmap = None
        
        # コンポーネント参照
        self.preview_panel = None
        self.status_info = None
        
        # 表示設定
        self.default_size = (400, 400)
        self.maximized_size = (800, 600)
        
    def set_components(self, preview_panel, status_info=None):
        """コンポーネントの参照を設定"""
        self.preview_panel = preview_panel
        self.status_info = status_info
    
    def display_image(self, image_path):
        """画像を表示"""
        try:
            if not image_path or not os.path.exists(image_path):
                self.main_window.show_status_message("❌ 画像ファイルが見つかりません")
                return False
            
            # 画像読み込み
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.main_window.show_status_message("❌ 画像読み込みに失敗しました")
                return False
            
            # 現在の画像情報を更新
            self.current_image = image_path
            self.current_pixmap = pixmap
            
            # プレビューパネルに表示
            success = self._update_preview_display(pixmap)
            
            if success:
                # 画像情報の更新
                self._update_image_info(image_path)
                self.main_window.show_status_message(f"🖼️ 画像表示: {os.path.basename(image_path)}")
                return True
            else:
                self.main_window.show_status_message("❌ 画像表示に失敗しました")
                return False
                
        except Exception as e:
            logging.error(f"画像表示エラー: {e}")
            self.main_window.show_status_message(f"❌ 画像表示エラー: {e}")
            return False
    
    def _update_preview_display(self, pixmap):
        """プレビューパネルに画像を表示"""
        try:
            if not self.preview_panel:
                return False
            
            # 表示サイズを決定
            display_size = self._get_display_size()
            
            # 画像をスケーリング
            scaled_pixmap = pixmap.scaled(
                display_size[0], display_size[1], 
                Qt.KeepAspectRatio, Qt.SmoothTransformation  # type: ignore
            )
            
            # プレビューパネルのタイプに応じて表示
            if hasattr(self.preview_panel, 'set_image'):
                # ImagePreviewViewの場合
                self.preview_panel.set_image(scaled_pixmap)
            elif hasattr(self.preview_panel, 'setPixmap'):
                # QLabel等の場合
                self.preview_panel.setPixmap(scaled_pixmap)
            elif hasattr(self.preview_panel, 'update_image'):
                # カスタム関数の場合
                self.preview_panel.update_image(self.current_image)
            else:
                logging.warning("プレビューパネルの表示方法が不明です")
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"プレビュー表示更新エラー: {e}")
            return False
    
    def _get_display_size(self):
        """表示サイズを取得（最大化状態を考慮）"""
        try:
            # 最大化状態の確認
            maximized_state = getattr(self.main_window, 'maximized_state', None)
            
            if maximized_state == 'image':
                # 最大化時はより大きくスケール
                maximize_handler = getattr(self.main_window, 'maximize_handler', None)
                if maximize_handler and hasattr(maximize_handler, 'get_available_size'):
                    available_size = maximize_handler.get_available_size()
                    if available_size:
                        max_width = max(800, available_size.width() - 50)
                        max_height = max(600, available_size.height() - 100)
                        return (max_width, max_height)
                
                # フォールバック
                return self.maximized_size
            else:
                # 通常時
                return self.default_size
                
        except Exception as e:
            logging.error(f"表示サイズ取得エラー: {e}")
            return self.default_size
    
    def _update_image_info(self, image_path):
        """画像情報を更新表示"""
        try:
            if not self.status_info:
                return
            
            # 基本情報を取得
            basic_info = self._get_basic_image_info(image_path)
            
            # EXIF情報を取得
            exif_info = self._get_exif_info(image_path)
            
            # HTML形式で表示
            info_html = self._format_image_info_html(basic_info, exif_info)
            
            self.status_info.setText(info_html)
            
        except Exception as e:
            logging.error(f"画像情報更新エラー: {e}")
            # エラー時は基本情報のみ表示
            if self.status_info:
                filename = os.path.basename(image_path)
                self.status_info.setText(f"📄 <b>{filename}</b><br>❌ 詳細情報の取得に失敗しました")
    
    def _get_basic_image_info(self, image_path):
        """基本的な画像情報を取得"""
        try:
            # ファイル情報
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
            if self.current_pixmap:
                width = self.current_pixmap.width()
                height = self.current_pixmap.height()
                dimensions = f"{width}x{height}"
            else:
                pixmap = QPixmap(image_path)
                if not pixmap.isNull():
                    dimensions = f"{pixmap.width()}x{pixmap.height()}"
                else:
                    dimensions = "不明"
            
            return {
                'filename': os.path.basename(image_path),
                'size': size_str,
                'dimensions': dimensions
            }
            
        except Exception as e:
            logging.error(f"基本画像情報取得エラー: {e}")
            return {
                'filename': os.path.basename(image_path) if image_path else "不明",
                'size': "不明",
                'dimensions': "不明"
            }
    
    def _get_exif_info(self, image_path):
        """EXIF情報を取得"""
        try:
            # 画像ユーティリティから情報を取得
            from logic.image_utils import extract_image_info
            
            image_info = extract_image_info(image_path)
            
            if not image_info:
                return {}
            
            # EXIF情報を整理
            exif_data = {}
            
            # カメラ情報
            if image_info.get('camera'):
                exif_data['camera'] = image_info['camera']
            elif image_info.get('メーカー') and image_info.get('機種'):
                maker = image_info['メーカー'].strip()
                model = image_info['機種'].strip()
                exif_data['camera'] = f"{maker} {model}" if maker and model else (maker or model or "")
            
            # 撮影日時
            if image_info.get('datetime'):
                exif_data['datetime'] = image_info['datetime']
            elif image_info.get('撮影日時'):
                exif_data['datetime'] = image_info['撮影日時']
            
            # 撮影設定
            shooting_settings = []
            
            # シャッター速度
            if image_info.get('shutter') and image_info['shutter'].strip():
                shooting_settings.append(f"シャッター: {image_info['shutter'].strip()}")
            
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
            
            if shooting_settings:
                exif_data['settings'] = ' | '.join(shooting_settings)
            
            return exif_data
            
        except Exception as e:
            logging.error(f"EXIF情報取得エラー: {e}")
            return {}
    
    def _format_image_info_html(self, basic_info, exif_info):
        """画像情報をHTML形式でフォーマット"""
        try:
            status_lines = []
            
            # ファイル名
            status_lines.append(f"📄 <b>{basic_info['filename']}</b>")
            
            # 画像サイズとファイルサイズ
            status_lines.append(f"📐 <b>サイズ:</b> {basic_info['dimensions']} | 💾 <b>容量:</b> {basic_info['size']}")
            
            # カメラ情報
            if exif_info.get('camera'):
                status_lines.append(f"📷 <b>カメラ:</b> {exif_info['camera']}")
            
            # 撮影日時
            if exif_info.get('datetime'):
                status_lines.append(f"🕒 <b>撮影日時:</b> {exif_info['datetime']}")
            
            # 撮影設定
            if exif_info.get('settings'):
                status_lines.append(f"⚙️ <b>設定:</b> {exif_info['settings']}")
            
            return "<br>".join(status_lines)
            
        except Exception as e:
            logging.error(f"画像情報HTML フォーマットエラー: {e}")
            return f"📄 <b>{basic_info.get('filename', '不明')}</b><br>❌ 情報表示エラー"
    
    def clear_display(self):
        """画像表示をクリア"""
        try:
            # プレビューパネルをクリア
            if self.preview_panel:
                if hasattr(self.preview_panel, 'clear'):
                    self.preview_panel.clear()
                elif hasattr(self.preview_panel, 'setPixmap'):
                    self.preview_panel.setPixmap(QPixmap())  # 空のPixmap
                elif hasattr(self.preview_panel, 'setText'):
                    self.preview_panel.setText("画像を選択してください")
            
            # ステータス情報をクリア
            if self.status_info:
                self.status_info.setText("画像を選択すると詳細情報が表示されます")
            
            # 現在の画像情報をクリア
            self.current_image = None
            self.current_pixmap = None
            
        except Exception as e:
            logging.error(f"画像表示クリアエラー: {e}")
    
    def refresh_display(self):
        """現在の画像を再表示"""
        try:
            if self.current_image:
                self.display_image(self.current_image)
                
        except Exception as e:
            logging.error(f"画像再表示エラー: {e}")
    
    def get_current_image(self):
        """現在表示中の画像パスを取得"""
        return self.current_image
    
    def is_image_displayed(self):
        """画像が表示されているかどうか"""
        return self.current_image is not None
    
    def set_display_size(self, width, height):
        """表示サイズを設定"""
        try:
            self.default_size = (width, height)
            
            # 現在の画像を再表示
            if self.current_image:
                self.refresh_display()
                
        except Exception as e:
            logging.error(f"表示サイズ設定エラー: {e}")
    
    def set_maximized_size(self, width, height):
        """最大化時の表示サイズを設定"""
        try:
            self.maximized_size = (width, height)
            
        except Exception as e:
            logging.error(f"最大化サイズ設定エラー: {e}")
    
    def apply_theme(self, theme_name):
        """画像表示エリアにテーマを適用"""
        try:
            if not self.preview_panel:
                return
            
            # テーマに応じたスタイル適用
            if theme_name == "dark":
                style = """
                    QLabel {
                        background-color: #2d2d2d;
                        color: #ffffff;
                        border: 1px solid #404040;
                        border-radius: 4px;
                        padding: 10px;
                    }
                """
            else:
                style = """
                    QLabel {
                        background-color: #ffffff;
                        color: #000000;
                        border: 1px solid #cccccc;
                        border-radius: 4px;
                        padding: 10px;
                    }
                """
            
            if hasattr(self.preview_panel, 'setStyleSheet'):
                self.preview_panel.setStyleSheet(style)  # type: ignore
            
            # ステータス情報エリアにもテーマを適用
            if self.status_info and hasattr(self.status_info, 'setStyleSheet'):
                self.status_info.setStyleSheet(style)  # type: ignore
                
        except Exception as e:
            logging.error(f"画像表示テーマ適用エラー: {e}")
    
    def get_image_dimensions(self):
        """現在の画像の実際のサイズを取得"""
        try:
            if self.current_pixmap:
                return (self.current_pixmap.width(), self.current_pixmap.height())
            return None
            
        except Exception as e:
            logging.error(f"画像サイズ取得エラー: {e}")
            return None
