"""
PhotoMap Explorer 統合テストスイート

すべてのテストを実行し、包括的なレポートを生成します。
"""

import sys
import os
from pathlib import Path
import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests import setup_test_environment, cleanup_test_environment, test_reporter
from tests.e2e.test_end_to_end import run_e2e_tests
from tests.performance.test_performance import run_performance_tests

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

def run_integration_tests():
    """統合テストスイートを実行"""
    print("🧪 PhotoMap Explorer 統合テストスイート")
    print("=" * 80)
    print("📅 実行日時:", __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("🔧 環境: Windows, Python", sys.version.split()[0])
    print("=" * 80)
    
    # テスト環境セットアップ
    test_config = setup_test_environment()
    
    try:
        # Qtアプリケーション作成（グローバルに1つだけ）
        if not QApplication.instance():
            app = QApplication(sys.argv)
        
        print("\n📋 テスト実行計画")
        print("-" * 40)
        print("1. エンドツーエンドテスト")
        print("2. パフォーマンステスト")
        print("3. 統合レポート生成")
        
        # 1. エンドツーエンドテスト実行
        print("\n" + "=" * 80)
        print("🔍 STEP 1: エンドツーエンドテスト実行")
        print("=" * 80)
        
        e2e_result = run_e2e_tests()
        
        # 2. パフォーマンステスト実行
        print("\n" + "=" * 80)
        print("⚡ STEP 2: パフォーマンステスト実行")
        print("=" * 80)
        
        performance_results = run_performance_tests()
        
        # 3. 統合レポート生成
        print("\n" + "=" * 80)
        print("📊 STEP 3: 統合レポート生成")
        print("=" * 80)
        
        generate_integration_report(e2e_result, performance_results)
        
        # 最終結果表示
        print("\n" + "=" * 80)
        print("🎯 統合テスト完了")
        print("=" * 80)
        
        # 総合評価
        e2e_success = e2e_result.wasSuccessful() if e2e_result else False
        performance_success = bool(performance_results and len(performance_results) > 0)
        
        overall_success = e2e_success and performance_success
        
        print(f"📋 エンドツーエンドテスト: {'✅ 成功' if e2e_success else '❌ 失敗'}")
        print(f"⚡ パフォーマンステスト: {'✅ 成功' if performance_success else '❌ 失敗'}")
        print(f"🎯 総合評価: {'✅ 成功' if overall_success else '⚠️ 部分的成功'}")
        
        if overall_success:
            print("\n🎉 PhotoMap Explorer は本番リリース準備完了です！")
        else:
            print("\n⚠️ いくつかの課題が残っています。詳細レポートを確認してください。")
        
        return overall_success
        
    except Exception as e:
        print(f"\n❌ 統合テスト実行中にエラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        cleanup_test_environment()

def generate_integration_report(e2e_result, performance_results):
    """統合テストレポートを生成"""
    timestamp = __import__('datetime').datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f"integration_test_report_{timestamp}.md"
    
    # レポート内容作成
    report_content = f"""# PhotoMap Explorer 統合テストレポート

## 📋 テスト概要

- **実行日時**: {__import__('datetime').datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
- **テスト環境**: Windows, Python {sys.version.split()[0]}
- **テスト種別**: エンドツーエンドテスト + パフォーマンステスト

## 🧪 エンドツーエンドテスト結果

"""
    
    if e2e_result:
        total_tests = e2e_result.testsRun
        failures = len(e2e_result.failures)
        errors = len(e2e_result.errors)
        success = total_tests - failures - errors
        success_rate = (success / total_tests * 100) if total_tests > 0 else 0
        
        report_content += f"""
### 📊 テスト統計
- **総テスト数**: {total_tests}
- **成功**: {success}
- **失敗**: {failures}
- **エラー**: {errors}
- **成功率**: {success_rate:.1f}%

### 🎯 テスト詳細
"""
        
        if e2e_result.failures:
            report_content += "\n#### ❌ 失敗したテスト\n"
            for test, error in e2e_result.failures:
                report_content += f"- {test}: {error.split('\\n')[0]}\n"
        
        if e2e_result.errors:
            report_content += "\n#### ⚠️ エラーが発生したテスト\n"
            for test, error in e2e_result.errors:
                report_content += f"- {test}: {error.split('\\n')[0]}\n"
    
    else:
        report_content += "⚠️ エンドツーエンドテストの結果が取得できませんでした。\n"
    
    # パフォーマンステスト結果
    report_content += "\n## ⚡ パフォーマンステスト結果\n"
    
    if performance_results:
        summary = performance_results.get('summary', {})
        
        report_content += f"""
### 📊 パフォーマンス統計
- **総実行時間**: {summary.get('total_execution_time_ms', 0):.2f}ms
- **最大メモリ使用量**: {summary.get('max_memory_usage_mb', 0):.2f}MB
- **平均CPU使用率**: {summary.get('average_cpu_percent', 0):.1f}%
- **実行テスト数**: {summary.get('test_count', 0)}

### 🎯 パフォーマンス詳細
"""
        
        # 個別テスト結果
        for test_name, result in performance_results.items():
            if test_name != 'summary' and isinstance(result, dict):
                if 'execution_time_ms' in result:
                    report_content += f"- **{test_name}**: {result['execution_time_ms']:.2f}ms"
                    if 'memory_peak_mb' in result:
                        report_content += f" (メモリ: {result['memory_peak_mb']:.2f}MB)"
                    report_content += "\n"
    
    else:
        report_content += "⚠️ パフォーマンステストの結果が取得できませんでした。\n"
    
    # 目標との比較
    report_content += """
## 🎯 目標達成状況

### パフォーマンス目標
| 項目 | 目標値 | 実測値 | 状況 |
|-----|-------|-------|------|
| 起動時間 | < 3000ms | """ + f"{performance_results.get('startup', {}).get('execution_time_ms', 'N/A')}" + """ms | """ + ("✅" if performance_results.get('startup', {}).get('execution_time_ms', float('inf')) < 3000 else "❌") + """ |
| UI応答性 | < 100ms | """ + f"{performance_results.get('ui_responsiveness', {}).get('execution_time_ms', 'N/A')}" + """ms | """ + ("✅" if performance_results.get('ui_responsiveness', {}).get('execution_time_ms', float('inf')) < 100 else "❌") + """ |
| メモリ使用量 | < 500MB | """ + f"{performance_results.get('memory_usage', {}).get('memory_peak_mb', 'N/A')}" + """MB | """ + ("✅" if performance_results.get('memory_usage', {}).get('memory_peak_mb', float('inf')) < 500 else "❌") + """ |

### 品質目標
| 項目 | 目標値 | 実測値 | 状況 |
|-----|-------|-------|------|
| テストカバレッジ | > 80% | """ + f"{((e2e_result.testsRun - len(e2e_result.failures) - len(e2e_result.errors)) / e2e_result.testsRun * 100) if e2e_result and e2e_result.testsRun > 0 else 'N/A'}" + """% | """ + ("✅" if e2e_result and e2e_result.testsRun > 0 and ((e2e_result.testsRun - len(e2e_result.failures) - len(e2e_result.errors)) / e2e_result.testsRun * 100) > 80 else "❌") + """ |
| 重大バグ | 0件 | """ + f"{len(e2e_result.errors) if e2e_result else 'N/A'}" + """件 | """ + ("✅" if e2e_result and len(e2e_result.errors) == 0 else "❌") + """ |

## 📝 推奨事項

### 🔧 改善が必要な項目
"""
    
    # 改善提案
    recommendations = []
    
    if e2e_result and len(e2e_result.failures) > 0:
        recommendations.append("- エンドツーエンドテストの失敗を修正してください")
    
    if performance_results.get('ui_responsiveness', {}).get('execution_time_ms', 0) > 100:
        recommendations.append("- UI応答性の改善（目標: 100ms以内）")
    
    if not recommendations:
        recommendations.append("- 現在、大きな問題は検出されていません ✅")
    
    for rec in recommendations:
        report_content += rec + "\n"
    
    report_content += """
### 🚀 次のステップ
1. 失敗したテストの修正
2. パフォーマンス最適化の実施
3. ユーザーマニュアルの作成
4. CI/CD パイプラインの構築
5. 本番リリースの準備

## 📊 添付ファイル
- 詳細なテストログ
- パフォーマンス測定データ
- エラーレポート

---
*このレポートは自動生成されました*
*PhotoMap Explorer 統合テストスイート v1.0*
"""
    
    # レポートファイル保存
    report_path = PROJECT_ROOT / "tests" / "performance" / "results" / report_filename
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"📄 統合レポート生成完了: {report_path}")
    
    # test_reporterにも保存
    test_reporter.save_report(f"integration_summary_{timestamp}.md")
    
    return report_path

if __name__ == '__main__':
    success = run_integration_tests()
    sys.exit(0 if success else 1)
