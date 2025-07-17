#!/usr/bin/env python3
"""
デバッグスクリプト: パネル表示問題の調査
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

def debug_panel_hierarchy():
    """パネル階層構造をデバッグ"""
    logger = logging.getLogger(__name__)
    logger.debug("パネル階層デバッグ開始")
    
    try:
        # Qt環境設定
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        from PyQt5.QtWidgets import QApplication
        app = QApplication([])
        
        # メインウィンドウの作成
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        window = RefactoredFunctionalMainWindow()
        
        # ウィジェット階層の分析
        logger.debug("=== メインウィンドウ構造分析 ===")
        logger.debug(f"ウィンドウサイズ: {window.size()}")
        logger.debug(f"中央ウィジェット: {window.centralWidget()}")
        
        if window.centralWidget():
            central = window.centralWidget()
            logger.debug(f"中央ウィジェットタイプ: {type(central).__name__}")
            logger.debug(f"中央ウィジェットサイズ: {central.size()}")
            logger.debug(f"中央ウィジェット子要素数: {len(central.children())}")
            
            # 子ウィジェットの詳細分析
            for i, child in enumerate(central.children()):
                if hasattr(child, 'objectName'):
                    logger.debug(f"  子ウィジェット{i}: {type(child).__name__} - {child.objectName()}")
                else:
                    logger.debug(f"  子ウィジェット{i}: {type(child).__name__}")
        
        # スプリッターの分析
        logger.debug("=== スプリッター存在確認 ===")
        logger.debug(f"main_splitter属性存在: {hasattr(window, 'main_splitter')}")
        if hasattr(window, 'main_splitter'):
            logger.debug(f"main_splitter値: {window.main_splitter}")
            logger.debug(f"main_splitter真偽値: {bool(window.main_splitter)}")
        
        if hasattr(window, 'main_splitter'):
            logger.debug("=== メインスプリッター分析 ===")
            splitter = window.main_splitter
            logger.debug(f"スプリッタータイプ: {type(splitter).__name__}")
            logger.debug(f"スプリッターサイズ: {splitter.size()}")
            logger.debug(f"スプリッター子要素数: {splitter.count()}")
            logger.debug(f"スプリッターサイズ設定: {splitter.sizes()}")
            
            for i in range(splitter.count()):
                widget = splitter.widget(i)
                if widget:
                    logger.debug(f"  スプリッター子{i}: {type(widget).__name__} - サイズ: {widget.size()}")
                    logger.debug(f"    可視性: {widget.isVisible()}")
                    logger.debug(f"    最小サイズ: {widget.minimumSize()}")
                    logger.debug(f"    最大サイズ: {widget.maximumSize()}")
                else:
                    logger.debug(f"  スプリッター子{i}: None")
        else:
            logger.debug("❌ main_splitterが存在しません")
        
        # 右スプリッターの分析
        if hasattr(window, 'right_splitter') and window.right_splitter:
            logger.debug("=== 右スプリッター分析 ===")
            right_splitter = window.right_splitter
            logger.debug(f"右スプリッタータイプ: {type(right_splitter).__name__}")
            logger.debug(f"右スプリッターサイズ: {right_splitter.size()}")
            logger.debug(f"右スプリッター子要素数: {right_splitter.count()}")
            
            for i in range(right_splitter.count()):
                widget = right_splitter.widget(i)
                if widget:
                    logger.debug(f"  右スプリッター子{i}: {type(widget).__name__} - サイズ: {widget.size()}")
                else:
                    logger.debug(f"  右スプリッター子{i}: None")
        
        # パネル管理クラスの分析
        logger.debug("=== パネル管理クラス分析 ===")
        if hasattr(window, 'left_panel_mgr') and window.left_panel_mgr:
            logger.debug(f"左パネル管理: {type(window.left_panel_mgr).__name__}")
            
        if hasattr(window, 'right_panel_mgr') and window.right_panel_mgr:
            logger.debug(f"右パネル管理: {type(window.right_panel_mgr).__name__}")
        
        logger.debug("パネル階層デバッグ完了")
        
    except Exception as e:
        logger.error(f"パネル階層デバッグエラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    setup_debug_logging()
    debug_panel_hierarchy()
