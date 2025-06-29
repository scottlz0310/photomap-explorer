#!/usr/bin/env python3
"""
修正されたマップ表示のテストスクリプト
"""

import sys
import os

def test_fixed_map():
    """修正されたマップ表示をテスト"""
    print("=== 修正されたマップ表示テスト ===")
    
    # テスト用のGPS座標
    test_lat, test_lon = 35.6762, 139.6503  # 東京駅
    
    try:
        # HTMLコンテンツ生成テスト
        print("1. 修正されたHTML生成テスト")
        from logic.image_utils import generate_map_html
        
        html_content = generate_map_html(test_lat, test_lon)
        print(f"  ✓ HTML生成成功: {len(html_content)} characters")
        print(f"  最初の200文字: {html_content[:200]}...")
        
        # HTMLファイルとして一時保存してブラウザで確認
        test_file = "test_map_output.html"
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"  ✓ テスト用HTMLファイル保存: {test_file}")
        
        # PyQt5でのテスト
        print("\n2. PyQt5でのテスト")
        from PyQt5.QtWidgets import QApplication
        from ui.map_panel import MapPanel
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        map_panel = MapPanel()
        success = map_panel.update_location(test_lat, test_lon)
        print(f"  update_location結果: {success}")
        
        print("\n=== 修正されたマップ表示テスト完了 ===")
        return True
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_fixed_map()
    sys.exit(0 if success else 1)
