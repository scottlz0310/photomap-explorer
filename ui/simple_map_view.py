"""
シンプルマップビュー（QtWebEngine非依存）

QtWebEngineが利用できない環境でも動作する
軽量なマップ表示コンポーネント
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SimpleMapView(QWidget):
    """
    シンプルなマップビュー
    
    QtWebEngineを使用せず、テキストベースで
    GPS情報を表示する軽量版
    """
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        """UI初期化"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # メインラベル
        self.main_label = QLabel()
        self.main_label.setAlignment(Qt.AlignCenter)
        self.main_label.setWordWrap(True)
        
        # フォント設定
        font = QFont()
        font.setPointSize(11)
        self.main_label.setFont(font)
        
        layout.addWidget(self.main_label)
        
        # 初期メッセージ表示
        self.show_initial_message()
    
    def show_initial_message(self):
        """初期メッセージを表示"""
        message = """
🗺️ シンプルマップビュー

GPS付きの画像を選択すると
位置情報がここに表示されます。

外部地図サービスでの詳細表示も可能です。
        """
        self.main_label.setText(message.strip())
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f5f5;
                border: 2px solid #ddd;
                border-radius: 8px;
            }
            QLabel {
                color: #666;
                padding: 20px;
            }
        """)
    
    def update_location(self, latitude, longitude):
        """
        GPS位置情報を表示
        
        Args:
            latitude (float): 緯度
            longitude (float): 経度
        """
        try:
            message = f"""
📍 GPS位置情報

緯度: {latitude:.6f}°
経度: {longitude:.6f}°

🌐 外部マップで表示:
• Google Maps
• OpenStreetMap
• 地理院地図

※ 右クリックでオプションを表示
            """
            
            self.main_label.setText(message.strip())
            self.setStyleSheet("""
                QWidget {
                    background-color: #e8f5e8;
                    border: 2px solid #4caf50;
                    border-radius: 8px;
                }
                QLabel {
                    color: #2e7d32;
                    padding: 20px;
                }
            """)
            
            # 座標をプロパティとして保存（右クリックメニュー用）
            self.latitude = latitude
            self.longitude = longitude
            
            return True
            
        except Exception as e:
            self.show_error(f"位置情報表示エラー: {e}")
            return False
    
    def show_no_gps(self):
        """GPS情報なしメッセージを表示"""
        message = """
📍 GPS情報なし

この画像には位置情報が
含まれていません。

GPS機能付きカメラや
スマートフォンで撮影された
画像を選択してください。
        """
        
        self.main_label.setText(message.strip())
        self.setStyleSheet("""
            QWidget {
                background-color: #fff3e0;
                border: 2px solid #ff9800;
                border-radius: 8px;
            }
            QLabel {
                color: #e65100;
                padding: 20px;
            }
        """)
    
    def show_error(self, error_message):
        """エラーメッセージを表示"""
        message = f"""
🚨 エラー

{error_message}

マップ表示に問題が発生しました。
        """
        
        self.main_label.setText(message.strip())
        self.setStyleSheet("""
            QWidget {
                background-color: #ffebee;
                border: 2px solid #f44336;
                border-radius: 8px;
            }
            QLabel {
                color: #c62828;
                padding: 20px;
            }
        """)
    
    def contextMenuEvent(self, event):
        """右クリックメニュー"""
        if hasattr(self, 'latitude') and hasattr(self, 'longitude'):
            from PyQt5.QtWidgets import QMenu, QAction
            
            menu = QMenu(self)
            
            # Google Maps
            google_action = QAction("Google Mapsで開く", self)
            google_action.triggered.connect(self.open_google_maps)
            menu.addAction(google_action)
            
            # OpenStreetMap
            osm_action = QAction("OpenStreetMapで開く", self)
            osm_action.triggered.connect(self.open_openstreetmap)
            menu.addAction(osm_action)
            
            # 座標をコピー
            copy_action = QAction("座標をコピー", self)
            copy_action.triggered.connect(self.copy_coordinates)
            menu.addAction(copy_action)
            
            menu.exec_(event.globalPos())
    
    def open_google_maps(self):
        """Google Mapsで開く"""
        if hasattr(self, 'latitude') and hasattr(self, 'longitude'):
            import webbrowser
            url = f"https://www.google.com/maps?q={self.latitude},{self.longitude}"
            webbrowser.open(url)
    
    def open_openstreetmap(self):
        """OpenStreetMapで開く"""
        if hasattr(self, 'latitude') and hasattr(self, 'longitude'):
            import webbrowser
            url = f"https://www.openstreetmap.org/?mlat={self.latitude}&mlon={self.longitude}&zoom=15"
            webbrowser.open(url)
    
    def copy_coordinates(self):
        """座標をクリップボードにコピー"""
        if hasattr(self, 'latitude') and hasattr(self, 'longitude'):
            from PyQt5.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            coordinates = f"{self.latitude:.6f}, {self.longitude:.6f}"
            clipboard.setText(coordinates)


def create_simple_map_view():
    """シンプルマップビューを作成"""
    return SimpleMapView()
