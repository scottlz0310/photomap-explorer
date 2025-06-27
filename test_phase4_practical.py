"""
Phase 4 統合テスト - 実用的な新旧UI比較

WebEngine問題を解決し、実際に動作する統合テストを提供します。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def test_new_ui_standalone():
    """新しいUIの単体テスト"""
    print("\n=== 新しいUI単体テスト ===")
    
    try:
        # Qt アプリケーション作成
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from presentation.views.main_view import MainView
        
        # 新しいMainViewを作成
        main_view = MainView()
        main_view.show()
        
        print("✅ 新しいMainView起動成功")
        print("📋 テスト項目:")
        print("  - ウィンドウ表示")
        print("  - 基本レイアウト")
        print("  - コンポーネント初期化")
        
        # 基本的な操作テスト
        main_view.show_status_message("Phase 4 統合テスト - 新UI動作確認")
        main_view.update_folder_path("C:\\")
        
        print("✅ 基本操作テスト完了")
        
        return app, main_view
        
    except Exception as e:
        print(f"❌ 新UI単体テストエラー: {e}")
        return None, None


def test_legacy_ui_standalone():
    """レガシーUIの単体テスト"""
    print("\n=== レガシーUI単体テスト ===")
    
    try:
        # Qt アプリケーション作成
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from window.main_window import MainWindow
        
        # レガシーMainWindowを作成
        main_window = MainWindow()
        main_window.show()
        
        print("✅ レガシーMainWindow起動成功")
        print("📋 テスト項目:")
        print("  - ウィンドウ表示")
        print("  - 既存機能")
        print("  - UI応答性")
        
        return app, main_window
        
    except Exception as e:
        print(f"❌ レガシーUI単体テストエラー: {e}")
        return None, None


def test_component_compatibility():
    """コンポーネント互換性テスト"""
    print("\n=== コンポーネント互換性テスト ===")
    
    try:
        # Qt アプリケーション作成
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # レガシー関数のテスト
        from presentation.views.controls.address_bar import create_controls, create_address_bar_widget
        from presentation.views.panels.folder_panel import create_folder_panel
        from presentation.views.controls.thumbnail_list import create_thumbnail_list
        from presentation.views.panels.map_panel import create_map_view, create_map_panel
        from presentation.views.panels.preview_panel import create_image_preview, create_preview_panel
        
        print("✅ レガシー関数インポート成功")
        
        # 基本的なコンポーネント作成テスト
        def dummy_callback():
            pass
        
        # コントロール
        controls_widget, address_bar, parent_btn = create_controls(dummy_callback, dummy_callback)
        address_widget, address_edit = create_address_bar_widget("C:\\", dummy_callback, dummy_callback)
        print("✅ アドレスバーコントロール作成成功")
        
        # パネル
        folder_panel = create_folder_panel(dummy_callback)
        thumbnail_list = create_thumbnail_list(dummy_callback)
        map_view = create_map_view()
        map_panel = create_map_panel()
        image_preview = create_image_preview()
        preview_panel = create_preview_panel()
        print("✅ 各種パネル作成成功")
        
        print("🎉 すべてのコンポーネント互換性テスト成功")
        return True
        
    except Exception as e:
        print(f"❌ コンポーネント互換性テストエラー: {e}")
        return False


def run_interactive_test():
    """対話式テスト"""
    print("\n=== 対話式テスト ===")
    
    while True:
        print("\n📋 テストオプション:")
        print("1. 新しいUI単体テスト")
        print("2. レガシーUI単体テスト") 
        print("3. コンポーネント互換性テスト")
        print("4. 新UIと既存UIの同時表示テスト")
        print("5. 終了")
        
        choice = input("選択してください (1-5): ").strip()
        
        if choice == "1":
            app, view = test_new_ui_standalone()
            if app and view:
                input("Enterを押すとウィンドウを閉じます...")
                view.close()
        
        elif choice == "2":
            app, window = test_legacy_ui_standalone()
            if app and window:
                input("Enterを押すとウィンドウを閉じます...")
                window.close()
        
        elif choice == "3":
            test_component_compatibility()
        
        elif choice == "4":
            print("新UIと既存UIの同時表示テストを開始...")
            app, new_view = test_new_ui_standalone()
            app2, legacy_window = test_legacy_ui_standalone()
            
            if new_view and legacy_window:
                # ウィンドウを並べて表示
                new_view.move(100, 100)
                legacy_window.move(800, 100)
                print("✅ 両方のUIを並べて表示しました")
                input("Enterを押すと両方のウィンドウを閉じます...")
                new_view.close()
                legacy_window.close()
        
        elif choice == "5":
            print("テストを終了します")
            break
        
        else:
            print("無効な選択です。1-5を選んでください。")


def main():
    """メイン関数"""
    print("🚀 PhotoMap Explorer Phase 4 実用統合テスト")
    print("=" * 60)
    print("📝 このテストでは新旧UIの実際の動作を比較・検証します")
    
    # 基本的な互換性チェック
    if test_component_compatibility():
        print("\n✅ 基本互換性確認完了")
        run_interactive_test()
    else:
        print("\n❌ 基本互換性に問題があります。修正が必要です。")
    
    print("\n🎯 Phase 4統合テスト完了")


if __name__ == "__main__":
    main()
