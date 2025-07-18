#!/usr/bin/env python3
"""
アドレスバー親子関係修正の検証スクリプト

修正が正常に動作しているかを確認します。
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from ui.controls.address_bar import IntegratedAddressBar

def main():
    app = QApplication(sys.argv)
    
    # メインウィンドウを作成
    main_window = QMainWindow()
    main_window.setWindowTitle("アドレスバー修正検証")
    main_window.resize(800, 600)
    
    # 中央ウィジェットとレイアウト
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    
    # アドレスバーを作成（親ウィンドウを明示的に設定）
    address_bar = IntegratedAddressBar(parent=central_widget)
    layout.addWidget(address_bar)
    
    main_window.setCentralWidget(central_widget)
    
    # 検証項目
    print("=== アドレスバー親子関係検証 ===")
    
    # 1. アドレスバーの親ウィンドウ確認
    address_bar_parent = address_bar.parent()
    print(f"✓ アドレスバーの親: {type(address_bar_parent).__name__}")
    
    # 2. ウィンドウフラグ確認
    window_flags = address_bar.windowFlags()
    is_window = bool(window_flags & Qt.WindowType.Window)
    print(f"✓ 独立ウィンドウフラグ: {is_window} (False であるべき)")
    
    # 3. 補完機能の親子関係確認
    if hasattr(address_bar, 'text_handler') and hasattr(address_bar.text_handler, 'completer'):
        completer = address_bar.text_handler.completer
        if completer and completer.popup():
            popup_parent = completer.popup().parent()
            print(f"✓ 補完ポップアップの親: {type(popup_parent).__name__}")
            
            popup_flags = completer.popup().windowFlags()
            popup_is_window = bool(popup_flags & Qt.WindowType.Window)
            print(f"✓ 補完ポップアップ独立ウィンドウフラグ: {popup_is_window}")
    
    # 結果判定
    if not is_window and address_bar_parent is not None:
        print("\n🎉 修正成功: アドレスバーは適切に親ウィンドウに関連付けられています")
    else:
        print("\n❌ 修正未完了: アドレスバーの親子関係に問題があります")
    
    main_window.show()
    print("\n検証完了。ウィンドウを閉じてください...")
    
    return app.exec_()

if __name__ == "__main__":
    sys.exit(main())
