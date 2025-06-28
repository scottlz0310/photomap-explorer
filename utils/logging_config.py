"""
ログ設定 - PhotoMap Explorer

標準出力を整理し、適切なログレベルでメッセージを管理
"""
import logging
import os
import sys

def setup_logging(debug_mode=False):
    """
    ログ設定をセットアップ
    
    Args:
        debug_mode: デバッグモード有効時はコンソールにも出力
    """
    # ログレベル設定
    log_level = logging.DEBUG if debug_mode else logging.WARNING
    
    # ログフォーマット
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ルートロガー設定
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 既存のハンドラーをクリア
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # ファイルハンドラー（常に有効）
    log_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "PhotoMapExplorer", "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    file_handler = logging.FileHandler(
        os.path.join(log_dir, "photomap-explorer.log"),
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # コンソールハンドラー（デバッグモード時のみ）
    if debug_mode:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    return root_logger

def is_debug_mode():
    """デバッグモードかどうかを確認"""
    return os.getenv('DEBUG_MODE') == '1' or '--debug' in sys.argv

# アプリケーション起動時のログ設定
logger = setup_logging(is_debug_mode())
