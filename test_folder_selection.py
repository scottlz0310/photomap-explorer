#!/usr/bin/env python3
"""
フォルダ選択機能のテスト

簡単なフォルダ選択ダイアログを表示してフォルダ内容を更新する
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
            
            # 左パネルマネージャーを使用してフォルダ内容を更新
            if window.left_panel_manager:
                window.left_panel_manager.update_folder_content(folder_path)
                
                # 画像ファイルのサムネイルも更新
                image_files = window.left_panel_manager._get_image_files_from_folder(folder_path)
                window.left_panel_manager.update_thumbnails(image_files)
                
                QMessageBox.information(window, "完了", f"フォルダを読み込みました\n画像: {len(image_files)}件")
    
    # ボタンをツールバーに追加
    if hasattr(window, 'toolbar'):
        folder_btn = QPushButton("📁 フォルダ選択")
        folder_btn.clicked.connect(select_folder)
        window.toolbar.addWidget(folder_btn)
    
    window.show()
    
    # デフォルトでtest_imagesフォルダを開く
    test_folder = os.path.join(os.path.dirname(__file__), "test_images")
    if os.path.exists(test_folder):
        print(f"デフォルトフォルダを読み込み: {test_folder}")
        window.left_panel_manager.update_folder_content(test_folder)
        image_files = window.left_panel_manager._get_image_files_from_folder(test_folder)
        window.left_panel_manager.update_thumbnails(image_files)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
