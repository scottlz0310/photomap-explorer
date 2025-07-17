#!/usr/bin/env python3
"""
デバッグスクリプト: 初期化フロー調査
配置場所: debug/
作成日: 2025-07-17
"""

import sys
import logging
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def setup_debug_logging():
    """デバッグ用のロガー設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def debug_initialization_flow():
    """初期化フローをデバッグ"""
    logger = logging.getLogger(__name__)
    logger.debug("初期化フローデバッグ開始")
    
    try:
        # Qt環境設定
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        from PyQt5.QtWidgets import QApplication
        app = QApplication([])
        
        # ステップバイステップデバッグ
        logger.debug("=== MainWindowCore初期化確認 ===")
        from presentation.views.functional_main_window.main_window_core import MainWindowCore
        core_window = MainWindowCore()
        logger.debug(f"CoreWindow main_splitter: {core_window.main_splitter}")
        logger.debug(f"CoreWindow main_splitter子要素数: {core_window.main_splitter.count()}")
        
        logger.debug("=== RefactoredFunctionalMainWindow初期化確認 ===")
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        
        # 各段階での状態を記録
        logger.debug("--- 初期化前 ---")
        
        window = RefactoredFunctionalMainWindow()
        
        logger.debug("--- 初期化後 ---")
        logger.debug(f"Window main_splitter: {window.main_splitter}")
        logger.debug(f"Window main_splitter子要素数: {window.main_splitter.count()}")
        
        # 管理クラスの状態確認
        logger.debug("=== 管理クラス状態確認 ===")
        logger.debug(f"left_panel_mgr: {window.left_panel_mgr}")
        logger.debug(f"right_panel_mgr: {window.right_panel_mgr}")
        
        # setup_managersが呼ばれたかの確認
        logger.debug("=== setup_managers実行確認 ===")
        if hasattr(window, 'left_panel_manager'):
            logger.debug(f"left_panel_manager設定済み: {window.left_panel_manager}")
        else:
            logger.debug("❌ left_panel_manager未設定")
            
        if hasattr(window, 'right_panel_manager'):
            logger.debug(f"right_panel_manager設定済み: {window.right_panel_manager}")
        else:
            logger.debug("❌ right_panel_manager未設定")
        
        logger.debug("初期化フローデバッグ完了")
        
    except Exception as e:
        logger.error(f"初期化フローデバッグエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_debug_logging()
    debug_initialization_flow()
