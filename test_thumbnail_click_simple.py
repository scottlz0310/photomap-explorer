#!/usr/bin/env python3
"""
サムネイルクリック機能の簡単なテスト
"""

import sys
import os
import time
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

# プロジェクトのrootをPythonパスに追加
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.debug_logger import info, debug, error


def test_thumbnail_click():
    """サムネイルクリック機能をテスト"""
    app = QApplication(sys.argv)
    
    try:
        info("📸 サムネイルクリック機能の簡単テスト開始")
        
        # メインウィンドウ作成
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        main_window = RefactoredFunctionalMainWindow()
        main_window.show()
        
        # フォルダ読み込み
        test_folder = "/home/hiro/Projects/photomap-explorer/test_images"
        if os.path.exists(test_folder):
            main_window.load_folder(test_folder)
            info(f"✅ フォルダ読み込み完了: {test_folder}")
            
            # UIの状態を確認
            QTimer.singleShot(1000, lambda: check_thumbnail_state(main_window))
            QTimer.singleShot(3000, app.quit)
            
            app.exec_()
        else:
            error(f"❌ テストフォルダが見つかりません: {test_folder}")
            
    except Exception as e:
        error(f"❌ テスト実行エラー: {e}")
        import traceback
        error(traceback.format_exc())


def check_thumbnail_state(main_window):
    """サムネイルの状態を確認"""
    try:
        info("🔍 サムネイル状態確認開始")
        
        if hasattr(main_window, 'left_panel_mgr') and main_window.left_panel_mgr:
            thumbnail_list = main_window.left_panel_mgr.thumbnail_list
            if thumbnail_list:
                count = thumbnail_list.count()
                info(f"📋 サムネイル数: {count}")
                
                if count > 0:
                    # 最初のサムネイルをクリックしてみる
                    info("🖱️ 最初のサムネイルをクリックテスト")
                    item = thumbnail_list.item(0)
                    if item:
                        debug(f"📸 テスト対象アイテム: {item.text()}")
                        
                        # 画像イベントハンドラを直接呼び出し
                        if hasattr(main_window, 'image_event_hdlr'):
                            image_path = item.data(32)  # Qt.UserRole
                            if image_path:
                                info(f"🔗 画像パス取得: {image_path}")
                                main_window.image_event_hdlr.on_image_selected(item)
                                info("✅ 画像選択イベント送信完了")
                            else:
                                error("❌ 画像パスが設定されていません")
                        else:
                            error("❌ image_event_hdlrがありません")
                    else:
                        error("❌ 最初のアイテムが取得できません")
                else:
                    error("❌ サムネイルが読み込まれていません")
            else:
                error("❌ thumbnail_listがNone")
        else:
            error("❌ left_panel_mgrがNone")
            
    except Exception as e:
        error(f"❌ 状態確認エラー: {e}")
        import traceback
        error(traceback.format_exc())


if __name__ == "__main__":
    test_thumbnail_click()
