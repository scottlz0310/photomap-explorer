#!/usr/bin/env python3
"""
ディレクトリ構造テスト

DEBUG_GUIDELINESで定義されたディレクトリ構造とファイル配置ルールの検証
配置場所: test/integration/
作成日: 2025-07-17
"""

import sys
import logging
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

def test_directory_structure():
    """推奨ディレクトリ構造の確認"""
    logger = logging.getLogger(__name__)
    logger.info("ディレクトリ構造テスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    
    # 必須ディレクトリの確認
    required_dirs = [
        "logic",
        "presentation", 
        "ui",
        "test",
        "test/integration",
        "test/manual",
        "debug",
        "logs",
        "docs"
    ]
    
    missing_dirs = []
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists() and dir_path.is_dir():
            logger.info(f"  ✅ {dir_name}/")
        else:
            logger.error(f"  ❌ 不足: {dir_name}/")
            missing_dirs.append(dir_name)
    
    return len(missing_dirs) == 0

def test_file_placement_rules():
    """ファイル配置ルールの確認"""
    logger = logging.getLogger(__name__)
    logger.info("ファイル配置ルールテスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    violations = []
    
    # ルートディレクトリにあってはいけないファイルの確認
    forbidden_patterns = [
        "debug_*.py",
        "test_*.py",
        "*_test.py",
        "simple_*.py"
    ]
    
    logger.info("  ルートディレクトリの不適切ファイル確認:")
    for pattern in forbidden_patterns:
        matching_files = list(project_root.glob(pattern))
        if matching_files:
            for file_path in matching_files:
                if file_path.name not in ["main.py"]:  # main.pyは例外
                    logger.error(f"    ❌ 不適切配置: {file_path.name}")
                    violations.append(f"root/{file_path.name}")
        else:
            logger.info(f"    ✅ {pattern} パターンなし")
    
    # test/ディレクトリの構造確認
    logger.info("  test/ディレクトリ構造確認:")
    test_dir = project_root / "test"
    if test_dir.exists():
        test_files = []
        for subdir in ["integration", "manual"]:
            subdir_path = test_dir / subdir
            if subdir_path.exists():
                py_files = list(subdir_path.glob("*.py"))
                test_files.extend(py_files)
                logger.info(f"    ✅ {subdir}/: {len(py_files)}ファイル")
            else:
                logger.error(f"    ❌ 不足: {subdir}/")
                violations.append(f"test/{subdir}")
    
    # debug/ディレクトリの確認
    logger.info("  debug/ディレクトリ確認:")
    debug_dir = project_root / "debug"
    if debug_dir.exists():
        debug_files = list(debug_dir.glob("*.py"))
        logger.info(f"    ✅ debug/: {len(debug_files)}ファイル")
    else:
        logger.error("    ❌ 不足: debug/")
        violations.append("debug")
    
    return len(violations) == 0

def test_template_files():
    """テンプレートファイルの存在確認"""
    logger = logging.getLogger(__name__)
    logger.info("テンプレートファイルテスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    
    required_templates = [
        "debug/debug_template.py",
        "test/manual/test_template.py"
    ]
    
    missing_templates = []
    for template_path in required_templates:
        file_path = project_root / template_path
        if file_path.exists():
            logger.info(f"  ✅ {template_path}")
            
            # テンプレートの内容確認
            try:
                content = file_path.read_text(encoding='utf-8')
                if "logging" in content and "logger" in content:
                    logger.info(f"    ✅ ロガー使用確認")
                else:
                    logger.warning(f"    ⚠️ ロガー使用不明確")
                    
                if "print(" in content and "print文" not in content:
                    logger.warning(f"    ⚠️ print文使用検出")
                else:
                    logger.info(f"    ✅ print文なし")
                    
            except Exception as e:
                logger.error(f"    ❌ ファイル読み取りエラー: {e}")
        else:
            logger.error(f"  ❌ 不足: {template_path}")
            missing_templates.append(template_path)
    
    return len(missing_templates) == 0

def test_documentation():
    """ドキュメント整備の確認"""
    logger = logging.getLogger(__name__)
    logger.info("ドキュメント整備テスト開始")
    
    project_root = Path(__file__).parent.parent.parent
    
    required_docs = [
        "docs/DEBUG_GUIDELINES.md",
        "docs/DOCUMENT_INDEX.md",
        "README.md"
    ]
    
    missing_docs = []
    for doc_path in required_docs:
        file_path = project_root / doc_path
        if file_path.exists():
            logger.info(f"  ✅ {doc_path}")
            
            # 内容の簡易確認
            try:
                content = file_path.read_text(encoding='utf-8')
                if doc_path == "docs/DEBUG_GUIDELINES.md":
                    if "デバッグ作業の鉄則" in content:
                        logger.info(f"    ✅ 適切な内容確認")
                    else:
                        logger.warning(f"    ⚠️ 期待される内容不明")
                elif doc_path == "README.md":
                    if "開発・デバッグ" in content:
                        logger.info(f"    ✅ デバッグセクション確認")
                    else:
                        logger.warning(f"    ⚠️ デバッグセクション未追加")
            except Exception as e:
                logger.error(f"    ❌ ファイル読み取りエラー: {e}")
        else:
            logger.error(f"  ❌ 不足: {doc_path}")
            missing_docs.append(doc_path)
    
    return len(missing_docs) == 0

def run_all_tests():
    """全テスト実行"""
    logger = logging.getLogger(__name__)
    logger.info("ディレクトリ構造テスト開始")
    logger.info("=" * 60)
    
    tests = [
        ("ディレクトリ構造", test_directory_structure),
        ("ファイル配置ルール", test_file_placement_rules),
        ("テンプレートファイル", test_template_files),
        ("ドキュメント整備", test_documentation)
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
        logger.info("🎉 ディレクトリ構造テスト全て合格！")
        return True
    else:
        logger.warning("⚠️  一部テストに失敗があります。")
        return False

if __name__ == "__main__":
    print("="*50)
    print("PhotoMap Explorer ディレクトリ構造テスト")
    print("="*50)
    
    setup_test_logging()
    success = run_all_tests()
    
    print("="*50)
    if success:
        print("ディレクトリ構造テスト成功")
        sys.exit(0)
    else:
        print("ディレクトリ構造テスト失敗") 
        sys.exit(1)
