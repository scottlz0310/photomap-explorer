"""
システムテーマ連携モジュール

このモジュールは presentation/themes/theme_manager.py から分離された
OS システム設定との連携機能を提供します。
"""

import sys
import logging
from typing import Optional, Dict, Any
from PyQt5.QtCore import QObject, QTimer, pyqtSignal
from enum import Enum


class ThemeMode(Enum):
    """テーマモード定義（ローカル定義）"""
    LIGHT = "light"
    DARK = "dark"
    AUTO = "auto"
    CUSTOM = "custom"


class SystemThemeDetector(QObject):
    """
    システムテーマ検出クラス
    
    OS（Windows/macOS/Linux）のシステム設定から
    ダークモード/ライトモードを検出
    """
    
    # シグナル
    system_theme_changed = pyqtSignal(str)  # システムテーマ変更検出
    detection_failed = pyqtSignal(str)      # 検出失敗
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # プラットフォーム検出
        self.platform = sys.platform
        self.is_windows = self.platform.startswith("win")
        self.is_macos = self.platform == "darwin"
        self.is_linux = self.platform.startswith("linux")
        
        # 監視設定
        self.monitoring_enabled = False
        self.monitor_timer: Optional[QTimer] = None
        self.check_interval = 5000  # 5秒間隔
        self.last_detected_theme: Optional[ThemeMode] = None
        
        logging.info(f"システムテーマ検出器初期化 - プラットフォーム: {self.platform}")
    
    def detect_system_theme(self) -> ThemeMode:
        """
        現在のシステムテーマを検出
        
        Returns:
            ThemeMode: 検出されたテーマモード
        """
        try:
            if self.is_windows:
                return self._detect_windows_theme()
            elif self.is_macos:
                return self._detect_macos_theme()
            elif self.is_linux:
                return self._detect_linux_theme()
            else:
                logging.warning(f"未対応プラットフォーム: {self.platform}")
                return ThemeMode.LIGHT
                
        except Exception as e:
            logging.error(f"システムテーマ検出エラー: {e}")
            self.detection_failed.emit(str(e))
            return ThemeMode.LIGHT
    
    def _detect_windows_theme(self) -> ThemeMode:
        """Windows システムテーマ検出"""
        try:
            import winreg
            
            # アプリケーションテーマ設定
            app_theme = self._get_windows_app_theme()
            if app_theme is not None:
                return app_theme
            
            # システムテーマ設定（フォールバック）
            system_theme = self._get_windows_system_theme()
            return system_theme or ThemeMode.LIGHT
            
        except ImportError:
            logging.warning("winreg モジュールが利用できません")
            return ThemeMode.LIGHT
        except Exception as e:
            logging.error(f"Windows テーマ検出エラー: {e}")
            return ThemeMode.LIGHT
    
    def _get_windows_app_theme(self) -> Optional[ThemeMode]:
        """Windows アプリケーションテーマ設定を取得"""
        try:
            import winreg  # type: ignore
            
            key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:  # type: ignore
                # AppsUseLightTheme: 0=ダーク, 1=ライト
                apps_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")  # type: ignore
                
                if apps_light_theme == 0:
                    logging.debug("Windows: アプリはダークテーマ")
                    return ThemeMode.DARK
                else:
                    logging.debug("Windows: アプリはライトテーマ")
                    return ThemeMode.LIGHT
                    
        except (OSError, FileNotFoundError) as e:
            logging.debug(f"Windows アプリテーマ設定読み取り失敗: {e}")
            return None
        except Exception as e:
            logging.error(f"Windows アプリテーマ読み取りエラー: {e}")
            return None
    
    def _get_windows_system_theme(self) -> Optional[ThemeMode]:
        """Windows システムテーマ設定を取得"""
        try:
            import winreg  # type: ignore
            
            key_path = r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize"
            
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path) as key:  # type: ignore
                # SystemUsesLightTheme: 0=ダーク, 1=ライト
                system_light_theme, _ = winreg.QueryValueEx(key, "SystemUsesLightTheme")  # type: ignore
                
                if system_light_theme == 0:
                    logging.debug("Windows: システムはダークテーマ")
                    return ThemeMode.DARK
                else:
                    logging.debug("Windows: システムはライトテーマ")
                    return ThemeMode.LIGHT
                    
        except (OSError, FileNotFoundError) as e:
            logging.debug(f"Windows システムテーマ設定読み取り失敗: {e}")
            return None
        except Exception as e:
            logging.error(f"Windows システムテーマ読み取りエラー: {e}")
            return None
    
    def _detect_macos_theme(self) -> ThemeMode:
        """macOS システムテーマ検出"""
        try:
            import subprocess
            
            # AppleInterfaceStyle を確認
            result = subprocess.run([
                "defaults", "read", "-g", "AppleInterfaceStyle"
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                interface_style = result.stdout.strip()
                if interface_style.lower() == "dark":
                    logging.debug("macOS: ダークテーマ")
                    return ThemeMode.DARK
            
            # エラーまたは設定なしの場合はライト
            logging.debug("macOS: ライトテーマ")
            return ThemeMode.LIGHT
            
        except subprocess.TimeoutExpired:
            logging.warning("macOS テーマ検出がタイムアウト")
            return ThemeMode.LIGHT
        except FileNotFoundError:
            logging.warning("macOS defaults コマンドが見つかりません")
            return ThemeMode.LIGHT
        except Exception as e:
            logging.error(f"macOS テーマ検出エラー: {e}")
            return ThemeMode.LIGHT
    
    def _detect_linux_theme(self) -> ThemeMode:
        """Linux システムテーマ検出"""
        try:
            # GNOME デスクトップ環境
            gnome_theme = self._detect_gnome_theme()
            if gnome_theme is not None:
                return gnome_theme
            
            # KDE デスクトップ環境
            kde_theme = self._detect_kde_theme()
            if kde_theme is not None:
                return kde_theme
            
            # GTK テーマ
            gtk_theme = self._detect_gtk_theme()
            if gtk_theme is not None:
                return gtk_theme
            
            # フォールバック
            logging.debug("Linux: デフォルトライトテーマ")
            return ThemeMode.LIGHT
            
        except Exception as e:
            logging.error(f"Linux テーマ検出エラー: {e}")
            return ThemeMode.LIGHT
    
    def _detect_gnome_theme(self) -> Optional[ThemeMode]:
        """GNOME デスクトップテーマ検出"""
        try:
            import subprocess
            
            # gsettings を使用してGNOMEテーマを確認
            result = subprocess.run([
                "gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                theme_name = result.stdout.strip().strip("'\"").lower()
                
                # ダークテーマキーワードを確認
                dark_keywords = ["dark", "adwaita-dark", "yaru-dark"]
                if any(keyword in theme_name for keyword in dark_keywords):
                    logging.debug(f"GNOME: ダークテーマ ({theme_name})")
                    return ThemeMode.DARK
                else:
                    logging.debug(f"GNOME: ライトテーマ ({theme_name})")
                    return ThemeMode.LIGHT
            
            return None
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logging.debug("GNOME テーマ検出失敗")
            return None
        except Exception as e:
            logging.debug(f"GNOME テーマ検出エラー: {e}")
            return None
    
    def _detect_kde_theme(self) -> Optional[ThemeMode]:
        """KDE デスクトップテーマ検出"""
        try:
            import subprocess
            
            # kreadconfig5 を使用してKDEテーマを確認
            result = subprocess.run([
                "kreadconfig5", "--group", "General", "--key", "ColorScheme"
            ], capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                color_scheme = result.stdout.strip().lower()
                
                # ダークテーマキーワードを確認
                dark_keywords = ["dark", "breeze dark", "breezedark"]
                if any(keyword in color_scheme for keyword in dark_keywords):
                    logging.debug(f"KDE: ダークテーマ ({color_scheme})")
                    return ThemeMode.DARK
                else:
                    logging.debug(f"KDE: ライトテーマ ({color_scheme})")
                    return ThemeMode.LIGHT
            
            return None
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logging.debug("KDE テーマ検出失敗")
            return None
        except Exception as e:
            logging.debug(f"KDE テーマ検出エラー: {e}")
            return None
    
    def _detect_gtk_theme(self) -> Optional[ThemeMode]:
        """GTK テーマ検出"""
        try:
            import os
            
            # GTK設定ファイルを確認
            gtk_config_paths = [
                os.path.expanduser("~/.config/gtk-3.0/settings.ini"),
                os.path.expanduser("~/.gtkrc-2.0")
            ]
            
            for config_path in gtk_config_paths:
                if os.path.exists(config_path):
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        
                        # ダークテーマキーワードを確認
                        dark_keywords = ["dark", "adwaita-dark"]
                        if any(keyword in content for keyword in dark_keywords):
                            logging.debug(f"GTK: ダークテーマ ({config_path})")
                            return ThemeMode.DARK
            
            logging.debug("GTK: ライトテーマ")
            return ThemeMode.LIGHT
            
        except Exception as e:
            logging.debug(f"GTK テーマ検出エラー: {e}")
            return None
    
    def start_monitoring(self):
        """システムテーマ変更の監視を開始"""
        try:
            if self.monitoring_enabled:
                logging.debug("システムテーマ監視は既に有効")
                return
            
            # 初期テーマを記録
            self.last_detected_theme = self.detect_system_theme()
            
            # タイマー設定
            self.monitor_timer = QTimer()
            self.monitor_timer.timeout.connect(self._check_theme_change)
            self.monitor_timer.start(self.check_interval)
            
            self.monitoring_enabled = True
            logging.info(f"システムテーマ監視開始 - 間隔: {self.check_interval}ms")
            
        except Exception as e:
            logging.error(f"システムテーマ監視開始エラー: {e}")
    
    def stop_monitoring(self):
        """システムテーマ変更の監視を停止"""
        try:
            if not self.monitoring_enabled:
                logging.debug("システムテーマ監視は既に無効")
                return
            
            if self.monitor_timer:
                self.monitor_timer.stop()
                self.monitor_timer = None
            
            self.monitoring_enabled = False
            logging.info("システムテーマ監視停止")
            
        except Exception as e:
            logging.error(f"システムテーマ監視停止エラー: {e}")
    
    def _check_theme_change(self):
        """テーマ変更をチェック"""
        try:
            current_theme = self.detect_system_theme()
            
            if current_theme != self.last_detected_theme:
                logging.info(f"システムテーマ変更検出: {self.last_detected_theme} → {current_theme}")
                self.last_detected_theme = current_theme
                self.system_theme_changed.emit(current_theme.value)
            
        except Exception as e:
            logging.error(f"テーマ変更チェックエラー: {e}")
    
    def set_check_interval(self, interval_ms: int):
        """監視間隔を設定"""
        try:
            if interval_ms < 1000:  # 最小1秒
                interval_ms = 1000
            elif interval_ms > 60000:  # 最大60秒
                interval_ms = 60000
            
            self.check_interval = interval_ms
            
            # 監視中の場合は再起動
            if self.monitoring_enabled and self.monitor_timer:
                self.monitor_timer.stop()
                self.monitor_timer.start(self.check_interval)
            
            logging.info(f"システムテーマ監視間隔変更: {interval_ms}ms")
            
        except Exception as e:
            logging.error(f"監視間隔設定エラー: {e}")
    
    def get_system_info(self) -> Dict[str, Any]:
        """システム情報を取得"""
        try:
            return {
                "platform": self.platform,
                "is_windows": self.is_windows,
                "is_macos": self.is_macos,
                "is_linux": self.is_linux,
                "monitoring_enabled": self.monitoring_enabled,
                "check_interval": self.check_interval,
                "last_detected_theme": self.last_detected_theme.value if self.last_detected_theme else None,
                "current_theme": self.detect_system_theme().value
            }
            
        except Exception as e:
            logging.error(f"システム情報取得エラー: {e}")
            return {"platform": "unknown"}


class SystemThemeSync(QObject):
    """
    システムテーマ同期クラス
    
    SystemThemeDetectorと連携して
    システム設定の変更を自動的にアプリケーションに反映
    """
    
    # シグナル
    auto_theme_changed = pyqtSignal(str)  # 自動テーマ変更
    sync_enabled_changed = pyqtSignal(bool)  # 同期有効/無効変更
    
    def __init__(self, theme_detector: SystemThemeDetector, parent=None):
        super().__init__(parent)
        
        self.detector = theme_detector
        self.sync_enabled = True
        self.auto_mode_active = False
        
        # 検出器と接続
        self.detector.system_theme_changed.connect(self._on_system_theme_changed)
        
        logging.info("システムテーマ同期初期化完了")
    
    def enable_auto_sync(self, enabled: bool = True):
        """自動同期の有効/無効を設定"""
        try:
            self.sync_enabled = enabled
            
            if enabled:
                # 監視開始
                self.detector.start_monitoring()
                
                # 現在のシステムテーマを適用
                current_system_theme = self.detector.detect_system_theme()
                self.auto_theme_changed.emit(current_system_theme.value)
                
                self.auto_mode_active = True
                logging.info("システムテーマ自動同期有効")
            else:
                # 監視停止
                self.detector.stop_monitoring()
                self.auto_mode_active = False
                logging.info("システムテーマ自動同期無効")
            
            self.sync_enabled_changed.emit(enabled)
            
        except Exception as e:
            logging.error(f"自動同期設定エラー: {e}")
    
    def _on_system_theme_changed(self, theme_name: str):
        """システムテーマ変更時の処理"""
        try:
            if self.sync_enabled and self.auto_mode_active:
                logging.info(f"システムテーマ変更により自動テーマ切り替え: {theme_name}")
                self.auto_theme_changed.emit(theme_name)
            
        except Exception as e:
            logging.error(f"システムテーマ変更処理エラー: {e}")
    
    def is_sync_enabled(self) -> bool:
        """同期が有効かどうかを確認"""
        return self.sync_enabled
    
    def is_auto_mode_active(self) -> bool:
        """自動モードが有効かどうかを確認"""
        return self.auto_mode_active
    
    def force_sync(self):
        """強制的にシステムテーマと同期"""
        try:
            if self.sync_enabled:
                current_system_theme = self.detector.detect_system_theme()
                self.auto_theme_changed.emit(current_system_theme.value)
                logging.info(f"強制同期実行: {current_system_theme.value}")
            
        except Exception as e:
            logging.error(f"強制同期エラー: {e}")
    
    def get_sync_status(self) -> Dict[str, Any]:
        """同期状態を取得"""
        try:
            return {
                "sync_enabled": self.sync_enabled,
                "auto_mode_active": self.auto_mode_active,
                "detector_monitoring": self.detector.monitoring_enabled,
                "check_interval": self.detector.check_interval,
                "current_system_theme": self.detector.detect_system_theme().value
            }
            
        except Exception as e:
            logging.error(f"同期状態取得エラー: {e}")
            return {"sync_enabled": False}
