#!/usr/bin/env python3
"""
テーマの簡素化をテスト - 基本3テーマのみ
"""
import sys
import os

# プロジェクトルートをパスに追加
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from presentation.themes.theme_init import ThemeInitializer

def test_simplified_themes():
    print("=== 簡素化されたテーマシステムテスト ===")
    
    # テーマイニシャライザー作成
    theme_init = ThemeInitializer()
    
    # 利用可能なテーマ一覧
    available_themes = theme_init.get_available_theme_names()
    print(f"利用可能なテーマ数: {len(available_themes)}")
    print(f"テーマ一覧: {available_themes}")
    
    # 各テーマをテスト
    for theme_name in available_themes:
        print(f"\n--- {theme_name} テーマテスト ---")
        theme_config = theme_init.get_theme_definition(theme_name)
        
        if theme_config:
            # 基本情報
            print(f"✅ 表示名: {theme_config.get('display_name', 'N/A')}")
            print(f"✅ 説明: {theme_config.get('description', 'N/A')}")
            print(f"✅ 背景色: {theme_config.get('backgroundColor', 'N/A')}")
            print(f"✅ テキスト色: {theme_config.get('textColor', 'N/A')}")
            print(f"✅ プライマリ色: {theme_config.get('primaryColor', 'N/A')}")
            
            # スタイルシート生成テスト
            try:
                stylesheet = theme_init.create_theme_stylesheet(theme_name)
                print(f"✅ スタイルシート生成成功: {len(stylesheet)} 文字")
            except Exception as e:
                print(f"❌ スタイルシート生成失敗: {e}")
        else:
            print(f"❌ テーマ設定が見つかりません")
    
    # テーマサイクルテスト
    print(f"\n--- シンプルテーマサイクルテスト ---")
    current = "dark"
    print(f"開始テーマ: {current}")
    
    for i in range(1, 6):  # 5回サイクル
        current_index = available_themes.index(current)
        next_index = (current_index + 1) % len(available_themes)
        current = available_themes[next_index]
        config = theme_init.get_theme_definition(current)
        display_name = config.get('display_name', current) if config else current
        print(f"サイクル {i}: {current} ({display_name})")
    
    print(f"最終テーマ: {current}")
    
    print(f"\n=== 簡素化テーマテスト完了 ===")

if __name__ == "__main__":
    test_simplified_themes()
