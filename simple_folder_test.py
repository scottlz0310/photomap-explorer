#!/usr/bin/env python3
"""
シンプルなフォルダ選択テスト

アドレスバーとパネルの連動をテストする
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox

def main():
    app = QApplication(sys.argv)
    
    # メインウィンドウを作成
    from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
    window = RefactoredFunctionalMainWindow()
    
    # フォルダ選択ボタンを追加
    def select_folder():
        folder_path = QFileDialog.getExistingDirectory(window, "フォルダを選択", os.path.expanduser("~"))
        if folder_path:
            print(f"選択されたフォルダ: {folder_path}")
            
            # アドレスバーを更新
            if hasattr(window, 'address_bar_manager') and window.address_bar_manager:
                if hasattr(window.address_bar_manager, 'set_path'):
                    window.address_bar_manager.set_path(folder_path)
                elif hasattr(window.address_bar_manager, 'address_bar') and hasattr(window.address_bar_manager.address_bar, 'setText'):
                    window.address_bar_manager.address_bar.setText(folder_path)
            
            # 左パネルマネージャーを使用してフォルダ内容を更新
            if hasattr(window, 'left_panel_manager') and window.left_panel_manager:
                window.left_panel_manager.update_folder_content(folder_path)
                
                # 画像ファイルのサムネイルも更新
                image_files = window.left_panel_manager._get_image_files_from_folder(folder_path)
                window.left_panel_manager.update_thumbnails(image_files)
                
                print(f"フォルダ読み込み完了: {len(image_files)}個の画像ファイル")
    
    # ツールバーに自分でボタンを追加する
    if hasattr(window, 'central_widget'):
        # 新しいボタンを作成
        folder_btn = QPushButton("📁 フォルダ選択")
        folder_btn.clicked.connect(select_folder)
        
        # 既存のレイアウトの先頭に追加
        if hasattr(window, 'main_layout'):
            # レイアウトの最初に挿入
            window.main_layout.insertWidget(0, folder_btn)
        else:
            # ウィンドウに直接追加
            folder_btn.setParent(window)
            folder_btn.move(10, 10)
            folder_btn.show()
    
    window.show()
    
    # デフォルトでtest_imagesフォルダを開く
    test_folder = os.path.join(os.path.dirname(__file__), "test_images")
    if os.path.exists(test_folder):
        print(f"デフォルトフォルダを読み込み: {test_folder}")
        if hasattr(window, 'left_panel_manager') and window.left_panel_manager:
            window.left_panel_manager.update_folder_content(test_folder)
            image_files = window.left_panel_manager._get_image_files_from_folder(test_folder)
            window.left_panel_manager.update_thumbnails(image_files)
            print(f"デフォルト読み込み完了: {len(image_files)}個の画像")
        
        # アドレスバーも更新
        if hasattr(window, 'address_bar_manager') and window.address_bar_manager:
            if hasattr(window.address_bar_manager, 'set_path'):
                window.address_bar_manager.set_path(test_folder)
            elif hasattr(window.address_bar_manager, 'address_bar') and hasattr(window.address_bar_manager.address_bar, 'setText'):
                window.address_bar_manager.address_bar.setText(test_folder)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
