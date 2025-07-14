"""
テーマ設定管理モジュール

このモジュールは presentation/themes/theme_manager.py から分離された
テーマ設定の永続化、読み込み、設定管理機能を提供します。
"""

import json
import os
from typing import Dict, Any, Optional, List, Callable
import logging
from dataclasses import dataclass, asdict, field
from pathlib import Path

from ..core.theme_engine import ThemeMode


@dataclass
class ThemeSettings:
    """テーマ設定データクラス"""
    current_theme: str = "light"
    theme_mode: str = "light"  # light, dark, auto
    auto_detect_system: bool = True
    font_scale: float = 1.0
    custom_colors: Dict[str, str] = field(default_factory=dict)
    last_updated: str = ""
    version: str = "2.2.0"
    
    def __post_init__(self):
        # field(default_factory=dict)を使用するため、この処理は不要
        pass


class ThemeSettingsManager:
    """
    テーマ設定管理クラス
    
    テーマ設定の読み込み、保存、管理を担当
    """
    
    def __init__(self, settings_file: Optional[str] = None):
        self._settings_file = settings_file or self._get_default_settings_file()
        self._settings: ThemeSettings = ThemeSettings()
        self._watchers: List[Callable] = []
        self._backup_enabled = True
        self._max_backups = 5
        
        # 設定読み込み
        self.load_settings()
    
    def _get_default_settings_file(self) -> str:
        """デフォルト設定ファイルパスを取得"""
        try:
            # settings/theme_settings.json を使用
            settings_dir = Path(__file__).parent.parent.parent.parent / "settings"
            settings_dir.mkdir(exist_ok=True)
            return str(settings_dir / "theme_settings.json")
            
        except Exception as e:
            logging.warning(f"デフォルト設定パス取得エラー: {e}")
            # フォールバック
            return os.path.expanduser("~/.photomap_theme_settings.json")
    
    def load_settings(self) -> bool:
        """
        設定を読み込み
        
        Returns:
            bool: 読み込み成功フラグ
        """
        try:
            if not os.path.exists(self._settings_file):
                logging.info("設定ファイルが存在しないため、デフォルト設定を使用")
                self._settings = ThemeSettings()
                return True
            
            with open(self._settings_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # バージョンチェック
            if not self._validate_settings_version(data):
                logging.warning("設定ファイルのバージョンが古いため、デフォルト設定を使用")
                self._settings = ThemeSettings()
                return True
            
            # 設定オブジェクト作成
            self._settings = ThemeSettings(
                current_theme=data.get("current_theme", "light"),
                theme_mode=data.get("theme_mode", "light"),
                auto_detect_system=data.get("auto_detect_system", True),
                font_scale=data.get("font_scale", 1.0),
                custom_colors=data.get("custom_colors", {}),
                last_updated=data.get("last_updated", ""),
                version=data.get("version", "2.2.0")
            )
            
            logging.debug(f"テーマ設定読み込み成功: {self._settings_file}")
            return True
            
        except Exception as e:
            logging.error(f"設定読み込みエラー: {e}")
            self._settings = ThemeSettings()
            return False
    
    def save_settings(self) -> bool:
        """
        設定を保存
        
        Returns:
            bool: 保存成功フラグ
        """
        try:
            # バックアップ作成
            if self._backup_enabled and os.path.exists(self._settings_file):
                self._create_backup()
            
            # 現在時刻を設定
            from datetime import datetime
            self._settings.last_updated = datetime.now().isoformat()
            
            # ディレクトリ作成
            os.makedirs(os.path.dirname(self._settings_file), exist_ok=True)
            
            # 保存
            with open(self._settings_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._settings), f, indent=2, ensure_ascii=False)
            
            logging.debug(f"テーマ設定保存成功: {self._settings_file}")
            
            # 変更通知
            self._notify_watchers()
            
            return True
            
        except Exception as e:
            logging.error(f"設定保存エラー: {e}")
            return False
    
    def _validate_settings_version(self, data: Dict[str, Any]) -> bool:
        """設定ファイルバージョンを検証"""
        try:
            version = data.get("version", "1.0.0")
            
            # 簡易バージョンチェック（メジャーバージョンが同じか確認）
            current_major = self._settings.version.split('.')[0]
            file_major = version.split('.')[0]
            
            return current_major == file_major
            
        except Exception as e:
            logging.error(f"バージョン検証エラー: {e}")
            return False
    
    def _create_backup(self):
        """設定ファイルのバックアップを作成"""
        try:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{self._settings_file}.backup_{timestamp}"
            
            import shutil
            shutil.copy2(self._settings_file, backup_file)
            
            # 古いバックアップを削除
            self._cleanup_backups()
            
            logging.debug(f"バックアップ作成: {backup_file}")
            
        except Exception as e:
            logging.error(f"バックアップ作成エラー: {e}")
    
    def _cleanup_backups(self):
        """古いバックアップファイルを削除"""
        try:
            directory = os.path.dirname(self._settings_file)
            filename = os.path.basename(self._settings_file)
            
            # バックアップファイル一覧取得
            backup_files = []
            for file in os.listdir(directory):
                if file.startswith(f"{filename}.backup_"):
                    backup_files.append(os.path.join(directory, file))
            
            # 日付順でソート
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            # 制限を超えた古いファイルを削除
            for old_backup in backup_files[self._max_backups:]:
                os.remove(old_backup)
                logging.debug(f"古いバックアップ削除: {old_backup}")
                
        except Exception as e:
            logging.error(f"バックアップクリーンアップエラー: {e}")
    
    def get_current_theme(self) -> str:
        """現在のテーマ名を取得"""
        return self._settings.current_theme
    
    def set_current_theme(self, theme_name: str) -> bool:
        """
        現在のテーマを設定
        
        Args:
            theme_name: テーマ名
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            self._settings.current_theme = theme_name
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"テーマ設定エラー: {e}")
            return False
    
    def get_theme_mode(self) -> ThemeMode:
        """テーマモードを取得"""
        try:
            mode_str = self._settings.theme_mode.lower()
            if mode_str == "dark":
                return ThemeMode.DARK
            elif mode_str == "auto":
                return ThemeMode.AUTO
            else:
                return ThemeMode.LIGHT
                
        except Exception as e:
            logging.error(f"テーマモード取得エラー: {e}")
            return ThemeMode.LIGHT
    
    def set_theme_mode(self, mode: ThemeMode) -> bool:
        """
        テーマモードを設定
        
        Args:
            mode: テーマモード
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            if mode == ThemeMode.DARK:
                self._settings.theme_mode = "dark"
            elif mode == ThemeMode.AUTO:
                self._settings.theme_mode = "auto"
            else:
                self._settings.theme_mode = "light"
            
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"テーマモード設定エラー: {e}")
            return False
    
    def get_auto_detect_system(self) -> bool:
        """システムテーマ自動検出設定を取得"""
        return self._settings.auto_detect_system
    
    def set_auto_detect_system(self, enabled: bool) -> bool:
        """
        システムテーマ自動検出を設定
        
        Args:
            enabled: 有効フラグ
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            self._settings.auto_detect_system = enabled
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"自動検出設定エラー: {e}")
            return False
    
    def get_font_scale(self) -> float:
        """フォントスケールを取得"""
        return self._settings.font_scale
    
    def set_font_scale(self, scale: float) -> bool:
        """
        フォントスケールを設定
        
        Args:
            scale: スケール倍率
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            if scale <= 0:
                scale = 1.0
            
            self._settings.font_scale = scale
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"フォントスケール設定エラー: {e}")
            return False
    
    def get_custom_colors(self) -> Dict[str, str]:
        """カスタムカラー設定を取得"""
        return self._settings.custom_colors.copy()
    
    def set_custom_color(self, color_name: str, color_value: str) -> bool:
        """
        カスタムカラーを設定
        
        Args:
            color_name: カラー名
            color_value: カラー値
            
        Returns:
            bool: 設定成功フラグ
        """
        try:
            self._settings.custom_colors[color_name] = color_value
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"カスタムカラー設定エラー: {e}")
            return False
    
    def remove_custom_color(self, color_name: str) -> bool:
        """
        カスタムカラーを削除
        
        Args:
            color_name: カラー名
            
        Returns:
            bool: 削除成功フラグ
        """
        try:
            if color_name in self._settings.custom_colors:
                del self._settings.custom_colors[color_name]
                return self.save_settings()
            
            return True
            
        except Exception as e:
            logging.error(f"カスタムカラー削除エラー: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """
        設定をデフォルトにリセット
        
        Returns:
            bool: リセット成功フラグ
        """
        try:
            self._settings = ThemeSettings()
            return self.save_settings()
            
        except Exception as e:
            logging.error(f"設定リセットエラー: {e}")
            return False
    
    def export_settings(self, export_file: str) -> bool:
        """
        設定をエクスポート
        
        Args:
            export_file: エクスポート先ファイル
            
        Returns:
            bool: エクスポート成功フラグ
        """
        try:
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(asdict(self._settings), f, indent=2, ensure_ascii=False)
            
            logging.info(f"設定エクスポート成功: {export_file}")
            return True
            
        except Exception as e:
            logging.error(f"設定エクスポートエラー: {e}")
            return False
    
    def import_settings(self, import_file: str) -> bool:
        """
        設定をインポート
        
        Args:
            import_file: インポート元ファイル
            
        Returns:
            bool: インポート成功フラグ
        """
        try:
            if not os.path.exists(import_file):
                logging.error(f"インポートファイルが存在しません: {import_file}")
                return False
            
            with open(import_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # バリデーション
            if not self._validate_import_data(data):
                logging.error("インポートデータのバリデーション失敗")
                return False
            
            # 設定更新
            self._settings = ThemeSettings(
                current_theme=data.get("current_theme", "light"),
                theme_mode=data.get("theme_mode", "light"),
                auto_detect_system=data.get("auto_detect_system", True),
                font_scale=data.get("font_scale", 1.0),
                custom_colors=data.get("custom_colors", {}),
                last_updated=data.get("last_updated", ""),
                version=self._settings.version  # 現在のバージョンを保持
            )
            
            success = self.save_settings()
            if success:
                logging.info(f"設定インポート成功: {import_file}")
            
            return success
            
        except Exception as e:
            logging.error(f"設定インポートエラー: {e}")
            return False
    
    def _validate_import_data(self, data: Dict[str, Any]) -> bool:
        """インポートデータを検証"""
        try:
            # 必要なフィールドチェック
            required_fields = ["current_theme", "theme_mode"]
            for field in required_fields:
                if field not in data:
                    logging.error(f"必須フィールド不足: {field}")
                    return False
            
            # 値の範囲チェック
            if data.get("font_scale", 1.0) <= 0:
                logging.error("無効なフォントスケール値")
                return False
            
            if data.get("theme_mode") not in ["light", "dark", "auto"]:
                logging.error("無効なテーマモード")
                return False
            
            return True
            
        except Exception as e:
            logging.error(f"インポートデータ検証エラー: {e}")
            return False
    
    def add_settings_watcher(self, callback: Callable):
        """
        設定変更監視コールバックを追加
        
        Args:
            callback: 変更時に呼び出される関数
        """
        if callback not in self._watchers:
            self._watchers.append(callback)
    
    def remove_settings_watcher(self, callback: Callable):
        """
        設定変更監視コールバックを削除
        
        Args:
            callback: 削除する関数
        """
        if callback in self._watchers:
            self._watchers.remove(callback)
    
    def _notify_watchers(self):
        """設定変更を監視者に通知"""
        for watcher in self._watchers:
            try:
                watcher(self._settings)
            except Exception as e:
                logging.error(f"設定変更通知エラー: {e}")
    
    def get_settings_summary(self) -> Dict[str, Any]:
        """設定のサマリーを取得"""
        return {
            "current_theme": self._settings.current_theme,
            "theme_mode": self._settings.theme_mode,
            "auto_detect_system": self._settings.auto_detect_system,
            "font_scale": self._settings.font_scale,
            "custom_colors_count": len(self._settings.custom_colors),
            "last_updated": self._settings.last_updated,
            "version": self._settings.version,
            "settings_file": self._settings_file
        }
