"""
アプリケーション制御モジュール

このモジュールはアプリケーション全体の初期化、ライフサイクル管理、
および主要なサービスの協調を担当します。
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from .config import Config, Environment
from ..utils.exceptions import ApplicationError, ConfigurationError
from ..utils.constants import APPLICATION_NAME, APPLICATION_VERSION


class Application:
    """
    アプリケーション制御クラス
    
    アプリケーションの初期化、設定の読み込み、ロギングの設定、
    および全体的な実行制御を行います。
    """
    
    def __init__(self, config_path: Optional[Path] = None):
        """
        アプリケーションを初期化
        
        Args:
            config_path: 設定ファイルのパス（Noneの場合はデフォルト設定を使用）
        """
        self.config: Optional[Config] = None
        self.logger: Optional[logging.Logger] = None
        self._initialized = False
        self._config_path = config_path
    
    def initialize(self) -> None:
        """
        アプリケーションを初期化します
        
        Raises:
            ApplicationError: 初期化に失敗した場合
            ConfigurationError: 設定の読み込みに失敗した場合
        """
        try:
            # 設定を読み込み
            self._load_configuration()
            
            # ロギングを設定
            self._setup_logging()
            
            # アプリケーション情報をログ出力
            self.logger.info(f"{APPLICATION_NAME} v{APPLICATION_VERSION} 開始")
            self.logger.info(f"環境: {self.config.environment.value}")
            
            self._initialized = True
            
        except Exception as e:
            raise ApplicationError(f"アプリケーションの初期化に失敗しました: {e}") from e
    
    def _load_configuration(self) -> None:
        """設定を読み込みます"""
        try:
            if self._config_path and self._config_path.exists():
                # カスタム設定ファイルから読み込み（将来実装）
                self.config = Config()
                # TODO: JSONやYAMLからの設定読み込み機能を実装
            else:
                # デフォルト設定を使用
                self.config = Config()
                
        except Exception as e:
            raise ConfigurationError(f"設定の読み込みに失敗しました: {e}") from e
    
    def _setup_logging(self) -> None:
        """ロギングを設定します"""
        # ロガーを取得
        self.logger = logging.getLogger(APPLICATION_NAME)
        self.logger.setLevel(self.config.log_level)
        
        # ハンドラーが既に設定されている場合はクリア
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # コンソールハンドラーを追加
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.config.log_level)
        
        # フォーマッターを設定
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
        
        # 開発環境の場合はファイルハンドラーも追加
        if self.config.environment == Environment.DEVELOPMENT:
            try:
                log_dir = Path("logs")
                log_dir.mkdir(exist_ok=True)
                
                file_handler = logging.FileHandler(
                    log_dir / "application.log", 
                    encoding='utf-8'
                )
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(formatter)
                
                self.logger.addHandler(file_handler)
                
            except Exception as e:
                # ファイルログの設定に失敗してもアプリケーションは継続
                print(f"警告: ファイルログの設定に失敗しました: {e}")
    
    def is_initialized(self) -> bool:
        """アプリケーションが初期化されているかを確認"""
        return self._initialized
    
    def shutdown(self) -> None:
        """アプリケーションを終了します"""
        if self.logger:
            self.logger.info(f"{APPLICATION_NAME} 終了")
        
        # リソースのクリーンアップ（必要に応じて拡張）
        self._initialized = False
    
    def get_config(self) -> Config:
        """設定オブジェクトを取得"""
        if not self._initialized:
            raise ApplicationError("アプリケーションが初期化されていません")
        return self.config
    
    def get_logger(self) -> logging.Logger:
        """ロガーを取得"""
        if not self._initialized:
            raise ApplicationError("アプリケーションが初期化されていません")
        return self.logger


# グローバルアプリケーションインスタンス
_app_instance: Optional[Application] = None


def get_application() -> Application:
    """
    グローバルアプリケーションインスタンスを取得
    
    Returns:
        Application: アプリケーションインスタンス
        
    Raises:
        ApplicationError: アプリケーションが初期化されていない場合
    """
    global _app_instance
    if _app_instance is None or not _app_instance.is_initialized():
        raise ApplicationError("アプリケーションが初期化されていません")
    return _app_instance


def initialize_application(config_path: Optional[Path] = None) -> Application:
    """
    グローバルアプリケーションインスタンスを初期化
    
    Args:
        config_path: 設定ファイルのパス
        
    Returns:
        Application: 初期化されたアプリケーションインスタンス
    """
    global _app_instance
    _app_instance = Application(config_path)
    _app_instance.initialize()
    return _app_instance


def shutdown_application() -> None:
    """グローバルアプリケーションインスタンスを終了"""
    global _app_instance
    if _app_instance:
        _app_instance.shutdown()
        _app_instance = None
