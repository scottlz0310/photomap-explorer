#!/usr/bin/env python3
"""
PhotoMap Explorer デバッグテスト

UI機能が動作しない問題を特定するためのデバッグスクリプト
"""

import sys
import os
import traceback
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """全ての重要なインポートをテスト"""
    print("🔍 インポートテスト開始...")
    
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtCore import Qt
        print("   ✅ PyQt5基本インポート成功")
    except Exception as e:
        print(f"   ❌ PyQt5インポートエラー: {e}")
        return False
    
    try:
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        print("   ✅ メインウィンドウインポート成功")
    except Exception as e:
        print(f"   ❌ メインウィンドウインポートエラー: {e}")
        traceback.print_exc()
        return False
    
    try:
        from ui.controls import create_controls
        print("   ✅ UIコントロールインポート成功")
    except Exception as e:
        print(f"   ❌ UIコントロールインポートエラー: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_window_creation():
    """ウィンドウ作成をテスト"""
    print("\n🏠 ウィンドウ作成テスト開始...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        
        # QApplication作成（既に存在する場合はスキップ）
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        print("   ✅ QApplication作成成功")
        
        # メインウィンドウ作成
        window = RefactoredFunctionalMainWindow()
        print("   ✅ メインウィンドウインスタンス作成成功")
        
        # ウィンドウ属性確認
        print(f"   📊 ウィンドウタイトル: {window.windowTitle()}")
        print(f"   📊 ウィンドウサイズ: {window.size().width()}x{window.size().height()}")
        print(f"   📊 表示可能: {window.isVisible()}")
        
        # 主要コンポーネント存在確認
        components = []
        if hasattr(window, 'folder_btn'):
            components.append("folder_btn")
        if hasattr(window, 'theme_toggle_btn'):
            components.append("theme_toggle_btn")
        if hasattr(window, 'address_bar'):
            components.append("address_bar")
        if hasattr(window, 'main_splitter'):
            components.append("main_splitter")
        
        print(f"   📊 利用可能コンポーネント: {', '.join(components) if components else 'なし'}")
        
        return window, app
        
    except Exception as e:
        print(f"   ❌ ウィンドウ作成エラー: {e}")
        traceback.print_exc()
        return None, None

def test_ui_controls():
    """UIコントロールの作成をテスト"""
    print("\n🎛️ UIコントロール作成テスト開始...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.controls import create_controls
        
        # QApplication作成（必須）
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # ダミーコールバック
        def dummy_callback(*args, **kwargs):
            print(f"   🔔 コールバック呼び出し: args={args}, kwargs={kwargs}")
        
        # コントロール作成
        controls_widget, address_bar, parent_button = create_controls(
            dummy_callback,
            dummy_callback
        )
        
        print("   ✅ UIコントロール作成成功")
        print(f"   📊 controls_widget: {type(controls_widget).__name__}")
        print(f"   📊 address_bar: {type(address_bar).__name__}")
        print(f"   📊 parent_button: {type(parent_button).__name__ if parent_button else 'None'}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ UIコントロール作成エラー: {e}")
        traceback.print_exc()
        return False

def test_theme_system():
    """テーマシステムをテスト"""
    print("\n🎨 テーマシステムテスト開始...")
    
    try:
        from presentation.themes.definitions.light_theme import create_light_theme
        from presentation.themes.definitions.dark_theme import create_dark_theme
        from presentation.themes.core.theme_factory import ThemeFactory
        
        # テーマ作成テスト
        light_theme = create_light_theme()
        dark_theme = create_dark_theme()
        
        print("   ✅ テーマ定義作成成功")
        print(f"   📊 ライトテーマ: {light_theme.get('name', 'Unknown')}")
        print(f"   📊 ダークテーマ: {dark_theme.get('name', 'Unknown')}")
        
        # テーマファクトリーテスト
        factory = ThemeFactory()
        available_themes = factory.get_available_themes()
        
        print(f"   📊 利用可能テーマ数: {len(available_themes)}")
        print(f"   📊 テーマ一覧: {', '.join(available_themes[:5])}...")
        
        return True
        
    except Exception as e:
        print(f"   ❌ テーマシステムエラー: {e}")
        traceback.print_exc()
        return False

def main():
    """メイン実行関数"""
    print("🚨 PhotoMap Explorer デバッグテスト開始")
    print("="*60)
    
    # テスト実行
    tests = [
        ("インポートテスト", test_imports),
        ("UIコントロールテスト", test_ui_controls),
        ("テーマシステムテスト", test_theme_system),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}で予期しないエラー: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    # ウィンドウ作成テスト（最後に実行）
    print("\n" + "="*60)
    window, app = test_window_creation()
    
    # 結果表示
    print("\n" + "="*60)
    print("📊 デバッグテスト結果:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    window_status = "✅ 成功" if window else "❌ 失敗"
    print(f"   ウィンドウ作成テスト: {window_status}")
    if window:
        passed += 1
    
    total_tests = len(results) + 1
    success_rate = (passed / total_tests) * 100
    print(f"\n総合結果: {passed}/{total_tests} テスト成功 ({success_rate:.0f}%)")
    
    if window:
        print("\n💡 次のステップ:")
        print("   1. ウィンドウを表示して手動確認")
        print("   2. コンポーネントの接続状態確認")
        print("   3. イベントハンドラーの動作確認")
        
        return window, app
    else:
        print("\n⚠️ ウィンドウ作成に失敗しています。上記エラーを修正してください。")
        return None, None

if __name__ == "__main__":
    window, app = main()
    
    # ウィンドウが作成された場合、表示テストを実行
    if window and app:
        print("\n🖥️ ウィンドウ表示テスト開始...")
        try:
            window.show()
            print("   ✅ ウィンドウ表示コマンド実行")
            print("   💡 GUIでウィンドウを確認してください")
            
            # 短時間実行してイベント処理
            import time
            for i in range(3):
                app.processEvents()
                time.sleep(0.1)
                
            print("   ✅ イベント処理完了")
            
        except Exception as e:
            print(f"   ❌ ウィンドウ表示エラー: {e}")
            traceback.print_exc()
