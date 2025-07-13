"""
ログレベル制御モジュール

デバッグ出力の表示/非表示を一元管理します。
コマンドライン引数に応じてログレベルを調整します。
"""

import sys
import logging
from typing import Any

class DebugLogger:
    """
    デバッグログの統一管理クラス
    
    --debug, --verbose フラグに応じてログ出力を制御します。
    """
    
    # ログレベル定数
    SILENT = 0     # エラーのみ
    NORMAL = 1     # 基本情報のみ  
    VERBOSE = 2    # 詳細情報
    DEBUG = 3      # 全てのデバッグ情報
    
    _instance = None
    _level = SILENT  # デフォルトはサイレント
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def set_level(cls, level: int):
        """ログレベルを設定"""
        cls._level = level
    
    @classmethod
    def set_level_from_args(cls, args=None):
        """コマンドライン引数からログレベルを設定"""
        if args is None:
            args = sys.argv[1:]
        
        if '--debug' in args:
            cls._level = cls.DEBUG
        elif '--verbose' in args or '-v' in args:
            cls._level = cls.VERBOSE
        elif '--normal' in args:
            cls._level = cls.NORMAL
        else:
            # デフォルトはサイレント（エラーのみ）
            cls._level = cls.SILENT
    
    @classmethod
    def debug(cls, message: str, *args):
        """デバッグレベルのログ出力（🔧）"""
        if cls._level >= cls.DEBUG:
            if args:
                message = message.format(*args)
            print(f"🔧 {message}")
    
    @classmethod
    def verbose(cls, message: str, *args):
        """詳細レベルのログ出力（📊）"""
        if cls._level >= cls.VERBOSE:
            if args:
                message = message.format(*args)
            print(f"📊 {message}")
    
    @classmethod
    def info(cls, message: str, *args):
        """情報レベルのログ出力（✅）"""
        if cls._level >= cls.VERBOSE:  # VERBOSEレベル以上で表示
            if args:
                message = message.format(*args)
            print(f"✅ {message}")
    
    @classmethod
    def warning(cls, message: str, *args):
        """警告レベルのログ出力（⚠️）"""
        if cls._level >= cls.NORMAL:  # NORMALレベル以上で表示
            if args:
                message = message.format(*args)
            print(f"⚠️ {message}")
    
    @classmethod
    def error(cls, message: str, *args):
        """エラーレベルのログ出力（❌）"""
        # エラーは常に表示
        if args:
            message = message.format(*args)
        print(f"❌ {message}")
    
    @classmethod
    def success(cls, message: str, *args):
        """成功ログ（🎉）"""
        if cls._level >= cls.VERBOSE:  # VERBOSEレベル以上で表示
            if args:
                message = message.format(*args)
            print(f"🎉 {message}")

# グローバルインスタンス
logger = DebugLogger()

# 便利関数のエクスポート
debug = logger.debug
verbose = logger.verbose
info = logger.info
warning = logger.warning
error = logger.error
success = logger.success
set_level = logger.set_level
set_level_from_args = logger.set_level_from_args
