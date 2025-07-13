from PyQt5.QtWebEngineWidgets import QWebEngineView
from utils.debug_logger import debug, info, warning, error, verbose

def create_map_view(parent=None):
    """地図ビューを作成して初期化する関数"""
    map_view = QWebEngineView(parent)
    # 初期表示内容を設定
    map_view.setHtml("<html><body><p>🗺️ 地図ビューがここに表示されます</p></body></html>")
    map_view.setMinimumSize(400, 400)

    return map_view
