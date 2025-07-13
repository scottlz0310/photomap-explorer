"""
ログ出力ブリッジ

debug_logger.pyからloggingモジュールへの移行を簡単にするためのブリッジユーティリティ
"""

import logging
from typing import Callable, Optional
from utils.debug_logger import debug, info, warning, error, verbose


class LoggingBridge:
    """ログ出力の統一インターフェース"""
    
    def __init__(self, logger_name: str = __name__, use_standard_logger: bool = False):
        """
        ログブリッジを初期化
        
        Args:
            logger_name: ロガー名
            use_standard_logger: Trueの場合、標準loggingを使用。Falseの場合debug_loggerを使用
        """
        self.logger_name = logger_name
        self.use_standard_logger = use_standard_logger
        
        if use_standard_logger:
            self.logger = logging.getLogger(logger_name)
        else:
            self.logger = None
    
    def log_debug(self, message: str, *args, **kwargs) -> None:
        """デバッグレベルログ"""
        if self.use_standard_logger and self.logger:
            self.logger.debug(message, *args, **kwargs)
        else:
            debug(message)
    
    def log_info(self, message: str, *args, **kwargs) -> None:
        """情報レベルログ"""
        if self.use_standard_logger and self.logger:
            self.logger.info(message, *args, **kwargs)
        else:
            info(message)
    
    def log_warning(self, message: str, *args, **kwargs) -> None:
        """警告レベルログ"""
        if self.use_standard_logger and self.logger:
            self.logger.warning(message, *args, **kwargs)
        else:
            warning(message)
    
    def log_error(self, message: str, *args, **kwargs) -> None:
        """エラーレベルログ"""
        if self.use_standard_logger and self.logger:
            self.logger.error(message, *args, **kwargs)
        else:
            error(message)
    
    def log_verbose(self, message: str, *args, **kwargs) -> None:
        """詳細レベルログ"""
        if self.use_standard_logger and self.logger:
            self.logger.debug(f"[VERBOSE] {message}", *args, **kwargs)
        else:
            verbose(message)
    
    def with_context(self, context: str) -> 'ContextualLogger':
        """コンテキスト付きロガーを作成"""
        return ContextualLogger(self, context)


class ContextualLogger:
    """コンテキスト情報付きロガー"""
    
    def __init__(self, bridge: LoggingBridge, context: str):
        self.bridge = bridge
        self.context = context
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """コンテキスト付きデバッグログ"""
        self.bridge.log_debug(f"[{self.context}] {message}", *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """コンテキスト付き情報ログ"""
        self.bridge.log_info(f"[{self.context}] {message}", *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """コンテキスト付き警告ログ"""
        self.bridge.log_warning(f"[{self.context}] {message}", *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """コンテキスト付きエラーログ"""
        self.bridge.log_error(f"[{self.context}] {message}", *args, **kwargs)
    
    def verbose(self, message: str, *args, **kwargs) -> None:
        """コンテキスト付き詳細ログ"""
        self.bridge.log_verbose(f"[{self.context}] {message}", *args, **kwargs)


# 簡単移行用のファクトリ関数
def create_logger(name: str, use_standard: bool = False) -> LoggingBridge:
    """ログブリッジを作成"""
    return LoggingBridge(name, use_standard)


def create_contextual_logger(name: str, context: str, use_standard: bool = False) -> ContextualLogger:
    """コンテキスト付きロガーを作成"""
    bridge = LoggingBridge(name, use_standard)
    return bridge.with_context(context)


# グローバル設定
_USE_STANDARD_LOGGING = False


def set_standard_logging(enabled: bool) -> None:
    """グローバルでの標準ログ使用を設定"""
    global _USE_STANDARD_LOGGING
    _USE_STANDARD_LOGGING = enabled


def get_theme_logger(context: str = "Theme") -> ContextualLogger:
    """テーマシステム用ロガーを取得"""
    return create_contextual_logger("photomap.theme", context, _USE_STANDARD_LOGGING)


def get_ui_logger(context: str = "UI") -> ContextualLogger:
    """UI系用ロガーを取得"""
    return create_contextual_logger("photomap.ui", context, _USE_STANDARD_LOGGING)


def get_system_logger(context: str = "System") -> ContextualLogger:
    """システム系用ロガーを取得"""
    return create_contextual_logger("photomap.system", context, _USE_STANDARD_LOGGING)
