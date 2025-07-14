"""
テーマファクトリーモジュール

このモジュールは presentation/themes/theme_manager.py から分離された
テーマの作成、管理、適用機能を提供します。
"""

from typing import Dict, Any, Optional, List, Callable
import logging
from enum import Enum

from ..definitions.light_theme import create_light_theme, create_light_theme_variant, get_light_color_variations
from ..definitions.dark_theme import create_dark_theme, create_dark_theme_variant, get_dark_color_variations
from .theme_engine import ThemeMode


class ThemeFactory:
    """
    テーマファクトリークラス
    
    テーマの作成、バリデーション、カスタマイズを担当
    """
    
    def __init__(self):
        self._theme_creators: Dict[str, Callable[[], Dict[str, Any]]] = {}
        self._theme_validators: List[Callable[[Dict[str, Any]], bool]] = []
        self._theme_customizers: Dict[str, Callable[[Dict[str, Any]], Dict[str, Any]]] = {}
        self._register_default_creators()
        self._register_default_validators()
    
    def _register_default_creators(self):
        """デフォルトのテーマ作成関数を登録"""
        self._theme_creators.update({
            "light": create_light_theme,
            "dark": create_dark_theme,
            # バリエーション
            "light_blue": lambda: create_light_theme_variant("blue"),
            "light_green": lambda: create_light_theme_variant("green"),
            "light_purple": lambda: create_light_theme_variant("purple"),
            "dark_blue": lambda: create_dark_theme_variant("blue"),
            "dark_cyan": lambda: create_dark_theme_variant("cyan"),
            "dark_purple": lambda: create_dark_theme_variant("purple"),
            "dark_orange": lambda: create_dark_theme_variant("orange"),
            "dark_green": lambda: create_dark_theme_variant("green")
        })
    
    def _register_default_validators(self):
        """デフォルトのバリデーターを登録"""
        self._theme_validators.extend([
            self._validate_required_fields,
            self._validate_colors,
            self._validate_styles
        ])
    
    def create_theme(self, theme_name: str, **kwargs) -> Optional[Dict[str, Any]]:
        """
        テーマを作成
        
        Args:
            theme_name: テーマ名
            **kwargs: テーマカスタマイズパラメータ
            
        Returns:
            Optional[Dict[str, Any]]: テーマ定義、失敗時はNone
        """
        try:
            if theme_name not in self._theme_creators:
                logging.warning(f"未登録のテーマ: {theme_name}")
                return None
            
            # テーマ作成
            theme = self._theme_creators[theme_name]()
            
            # カスタマイズ適用
            theme = self._apply_customizations(theme, **kwargs)
            
            # バリデーション
            if not self.validate_theme(theme):
                logging.error(f"テーマバリデーション失敗: {theme_name}")
                return None
            
            logging.debug(f"テーマ作成成功: {theme_name}")
            return theme
            
        except Exception as e:
            logging.error(f"テーマ作成エラー ({theme_name}): {e}")
            return None
    
    def validate_theme(self, theme: Dict[str, Any]) -> bool:
        """
        テーマをバリデーション
        
        Args:
            theme: テーマ定義
            
        Returns:
            bool: バリデーション結果
        """
        try:
            for validator in self._theme_validators:
                if not validator(theme):
                    return False
            return True
            
        except Exception as e:
            logging.error(f"テーマバリデーションエラー: {e}")
            return False
    
    def _validate_required_fields(self, theme: Dict[str, Any]) -> bool:
        """必須フィールドの検証"""
        required_fields = ["name", "display_name", "colors", "styles"]
        
        for field in required_fields:
            if field not in theme:
                logging.error(f"必須フィールド不足: {field}")
                return False
            
            if not theme[field]:
                logging.error(f"必須フィールドが空: {field}")
                return False
        
        return True
    
    def _validate_colors(self, theme: Dict[str, Any]) -> bool:
        """カラー定義の検証"""
        colors = theme.get("colors", {})
        required_colors = [
            "background", "foreground", "primary", "secondary", "accent"
        ]
        
        for color in required_colors:
            if color not in colors:
                logging.error(f"必須カラー不足: {color}")
                return False
            
            # カラーコード形式チェック（簡易）
            color_value = colors[color]
            if not isinstance(color_value, str) or not color_value.startswith("#"):
                logging.error(f"無効なカラーコード: {color}={color_value}")
                return False
        
        return True
    
    def _validate_styles(self, theme: Dict[str, Any]) -> bool:
        """スタイル定義の検証"""
        styles = theme.get("styles", {})
        required_styles = ["main_window", "button", "group_box"]
        
        for style in required_styles:
            if style not in styles:
                logging.error(f"必須スタイル不足: {style}")
                return False
            
            if not isinstance(styles[style], str):
                logging.error(f"無効なスタイル定義: {style}")
                return False
        
        return True
    
    def _apply_customizations(self, theme: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        テーマにカスタマイズを適用
        
        Args:
            theme: ベーステーマ
            **kwargs: カスタマイズパラメータ
            
        Returns:
            Dict[str, Any]: カスタマイズ済みテーマ
        """
        try:
            customized_theme = theme.copy()
            
            # カラーオーバーライド
            if "color_overrides" in kwargs:
                color_overrides = kwargs["color_overrides"]
                if isinstance(color_overrides, dict):
                    customized_theme["colors"].update(color_overrides)
            
            # スタイルオーバーライド
            if "style_overrides" in kwargs:
                style_overrides = kwargs["style_overrides"]
                if isinstance(style_overrides, dict):
                    customized_theme["styles"].update(style_overrides)
            
            # フォントサイズ調整
            if "font_scale" in kwargs:
                font_scale = kwargs.get("font_scale", 1.0)
                customized_theme = self._apply_font_scaling(customized_theme, font_scale)
            
            # カスタマイザー適用
            theme_name = customized_theme.get("name", "")
            if theme_name in self._theme_customizers:
                customized_theme = self._theme_customizers[theme_name](customized_theme)
            
            return customized_theme
            
        except Exception as e:
            logging.error(f"カスタマイズ適用エラー: {e}")
            return theme
    
    def _apply_font_scaling(self, theme: Dict[str, Any], scale: float) -> Dict[str, Any]:
        """
        フォントサイズスケーリングを適用
        
        Args:
            theme: テーマ定義
            scale: スケール倍率
            
        Returns:
            Dict[str, Any]: スケーリング適用済みテーマ
        """
        try:
            if scale <= 0:
                scale = 1.0
            
            scaled_theme = theme.copy()
            styles = scaled_theme.get("styles", {})
            
            # フォントサイズを調整
            for style_name, style_definition in styles.items():
                if "font-size:" in style_definition:
                    # 簡単なフォントサイズ置換（実際はより複雑な処理が必要）
                    import re
                    def scale_font_size(match):
                        size = int(match.group(1))
                        new_size = max(8, int(size * scale))  # 最小8px
                        return f"font-size: {new_size}px"
                    
                    styles[style_name] = re.sub(
                        r'font-size:\s*(\d+)px',
                        scale_font_size,
                        style_definition
                    )
            
            return scaled_theme
            
        except Exception as e:
            logging.error(f"フォントスケーリングエラー: {e}")
            return theme
    
    def register_theme_creator(self, theme_name: str, creator: Callable[[], Dict[str, Any]]):
        """
        カスタムテーマ作成関数を登録
        
        Args:
            theme_name: テーマ名
            creator: テーマ作成関数
        """
        self._theme_creators[theme_name] = creator
        logging.debug(f"テーマ作成関数登録: {theme_name}")
    
    def register_theme_customizer(self, theme_name: str, customizer: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """
        テーマカスタマイザーを登録
        
        Args:
            theme_name: テーマ名
            customizer: カスタマイザー関数
        """
        self._theme_customizers[theme_name] = customizer
        logging.debug(f"テーマカスタマイザー登録: {theme_name}")
    
    def get_available_themes(self) -> List[str]:
        """
        利用可能なテーマ一覧を取得
        
        Returns:
            List[str]: テーマ名のリスト
        """
        return list(self._theme_creators.keys())
    
    def get_theme_variations(self, base_theme: str) -> List[str]:
        """
        ベーステーマのバリエーション一覧を取得
        
        Args:
            base_theme: ベーステーマ名（light または dark）
            
        Returns:
            List[str]: バリエーション名のリスト
        """
        try:
            if base_theme == "light":
                variations = list(get_light_color_variations().keys())
                return [f"light_{var}" for var in variations]
            elif base_theme == "dark":
                variations = list(get_dark_color_variations().keys())
                return [f"dark_{var}" for var in variations]
            else:
                return []
                
        except Exception as e:
            logging.error(f"バリエーション取得エラー: {e}")
            return []
    
    def create_custom_theme(self, name: str, base_theme: str, customizations: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        カスタムテーマを作成
        
        Args:
            name: カスタムテーマ名
            base_theme: ベーステーマ名
            customizations: カスタマイズ設定
            
        Returns:
            Optional[Dict[str, Any]]: カスタムテーマ定義
        """
        try:
            # ベーステーマ作成
            base = self.create_theme(base_theme)
            if not base:
                logging.error(f"ベーステーマ作成失敗: {base_theme}")
                return None
            
            # カスタマイズ適用
            custom_theme = self._apply_customizations(base, **customizations)
            
            # メタデータ更新
            custom_theme["name"] = name
            custom_theme["display_name"] = customizations.get("display_name", name)
            custom_theme["description"] = customizations.get("description", f"{base_theme}ベースのカスタムテーマ")
            custom_theme["base_theme"] = base_theme
            
            # バリデーション
            if not self.validate_theme(custom_theme):
                logging.error(f"カスタムテーマバリデーション失敗: {name}")
                return None
            
            logging.info(f"カスタムテーマ作成成功: {name}")
            return custom_theme
            
        except Exception as e:
            logging.error(f"カスタムテーマ作成エラー ({name}): {e}")
            return None


class ThemePresetManager:
    """
    テーマプリセット管理クラス
    
    よく使用されるテーマ設定のプリセットを管理
    """
    
    def __init__(self):
        self._presets: Dict[str, Dict[str, Any]] = {}
        self._register_default_presets()
    
    def _register_default_presets(self):
        """デフォルトプリセットを登録"""
        self._presets.update({
            "default_light": {
                "theme": "light",
                "description": "標準ライトテーマ",
                "settings": {}
            },
            "default_dark": {
                "theme": "dark",
                "description": "標準ダークテーマ",
                "settings": {}
            },
            "large_text": {
                "theme": "light",
                "description": "大きなフォントのライトテーマ",
                "settings": {
                    "font_scale": 1.2
                }
            },
            "high_contrast": {
                "theme": "dark",
                "description": "高コントラスト",
                "settings": {
                    "color_overrides": {
                        "background": "#000000",
                        "foreground": "#ffffff",
                        "border": "#ffffff"
                    }
                }
            },
            "photography": {
                "theme": "dark",
                "description": "写真編集向け",
                "settings": {
                    "color_overrides": {
                        "background": "#1a1a1a",
                        "panel_bg": "#1e1e1e"
                    }
                }
            }
        })
    
    def get_preset(self, preset_name: str) -> Optional[Dict[str, Any]]:
        """
        プリセット取得
        
        Args:
            preset_name: プリセット名
            
        Returns:
            Optional[Dict[str, Any]]: プリセット定義
        """
        return self._presets.get(preset_name)
    
    def register_preset(self, name: str, theme: str, description: str, settings: Dict[str, Any]):
        """
        プリセット登録
        
        Args:
            name: プリセット名
            theme: ベーステーマ
            description: 説明
            settings: 設定
        """
        self._presets[name] = {
            "theme": theme,
            "description": description,
            "settings": settings
        }
        logging.debug(f"プリセット登録: {name}")
    
    def get_available_presets(self) -> List[str]:
        """利用可能なプリセット一覧を取得"""
        return list(self._presets.keys())
    
    def create_theme_from_preset(self, preset_name: str, factory: ThemeFactory) -> Optional[Dict[str, Any]]:
        """
        プリセットからテーマを作成
        
        Args:
            preset_name: プリセット名
            factory: テーマファクトリー
            
        Returns:
            Optional[Dict[str, Any]]: テーマ定義
        """
        try:
            preset = self.get_preset(preset_name)
            if not preset:
                logging.error(f"プリセット未見つからない: {preset_name}")
                return None
            
            return factory.create_theme(preset["theme"], **preset["settings"])
            
        except Exception as e:
            logging.error(f"プリセットテーマ作成エラー ({preset_name}): {e}")
            return None
