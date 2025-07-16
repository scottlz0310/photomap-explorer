"""
PhotoMap Explorer デバッグロガー v2.2.0

高機能なデバッグ・ログシステム
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional, Any
from pathlib import Path

# ログレベル定数
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

class PhotoMapLogger:
    """PhotoMap Explorer専用ロガークラス"""
    
    _instance = None
    _logger = None
    _debug_mode = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._logger is None:
            self._setup_logger()
    
    def _setup_logger(self):
        """ロガーの初期設定"""
        self._logger = logging.getLogger('PhotoMapExplorer')
        
        # デフォルトレベル設定（通常は警告以上のみ）
        self._logger.setLevel(logging.WARNING)
        
        # コンソールハンドラー（デフォルトは警告以上のみ表示）
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.WARNING)
        
        # フォーマッター
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        
        # ハンドラー追加
        self._logger.addHandler(console_handler)
        
        # ファイルハンドラー（オプション）
        self._setup_file_handler()
    
    def _setup_file_handler(self):
        """ファイルロガーの設定"""
        try:
            # ログディレクトリ作成
            log_dir = Path.cwd() / "logs"
            log_dir.mkdir(exist_ok=True)
            
            # ログファイル名
            log_file = log_dir / f"photomap_explorer_{datetime.now().strftime('%Y%m%d')}.log"
            
            # ファイルハンドラー作成
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            
            # 詳細フォーマッター
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            
            self._logger.addHandler(file_handler)
            
        except Exception as e:
            print(f"ファイルログ設定エラー: {e}")
    
    def set_debug_mode(self, enabled: bool = True):
        """デバッグモードの設定"""
        self._debug_mode = enabled
        if self._logger and enabled:
            # デバッグモード: すべてのメッセージをコンソールに表示
            for handler in self._logger.handlers:
                if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                    handler.setLevel(logging.DEBUG)
            self._logger.setLevel(logging.DEBUG)
        elif self._logger:
            # 通常モード: 警告以上のみコンソールに表示
            for handler in self._logger.handlers:
                if isinstance(handler, logging.StreamHandler) and handler.stream == sys.stdout:
                    handler.setLevel(logging.WARNING)
            self._logger.setLevel(logging.INFO)
    
    def log(self, level: int, message: str, *args, **kwargs):
        """基本ログ出力"""
        self._logger.log(level, message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """デバッグメッセージ"""
        if self._debug_mode:
            self._logger.debug(f"🐛 {message}", *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """情報メッセージ"""
        self._logger.info(f"ℹ️ {message}", *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """警告メッセージ"""
        self._logger.warning(f"⚠️ {message}", *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """エラーメッセージ"""
        self._logger.error(f"❌ {message}", *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """重大エラーメッセージ"""
        self._logger.critical(f"🔥 {message}", *args, **kwargs)
    
    def verbose(self, message: str, *args, **kwargs):
        """詳細メッセージ（デバッグモード時のみ）"""
        if self._debug_mode:
            self._logger.debug(f"📋 VERBOSE: {message}", *args, **kwargs)

# グローバルロガーインスタンス
_global_logger = PhotoMapLogger()

# パッケージレベル関数（後方互換性のため）
def debug(message: str, *args, **kwargs):
    """デバッグメッセージ"""
    _global_logger.debug(message, *args, **kwargs)

def info(message: str, *args, **kwargs):
    """情報メッセージ"""
    _global_logger.info(message, *args, **kwargs)

def warning(message: str, *args, **kwargs):
    """警告メッセージ"""
    _global_logger.warning(message, *args, **kwargs)

def error(message: str, *args, **kwargs):
    """エラーメッセージ"""
    _global_logger.error(message, *args, **kwargs)

def critical(message: str, *args, **kwargs):
    """重大エラーメッセージ"""
    _global_logger.critical(message, *args, **kwargs)

def verbose(message: str, *args, **kwargs):
    """詳細メッセージ"""
    _global_logger.verbose(message, *args, **kwargs)

def set_debug_mode(enabled: bool = True):
    """デバッグモードの設定"""
    _global_logger.set_debug_mode(enabled)

def get_logger():
    """ロガーインスタンスを取得"""
    return _global_logger

# 起動時ログ
info("PhotoMap Explorer デバッグロガー v2.2.0 初期化完了")
