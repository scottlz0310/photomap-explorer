"""
統一テーマ初期化モジュール

settings/theme_settings.jsonから設定を読み込み、
統一されたテーマシステムを提供します。
"""

import json
import os
from typing import Dict, Any, List, Optional
from utils.logging_bridge import get_theme_logger


class ThemeInitializer:
    """統一テーマ初期化クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_theme_logger("ThemeInitializer")
        self.settings_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "settings", "theme_settings.json"
        )
        # パスを正規化
        self.settings_path = os.path.normpath(self.settings_path)
        self.theme_cache = {}
        self.load_theme_settings()
    
    def load_theme_settings(self) -> bool:
        """テーマ設定を読み込み"""
        try:
            with open(self.settings_path, 'r', encoding='utf-8') as f:
                self.settings = json.load(f)
            
            self.logger.info(f"テーマ設定を読み込み: {len(self.settings.get('available_themes', {}))}個のテーマ")
            return True
            
        except Exception as e:
            self.logger.error(f"テーマ設定読み込みエラー: {e}")
            self.settings = self._create_fallback_settings()
            return False
    
    def _create_fallback_settings(self) -> Dict[str, Any]:
        """フォールバック設定を作成"""
        return {
            "current_theme": "light",
            "last_selected_theme": "light",
            "theme_switching_enabled": True,
            "remember_theme_choice": True,
            "version": "2.2.0",
            "available_themes": {
                "light": {
                    "name": "light",
                    "display_name": "ライトモード",
                    "description": "明るい背景の標準テーマ",
                    "primaryColor": "#007acc",
                    "backgroundColor": "#ffffff",
                    "textColor": "#000000"
                }
            }
        }
    
    def get_available_theme_names(self) -> List[str]:
        """利用可能なテーマ名一覧を取得"""
        return list(self.settings.get('available_themes', {}).keys())
    
    def get_theme_definition(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """特定のテーマ定義を取得"""
        themes = self.settings.get('available_themes', {})
        return themes.get(theme_name)
    
    def create_theme_stylesheet(self, theme_name: str) -> str:
        """テーマのスタイルシートを生成"""
        try:
            if theme_name in self.theme_cache:
                return self.theme_cache[theme_name]
            
            theme_def = self.get_theme_definition(theme_name)
            if not theme_def:
                self.logger.warning(f"未知のテーマ: {theme_name}")
                return self._create_fallback_stylesheet()
            
            stylesheet = self._generate_stylesheet(theme_def)
            self.theme_cache[theme_name] = stylesheet
            
            self.logger.debug(f"スタイルシート生成完了: {theme_name}")
            return stylesheet
            
        except Exception as e:
            self.logger.error(f"スタイルシート生成エラー {theme_name}: {e}")
            return self._create_fallback_stylesheet()
    
    def _generate_stylesheet(self, theme_def: Dict[str, Any]) -> str:
        """テーマ定義からスタイルシートを生成"""
        
        # 色の取得（フォールバック付き）
        bg_color = theme_def.get('backgroundColor', '#ffffff')
        text_color = theme_def.get('textColor', '#000000')
        primary_color = theme_def.get('primaryColor', '#007acc')
        accent_color = theme_def.get('accentColor', primary_color)
        
        # ボタン設定
        button_settings = theme_def.get('button', {})
        button_bg = button_settings.get('background', '#f0f0f0')
        button_text = button_settings.get('text', text_color)
        button_hover = button_settings.get('hover', '#e0e0e0')
        button_pressed = button_settings.get('pressed', accent_color)
        button_border = button_settings.get('border', '#ddd')
        
        # パネル設定
        panel_settings = theme_def.get('panel', {})
        panel_bg = panel_settings.get('background', bg_color)
        panel_border = panel_settings.get('border', '#ddd')
        panel_header = panel_settings.get('header', {})
        panel_header_bg = panel_header.get('background', panel_bg)
        panel_header_text = panel_header.get('text', text_color)
        panel_header_border = panel_header.get('border', panel_border)
        
        # テキスト設定
        text_settings = theme_def.get('text', {})
        text_primary = text_settings.get('primary', text_color)
        text_secondary = text_settings.get('secondary', text_color)
        text_muted = text_settings.get('muted', '#888888')
        text_heading = text_settings.get('heading', text_color)
        text_link = text_settings.get('link', accent_color)
        text_success = text_settings.get('success', '#28a745')
        text_warning = text_settings.get('warning', '#ffc107')
        text_error = text_settings.get('error', '#dc3545')
        
        # 入力フィールド設定
        input_settings = theme_def.get('input', {})
        input_bg = input_settings.get('background', panel_bg)
        input_text = input_settings.get('text', text_color)
        input_border = input_settings.get('border', panel_border)
        input_focus = input_settings.get('focus', primary_color)
        input_placeholder = input_settings.get('placeholder', text_muted)
        
        # ツールバー設定
        toolbar_settings = theme_def.get('toolbar', {})
        toolbar_bg = toolbar_settings.get('background', panel_bg)
        toolbar_text = toolbar_settings.get('text', text_color)
        toolbar_border = toolbar_settings.get('border', panel_border)
        toolbar_button = toolbar_settings.get('button', {})
        toolbar_btn_bg = toolbar_button.get('background', button_bg)
        toolbar_btn_text = toolbar_button.get('text', button_text)
        toolbar_btn_hover = toolbar_button.get('hover', button_hover)
        toolbar_btn_pressed = toolbar_button.get('pressed', button_pressed)
        
        # ステータスバー設定
        status_settings = theme_def.get('status', {})
        status_bg = status_settings.get('background', panel_bg)
        status_text = status_settings.get('text', text_secondary)
        status_border = status_settings.get('border', panel_border)
        
        # 統一スタイルシートを生成
        stylesheet = f"""
            /* メインウィンドウ */
            QMainWindow {{
                background-color: {bg_color};
                color: {text_primary};
            }}
            
            /* 基本ウィジェット */
            QWidget {{
                background-color: {bg_color};
                color: {text_primary};
            }}
            
            /* ラベル・テキスト */
            QLabel {{
                color: {text_primary};
                background-color: transparent;
            }}
            
            /* 見出し用ラベル */
            QLabel[heading="true"] {{
                color: {text_heading};
                font-weight: bold;
                font-size: 16px;
            }}
            
            /* セカンダリテキスト */
            QLabel[secondary="true"] {{
                color: {text_secondary};
            }}
            
            /* ミュートテキスト */
            QLabel[muted="true"] {{
                color: {text_muted};
            }}
            
            /* ボタン */
            QPushButton {{
                background-color: {button_bg};
                color: {button_text};
                border: 1px solid {button_border};
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {button_hover};
                border-color: {primary_color};
            }}
            QPushButton:pressed {{
                background-color: {button_pressed};
                color: #ffffff;
            }}
            QPushButton:disabled {{
                background-color: {text_muted};
                color: #888888;
                border-color: {text_muted};
            }}
            
            /* ツールバーボタン */
            QPushButton[toolbar="true"] {{
                background-color: {toolbar_btn_bg};
                color: {toolbar_btn_text};
                border: 1px solid {toolbar_border};
            }}
            QPushButton[toolbar="true"]:hover {{
                background-color: {toolbar_btn_hover};
                color: {toolbar_btn_text};
            }}
            QPushButton[toolbar="true"]:pressed {{
                background-color: {toolbar_btn_pressed};
            }}
            
            /* 入力フィールド */
            QLineEdit {{
                background-color: {input_bg};
                color: {input_text};
                border: 1px solid {input_border};
                border-radius: 4px;
                padding: 4px 8px;
            }}
            QLineEdit:focus {{
                border-color: {input_focus};
            }}
            QLineEdit::placeholder {{
                color: {input_placeholder};
            }}
            
            /* ツールバー */
            QToolBar {{
                background-color: {toolbar_bg};
                color: {toolbar_text};
                border: 1px solid {toolbar_border};
                spacing: 2px;
            }}
            
            /* ステータスバー */
            QStatusBar {{
                background-color: {status_bg};
                color: {status_text};
                border-top: 1px solid {status_border};
            }}
            
            /* パネルヘッダー */
            QWidget[panel_header="true"] {{
                background-color: {panel_header_bg};
                color: {panel_header_text};
                border: 1px solid {panel_header_border};
                padding: 4px 8px;
                font-weight: bold;
            }}
            
            /* リスト */
            QListWidget {{
                background-color: {panel_bg};
                color: {text_primary};
                border: 1px solid {panel_border};
                border-radius: 4px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 4px;
                border-bottom: 1px solid {panel_border};
            }}
            QListWidget::item:selected {{
                background-color: {primary_color};
                color: #ffffff;
            }}
            QListWidget::item:hover {{
                background-color: {button_hover};
            }}
            
            /* グループボックス */
            QGroupBox {{
                color: {text_heading};
                border: 2px solid {panel_border};
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: 600;
            }}
            QGroupBox::title {{
                color: {text_heading};
                font-weight: 700;
                padding: 0 8px;
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
            }}
            
            /* スプリッタ */
            QSplitter::handle {{
                background-color: {panel_border};
                border: 1px solid {panel_border};
            }}
            QSplitter::handle:horizontal {{
                width: 3px;
            }}
            QSplitter::handle:vertical {{
                height: 3px;
            }}
            
            /* ステータスバー */
            QStatusBar {{
                background-color: {panel_bg};
                color: {text_color};
                border-top: 1px solid {panel_border};
            }}
            
            /* スクロールバー */
            QScrollBar:vertical {{
                background-color: {bg_color};
                width: 12px;
                border: none;
            }}
            QScrollBar::handle:vertical {{
                background-color: {panel_border};
                border-radius: 6px;
                min-height: 20px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: {primary_color};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            QScrollBar:horizontal {{
                background-color: {bg_color};
                height: 12px;
                border: none;
            }}
            QScrollBar::handle:horizontal {{
                background-color: {panel_border};
                border-radius: 6px;
                min-width: 20px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: {primary_color};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
        """
        
        return stylesheet
    
    def _create_fallback_stylesheet(self) -> str:
        """フォールバックスタイルシートを作成"""
        return """
            QMainWindow {
                background-color: #ffffff;
                color: #000000;
            }
            QLabel {
                color: #000000;
            }
            QPushButton {
                background-color: #f0f0f0;
                color: #000000;
                border: 1px solid #ddd;
                padding: 6px 12px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """
    
    def get_current_theme(self) -> str:
        """現在のテーマ名を取得"""
        return self.settings.get('current_theme', 'light')
    
    def get_current_theme_data(self) -> Dict[str, Any]:
        """現在のテーマデータを取得"""
        try:
            current_theme = self.get_current_theme()
            return self.get_theme_data(current_theme)
        except Exception as e:
            self.logger.error(f"現在のテーマデータ取得エラー: {e}")
            return {}
    
    def get_theme_data(self, theme_name: str) -> Dict[str, Any]:
        """指定されたテーマのデータを取得"""
        try:
            available_themes = self.settings.get('available_themes', {})
            return available_themes.get(theme_name, {})
        except Exception as e:
            self.logger.error(f"テーマデータ取得エラー ({theme_name}): {e}")
            return {}
    
    def set_current_theme(self, theme_name: str) -> bool:
        """現在のテーマを設定"""
        try:
            if theme_name not in self.get_available_theme_names():
                self.logger.warning(f"未知のテーマ: {theme_name}")
                return False
            
            self.settings['current_theme'] = theme_name
            self.settings['last_selected_theme'] = theme_name
            
            # 設定を保存
            self.save_settings()
            
            self.logger.info(f"テーマ変更: {theme_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"テーマ設定エラー: {e}")
            return False
    
    def save_settings(self) -> bool:
        """設定を保存"""
        try:
            with open(self.settings_path, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
            
            self.logger.debug("テーマ設定を保存")
            return True
            
        except Exception as e:
            self.logger.error(f"テーマ設定保存エラー: {e}")
            return False
    
    def cycle_theme(self) -> str:
        """テーマを順次切り替え"""
        try:
            available_themes = self.get_available_theme_names()
            current_theme = self.get_current_theme()
            
            if not available_themes:
                return current_theme
            
            try:
                current_index = available_themes.index(current_theme)
            except ValueError:
                current_index = -1
            
            next_index = (current_index + 1) % len(available_themes)
            next_theme = available_themes[next_index]
            
            if self.set_current_theme(next_theme):
                # キャッシュをクリア
                self.theme_cache.clear()
                self.logger.info(f"テーマサイクル: {current_theme} → {next_theme}")
                return next_theme
            
            return current_theme
            
        except Exception as e:
            self.logger.error(f"テーマサイクルエラー: {e}")
            return self.get_current_theme()
    
    def clear_cache(self):
        """キャッシュをクリア"""
        self.theme_cache.clear()
        self.logger.debug("テーマキャッシュをクリア")


# グローバルインスタンス
_theme_initializer = None

def get_theme_initializer() -> ThemeInitializer:
    """テーマ初期化インスタンスを取得（シングルトン）"""
    global _theme_initializer
    if _theme_initializer is None:
        _theme_initializer = ThemeInitializer()
    return _theme_initializer

def get_current_theme_stylesheet() -> str:
    """現在のテーマのスタイルシートを取得"""
    initializer = get_theme_initializer()
    current_theme = initializer.get_current_theme()
    return initializer.create_theme_stylesheet(current_theme)

def apply_theme_to_widget(widget, theme_name: Optional[str] = None):
    """ウィジェットにテーマを適用"""
    initializer = get_theme_initializer()
    if theme_name is None:
        theme_name = initializer.get_current_theme()
    
    stylesheet = initializer.create_theme_stylesheet(theme_name)
    widget.setStyleSheet(stylesheet)
