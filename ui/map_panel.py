from ui.map_view import create_map_view
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class MapPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.view = create_map_view()
        self.view.setMinimumHeight(200)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    def load_map(self, map_file):
        """ローカルファイルから地図を読み込み"""
        self.view.load(QUrl.fromLocalFile(map_file))
    
    def set_map_html(self, html_content):
        """HTMLコンテンツを直接設定して地図を表示"""
        self.view.setHtml(html_content)
    
    def update_location(self, lat, lon):
        """指定された座標の地図を表示"""
        try:
            from logic.image_utils import generate_map_html
            html_content = generate_map_html(lat, lon)
            if html_content:
                self.set_map_html(html_content)
                return True
        except Exception as e:
            # デバッグ出力を削除し、静かに失敗
            pass
        return False


def create_map_panel():
    """マップパネルウィジェットを作成"""
    return MapPanel()
