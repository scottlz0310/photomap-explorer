#!/usr/bin/env python3
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
