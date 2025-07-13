#!/usr/bin/env python3
"""
新しく追加されたテーマのテストスクリプト
"""

import sys
import os

# プロジェクトルートを追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_new_themes():
    """新しく追加されたテーマをテスト"""
    print("=== 新しいテーマテスト開始 ===")
    
    try:
        from presentation.themes.theme_init import get_theme_initializer
        
        # テーマ初期化
        initializer = get_theme_initializer()
        
        # 設定ファイルを再読み込み（新しいテーマを認識させる）
        initializer.load_theme_settings()
        
        available_themes = initializer.get_available_theme_names()
        print(f"利用可能なテーマ数: {len(available_themes)}")
        print(f"テーマ一覧: {available_themes}")
        
        # 新しく追加されたテーマを特にテスト
        new_themes = ['orange', 'pink', 'red', 'teal', 'yellow', 'gray']
        
        for theme_name in new_themes:
            if theme_name in available_themes:
                print(f"\n--- {theme_name} テーマテスト ---")
                
                # テーマ定義を取得
                theme_def = initializer.get_theme_definition(theme_name)
                if theme_def:
                    print(f"✅ 表示名: {theme_def.get('display_name', theme_name)}")
                    print(f"✅ 説明: {theme_def.get('description', 'なし')}")
                    print(f"✅ 背景色: {theme_def.get('backgroundColor', 'なし')}")
                    print(f"✅ テキスト色: {theme_def.get('textColor', 'なし')}")
                    print(f"✅ プライマリ色: {theme_def.get('primaryColor', 'なし')}")
                
                # スタイルシート生成テスト
                stylesheet = initializer.create_theme_stylesheet(theme_name)
                if stylesheet:
                    print(f"✅ スタイルシート生成成功: {len(stylesheet)} 文字")
                else:
                    print("❌ スタイルシート生成失敗")
            else:
                print(f"❌ {theme_name} テーマが見つかりません")
        
        # テーマサイクルテスト（新しいテーマを含む）
        print(f"\n--- 拡張テーマサイクルテスト ---")
        original_theme = initializer.get_current_theme()
        print(f"開始テーマ: {original_theme}")
        
        for i in range(len(available_themes)):
            new_theme = initializer.cycle_theme()
            theme_def = initializer.get_theme_definition(new_theme)
            display_name = theme_def.get('display_name', new_theme) if theme_def else new_theme
            print(f"サイクル {i+1}: {new_theme} ({display_name})")
        
        print(f"最終テーマ: {initializer.get_current_theme()}")
        
    except Exception as e:
        print(f"テストエラー: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== 新しいテーマテスト完了 ===")

if __name__ == "__main__":
    # DEBUG_LEVELを設定
    os.environ["DEBUG_LEVEL"] = "VERBOSE"
    
    test_new_themes()
