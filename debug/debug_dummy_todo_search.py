#!/usr/bin/env python3
"""
デバッグスクリプト: ダミー実装・TODO・先送りコメント調査
配置場所: debug/
作成日: 2025-07-17
"""

import sys
import logging
import os
import re
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def setup_debug_logging():
    """デバッグ用のロガー設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def search_dummy_and_todo():
    """ダミー実装とTODOコメントを検索"""
    logger = logging.getLogger(__name__)
    logger.debug("ダミー実装・TODO調査開始")
    
    # 検索パターン
    patterns = [
        r'(?i)dummy|ダミー',
        r'(?i)todo|TO\s*DO',
        r'(?i)後で実装|あとで実装',
        r'(?i)暫定|仮実装',
        r'(?i)placeholder|プレースホルダー',
        r'(?i)not\s+implemented|未実装',
        r'(?i)fixme|FIX\s*ME',
        r'(?i)hack|ハック',
        r'pass\s*#.*暫定|pass\s*#.*ダミー|pass\s*#.*TODO'
    ]
    
    # 検索対象ディレクトリ
    search_dirs = [
        'presentation/views/functional_main_window',
        'ui/controls',
        'presentation/themes',
        'logic',
        'utils'
    ]
    
    findings = []
    
    for search_dir in search_dirs:
        search_path = project_root / search_dir
        if not search_path.exists():
            logger.warning(f"ディレクトリが存在しません: {search_path}")
            continue
            
        logger.debug(f"検索中: {search_dir}")
        
        # Pythonファイルを再帰的に検索
        for py_file in search_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                for i, line in enumerate(lines, 1):
                    for pattern in patterns:
                        if re.search(pattern, line):
                            relative_path = py_file.relative_to(project_root)
                            findings.append({
                                'file': str(relative_path),
                                'line': i,
                                'content': line.strip(),
                                'pattern': pattern
                            })
                            
            except Exception as e:
                logger.error(f"ファイル読み込みエラー {py_file}: {e}")
    
    # 結果レポート
    logger.debug("=== ダミー実装・TODO調査結果 ===")
    logger.debug(f"総検出数: {len(findings)}")
    
    # ファイル別にグループ化
    files_dict = {}
    for finding in findings:
        file_path = finding['file']
        if file_path not in files_dict:
            files_dict[file_path] = []
        files_dict[file_path].append(finding)
    
    # 優先度順にソート
    priority_files = []
    for file_path, file_findings in files_dict.items():
        if 'main_window' in file_path.lower():
            priority_files.append((file_path, file_findings, 'HIGH'))
        elif 'event' in file_path.lower() or 'handler' in file_path.lower():
            priority_files.append((file_path, file_findings, 'MEDIUM'))
        else:
            priority_files.append((file_path, file_findings, 'LOW'))
    
    # 優先度順にソート
    priority_files.sort(key=lambda x: {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}[x[2]])
    
    for file_path, file_findings, priority in priority_files:
        logger.debug(f"\n📁 {file_path} (優先度: {priority})")
        for finding in file_findings:
            logger.debug(f"  🔍 行{finding['line']}: {finding['content']}")
    
    return priority_files

def analyze_specific_implementations():
    """特定の実装状況を詳細分析"""
    logger = logging.getLogger(__name__)
    logger.debug("=== 特定実装状況分析 ===")
    
    # main_window_core.pyの分析
    main_window_file = project_root / 'presentation/views/functional_main_window/main_window_core.py'
    if main_window_file.exists():
        logger.debug("📋 MainWindowCore実装状況:")
        with open(main_window_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # ダミーコールバック確認
        if 'dummy_callback' in content:
            logger.debug("  ❌ ダミーコールバックが残存")
            
        # イベントハンドラ実装確認
        if 'self.folder_event_handler = None' in content:
            logger.debug("  ❌ イベントハンドラがNone初期化")
            
        # TODO確認
        if 'TODO' in content:
            logger.debug("  ❌ TODOコメントが残存")
    
    # refactored_main_window.pyの分析
    refactored_file = project_root / 'presentation/views/functional_main_window/refactored_main_window.py'
    if refactored_file.exists():
        logger.debug("📋 RefactoredFunctionalMainWindow実装状況:")
        with open(refactored_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 未実装管理クラス確認
        none_managers = [
            'self.address_bar_mgr = None',
            'self.maximize_hdlr = None',
            'self.folder_event_hdlr = None',
            'self.image_event_hdlr = None',
            'self.theme_event_hdlr = None'
        ]
        
        for none_manager in none_managers:
            if none_manager in content:
                logger.debug(f"  ❌ 未実装管理クラス: {none_manager}")

if __name__ == "__main__":
    setup_debug_logging()
    priority_files = search_dummy_and_todo()
    analyze_specific_implementations()
    
    logger = logging.getLogger(__name__)
    logger.debug("ダミー実装・TODO調査完了")
    
    # 優先実装候補の提示
    if priority_files:
        logger.debug("\n🎯 優先実装候補:")
        for file_path, findings, priority in priority_files[:5]:  # 上位5件
            logger.debug(f"  {priority}: {file_path} ({len(findings)}件)")
