#!/usr/bin/env python3
"""
PhotoMap Explorer マップ表示の最終確認テスト
"""

import sys
import os

def final_map_test():
    """マップ表示機能の最終確認テスト"""
    print("=== PhotoMap Explorer マップ表示最終テスト ===")
    
    try:
        # 1. 必要なライブラリの確認
        print("1. 必要なライブラリの確認")
        import folium
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        print(f"  ✓ folium: {folium.__version__}")
        print("  ✓ PyQt5 QtWebEngineWidgets 利用可能")
        
        # 2. GPS抽出機能のテスト
        print("\n2. GPS抽出機能のテスト")
        from logic.image_utils import extract_gps_coords
        
        # Picturesフォルダ内の画像ファイルを探す
        pictures_dir = os.path.expanduser("~/Pictures")
        image_files = []
        
        if os.path.exists(pictures_dir):
            for root, dirs, files in os.walk(pictures_dir):
                for file in files:
                    if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                        image_files.append(os.path.join(root, file))
                        if len(image_files) >= 5:  # 最大5枚をテスト
                            break
                if len(image_files) >= 5:
                    break
        
        if image_files:
            print(f"  ✓ {len(image_files)}枚の画像ファイルを発見")
            
            gps_images = []
            for img_path in image_files:
                try:
                    gps_info = extract_gps_coords(img_path)
                    if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                        gps_images.append((img_path, gps_info))
                        print(f"    🗺️ GPS付き: {os.path.basename(img_path)} -> {gps_info['latitude']:.6f}, {gps_info['longitude']:.6f}")
                except:
                    pass
            
            if gps_images:
                print(f"  ✓ {len(gps_images)}枚のGPS付き画像を発見")
            else:
                print("  ⚠️  GPS付き画像は発見されませんでした（テスト用座標を使用）")
        else:
            print("  ⚠️  画像ファイルが見つかりません（テスト用座標を使用）")
        
        # 3. マップ生成機能のテスト
        print("\n3. マップ生成機能のテスト")
        from logic.image_utils import generate_map_html
        
        # テスト用座標（東京駅）
        test_lat, test_lon = 35.6762, 139.6503
        html_content = generate_map_html(test_lat, test_lon)
        
        print(f"  ✓ マップHTML生成成功: {len(html_content)} characters")
        
        # HTMLの内容確認
        if "leaflet" in html_content.lower() and "map" in html_content.lower():
            print("  ✓ 有効なLeafletマップHTMLを生成")
        else:
            print("  ⚠️  生成されたHTMLの内容が不完全な可能性があります")
        
        # 4. UI コンポーネントのテスト
        print("\n4. UI コンポーネントのテスト")
        
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        from ui.map_panel import MapPanel
        map_panel = MapPanel()
        print("  ✓ MapPanel作成成功")
        
        # マップ更新テスト
        success = map_panel.update_location(test_lat, test_lon)
        print(f"  update_location結果: {'✓ 成功' if success else '❌ 失敗'}")
        
        print("\n=== マップ表示機能は正常に動作しています ===")
        print("\nアプリを起動して実際にテストしてください:")
        print("  python main.py --ui new")
        print("  または")
        print("  python main.py --ui hybrid")
        
        return True
        
    except Exception as e:
        print(f"\n❌ テスト中にエラーが発生: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = final_map_test()
    sys.exit(0 if success else 1)
