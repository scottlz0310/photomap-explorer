#!/usr/bin/env python3
"""
パネル状態の詳細診断

各パネルの初期化状態を詳しく確認する
"""

import sys
import os
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    
    # メインウィンドウを作成
    from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
    window = RefactoredFunctionalMainWindow()
    
    print("=== メインウィンドウ診断 ===")
    print(f"ウィンドウクラス: {type(window).__name__}")
    print(f"ウィンドウタイトル: {window.windowTitle()}")
    
    print("\n=== 管理クラス診断 ===")
    print(f"left_panel_manager: {hasattr(window, 'left_panel_manager')} -> {window.left_panel_manager if hasattr(window, 'left_panel_manager') else 'None'}")
    print(f"right_panel_manager: {hasattr(window, 'right_panel_manager')} -> {window.right_panel_manager if hasattr(window, 'right_panel_manager') else 'None'}")
    print(f"address_bar_manager: {hasattr(window, 'address_bar_manager')} -> {window.address_bar_manager if hasattr(window, 'address_bar_manager') else 'None'}")
    
    print("\n=== 左パネル詳細 ===")
    if hasattr(window, 'left_panel_manager') and window.left_panel_manager:
        lpm = window.left_panel_manager
        print(f"panel: {hasattr(lpm, 'panel')} -> {lpm.panel if hasattr(lpm, 'panel') else 'None'}")
        print(f"folder_content_list: {hasattr(lpm, 'folder_content_list')} -> {lpm.folder_content_list if hasattr(lpm, 'folder_content_list') else 'None'}")
        print(f"thumbnail_list: {hasattr(lpm, 'thumbnail_list')} -> {lpm.thumbnail_list if hasattr(lpm, 'thumbnail_list') else 'None'}")
        print(f"status_info: {hasattr(lpm, 'status_info')} -> {lpm.status_info if hasattr(lpm, 'status_info') else 'None'}")
    
    print("\n=== メインウィンドウパネル参照 ===")
    print(f"window.folder_content_list: {hasattr(window, 'folder_content_list')} -> {window.folder_content_list if hasattr(window, 'folder_content_list') else 'None'}")
    print(f"window.thumbnail_list: {hasattr(window, 'thumbnail_list')} -> {window.thumbnail_list if hasattr(window, 'thumbnail_list') else 'None'}")
    print(f"window.preview_panel: {hasattr(window, 'preview_panel')} -> {window.preview_panel if hasattr(window, 'preview_panel') else 'None'}")
    print(f"window.map_panel: {hasattr(window, 'map_panel')} -> {window.map_panel if hasattr(window, 'map_panel') else 'None'}")
    
    print("\n=== 右パネル詳細 ===")
    if hasattr(window, 'right_panel_manager') and window.right_panel_manager:
        rpm = window.right_panel_manager
        print(f"panel: {hasattr(rpm, 'panel')} -> {rpm.panel if hasattr(rpm, 'panel') else 'None'}")
        print(f"right_splitter: {hasattr(rpm, 'right_splitter')} -> {rpm.right_splitter if hasattr(rpm, 'right_splitter') else 'None'}")
        print(f"preview_panel: {hasattr(rpm, 'preview_panel')} -> {rpm.preview_panel if hasattr(rpm, 'preview_panel') else 'None'}")
        print(f"map_panel: {hasattr(rpm, 'map_panel')} -> {rpm.map_panel if hasattr(rpm, 'map_panel') else 'None'}")
    
    # 実際に表示してUIを確認
    window.show()
    
    print("\n=== 表示後再診断 ===")
    print("ウィンドウが表示されました。UIを確認してください。")
    print("左パネル: フォルダ内容、サムネイル、ステータス情報のセクションが見えますか？")
    print("右パネル: プレビューとマップのセクションが見えますか？")
    
    # 少し待ってからテスト実行
    from PyQt5.QtCore import QTimer
    def delayed_test():
        print("\n=== 遅延テスト実行 ===")
        test_folder = "/home/hiro/Projects/photomap-explorer/test_images"
        if os.path.exists(test_folder):
            print(f"テストフォルダ: {test_folder}")
            if hasattr(window, 'left_panel_manager') and window.left_panel_manager:
                try:
                    window.left_panel_manager.update_folder_content(test_folder)
                    image_files = window.left_panel_manager._get_image_files_from_folder(test_folder)
                    window.left_panel_manager.update_thumbnails(image_files)
                    print(f"✅ 遅延テスト成功: {len(image_files)}個の画像")
                except Exception as e:
                    print(f"❌ 遅延テストエラー: {e}")
    
    # 2秒後にテスト実行
    QTimer.singleShot(2000, delayed_test)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
