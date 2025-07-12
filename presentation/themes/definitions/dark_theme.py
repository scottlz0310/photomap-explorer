"""
ダークテーマ定義モジュール

このモジュールは presentation/themes/theme_manager.py から分離された
ダークテーマの定義を提供します。
"""

from typing import Dict, Any
import logging


def create_dark_theme() -> Dict[str, Any]:
    """
    ダークテーマ定義を作成
    
    Returns:
        Dict[str, Any]: ダークテーマの完全な定義
    """
    try:
        return {
            "name": "dark",
            "display_name": "ダークモード",
            "description": "暗い背景の低負荷テーマ",
            "version": "2.2.0",
            "author": "PhotoMap Explorer Team",
            "colors": _create_dark_colors(),
            "styles": _create_dark_styles()
        }
        
    except Exception as e:
        logging.error(f"ダークテーマ作成エラー: {e}")
        return _create_fallback_dark_theme()


def _create_dark_colors() -> Dict[str, str]:
    """ダークテーマのカラーパレットを作成"""
    return {
        # 基本色
        "background": "#2b2b2b",
        "foreground": "#ffffff",
        "primary": "#4fc3f7",
        "secondary": "#3c3c3c",
        "accent": "#29b6f6",
        
        # UI要素色
        "border": "#555",
        "border_light": "#666",
        "border_dark": "#444",
        
        # 状態色
        "error": "#f44336",
        "warning": "#ff9800",
        "success": "#4caf50",
        "info": "#2196f3",
        "muted": "#aaa",
        
        # インタラクション色
        "hover": "#404040",
        "selection": "#1e88e5",
        "focus": "#29b6f6",
        "active": "#0277bd",
        
        # ボタン色
        "button_bg": "#3c3c3c",
        "button_hover": "#484848",
        "button_pressed": "#2a2a2a",
        "button_disabled": "#2a2a2a",
        
        # 入力フィールド色
        "input_bg": "#2b2b2b",
        "input_border": "#555",
        "input_focus_border": "#29b6f6",
        "input_error_border": "#f44336",
        
        # パネル・グループ色
        "group_bg": "#353535",
        "panel_bg": "#2b2b2b",
        "status_bg": "#353535",
        "toolbar_bg": "#383838",
        
        # リスト・テーブル色
        "list_bg": "#2b2b2b",
        "list_alternate": "#353535",
        "list_hover": "#404040",
        "list_selection": "#1e88e5",
        
        # アドレスバー専用色
        "breadcrumb_bg": "#3c3c3c",
        "breadcrumb_hover": "#484848",
        "breadcrumb_active": "#1e88e5",
        "breadcrumb_separator": "#666",
        
        # サムネイル・画像色
        "thumbnail_bg": "#2b2b2b",
        "thumbnail_border": "#555",
        "thumbnail_hover": "#404040",
        "thumbnail_selection": "#29b6f6",
        
        # マップ色
        "map_bg": "#353535",
        "map_border": "#555",
        "marker_color": "#f44336",
        "marker_selected": "#e53935"
    }


def _create_dark_styles() -> Dict[str, str]:
    """ダークテーマのスタイル定義を作成"""
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
    border-color: {border_dark};
}}
QPushButton:focus {{
    border-color: {focus};
    outline: none;
}}
        """,
        
        "primary_button": """
QPushButton {{
    background-color: {primary};
    color: {background};
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
    background-color: #01579b;
}}
QPushButton:disabled {{
    background-color: {muted};
    border-color: {muted};
}}
        """,
        
        "maximize_button": """
QPushButton {{
    background: rgba(60, 60, 60, 0.9);
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
    background: rgba(41, 182, 246, 0.9);
    color: {background};
    border-color: {accent};
}}
QPushButton:pressed {{
    background: rgba(2, 119, 189, 0.9);
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
    border-bottom: 1px solid {border_dark};
    color: {foreground};
    min-height: 20px;
}}
QListWidget::item:hover {{
    background-color: {list_hover};
}}
QListWidget::item:selected {{
    background-color: {list_selection};
    color: white;
}}
QListWidget::item:selected:active {{
    background-color: {primary};
    color: {background};
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
    color: {foreground};
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
    background-color: {border_light};
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
    background-color: {border_light};
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
    color: {foreground};
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


def _create_fallback_dark_theme() -> Dict[str, Any]:
    """フォールバック用の簡易ダークテーマ"""
    return {
        "name": "dark",
        "display_name": "ダークモード (フォールバック)",
        "description": "簡易ダークテーマ",
        "version": "1.0.0",
        "colors": {
            "background": "#2b2b2b",
            "foreground": "#ffffff",
            "primary": "#4fc3f7",
            "secondary": "#3c3c3c",
            "accent": "#29b6f6",
            "border": "#555"
        },
        "styles": {
            "main_window": "QMainWindow { background-color: #2b2b2b; color: #ffffff; }",
            "button": "QPushButton { background-color: #3c3c3c; border: 1px solid #555; color: #fff; }"
        }
    }


def get_dark_color_variations() -> Dict[str, Dict[str, str]]:
    """ダークテーマのカラーバリエーションを取得"""
    return {
        "blue": {
            "primary": "#4fc3f7",
            "accent": "#29b6f6",
            "selection": "#1e88e5"
        },
        "cyan": {
            "primary": "#4dd0e1",
            "accent": "#26c6da",
            "selection": "#00acc1"
        },
        "purple": {
            "primary": "#ab47bc",
            "accent": "#ba68c8",
            "selection": "#8e24aa"
        },
        "orange": {
            "primary": "#ff8a65",
            "accent": "#ff7043",
            "selection": "#f4511e"
        },
        "green": {
            "primary": "#66bb6a",
            "accent": "#4caf50",
            "selection": "#388e3c"
        }
    }


def create_dark_theme_variant(variant: str) -> Dict[str, Any]:
    """
    ダークテーマのバリエーションを作成
    
    Args:
        variant: バリエーション名 (blue, cyan, purple, orange, green)
        
    Returns:
        Dict[str, Any]: バリエーションテーマ定義
    """
    try:
        base_theme = create_dark_theme()
        variations = get_dark_color_variations()
        
        if variant not in variations:
            logging.warning(f"未対応のバリエーション: {variant}")
            return base_theme
        
        # カラーを置換
        variant_colors = variations[variant]
        base_theme["colors"].update(variant_colors)
        base_theme["name"] = f"dark_{variant}"
        base_theme["display_name"] = f"ダークモード ({variant.title()})"
        
        return base_theme
        
    except Exception as e:
        logging.error(f"ダークテーマバリエーション作成エラー: {e}")
        return create_dark_theme()


def create_high_contrast_dark_theme() -> Dict[str, Any]:
    """
    高コントラストダークテーマを作成
    
    Returns:
        Dict[str, Any]: 高コントラストダークテーマ定義
    """
    try:
        base_theme = create_dark_theme()
        
        # 高コントラスト用にカラーを調整
        high_contrast_colors = {
            "background": "#000000",
            "foreground": "#ffffff",
            "primary": "#00ffff",
            "secondary": "#1a1a1a",
            "accent": "#ffff00",
            "border": "#ffffff",
            "selection": "#00ff00",
            "hover": "#333333"
        }
        
        base_theme["colors"].update(high_contrast_colors)
        base_theme["name"] = "dark_high_contrast"
        base_theme["display_name"] = "ダークモード (高コントラスト)"
        base_theme["description"] = "視認性を最大化した高コントラストダークテーマ"
        
        return base_theme
        
    except Exception as e:
        logging.error(f"高コントラストダークテーマ作成エラー: {e}")
        return create_dark_theme()
