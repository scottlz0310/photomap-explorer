"""
マップビューコンポーネント
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

try:
    from PyQt5.QtWebEngineWidgets import QWebEngineView
    WEB_ENGINE_AVAILABLE = True
except ImportError:
    WEB_ENGINE_AVAILABLE = False
    # WebEngineが利用できない場合のフォールバック
    from PyQt5.QtWidgets import QTextEdit as QWebEngineView


class MapWebView(QWebEngineView):
    """
    地図表示用WebEngineView
    Clean Architecture対応版
    """
    # シグナル
    map_loaded = pyqtSignal()  # 地図ロード完了時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        if WEB_ENGINE_AVAILABLE:
            # 初期表示内容を設定
            self.setHtml("<html><body><p>🗺️ 地図ビューがここに表示されます</p></body></html>")
            self.setMinimumSize(400, 400)
            
            # ロード完了シグナル接続
            if hasattr(self, 'loadFinished'):
                self.loadFinished.connect(self._on_load_finished)
        else:
            # WebEngineが利用できない場合
            self.setText("🗺️ 地図ビューがここに表示されます\n（WebEngineが利用できません）")
            self.setMinimumSize(400, 400)
    
    def _on_load_finished(self, success):
        """ロード完了時の処理"""
        if success:
            self.map_loaded.emit()
    
    def load_map_file(self, map_file_path):
        """地図ファイルを読み込み"""
        if not WEB_ENGINE_AVAILABLE:
            self.setText(f"地図ファイル: {map_file_path}\n（WebEngineが利用できません）")
            return
            
        if os.path.exists(map_file_path):
            url = QUrl.fromLocalFile(map_file_path)
            self.load(url)
        else:
            self.show_error("指定された地図ファイルが見つかりません")
    
    def show_error(self, message):
        """エラーメッセージを表示"""
        if not WEB_ENGINE_AVAILABLE:
            self.setText(f"エラー: {message}")
            return
            
        error_html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #d32f2f;">🚫 エラー</h2>
            <p>{message}</p>
        </body>
        </html>
        """
        self.setHtml(error_html)
    
    def show_no_gps_message(self):
        """GPS情報なしメッセージを表示"""
        if not WEB_ENGINE_AVAILABLE:
            self.setText("GPS情報なし\n選択された画像にはGPS情報が含まれていません。")
            return
            
        no_gps_html = """
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #ff9800;">📍 GPS情報なし</h2>
            <p>選択された画像にはGPS情報が含まれていません。</p>
            <p>位置情報付きの画像を選択してください。</p>
        </body>
        </html>
        """
        self.setHtml(no_gps_html)
    
    def show_loading_message(self):
        """ローディングメッセージを表示"""
        if not WEB_ENGINE_AVAILABLE:
            self.setText("読み込み中...\n地図を生成しています。")
            return
            
        loading_html = """
        <html>
        <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
            <h2 style="color: #2196f3;">🔄 読み込み中...</h2>
            <p>地図を生成しています。しばらくお待ちください。</p>
        </body>
        </html>
        """
        self.setHtml(loading_html)


class MapPanel(QWidget):
    """
    地図パネル（マップビュー + コントロール）
    Clean Architecture対応版
    """
    # シグナル
    map_loaded = pyqtSignal()  # 地図ロード完了時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # マップビュー
        self.map_view = MapWebView()
        self.map_view.setMinimumHeight(200)
        layout.addWidget(self.map_view)
    
    def _connect_signals(self):
        """シグナル接続"""
        self.map_view.map_loaded.connect(self.map_loaded.emit)
    
    def load_map(self, map_file_path):
        """地図ファイルを読み込み"""
        self.map_view.load_map_file(map_file_path)
    
    def show_loading(self):
        """ローディング表示"""
        self.map_view.show_loading_message()
    
    def show_no_gps_data(self):
        """GPS情報なしメッセージ表示"""
        self.map_view.show_no_gps_message()
    
    def show_error(self, message):
        """エラーメッセージ表示"""
        self.map_view.show_error(message)
    
    def clear_map(self):
        """地図をクリア"""
        if not WEB_ENGINE_AVAILABLE:
            self.map_view.setText("🗺️ 地図ビューがここに表示されます\n（WebEngineが利用できません）")
        else:
            self.map_view.setHtml("<html><body><p>🗺️ 地図ビューがここに表示されます</p></body></html>")


# 後方互換性のための関数（既存コードとの互換性維持）
def create_map_view():
    """
    レガシー関数：地図ビューを作成
    新しいMapWebViewクラスを使用して実装
    """
    return MapWebView()


def create_map_panel():
    """
    レガシー関数：地図パネルを作成
    新しいMapPanelクラスを使用して実装
    """
    return MapPanel()