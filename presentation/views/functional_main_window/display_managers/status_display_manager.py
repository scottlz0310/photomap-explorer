"""
ステータス・EXIF情報表示を担当するマネージャー

このモジュールは functional_new_main_view.py から分離された
ステータス情報・EXIF表示関連の機能を担当します。
"""

import os
import logging
from PyQt5.QtWidgets import QLabel


class StatusDisplayManager:
    """ステータス・EXIF情報表示を担当するマネージャー"""
    
    def __init__(self, main_window):
        """
        ステータス表示マネージャーを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.current_image = None
        
        # コンポーネント参照
        self.status_info = None
        self.status_bar = None
        
    def set_components(self, status_info=None, status_bar=None):
        """コンポーネントの参照を設定"""
        self.status_info = status_info
        self.status_bar = status_bar
    
    def update_image_status(self, image_path):
        """画像のステータス情報を更新"""
        try:
            if not image_path or not os.path.exists(image_path):
                self.clear_image_status()
                return False
            
            self.current_image = image_path
            
            # 基本情報とEXIF情報を取得
            basic_info = self._get_basic_info(image_path)
            exif_info = self._get_exif_info(image_path)
            gps_info = self._get_gps_info(image_path)
            
            # ステータス情報を更新
            if self.status_info:
                info_html = self._format_detailed_info_html(basic_info, exif_info, gps_info)
                self.status_info.setText(info_html)
            
            # ステータスバーを更新
            if self.status_bar:
                status_text = self._format_status_bar_text(basic_info)
                self.show_status_message(status_text)
            
            return True
            
        except Exception as e:
            logging.error(f"画像ステータス更新エラー: {e}")
            self._show_error_status(image_path, str(e))
            return False
    
    def _get_basic_info(self, image_path):
        """基本的な画像情報を取得"""
        try:
            # ファイル情報
            file_stat = os.stat(image_path)
            file_size = file_stat.st_size
            
            # ファイルサイズを人間読み取り可能な形式に変換
            size_str = self._format_file_size(file_size)
            
            # 画像サイズを取得
            dimensions = self._get_image_dimensions(image_path)
            
            return {
                'filename': os.path.basename(image_path),
                'filepath': image_path,
                'size': size_str,
                'size_bytes': file_size,
                'dimensions': dimensions
            }
            
        except Exception as e:
            logging.error(f"基本情報取得エラー: {e}")
            return {
                'filename': os.path.basename(image_path) if image_path else "不明",
                'filepath': image_path or "",
                'size': "不明",
                'size_bytes': 0,
                'dimensions': "不明"
            }
    
    def _get_exif_info(self, image_path):
        """EXIF情報を取得"""
        try:
            # 画像ユーティリティから情報を取得
            try:
                from logic.image_utils import extract_image_metadata
                image_info = extract_image_metadata(image_path)
            except ImportError:
                logging.warning("extract_image_metadata が利用できません")
                return {}
            
            if not image_info:
                return {}
            
            # EXIF情報を整理
            exif_data = {}
            
            # カメラ情報
            camera = self._extract_camera_info(image_info)
            if camera:
                exif_data['camera'] = camera
            
            # 撮影日時
            datetime_info = self._extract_datetime_info(image_info)
            if datetime_info:
                exif_data['datetime'] = datetime_info
            
            # 撮影設定
            settings = self._extract_shooting_settings(image_info)
            if settings:
                exif_data['settings'] = settings
            
            return exif_data
            
        except Exception as e:
            logging.error(f"EXIF情報取得エラー: {e}")
            return {}
    
    def _get_gps_info(self, image_path):
        """GPS情報を取得"""
        try:
            from logic.image_utils import extract_gps_coords
            return extract_gps_coords(image_path)
            
        except ImportError:
            logging.warning("extract_gps_coords が利用できません")
            return None
        except Exception as e:
            logging.error(f"GPS情報取得エラー: {e}")
            return None
    
    def _extract_camera_info(self, image_info):
        """カメラ情報を抽出"""
        try:
            if image_info.get('camera'):
                return image_info['camera']
            
            maker = image_info.get('メーカー', '').strip()
            model = image_info.get('機種', '').strip()
            
            if maker and model:
                return f"{maker} {model}"
            elif maker or model:
                return maker or model
            
            return None
            
        except Exception as e:
            logging.error(f"カメラ情報抽出エラー: {e}")
            return None
    
    def _extract_datetime_info(self, image_info):
        """撮影日時情報を抽出"""
        try:
            return image_info.get('datetime') or image_info.get('撮影日時')
            
        except Exception as e:
            logging.error(f"日時情報抽出エラー: {e}")
            return None
    
    def _extract_shooting_settings(self, image_info):
        """撮影設定を抽出"""
        try:
            settings = []
            
            # シャッター速度
            shutter = image_info.get('shutter', '').strip()
            if shutter:
                settings.append(f"シャッター: {shutter}")
            
            # 絞り値
            aperture = image_info.get('aperture', '').strip() or image_info.get('絞り値', '').strip()
            if aperture:
                settings.append(f"絞り: {aperture}")
            
            # ISO感度
            iso = image_info.get('iso', '').strip() or image_info.get('ISO感度', '').strip()
            if iso:
                settings.append(f"ISO: {iso}")
            
            # 焦点距離
            focal = image_info.get('focal_length', '').strip() or image_info.get('焦点距離', '').strip()
            if focal:
                settings.append(f"焦点距離: {focal}")
            
            return ' | '.join(settings) if settings else None
            
        except Exception as e:
            logging.error(f"撮影設定抽出エラー: {e}")
            return None
    
    def _format_file_size(self, file_size):
        """ファイルサイズを人間読み取り可能な形式に変換"""
        try:
            if file_size < 1024:
                return f"{file_size} B"
            elif file_size < 1024 * 1024:
                return f"{file_size / 1024:.1f} KB"
            elif file_size < 1024 * 1024 * 1024:
                return f"{file_size / (1024 * 1024):.1f} MB"
            else:
                return f"{file_size / (1024 * 1024 * 1024):.1f} GB"
                
        except Exception as e:
            logging.error(f"ファイルサイズフォーマットエラー: {e}")
            return "不明"
    
    def _get_image_dimensions(self, image_path):
        """画像のサイズを取得"""
        try:
            from PyQt5.QtGui import QPixmap
            from utils.debug_logger import debug, info, warning, error, verbose
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                return f"{pixmap.width()}x{pixmap.height()}"
            return "不明"
            
        except Exception as e:
            logging.error(f"画像サイズ取得エラー: {e}")
            return "不明"
    
    def _format_detailed_info_html(self, basic_info, exif_info, gps_info):
        """詳細情報をHTML形式でフォーマット"""
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
            
            # GPS情報
            if gps_info and 'latitude' in gps_info and 'longitude' in gps_info:
                lat, lon = gps_info['latitude'], gps_info['longitude']
                status_lines.append(f"🌍 <b>GPS:</b> {lat:.6f}, {lon:.6f}")
            else:
                status_lines.append(f"🌍 <b>GPS:</b> 位置情報なし")
            
            return "<br>".join(status_lines)
            
        except Exception as e:
            logging.error(f"詳細情報HTMLフォーマットエラー: {e}")
            return f"📄 <b>{basic_info.get('filename', '不明')}</b><br>❌ 詳細情報表示エラー"
    
    def _format_status_bar_text(self, basic_info):
        """ステータスバー用のテキストをフォーマット"""
        try:
            return f"📄 {basic_info['filename']} | 📐 {basic_info['dimensions']} | 💾 {basic_info['size']}"
            
        except Exception as e:
            logging.error(f"ステータスバーテキストフォーマットエラー: {e}")
            return f"📄 {basic_info.get('filename', '不明')}"
    
    def _show_error_status(self, image_path, error_msg):
        """エラー時のステータス表示"""
        try:
            filename = os.path.basename(image_path) if image_path else "不明"
            
            if self.status_info:
                self.status_info.setText(f"📄 <b>{filename}</b><br>❌ 詳細情報の取得に失敗しました<br><small>{error_msg}</small>")
            
            if self.status_bar:
                self.show_status_message(f"❌ ステータス更新エラー: {filename}")
                
        except Exception as e:
            logging.error(f"エラーステータス表示エラー: {e}")
    
    def clear_image_status(self):
        """画像詳細情報をクリア"""
        try:
            if self.status_info:
                self.status_info.setText("画像を選択すると詳細情報が表示されます")
            
            if self.status_bar:
                self.show_status_message("📁 画像を選択してください")
            
            self.current_image = None
            
        except Exception as e:
            logging.error(f"ステータスクリアエラー: {e}")
    
    def show_status_message(self, message, timeout=3000):
        """ステータスメッセージを表示"""
        try:
            # メインウィンドウのステータス表示メソッドを使用
            if hasattr(self.main_window, 'show_status_message'):
                self.main_window.show_status_message(message)
                return
            
            # ステータスバーが利用可能な場合
            if self.status_bar and hasattr(self.status_bar, 'showMessage'):
                self.status_bar.showMessage(message, timeout)
                return
            
            # フォールバック: コンソール出力
            from utils.debug_logger import info
            info(f"[STATUS] {message}")
            
        except Exception as e:
            logging.error(f"ステータスメッセージ表示エラー: {e}")
    
    def update_folder_status(self, folder_path, image_count=0, file_count=0):
        """フォルダ選択時のステータス更新"""
        try:
            if folder_path:
                folder_name = os.path.basename(folder_path)
                message = f"📁 {folder_name} | 🖼️ 画像: {image_count} | 📄 ファイル: {file_count}"
            else:
                message = "📁 フォルダが選択されていません"
            
            self.show_status_message(message)
            
        except Exception as e:
            logging.error(f"フォルダステータス更新エラー: {e}")
    
    def update_progress_status(self, message, progress=None):
        """進行状況のステータス更新"""
        try:
            if progress is not None:
                full_message = f"{message} ({progress}%)"
            else:
                full_message = message
            
            self.show_status_message(full_message)
            
        except Exception as e:
            logging.error(f"進行状況ステータス更新エラー: {e}")
    
    def get_current_image(self):
        """現在のステータス表示対象画像を取得"""
        return self.current_image
    
    def apply_theme(self, theme_name):
        """ステータス表示エリアにテーマを適用"""
        try:
            if not self.status_info:
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
                        font-size: 11px;
                        line-height: 1.4;
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
                        font-size: 11px;
                        line-height: 1.4;
                    }
                """
            
            if hasattr(self.status_info, 'setStyleSheet'):
                self.status_info.setStyleSheet(style)  # type: ignore
                
        except Exception as e:
            logging.error(f"ステータステーマ適用エラー: {e}")
    
    def refresh_status(self):
        """現在の画像でステータスを再表示"""
        try:
            if self.current_image:
                self.update_image_status(self.current_image)
                
        except Exception as e:
            logging.error(f"ステータス再表示エラー: {e}")
