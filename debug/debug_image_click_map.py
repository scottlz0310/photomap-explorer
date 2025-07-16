#!/usr/bin/env python3
"""画像クリック→地図表示のデバッグスクリプト"""

import sys
import os

# プロジェクトルートを追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

try:
    from utils.debug_logger import debug_logger
except ImportError:
    class FallbackLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def debug(self, msg): print(f"DEBUG: {msg}")
    debug_logger = FallbackLogger()

def simulate_image_click_map_update():
    """画像クリック時の地図更新処理をシミュレーション"""
    debug_logger.info("🔄 画像クリック→地図表示シミュレーション開始")
    
    # GPS付き画像をテスト
    test_image = "test_images/taiwan-jiufen.jpg"
    
    if not os.path.exists(test_image):
        debug_logger.error(f"❌ テスト画像が見つかりません: {test_image}")
        return False
    
    debug_logger.info(f"📷 テスト画像: {test_image}")
    
    # GPS抽出テスト
    try:
        from logic.image_utils import extract_gps_coords
        gps_info = extract_gps_coords(test_image)
        
        if gps_info and "latitude" in gps_info and "longitude" in gps_info:
            lat, lon = gps_info["latitude"], gps_info["longitude"]
            debug_logger.info(f"✅ GPS抽出成功: {lat:.6f}, {lon:.6f}")
            
            # 地図HTML生成テスト
            try:
                from logic.image_utils import generate_map_html
                map_path = generate_map_html(lat, lon)
                debug_logger.info(f"✅ 地図HTML生成成功: {map_path}")
                
                # ファイル確認
                if os.path.exists(map_path):
                    file_size = os.path.getsize(map_path)
                    debug_logger.info(f"✅ 地図ファイル確認: {file_size} bytes")
                    
                    # QtWebEngineでの読み込みをシミュレーション
                    debug_logger.info("🔄 QtWebEngine読み込みシミュレーション...")
                    
                    # ファイルURL形式
                    file_url = f"file://{os.path.abspath(map_path)}"
                    debug_logger.info(f"📍 地図URL: {file_url}")
                    
                    return True
                else:
                    debug_logger.error("❌ 地図ファイルが生成されていません")
                    return False
                    
            except Exception as e:
                debug_logger.error(f"❌ 地図HTML生成エラー: {e}")
                return False
                
        else:
            debug_logger.warning("⚠️ GPS情報が見つかりません")
            return False
            
    except Exception as e:
        debug_logger.error(f"❌ GPS抽出エラー: {e}")
        return False

def debug_map_display_issue():
    """地図表示問題のデバッグ"""
    debug_logger.info("🔍 地図表示問題デバッグ開始")
    
    issues = []
    
    # 1. QtWebEngine利用可能性チェック
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        debug_logger.info("✅ QtWebEngineWidgets利用可能")
    except ImportError as e:
        debug_logger.error(f"❌ QtWebEngineWidgets不利用: {e}")
        issues.append("QtWebEngineWidgets import失敗")
    
    # 2. Folium利用可能性チェック
    try:
        import folium
        debug_logger.info(f"✅ Folium利用可能: v{folium.__version__}")
    except ImportError as e:
        debug_logger.error(f"❌ Folium不利用: {e}")
        issues.append("Folium import失敗")
    
    # 3. 地図生成機能チェック
    try:
        from logic.image_utils import generate_map_html
        debug_logger.info("✅ 地図生成機能利用可能")
    except ImportError as e:
        debug_logger.error(f"❌ 地図生成機能不利用: {e}")
        issues.append("地図生成機能 import失敗")
    
    # 4. GPS抽出機能チェック
    try:
        from logic.image_utils import extract_gps_coords
        debug_logger.info("✅ GPS抽出機能利用可能")
    except ImportError as e:
        debug_logger.error(f"❌ GPS抽出機能不利用: {e}")
        issues.append("GPS抽出機能 import失敗")
    
    debug_logger.info(f"📊 問題数: {len(issues)}")
    for issue in issues:
        debug_logger.warning(f"  ⚠️ {issue}")
    
    return len(issues) == 0

if __name__ == "__main__":
    print("🔄 画像クリック→地図表示デバッグ開始")
    
    # 基本機能チェック
    basic_ok = debug_map_display_issue()
    
    if basic_ok:
        # 画像クリックシミュレーション
        success = simulate_image_click_map_update()
        
        if success:
            print("\n✅ 画像クリック→地図表示プロセス正常")
            print("📌 メインアプリケーションでの確認ポイント:")
            print("1. 画像クリック時のコンソール出力を確認")
            print("2. マップパネルエリアの右クリック→「要素を検証」で内容確認")
            print("3. QtWebEngineプロセスのログ確認")
        else:
            print("\n❌ 画像クリック→地図表示プロセスで問題発生")
    else:
        print("\n❌ 基本機能に問題があります")
    
    print("\n🎯 次のアクション:")
    print("1. メインアプリケーションでtest_images/taiwan-jiufen.jpgをクリック")
    print("2. 右パネル下部の地図エリアを確認")
    print("3. 地図が表示されない場合は、QtWebEngineの初期化問題")
