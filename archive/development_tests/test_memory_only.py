#!/usr/bin/env python3
"""
完全メモリ内処理でのマップ生成テスト
"""

import sys
import os

def generate_map_html_memory_only(lat, lon):
    """メモリ内のみでマップHTMLを生成（一時ファイルなし）"""
    import folium
    import io
    
    # Foliumマップを作成
    map_obj = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="画像の位置").add_to(map_obj)
    
    # BytesIOを使用してメモリ内でHTMLを生成
    output = io.BytesIO()
    map_obj.save(output, close_file=False)
    html_content = output.getvalue().decode('utf-8')
    output.close()
    
    return html_content

def test_memory_only_approach():
    """完全メモリ内処理のテスト"""
    print("=== 完全メモリ内処理マップ生成テスト ===")
    
    try:
        # テスト用座標（東京駅）
        test_lat, test_lon = 35.6762, 139.6503
        
        print("1. メモリ内のみでHTML生成テスト")
        html_content = generate_map_html_memory_only(test_lat, test_lon)
        print(f"  ✓ HTML生成成功: {len(html_content)} characters")
        print(f"  最初の200文字: {html_content[:200]}...")
        
        # HTMLの内容確認
        if "leaflet" in html_content.lower() and "map" in html_content.lower():
            print("  ✓ 有効なLeafletマップHTMLを生成")
        else:
            print("  ⚠️  生成されたHTMLの内容が不完全な可能性があります")
        
        # 現在の一時ファイル方式と比較
        print("\n2. 現在の実装との比較")
        from logic.image_utils import generate_map_html
        current_html = generate_map_html(test_lat, test_lon)
        print(f"  現在の実装: {len(current_html)} characters")
        print(f"  メモリ内実装: {len(html_content)} characters")
        
        # 内容の差分確認
        if len(current_html) == len(html_content):
            print("  ✓ 同じ長さのHTMLが生成されました")
        else:
            print(f"  📊 長さの差: {abs(len(current_html) - len(html_content))} characters")
        
        # PyQt5でのテスト
        print("\n3. PyQt5での表示テスト")
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        web_view = QWebEngineView()
        web_view.setHtml(html_content)
        print("  ✓ メモリ内生成HTMLをQWebEngineViewに設定成功")
        
        # テスト用HTMLファイルとして保存（検証用）
        test_file = "test_memory_only_map.html"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  ✓ 検証用HTMLファイル保存: {test_file}")
        
        print("\n=== 完全メモリ内処理テスト成功 ===")
        print("\nメモリ内処理の利点:")
        print("  ✓ 一時ファイルの作成・削除なし")
        print("  ✓ ディスクI/Oの削減")
        print("  ✓ よりクリーンな実装")
        
        return True
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_memory_only_approach()
    sys.exit(0 if success else 1)
