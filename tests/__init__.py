"""
PhotoMap Explorer テストスイート設定

This module provides test configuration and utilities for PhotoMap Explorer.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# テスト用設定
TEST_CONFIG = {
    'temp_dir': None,
    'sample_images_dir': None,
    'test_output_dir': None,
    'performance_results_dir': None
}

def setup_test_environment():
    """テスト環境をセットアップ"""
    # 一時ディレクトリ作成
    TEST_CONFIG['temp_dir'] = tempfile.mkdtemp(prefix='photomap_test_')
    TEST_CONFIG['test_output_dir'] = os.path.join(TEST_CONFIG['temp_dir'], 'output')
    TEST_CONFIG['sample_images_dir'] = os.path.join(TEST_CONFIG['temp_dir'], 'sample_images')
    TEST_CONFIG['performance_results_dir'] = os.path.join(PROJECT_ROOT, 'tests', 'performance', 'results')
    
    # ディレクトリ作成
    os.makedirs(TEST_CONFIG['test_output_dir'], exist_ok=True)
    os.makedirs(TEST_CONFIG['sample_images_dir'], exist_ok=True)
    os.makedirs(TEST_CONFIG['performance_results_dir'], exist_ok=True)
    
    print(f"✅ テスト環境セットアップ完了: {TEST_CONFIG['temp_dir']}")
    return TEST_CONFIG

def cleanup_test_environment():
    """テスト環境をクリーンアップ"""
    if TEST_CONFIG['temp_dir'] and os.path.exists(TEST_CONFIG['temp_dir']):
        shutil.rmtree(TEST_CONFIG['temp_dir'])
        print(f"✅ テスト環境クリーンアップ完了: {TEST_CONFIG['temp_dir']}")

def create_sample_images():
    """テスト用サンプル画像を作成"""
    from PIL import Image, ExifTags
    import random
    
    if not TEST_CONFIG['sample_images_dir']:
        setup_test_environment()
    
    # GPS座標の例（東京周辺）
    sample_coordinates = [
        (35.6762, 139.6503),  # 東京駅
        (35.6584, 139.7016),  # 東京タワー
        (35.6593, 139.7006),  # 六本木ヒルズ
        (35.6751, 139.7648),  # スカイツリー
        (35.6586, 139.7454),  # 渋谷
    ]
    
    created_files = []
    
    for i, (lat, lon) in enumerate(sample_coordinates):
        # 簡単な画像作成
        img = Image.new('RGB', (800, 600), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        
        # GPS EXIFデータを追加する場合（簡易版）
        filename = f"test_image_{i+1:03d}.jpg"
        filepath = os.path.join(TEST_CONFIG['sample_images_dir'], filename)
        img.save(filepath, 'JPEG')
        created_files.append(filepath)
    
    print(f"✅ サンプル画像作成完了: {len(created_files)}枚")
    return created_files

class TestReporter:
    """テスト結果レポーター"""
    
    def __init__(self):
        self.results = {
            'total_tests': 0,
            'passed': 0,
            'failed': 0,
            'errors': 0,
            'performance_metrics': {}
        }
    
    def add_result(self, test_name, status, duration=None, error=None):
        """テスト結果を追加"""
        self.results['total_tests'] += 1
        
        if status == 'passed':
            self.results['passed'] += 1
        elif status == 'failed':
            self.results['failed'] += 1
        elif status == 'error':
            self.results['errors'] += 1
        
        if duration:
            self.results['performance_metrics'][test_name] = duration
    
    def add_performance_metric(self, metric_name, value, unit='ms'):
        """パフォーマンスメトリクスを追加"""
        self.results['performance_metrics'][f"{metric_name} ({unit})"] = value
    
    def generate_report(self):
        """レポートを生成"""
        success_rate = (self.results['passed'] / self.results['total_tests'] * 100) if self.results['total_tests'] > 0 else 0
        
        report = f"""
📊 PhotoMap Explorer テスト結果レポート
=====================================

🎯 総合結果
-----------
- 総テスト数: {self.results['total_tests']}
- 成功: {self.results['passed']}
- 失敗: {self.results['failed']}
- エラー: {self.results['errors']}
- 成功率: {success_rate:.1f}%

⚡ パフォーマンスメトリクス
------------------------
"""
        
        for metric, value in self.results['performance_metrics'].items():
            report += f"- {metric}: {value}\n"
        
        return report
    
    def save_report(self, filename=None):
        """レポートをファイルに保存"""
        if not filename:
            timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"test_report_{timestamp}.md"
        
        report_path = os.path.join(TEST_CONFIG['performance_results_dir'], filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(self.generate_report())
        
        print(f"📄 レポート保存: {report_path}")
        return report_path

# グローバルレポーター
test_reporter = TestReporter()
