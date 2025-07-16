#!/usr/bin/env python3
"""
map.html生成・表示確認テストスクリプト

GPS情報からmap.htmlが正しく生成され、メインウィンドウで表示されるかを確認します。
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ロガー設定
from utils.debug_logger import debug, info, error, warning, verbose, set_debug_mode

def test_map_html_generation():
    """地図HTML生成の詳細テスト"""
    info("=== 地図HTML生成テスト開始 ===")
    
    try:
        from logic.image_utils import generate_map_html
        
        # テスト座標（東京駅）
        test_lat, test_lon = 35.681236, 139.767125
        
        info(f"テスト座標: 緯度={test_lat}, 経度={test_lon}")
        
        # 既存のmap.htmlを削除（もしあれば）
        map_file_path = project_root / "map.html"
        if map_file_path.exists():
            info(f"既存のmap.htmlを削除: {map_file_path}")
            map_file_path.unlink()
        
        # 地図HTMLを生成
        info("地図HTML生成中...")
        map_file = generate_map_html(test_lat, test_lon)
        debug(f"生成された地図ファイルパス: {map_file}")
        
        # ファイル生成確認
        if os.path.exists(map_file):
            file_size = os.path.getsize(map_file)
            info(f"✅ 地図HTML生成成功: {map_file}")
            info(f"   ファイルサイズ: {file_size} bytes")
            
            # ファイル内容の詳細確認
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                info("📄 ファイル内容分析:")
                info(f"   総文字数: {len(content)}")
                
                # 重要な要素の確認
                checks = {
                    'leaflet': 'leaflet' in content.lower(),
                    'folium': 'folium' in content.lower(),
                    'map': 'map' in content.lower(),
                    'latitude': str(test_lat) in content,
                    'longitude': str(test_lon) in content,
                    'marker': 'marker' in content.lower(),
                    'html_structure': '<html>' in content.lower() and '</html>' in content.lower()
                }
                
                for check_name, result in checks.items():
                    status = "✅" if result else "❌"
                    info(f"   {status} {check_name}: {result}")
                
                # ファイル内容の先頭と末尾を表示
                verbose("ファイル内容の先頭100文字:")
                verbose(content[:100])
                verbose("ファイル内容の末尾100文字:")
                verbose(content[-100:])
                
                # 全体の妥当性判定
                all_checks_passed = all(checks.values())
                if all_checks_passed:
                    info("✅ 地図HTMLの内容は正常です")
                    return True, map_file
                else:
                    warning("⚠️ 地図HTMLの内容に問題があります")
                    return False, map_file
        else:
            error(f"❌ 地図HTMLファイルが生成されませんでした: {map_file}")
            return False, None
            
    except Exception as e:
        error(f"❌ 地図HTML生成エラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False, None

def test_real_image_gps_and_map():
    """実際の画像からGPS抽出して地図生成テスト"""
    info("=== 実画像GPS→地図生成テスト開始 ===")
    
    try:
        from logic.image_utils import extract_gps_coords, generate_map_html
        
        # テスト画像フォルダをチェック
        test_images_dir = project_root / "test_images"
        
        if not test_images_dir.exists():
            warning(f"⚠️ テスト画像フォルダが見つかりません: {test_images_dir}")
            return False
        
        # GPS付き画像を検索
        image_files = []
        for ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
            image_files.extend(test_images_dir.glob(f"*{ext}"))
        
        if not image_files:
            warning(f"⚠️ テスト画像が見つかりません: {test_images_dir}")
            return False
        
        success_count = 0
        for image_file in image_files:
            info(f"📸 画像処理: {image_file.name}")
            
            # GPS情報抽出
            gps_info = extract_gps_coords(str(image_file))
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                info(f"   GPS情報: 緯度={lat}, 経度={lon}")
                
                # この座標で地図生成
                try:
                    map_file = generate_map_html(lat, lon)
                    if os.path.exists(map_file):
                        file_size = os.path.getsize(map_file)
                        info(f"   ✅ 地図生成成功: {file_size} bytes")
                        success_count += 1
                    else:
                        warning(f"   ⚠️ 地図ファイル生成失敗")
                except Exception as e:
                    error(f"   ❌ 地図生成エラー: {e}")
            else:
                info(f"   ℹ️ GPS情報なし")
        
        if success_count > 0:
            info(f"✅ 実画像GPS→地図生成テスト: {success_count}/{len(image_files)} 成功")
            return True
        else:
            warning("⚠️ GPS付き画像から地図生成に成功しませんでした")
            return False
            
    except Exception as e:
        error(f"❌ 実画像GPS→地図生成テスト エラー: {e}")
        return False

def test_map_display_in_main_window():
    """メインウィンドウでの地図表示テスト"""
    info("=== メインウィンドウ地図表示テスト開始 ===")
    
    try:
        # QtWebEngineの適切な初期化
        from PyQt5.QtCore import Qt, QCoreApplication
        from PyQt5.QtWidgets import QApplication
        
        # 事前に設定
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # 地図パネルを作成
        info("地図パネル作成中...")
        from ui.map_panel import create_map_panel
        map_panel = create_map_panel()
        
        debug(f"地図パネル: {type(map_panel)}")
        debug(f"WebEngine使用: {getattr(map_panel, 'use_webengine', '不明')}")
        
        # テスト用座標で地図更新
        test_lat, test_lon = 35.681236, 139.767125
        info(f"テスト座標で地図更新: 緯度={test_lat}, 経度={test_lon}")
        
        # 更新前のmap.htmlの状態確認
        map_file_path = project_root / "map.html"
        before_exists = map_file_path.exists()
        info(f"更新前map.html存在: {before_exists}")
        
        # 地図更新実行
        result = map_panel.update_location(test_lat, test_lon)
        
        # 更新後のmap.htmlの状態確認
        after_exists = map_file_path.exists()
        info(f"更新後map.html存在: {after_exists}")
        
        if after_exists:
            file_size = os.path.getsize(map_file_path)
            info(f"map.htmlサイズ: {file_size} bytes")
            
            # ファイル内容を確認
            with open(map_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if str(test_lat) in content and str(test_lon) in content:
                    info("✅ map.htmlに正しい座標が含まれています")
                else:
                    warning("⚠️ map.htmlに期待する座標が見つかりません")
                    debug(f"ファイル内容の先頭200文字: {content[:200]}")
        
        if result:
            info("✅ 地図パネルでの地図更新成功")
        else:
            warning("⚠️ 地図パネルでの地図更新失敗")
        
        # パネルを表示
        map_panel.show()
        app.processEvents()
        
        # WebEngineビューの状態確認
        if hasattr(map_panel, 'view') and map_panel.view:
            debug(f"地図ビューの状態: {type(map_panel.view)}")
            if hasattr(map_panel.view, 'url'):
                current_url = map_panel.view.url()
                debug(f"現在読み込み中のURL: {current_url.toString()}")
        
        return result and after_exists
        
    except Exception as e:
        error(f"❌ メインウィンドウ地図表示テスト エラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def test_map_display_manager_integration():
    """地図表示マネージャーとの統合テスト"""
    info("=== 地図表示マネージャー統合テスト開始 ===")
    
    try:
        from PyQt5.QtCore import Qt, QCoreApplication
        from PyQt5.QtWidgets import QApplication
        
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # ダミーメインウィンドウ
        class DummyMainWindow:
            def show_status_message(self, msg):
                info(f"ステータスメッセージ: {msg}")
        
        dummy_window = DummyMainWindow()
        
        # 地図表示マネージャーを作成
        from presentation.views.functional_main_window.display_managers.map_display_manager import MapDisplayManager
        map_manager = MapDisplayManager(dummy_window)
        
        # 地図パネルを設定
        from ui.map_panel import create_map_panel
        map_panel = create_map_panel()
        map_manager.set_components(map_panel)
        
        debug(f"地図表示マネージャー: {type(map_manager)}")
        debug(f"地図パネル設定: {map_manager.map_panel is not None}")
        
        # テスト画像でマップ更新
        test_image_path = project_root / "test_images" / "england-london-bridge.jpg"
        if test_image_path.exists():
            info(f"テスト画像でマップ更新: {test_image_path.name}")
            
            # 更新前のmap.htmlの状態
            map_file_path = project_root / "map.html"
            before_exists = map_file_path.exists()
            before_size = os.path.getsize(map_file_path) if before_exists else 0
            
            info(f"更新前: 存在={before_exists}, サイズ={before_size}")
            
            # マップ更新実行
            result = map_manager.update_map(str(test_image_path))
            
            # 更新後のmap.htmlの状態
            after_exists = map_file_path.exists()
            after_size = os.path.getsize(map_file_path) if after_exists else 0
            
            info(f"更新後: 存在={after_exists}, サイズ={after_size}")
            
            if result:
                info("✅ 地図表示マネージャーでの更新成功")
            else:
                warning("⚠️ 地図表示マネージャーでの更新失敗")
            
            # map.htmlの内容確認
            if after_exists and after_size > 0:
                info("✅ map.htmlが正常に生成されました")
                return True
            else:
                warning("⚠️ map.htmlの生成に問題があります")
                return False
        else:
            warning(f"⚠️ テスト画像が見つかりません: {test_image_path}")
            return False
        
    except Exception as e:
        error(f"❌ 地図表示マネージャー統合テスト エラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def verify_final_map_html():
    """最終的なmap.htmlファイルの検証"""
    info("=== 最終map.html検証 ===")
    
    map_file_path = project_root / "map.html"
    
    if map_file_path.exists():
        file_size = os.path.getsize(map_file_path)
        info(f"✅ map.html存在確認: {map_file_path}")
        info(f"   ファイルサイズ: {file_size} bytes")
        
        # ファイルを開いてブラウザで表示可能かテスト
        try:
            with open(map_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # HTML構造の確認
                has_html = '<html>' in content.lower() and '</html>' in content.lower()
                has_head = '<head>' in content.lower() and '</head>' in content.lower()
                has_body = '<body>' in content.lower() and '</body>' in content.lower()
                has_leaflet = 'leaflet' in content.lower()
                has_map_div = 'map' in content.lower()
                
                info("📄 HTML構造チェック:")
                info(f"   ✅ HTML構造: {has_html}")
                info(f"   ✅ HEAD要素: {has_head}")
                info(f"   ✅ BODY要素: {has_body}")
                info(f"   ✅ Leaflet: {has_leaflet}")
                info(f"   ✅ MAP要素: {has_map_div}")
                
                all_valid = all([has_html, has_head, has_body, has_leaflet, has_map_div])
                
                if all_valid:
                    info("✅ map.htmlは有効なHTML地図ファイルです")
                    
                    # ファイルの絶対パスを表示
                    abs_path = map_file_path.absolute()
                    info(f"🌐 ブラウザで確認可能: file://{abs_path}")
                    
                    return True
                else:
                    warning("⚠️ map.htmlに必要な要素が不足しています")
                    return False
                    
        except Exception as e:
            error(f"❌ map.htmlの読み込みエラー: {e}")
            return False
    else:
        error("❌ map.htmlファイルが存在しません")
        return False

def main():
    """メインテスト実行"""
    print("=" * 70)
    print("🗺️ map.html生成・表示確認テストスクリプト")
    print("=" * 70)
    
    # デバッグモード有効化
    set_debug_mode(True)
    
    # 各テストを実行
    tests = [
        ("地図HTML生成テスト", test_map_html_generation),
        ("実画像GPS→地図生成", test_real_image_gps_and_map),
        ("メインウィンドウ地図表示", test_map_display_in_main_window),
        ("地図表示マネージャー統合", test_map_display_manager_integration),
        ("最終map.html検証", verify_final_map_html),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            error(f"テスト実行エラー: {e}")
            results[test_name] = False
    
    # 結果まとめ
    print("\n" + "=" * 70)
    print("🔍 map.html生成・表示テスト結果まとめ")
    print("=" * 70)
    
    passed_tests = 0
    for test_name, result in results.items():
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{status} {test_name}")
        if result:
            passed_tests += 1
    
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n📊 総合結果: {passed_tests}/{total_tests} 成功 ({success_rate:.1f}%)")
    
    # 最終的なmap.htmlファイルの場所を表示
    map_file_path = project_root / "map.html"
    if map_file_path.exists():
        abs_path = map_file_path.absolute()
        print(f"\n🗺️ 生成されたmap.html: file://{abs_path}")
        print("   ↑ このURLをブラウザで開いて地図を確認できます")
    
    if success_rate >= 80:
        print("\n🎉 map.html生成・表示機能は正常に動作しています！")
    elif success_rate >= 60:
        print("\n⚠️ map.html生成・表示機能は概ね動作していますが、一部改善が必要です。")
    else:
        print("\n❌ map.html生成・表示機能に重大な問題があります。")

if __name__ == "__main__":
    main()
