"""
PhotoMap Explorer パフォーマンスプロファイラー

UI コンポーネントとアプリケーションのボトルネックを特定し、
詳細な分析結果を提供します。
"""

import sys
import time
import cProfile
import pstats
import tracemalloc
import threading
from pathlib import Path
from typing import Dict, List, Any, Callable
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
import psutil

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

class PerformanceProfiler(QObject):
    """パフォーマンスプロファイラー"""
    
    profile_completed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.profiler = cProfile.Profile()
        self.memory_tracker = None
        self.start_time = None
        self.process = psutil.Process()
        self.measurements = {}
        
    def start_profiling(self, name: str = "default"):
        """プロファイリング開始"""
        self.start_time = time.time()
        tracemalloc.start()
        
        # 既存のプロファイラーがアクティブな場合は無効化
        try:
            self.profiler.disable()
        except:
            pass
        
        self.profiler.enable()
        
        # 初期メモリ状態を記録
        self.measurements[name] = {
            'start_time': self.start_time,
            'start_memory': self.process.memory_info().rss / 1024 / 1024,  # MB
            'start_cpu': self.process.cpu_percent()
        }
        
        # プロファイリング開始ログ（デバッグモード時のみ）
        import os
        if os.getenv('DEBUG_MODE') == '1':
            print(f"📊 プロファイリング開始: {name}")
        
    def stop_profiling(self, name: str = "default") -> Dict[str, Any]:
        """プロファイリング終了"""
        self.profiler.disable()
        
        # 終了時点の情報を記録
        end_time = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        if name in self.measurements:
            measurement = self.measurements[name]
            result = {
                'name': name,
                'duration_ms': (end_time - measurement['start_time']) * 1000,
                'memory_start_mb': measurement['start_memory'],
                'memory_end_mb': self.process.memory_info().rss / 1024 / 1024,
                'memory_peak_mb': peak / 1024 / 1024,
                'memory_delta_mb': (self.process.memory_info().rss / 1024 / 1024) - measurement['start_memory'],
                'cpu_percent': self.process.cpu_percent(interval=0.1),
                'thread_count': threading.active_count()
            }
            
            # プロファイリング結果出力（デバッグモード時のみ）
            import os
            if os.getenv('DEBUG_MODE') == '1':
                print(f"📊 プロファイリング完了: {name}")
                print(f"   ⏱️  実行時間: {result['duration_ms']:.2f}ms")
                print(f"   💾 メモリ使用量: {result['memory_peak_mb']:.2f}MB (差分: +{result['memory_delta_mb']:.2f}MB)")
                print(f"   ⚡ CPU使用率: {result['cpu_percent']:.1f}%")
            
            self.profile_completed.emit(result)
            return result
        
        return {}
        
    def get_function_stats(self, sort_by: str = 'cumulative', limit: int = 20) -> List[Dict]:
        """関数別統計を取得"""
        stats = pstats.Stats(self.profiler)
        stats.sort_stats(sort_by)
        
        # 統計データを辞書形式で取得
        function_stats = []
        for func, (cc, nc, tt, ct, callers) in stats.stats.items():
            function_stats.append({
                'function': f"{func[0]}:{func[1]}({func[2]})",
                'call_count': nc,
                'total_time': tt,
                'cumulative_time': ct,
                'time_per_call': tt / nc if nc > 0 else 0
            })
        
        return function_stats[:limit]
    
    def save_profile_report(self, name: str, stats: Dict[str, Any]) -> str:
        """プロファイルレポートを保存"""
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        report_path = PROJECT_ROOT / "tests" / "performance" / "results" / f"profile_{name}_{timestamp}.md"
        
        # 関数統計を取得
        function_stats = self.get_function_stats()
        
        report_content = f"""# パフォーマンスプロファイルレポート: {name}

## 📊 全体統計
- **実行時間**: {stats.get('duration_ms', 0):.2f}ms
- **メモリ使用量**: {stats.get('memory_peak_mb', 0):.2f}MB
- **メモリ増加量**: +{stats.get('memory_delta_mb', 0):.2f}MB
- **CPU使用率**: {stats.get('cpu_percent', 0):.1f}%
- **アクティブスレッド数**: {stats.get('thread_count', 0)}

## 🔍 パフォーマンス分析

### メモリ効率
"""
        
        memory_efficiency = "excellent" if stats.get('memory_delta_mb', 0) < 10 else "good" if stats.get('memory_delta_mb', 0) < 50 else "needs_improvement"
        
        report_content += f"- **効率レベル**: {memory_efficiency}\n"
        report_content += f"- **メモリリーク**: {'検出されず' if stats.get('memory_delta_mb', 0) < 1 else '要確認'}\n\n"
        
        # 関数別統計
        report_content += "## ⚡ 関数別パフォーマンス（上位20件）\n\n"
        report_content += "| 関数 | 呼び出し回数 | 総実行時間(s) | 累積時間(s) | 1回あたり(ms) |\n"
        report_content += "|------|-------------|-------------|-------------|-------------|\n"
        
        for func_stat in function_stats:
            report_content += f"| {func_stat['function'][:50]}... | {func_stat['call_count']} | {func_stat['total_time']:.4f} | {func_stat['cumulative_time']:.4f} | {func_stat['time_per_call']*1000:.2f} |\n"
        
        report_content += """
## 💡 最適化推奨事項

### 高優先度
- 実行時間が長い関数の最適化
- メモリ使用量の削減
- 不要な処理の除去

### 中優先度  
- 関数呼び出し回数の削減
- キャッシュ機能の導入
- 非同期処理の活用

---
*自動生成レポート*
"""
        
        # ファイル保存
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # レポート保存ログ（デバッグモード時のみ）
        import os
        if os.getenv('DEBUG_MODE') == '1':
            print(f"📄 プロファイルレポート保存: {report_path}")
        return str(report_path)

class UIComponentProfiler:
    """UIコンポーネント専用プロファイラー"""
    
    def __init__(self):
        self.profiler = PerformanceProfiler()
        self.component_timings = {}
        
    def profile_widget_creation(self, widget_class: type, *args, **kwargs):
        """ウィジェット作成時間を測定"""
        component_name = widget_class.__name__
        
        self.profiler.start_profiling(f"widget_creation_{component_name}")
        
        try:
            widget = widget_class(*args, **kwargs)
            stats = self.profiler.stop_profiling(f"widget_creation_{component_name}")
            
            self.component_timings[f"creation_{component_name}"] = stats
            return widget
            
        except Exception as e:
            # エラーログを適切に処理（デバッグモード時のみ標準出力）
            import os
            import logging
            logging.error(f"ウィジェット作成エラー ({component_name}): {e}")
            if os.getenv('DEBUG_MODE') == '1':
                print(f"❌ ウィジェット作成エラー ({component_name}): {e}")
            raise
    
    def profile_method_call(self, obj: object, method_name: str, *args, **kwargs):
        """メソッド呼び出し時間を測定"""
        full_name = f"{obj.__class__.__name__}.{method_name}"
        
        self.profiler.start_profiling(f"method_{full_name}")
        
        try:
            method = getattr(obj, method_name)
            result = method(*args, **kwargs)
            stats = self.profiler.stop_profiling(f"method_{full_name}")
            
            self.component_timings[f"method_{full_name}"] = stats
            return result
            
        except Exception as e:
            # エラーログを適切に処理（デバッグモード時のみ標準出力）
            import os
            import logging
            logging.error(f"メソッド実行エラー ({full_name}): {e}")
            if os.getenv('DEBUG_MODE') == '1':
                print(f"❌ メソッド実行エラー ({full_name}): {e}")
            raise
    
    def generate_ui_performance_report(self) -> str:
        """UI パフォーマンスレポートを生成"""
        if not self.component_timings:
            return "パフォーマンスデータがありません"
        
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        report_path = PROJECT_ROOT / "tests" / "performance" / "results" / f"ui_performance_{timestamp}.md"
        
        report_content = "# UI コンポーネントパフォーマンスレポート\n\n"
        
        # 実行時間でソート
        sorted_timings = sorted(
            self.component_timings.items(), 
            key=lambda x: x[1].get('duration_ms', 0), 
            reverse=True
        )
        
        report_content += "## ⏱️ 実行時間ランキング\n\n"
        report_content += "| 順位 | コンポーネント/メソッド | 実行時間(ms) | メモリ使用量(MB) | CPU(%) |\n"
        report_content += "|------|----------------------|-------------|----------------|--------|\n"
        
        for i, (name, stats) in enumerate(sorted_timings[:10], 1):
            report_content += f"| {i} | {name} | {stats.get('duration_ms', 0):.2f} | {stats.get('memory_peak_mb', 0):.2f} | {stats.get('cpu_percent', 0):.1f} |\n"
        
        # 改善提案
        slow_components = [name for name, stats in sorted_timings if stats.get('duration_ms', 0) > 50]
        
        report_content += "\n## 💡 最適化推奨事項\n\n"
        
        if slow_components:
            report_content += "### 🐌 重いコンポーネント（50ms以上）\n"
            for component in slow_components:
                report_content += f"- {component}\n"
            report_content += "\n"
        
        report_content += """### 🚀 最適化戦略
1. **遅延初期化**: 重いコンポーネントの初期化を遅延させる
2. **非同期処理**: UI をブロックしないように非同期で処理
3. **キャッシュ**: 計算結果をキャッシュして再利用
4. **軽量化**: 不要な処理や機能を削除

---
*自動生成 UI パフォーマンスレポート*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        # UIレポート保存ログ（デバッグモード時のみ）
        import os
        if os.getenv('DEBUG_MODE') == '1':
            print(f"📄 UI パフォーマンスレポート保存: {report_path}")
        return str(report_path)

def profile_function(func: Callable) -> Callable:
    """関数デコレータ：関数実行時間を自動測定"""
    def wrapper(*args, **kwargs):
        profiler = PerformanceProfiler()
        profiler.start_profiling(func.__name__)
        
        try:
            result = func(*args, **kwargs)
            profiler.stop_profiling(func.__name__)
            return result
        except Exception as e:
            profiler.stop_profiling(func.__name__)
            raise
    
    return wrapper

# グローバルプロファイラーインスタンス
global_profiler = PerformanceProfiler()
ui_profiler = UIComponentProfiler()
