#!/usr/bin/env python3
"""
全テスト実行スクリプト

すべてのテストを順番に実行して統合的な結果を出力します。
配置場所: test/
作成日: 2025-07-17
"""

import sys
import logging
import subprocess
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

def setup_test_logging():
    """テスト用のロガー設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def run_test_script(script_path, test_name):
    """個別テストスクリプトの実行"""
    logger = logging.getLogger(__name__)
    logger.info(f"\n🧪 {test_name} 実行中...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            timeout=60  # 1分のタイムアウト
        )
        
        if result.returncode == 0:
            logger.info(f"✅ {test_name} 成功")
            # 成功時も出力を表示（重要な情報があるため）
            if result.stdout.strip():
                print(f"\n--- {test_name} 出力 ---")
                print(result.stdout)
                print(f"--- {test_name} 終了 ---")
            return True
        else:
            logger.error(f"❌ {test_name} 失敗")
            if result.stdout.strip():
                print(f"\n--- {test_name} 標準出力 ---")
                print(result.stdout)
            if result.stderr.strip():
                print(f"--- {test_name} エラー出力 ---")
                print(result.stderr)
                print(f"--- {test_name} 終了 ---")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error(f"❌ {test_name} タイムアウト")
        return False
    except Exception as e:
        logger.error(f"❌ {test_name} 実行エラー: {e}")
        return False

def run_all_tests():
    """全テスト実行"""
    logger = logging.getLogger(__name__)
    logger.info("PhotoMap Explorer 統合テストスイート開始")
    logger.info("=" * 70)
    
    project_root = Path(__file__).parent.parent
    
    # テストスクリプトのリスト（実行順序）
    test_scripts = [
        (project_root / "test" / "integration" / "test_directory_structure.py", "ディレクトリ構造テスト"),
        (project_root / "test" / "integration" / "test_logger_system.py", "ロガーシステムテスト"),
        (project_root / "test" / "integration" / "test_refactoring_integration.py", "リファクタリング統合テスト"),
        (project_root / "test" / "manual" / "simple_test.py", "簡易動作確認テスト")
    ]
    
    passed = 0
    total = len(test_scripts)
    results = []
    
    for script_path, test_name in test_scripts:
        if script_path.exists():
            success = run_test_script(script_path, test_name)
            results.append((test_name, "PASS" if success else "FAIL"))
            if success:
                passed += 1
        else:
            logger.error(f"❌ テストスクリプトが見つかりません: {script_path}")
            results.append((test_name, "NOT_FOUND"))
    
    # 結果サマリー
    logger.info("\n" + "=" * 70)
    logger.info("📊 テスト結果サマリー")
    logger.info("=" * 70)
    
    for test_name, result in results:
        if result == "PASS":
            logger.info(f"✅ {test_name}: {result}")
        else:
            logger.error(f"❌ {test_name}: {result}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"📊 総合結果: {passed}/{total} 成功")
    
    if passed == total:
        logger.info("🎉 全テスト合格！システム正常動作確認")
        success_rate = 100
    else:
        failed_count = total - passed
        success_rate = (passed / total) * 100
        logger.warning(f"⚠️ {failed_count}件のテストに失敗 (成功率: {success_rate:.1f}%)")
    
    # 改善提案
    if success_rate < 100:
        logger.info("\n🔧 改善提案:")
        for test_name, result in results:
            if result == "FAIL":
                logger.info(f"  - {test_name}の詳細ログを確認してください")
            elif result == "NOT_FOUND":
                logger.info(f"  - {test_name}スクリプトを作成してください")
    
    return passed == total

def main():
    """メイン実行関数"""
    print("="*70)
    print("PhotoMap Explorer 統合テストスイート")
    print("test2_2_0_gpt4_1 ブランチ検証")
    print("="*70)
    
    setup_test_logging()
    
    # テスト実行
    success = run_all_tests()
    
    print("="*70)
    if success:
        print("🎉 全テスト成功 - システム準備完了")
        print("デバッグ作業を開始できます！")
        return 0
    else:
        print("⚠️ 一部テスト失敗 - 問題を解決してから作業開始してください")
        return 1

if __name__ == "__main__":
    sys.exit(main())
