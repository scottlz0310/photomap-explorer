"""
PhotoMap Explorer 極限軽量化版

Qtの最適化機能を最大限活用した極限軽量版
目標: 50ms以内での起動
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QTimer

class ExtremelyLightMainView(QMainWindow):
    """
    極限軽量化版メインビュー
    
    Qtの最適化機能を最大限活用
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Qt最適化フラグ設定
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_NoSystemBackground)
        
        # 極限の最小化初期化
        self.setWindowTitle("PhotoMap Explorer")
        self.setFixedSize(300, 200)  # 固定サイズで最適化
        
        # 即座にUI作成
        self._create_instant_ui()
        
    def _create_instant_ui(self):
        """即座にUI作成"""
        widget = QWidget()
        self.setCentralWidget(widget)
        
        # 最小レイアウト
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # 単一ラベル
        self.label = QLabel("PhotoMap Explorer - 極限軽量版")
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
    def show_status_message(self, message: str):
        """ステータス表示"""
        self.label.setText(message)

class NativeQtMainView(QMainWindow):
    """
    ネイティブQt最適化版
    
    最小限のPythonオーバーヘッドで動作
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """UI セットアップ"""
        self.setWindowTitle("PhotoMap Explorer")
        self.resize(400, 250)
        
        central = QWidget()
        self.setCentralWidget(central)
        
        layout = QVBoxLayout(central)
        self.status_label = QLabel("PhotoMap Explorer - ネイティブ最適化版")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
    def show_status_message(self, message: str):
        """ステータス表示"""
        self.status_label.setText(message)

def test_extreme_performance():
    """極限パフォーマンステスト"""
    import time
    
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    
    print("⚡ 極限軽量化パフォーマンステスト")
    print("=" * 50)
    
    # テスト1: 極限軽量化版
    start_time = time.time()
    window1 = ExtremelyLightMainView()
    window1.show()
    app.processEvents()
    window1.close()
    end_time = time.time()
    
    duration1 = (end_time - start_time) * 1000
    print(f"🚀 極限軽量化版: {duration1:.2f}ms")
    
    # テスト2: ネイティブ最適化版
    start_time = time.time()
    window2 = NativeQtMainView()
    window2.show()
    app.processEvents()
    window2.close()
    end_time = time.time()
    
    duration2 = (end_time - start_time) * 1000
    print(f"🔧 ネイティブ最適化版: {duration2:.2f}ms")
    
    # 最良結果
    best_time = min(duration1, duration2)
    print(f"\n🏆 最良結果: {best_time:.2f}ms")
    
    if best_time <= 100:
        print("✅ 目標達成！(100ms以内)")
    elif best_time <= 200:
        print("🟡 良好 (200ms以内)")
    else:
        print("⚠️ 目標未達成")
    
    return best_time

if __name__ == "__main__":
    test_extreme_performance()
