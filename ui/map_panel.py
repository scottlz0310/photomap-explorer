from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import os


class MapPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.view = None
        self.setup_view()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
    
    def setup_view(self):
        """マップビューのセットアップ（フォールバック対応）"""
        try:
            # 最初にQtWebEngineベースを試行
            from ui.map_view import create_map_view
            self.view = create_map_view()
            self.view.setMinimumHeight(200)
            self.use_webengine = True
        except Exception as e:
            # QtWebEngineが利用できない場合はシンプルビューを使用
            print(f"QtWebEngine利用不可、シンプルビューを使用: {e}")
            from ui.simple_map_view import create_simple_map_view
            self.view = create_simple_map_view()
            self.view.setMinimumHeight(200)
            self.use_webengine = False

    def load_map(self, map_file):
        """地図ファイルを読み込み"""
        if self.use_webengine and hasattr(self.view, 'load'):
            self.view.load(QUrl.fromLocalFile(map_file))
    
    def update_location(self, latitude, longitude):
        """
        指定された緯度・経度で地図を更新
        
        Args:
            latitude (float): 緯度
            longitude (float): 経度
            
        Returns:
            bool: 成功した場合True
        """
        try:
            if self.use_webengine:
                # QtWebEngineベースの処理
                from logic.image_utils import generate_map_html
                
                # 地図HTMLファイルを生成
                map_file = generate_map_html(latitude, longitude)
                
                # 地図を読み込み
                if os.path.exists(map_file):
                    self.load_map(map_file)
                    return True
                else:
                    self._show_error_message("地図ファイルの生成に失敗しました")
                    return False
            else:
                # シンプルビューの処理
                if hasattr(self.view, 'update_location'):
                    return self.view.update_location(latitude, longitude)
                else:
                    return False
                    
        except Exception as e:
            self._show_error_message(f"地図更新エラー: {str(e)}")
            return False
    
    def _show_error_message(self, message):
        """エラーメッセージを表示"""
        if self.use_webengine and hasattr(self.view, 'setHtml'):
            error_html = f"""
            <html>
            <body style="background-color: #f8f8f8; font-family: Arial, sans-serif; padding: 20px;">
                <div style="color: #d32f2f; font-size: 14px;">
                    <strong>🚨 地図表示エラー</strong><br>
                    {message}
                </div>
            </body>
            </html>
            """
            self.view.setHtml(error_html)
        elif hasattr(self.view, 'show_error'):
            self.view.show_error(message)
    
    def show_no_gps_message(self):
        """GPS情報がない場合のメッセージを表示"""
        if self.use_webengine and hasattr(self.view, 'setHtml'):
            no_gps_html = """
            <html>
            <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px; text-align: center;">
                <div style="color: #666; font-size: 16px;">
                    <strong>📍 GPS情報がありません</strong><br><br>
                    この画像にはGPS位置情報が含まれていません。<br>
                    GPS付きカメラやスマートフォンで撮影された画像を選択してください。
                </div>
            </body>
            </html>
            """
            self.view.setHtml(no_gps_html)
        elif hasattr(self.view, 'show_no_gps'):
            self.view.show_no_gps()


def create_map_panel():
    """マップパネルを作成して返す関数"""
    return MapPanel()
