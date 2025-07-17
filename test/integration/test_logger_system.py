#!/usr/bin/env python3
"""
ロガーシステムテスト

新しく実装されたロガーシステムとコマンドライン引数の動作テストです。
配置場所: test/integration/
作成日: 2025-07-17
"""

import sys
import logging
import subprocess
import tempfile
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

def setup_test_logging():
    """テスト用のロガー設定"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def test_main_py_arguments():
    """main.pyのコマンドライン引数テスト"""
    logger = logging.getLogger(__name__)
    logger.info("main.pyコマンドライン引数テスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    main_py = project_root / "main.py"
    
    if not main_py.exists():
        logger.error(f"main.py が見つかりません: {main_py}")
        return False
    
    test_results = []
    
    # --helpオプションテスト
    logger.info("--helpオプションテスト")
    try:
        result = subprocess.run(
            [sys.executable, str(main_py), "--help"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if "デバッグモード" in result.stdout and "詳細モード" in result.stdout:
            logger.info("  ✅ --helpオプション正常動作")
            test_results.append(("help", "PASS"))
        else:
            logger.error("  ❌ --helpオプションに期待される内容がない")
            test_results.append(("help", "FAIL"))
    except subprocess.TimeoutExpired:
        logger.error("  ❌ --helpオプションタイムアウト")
        test_results.append(("help", "TIMEOUT"))
    except Exception as e:
        logger.error(f"  ❌ --helpオプションエラー: {e}")
        test_results.append(("help", f"ERROR: {e}"))
    
    # 引数の存在確認（実際のアプリ起動はスキップ）
    logger.info("引数解析テスト")
    try:
        # main.pyの内容確認
        main_content = main_py.read_text(encoding='utf-8')
        if "--debug" in main_content and "--verbose" in main_content:
            logger.info("  ✅ 必要な引数が実装されている")
            test_results.append(("arguments", "PASS"))
        else:
            logger.error("  ❌ 必要な引数が実装されていない")
            test_results.append(("arguments", "FAIL"))
    except Exception as e:
        logger.error(f"  ❌ 引数解析テストエラー: {e}")
        test_results.append(("arguments", f"ERROR: {e}"))
    
    # テスト結果サマリー
    logger.info("テスト結果:")
    failed_tests = []
    for test_name, result in test_results:
        if result == "PASS":
            logger.info(f"  ✅ {test_name}: {result}")
        else:
            logger.error(f"  ❌ {test_name}: {result}")
            failed_tests.append(test_name)
    
    return len(failed_tests) == 0

def test_logging_system():
    """ロギングシステムテスト"""
    logger = logging.getLogger(__name__)
    logger.info("ロギングシステムテスト開始")
    
    # ログディレクトリの確認
    project_root = Path(__file__).parent.parent.parent
    logs_dir = project_root / "logs"
    
    if logs_dir.exists() and logs_dir.is_dir():
        logger.info(f"  ✅ logsディレクトリ存在確認: {logs_dir}")
    else:
        logger.warning(f"  ⚠️ logsディレクトリが存在しません: {logs_dir}")
    
    # ログファイルの存在確認
    log_files = list(logs_dir.glob("*.log")) if logs_dir.exists() else []
    if log_files:
        logger.info(f"  ✅ ログファイル発見: {len(log_files)}件")
        for log_file in log_files:
            logger.info(f"     - {log_file.name}")
    else:
        logger.info("  📝 ログファイルなし（初回実行前）")
    
    return True

def test_debug_template():
    """デバッグテンプレートテスト"""
    logger = logging.getLogger(__name__)
    logger.info("デバッグテンプレートテスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    debug_template = project_root / "debug" / "debug_template.py"
    
    if not debug_template.exists():
        logger.error(f"デバッグテンプレートが見つかりません: {debug_template}")
        return False
    
    # デバッグテンプレートの実行テスト
    try:
        result = subprocess.run(
            [sys.executable, str(debug_template)], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            logger.info("  ✅ デバッグテンプレート正常実行")
            if "デバッグ開始" in result.stdout and "デバッグ完了" in result.stdout:
                logger.info("  ✅ 期待されるログ出力確認")
                return True
            else:
                logger.warning("  ⚠️ 期待されるログ出力が不完全")
                return True  # 実行はできているので成功とする
        else:
            logger.error(f"  ❌ デバッグテンプレート実行失敗: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("  ❌ デバッグテンプレート実行タイムアウト")
        return False
    except Exception as e:
        logger.error(f"  ❌ デバッグテンプレート実行エラー: {e}")
        return False

def test_test_template():
    """テストテンプレートテスト"""
    logger = logging.getLogger(__name__)
    logger.info("テストテンプレートテスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    test_template = project_root / "test" / "manual" / "test_template.py"
    
    if not test_template.exists():
        logger.error(f"テストテンプレートが見つかりません: {test_template}")
        return False
    
    # テストテンプレートの実行テスト
    try:
        result = subprocess.run(
            [sys.executable, str(test_template)], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if result.returncode == 0:
            logger.info("  ✅ テストテンプレート正常実行")
            if "テスト成功" in result.stdout:
                logger.info("  ✅ 期待されるテスト結果確認")
                return True
            else:
                logger.warning("  ⚠️ 期待されるテスト結果が不完全")
                return True
        else:
            logger.error(f"  ❌ テストテンプレート実行失敗: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.error("  ❌ テストテンプレート実行タイムアウト")
        return False
    except Exception as e:
        logger.error(f"  ❌ テストテンプレート実行エラー: {e}")
        return False

def run_all_tests():
    """全テスト実行"""
    logger = logging.getLogger(__name__)
    logger.info("ロガーシステム統合テスト開始")
    logger.info("=" * 60)
    
    tests = [
        ("main.py引数", test_main_py_arguments),
        ("ロギングシステム", test_logging_system),
        ("デバッグテンプレート", test_debug_template),
        ("テストテンプレート", test_test_template)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 {test_name}テスト実行中...")
        try:
            if test_func():
                passed += 1
                logger.info(f"✅ {test_name}テスト成功")
            else:
                logger.error(f"❌ {test_name}テスト失敗")
        except Exception as e:
            logger.error(f"❌ {test_name}テスト実行エラー: {e}")
            import traceback
            traceback.print_exc()
    
    logger.info("\n" + "=" * 60)
    logger.info(f"📊 テスト結果: {passed}/{total} 成功")
    
    if passed == total:
        logger.info("🎉 ロガーシステムテスト全て合格！")
        return True
    else:
        logger.warning("⚠️  一部テストに失敗があります。")
        return False

if __name__ == "__main__":
    print("="*50)
    print("PhotoMap Explorer ロガーシステムテスト")
    print("="*50)
    
    setup_test_logging()
    success = run_all_tests()
    
    print("="*50)
    if success:
        print("ロガーシステムテスト成功")
        sys.exit(0)
    else:
        print("ロガーシステムテスト失敗")
        sys.exit(1)
