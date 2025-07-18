#!/usr/bin/env python3
"""
アドレスバーの親子関係デバッグスクリプト

アドレスバーが子ウィンドウに表示される問題を調査し、修正方法を特定する
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

def debug_address_bar_parent():
    """アドレスバーの親子関係をデバッグ"""
    logger = logging.getLogger(__name__)
    logger.debug("=== アドレスバー親子関係デバッグ開始 ===")
    
    try:
        # QApplicationインスタンス作成
        app = QApplication([])
        
        # 1. create_controls関数のテスト
        logger.debug("=== create_controls関数テスト ===")
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
                logger.info(f"独立ウィンドウか: {bool(flags & Qt.WindowType.Window)}")
        
        if parent_button:
            parent_button_parent = parent_button.parent()
            logger.info(f"parent_button.parent(): {type(parent_button_parent).__name__ if parent_button_parent else 'None'}")
            logger.info(f"controls_widget == parent_button.parent(): {controls_widget == parent_button_parent}")
        
        # 2. メインウィンドウでの統合テスト
        logger.debug("=== メインウィンドウ統合テスト ===")
        try:
            from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
            
            main_window = RefactoredFunctionalMainWindow()
            logger.info(f"メインウィンドウ作成: {type(main_window).__name__}")
            
            # controls_widgetの確認
            if hasattr(main_window, 'controls_widget'):
                main_controls = main_window.controls_widget
                logger.info(f"メインウィンドウのcontrols_widget: {type(main_controls).__name__}")
                logger.info(f"controls_widget.parent(): {type(main_controls.parent()).__name__ if main_controls.parent() else 'None'}")
            
            # address_barの確認
            if hasattr(main_window, 'address_bar'):
                main_address_bar = main_window.address_bar
                logger.info(f"メインウィンドウのaddress_bar: {type(main_address_bar).__name__}")
                logger.info(f"address_bar.parent(): {type(main_address_bar.parent()).__name__ if main_address_bar.parent() else 'None'}")
                
                # 問題のチェック
                if hasattr(main_address_bar, 'windowFlags'):
                    flags = main_address_bar.windowFlags()
                    is_independent = bool(flags & Qt.WindowType.Window)
                    logger.warning(f"メインのアドレスバーが独立ウィンドウ: {is_independent}")
                    if is_independent:
                        logger.error("問題発見: メインウィンドウのアドレスバーが独立ウィンドウとして設定されています!")
            
            # アドレスバーマネージャーの確認
            if hasattr(main_window, 'address_bar_mgr'):
                mgr = main_window.address_bar_mgr
                logger.info(f"AddressBarManager: {mgr}")
                
                if hasattr(mgr, 'address_bar') and mgr.address_bar:
                    mgr_address_bar = mgr.address_bar
                    logger.info(f"マネージャーのアドレスバー: {type(mgr_address_bar).__name__}")
                    logger.info(f"マネージャーアドレスバー.parent(): {type(mgr_address_bar.parent()).__name__ if mgr_address_bar.parent() else 'None'}")
                    
                    # ウィンドウフラグのチェック
                    if hasattr(mgr_address_bar, 'windowFlags'):
                        flags = mgr_address_bar.windowFlags()
                        is_independent = bool(flags & Qt.WindowType.Window)
                        logger.warning(f"マネージャーのアドレスバーが独立ウィンドウ: {is_independent}")
                        if is_independent:
                            logger.error("問題発見: マネージャーのアドレスバーが独立ウィンドウとして設定されています!")
            
            # ウィンドウ表示テスト
            main_window.show()
            app.processEvents()
            
            logger.info("表示テスト完了")
            
        except ImportError as e:
            logger.warning(f"メインウィンドウのインポートエラー: {e}")
        except Exception as e:
            logger.error(f"メインウィンドウテストエラー: {e}")
        
        # 問題の修正提案
        logger.info("=== 修正提案 ===")
        logger.info("1. create_controls関数でアドレスバーの親を正しく設定")
        logger.info("2. アドレスバーのWindowフラグを削除")
        logger.info("3. 適切な親ウィジェットの設定確認")
        
        app.quit()
        
    except Exception as e:
        logger.error(f"デバッグ実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_debug_logging()
    debug_address_bar_parent()
            
            if address_bar_parent:
                logger.debug(f"address_bar.parent() type: {type(address_bar_parent)}")
            else:
                logger.warning("アドレスバーに親ウィジェットが設定されていません！")
        
        # 親ボタンの親ウィジェット確認
        if parent_button:
            parent_button_parent = parent_button.parent()
            logger.debug(f"parent_button.parent(): {parent_button_parent}")
            logger.debug(f"parent_button.parent() == controls_widget: {parent_button_parent == controls_widget}")
            
            if parent_button_parent:
                logger.debug(f"parent_button.parent() type: {type(parent_button_parent)}")
            else:
                logger.warning("親ボタンに親ウィジェットが設定されていません！")
        
        # controls_widgetの子ウィジェット確認
        if controls_widget:
            children = controls_widget.children()
            logger.debug(f"controls_widget.children(): {children}")
            logger.debug(f"controls_widget children count: {len(children)}")
            
            # 子ウィジェットの詳細確認
            for i, child in enumerate(children):
                logger.debug(f"Child {i}: {child} (type: {type(child)})")
        
        # アドレスバーの内部構造確認
        if address_bar:
            logger.debug("=== アドレスバー内部構造確認 ===")
            logger.debug(f"address_bar hasattr 'address_bar_core': {hasattr(address_bar, 'address_bar_core')}")
            
            if hasattr(address_bar, 'address_bar_core'):
                core = address_bar.address_bar_core
                logger.debug(f"address_bar_core: {core}")
                if core:
                    core_parent = core.parent()
                    logger.debug(f"address_bar_core.parent(): {core_parent}")
                    logger.debug(f"address_bar_core.parent() == address_bar: {core_parent == address_bar}")
        
        logger.debug("=== アドレスバー親子関係デバッグ完了 ===")
        
    except Exception as e:
        logger.error(f"デバッグ実行エラー: {e}", exc_info=True)

if __name__ == "__main__":
    setup_debug_logging()
    debug_address_bar_parent()
