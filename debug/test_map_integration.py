#!/usr/bin/env python3
"""
地図ビュー統合テストスクリプト

実際のメインウィンドウとの統合でどこで問題が発生しているかを特定します。
"""

import os
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ロガー設定
from utils.debug_logger import debug, info, error, warning, verbose, set_debug_mode

def test_main_window_map_integration():
    """メインウィンドウとの地図統合テスト"""
    info("メインウィンドウとの地図統合テスト開始...")
    
    try:
        # Qt環境セットアップ
        from PyQt5.QtCore import Qt, QCoreApplication
        from PyQt5.QtWidgets import QApplication
        
        # Qt環境の設定
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # メインウィンドウを作成
        info("メインウィンドウを作成中...")
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        
        window = RefactoredFunctionalMainWindow()
        debug(f"メインウィンドウ作成成功: {type(window)}")
        
        # 右パネルマネージャーの確認
        if hasattr(window, 'right_panel_manager') and window.right_panel_manager:
            info("✅ 右パネルマネージャーが存在")
            verbose(f"右パネルマネージャータイプ: {type(window.right_panel_manager)}")
            
            # 右パネル内容確認
            if hasattr(window.right_panel_manager, 'panel'):
                debug(f"右パネル存在: {window.right_panel_manager.panel is not None}")
                
                if hasattr(window.right_panel_manager, 'right_splitter'):
                    debug(f"右スプリッター存在: {window.right_panel_manager.right_splitter is not None}")
                    
                    if window.right_panel_manager.right_splitter:
                        splitter = window.right_panel_manager.right_splitter
                        debug(f"右スプリッター子要素数: {splitter.count()}")
                        
                        for i in range(splitter.count()):
                            widget = splitter.widget(i)
                            debug(f"子要素{i}: {type(widget).__name__}")
                            
                            # 地図パネルを探す
                            if hasattr(widget, 'objectName'):
                                debug(f"  オブジェクト名: {widget.objectName()}")
                            
                            # 地図パネルかどうか確認
                            if 'map' in type(widget).__name__.lower():
                                info(f"✅ 地図パネル発見: {type(widget).__name__}")
                                
                                # 地図パネルの詳細確認
                                if hasattr(widget, 'view'):
                                    debug(f"地図ビュー存在: {widget.view is not None}")
                                    if widget.view:
                                        debug(f"地図ビュータイプ: {type(widget.view)}")
                                
                                if hasattr(widget, 'use_webengine'):
                                    debug(f"WebEngine使用: {widget.use_webengine}")
        
        # 地図表示マネージャーの確認
        if hasattr(window, 'map_display_manager'):
            info("✅ 地図表示マネージャーが存在")
            verbose(f"地図表示マネージャータイプ: {type(window.map_display_manager)}")
        else:
            warning("⚠️ 地図表示マネージャーが見つかりません")
        
        # ウィンドウを表示してテスト
        info("ウィンドウを表示してテスト...")
        window.show()
        app.processEvents()
        
        # テスト用画像でGPS表示テスト
        test_image_path = project_root / "test_images" / "england-london-bridge.jpg"
        if test_image_path.exists():
            info(f"テスト画像でGPS表示テスト: {test_image_path.name}")
            
            # GPS情報を抽出
            from logic.image_utils import extract_gps_coords
            gps_info = extract_gps_coords(str(test_image_path))
            
            if gps_info:
                debug(f"GPS情報: 緯度={gps_info['latitude']}, 経度={gps_info['longitude']}")
                
                # 地図表示マネージャーを使って地図更新
                if hasattr(window, 'map_display_manager') and window.map_display_manager:
                    try:
                        result = window.map_display_manager.update_map(str(test_image_path))
                        if result:
                            info("✅ 地図更新成功")
                        else:
                            warning("⚠️ 地図更新失敗")
                    except Exception as e:
                        error(f"❌ 地図更新エラー: {e}")
                        import traceback
                        debug(f"スタックトレース: {traceback.format_exc()}")
                else:
                    warning("⚠️ 地図表示マネージャーが利用できません")
        
        return True
        
    except Exception as e:
        error(f"❌ 統合テストエラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def test_map_panel_direct():
    """地図パネルの直接テスト"""
    info("地図パネルの直接テスト開始...")
    
    try:
        from PyQt5.QtWidgets import QApplication
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # 地図パネルを直接作成
        from ui.map_panel import create_map_panel
        map_panel = create_map_panel()
        
        debug(f"地図パネル作成: {type(map_panel)}")
        debug(f"WebEngine使用: {getattr(map_panel, 'use_webengine', '不明')}")
        
        # テスト用座標で地図更新
        test_lat, test_lon = 51.504105555555554, -0.074575  # ロンドン橋
        
        info(f"テスト座標で地図更新: 緯度={test_lat}, 経度={test_lon}")
        result = map_panel.update_location(test_lat, test_lon)
        
        if result:
            info("✅ 地図パネル直接テスト成功")
        else:
            warning("⚠️ 地図パネル直接テスト失敗")
        
        # パネルを表示してテスト
        map_panel.show()
        app.processEvents()
        
        return result
        
    except Exception as e:
        error(f"❌ 地図パネル直接テストエラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def test_webengine_loading():
    """WebEngine地図読み込みテスト"""
    info("WebEngine地図読み込みテスト開始...")
    
    try:
        from PyQt5.QtCore import QUrl
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        # WebEngineビューを作成
        view = QWebEngineView()
        
        # 地図HTMLファイルを読み込み
        map_html_path = project_root / "map.html"
        if map_html_path.exists():
            info(f"地図HTMLファイルを読み込み: {map_html_path}")
            
            url = QUrl.fromLocalFile(str(map_html_path.absolute()))
            debug(f"読み込みURL: {url.toString()}")
            
            view.load(url)
            view.show()
            
            # ページ読み込み完了まで待機
            from PyQt5.QtCore import QEventLoop, QTimer
            loop = QEventLoop()
            
            def on_load_finished(ok):
                debug(f"ページ読み込み完了: {ok}")
                loop.quit()
            
            view.loadFinished.connect(on_load_finished)
            
            # タイムアウト設定
            timer = QTimer()
            timer.setSingleShot(True)
            timer.timeout.connect(loop.quit)
            timer.start(5000)  # 5秒タイムアウト
            
            loop.exec_()
            
            info("✅ WebEngine地図読み込みテスト完了")
            return True
        else:
            error(f"❌ 地図HTMLファイルが見つかりません: {map_html_path}")
            return False
        
    except Exception as e:
        error(f"❌ WebEngine地図読み込みテストエラー: {e}")
        import traceback
        debug(f"スタックトレース: {traceback.format_exc()}")
        return False

def main():
    """メイン統合テスト実行"""
    print("=" * 60)
    print("🗺️ 地図ビュー統合テストスクリプト")
    print("=" * 60)
    
    # デバッグモード有効化
    set_debug_mode(True)
    
    # 各テストを実行
    tests = [
        ("地図パネル直接テスト", test_map_panel_direct),
        ("WebEngine地図読み込みテスト", test_webengine_loading),
        ("メインウィンドウ統合テスト", test_main_window_map_integration),
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
    print("🔍 統合テスト結果まとめ")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ 正常" if result else "❌ 問題あり"
        print(f"{status} {test_name}")

if __name__ == "__main__":
    main()
