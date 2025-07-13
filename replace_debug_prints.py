#!/usr/bin/env python3
"""
デバッグ出力一括置換スクリプト

既存のprint文をutils.debug_loggerのメソッドに置き換えます。
"""

import os
import re
import glob

def replace_debug_prints():
    """デバッグ出力を一括置換"""
    
    # 置換ルール: 絵文字パターンに基づく分類
    replacements = [
        # デバッグレベル (🔧)
        (r'print\(\s*f?"🔧\s*([^"]*?)"\s*\)', r'debug("\1")'),
        (r'print\(\s*"🔧\s*([^"]*?)"\s*\)', r'debug("\1")'),
        
        # 詳細レベル (📊)
        (r'print\(\s*f?"📊\s*([^"]*?)"\s*\)', r'verbose("\1")'),
        (r'print\(\s*"📊\s*([^"]*?)"\s*\)', r'verbose("\1")'),
        
        # 分析レベル (🔍)
        (r'print\(\s*f?"🔍\s*([^"]*?)"\s*\)', r'verbose("\1")'),
        (r'print\(\s*"🔍\s*([^"]*?)"\s*\)', r'verbose("\1")'),
        
        # 情報レベル (✅)
        (r'print\(\s*f?"✅\s*([^"]*?)"\s*\)', r'info("\1")'),
        (r'print\(\s*"✅\s*([^"]*?)"\s*\)', r'info("\1")'),
        
        # 成功レベル (🎉, 🎯)
        (r'print\(\s*f?"🎉\s*([^"]*?)"\s*\)', r'info("\1")'),
        (r'print\(\s*"🎉\s*([^"]*?)"\s*\)', r'info("\1")'),
        (r'print\(\s*f?"🎯\s*([^"]*?)"\s*\)', r'debug("\1")'),
        (r'print\(\s*"🎯\s*([^"]*?)"\s*\)', r'debug("\1")'),
        
        # 警告レベル (⚠️)
        (r'print\(\s*f?"⚠️\s*([^"]*?)"\s*\)', r'warning("\1")'),
        (r'print\(\s*"⚠️\s*([^"]*?)"\s*\)', r'warning("\1")'),
        
        # エラーレベル (❌)
        (r'print\(\s*f?"❌\s*([^"]*?)"\s*\)', r'error("\1")'),
        (r'print\(\s*"❌\s*([^"]*?)"\s*\)', r'error("\1")'),
        
        # その他の重要なもの
        (r'print\(\s*f?"📦\s*([^"]*?)"\s*\)', r'verbose("\1")'),
        (r'print\(\s*"📦\s*([^"]*?)"\s*\)', r'verbose("\1")'),
        (r'print\(\s*f?"🚨\s*([^"]*?)"\s*\)', r'error("\1")'),
        (r'print\(\s*"🚨\s*([^"]*?)"\s*\)', r'error("\1")'),
    ]
    
    # 対象ファイル
    target_files = [
        "presentation/views/functional_main_window/**/*.py",
        "presentation/views/functional_main_window/ui_components/*.py",
        "presentation/views/functional_main_window/event_handlers/*.py",
        "presentation/views/functional_main_window/display_managers/*.py",
        "ui/controls/**/*.py",
        "ui/*.py"
    ]
    
    total_replaced = 0
    
    for pattern in target_files:
        files = glob.glob(pattern, recursive=True)
        for file_path in files:
            if os.path.isfile(file_path) and file_path.endswith('.py'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    file_changed = False
                    
                    # importを追加
                    if 'from utils.debug_logger import' not in content:
                        import_line = "from utils.debug_logger import debug, info, warning, error, verbose\n"
                        # 既存のimportの後に追加
                        import_pos = content.rfind('import ')
                        if import_pos != -1:
                            # 次の改行を見つける
                            newline_pos = content.find('\n', import_pos)
                            if newline_pos != -1:
                                content = content[:newline_pos+1] + import_line + content[newline_pos+1:]
                                file_changed = True
                    
                    # 置換処理
                    file_replacements = 0
                    for pattern, replacement in replacements:
                        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
                        if new_content != content:
                            count = len(re.findall(pattern, content))
                            file_replacements += count
                            content = new_content
                            file_changed = True
                    
                    # ファイルを更新
                    if file_changed:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"✅ {file_path}: {file_replacements}個のprint文を置換")
                        total_replaced += file_replacements
                    
                except Exception as e:
                    print(f"❌ {file_path}: エラー - {e}")
    
    print(f"\n🎉 合計 {total_replaced}個のprint文を置換しました")

if __name__ == "__main__":
    replace_debug_prints()
