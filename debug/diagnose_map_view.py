#!/usr/bin/env python3
"""
地図ビュー機能の診断・デバッグスクリプト

このスクリプトは地図ビュー関連の問題を特定し、修正のための情報を提供します。
"""

import os
import sys
import logging
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ロガー設定
from utils.debug_logger import debug, info, error, warning, verbose, set_debug_mode

def test_qtwebengine_availability():
    """QtWebEngineの利用可能性をテスト"""
    info("QtWebEngineの利用可能性をテスト中...")
    
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        info("✅ QtWebEngineWidgets.QWebEngineView - インポート成功")
        return True
    except ImportError as e:
        error(f"❌ QtWebEngineWidgets.QWebEngineView - インポート失敗: {e}")
        return False
    except Exception as e:
        error(f"❌ QtWebEngineWidgets.QWebEngineView - 予期しないエラー: {e}")
        return False

def test_folium_availability():
    """Foliumライブラリの利用可能性をテスト"""
    info("Foliumライブラリの利用可能性をテスト中...")
    
    try:
        import folium
        version = getattr(folium, '__version__', '不明')
        info(f"✅ Folium - インポート成功 (バージョン: {version})")
        return True
    except ImportError as e:
        error(f"❌ Folium - インポート失敗: {e}")
        return False
    except Exception as e:
        error(f"❌ Folium - 予期しないエラー: {e}")
        return False

def test_exifread_availability():
    """exifreadライブラリの利用可能性をテスト"""
    info("exifreadライブラリの利用可能性をテスト中...")
    
    try:
        import exifread
        info(f"✅ exifread - インポート成功")
        return True
    except ImportError as e:
        error(f"❌ exifread - インポート失敗: {e}")
        return False
    except Exception as e:
        error(f"❌ exifread - 予期しないエラー: {e}")
        return False

def test_map_html_generation():
    """地図HTML生成機能をテスト"""
    info("地図HTML生成機能をテスト中...")
    
    try:
        from logic.image_utils import generate_map_html
        
        # 東京駅の座標でテスト
        test_lat, test_lon = 35.681236, 139.767125
        
        debug(f"テスト座標: 緯度={test_lat}, 経度={test_lon}")
        
        # 地図HTMLを生成
        map_file = generate_map_html(test_lat, test_lon)
        
        if os.path.exists(map_file):
            file_size = os.path.getsize(map_file)
            info(f"✅ 地図HTML生成成功: {map_file} (サイズ: {file_size} bytes)")
            
            # ファイル内容の一部を確認
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read(500)  # 最初の500文字
                if 'leaflet' in content.lower() and 'map' in content.lower():
                    info("✅ 地図HTMLの内容も正常")
                else:
                    warning("⚠️ 地図HTMLの内容に異常の可能性")
                    verbose(f"ファイル内容の先頭: {content}")
            
            return True
        else:
            error(f"❌ 地図HTMLファイルが見つかりません: {map_file}")
            return False
            
    except Exception as e:
        error(f"❌ 地図HTML生成エラー: {e}")
        return False

def test_gps_extraction():
    """GPS情報抽出機能をテスト"""
    info("GPS情報抽出機能をテスト中...")
    
    try:
        from logic.image_utils import extract_gps_coords
        
        # テスト用画像フォルダをチェック
        test_images_dir = project_root / "test_images"
        
        if not test_images_dir.exists():
            warning(f"⚠️ テスト画像フォルダが見つかりません: {test_images_dir}")
            return False
        
        # テスト画像ファイルを検索
        image_files = []
        for ext in ['.jpg', '.jpeg', '.JPG', '.JPEG']:
            image_files.extend(test_images_dir.glob(f"*{ext}"))
        
        if not image_files:
            warning(f"⚠️ テスト画像が見つかりません: {test_images_dir}")
            return False
        
        success_count = 0
        for image_file in image_files[:3]:  # 最初の3つをテスト
            debug(f"GPS情報抽出テスト: {image_file.name}")
            
            gps_info = extract_gps_coords(str(image_file))
            
            if gps_info:
                info(f"✅ GPS情報抽出成功: {image_file.name}")
                verbose(f"   緯度: {gps_info.get('latitude', 'N/A')}")
                verbose(f"   経度: {gps_info.get('longitude', 'N/A')}")
                success_count += 1
            else:
                info(f"ℹ️ GPS情報なし: {image_file.name}")
        
        if success_count > 0:
            info(f"✅ GPS抽出テスト完了: {success_count}/{len(image_files[:3])} 成功")
            return True
        else:
            warning("⚠️ GPS情報を持つ画像が見つかりませんでした")
            return False
            
    except Exception as e:
        error(f"❌ GPS情報抽出テスト エラー: {e}")
        return False

def test_map_components():
    """地図コンポーネントの作成テスト"""
    info("地図コンポーネントの作成テスト中...")
    
    try:
        # PyQt5アプリケーション初期化
        from PyQt5.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # map_viewのテスト
        try:
            from ui.map_view import create_map_view
            map_view = create_map_view()
            info("✅ map_view作成成功")
            verbose(f"   map_viewタイプ: {type(map_view)}")
        except Exception as e:
            error(f"❌ map_view作成失敗: {e}")
        
        # map_panelのテスト
        try:
            from ui.map_panel import create_map_panel
            map_panel = create_map_panel()
            info("✅ map_panel作成成功")
            verbose(f"   map_panelタイプ: {type(map_panel)}")
            verbose(f"   WebEngine使用: {getattr(map_panel, 'use_webengine', '不明')}")
        except Exception as e:
            error(f"❌ map_panel作成失敗: {e}")
        
        # map_display_managerのテスト
        try:
            from presentation.views.functional_main_window.display_managers.map_display_manager import MapDisplayManager
            
            # ダミーのメインウィンドウ
            class DummyMainWindow:
                def show_status_message(self, msg):
                    debug(f"ステータス: {msg}")
            
            dummy_window = DummyMainWindow()
            map_manager = MapDisplayManager(dummy_window)
            info("✅ MapDisplayManager作成成功")
            verbose(f"   MapDisplayManagerタイプ: {type(map_manager)}")
        except Exception as e:
            error(f"❌ MapDisplayManager作成失敗: {e}")
        
        return True
        
    except Exception as e:
        error(f"❌ 地図コンポーネントテスト エラー: {e}")
        return False

def check_environment_setup():
    """環境設定をチェック"""
    info("環境設定をチェック中...")
    
    # Python環境
    info(f"Python バージョン: {sys.version}")
    info(f"プロジェクトルート: {project_root}")
    
    # 重要なファイルの存在確認
    important_files = [
        "logic/image_utils.py",
        "ui/map_view.py", 
        "ui/map_panel.py",
        "presentation/views/functional_main_window/display_managers/map_display_manager.py",
        "map.html"
    ]
    
    for file_path in important_files:
        full_path = project_root / file_path
        if full_path.exists():
            info(f"✅ {file_path} - 存在")
        else:
            error(f"❌ {file_path} - 存在しない")

def main():
    """メイン診断実行"""
    print("=" * 60)
    print("🗺️ 地図ビュー機能診断スクリプト")
    print("=" * 60)
    
    # デバッグモード有効化
    set_debug_mode(True)
    
    # 各テストを実行
    tests = [
        ("環境設定チェック", check_environment_setup),
        ("QtWebEngine利用可能性", test_qtwebengine_availability),
        ("Folium利用可能性", test_folium_availability),
        ("exifread利用可能性", test_exifread_availability),
        ("地図HTML生成", test_map_html_generation),
        ("GPS情報抽出", test_gps_extraction),
        ("地図コンポーネント", test_map_components),
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
    print("🔍 診断結果まとめ")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 正常" if result else "❌ 問題あり"
        print(f"{status} {test_name}")
    
    # 推奨事項
    failed_tests = [name for name, result in results.items() if not result]
    if failed_tests:
        print(f"\n⚠️ 問題が検出された項目: {len(failed_tests)} 個")
        for test_name in failed_tests:
            print(f"   - {test_name}")
        
        print("\n💡 推奨修正措置:")
        if "QtWebEngine利用可能性" in failed_tests:
            print("   - QtWebEngineWidgetsのインストール確認")
        if "Folium利用可能性" in failed_tests:
            print("   - pip install folium")
        if "exifread利用可能性" in failed_tests:
            print("   - pip install exifread")
    else:
        print("\n🎉 すべてのテストが正常に完了しました！")

if __name__ == "__main__":
    main()
