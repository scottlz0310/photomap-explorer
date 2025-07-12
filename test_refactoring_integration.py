#!/usr/bin/env python3
"""
リファクタリング統合テスト

Phase 2とPhase 3で実施されたリファクタリング結果の統合テストを実行します。
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_basic_imports():
    """基本インポートテスト"""
    print("🧪 基本インポートテスト開始...")
    
    # PyQt5インポートテスト
    try:
        from PyQt5.QtWidgets import QApplication, QMainWindow
        from PyQt5.QtCore import Qt
        print("  ✅ PyQt5インポート成功")
    except ImportError as e:
        print(f"  ❌ PyQt5インポートエラー: {e}")
        return False
    
    # Phase 2: UIコントロールインポートテスト
    try:
        from ui.controls import create_controls
        print("  ✅ リファクタリング後UIコントロールインポート成功")
    except ImportError as e:
        print(f"  ❌ UIコントロールインポートエラー: {e}")
        return False
    
    # Phase 3: テーマシステムインポートテスト
    try:
        from presentation.themes.definitions.light_theme import create_light_theme
        from presentation.themes.definitions.dark_theme import create_dark_theme
        print("  ✅ テーマ定義モジュールインポート成功")
    except ImportError as e:
        print(f"  ❌ テーマ定義インポートエラー: {e}")
        return False
    
    print("✅ 基本インポートテスト完了\n")
    return True


def test_theme_system():
    """テーマシステムテスト"""
    print("🎨 テーマシステムテスト開始...")
    
    try:
        from presentation.themes.definitions.light_theme import create_light_theme
        from presentation.themes.definitions.dark_theme import create_dark_theme
        
        # ライトテーマ作成テスト
        light_theme = create_light_theme()
        assert isinstance(light_theme, dict), "ライトテーマが辞書で返されない"
        assert "name" in light_theme, "テーマに名前がない"
        assert "colors" in light_theme, "テーマにカラー定義がない"
        assert "styles" in light_theme, "テーマにスタイル定義がない"
        print("  ✅ ライトテーマ作成成功")
        
        # ダークテーマ作成テスト
        dark_theme = create_dark_theme()
        assert isinstance(dark_theme, dict), "ダークテーマが辞書で返されない"
        assert "name" in dark_theme, "テーマに名前がない"
        assert "colors" in dark_theme, "テーマにカラー定義がない"
        assert "styles" in dark_theme, "テーマにスタイル定義がない"
        print("  ✅ ダークテーマ作成成功")
        
        # テーマファクトリーテスト
        from presentation.themes.core.theme_factory import ThemeFactory
        factory = ThemeFactory()
        
        # テーマ作成テスト
        test_light = factory.create_theme("light")
        assert test_light is not None, "ファクトリーでライトテーマ作成失敗"
        print("  ✅ テーマファクトリー動作確認")
        
        # 利用可能テーマ一覧
        available_themes = factory.get_available_themes()
        print(f"  📋 利用可能テーマ数: {len(available_themes)}")
        print(f"     テーマ一覧: {', '.join(available_themes)}")
        
    except Exception as e:
        print(f"  ❌ テーマシステムエラー: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("✅ テーマシステムテスト完了\n")
    return True


def test_ui_controls():
    """UIコントロールテスト"""
    print("🎛️ UIコントロールテスト開始...")
    
    try:
        from ui.controls import create_controls
        
        # モックのQWidgetを使ってコントロール作成テスト
        from PyQt5.QtWidgets import QWidget, QApplication
        
        # QApplicationが必要
        if not QApplication.instance():
            app = QApplication([])
        
        parent = QWidget()
        
        # コントロール作成
        controls = create_controls(parent)
        assert controls is not None, "コントロール作成失敗"
        print("  ✅ UIコントロール作成成功")
        
        # 分割されたモジュールの確認
        from ui.controls.address_bar import create_address_bar
        from ui.controls.toolbar import create_toolbar
        
        print("  ✅ 分割されたモジュールインポート成功")
        
    except Exception as e:
        print(f"  ❌ UIコントロールエラー: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("✅ UIコントロールテスト完了\n")
    return True


def test_main_application():
    """メインアプリケーション統合テスト"""
    print("🏠 メインアプリケーション統合テスト開始...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        
        # QApplicationが必要
        if not QApplication.instance():
            app = QApplication([])
        
        # メインウィンドウ作成テスト（実際の表示はしない）
        window = RefactoredFunctionalMainWindow()
        assert window is not None, "メインウィンドウ作成失敗"
        print("  ✅ メインウィンドウ作成成功")
        
        # ウィンドウタイトル確認
        title = window.windowTitle()
        assert "PhotoMap Explorer" in title, "ウィンドウタイトルが不正"
        print(f"  📝 ウィンドウタイトル: {title}")
        
        # 基本メソッド呼び出しテスト
        window.show_status_message("テストメッセージ")
        print("  ✅ ステータスメッセージ表示テスト成功")
        
    except Exception as e:
        print(f"  ❌ メインアプリケーションエラー: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("✅ メインアプリケーション統合テスト完了\n")
    return True


def test_file_structure():
    """ファイル構造テスト"""
    print("📁 リファクタリング後ファイル構造テスト開始...")
    
    # Phase 2: UIコントロール分割確認
    ui_controls_files = [
        "ui/controls/__init__.py",
        "ui/controls/address_bar/__init__.py",
        "ui/controls/address_bar/address_bar_core.py",
        "ui/controls/address_bar/breadcrumb_manager.py", 
        "ui/controls/address_bar/text_input_handler.py",
        "ui/controls/toolbar/__init__.py",
        "ui/controls/toolbar/navigation_controls.py",
        "ui/controls/toolbar/utility_controls.py"
    ]
    
    for file_path in ui_controls_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ 不足: {file_path}")
            return False
    
    # Phase 3: テーマシステム分割確認
    theme_files = [
        "presentation/themes/__init__.py",
        "presentation/themes/core/theme_engine.py",
        "presentation/themes/core/theme_factory.py",
        "presentation/themes/system/system_theme_detector.py",
        "presentation/themes/system/theme_settings.py",
        "presentation/themes/definitions/light_theme.py",
        "presentation/themes/definitions/dark_theme.py"
    ]
    
    for file_path in theme_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ 不足: {file_path}")
            return False
    
    print("✅ ファイル構造テスト完了\n")
    return True


def run_all_tests():
    """全テスト実行"""
    print("🚀 PhotoMap Explorer リファクタリング統合テスト開始")
    print("=" * 60)
    
    tests = [
        ("ファイル構造", test_file_structure),
        ("基本インポート", test_basic_imports),
        ("テーマシステム", test_theme_system),
        ("UIコントロール", test_ui_controls),
        ("メインアプリケーション", test_main_application)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}テスト実行中...")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name}テスト成功")
            else:
                print(f"❌ {test_name}テスト失敗")
        except Exception as e:
            print(f"❌ {test_name}テスト実行エラー: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 テスト結果: {passed}/{total} 成功")
    
    if passed == total:
        print("🎉 全テスト合格！リファクタリング成功!")
        return True
    else:
        print("⚠️  一部テストに失敗があります。詳細を確認してください。")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
