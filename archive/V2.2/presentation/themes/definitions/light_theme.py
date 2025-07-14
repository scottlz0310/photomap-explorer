"""
ライトテーマ定義モジュール

このモジュールは presentation/themes/theme_manager.py から分離された
ライトテーマの定義を提供します。
"""

from typing import Dict, Any
import logging


def create_light_theme() -> Dict[str, Any]:
    """
    ライトテーマ定義を作成
    
    Returns:
        Dict[str, Any]: ライトテーマの完全な定義
    """
    try:
        return {
            "name": "light",
            "display_name": "ライトモード",
            "description": "明るい背景の標準テーマ",
            "version": "2.2.0",
            "author": "PhotoMap Explorer Team",
            "colors": _create_light_colors(),
            "styles": _create_light_styles()
        }
        
    except Exception as e:
        logging.error(f"ライトテーマ作成エラー: {e}")
        return _create_fallback_light_theme()


def _create_light_colors() -> Dict[str, str]:
    """ライトテーマのカラーパレットを作成"""
    return {
        # 基本色
        "background": "#ffffff",
        "foreground": "#000000",
        "primary": "#007acc",
        "secondary": "#f8f8f8",
        "accent": "#0078d4",
        
        # UI要素色
        "border": "#ddd",
        "border_light": "#e8e8e8",
        "border_dark": "#ccc",
        
        # 状態色
        "error": "#e74c3c",
        "warning": "#f39c12", 
        "success": "#27ae60",
        "info": "#3498db",
        "muted": "#666",
        
        # インタラクション色
        "hover": "#e6f3ff",
        "selection": "#cce8ff",
        "focus": "#0078d4",
        "active": "#005a9e",
        
        # ボタン色
        "button_bg": "#f0f0f0",
        "button_hover": "#e0e0e0",
        "button_pressed": "#d0d0d0",
        "button_disabled": "#f8f8f8",
        
        # 入力フィールド色
        "input_bg": "#ffffff",
        "input_border": "#ccc",
        "input_focus_border": "#0078d4",
        "input_error_border": "#e74c3c",
        
        # パネル・グループ色
        "group_bg": "#f8f8f8",
        "panel_bg": "#ffffff",
        "status_bg": "#f8f8f8",
        "toolbar_bg": "#f0f0f0",
        
        # リスト・テーブル色
        "list_bg": "#ffffff",
        "list_alternate": "#f8f8f8",
        "list_hover": "#e6f3ff",
        "list_selection": "#cce8ff",
        
        # アドレスバー専用色
        "breadcrumb_bg": "#f0f0f0",
        "breadcrumb_hover": "#e0e0e0",
        "breadcrumb_active": "#cce8ff",
        "breadcrumb_separator": "#c0c0c0",
        
        # サムネイル・画像色
        "thumbnail_bg": "#ffffff",
        "thumbnail_border": "#ddd",
        "thumbnail_hover": "#e6f3ff",
        "thumbnail_selection": "#0078d4",
        
        # マップ色
        "map_bg": "#f8f8f8",
        "map_border": "#ddd",
        "marker_color": "#e74c3c",
        "marker_selected": "#c0392b"
    }


def _create_light_styles() -> Dict[str, str]:
    """ライトテーマのスタイル定義を作成"""
    return {
        "main_window": """
QMainWindow {{
    background-color: {background};
    color: {foreground};
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 9pt;
}}
        """,
        
        "group_box": """
QGroupBox {{
    font-size: 12px;
    font-weight: bold;
    background-color: {group_bg};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 5px;
    margin: 5px 0;
    padding-top: 15px;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 10px;
    padding: 0 5px;
    color: {primary};
    font-weight: bold;
}}
        """,
        
        "button": """
QPushButton {{
    background-color: {button_bg};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: normal;
    min-width: 60px;
    min-height: 24px;
}}
QPushButton:hover {{
    background-color: {button_hover};
    border-color: {accent};
}}
QPushButton:pressed {{
    background-color: {button_pressed};
}}
QPushButton:disabled {{
    background-color: {button_disabled};
    color: {muted};
    border-color: {border_light};
}}
QPushButton:focus {{
    border-color: {focus};
    outline: none;
}}
        """,
        
        "primary_button": """
QPushButton {{
    background-color: {primary};
    color: white;
    border: 1px solid {primary};
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 11px;
    font-weight: 500;
    min-width: 60px;
    min-height: 24px;
}}
QPushButton:hover {{
    background-color: {active};
    border-color: {active};
}}
QPushButton:pressed {{
    background-color: #004578;
}}
QPushButton:disabled {{
    background-color: {muted};
    border-color: {muted};
}}
        """,
        
        "maximize_button": """
QPushButton {{
    background: rgba(255, 255, 255, 0.9);
    color: {foreground};
    border: 1px solid {border};
    border-radius: 15px;
    font-size: 12px;
    font-weight: bold;
    padding: 0;
    width: 30px;
    height: 30px;
}}
QPushButton:hover {{
    background: rgba(0, 120, 212, 0.9);
    color: white;
    border-color: {accent};
}}
QPushButton:pressed {{
    background: rgba(0, 90, 158, 0.9);
}}
        """,
        
        "status_info": """
QLabel {{
    padding: 10px;
    background: {status_bg};
    border: 1px solid {border};
    border-radius: 5px;
    font-size: 11px;
    line-height: 1.4;
    color: {foreground};
}}
        """,
        
        "list_widget": """
QListWidget {{
    background-color: {list_bg};
    color: {foreground};
    border: 1px solid {border};
    border-radius: 3px;
    selection-background-color: {list_selection};
    alternate-background-color: {list_alternate};
    outline: none;
}}
QListWidget::item {{
    padding: 5px;
    border-bottom: 1px solid {border_light};
    min-height: 20px;
}}
QListWidget::item:hover {{
    background-color: {list_hover};
}}
QListWidget::item:selected {{
    background-color: {list_selection};
    color: {foreground};
}}
QListWidget::item:selected:active {{
    background-color: {primary};
    color: white;
}}
        """,
        
        "line_edit": """
QLineEdit {{
    background-color: {input_bg};
    color: {foreground};
    border: 1px solid {input_border};
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 11px;
    selection-background-color: {selection};
}}
QLineEdit:focus {{
    border-color: {input_focus_border};
}}
QLineEdit:disabled {{
    background-color: {button_disabled};
    color: {muted};
}}
        """,
        
        "combo_box": """
QComboBox {{
    background-color: {input_bg};
    color: {foreground};
    border: 1px solid {input_border};
    border-radius: 3px;
    padding: 4px 8px;
    font-size: 11px;
    min-width: 80px;
}}
QComboBox:hover {{
    border-color: {accent};
}}
QComboBox:focus {{
    border-color: {input_focus_border};
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox::down-arrow {{
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 5px solid {foreground};
    margin-right: 5px;
}}
QComboBox QAbstractItemView {{
    background-color: {input_bg};
    border: 1px solid {border};
    selection-background-color: {selection};
}}
        """,
        
        "panel": """
QWidget {{
    background-color: {panel_bg};
    color: {foreground};
}}
        """,
        
        "toolbar": """
QWidget {{
    background-color: {toolbar_bg};
    color: {foreground};
    border-bottom: 1px solid {border};
    padding: 2px;
}}
        """,
        
        "scroll_bar": """
QScrollBar:vertical {{
    background-color: {secondary};
    width: 12px;
    border: none;
    border-radius: 6px;
}}
QScrollBar::handle:vertical {{
    background-color: {border_dark};
    border-radius: 6px;
    min-height: 20px;
}}
QScrollBar::handle:vertical:hover {{
    background-color: {muted};
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0px;
}}
QScrollBar:horizontal {{
    background-color: {secondary};
    height: 12px;
    border: none;
    border-radius: 6px;
}}
QScrollBar::handle:horizontal {{
    background-color: {border_dark};
    border-radius: 6px;
    min-width: 20px;
}}
QScrollBar::handle:horizontal:hover {{
    background-color: {muted};
}}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
    width: 0px;
}}
        """,
        
        "progress_bar": """
QProgressBar {{
    background-color: {secondary};
    border: 1px solid {border};
    border-radius: 3px;
    text-align: center;
    font-size: 10px;
}}
QProgressBar::chunk {{
    background-color: {primary};
    border-radius: 2px;
}}
        """,
        
        "splitter": """
QSplitter::handle {{
    background-color: {border};
}}
QSplitter::handle:horizontal {{
    width: 3px;
}}
QSplitter::handle:vertical {{
    height: 3px;
}}
QSplitter::handle:hover {{
    background-color: {accent};
}}
        """,
        
        "tab_widget": """
QTabWidget::pane {{
    border: 1px solid {border};
    background-color: {background};
}}
QTabBar::tab {{
    background-color: {secondary};
    color: {foreground};
    border: 1px solid {border};
    padding: 6px 12px;
    margin-right: 2px;
}}
QTabBar::tab:selected {{
    background-color: {background};
    border-bottom-color: {background};
}}
QTabBar::tab:hover {{
    background-color: {hover};
}}
        """
    }


def _create_fallback_light_theme() -> Dict[str, Any]:
    """フォールバック用の簡易ライトテーマ"""
    return {
        "name": "light",
        "display_name": "ライトモード (フォールバック)",
        "description": "簡易ライトテーマ",
        "version": "1.0.0",
        "colors": {
            "background": "#ffffff",
            "foreground": "#000000",
            "primary": "#007acc",
            "secondary": "#f8f8f8",
            "accent": "#0078d4",
            "border": "#ddd"
        },
        "styles": {
            "main_window": "QMainWindow { background-color: #ffffff; color: #000000; }",
            "button": "QPushButton { background-color: #f0f0f0; border: 1px solid #ddd; }"
        }
    }


def get_light_color_variations() -> Dict[str, Dict[str, str]]:
    """ライトテーマのカラーバリエーションを取得"""
    return {
        "blue": {
            "primary": "#007acc",
            "accent": "#0078d4",
            "selection": "#cce8ff"
        },
        "green": {
            "primary": "#16a085",
            "accent": "#1abc9c",
            "selection": "#d5f4e6"
        },
        "purple": {
            "primary": "#8e44ad",
            "accent": "#9b59b6",
            "selection": "#ebdef0"
        },
        "orange": {
            "primary": "#e67e22",
            "accent": "#f39c12",
            "selection": "#fdeaa7"
        }
    }


def create_light_theme_variant(variant: str) -> Dict[str, Any]:
    """
    ライトテーマのバリエーションを作成
    
    Args:
        variant: バリエーション名 (blue, green, purple, orange)
        
    Returns:
        Dict[str, Any]: バリエーションテーマ定義
    """
    try:
        base_theme = create_light_theme()
        variations = get_light_color_variations()
        
        if variant not in variations:
            logging.warning(f"未対応のバリエーション: {variant}")
            return base_theme
        
        # カラーを置換
        variant_colors = variations[variant]
        base_theme["colors"].update(variant_colors)
        base_theme["name"] = f"light_{variant}"
        base_theme["display_name"] = f"ライトモード ({variant.title()})"
        
        return base_theme
        
    except Exception as e:
        logging.error(f"ライトテーマバリエーション作成エラー: {e}")
        return create_light_theme()
