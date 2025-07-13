#!/usr/bin/env python3
"""
PhotoMap Explorer 手動テストヘルパー

アプリケーションが正常に動作しているかを確認するための
手動テスト支援スクリプト
"""

import sys
import os
import time
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_application_responsiveness():
    """アプリケーションの応答性をテスト"""
    print("🔍 アプリケーション応答性テスト開始...")
    
    try:
        # プロセス確認
        import subprocess
        result = subprocess.run(['pgrep', '-f', 'python main.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and result.stdout.strip():
            pid = result.stdout.strip()
            print(f"   ✅ アプリケーションプロセス稼働中 (PID: {pid})")
            
            # プロセス詳細情報
            ps_result = subprocess.run(['ps', '-p', pid, '-o', 'pid,ppid,cmd,%cpu,%mem'], 
                                     capture_output=True, text=True)
            if ps_result.returncode == 0:
                print("   📊 プロセス詳細:")
                for line in ps_result.stdout.strip().split('\n'):
                    print(f"      {line}")
            
            return True
        else:
            print("   ❌ アプリケーションプロセスが見つかりません")
            return False
            
    except Exception as e:
        print(f"   ❌ プロセス確認エラー: {e}")
        return False

def test_ui_components():
    """UI コンポーネントのインポートテスト"""
    print("\n🎛️ UIコンポーネントテスト開始...")
    
    try:
        # メインウィンドウクラステスト
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        print("   ✅ メインウィンドウクラスインポート成功")
        
        # UIコントロールテスト
        from ui.controls import create_controls
        print("   ✅ UIコントロールインポート成功")
        
        # テーマシステムテスト
        from presentation.themes.definitions.light_theme import create_light_theme
        from presentation.themes.definitions.dark_theme import create_dark_theme
        print("   ✅ テーマシステムインポート成功")
        
        return True
        
    except Exception as e:
        print(f"   ❌ UIコンポーネントエラー: {e}")
        return False

def test_file_structure():
    """ファイル構造の整合性をテスト"""
    print("\n📁 ファイル構造テスト開始...")
    
    critical_files = [
        "main.py",
        "presentation/views/functional_main_window/refactored_main_window.py",
        "presentation/views/functional_main_window/main_window_core.py",
        "ui/controls/__init__.py",
        "presentation/themes/core/theme_engine.py",
        "settings/theme_settings.json"
    ]
    
    all_present = True
    for file_path in critical_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            all_present = False
    
    return all_present

def display_manual_test_checklist():
    """手動テストチェックリストを表示"""
    print("\n" + "="*60)
    print("📋 PhotoMap Explorer 手動テストチェックリスト")
    print("="*60)
    
    checklist = [
        ("基本動作", [
            "ウィンドウが正常に表示される",
            "タイトルバーに適切なタイトルが表示される",
            "メニューバーが表示される",
            "ツールバーが表示される"
        ]),
        ("フォルダ選択機能", [
            "「フォルダを選択」ボタンが動作する",
            "フォルダ選択ダイアログが開く", 
            "選択したフォルダのパスが表示される",
            "画像ファイルが一覧表示される"
        ]),
        ("地図表示機能", [
            "地図パネルが表示される",
            "GPS情報を持つ画像のマーカーが表示される",
            "マーカーをクリックすると画像が表示される",
            "地図の拡大・縮小が動作する"
        ]),
        ("テーマ機能", [
            "テーマ切り替えボタンが動作する",
            "ライト/ダークテーマの切り替えができる",
            "テーマ変更が全体に反映される",
            "設定が保存される"
        ]),
        ("画像プレビュー", [
            "画像をクリックするとプレビューが表示される",
            "EXIF情報が表示される",
            "次/前の画像に移動できる",
            "プレビューウィンドウが正常に閉じる"
        ])
    ]
    
    for category, items in checklist:
        print(f"\n🔍 {category}:")
        for item in items:
            print(f"   □ {item}")
    
    print(f"\n{'='*60}")
    print("💡 テスト方法:")
    print("   1. アプリケーションのウィンドウで各機能を実際に操作")
    print("   2. 期待通りに動作するかを確認")
    print("   3. エラーが発生した場合はコンソール出力を確認")
    print("   4. 問題があれば詳細を報告")

def main():
    """メイン実行関数"""
    print("🚀 PhotoMap Explorer 手動テストヘルパー開始")
    print("="*60)
    
    # 自動チェック
    results = []
    results.append(("応答性テスト", test_application_responsiveness()))
    results.append(("UIコンポーネントテスト", test_ui_components()))
    results.append(("ファイル構造テスト", test_file_structure()))
    
    # 結果表示
    print(f"\n{'='*60}")
    print("📊 自動テスト結果:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\n総合結果: {passed}/{len(results)} テスト成功 ({success_rate:.0f}%)")
    
    if success_rate >= 80:
        print("🎉 アプリケーションは手動テストの準備が整っています！")
        display_manual_test_checklist()
    else:
        print("⚠️ 一部の自動テストに失敗しています。修正後に再実行してください。")

if __name__ == "__main__":
    main()
