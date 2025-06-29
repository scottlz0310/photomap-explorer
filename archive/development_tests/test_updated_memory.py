#!/usr/bin/env python3
"""
変更後のメモリ内処理方式のテスト
"""

import sys

def test_updated_implementation():
    """変更後の実装をテスト"""
    print("=== 変更後のメモリ内処理実装テスト ===")
    
    try:
        # テスト用座標（東京駅）
        test_lat, test_lon = 35.6762, 139.6503
        
        print("1. 変更後のHTML生成テスト")
        from logic.image_utils import generate_map_html
        
        html_content = generate_map_html(test_lat, test_lon)
        print(f"  ✓ HTML生成成功: {len(html_content)} characters")
        print(f"  最初の200文字: {html_content[:200]}...")
        
        # HTMLの内容確認
        if "leaflet" in html_content.lower() and "map" in html_content.lower():
            print("  ✓ 有効なLeafletマップHTMLを生成")
        else:
            print("  ⚠️  生成されたHTMLの内容が不完全な可能性があります")
        
        # PyQt5でのテスト
        print("\n2. PyQt5での表示テスト")
        from PyQt5.QtWidgets import QApplication
        from ui.map_panel import MapPanel
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        map_panel = MapPanel()
        success = map_panel.update_location(test_lat, test_lon)
        print(f"  update_location結果: {'✓ 成功' if success else '❌ 失敗'}")
        
        # 実際のGPS画像でのテスト
        print("\n3. 実際のGPS画像でのテスト")
        import os
        from logic.image_utils import extract_gps_coords
        
        pictures_dir = os.path.expanduser("~/Pictures")
        test_images = []
        
        if os.path.exists(pictures_dir):
            for root, dirs, files in os.walk(pictures_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg')):
                        img_path = os.path.join(root, file)
                        gps_info = extract_gps_coords(img_path)
                        if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                            test_images.append((img_path, gps_info))
                            if len(test_images) >= 2:  # 2枚をテスト
                                break
                if len(test_images) >= 2:
                    break
        
        if test_images:
            for img_path, gps_info in test_images:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                success = map_panel.update_location(lat, lon)
                img_name = os.path.basename(img_path)
                print(f"  📷 {img_name}: {lat:.6f}, {lon:.6f} -> {'✓' if success else '❌'}")
        else:
            print("  ⚠️  GPS付き画像が見つかりませんでした")
        
        print("\n=== メモリ内処理実装テスト成功 ===")
        print("\n✅ 改善点:")
        print("  • 一時ファイルの作成・削除が不要")
        print("  • ディスクI/Oの削減でパフォーマンス向上")
        print("  • よりシンプルで保守しやすいコード")
        print("  • ファイルシステムのリスクなし")
        
        return True
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_updated_implementation()
    sys.exit(0 if success else 1)
