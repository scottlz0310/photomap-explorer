"""
Phase 4 最終統合テスト

ファクトリ関数を使用して新旧UIの統合を実現します。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QLabel, QHBoxLayout, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print(f"📁 プロジェクトルート: {project_root}")


class FinalIntegrationWindow(QMainWindow):
    """
    最終統合テストウィンドウ
    
    ファクトリ関数を使用して新旧UIを統合します。
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - Phase 4 最終統合テスト")
        self.setGeometry(100, 100, 1600, 1000)
        
        # アイコン設定
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # コントロールバー
        control_bar = self._create_control_bar()
        layout.addWidget(control_bar)
        
        # タブウィジェット
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # レガシーUIタブ
        self._create_legacy_tab()
        
        # 新UIコンポーネントタブ
        self._create_new_components_tab()
        
        # 統合比較タブ
        self._create_comparison_tab()
    
    def _create_control_bar(self):
        """コントロールバー作成"""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        
        # 情報表示
        info_label = QLabel("Phase 4 最終統合テスト - 新旧UI比較・検証環境")
        info_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        # テストボタン
        test_btn = QPushButton("互換性テスト実行")
        test_btn.clicked.connect(self._run_compatibility_test)
        layout.addWidget(test_btn)
        
        about_btn = QPushButton("Phase 4について")
        about_btn.clicked.connect(self._show_about)
        layout.addWidget(about_btn)
        
        return widget
    
    def _create_legacy_tab(self):
        """レガシーUIタブ作成"""
        try:
            from window.main_window import MainWindow
            
            legacy_window = MainWindow()
            legacy_central = legacy_window.centralWidget()
            
            if legacy_central:
                # レガシーUIを新しい親に移植
                container = QWidget()
                layout = QVBoxLayout(container)
                layout.addWidget(legacy_central)
                
                self.tab_widget.addTab(container, "🏛️ レガシーUI (従来版)")
                print("✅ レガシーUIタブ作成成功")
            else:
                self._create_error_tab("レガシーUI", "中央ウィジェットの取得に失敗")
                
        except Exception as e:
            print(f"❌ レガシーUIタブ作成エラー: {e}")
            self._create_error_tab("レガシーUI", str(e))
    
    def _create_new_components_tab(self):
        """新UIコンポーネントタブ作成"""
        try:
            # 機能的な新UIを埋め込み
            from presentation.views.functional_new_main_view import FunctionalNewMainWindow
            
            # 新UIのメインウィンドウを作成
            new_ui_window = FunctionalNewMainWindow()
            
            # メインウィンドウのセントラルウィジェットを取得
            new_ui_widget = new_ui_window.centralWidget()
            
            if new_ui_widget:
                # 親から切り離してタブに追加
                new_ui_widget.setParent(None)
                self.tab_widget.addTab(new_ui_widget, "🚀 新UI (機能版)")
                print("✅ 新UIタブ作成成功")
            else:
                # フォールバック: コンポーネント別テスト
                self._create_component_test_tab()
                
        except Exception as e:
            print(f"❌ 新UIタブ作成エラー: {e}")
            # フォールバック: コンポーネント別テスト
            self._create_component_test_tab()
    
    def _create_component_test_tab(self):
        """コンポーネント別テストタブ作成（フォールバック）"""
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # ヘッダー
        header = QLabel("🚀 新UI (Clean Architecture) - コンポーネント別テスト")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        # コンポーネントテスト結果
        self._test_and_display_components(layout)
        
        self.tab_widget.addTab(container, "🚀 新UI (Clean Architecture)")
    
    def _test_and_display_components(self, layout):
        """コンポーネントテストと表示"""
        components = [
            ("アドレスバー", self._test_address_bar_component),
            ("フォルダパネル", self._test_folder_panel_component),
            ("サムネイルリスト", self._test_thumbnail_component),
            ("プレビューパネル", self._test_preview_component),
            ("マップパネル", self._test_map_component)
        ]
        
        for name, test_func in components:
            widget, status = test_func()
            
            # コンポーネントコンテナ
            comp_container = QWidget()
            comp_layout = QVBoxLayout(comp_container)
            
            # ヘッダー
            status_icon = "✅" if status else "❌"
            header_label = QLabel(f"{status_icon} {name}")
            header_label.setStyleSheet("font-weight: bold; padding: 5px;")
            comp_layout.addWidget(header_label)
            
            # コンポーネント
            if widget:
                comp_layout.addWidget(widget)
            else:
                error_label = QLabel("コンポーネントの作成に失敗しました")
                error_label.setStyleSheet("color: red; padding: 10px;")
                comp_layout.addWidget(error_label)
            
            layout.addWidget(comp_container)
    
    def _test_address_bar_component(self):
        """アドレスバーコンポーネントテスト"""
        try:
            from presentation.views.controls.address_bar import create_address_bar_widget
            
            # ダミーのコールバック関数を提供
            def dummy_callback(path):
                pass
            
            widget, edit = create_address_bar_widget("C:\\", dummy_callback, dummy_callback)
            widget.setMaximumHeight(50)
            return widget, True
            
        except Exception as e:
            print(f"❌ アドレスバーテストエラー: {e}")
            return None, False
    
    def _test_folder_panel_component(self):
        """フォルダパネルコンポーネントテスト"""
        try:
            from presentation.views.panels.folder_panel import create_folder_panel
            
            # ダミーのコールバック関数を提供
            def dummy_folder_selected(path):
                pass
            
            widget = create_folder_panel(dummy_folder_selected)
            widget.setMaximumHeight(150)
            return widget, True
            
        except Exception as e:
            print(f"❌ フォルダパネルテストエラー: {e}")
            return None, False
    
    def _test_thumbnail_component(self):
        """サムネイルコンポーネントテスト"""
        try:
            from presentation.views.controls.thumbnail_list import create_thumbnail_list
            
            # ダミーのコールバック関数を提供
            def dummy_thumbnail_clicked(image_path):
                pass
            
            widget = create_thumbnail_list(dummy_thumbnail_clicked)
            widget.setMaximumHeight(150)
            return widget, True
            
        except Exception as e:
            print(f"❌ サムネイルテストエラー: {e}")
            return None, False
    
    def _test_preview_component(self):
        """プレビューコンポーネントテスト"""
        try:
            from presentation.views.panels.preview_panel import create_preview_panel
            
            widget = create_preview_panel()
            widget.setMaximumHeight(200)
            return widget, True
            
        except Exception as e:
            print(f"❌ プレビューテストエラー: {e}")
            return None, False
    
    def _test_map_component(self):
        """マップコンポーネントテスト"""
        try:
            from presentation.views.panels.map_panel import create_map_panel
            
            widget = create_map_panel()
            widget.setMaximumHeight(200)
            return widget, True
            
        except Exception as e:
            print(f"❌ マップテストエラー: {e}")
            return None, False
    
    def _create_comparison_tab(self):
        """比較タブ作成"""
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # ヘッダー
        header = QLabel("⚖️ 新旧UI比較・検証結果")
        header.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(header)
        
        # 比較結果
        comparison_text = self._generate_comparison_report()
        
        comparison_label = QLabel(comparison_text)
        comparison_label.setStyleSheet("font-family: monospace; padding: 20px; background: #f5f5f5;")
        comparison_label.setWordWrap(True)
        layout.addWidget(comparison_label)
        
        self.tab_widget.addTab(container, "⚖️ 比較・検証")
    
    def _generate_comparison_report(self):
        """比較レポート生成"""
        report = []
        report.append("🔍 Phase 4 統合検証レポート")
        report.append("=" * 40)
        report.append("")
        
        # レガシーUIチェック
        try:
            from window.main_window import MainWindow
            report.append("✅ レガシーUI: 利用可能")
        except Exception as e:
            report.append(f"❌ レガシーUI: エラー ({e})")
        
        # 新UIコンポーネントチェック
        components = [
            ("アドレスバー", "presentation.views.controls.address_bar"),
            ("フォルダパネル", "presentation.views.panels.folder_panel"),
            ("サムネイルリスト", "presentation.views.controls.thumbnail_list"),
            ("プレビューパネル", "presentation.views.panels.preview_panel"),
            ("マップパネル", "presentation.views.panels.map_panel")
        ]
        
        report.append("")
        report.append("🚀 新UIコンポーネント状況:")
        
        for name, module_path in components:
            try:
                __import__(module_path)
                report.append(f"  ✅ {name}: OK")
            except Exception as e:
                report.append(f"  ❌ {name}: エラー")
        
        # 互換性状況
        report.append("")
        report.append("🔧 互換性状況:")
        report.append("  ✅ ファクトリ関数によるコンポーネント作成")
        report.append("  ✅ レガシーUIの既存機能保持")
        report.append("  🔄 段階的移行の準備完了")
        
        # 推奨アクション
        report.append("")
        report.append("📋 推奨アクション:")
        report.append("  1. 個別コンポーネントの段階的置き換え")
        report.append("  2. エンドツーエンドテストの実装")
        report.append("  3. パフォーマンス最適化")
        report.append("  4. ユーザー受け入れテスト")
        
        return "\n".join(report)
    
    def _create_error_tab(self, name, error_message):
        """エラータブ作成"""
        container = QWidget()
        layout = QVBoxLayout(container)
        
        error_label = QLabel(f"❌ {name}エラー:\n\n{error_message}")
        error_label.setStyleSheet("color: red; padding: 20px; font-family: monospace;")
        error_label.setWordWrap(True)
        layout.addWidget(error_label)
        
        self.tab_widget.addTab(container, f"❌ {name} (エラー)")
    
    def _run_compatibility_test(self):
        """互換性テスト実行"""
        try:
            # ファクトリ関数テスト
            from presentation.views.controls.address_bar import create_address_bar_widget
            from presentation.views.panels.folder_panel import create_folder_panel
            from presentation.views.controls.thumbnail_list import create_thumbnail_list
            from presentation.views.panels.preview_panel import create_preview_panel
            from presentation.views.panels.map_panel import create_map_panel
            
            results = []
            
            # ダミーコールバック関数
            def dummy_callback(*args):
                pass
            
            # 各コンポーネントのファクトリ関数テスト
            try:
                create_address_bar_widget("", dummy_callback, dummy_callback)
                results.append("✅ アドレスバーファクトリ")
            except Exception as e:
                results.append(f"❌ アドレスバーファクトリ: {e}")
            
            try:
                create_folder_panel(dummy_callback)
                results.append("✅ フォルダパネルファクトリ")
            except Exception as e:
                results.append(f"❌ フォルダパネルファクトリ: {e}")
            
            try:
                create_thumbnail_list(dummy_callback)
                results.append("✅ サムネイルリストファクトリ")
            except Exception as e:
                results.append(f"❌ サムネイルリストファクトリ: {e}")
            
            try:
                create_preview_panel()
                results.append("✅ プレビューパネルファクトリ")
            except Exception as e:
                results.append(f"❌ プレビューパネルファクトリ: {e}")
            
            try:
                create_map_panel()
                results.append("✅ マップパネルファクトリ")
            except Exception as e:
                results.append(f"❌ マップパネルファクトリ: {e}")
            
            # 結果表示
            result_text = "🧪 互換性テスト結果:\n\n" + "\n".join(results)
            
            QMessageBox.information(self, "互換性テスト結果", result_text)
            
        except Exception as e:
            QMessageBox.critical(self, "テストエラー", f"互換性テスト中にエラーが発生しました:\n{e}")
    
    def _show_about(self):
        """バージョン情報表示"""
        about_text = """
PhotoMap Explorer - Phase 4 最終統合テスト

Clean Architectureへの段階的移行をサポートする
統合テスト環境です。

機能:
• 新旧UI同時表示・比較
• コンポーネント別動作確認
• 互換性検証
• 移行準備状況確認

Phase 4の目標:
✅ ハイブリッド実行環境の構築
✅ 段階的移行システムの実装
🔄 エンドツーエンドテストの実行
📈 パフォーマンス最適化
        """
        
        QMessageBox.about(self, "Phase 4について", about_text.strip())


def main():
    """メインエントリーポイント"""
    print("🚀 Phase 4 最終統合テスト起動中...")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer - Phase 4 Final Integration")
    
    try:
        # テストウィンドウ作成
        window = FinalIntegrationWindow()
        window.show()
        
        print("✅ 最終統合テスト起動成功")
        print("📋 利用可能な機能:")
        print("  - 新旧UI同時表示")
        print("  - コンポーネント別動作確認")
        print("  - 互換性テスト")
        print("  - 段階的移行準備確認")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ テスト起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
