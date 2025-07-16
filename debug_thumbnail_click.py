#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サムネイルクリック問題のデバッグスクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
import traceback

def test_thumbnail_click():
    """サムネイルクリック機能をテスト"""
    try:
        # デバッグロガー設定
        from utils.debug_logger import debug, info, error, warning, set_debug_mode
        set_debug_mode(True)  # デバッグモード有効化
        
        # QApplication作成
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        info("🔍 サムネイルクリック機能の詳細テスト開始")
        
        # RefactoredFunctionalMainWindowを作成
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        
        info("1. メインウィンドウ作成中...")
        main_window = RefactoredFunctionalMainWindow()
        
        info("2. メインウィンドウ表示...")
        main_window.show()
        
        info("3. イベントハンドラの状態確認...")
        if hasattr(main_window, 'image_event_hdlr') and main_window.image_event_hdlr:
            info(f"✅ image_event_hdlr: {main_window.image_event_hdlr}")
            if hasattr(main_window.image_event_hdlr, 'on_image_selected'):
                info(f"✅ on_image_selected: {main_window.image_event_hdlr.on_image_selected}")
            else:
                error("❌ on_image_selectedメソッドがありません")
        else:
            error("❌ image_event_hdlrがありません")
        
        info("4. 左パネルマネージャーの状態確認...")
        if hasattr(main_window, 'left_panel_mgr') and main_window.left_panel_mgr:
            info(f"✅ left_panel_mgr: {main_window.left_panel_mgr}")
            if hasattr(main_window.left_panel_mgr, '_show_image_in_preview'):
                info(f"✅ _show_image_in_preview: {main_window.left_panel_mgr._show_image_in_preview}")
            else:
                error("❌ _show_image_in_previewメソッドがありません")
                
            if hasattr(main_window.left_panel_mgr, 'thumbnail_list'):
                info(f"✅ thumbnail_list: {main_window.left_panel_mgr.thumbnail_list}")
            else:
                error("❌ thumbnail_listがありません")
        else:
            error("❌ left_panel_mgrがありません")
        
        info("5. プレビューパネルの状態確認...")
        if hasattr(main_window, 'preview_panel') and main_window.preview_panel:
            info(f"✅ preview_panel: {main_window.preview_panel}")
            if hasattr(main_window.preview_panel, 'display_image'):
                info(f"✅ display_image: {main_window.preview_panel.display_image}")
            else:
                error("❌ display_imageメソッドがありません")
        else:
            error("❌ preview_panelがありません")
        
        info("6. テスト画像フォルダを読み込み...")
        test_folder = "/home/hiro/Projects/photomap-explorer/test_images"
        if os.path.exists(test_folder):
            main_window.load_folder(test_folder)
            info(f"✅ テストフォルダ読み込み: {test_folder}")
            
            # FolderEventHandlerの状態確認
            info("6.1. FolderEventHandlerのコンポーネント参照確認...")
            if hasattr(main_window, 'folder_event_hdlr') and main_window.folder_event_hdlr:
                feh = main_window.folder_event_hdlr
                info(f"✅ folder_event_hdlr: {feh}")
                info(f"📋 folder_event_hdlr.thumbnail_list: {getattr(feh, 'thumbnail_list', None)}")
                info(f"📋 folder_event_hdlr.address_bar: {getattr(feh, 'address_bar', None)}")
                info(f"📋 folder_event_hdlr.folder_content_list: {getattr(feh, 'folder_content_list', None)}")
            else:
                error("❌ folder_event_hdlrがありません")
            
            # 読み込み後のサムネイルリスト状態を確認
            info("6.2. 読み込み後のサムネイルリスト状態確認...")
            if hasattr(main_window, 'left_panel_mgr') and main_window.left_panel_mgr:
                if hasattr(main_window.left_panel_mgr, 'thumbnail_list'):
                    tl = main_window.left_panel_mgr.thumbnail_list
                    debug(f"📋 thumbnail_list: {tl}")
                    if tl:
                        count = tl.count()
                        info(f"📋 サムネイル数: {count}")
                        if count == 0:
                            info("⏰ サムネイル読み込み待機中...")
                            # QApplicationのイベントを処理して更新を待つ
                            import time
                            for i in range(10):  # 最大1秒待機
                                app.processEvents()
                                time.sleep(0.1)
                                count = tl.count()
                                if count > 0:
                                    info(f"✅ サムネイル読み込み完了: {count}件")
                                    break
                    else:
                        error("❌ thumbnail_listがNone")
                else:
                    error("❌ thumbnail_list属性がありません")
            else:
                error("❌ left_panel_mgrがありません")
            
            # サムネイル数確認
            if hasattr(main_window, 'left_panel_mgr') and main_window.left_panel_mgr and hasattr(main_window.left_panel_mgr, 'thumbnail_list') and main_window.left_panel_mgr.thumbnail_list:
                count = main_window.left_panel_mgr.thumbnail_list.count()
                info(f"📋 最終サムネイル数: {count}")
                
                if count > 0:
                    info("7. サムネイルクリック仮想テスト...")
                    
                    # 最初のサムネイルを取得
                    first_item = main_window.left_panel_mgr.thumbnail_list.item(0)
                    if first_item:
                        image_path = first_item.data(Qt.ItemDataRole.UserRole)
                        info(f"📋 最初のサムネイル: {image_path}")
                        
                        # 直接on_image_selectedを呼び出し
                        if hasattr(main_window, 'image_event_hdlr') and main_window.image_event_hdlr:
                            try:
                                main_window.image_event_hdlr.on_image_selected(image_path)
                                info("✅ on_image_selected呼び出し成功")
                            except Exception as e:
                                error(f"❌ on_image_selected呼び出しエラー: {e}")
                                traceback.print_exc()
                    else:
                        error("❌ 最初のサムネイルアイテムを取得できません")
                else:
                    error("❌ サムネイルが見つかりません")
            else:
                error("❌ thumbnail_listが最終的に見つかりません")
        else:
            error(f"❌ テストフォルダが見つかりません: {test_folder}")
        
        info("\n🎯 テスト完了")
        
        # 短時間実行
        from PyQt5.QtCore import QTimer
        timer = QTimer()
        def end_test():
            info("テスト終了")
            app.quit()
        timer.timeout.connect(end_test)
        timer.start(3000)  # 3秒後に終了
        
        app.exec_()
        
        return True
        
    except Exception as e:
        from utils.debug_logger import error
        error(f"❌ テストエラー: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_thumbnail_click()
    sys.exit(0 if success else 1)
