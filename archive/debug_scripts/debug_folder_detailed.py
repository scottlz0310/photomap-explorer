#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新UIフォルダ内容表示の詳細デバッグスクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
import traceback

def test_detailed_functional_new_main_window():
    """FunctionalNewMainWindowの詳細デバッグテスト"""
    print("=== FunctionalNewMainWindow 詳細デバッグ ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        from presentation.views.functional_new_main_view import FunctionalNewMainWindow
        
        print("✅ FunctionalNewMainWindow インポート成功")
        
        # インスタンス作成前に静的解析
        print("📄 クラス定義確認:")
        print(f"  - _load_initial_folder メソッド: {hasattr(FunctionalNewMainWindow, '_load_initial_folder')}")
        print(f"  - _load_folder メソッド: {hasattr(FunctionalNewMainWindow, '_load_folder')}")
        print(f"  - _update_folder_content メソッド: {hasattr(FunctionalNewMainWindow, '_update_folder_content')}")
        
        # インスタンス作成
        print("\n🔧 インスタンス作成中...")
        main_view = FunctionalNewMainWindow()
        print("✅ FunctionalNewMainWindow インスタンス作成成功")
        
        # UI要素の初期状態確認
        print("\n🖥️ UI要素初期状態:")
        print(f"  - folder_content_list: {main_view.folder_content_list}")
        print(f"  - folder_content_list type: {type(main_view.folder_content_list)}")
        
        if main_view.folder_content_list:
            print(f"  - アイテム数: {main_view.folder_content_list.count()}")
            
            # リストの内容を確認
            if main_view.folder_content_list.count() > 0:
                print("  - アイテム一覧:")
                for i in range(min(5, main_view.folder_content_list.count())):
                    item = main_view.folder_content_list.item(i)
                    print(f"    {i}: {item.text()}")
            else:
                print("  - リストが空です")
        else:
            print("  - folder_content_list が None")
        
        # 現在のフォルダ状態確認
        print(f"\n📁 現在のフォルダ情報:")
        print(f"  - current_folder: {main_view.current_folder}")
        
        if main_view.current_folder:
            folder_exists = os.path.exists(main_view.current_folder)
            print(f"  - フォルダ存在: {folder_exists}")
            
            if folder_exists:
                try:
                    folder = Path(main_view.current_folder)
                    items = list(folder.iterdir())
                    print(f"  - フォルダ内アイテム数: {len(items)}")
                    
                    # 最初の5個を表示
                    for i, item in enumerate(items[:5]):
                        item_type = "📁" if item.is_dir() else "📄"
                        print(f"    {item_type} {item.name}")
                    
                    if len(items) > 5:
                        print(f"    ... あと{len(items) - 5}個")
                        
                except Exception as e:
                    print(f"  ❌ フォルダ内容取得エラー: {e}")
        
        # 手動でフォルダ内容更新を試行
        print(f"\n🔄 手動フォルダ内容更新テスト:")
        test_folder = os.path.join(os.path.expanduser("~"), "Pictures")
        print(f"  - テストフォルダ: {test_folder}")
        
        try:
            print("  - _update_folder_content 呼び出し前のアイテム数:", 
                  main_view.folder_content_list.count() if main_view.folder_content_list else "None")
            
            main_view._update_folder_content(test_folder)
            
            print("  - _update_folder_content 呼び出し後のアイテム数:", 
                  main_view.folder_content_list.count() if main_view.folder_content_list else "None")
                  
            # 更新後のリスト内容を表示
            if main_view.folder_content_list and main_view.folder_content_list.count() > 0:
                print("  - 更新後のアイテム一覧:")
                for i in range(min(5, main_view.folder_content_list.count())):
                    item = main_view.folder_content_list.item(i)
                    print(f"    {i}: {item.text()}")
            else:
                print("  ❌ 更新後もリストが空")
                
        except Exception as e:
            print(f"  ❌ 手動更新エラー: {e}")
            traceback.print_exc()
        
        # _load_folder メソッドを直接テスト
        print(f"\n🔄 _load_folder 直接テスト:")
        try:
            print("  - _load_folder 呼び出し前のアイテム数:", 
                  main_view.folder_content_list.count() if main_view.folder_content_list else "None")
            
            main_view._load_folder(test_folder)
            
            print("  - _load_folder 呼び出し後のアイテム数:", 
                  main_view.folder_content_list.count() if main_view.folder_content_list else "None")
                  
            # 更新後のリスト内容を表示
            if main_view.folder_content_list and main_view.folder_content_list.count() > 0:
                print("  - _load_folder後のアイテム一覧:")
                for i in range(min(5, main_view.folder_content_list.count())):
                    item = main_view.folder_content_list.item(i)
                    print(f"    {i}: {item.text()}")
            else:
                print("  ❌ _load_folder後もリストが空")
                
        except Exception as e:
            print(f"  ❌ _load_folder エラー: {e}")
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ 詳細デバッグエラー: {e}")
        traceback.print_exc()
        return False

def main():
    """メイン処理"""
    print("新UIフォルダ内容表示の詳細デバッグ開始")
    
    result = test_detailed_functional_new_main_window()
    
    print(f"\n{'='*50}")
    print(f"詳細デバッグ結果: {'✅ 完了' if result else '❌ エラー'}")

if __name__ == "__main__":
    main()
