#!/usr/bin/env python3
"""
テーマ継承問題のデバッグスクリプト
"""
import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=== テーマ継承デバッグ ===")

try:
    # ThemeAwareMixin のインポート
    from presentation.themes.theme_mixin import ThemeAwareMixin
    print("✅ ThemeAwareMixin インポート成功")
    print("   メソッド:", [m for m in dir(ThemeAwareMixin) if not m.startswith('_')])
    
    # MainWindowCore のインポート
    from presentation.views.functional_main_window.main_window_core import MainWindowCore
    print("✅ MainWindowCore インポート成功")
    
    # MRO (Method Resolution Order) 確認
    print("   MRO:", [c.__name__ for c in MainWindowCore.__mro__])
    
    # インスタンス作成（UIなしで）
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    import PyQt5.QtWidgets
    app = PyQt5.QtWidgets.QApplication([])
    
    instance = MainWindowCore()
    print("✅ MainWindowCore インスタンス作成成功")
    
    # register_theme_component メソッドの確認
    if hasattr(instance, 'register_theme_component'):
        print("✅ register_theme_component メソッド利用可能")
    else:
        print("❌ register_theme_component メソッドが見つかりません")
        print("   利用可能メソッド:", [m for m in dir(instance) if 'theme' in m.lower()])
    
    # RefactoredFunctionalMainWindow のテスト
    try:
        from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
        print("✅ RefactoredFunctionalMainWindow インポート成功")
        
        refactored_instance = RefactoredFunctionalMainWindow()
        print("✅ RefactoredFunctionalMainWindow インスタンス作成成功")
        
        if hasattr(refactored_instance, 'register_theme_component'):
            print("✅ RefactoredFunctionalMainWindow でも register_theme_component 利用可能")
        else:
            print("❌ RefactoredFunctionalMainWindow で register_theme_component が見つかりません")
            
    except Exception as e:
        print(f"❌ RefactoredFunctionalMainWindow エラー: {e}")
        import traceback
        traceback.print_exc()
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

print("\n=== デバッグ完了 ===")
