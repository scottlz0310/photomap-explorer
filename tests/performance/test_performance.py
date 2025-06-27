"""
PhotoMap Explorer パフォーマンステスト

このモジュールは、アプリケーションのパフォーマンスを測定し、
目標値との比較を行います。
"""

import sys
import os
import time
import threading
import psutil
import tracemalloc
from pathlib import Path
from typing import Dict, List, Any
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests import setup_test_environment, cleanup_test_environment, create_sample_images, test_reporter

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

class PerformanceMetrics:
    """パフォーマンスメトリクス収集クラス"""
    
    def __init__(self):
        self.metrics = {}
        self.start_memory = None
        self.start_time = None
    
    def start_monitoring(self):
        """メトリクス収集開始"""
        self.start_time = time.time()
        self.start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        tracemalloc.start()
    
    def stop_monitoring(self, test_name: str):
        """メトリクス収集終了"""
        end_time = time.time()
        end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self.metrics[test_name] = {
            'execution_time_ms': (end_time - self.start_time) * 1000,
            'memory_start_mb': self.start_memory,
            'memory_end_mb': end_memory,
            'memory_delta_mb': end_memory - self.start_memory,
            'memory_peak_mb': peak / 1024 / 1024,
            'cpu_percent': psutil.cpu_percent(interval=0.1)
        }
        
        return self.metrics[test_name]
    
    def get_summary(self) -> Dict[str, Any]:
        """パフォーマンスサマリーを取得"""
        if not self.metrics:
            return {}
        
        total_time = sum(m['execution_time_ms'] for m in self.metrics.values())
        max_memory = max(m['memory_peak_mb'] for m in self.metrics.values())
        avg_cpu = sum(m['cpu_percent'] for m in self.metrics.values()) / len(self.metrics)
        
        return {
            'total_execution_time_ms': total_time,
            'max_memory_usage_mb': max_memory,
            'average_cpu_percent': avg_cpu,
            'test_count': len(self.metrics)
        }

class PhotoMapPerformanceTester:
    """PhotoMap Explorer パフォーマンステスター"""
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.test_config = setup_test_environment()
        self.sample_images = create_sample_images()
        
        # Qtアプリケーション作成
        if not QApplication.instance():
            self.app = QApplication(sys.argv)
        else:
            self.app = QApplication.instance()
    
    def __del__(self):
        cleanup_test_environment()
    
    def test_startup_performance(self) -> Dict[str, Any]:
        """起動パフォーマンステスト"""
        print("⚡ 起動パフォーマンステスト")
        
        self.metrics.start_monitoring()
        
        try:
            from presentation.views.simple_main_view import SimpleNewMainWindow
            window = SimpleNewMainWindow()
            window.show()
            self.app.processEvents()  # イベント処理
            window.close()
            
            result = self.metrics.stop_monitoring('startup_performance')
            
            # 目標値チェック
            target_time_ms = 3000
            success = result['execution_time_ms'] <= target_time_ms
            
            print(f"📊 起動時間: {result['execution_time_ms']:.2f}ms (目標: {target_time_ms}ms)")
            print(f"📊 メモリ使用量: {result['memory_peak_mb']:.2f}MB")
            print(f"{'✅' if success else '⚠️'} 起動パフォーマンス {'達成' if success else '未達成'}")
            
            return result
            
        except Exception as e:
            print(f"❌ 起動パフォーマンステスト失敗: {e}")
            return {}
    
    def test_ui_responsiveness(self) -> Dict[str, Any]:
        """UI応答性テスト"""
        print("🖱️ UI応答性テスト")
        
        self.metrics.start_monitoring()
        
        try:
            from presentation.views.simple_main_view import SimpleNewMainWindow
            window = SimpleNewMainWindow()
            window.show()
            
            # UI操作シミュレーション
            for i in range(10):
                self.app.processEvents()
                time.sleep(0.01)  # 10ms間隔でイベント処理
            
            window.close()
            
            result = self.metrics.stop_monitoring('ui_responsiveness')
            
            # UI応答性の目標: 100ms以内
            target_time_ms = 100
            success = result['execution_time_ms'] <= target_time_ms
            
            print(f"📊 UI応答時間: {result['execution_time_ms']:.2f}ms (目標: {target_time_ms}ms)")
            print(f"{'✅' if success else '⚠️'} UI応答性 {'達成' if success else '未達成'}")
            
            return result
            
        except Exception as e:
            print(f"❌ UI応答性テスト失敗: {e}")
            return {}
    
    def test_image_loading_performance(self) -> Dict[str, Any]:
        """画像読み込みパフォーマンステスト"""
        print("📸 画像読み込みパフォーマンステスト")
        
        if not self.sample_images:
            print("⚠️ サンプル画像が見つかりません")
            return {}
        
        self.metrics.start_monitoring()
        
        try:
            from domain.services.photo_domain_service import PhotoDomainService
            from infrastructure.repositories import FileSystemPhotoRepository, InMemoryPhotoCollectionRepository
            
            photo_repo = FileSystemPhotoRepository()
            collection_repo = InMemoryPhotoCollectionRepository()
            domain_service = PhotoDomainService(photo_repo, collection_repo)
            
            folder_path = os.path.dirname(self.sample_images[0])
            photos = domain_service.load_photos_from_folder(folder_path)
            
            result = self.metrics.stop_monitoring('image_loading_performance')
            
            # 画像読み込みの目標: 1秒以内（100枚まで）
            target_time_ms = 1000
            success = result['execution_time_ms'] <= target_time_ms
            
            print(f"📊 画像読み込み時間: {result['execution_time_ms']:.2f}ms ({len(photos)}枚)")
            print(f"📊 メモリ使用量: {result['memory_peak_mb']:.2f}MB")
            print(f"{'✅' if success else '⚠️'} 画像読み込みパフォーマンス {'達成' if success else '未達成'}")
            
            return result
            
        except Exception as e:
            print(f"❌ 画像読み込みパフォーマンステスト失敗: {e}")
            return {}
    
    def test_memory_usage(self) -> Dict[str, Any]:
        """メモリ使用量テスト"""
        print("💾 メモリ使用量テスト")
        
        self.metrics.start_monitoring()
        
        try:
            # 複数のUIを同時に作成してメモリ使用量を測定
            windows = []
            
            for i in range(3):  # 3つのウィンドウを作成
                from presentation.views.simple_main_view import SimpleNewMainWindow
                window = SimpleNewMainWindow()
                window.show()
                windows.append(window)
                self.app.processEvents()
            
            # すべて閉じる
            for window in windows:
                window.close()
            
            result = self.metrics.stop_monitoring('memory_usage')
            
            # メモリ使用量の目標: 500MB以内
            target_memory_mb = 500
            success = result['memory_peak_mb'] <= target_memory_mb
            
            print(f"📊 ピークメモリ使用量: {result['memory_peak_mb']:.2f}MB (目標: {target_memory_mb}MB)")
            print(f"📊 メモリ増加量: {result['memory_delta_mb']:.2f}MB")
            print(f"{'✅' if success else '⚠️'} メモリ使用量 {'達成' if success else '未達成'}")
            
            return result
            
        except Exception as e:
            print(f"❌ メモリ使用量テスト失敗: {e}")
            return {}
    
    def run_all_tests(self) -> Dict[str, Any]:
        """全パフォーマンステストを実行"""
        print("🚀 PhotoMap Explorer パフォーマンステスト開始")
        print("=" * 60)
        
        results = {}
        
        # 個別テスト実行
        results['startup'] = self.test_startup_performance()
        results['ui_responsiveness'] = self.test_ui_responsiveness()
        results['image_loading'] = self.test_image_loading_performance()
        results['memory_usage'] = self.test_memory_usage()
        
        # 全体サマリー
        summary = self.metrics.get_summary()
        results['summary'] = summary
        
        print("\n" + "=" * 60)
        print("📊 パフォーマンステスト結果サマリー")
        print("=" * 60)
        print(f"📝 総実行時間: {summary.get('total_execution_time_ms', 0):.2f}ms")
        print(f"💾 最大メモリ使用量: {summary.get('max_memory_usage_mb', 0):.2f}MB")
        print(f"⚡ 平均CPU使用率: {summary.get('average_cpu_percent', 0):.1f}%")
        print(f"🧪 実行テスト数: {summary.get('test_count', 0)}")
        
        # パフォーマンス目標の総合評価
        goals_met = 0
        total_goals = 4
        
        if results.get('startup', {}).get('execution_time_ms', float('inf')) <= 3000:
            goals_met += 1
        if results.get('ui_responsiveness', {}).get('execution_time_ms', float('inf')) <= 100:
            goals_met += 1
        if results.get('image_loading', {}).get('execution_time_ms', float('inf')) <= 1000:
            goals_met += 1
        if results.get('memory_usage', {}).get('memory_peak_mb', float('inf')) <= 500:
            goals_met += 1
        
        success_rate = (goals_met / total_goals) * 100
        print(f"🎯 パフォーマンス目標達成率: {success_rate:.1f}% ({goals_met}/{total_goals})")
        
        # テストレポーターに結果を追加
        for test_name, result in results.items():
            if isinstance(result, dict) and 'execution_time_ms' in result:
                test_reporter.add_performance_metric(
                    f"{test_name}_time", 
                    f"{result['execution_time_ms']:.2f}", 
                    "ms"
                )
                if 'memory_peak_mb' in result:
                    test_reporter.add_performance_metric(
                        f"{test_name}_memory", 
                        f"{result['memory_peak_mb']:.2f}", 
                        "MB"
                    )
        
        return results

def run_performance_tests():
    """パフォーマンステストを実行"""
    tester = PhotoMapPerformanceTester()
    return tester.run_all_tests()

if __name__ == '__main__':
    run_performance_tests()
