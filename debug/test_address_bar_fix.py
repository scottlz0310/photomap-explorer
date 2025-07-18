#!/usr/bin/env python3
"""
アドレスバー問題の修正確認スクリプト

修正したアドレスバーが正常に動作するかテストします。
"""

import sys
import logging
import os
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

def setup_debug_logging():
    """デバッグ用のロガー設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def test_fixed_address_bar():
    """修正されたアドレスバーをテスト"""
    logger = logging.getLogger(__name__)
    logger.debug("=== 修正されたアドレスバーのテスト開始 ===")
    
    try:
        # QApplicationインスタンス作成
        app = QApplication([])
        
        # 修正されたcreate_controls関数のテスト
        logger.debug("=== 修正されたcreate_controls関数テスト ===")
        from ui.controls import create_controls
        
        def dummy_address_callback(path):
            logger.debug(f"アドレス変更: {path}")
        
        def dummy_parent_callback():
            logger.debug("親フォルダボタンクリック")
        
        # 関数を呼び出し
        controls_widget, address_bar, parent_button = create_controls(
            dummy_address_callback, 
            dummy_parent_callback
        )
        
        # 基本情報出力
        logger.info(f"controls_widget: {type(controls_widget).__name__}")
        logger.info(f"address_bar: {type(address_bar).__name__}")
        logger.info(f"parent_button: {type(parent_button).__name__}")
        
        # 親子関係チェック
        if address_bar:
            address_bar_parent = address_bar.parent()
            logger.info(f"address_bar.parent(): {type(address_bar_parent).__name__ if address_bar_parent else 'None'}")
            logger.info(f"controls_widget == address_bar.parent(): {controls_widget == address_bar_parent}")
            
            # ウィンドウフラグのチェック
            if hasattr(address_bar, 'windowFlags'):
                flags = address_bar.windowFlags()
                logger.info(f"address_bar windowFlags: {flags}")
                is_independent = bool(flags & Qt.WindowType.Window)
                logger.info(f"独立ウィンドウか: {is_independent}")
                
                if not is_independent:
                    logger.info("✅ 修正成功: アドレスバーは独立ウィンドウではありません")
                else:
                    logger.warning("❌ 修正失敗: アドレスバーがまだ独立ウィンドウです")
        
        # テキスト入力テスト
        logger.debug("=== テキスト入力テスト ===")
        if hasattr(address_bar, 'address_bar_core') and address_bar.address_bar_core:
            core = address_bar.address_bar_core
            if hasattr(core, 'text_edit') and core.text_edit:
                text_edit = core.text_edit
                
                # 補完機能のテスト
                if hasattr(text_edit, 'completer') and text_edit.completer():
                    completer = text_edit.completer()
                    popup = completer.popup()
                    if popup:
                        popup_parent = popup.parent()
                        logger.info(f"補完ポップアップの親: {type(popup_parent).__name__ if popup_parent else 'None'}")
                        
                        popup_flags = popup.windowFlags()
                        popup_is_independent = bool(popup_flags & Qt.WindowType.Window)
                        logger.info(f"補完ポップアップが独立ウィンドウか: {popup_is_independent}")
                        
                        if not popup_is_independent:
                            logger.info("✅ 修正成功: 補完ポップアップは独立ウィンドウではありません")
                        else:
                            logger.warning("❌ 修正失敗: 補完ポップアップがまだ独立ウィンドウです")
        
        # 実際の表示テスト
        logger.debug("=== 実際の表示テスト ===")
        controls_widget.show()
        app.processEvents()
        
        # 編集モードのテスト
        if hasattr(address_bar, 'address_bar_core'):
            core = address_bar.address_bar_core
            if hasattr(core, '_toggle_edit_mode'):
                logger.debug("編集モードに切り替え")
                core._toggle_edit_mode()
                app.processEvents()
                
                # 編集モードでの状態確認
                if hasattr(core, 'text_edit') and core.text_edit:
                    text_edit = core.text_edit
                    logger.info(f"編集モード時のtext_edit表示状態: {text_edit.isVisible()}")
                    logger.info(f"編集モード時のtext_edit親: {type(text_edit.parent()).__name__ if text_edit.parent() else 'None'}")
        
        # 少し待機してから終了
        import time
        time.sleep(1)
        
        logger.info("=== テスト完了 ===")
        app.quit()
        
    except Exception as e:
        logger.error(f"テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_debug_logging()
    test_fixed_address_bar()
