"""
簡素化されたUI最適化テスト

プロファイラーの競合を避けて、シンプルな時間測定でパフォーマンスを比較します。
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

def simple_ui_performance_test():
    """簡素化されたUIパフォーマンステスト"""
    print("🚀 簡素化UI最適化パフォーマンステスト")
    print("=" * 60)
    
    # Qtアプリケーション作成
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    results = {}
    
    # 1. 従来UI テスト
    print("\n📊 従来UI テスト")
    print("-" * 30)
    
    start_time = time.time()
    
    from presentation.views.simple_main_view import SimpleNewMainWindow
    original_window = SimpleNewMainWindow()
    original_window.show()
    app.processEvents()
    original_window.close()
    
    original_time = (time.time() - start_time) * 1000  # ms
    results['original'] = original_time
    
    print(f"従来UI時間: {original_time:.2f}ms")
    
    # 2. 最適化UI テスト
    print("\n⚡ 最適化UI テスト")
    print("-" * 30)
    
    start_time = time.time()
    
    from presentation.views.optimized_main_view import OptimizedMainWindow
    optimized_window = OptimizedMainWindow()
    optimized_window.show()
    
    # 非同期初期化完了まで待機
    wait_start = time.time()
    while not hasattr(optimized_window, 'lazy_components') or len(optimized_window.lazy_components) < 4:
        app.processEvents()
        time.sleep(0.01)
        if time.time() - wait_start > 3:  # 3秒でタイムアウト
            break
    
    optimized_window.close()
    
    optimized_time = (time.time() - start_time) * 1000  # ms
    results['optimized'] = optimized_time
    
    print(f"最適化UI時間: {optimized_time:.2f}ms")
    
    # 3. 結果分析
    print("\n📊 パフォーマンス比較")
    print("=" * 60)
    
    improvement = ((original_time - optimized_time) / original_time * 100) if original_time > 0 else 0
    
    print(f"従来UI:           {original_time:.2f}ms")
    print(f"最適化UI:         {optimized_time:.2f}ms")
    print(f"改善率:           {improvement:+.1f}%")
    
    # 目標判定
    target_time = 100  # ms
    target_achieved = optimized_time <= target_time
    
    print(f"\n🎯 目標達成状況")
    print(f"目標時間:         {target_time}ms以内")
    print(f"実測値:           {optimized_time:.2f}ms")
    print(f"達成状況:         {'✅ 達成' if target_achieved else '❌ 未達成'}")
    
    if target_achieved:
        print("\n🎉 UI応答性目標達成！")
        if improvement > 0:
            print(f"さらに従来UIより {improvement:.1f}% 高速化されました！")
    else:
        print(f"\n⚠️ 目標まで {optimized_time - target_time:.1f}ms の改善が必要です。")
    
    return results, target_achieved

def test_new_ui_modes():
    """新UIのモード別テスト"""
    print("\n🧪 新UIモード別テスト")
    print("=" * 60)
    
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    
    results = {}
    
    # 最適化UI単体テスト
    print("\n⚡ 最適化UI単体起動テスト")
    start_time = time.time()
    
    from presentation.views.optimized_main_view import OptimizedMainWindow
    window = OptimizedMainWindow()
    window.show()
    app.processEvents()
    window.close()
    
    single_time = (time.time() - start_time) * 1000
    results['optimized_single'] = single_time
    
    print(f"最適化UI単体: {single_time:.2f}ms")
    
    # main.pyからの起動テスト
    print("\n🚀 main.py経由起動テスト")
    start_time = time.time()
    
    try:
        import main
        from main import launch_new_ui
        
        window = launch_new_ui(debug=False)
        app.processEvents()
        if window:
            window.close()
        
        main_time = (time.time() - start_time) * 1000
        results['main_launch'] = main_time
        
        print(f"main.py経由: {main_time:.2f}ms")
        
    except Exception as e:
        print(f"main.py起動エラー: {e}")
        results['main_launch'] = 0
    
    return results

if __name__ == '__main__':
    # 基本パフォーマンステスト
    ui_results, target_achieved = simple_ui_performance_test()
    
    # モード別テスト
    mode_results = test_new_ui_modes()
    
    # 最終まとめ
    print("\n" + "=" * 80)
    print("🎯 Phase 5.2 UI最適化テスト結果")
    print("=" * 80)
    
    if target_achieved:
        print("✅ UI応答性目標達成！")
        print("🚀 Phase 5.2 UI最適化 - 成功")
    else:
        print("⚠️ UI応答性目標未達成")
        print("🔧 さらなる最適化が必要")
    
    print(f"\n📊 詳細結果:")
    for key, value in {**ui_results, **mode_results}.items():
        if value > 0:
            print(f"  {key}: {value:.2f}ms")
    
    print("\n🎉 Phase 5.2 パフォーマンス最適化テスト完了")
