#!/usr/bin/env python3
"""
マップ表示問題のデバッグスクリプト
"""

import sys
import os
import traceback

def debug_map_issue():
    """マップ表示の問題をデバッグ"""
    print("=== マップ表示デバッグ開始 ===")
    
    # テスト用のGPS座標
    test_lat, test_lon = 35.6762, 139.6503  # 東京駅
    
    try:
        # 1. 必要なライブラリのインポートテスト
        print("1. ライブラリのインポートテスト")
        import folium
        print(f"  ✓ folium インポート成功: {folium.__version__}")
        
        from logic.image_utils import generate_map_html
        print("  ✓ generate_map_html インポート成功")
        
        # 2. HTMLコンテンツ生成テスト
        print("\n2. HTMLコンテンツ生成テスト")
        html_content = generate_map_html(test_lat, test_lon)
        print(f"  ✓ HTML生成成功: {len(html_content)} characters")
        print(f"  最初の200文字: {html_content[:200]}...")
        
        # 3. PyQt5コンポーネントのテスト
        print("\n3. PyQt5コンポーネントのテスト")
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        
        # アプリケーションインスタンスを作成（まだ存在しない場合）
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # QWebEngineViewの作成
        web_view = QWebEngineView()
        print("  ✓ QWebEngineView作成成功")
        
        # HTMLの設定
        web_view.setHtml(html_content)
        print("  ✓ setHtml実行成功")
        
        # 4. MapPanelのテスト
        print("\n4. MapPanelのテスト")
        from ui.map_panel import MapPanel
        
        map_panel = MapPanel()
        print("  ✓ MapPanel作成成功")
        
        # update_locationメソッドのテスト
        result = map_panel.update_location(test_lat, test_lon)
        print(f"  update_location結果: {result}")
        
        # 5. 実際のUI表示テスト
        print("\n5. UI表示テスト")
        from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget
        
        main_window = QMainWindow()
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(map_panel)
        
        main_window.setCentralWidget(central_widget)
        main_window.setWindowTitle("マップテスト")
        main_window.resize(800, 600)
        
        print("  ✓ テストウィンドウ準備完了")
        
        # ウィンドウを表示
        main_window.show()
        print("  ✓ ウィンドウ表示中...")
        
        # 短時間実行してからクローズ
        from PyQt5.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(lambda: (print("  ✓ テスト完了"), app.quit()))
        timer.start(3000)  # 3秒後に終了
        
        app.exec_()
        
        print("\n=== マップ表示デバッグ成功 ===")
        return True
        
    except Exception as e:
        print(f"\n❌ デバッグ中にエラーが発生: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = debug_map_issue()
    sys.exit(0 if success else 1)
