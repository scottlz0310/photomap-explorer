"""
PhotoMap Explorer - ハイブリッドメインアプリケーション（Phase 4）

新旧UIの統合と段階的移行を行うメインアプリケーションです。
設定により新旧UIを切り替えて、比較・検証を行えます。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtCore import Qt, QCommandLineParser, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMenuBar, QMenu, QAction
from PyQt5.QtGui import QIcon

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# アプリケーション層の初期化（オプション）
try:
    from app.application import initialize_application
    app_context = initialize_application()
    print("✅ アプリケーション層初期化成功")
except Exception as e:
    print(f"⚠️  アプリケーション層初期化警告: {e}")
    print("   レガシーモードで動作します")
    app_context = None


class HybridMainWindow(QMainWindow):
    """
    ハイブリッドメインウィンドウ
    
    新旧UIを統合し、段階的移行をサポートします。
    """
    
    def __init__(self, mode="new"):
        super().__init__()
        self.mode = mode  # "new", "legacy", "hybrid"
        self.setWindowTitle(f"PhotoMap Explorer - Phase 4 統合版 ({mode.upper()})")
        self.setGeometry(100, 100, 1600, 1000)
        
        # アイコン設定
        self._setup_icon()
        
        # モードに応じてUIを構築
        if mode == "hybrid":
            self._setup_hybrid_ui()
        elif mode == "new":
            self._setup_new_ui()
        elif mode == "legacy":
            self._setup_legacy_ui()
        
        self._setup_menu()
    
    def _setup_icon(self):
        """アプリケーションアイコンの設定"""
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_hybrid_ui(self):
        """ハイブリッドUI（新旧両方をタブで表示）"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # 新UIタブ
        try:
            from presentation.views.main_view import MainView
            self.new_ui = MainView()
            self.tab_widget.addTab(self.new_ui, "新UI (Clean Architecture)")
            print("✅ 新UI追加成功")
        except Exception as e:
            print(f"❌ 新UI追加エラー: {e}")
        
        # レガシーUIタブ
        try:
            from window.main_window import MainWindow
            self.legacy_ui = MainWindow()
            # MainWindowの中央ウィジェットを取得してタブに追加
            legacy_central = self.legacy_ui.centralWidget()
            if legacy_central:
                self.tab_widget.addTab(legacy_central, "レガシーUI (従来版)")
                print("✅ レガシーUI追加成功")
        except Exception as e:
            print(f"❌ レガシーUI追加エラー: {e}")
    
    def _setup_new_ui(self):
        """新UIのみ"""
        try:
            from presentation.views.main_view import MainView
            self.main_view = MainView()
            self.setCentralWidget(self.main_view)
            print("✅ 新UIセットアップ成功")
        except Exception as e:
            print(f"❌ 新UIセットアップエラー: {e}")
    
    def _setup_legacy_ui(self):
        """レガシーUIのみ"""
        try:
            from window.main_window import MainWindow
            self.legacy_window = MainWindow()
            # レガシーウィンドウの内容をこのウィンドウに移植
            legacy_central = self.legacy_window.centralWidget()
            if legacy_central:
                self.setCentralWidget(legacy_central)
                print("✅ レガシーUIセットアップ成功")
        except Exception as e:
            print(f"❌ レガシーUIセットアップエラー: {e}")
    
    def _setup_menu(self):
        """メニューバーの設定"""
        menubar = self.menuBar()
        
        # ファイルメニュー
        file_menu = menubar.addMenu('ファイル(&F)')
        
        exit_action = QAction('終了(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 表示メニュー
        view_menu = menubar.addMenu('表示(&V)')
        
        if self.mode == "hybrid":
            switch_new_action = QAction('新UIタブに切り替え', self)
            switch_new_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(0))
            view_menu.addAction(switch_new_action)
            
            switch_legacy_action = QAction('レガシーUIタブに切り替え', self)
            switch_legacy_action.triggered.connect(lambda: self.tab_widget.setCurrentIndex(1))
            view_menu.addAction(switch_legacy_action)
        
        # ヘルプメニュー
        help_menu = menubar.addMenu('ヘルプ(&H)')
        
        about_action = QAction('Phase 4について', self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _show_about(self):
        """バージョン情報表示"""
        from PyQt5.QtWidgets import QMessageBox
        QMessageBox.about(self, "Phase 4統合版について", 
                         "PhotoMap Explorer - Phase 4 統合版\n\n"
                         "Clean Architectureへの段階的移行をサポートする\n"
                         "ハイブリッドアプリケーションです。\n\n"
                         f"実行モード: {self.mode.upper()}")


def parse_command_line():
    """コマンドライン引数の解析"""
    parser = QCommandLineParser()
    parser.addHelpOption()
    parser.addVersionOption()
    
    # UIモードオプション
    from PyQt5.QtCore import QCommandLineOption
    mode_option = QCommandLineOption(["mode"], "UI mode (new/legacy/hybrid)", "mode", "new")
    parser.addOption(mode_option)
    
    parser.process(QCoreApplication.arguments())
    
    mode = parser.value("mode").lower()
    if mode not in ["new", "legacy", "hybrid"]:
        print(f"⚠️  無効なモード '{mode}'。'new' を使用します。")
        mode = "new"
    
    return mode


def main():
    """メインエントリーポイント"""
    print("🚀 PhotoMap Explorer Phase 4 統合版起動中...")
    print(f"📁 作業ディレクトリ: {os.getcwd()}")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer")
    app.setApplicationVersion("Phase 4")
    app.setOrganizationName("PhotoMap Explorer Project")
    
    # コマンドライン引数解析
    mode = parse_command_line()
    print(f"🎮 実行モード: {mode.upper()}")
    
    try:
        # メインウィンドウ作成
        window = HybridMainWindow(mode)
        window.show()
        
        print("✅ アプリケーション起動成功")
        print("📋 操作可能な機能:")
        if mode == "hybrid":
            print("  - 新旧UIのタブ切り替え")
            print("  - 機能比較とテスト")
        elif mode == "new":
            print("  - 新しいClean ArchitectureUI")
        elif mode == "legacy":
            print("  - 従来のレガシーUI")
        print("  - メニューからの各種操作")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ アプリケーション起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
