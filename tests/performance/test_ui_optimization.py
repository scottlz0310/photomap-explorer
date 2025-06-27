"""
最適化UIのパフォーマンステスト

最適化されたメインビューのパフォーマンスを測定し、
従来版との比較を行います。
"""

import sys
import time
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests import setup_test_environment, cleanup_test_environment, test_reporter
from utils.profiler import ui_profiler, global_profiler

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

def test_ui_optimization_performance():
    """UI最適化パフォーマンステスト"""
    print("🚀 UI最適化パフォーマンステスト開始")
    print("=" * 60)
    
    # テスト環境セットアップ
    test_config = setup_test_environment()
    
    try:
        # Qtアプリケーション作成
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        results = {}
        
        # 1. 従来のSimpleMainWindow テスト
        print("\n📊 従来UI (SimpleMainWindow) テスト")
        print("-" * 40)
        
        global_profiler.start_profiling("original_ui")
        
        from presentation.views.simple_main_view import SimpleNewMainWindow
        original_window = SimpleNewMainWindow()
        original_window.show()
        app.processEvents()
        original_window.close()
        
        original_stats = global_profiler.stop_profiling("original_ui")
        results['original'] = original_stats
        
        # 2. 最適化されたUI テスト
        print("\n⚡ 最適化UI (OptimizedMainWindow) テスト")
        print("-" * 40)
        
        global_profiler.start_profiling("optimized_ui")
        
        from presentation.views.optimized_main_view import OptimizedMainWindow
        optimized_window = OptimizedMainWindow()
        optimized_window.show()
        
        # 非同期初期化完了まで待機
        start_wait = time.time()
        while not hasattr(optimized_window, 'lazy_components') or len(optimized_window.lazy_components) < 4:
            app.processEvents()
            time.sleep(0.01)
            if time.time() - start_wait > 5:  # 5秒でタイムアウト
                break
        
        optimized_window.close()
        
        optimized_stats = global_profiler.stop_profiling("optimized_ui")
        results['optimized'] = optimized_stats
        
        # 3. 結果比較・分析
        print("\n📊 パフォーマンス比較結果")
        print("=" * 60)
        
        original_time = original_stats.get('duration_ms', 0)
        optimized_time = optimized_stats.get('duration_ms', 0)
        improvement = ((original_time - optimized_time) / original_time * 100) if original_time > 0 else 0
        
        print(f"従来UI実行時間:     {original_time:.2f}ms")
        print(f"最適化UI実行時間:   {optimized_time:.2f}ms")
        print(f"改善率:           {improvement:+.1f}%")
        
        original_memory = original_stats.get('memory_peak_mb', 0)
        optimized_memory = optimized_stats.get('memory_peak_mb', 0)
        memory_improvement = ((original_memory - optimized_memory) / original_memory * 100) if original_memory > 0 else 0
        
        print(f"従来UIメモリ:      {original_memory:.2f}MB")
        print(f"最適化UIメモリ:    {optimized_memory:.2f}MB")
        print(f"メモリ改善率:     {memory_improvement:+.1f}%")
        
        # 目標達成判定
        ui_response_target = 100  # ms
        ui_response_achieved = optimized_time <= ui_response_target
        
        print(f"\n🎯 目標達成状況")
        print(f"UI応答性目標:     {ui_response_target}ms以内")
        print(f"実測値:          {optimized_time:.2f}ms")
        print(f"達成状況:        {'✅ 達成' if ui_response_achieved else '❌ 未達成'}")
        
        # テストレポーターに結果を記録
        test_reporter.add_performance_metric("original_ui_time", f"{original_time:.2f}", "ms")
        test_reporter.add_performance_metric("optimized_ui_time", f"{optimized_time:.2f}", "ms")
        test_reporter.add_performance_metric("ui_improvement", f"{improvement:.1f}", "%")
        test_reporter.add_performance_metric("memory_improvement", f"{memory_improvement:.1f}", "%")
        
        results['comparison'] = {
            'time_improvement_percent': improvement,
            'memory_improvement_percent': memory_improvement,
            'target_achieved': ui_response_achieved
        }
        
        return results
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()
        return {}
    
    finally:
        cleanup_test_environment()

def test_component_loading_performance():
    """コンポーネント読み込みパフォーマンステスト"""
    print("\n🧩 コンポーネント読み込みパフォーマンステスト")
    print("=" * 60)
    
    try:
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        from presentation.views.optimized_main_view import OptimizedMainWindow
        
        # UIプロファイラーを使用してコンポーネント別測定
        window = ui_profiler.profile_widget_creation(OptimizedMainWindow)
        window.show()
        
        # 各コンポーネントの読み込み時間を測定
        start_time = time.time()
        while len(getattr(window, 'lazy_components', {})) < 4:
            app.processEvents()
            time.sleep(0.01)
            if time.time() - start_time > 10:  # 10秒でタイムアウト
                break
        
        window.close()
        
        # UIプロファイラーレポート生成
        report_path = ui_profiler.generate_ui_performance_report()
        print(f"📄 UIパフォーマンスレポート: {report_path}")
        
        return ui_profiler.component_timings
        
    except Exception as e:
        print(f"❌ コンポーネントテストエラー: {e}")
        return {}

def run_optimization_tests():
    """最適化テストを実行"""
    print("🧪 PhotoMap Explorer UI最適化テスト")
    print("=" * 80)
    
    # 1. UI最適化パフォーマンステスト
    ui_results = test_ui_optimization_performance()
    
    # 2. コンポーネント読み込みテスト
    component_results = test_component_loading_performance()
    
    # 3. 総合レポート生成
    print("\n📊 最適化テスト総合結果")
    print("=" * 80)
    
    if ui_results:
        comparison = ui_results.get('comparison', {})
        time_improvement = comparison.get('time_improvement_percent', 0)
        memory_improvement = comparison.get('memory_improvement_percent', 0)
        target_achieved = comparison.get('target_achieved', False)
        
        print(f"⚡ UI応答性改善:    {time_improvement:+.1f}%")
        print(f"💾 メモリ効率改善:  {memory_improvement:+.1f}%")
        print(f"🎯 目標達成:       {'✅ Yes' if target_achieved else '❌ No'}")
        
        # 改善提案
        if not target_achieved:
            print("\n💡 さらなる最適化提案:")
            print("  - より軽量なウィジェット使用")
            print("  - 初期化タイミングの調整") 
            print("  - キャッシュ機能の追加")
        else:
            print("\n🎉 UI応答性目標達成！優秀なパフォーマンスです。")
    
    # 最終レポート保存
    test_reporter.save_report("optimization_test_summary.md")
    
    return ui_results, component_results

if __name__ == '__main__':
    run_optimization_tests()
