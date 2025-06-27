"""
Phase 4 簡単統合テスト

基本的な新旧UI統合をシンプルにテストします。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"📁 プロジェクトルート: {project_root}")
print(f"📂 作業ディレクトリ: {os.getcwd()}")


class SimpleHybridWindow(QMainWindow):
    """
    シンプルなハイブリッドウィンドウ
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - Phase 4 シンプル統合テスト")
        self.setGeometry(100, 100, 1400, 900)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 新UIテスト
        self._test_new_ui()
        
        # レガシーUIテスト
        self._test_legacy_ui()
    
    def _test_new_ui(self):
        """新UIテスト"""
        try:
            print("🧪 新UIテスト開始...")
            
            # まずpresentationディレクトリが存在するか確認
            presentation_path = project_root / "presentation"
            print(f"📁 presentation パス: {presentation_path}")
            print(f"📂 presentation 存在: {presentation_path.exists()}")
            
            if presentation_path.exists():
                print("📋 presentation ディレクトリ内容:")
                for item in presentation_path.iterdir():
                    print(f"  - {item.name}")
            
            # インポートテスト
            sys.path.insert(0, str(presentation_path.parent))  # プロジェクトルートを確実に追加
            
            from presentation.views.main_view import MainView
            
            new_ui = MainView()
            self.tab_widget.addTab(new_ui, "新UI (Clean Architecture)")
            print("✅ 新UI作成成功")
            
        except ImportError as e:
            print(f"❌ 新UIインポートエラー: {e}")
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            error_label = QLabel(f"新UIエラー:\n{str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_layout.addWidget(error_label)
            self.tab_widget.addTab(error_widget, "新UI (エラー)")
        except Exception as e:
            print(f"❌ 新UI作成エラー: {e}")
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            error_label = QLabel(f"新UI作成エラー:\n{str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_layout.addWidget(error_label)
            self.tab_widget.addTab(error_widget, "新UI (作成エラー)")
    
    def _test_legacy_ui(self):
        """レガシーUIテスト"""
        try:
            print("🧪 レガシーUIテスト開始...")
            
            # レガシーUIディレクトリ確認
            window_path = project_root / "window"
            print(f"📁 window パス: {window_path}")
            print(f"📂 window 存在: {window_path.exists()}")
            
            from window.main_window import MainWindow
            
            legacy_window = MainWindow()
            legacy_central = legacy_window.centralWidget()
            
            if legacy_central:
                self.tab_widget.addTab(legacy_central, "レガシーUI")
                print("✅ レガシーUI作成成功")
            else:
                print("⚠️ レガシーUIの中央ウィジェットが取得できませんでした")
                
        except ImportError as e:
            print(f"❌ レガシーUIインポートエラー: {e}")
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            error_label = QLabel(f"レガシーUIエラー:\n{str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            error_layout.addWidget(error_label)
            self.tab_widget.addTab(error_widget, "レガシーUI (エラー)")
        except Exception as e:
            print(f"❌ レガシーUI作成エラー: {e}")


def main():
    """メインエントリーポイント"""
    print("🚀 Phase 4 シンプル統合テスト起動中...")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer - Simple Phase 4 Test")
    
    try:
        # テストウィンドウ作成
        window = SimpleHybridWindow()
        window.show()
        
        print("✅ シンプル統合テスト起動成功")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ テスト起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
