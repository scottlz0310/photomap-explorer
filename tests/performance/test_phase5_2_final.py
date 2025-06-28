"""
Phase 5.2 最終パフォーマンステスト

全最適化技術の総合評価
"""

import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

def test_all_optimizations():
    """全最適化版の総合テスト"""
    
    app = QApplication(sys.argv) if not QApplication.instance() else QApplication.instance()
    
    print("🎯 Phase 5.2 最終パフォーマンステスト")
    print("=" * 60)
    
    results = {}
    
    # テスト1: 従来版（SimpleNewMainWindow）
    print("\n📊 テスト1: 従来版UI")
    try:
        from presentation.views.simple_main_view import SimpleNewMainWindow
        
        start_time = time.time()
        window1 = SimpleNewMainWindow()
        window1.show()
        app.processEvents()
        window1.close()
        end_time = time.time()
        
        duration1 = (end_time - start_time) * 1000
        results['従来版'] = duration1
        print(f"⏱️ 従来版: {duration1:.2f}ms")
        
    except Exception as e:
        print(f"❌ 従来版テスト失敗: {e}")
        results['従来版'] = None
    
    # テスト2: 最適化版（OptimizedMainView）
    print("\n📊 テスト2: 最適化版UI")
    try:
        from presentation.views.optimized_main_view import OptimizedMainView
        
        start_time = time.time()
        window2 = OptimizedMainView()
        window2.show()
        app.processEvents()
        window2.close()
        end_time = time.time()
        
        duration2 = (end_time - start_time) * 1000
        results['最適化版'] = duration2
        print(f"⏱️ 最適化版: {duration2:.2f}ms")
        
    except Exception as e:
        print(f"❌ 最適化版テスト失敗: {e}")
        results['最適化版'] = None
    
    # テスト3: 最終最適化版（OptimizedFinalMainView）
    print("\n📊 テスト3: 最終最適化版UI")
    try:
        from presentation.views.final_optimized_main_view import OptimizedFinalMainView
        
        start_time = time.time()
        window3 = OptimizedFinalMainView()
        window3.show()
        app.processEvents()
        window3.close()
        end_time = time.time()
        
        duration3 = (end_time - start_time) * 1000
        results['最終最適化版'] = duration3
        print(f"⏱️ 最終最適化版: {duration3:.2f}ms")
        
    except Exception as e:
        print(f"❌ 最終最適化版テスト失敗: {e}")
        results['最終最適化版'] = None
    
    # テスト4: 極限軽量版（NativeQtMainView）
    print("\n📊 テスト4: 極限軽量版UI")
    try:
        from presentation.views.extreme_light_view import NativeQtMainView
        
        start_time = time.time()
        window4 = NativeQtMainView()
        window4.show()
        app.processEvents()
        window4.close()
        end_time = time.time()
        
        duration4 = (end_time - start_time) * 1000
        results['極限軽量版'] = duration4
        print(f"⏱️ 極限軽量版: {duration4:.2f}ms")
        
    except Exception as e:
        print(f"❌ 極限軽量版テスト失敗: {e}")
        results['極限軽量版'] = None
    
    # 結果分析
    print("\n" + "=" * 60)
    print("📊 パフォーマンス比較結果")
    print("=" * 60)
    
    valid_results = {k: v for k, v in results.items() if v is not None}
    
    if valid_results:
        baseline = valid_results.get('従来版', max(valid_results.values()))
        
        for name, duration in valid_results.items():
            if baseline and duration:
                improvement = ((baseline - duration) / baseline) * 100
                target_achieved = "✅" if duration <= 100 else ("🟡" if duration <= 200 else "❌")
                print(f"{target_achieved} {name:12}: {duration:7.2f}ms ({improvement:+6.1f}%)")
            else:
                target_achieved = "✅" if duration <= 100 else ("🟡" if duration <= 200 else "❌")
                print(f"{target_achieved} {name:12}: {duration:7.2f}ms")
        
        # 最良結果
        best_name = min(valid_results, key=valid_results.get)
        best_time = valid_results[best_name]
        
        print(f"\n🏆 最良結果: {best_name} - {best_time:.2f}ms")
        
        if best_time <= 100:
            print("🎉 目標達成！(100ms以内)")
        elif best_time <= 200:
            print("🟡 良好な結果 (200ms以内)")
        else:
            print("⚠️ 目標未達成")
        
        # Phase 5.2 総評
        print(f"\n🎯 Phase 5.2 総評")
        print("-" * 30)
        
        if best_time <= 100:
            print("✅ Phase 5.2 目標完全達成")
        elif best_time <= 200:
            print("🟡 Phase 5.2 部分的達成")
        else:
            print("⚠️ Phase 5.2 追加最適化要")
        
        return best_time, results
    
    else:
        print("❌ 有効なテスト結果が得られませんでした")
        return None, results

if __name__ == "__main__":
    test_all_optimizations()
