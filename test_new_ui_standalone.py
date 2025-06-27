"""
Phase 4 統合のための新UIテスト（スタンドアロン版）

相対インポートの問題を解決し、新UIを単独でテストします。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"📁 プロジェクトルート: {project_root}")
print(f"📂 作業ディレクトリ: {os.getcwd()}")


class NewUITestWindow(QMainWindow):
    """
    新UIテストウィンドウ
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - 新UI単独テスト")
        self.setGeometry(100, 100, 1400, 900)
        
        self._test_components()
    
    def _test_components(self):
        """コンポーネントテスト"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 結果表示用のラベル
        self.result_label = QLabel()
        layout.addWidget(self.result_label)
        
        results = []
        
        # 各コンポーネントを個別にテスト
        results.append(self._test_address_bar())
        results.append(self._test_folder_panel())
        results.append(self._test_thumbnail_list())
        results.append(self._test_preview_panel())
        results.append(self._test_map_panel())
        results.append(self._test_viewmodels())
        results.append(self._test_controllers())
        
        # 結果をまとめて表示
        result_text = "🧪 新UIコンポーネントテスト結果:\n\n" + "\n".join(results)
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet("font-family: monospace; padding: 20px;")
    
    def _test_address_bar(self):
        """アドレスバーテスト"""
        try:
            from presentation.views.controls.address_bar import NavigationControls, create_address_bar_widget
            
            # ファクトリ関数テスト
            widget, edit = create_address_bar_widget("C:\\", None, None)
            
            return "✅ アドレスバー: OK"
        except Exception as e:
            return f"❌ アドレスバー: {e}"
    
    def _test_folder_panel(self):
        """フォルダパネルテスト"""
        try:
            from presentation.views.panels.folder_panel import FolderPanel, create_folder_panel
            
            # ファクトリ関数テスト
            panel = create_folder_panel()
            
            return "✅ フォルダパネル: OK"
        except Exception as e:
            return f"❌ フォルダパネル: {e}"
    
    def _test_thumbnail_list(self):
        """サムネイルリストテスト"""
        try:
            from presentation.views.controls.thumbnail_list import ThumbnailPanel, create_thumbnail_list
            
            # ファクトリ関数テスト
            panel = create_thumbnail_list(None, None)
            
            return "✅ サムネイルリスト: OK"
        except Exception as e:
            return f"❌ サムネイルリスト: {e}"
    
    def _test_preview_panel(self):
        """プレビューパネルテスト"""
        try:
            from presentation.views.panels.preview_panel import PreviewPanel, create_preview_panel
            
            # ファクトリ関数テスト
            panel = create_preview_panel()
            
            return "✅ プレビューパネル: OK"
        except Exception as e:
            return f"❌ プレビューパネル: {e}"
    
    def _test_map_panel(self):
        """マップパネルテスト"""
        try:
            from presentation.views.panels.map_panel import MapPanel, create_map_panel
            
            # ファクトリ関数テスト
            panel = create_map_panel()
            
            return "✅ マップパネル: OK"
        except Exception as e:
            return f"❌ マップパネル: {e}"
    
    def _test_viewmodels(self):
        """ビューモデルテスト"""
        try:
            from presentation.viewmodels.base_viewmodel import BaseViewModel
            from presentation.viewmodels.simple_main_viewmodel import SimpleMainViewModel
            
            # SimpleMainViewModelインスタンス作成テスト
            viewmodel = SimpleMainViewModel()
            
            return "✅ ビューモデル: OK"
        except Exception as e:
            return f"❌ ビューモデル: {e}"
    
    def _test_controllers(self):
        """コントローラーテスト"""
        try:
            from presentation.controllers.main_controller import MainController
            
            return "✅ コントローラー: OK"
        except Exception as e:
            return f"❌ コントローラー: {e}"


def main():
    """メインエントリーポイント"""
    print("🚀 新UI単独テスト起動中...")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer - New UI Test")
    
    try:
        # テストウィンドウ作成
        window = NewUITestWindow()
        window.show()
        
        print("✅ 新UI単独テスト起動成功")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ テスト起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
