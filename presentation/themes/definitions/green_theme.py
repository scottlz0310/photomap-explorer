"""
グリーンテーマ定義モジュール

このモジュールは自然なグリーンベースのテーマを提供します。
"""

from typing import Dict, Any
import logging


def create_green_theme() -> Dict[str, Any]:
    """
    グリーンテーマ定義を作成
    
    Returns:
        Dict[str, Any]: グリーンテーマの完全な定義
    """
    try:
        return {
            "name": "green",
            "display_name": "グリーンモード",
            "description": "自然なグリーンベーステーマ",
            "version": "2.2.0",
            "author": "PhotoMap Explorer Team",
            "colors": _create_green_colors(),
            "styles": _create_green_styles()
        }
        
    except Exception as e:
        logging.error(f"グリーンテーマ作成エラー: {e}")
        return _create_fallback_green_theme()


def _create_green_colors() -> Dict[str, str]:
    """グリーンテーマのカラーパレットを作成"""
    return {
        # 基本色
        "background": "#1a2e1a",
        "foreground": "#ffffff",
        "primary": "#4ade80",
        "secondary": "#22543d",
        "accent": "#38a169",
        
        # UI要素色
        "border": "#2d5016",
        "border_light": "#3d6026",
        "border_dark": "#1d4006",
        
        # 状態色
        "success": "#48bb78",
        "warning": "#ed8936",
        "error": "#f56565",
        "info": "#4ade80",
        
        # パネル色
        "panel_bg": "#1a2e1a",
        "panel_border": "#2d5016",
        "panel_header": "#22543d",
        
        # ボタン色
        "button_bg": "#38a169",
        "button_bg_hover": "#2f855a",
        "button_bg_pressed": "#22543d",
        "button_text": "#ffffff",
        
        # 入力フィールド色
        "input_bg": "#2d5016",
        "input_border": "#3d6026",
        "input_border_focus": "#4ade80",
        "input_text": "#ffffff",
        "input_placeholder": "#a0aec0",
        
        # リスト色
        "list_bg": "#1a2e1a",
        "list_item_bg": "#2d5016",
        "list_item_bg_hover": "#38a169",
        "list_item_bg_selected": "#4ade80",
        "list_item_text": "#ffffff",
        
        # ツールバー色
        "toolbar_bg": "#22543d",
        "toolbar_border": "#3d6026",
        "toolbar_text": "#ffffff",
        
        # マップ色
        "map_bg": "#1a2e1a",
        "map_border": "#2d5016",
        
        # スクロールバー色
        "scrollbar_bg": "#2d5016",
        "scrollbar_handle": "#4ade80",
        "scrollbar_handle_hover": "#38a169"
    }


def _create_green_styles() -> Dict[str, str]:
    """グリーンテーマのスタイル定義を作成"""
    colors = _create_green_colors()
    
    return {
        "main_window": f"""
            QMainWindow {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
        """,
        
        "QMainWindow": f"""
            QMainWindow {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
        """,
        
        "QWidget": f"""
            QWidget {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
        """,
        
        "QPushButton": f"""
            QPushButton {{
                background-color: {colors['button_bg']};
                color: {colors['button_text']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors['button_bg_hover']};
                border-color: {colors['primary']};
            }}
            QPushButton:pressed {{
                background-color: {colors['button_bg_pressed']};
            }}
            QPushButton:disabled {{
                background-color: {colors['secondary']};
                color: {colors['input_placeholder']};
            }}
        """,
        
        "QLineEdit": f"""
            QLineEdit {{
                background-color: {colors['input_bg']};
                color: {colors['input_text']};
                border: 2px solid {colors['input_border']};
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }}
            QLineEdit:focus {{
                border-color: {colors['input_border_focus']};
                background-color: {colors['panel_bg']};
            }}
            QLineEdit::placeholder {{
                color: {colors['input_placeholder']};
            }}
        """,
        
        "QListWidget": f"""
            QListWidget {{
                background-color: {colors['list_bg']};
                color: {colors['list_item_text']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                outline: none;
            }}
            QListWidget::item {{
                background-color: {colors['list_item_bg']};
                border: none;
                padding: 8px;
                margin: 2px;
                border-radius: 4px;
            }}
            QListWidget::item:hover {{
                background-color: {colors['list_item_bg_hover']};
            }}
            QListWidget::item:selected {{
                background-color: {colors['list_item_bg_selected']};
            }}
        """,
        
        "group_box": f"""
            QGroupBox {{
                background-color: {colors['panel_bg']};
                color: {colors['foreground']};
                border: 2px solid {colors['border']};
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                font-weight: 600;
            }}
            QGroupBox::title {{
                color: {colors['primary']};
                font-weight: 700;
                padding: 0 8px;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
            }}
        """,
        
        "QSplitter": f"""
            QSplitter::handle {{
                background-color: {colors['border']};
                border: 1px solid {colors['border_dark']};
            }}
            QSplitter::handle:horizontal {{
                width: 6px;
            }}
            QSplitter::handle:vertical {{
                height: 6px;
            }}
            QSplitter::handle:hover {{
                background-color: {colors['primary']};
            }}
        """,
        
        "QStatusBar": f"""
            QStatusBar {{
                background-color: {colors['toolbar_bg']};
                color: {colors['toolbar_text']};
                border-top: 1px solid {colors['toolbar_border']};
                padding: 4px;
            }}
        """,
        
        "QScrollBar:vertical": f"""
            QScrollBar:vertical {{
                background-color: {colors['scrollbar_bg']};
                width: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:vertical {{
                background-color: {colors['scrollbar_handle']};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {colors['scrollbar_handle_hover']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """,
        
        "QScrollBar:horizontal": f"""
            QScrollBar:horizontal {{
                background-color: {colors['scrollbar_bg']};
                height: 12px;
                border-radius: 6px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {colors['scrollbar_handle']};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {colors['scrollbar_handle_hover']};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """,
        
        "QLabel": f"""
            QLabel {{
                color: {colors['foreground']};
                background-color: transparent;
            }}
        """,
        
        "button": f"""
            QPushButton {{
                background-color: {colors['button_bg']};
                color: {colors['button_text']};
                border: 1px solid {colors['border']};
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {colors['button_bg_hover']};
                border-color: {colors['primary']};
            }}
            QPushButton:pressed {{
                background-color: {colors['button_bg_pressed']};
            }}
            QPushButton:disabled {{
                background-color: {colors['secondary']};
                color: {colors['input_placeholder']};
            }}
        """,
        
        "main": f"""
            QMainWindow {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
            QWidget {{
                background-color: {colors['background']};
                color: {colors['foreground']};
            }}
        """
    }


def _create_fallback_green_theme() -> Dict[str, Any]:
    """フォールバック用の簡易グリーンテーマ"""
    return {
        "name": "green",
        "display_name": "グリーンモード（簡易）",
        "description": "フォールバック用グリーンテーマ",
        "version": "2.2.0",
        "author": "PhotoMap Explorer Team",
        "colors": {
            "background": "#1a2e1a",
            "foreground": "#ffffff",
            "primary": "#4ade80",
            "secondary": "#22543d"
        },
        "styles": {
            "QWidget": "QWidget { background-color: #1a2e1a; color: #ffffff; }"
        }
    }
