#!/usr/bin/env python3
"""地図パネルの動作確認テスト"""

import sys
import os

# プロジェクトルートを追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl
import tempfile

try:
    from utils.debug_logger import debug_logger
except ImportError:
    class FallbackLogger:
        def info(self, msg): print(f"INFO: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def debug(self, msg): print(f"DEBUG: {msg}")
    debug_logger = FallbackLogger()

def test_map_panel_functionality():
    """地図パネル機能テスト"""
    debug_logger.info("🔄 地図パネル機能テスト開始")
    
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    
    try:
        # MapPanelをインポート
        from ui.map_panel import MapPanel
        debug_logger.info("✅ MapPanelインポート成功")
        
        # MapPanelを作成
        map_panel = MapPanel()
        debug_logger.info(f"✅ MapPanel作成成功: use_webengine={map_panel.use_webengine}")
        
        # テスト用GPS座標
        test_lat, test_lon = 25.108204, 121.843948  # 台湾・九份
        
        debug_logger.info(f"📍 テスト座標: {test_lat}, {test_lon}")
        
        # update_locationテスト
        success = map_panel.update_location(test_lat, test_lon)
        debug_logger.info(f"🗺️ update_location結果: {'✅ 成功' if success else '❌ 失敗'}")
        
        # 地図ファイル確認
        map_file = f"{project_root}/map.html"
        if os.path.exists(map_file):
            file_size = os.path.getsize(map_file)
            debug_logger.info(f"✅ 地図ファイル確認: {file_size} bytes")
            
            # ファイル内容の簡易チェック
            with open(map_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if "folium" in content.lower() and "openstreetmap" in content.lower():
                    debug_logger.info("✅ 地図ファイル内容確認: Folium地図")
                else:
                    debug_logger.warning("⚠️ 地図ファイル内容が予期しない形式")
        else:
            debug_logger.error("❌ 地図ファイルが生成されていません")
        
        # QtWebEngineView確認
        if hasattr(map_panel, 'view') and map_panel.view:
            debug_logger.info(f"✅ WebEngineView確認: {type(map_panel.view).__name__}")
            
            # URLロード状況確認
            if hasattr(map_panel.view, 'url'):
                current_url = map_panel.view.url()
                debug_logger.info(f"📍 現在のURL: {current_url.toString()}")
            
            # HTML設定状況確認
            if hasattr(map_panel.view, 'page'):
                page = map_panel.view.page()
                if page:
                    debug_logger.info("✅ WebEnginePage確認")
                else:
                    debug_logger.warning("⚠️ WebEnginePageが取得できません")
        else:
            debug_logger.error("❌ WebEngineViewが取得できません")
        
        return success
        
    except Exception as e:
        debug_logger.error(f"❌ 地図パネルテストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_qtwebengine_loading():
    """QtWebEngine読み込みテスト"""
    debug_logger.info("🔄 QtWebEngine読み込みテスト開始")
    
    try:
        from PyQt5.QtWebEngineWidgets import QWebEngineView
        from PyQt5.QtWidgets import QMainWindow
        
        app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
        
        # シンプルなWebEngineViewテスト
        main_window = QMainWindow()
        web_view = QWebEngineView()
        main_window.setCentralWidget(web_view)
        
        # テスト用HTML
        test_html = """
        <html>
        <head><title>テスト地図</title></head>
        <body style="background-color: #2d2d2d; color: white; text-align: center; padding: 50px;">
            <h1>🗺️ 地図テスト</h1>
            <p>QtWebEngineが正常に動作しています</p>
        </body>
        </html>
        """
        
        web_view.setHtml(test_html)
        debug_logger.info("✅ QtWebEngine HTML設定成功")
        
        # 実際のFolium地図ファイルをテスト
        map_file = f"{project_root}/map.html"
        if os.path.exists(map_file):
            file_url = QUrl.fromLocalFile(os.path.abspath(map_file))
            web_view.load(file_url)
            debug_logger.info(f"✅ Folium地図ファイル読み込み: {file_url.toString()}")
        
        return True
        
    except Exception as e:
        debug_logger.error(f"❌ QtWebEngine読み込みエラー: {e}")
        return False

if __name__ == "__main__":
    print("🔄 地図パネル詳細テスト開始")
    
    # 基本機能テスト
    basic_success = test_qtwebengine_loading()
    
    if basic_success:
        # 地図パネル機能テスト
        panel_success = test_map_panel_functionality()
        
        if panel_success:
            print("\n✅ 地図パネル機能テスト成功")
            print("📌 確認ポイント:")
            print("1. use_webengine設定")
            print("2. 地図ファイル生成")
            print("3. QtWebEngineViewへの読み込み")
        else:
            print("\n❌ 地図パネル機能に問題があります")
    else:
        print("\n❌ QtWebEngine基本機能に問題があります")
    
    print("\n🎯 メインアプリケーションでのテスト:")
    print("1. taiwan-jiufen.jpgを選択")
    print("2. コンソール出力でupdate_location呼び出しを確認")
    print("3. 地図エリアで右クリック→「要素を検証」でHTML確認")
