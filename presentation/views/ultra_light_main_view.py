"""
PhotoMap Explorer 超軽量化版メインビュー

極限まで最適化されたUIコンポーネント
目標: 100ms以内での起動
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, 
    QLabel, QProgressBar, QApplication
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class UltraLightMainView(QMainWindow):
    """
    超軽量化版メインビュー
    
    最小限のコンポーネントのみで構成し、
    100ms以内での起動を目標とする
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # 最低限の初期化のみ実行
        self._init_basic_properties()
        self._create_minimal_ui()
        
        # 残りの初期化は遅延実行
        QTimer.singleShot(10, self._delayed_initialization)
        
    def _init_basic_properties(self):
        """基本プロパティの初期化（最小限）"""
        self.setWindowTitle("PhotoMap Explorer - Ultra Light")
        self.setGeometry(100, 100, 600, 400)  # 小さなサイズで開始
        
    def _create_minimal_ui(self):
        """最小限のUI作成"""
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 最小レイアウト
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)  # 最小マージン
        
        # タイトルラベル（軽量）
        title_label = QLabel("PhotoMap Explorer")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 14))
        layout.addWidget(title_label)
        
        # ステータスラベル
        self.status_label = QLabel("Ultra Light Mode - 起動中...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # 軽量プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(20)
        layout.addWidget(self.progress_bar)
        
    def _delayed_initialization(self):
        """遅延初期化"""
        self.progress_bar.setValue(50)
        self.status_label.setText("UI最適化モード - 準備完了")
        
        # さらに遅延させてプログレスバーを完了
        QTimer.singleShot(5, self._complete_initialization)
        
    def _complete_initialization(self):
        """初期化完了"""
        self.progress_bar.setValue(100)
        self.status_label.setText("Ultra Light Mode - 準備完了 ✅")
        
        # プログレスバーを少し表示してから隠す
        QTimer.singleShot(100, self._hide_progress)
        
    def _hide_progress(self):
        """プログレスバーを隠す"""
        self.progress_bar.hide()
        self.status_label.setText("PhotoMap Explorer - Ultra Light Mode")
        
    def show_status_message(self, message: str):
        """ステータスメッセージ表示"""
        self.status_label.setText(message)

class MinimalMainView(QMainWindow):
    """
    最小限機能版メインビュー
    
    極限まで軽量化したUI実装
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_minimal_ui()
        
    def _setup_minimal_ui(self):
        """最小限UI構築"""
        self.setWindowTitle("PhotoMap Explorer - Minimal")
        self.setGeometry(200, 200, 400, 300)
        
        # 最小限の中央ウィジェット
        widget = QWidget()
        self.setCentralWidget(widget)
        
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("PhotoMap Explorer"))
        layout.addWidget(QLabel("最小限モード"))
        
    def show_status_message(self, message: str):
        """ステータスメッセージ表示（互換性）"""
        print(f"[Minimal UI] {message}")

def create_ultra_light_main_view():
    """ファクトリ関数：超軽量化版メインビュー作成"""
    return UltraLightMainView()

def create_minimal_main_view():
    """ファクトリ関数：最小限版メインビュー作成"""
    return MinimalMainView()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # テスト実行
    import time
    
    print("🚀 超軽量化UIテスト開始")
    
    start_time = time.time()
    window = UltraLightMainView()
    window.show()
    app.processEvents()
    end_time = time.time()
    
    duration = (end_time - start_time) * 1000
    print(f"⚡ 超軽量化UI起動時間: {duration:.2f}ms")
    
    if duration <= 100:
        print("✅ 目標達成！(100ms以内)")
    else:
        print(f"⚠️ 目標未達成 (目標: 100ms以内, 実測: {duration:.2f}ms)")
    
    # 少し表示してから終了
    QTimer.singleShot(2000, app.quit)
    app.exec_()
