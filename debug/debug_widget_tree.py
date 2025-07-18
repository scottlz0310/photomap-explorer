#!/usr/bin/env python3
"""
ウィジェット階層詳細分析

左パネルの入れ子構造を詳しく分析
"""

import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QListWidget

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

def setup_debug_logging():
    """デバッグ用のロガー設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def analyze_widget_children(widget, indent=0):
    """ウィジェットの子要素を再帰的に分析"""
    logger = logging.getLogger(__name__)
    indent_str = "  " * indent
    
    if widget is None:
        logger.debug(f"{indent_str}❌ None widget")
        return
    
    widget_type = type(widget).__name__
    object_name = widget.objectName() if hasattr(widget, 'objectName') else "unnamed"
    visible = widget.isVisible() if hasattr(widget, 'isVisible') else "N/A"
    
    logger.debug(f"{indent_str}📦 {widget_type} ({object_name}) - visible: {visible}")
    
    # 特殊なウィジェット情報
    if isinstance(widget, QGroupBox):
        title = widget.title() if hasattr(widget, 'title') else "No title"
        logger.debug(f"{indent_str}   📋 GroupBox title: '{title}'")
    elif isinstance(widget, QListWidget):
        count = widget.count() if hasattr(widget, 'count') else "N/A"
        logger.debug(f"{indent_str}   📝 ListWidget items: {count}")
    
    # 子要素を再帰的に分析
    try:
        children = widget.children() if hasattr(widget, 'children') else []
        logger.debug(f"{indent_str}   🔢 Children count: {len(children)}")
        
        for i, child in enumerate(children):
            if isinstance(child, QWidget):
                logger.debug(f"{indent_str}   🔸 Child {i}:")
                analyze_widget_children(child, indent + 2)
    except Exception as e:
        logger.debug(f"{indent_str}   ❌ Error analyzing children: {e}")

def main():
    """メインデバッグ関数"""
    setup_debug_logging()
    logger = logging.getLogger(__name__)
    
    app = QApplication(sys.argv)
    logger.debug("=== ウィジェット階層詳細分析開始 ===")
    
    try:
        # アプリケーションのインスタンス作成
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        window = RefactoredFunctionalMainWindow()
        
        logger.debug("=== 左パネル階層分析 ===")
        if hasattr(window, 'left_panel_manager') and window.left_panel_manager:
            left_panel = window.left_panel_manager.panel
            logger.debug(f"左パネル: {left_panel}")
            analyze_widget_children(left_panel)
        else:
            logger.debug("❌ 左パネル管理クラスが見つかりません")
        
        logger.debug("=== 右パネル階層分析 ===")
        if hasattr(window, 'right_panel_manager') and window.right_panel_manager:
            right_panel = window.right_panel_manager.panel
            logger.debug(f"右パネル: {right_panel}")
            analyze_widget_children(right_panel)
        else:
            logger.debug("❌ 右パネル管理クラスが見つかりません")
        
        logger.debug("=== フォルダ内容リスト特定分析 ===")
        if hasattr(window, 'folder_content_list'):
            folder_list = window.folder_content_list
            logger.debug(f"フォルダ内容リスト: {folder_list}")
            logger.debug(f"フォルダ内容リスト親: {folder_list.parent() if folder_list else None}")
            
            # 親の親を辿る
            current = folder_list
            level = 0
            while current and level < 5:
                parent = current.parent() if hasattr(current, 'parent') else None
                parent_type = type(parent).__name__ if parent else "None"
                logger.debug(f"  レベル{level}: {parent_type}")
                current = parent
                level += 1
        else:
            logger.debug("❌ フォルダ内容リストが見つかりません")
        
        window.show()
        logger.debug("=== ウィジェット階層詳細分析完了 ===")
        
    except Exception as e:
        logger.error(f"分析エラー: {e}")
        import traceback
        traceback.print_exc()
    
    app.quit()

if __name__ == "__main__":
    main()
