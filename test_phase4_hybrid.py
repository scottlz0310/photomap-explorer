"""
Phase 4 統合テスト - ハイブリッド実行環境

新しいプレゼンテーション層と既存UIの比較テストを行う環境です。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QDir

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# アプリケーション層の初期化
try:
    from app.application import initialize_application
    app = initialize_application()
    print("✅ アプリケーション層初期化成功")
except Exception as e:
    print(f"⚠️  アプリケーション層初期化警告: {e}")


class HybridTestWindow(QMainWindow):
    """
    新旧UIの比較テスト用ウィンドウ
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - Phase 4 統合テスト")
        self.setGeometry(100, 100, 1600, 1000)
        
        # アイコン設定
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_path))
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # コントロールパネル
        self._setup_control_panel(layout)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # タブを追加
        self._add_legacy_tab()
        self._add_new_tab()
        self._add_comparison_tab()
        
        # ステータスバー
        self.statusBar().showMessage("Phase 4 統合テスト環境 - タブを切り替えて比較してください")
    
    def _setup_control_panel(self, parent_layout):
        """コントロールパネルのセットアップ"""
        control_widget = QWidget()
        control_layout = QHBoxLayout(control_widget)
        
        # 説明ラベル
        info_label = QLabel("Phase 4 統合テスト: 新旧UIの比較・検証環境")
        info_label.setStyleSheet("font-weight: bold; color: #2196f3; padding: 10px;")
        control_layout.addWidget(info_label)
        
        control_layout.addStretch()
        
        # テストフォルダ設定ボタン
        self.set_test_folder_btn = QPushButton("テストフォルダ設定")
        self.set_test_folder_btn.clicked.connect(self._set_test_folder)
        control_layout.addWidget(self.set_test_folder_btn)
        
        # 機能テストボタン
        self.run_test_btn = QPushButton("機能テスト実行")
        self.run_test_btn.clicked.connect(self._run_functionality_test)
        control_layout.addWidget(self.run_test_btn)
        
        parent_layout.addWidget(control_widget)
    
    def _add_legacy_tab(self):
        """レガシーUIタブを追加"""
        try:
            from window.main_window import MainWindow
            
            legacy_window = MainWindow()
            # メインウィンドウとしてではなく、ウィジェットとして埋め込み
            legacy_widget = legacy_window.centralWidget()
            if legacy_widget:
                self.tab_widget.addTab(legacy_widget, "🏠 レガシーUI (既存)")
            else:
                # フォールバック: 簡単な説明ウィジェット
                fallback_widget = QWidget()
                fallback_layout = QVBoxLayout(fallback_widget)
                fallback_layout.addWidget(QLabel("レガシーUIの読み込みに失敗しました"))
                self.tab_widget.addTab(fallback_widget, "🏠 レガシーUI (エラー)")
                
        except Exception as e:
            print(f"レガシーUI読み込みエラー: {e}")
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            error_layout.addWidget(QLabel(f"レガシーUI読み込みエラー:\n{str(e)}"))
            self.tab_widget.addTab(error_widget, "🏠 レガシーUI (エラー)")
    
    def _add_new_tab(self):
        """新しいUIタブを追加"""
        try:
            from presentation.views.main_view import MainView
            
            new_view = MainView()
            # ウィンドウとしてではなく、ウィジェットとして使用
            new_widget = new_view.centralWidget()
            if new_widget:
                self.tab_widget.addTab(new_widget, "🆕 新UI (Clean Architecture)")
            else:
                # MainViewを直接ウィジェットとして使用
                self.tab_widget.addTab(new_view, "🆕 新UI (Clean Architecture)")
                
        except Exception as e:
            print(f"新UI読み込みエラー: {e}")
            error_widget = QWidget()
            error_layout = QVBoxLayout(error_widget)
            error_layout.addWidget(QLabel(f"新UI読み込みエラー:\n{str(e)}"))
            self.tab_widget.addTab(error_widget, "🆕 新UI (エラー)")
    
    def _add_comparison_tab(self):
        """比較タブを追加"""
        comparison_widget = QWidget()
        layout = QVBoxLayout(comparison_widget)
        
        # 比較情報
        info_text = """
# Phase 4 統合テスト - UI比較

## 📊 比較項目

### 1. 基本機能
- ✅ フォルダ選択・表示
- ✅ 画像サムネイル表示
- ✅ 画像プレビュー
- ✅ 地図表示（GPS情報付き画像）
- ✅ ナビゲーション（アドレスバー、親フォルダボタン）

### 2. アーキテクチャ比較
#### レガシーUI
- 直接的なUI結合
- logic/ディレクトリの直接利用
- 単一ファイルでの実装

#### 新UI (Clean Architecture)
- MVVM/MVCパターン
- レイヤー分離（presentation/domain/infrastructure）
- モジュラー設計

### 3. テスト方法
1. 「テストフォルダ設定」で同じフォルダを設定
2. 両方のタブで同じ操作を実行
3. 動作・パフォーマンス・安定性を比較

### 4. 期待される結果
- ✅ 同等の機能性
- ✅ より良い応答性
- ✅ エラーハンドリングの改善
- ✅ コードの保守性向上
        """
        
        info_label = QLabel(info_text)
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignTop)
        info_label.setStyleSheet("padding: 20px; font-family: monospace; background-color: #f5f5f5;")
        layout.addWidget(info_label)
        
        self.tab_widget.addTab(comparison_widget, "📊 比較・テスト情報")
    
    def _set_test_folder(self):
        """テストフォルダを設定"""
        from PyQt5.QtWidgets import QFileDialog
        
        folder_path = QFileDialog.getExistingDirectory(
            self, 
            "テスト用フォルダを選択", 
            QDir.homePath()
        )
        
        if folder_path:
            self.statusBar().showMessage(f"テストフォルダ設定: {folder_path}")
            print(f"📁 テストフォルダ設定: {folder_path}")
            
            # TODO: 両方のUIにフォルダパスを設定
            # この機能は次のステップで実装
    
    def _run_functionality_test(self):
        """機能テストを実行"""
        self.statusBar().showMessage("機能テスト実行中...")
        print("🧪 機能テスト実行開始")
        
        # TODO: 自動化された機能テストの実装
        # この機能は次のステップで実装
        
        self.statusBar().showMessage("機能テスト完了 - 詳細はコンソールを確認してください")


def main():
    """メイン関数"""
    print("🚀 PhotoMap Explorer Phase 4 統合テスト開始")
    print("=" * 60)
    
    # Qt アプリケーション作成
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # ハイブリッドテストウィンドウを作成
        hybrid_window = HybridTestWindow()
        hybrid_window.show()
        
        print("✅ ハイブリッドテスト環境起動成功")
        print("📋 使用方法:")
        print("  1. タブを切り替えて新旧UIを比較")
        print("  2. 同じ操作を両方で実行して動作確認")
        print("  3. パフォーマンス・安定性を評価")
        
        # アプリケーション実行
        return app.exec_()
        
    except Exception as e:
        print(f"❌ ハイブリッドテスト環境起動エラー: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
