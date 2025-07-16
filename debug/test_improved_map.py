#!/usr/bin/env python3
"""
地図ビュー修正後テストスクリプト

修正された地図ビュー機能をテストします。
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ロガー設定
from utils.debug_logger import debug, info, error, warning, verbose, set_debug_mode

def test_improved_map_panel():
    """改善された地図パネルのテスト"""
    info("改善された地図パネルのテスト開始...")
    
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
        info("地図パネルを作成中...")
        from ui.map_panel import create_map_panel
        map_panel = create_map_panel()
        
        debug(f"地図パネル作成: {type(map_panel)}")
        debug(f"WebEngine使用: {getattr(map_panel, 'use_webengine', '不明')}")
        debug(f"ビュータイプ: {type(map_panel.view) if map_panel.view else 'None'}")
        
        # テスト用座標で地図更新
        test_coordinates = [
            (51.504105555555554, -0.074575, "ロンドン橋"),
            (25.10820386111111, 121.8439483611111, "台湾・九份"),
            (35.699777777777776, 139.7717, "日本・東京")
        ]
        
        success_count = 0
        for lat, lon, location_name in test_coordinates:
            info(f"テスト座標で地図更新: {location_name} (緯度={lat}, 経度={lon})")
            
            try:
                result = map_panel.update_location(lat, lon)
                if result:
                    info(f"✅ {location_name}の地図更新成功")
                    success_count += 1
                else:
                    warning(f"⚠️ {location_name}の地図更新失敗")
            except Exception as e:
                error(f"❌ {location_name}の地図更新エラー: {e}")
        
        # GPS情報なしのテスト
        info("GPS情報なしメッセージのテスト...")
        try:
            map_panel.show_no_gps_message()
            info("✅ GPS情報なしメッセージ表示成功")
        except Exception as e:
            error(f"❌ GPS情報なしメッセージ表示エラー: {e}")
        
        # パネルを表示
        map_panel.show()
        app.processEvents()
        
        # 結果評価
        total_tests = len(test_coordinates)
        if success_count == total_tests:
            info(f"🎉 地図パネルテスト完全成功: {success_count}/{total_tests}")
            return True
        elif success_count > 0:
            warning(f"⚠️ 地図パネルテスト部分成功: {success_count}/{total_tests}")
            return True
        else:
            error("❌ 地図パネルテスト全失敗")
            return False
        
    except Exception as e:
        error(f"❌ 地図パネルテストエラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def test_gps_integration_with_test_images():
    """テスト画像を使用したGPS統合テスト"""
    info("テスト画像を使用したGPS統合テスト開始...")
    
    try:
        from PyQt5.QtCore import Qt, QCoreApplication
        from PyQt5.QtWidgets import QApplication
        
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # テスト画像フォルダを確認
        test_images_dir = project_root / "test_images"
        if not test_images_dir.exists():
            warning(f"⚠️ テスト画像フォルダが見つかりません: {test_images_dir}")
            return False
        
        # 地図パネルを作成
        from ui.map_panel import create_map_panel
        map_panel = create_map_panel()
        
        # GPS抽出機能を取得
        from logic.image_utils import extract_gps_coords
        
        # テスト画像を検索
        image_files = []
        for ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
            image_files.extend(test_images_dir.glob(f"*{ext}"))
        
        if not image_files:
            warning(f"⚠️ テスト画像が見つかりません: {test_images_dir}")
            return False
        
        success_count = 0
        for image_file in image_files[:3]:  # 最初の3つをテスト
            info(f"GPS統合テスト: {image_file.name}")
            
            # GPS情報抽出
            gps_info = extract_gps_coords(str(image_file))
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                debug(f"GPS情報: 緯度={lat}, 経度={lon}")
                
                # 地図更新
                try:
                    result = map_panel.update_location(lat, lon)
                    if result:
                        info(f"✅ {image_file.name}の地図統合成功")
                        success_count += 1
                    else:
                        warning(f"⚠️ {image_file.name}の地図統合失敗")
                except Exception as e:
                    error(f"❌ {image_file.name}の地図統合エラー: {e}")
            else:
                info(f"ℹ️ {image_file.name}: GPS情報なし - GPS情報なし表示をテスト")
                try:
                    map_panel.show_no_gps_message()
                    info(f"✅ {image_file.name}のGPS情報なし表示成功")
                    success_count += 1
                except Exception as e:
                    error(f"❌ {image_file.name}のGPS情報なし表示エラー: {e}")
        
        # パネルを表示
        map_panel.show()
        app.processEvents()
        
        total_tests = len(image_files[:3])
        if success_count >= total_tests * 0.5:  # 50%以上成功なら合格
            info(f"✅ GPS統合テスト成功: {success_count}/{total_tests}")
            return True
        else:
            warning(f"⚠️ GPS統合テスト失敗: {success_count}/{total_tests}")
            return False
        
    except Exception as e:
        error(f"❌ GPS統合テストエラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def test_main_window_map_display_manager():
    """メインウィンドウの地図表示マネージャーテスト"""
    info("メインウィンドウの地図表示マネージャーテスト開始...")
    
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
                debug(f"ステータスメッセージ: {msg}")
        
        dummy_window = DummyMainWindow()
        
        # 地図表示マネージャーを作成
        from presentation.views.functional_main_window.display_managers.map_display_manager import MapDisplayManager
        map_manager = MapDisplayManager(dummy_window)
        
        # 地図パネルを設定
        from ui.map_panel import create_map_panel
        map_panel = create_map_panel()
        map_manager.set_components(map_panel)
        
        debug(f"地図表示マネージャー作成: {type(map_manager)}")
        debug(f"地図パネル設定: {map_manager.map_panel is not None}")
        
        # テスト画像でマップ更新
        test_image_path = project_root / "test_images" / "england-london-bridge.jpg"
        if test_image_path.exists():
            info(f"テスト画像でマップ更新: {test_image_path.name}")
            
            try:
                result = map_manager.update_map(str(test_image_path))
                if result:
                    info("✅ マップ表示マネージャー更新成功")
                    return True
                else:
                    warning("⚠️ マップ表示マネージャー更新失敗")
                    return False
            except Exception as e:
                error(f"❌ マップ表示マネージャー更新エラー: {e}")
                import traceback
                debug(f"スタックトレース: {traceback.format_exc()}")
                return False
        else:
            warning(f"⚠️ テスト画像が見つかりません: {test_image_path}")
            return False
        
    except Exception as e:
        error(f"❌ 地図表示マネージャーテストエラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def main():
    """メイン修正後テスト実行"""
    print("=" * 60)
    print("🗺️ 地図ビュー修正後テストスクリプト")
    print("=" * 60)
    
    # デバッグモード有効化
    set_debug_mode(True)
    
    # 各テストを実行
    tests = [
        ("改善された地図パネル", test_improved_map_panel),
        ("GPS統合テスト", test_gps_integration_with_test_images),
        ("地図表示マネージャーテスト", test_main_window_map_display_manager),
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
    print("\n" + "=" * 60)
    print("🔍 修正後テスト結果まとめ")
    print("=" * 60)
    
    passed_tests = 0
    for test_name, result in results.items():
        status = "✅ 成功" if result else "❌ 失敗"
        print(f"{status} {test_name}")
        if result:
            passed_tests += 1
    
    total_tests = len(results)
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n📊 総合結果: {passed_tests}/{total_tests} 成功 ({success_rate:.1f}%)")
    
    if success_rate >= 75:
        print("🎉 地図ビュー機能は概ね正常に動作しています！")
    elif success_rate >= 50:
        print("⚠️ 地図ビュー機能は部分的に動作していますが、改善が必要です。")
    else:
        print("❌ 地図ビュー機能に重大な問題があります。さらなる修正が必要です。")

if __name__ == "__main__":
    main()
