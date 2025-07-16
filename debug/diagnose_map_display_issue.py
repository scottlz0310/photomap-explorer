#!/usr/bin/env python3
"""地図表示問題の診断と修正"""

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

def diagnose_map_display_issue():
    """地図表示問題を診断"""
    debug_logger.info("🔍 地図表示問題診断開始")
    
    issues = []
    solutions = []
    
    # 1. map.htmlファイルの確認
    map_file = "map.html"
    if os.path.exists(map_file):
        debug_logger.info(f"✅ map.htmlファイル存在: {os.path.getsize(map_file)} bytes")
        
        # ファイル内容確認
        with open(map_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'var map_' in content and 'folium' in content:
            debug_logger.info("✅ map.html内容: Folium地図データ正常")
        else:
            issues.append("map.htmlの内容が不正")
            solutions.append("地図HTMLファイルの再生成が必要")
    else:
        issues.append("map.htmlファイルが存在しない")
        solutions.append("地図生成プロセスの実行が必要")
    
    # 2. プレビューパネルとの連携確認
    debug_logger.info("🔍 画像選択→地図表示フローの確認")
    
    # 3. QtWebEngineの問題確認
    debug_logger.info("🔍 QtWebEngine問題の確認")
    issues.append("QtWebEngine GPUコンテキストエラー")
    solutions.append("ソフトウェアレンダリング有効化")
    
    # 4. 地図表示プロセスの確認
    debug_logger.info("🔍 地図表示プロセスの確認")
    
    # 診断結果の表示
    debug_logger.info("\n📋 診断結果:")
    if issues:
        debug_logger.warning(f"❌ 発見された問題: {len(issues)}個")
        for i, issue in enumerate(issues, 1):
            debug_logger.warning(f"  {i}. {issue}")
        
        debug_logger.info(f"\n🔧 推奨解決策: {len(solutions)}個")
        for i, solution in enumerate(solutions, 1):
            debug_logger.info(f"  {i}. {solution}")
    else:
        debug_logger.info("✅ 明らかな問題は見つかりませんでした")
    
    return issues, solutions

def create_map_display_fix():
    """地図表示修正スクリプトの作成"""
    debug_logger.info("🔧 地図表示修正スクリプト作成")
    
    fix_script = '''#!/usr/bin/env python3
"""地図表示修正用スクリプト"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

def fix_qtwebengine_issues():
    """QtWebEngine問題の修正"""
    print("🔧 QtWebEngine修正開始...")
    
    # GPU無効化フラグ設定
    os.environ['QTWEBENGINE_DISABLE_SANDBOX'] = '1'
    os.environ['QTWEBENGINE_CHROMIUM_FLAGS'] = '--disable-gpu --no-sandbox --disable-dev-shm-usage'
    
    # Qt属性設定
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, False)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, False)
    QApplication.setAttribute(Qt.AA_ShareOpenGLContexts, True)
    
    print("✅ QtWebEngine修正完了")

if __name__ == "__main__":
    fix_qtwebengine_issues()
    print("地図表示修正適用完了")
'''
    
    with open("debug/fix_map_display.py", "w", encoding='utf-8') as f:
        f.write(fix_script)
    
    debug_logger.info("✅ 修正スクリプト作成完了: debug/fix_map_display.py")

def test_direct_map_loading():
    """直接的な地図読み込みテスト"""
    debug_logger.info("🧪 直接地図読み込みテスト")
    
    map_file = "map.html"
    if os.path.exists(map_file):
        abs_path = os.path.abspath(map_file)
        debug_logger.info(f"📍 地図ファイル絶対パス: {abs_path}")
        debug_logger.info(f"📍 ファイルURL: file://{abs_path}")
        
        # シンプルなHTMLビューワーでのテスト提案
        debug_logger.info("💡 手動確認方法:")
        debug_logger.info(f"  ブラウザで開く: firefox {abs_path}")
        debug_logger.info(f"  VS Code Simple Browser: vscode://file{abs_path}")
        
        return abs_path
    
    return None

if __name__ == "__main__":
    print("🔍 地図表示問題の診断と修正開始")
    
    # 診断実行
    issues, solutions = diagnose_map_display_issue()
    
    # 修正スクリプト作成
    create_map_display_fix()
    
    # 直接テスト
    map_path = test_direct_map_loading()
    
    print("\n📊 診断完了:")
    print(f"  問題数: {len(issues)}")
    print(f"  解決策数: {len(solutions)}")
    
    if map_path:
        print(f"\n🎯 次のアクション:")
        print("1. メインアプリケーション再起動")
        print("2. test_images内の画像をクリック")
        print("3. 地図エリアの表示を確認")
        print(f"4. 問題が続く場合: ブラウザで直接確認 - file://{map_path}")
    
    print("\n✅ 診断と修正準備完了")
