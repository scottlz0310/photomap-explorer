#!/usr/bin/env python3
"""
デバッグスクリプトテンプレート
配置場所: debug/
作成日: 2025-07-17

使用方法:
1. このファイルをコピーして新しいデバッグスクリプトを作成
2. debug_specific_feature() 関数内にデバッグロジックを実装
3. python debug/debug_template.py で実行
"""

import sys
import logging
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

def setup_debug_logging():
    """デバッグ用のロガー設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()  # コンソールのみに出力
        ]
    )

def debug_specific_feature():
    """
    デバッグ対象の機能
    
    ここに具体的なデバッグロジックを記述してください。
    """
    logger = logging.getLogger(__name__)
    
    logger.debug("デバッグ開始")
    
    try:
        # ここにデバッグコードを記述
        logger.info("デバッグ処理実行中...")
        
        # 例: モジュールのインポートテスト
        # from logic.image_utils import ImageProcessor
        # processor = ImageProcessor()
        # logger.debug(f"ImageProcessor インスタンス作成: {processor}")
        
        logger.info("デバッグ処理完了")
        
    except Exception as e:
        logger.error(f"デバッグ中にエラーが発生: {e}", exc_info=True)
        raise
    finally:
        logger.debug("デバッグ終了")

if __name__ == "__main__":
    print("="*50)
    print("PhotoMap Explorer デバッグスクリプト")
    print("="*50)
    
    setup_debug_logging()
    debug_specific_feature()
    
    print("="*50)
    print("デバッグ完了")
    print("="*50)
