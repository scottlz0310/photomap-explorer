"""
テーマ設定管理モジュール

テーマの保存・読み込み・記憶機能を提供します。
"""

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from utils.logging_bridge import get_theme_logger


class ThemeSettingsManager:
    """テーマ設定の管理クラス"""
    
    def __init__(self):
        """初期化"""
        self.logger = get_theme_logger("SettingsManager")
        self.settings_file_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "settings", "theme_settings.json"
        )
        self.current_settings = None
        self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """設定ファイルを読み込み"""
        try:
            if os.path.exists(self.settings_file_path):
                with open(self.settings_file_path, 'r', encoding='utf-8') as f:
                    self.current_settings = json.load(f)
                self.logger.verbose(f"テーマ設定を読み込み: {self.settings_file_path}")
                return self.current_settings
            else:
                self.logger.warning("テーマ設定ファイルが見つかりません、デフォルト設定を作成します")
                return self._create_default_settings()
                
        except Exception as e:
            self.logger.error(f"テーマ設定読み込みエラー: {e}")
            return self._create_default_settings()
    
    def save_settings(self, settings: Optional[Dict[str, Any]] = None) -> bool:
        """設定ファイルを保存"""
        try:
            settings_to_save = settings or self.current_settings
            if not settings_to_save:
                self.logger.warning("保存する設定がありません")
                return False
            
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
            
            with open(self.settings_file_path, 'w', encoding='utf-8') as f:
                json.dump(settings_to_save, f, indent=2, ensure_ascii=False)
            
            self.current_settings = settings_to_save
            self.logger.verbose(f"テーマ設定を保存: {self.settings_file_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"テーマ設定保存エラー: {e}")
            return False
    
    def get_current_theme(self) -> str:
        """現在のテーマ名を取得"""
        if not self.current_settings:
            self.load_settings()
        
        if not self.current_settings:
            return 'dark'
        
        return self.current_settings.get('current_theme', 'dark')
    
    def set_current_theme(self, theme_name: str) -> bool:
        """現在のテーマを設定"""
        try:
            if not self.current_settings:
                self.load_settings()
            
            if not self.current_settings:
                return False
            
            # テーマが利用可能かチェック
            available_themes = self.get_available_themes()
            if theme_name not in available_themes:
                self.logger.warning(f"未知のテーマ名: {theme_name}")
                return False
            
            self.current_settings['current_theme'] = theme_name
            
            # 記憶機能が有効な場合は last_selected_theme も更新
            if self.current_settings.get('remember_theme_choice', True):
                self.current_settings['last_selected_theme'] = theme_name
            
            return self.save_settings()
            
        except Exception as e:
            self.logger.error(f"テーマ設定エラー: {e}")
            return False
    
    def get_available_themes(self) -> Dict[str, Dict[str, Any]]:
        """利用可能なテーマ一覧を取得"""
        if not self.current_settings:
            self.load_settings()
        
        if not self.current_settings:
            return {}
        
        return self.current_settings.get('available_themes', {})
    
    def get_theme_info(self, theme_name: str) -> Optional[Dict[str, Any]]:
        """特定のテーマの情報を取得"""
        available_themes = self.get_available_themes()
        return available_themes.get(theme_name)
    
    def get_theme_display_names(self) -> List[str]:
        """テーマの表示名一覧を取得"""
        available_themes = self.get_available_themes()
        return [theme_info.get('display_name', theme_name) 
                for theme_name, theme_info in available_themes.items()]
    
    def get_theme_names(self) -> List[str]:
        """テーマ名一覧を取得"""
        return list(self.get_available_themes().keys())
    
    def get_available_theme_names(self) -> List[str]:
        """利用可能なテーマ名のリストを取得（互換性メソッド）"""
        return self.get_theme_names()
    
    def get_last_selected_theme(self) -> str:
        """最後に選択されたテーマを取得"""
        if not self.current_settings:
            self.load_settings()
        
        if not self.current_settings:
            return 'dark'
        
        return self.current_settings.get('last_selected_theme', 'dark')
    
    def is_theme_remembering_enabled(self) -> bool:
        """テーマ記憶機能が有効かどうか"""
        if not self.current_settings:
            self.load_settings()
        
        if not self.current_settings:
            return True
        
        return self.current_settings.get('remember_theme_choice', True)
    
    def set_theme_remembering(self, enabled: bool) -> bool:
        """テーマ記憶機能の有効/無効を設定"""
        try:
            if not self.current_settings:
                self.load_settings()
            
            if not self.current_settings:
                return False
            
            self.current_settings['remember_theme_choice'] = enabled
            return self.save_settings()
            
        except Exception as e:
            self.logger.error(f"テーマ記憶設定エラー: {e}")
            return False
    
    def get_breadcrumb_settings(self) -> Dict[str, Any]:
        """パンくずリスト設定を取得"""
        if not self.current_settings:
            self.load_settings()
        
        if not self.current_settings:
            return {
                'enabled': True,
                'show_home_button': True,
                'show_parent_button': True,
                'max_path_length': 50,
                'separator': ' / ',
                'auto_scroll': True
            }
        
        return self.current_settings.get('breadcrumb_settings', {
            'enabled': True,
            'show_home_button': True,
            'show_parent_button': True,
            'max_path_length': 50,
            'separator': ' / ',
            'auto_scroll': True
        })
    
    def set_breadcrumb_settings(self, settings: Dict[str, Any]) -> bool:
        """パンくずリスト設定を保存"""
        try:
            if not self.current_settings:
                self.load_settings()
            
            if not self.current_settings:
                return False
            
            self.current_settings['breadcrumb_settings'] = settings
            return self.save_settings()
            
        except Exception as e:
            self.logger.error(f"パンくずリスト設定保存エラー: {e}")
            return False
    
    def add_custom_theme(self, theme_name: str, theme_definition: Dict[str, Any]) -> bool:
        """カスタムテーマを追加"""
        try:
            if not self.current_settings:
                self.load_settings()
            
            if not self.current_settings:
                return False
            
            if 'available_themes' not in self.current_settings:
                self.current_settings['available_themes'] = {}
            
            self.current_settings['available_themes'][theme_name] = theme_definition
            return self.save_settings()
            
        except Exception as e:
            self.logger.error(f"カスタムテーマ追加エラー: {e}")
            return False
    
    def remove_theme(self, theme_name: str) -> bool:
        """テーマを削除（デフォルトテーマは削除不可）"""
        try:
            default_themes = ['dark', 'light', 'blue', 'green', 'purple']
            if theme_name in default_themes:
                self.logger.warning(f"デフォルトテーマは削除できません: {theme_name}")
                return False
            
            if not self.current_settings:
                self.load_settings()
            
            if not self.current_settings:
                return False
            
            available_themes = self.current_settings.get('available_themes', {})
            if theme_name in available_themes:
                del available_themes[theme_name]
                
                # 現在のテーマが削除されたテーマの場合はdarkに戻す
                if self.current_settings.get('current_theme') == theme_name:
                    self.current_settings['current_theme'] = 'dark'
                
                return self.save_settings()
            
            self.logger.warning(f"削除対象のテーマが見つかりません: {theme_name}")
            return False
            
        except Exception as e:
            self.logger.error(f"テーマ削除エラー: {e}")
            return False
    
    def cycle_theme(self) -> str:
        """次のテーマに切り替え（サイクル）"""
        try:
            available_themes = self.get_theme_names()
            if not available_themes:
                self.logger.warning("利用可能なテーマがありません")
                return 'dark'
            
            current_theme = self.get_current_theme()
            current_index = 0
            
            try:
                current_index = available_themes.index(current_theme)
            except ValueError:
                # 現在のテーマが見つからない場合は最初のテーマから開始
                current_index = 0
            
            # 次のテーマのインデックス（循環）
            next_index = (current_index + 1) % len(available_themes)
            next_theme = available_themes[next_index]
            
            # テーマを設定
            success = self.set_current_theme(next_theme)
            
            if success:
                self.logger.info(f"テーマをサイクル: {current_theme} → {next_theme}")
                return next_theme
            else:
                self.logger.warning(f"テーマサイクル失敗: {next_theme}")
                return current_theme
                
        except Exception as e:
            self.logger.error(f"テーマサイクルエラー: {e}")
            return self.get_current_theme()
    
    def _create_default_settings(self) -> Dict[str, Any]:
        """デフォルト設定を作成"""
        default_settings = {
            "current_theme": "dark",
            "last_selected_theme": "dark",
            "theme_switching_enabled": True,
            "remember_theme_choice": True,
            "version": "2.2.0",
            "available_themes": {
                "dark": {
                    "name": "dark",
                    "display_name": "ダークモード",
                    "description": "暗い背景の低負荷テーマ"
                },
                "light": {
                    "name": "light",
                    "display_name": "ライトモード", 
                    "description": "明るい背景の標準テーマ"
                },
                "blue": {
                    "name": "blue",
                    "display_name": "ブルーモード",
                    "description": "プロフェッショナルなブルーベーステーマ"
                },
                "green": {
                    "name": "green",
                    "display_name": "グリーンモード",
                    "description": "自然なグリーンベーステーマ"
                },
                "purple": {
                    "name": "purple",
                    "display_name": "パープルモード",
                    "description": "エレガントなパープルベーステーマ"
                }
            },
            "breadcrumb_settings": {
                "enabled": True,
                "show_home_button": True,
                "show_parent_button": True,
                "max_path_length": 50,
                "separator": " / ",
                "auto_scroll": True
            }
        }
        
        self.current_settings = default_settings
        self.save_settings()
        self.logger.info("デフォルトテーマ設定を作成しました")
        return default_settings
    
    def reset_to_defaults(self) -> bool:
        """設定をデフォルトにリセット"""
        try:
            self._create_default_settings()
            self.logger.info("テーマ設定をデフォルトにリセットしました")
            return True
            
        except Exception as e:
            self.logger.error(f"設定リセットエラー: {e}")
            return False
    
    def backup_settings(self, backup_path: Optional[str] = None) -> bool:
        """設定をバックアップ"""
        try:
            if not backup_path:
                backup_path = f"{self.settings_file_path}.backup"
            
            if self.current_settings:
                with open(backup_path, 'w', encoding='utf-8') as f:
                    json.dump(self.current_settings, f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"テーマ設定をバックアップ: {backup_path}")
                return True
            
            self.logger.warning("バックアップする設定がありません")
            return False
            
        except Exception as e:
            self.logger.error(f"設定バックアップエラー: {e}")
            return False
    
    def restore_settings(self, backup_path: str) -> bool:
        """設定をバックアップから復元"""
        try:
            if not os.path.exists(backup_path):
                self.logger.warning(f"バックアップファイルが見つかりません: {backup_path}")
                return False
            
            with open(backup_path, 'r', encoding='utf-8') as f:
                restored_settings = json.load(f)
            
            self.current_settings = restored_settings
            success = self.save_settings()
            
            if success:
                self.logger.info(f"テーマ設定を復元: {backup_path}")
            
            return success
            
        except Exception as e:
            self.logger.error(f"設定復元エラー: {e}")
            return False
