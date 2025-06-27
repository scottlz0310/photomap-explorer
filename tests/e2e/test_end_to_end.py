"""
PhotoMap Explorer エンドツーエンドテスト

このモジュールは、PhotoMap Explorerの完全な機能テストを実行します。
新UI、レガシーUI、ハイブリッドUIの全てをテストします。
"""

import sys
import os
import time
import unittest
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtTest import QTest

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tests import setup_test_environment, cleanup_test_environment, create_sample_images, test_reporter

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

class PhotoMapExplorerE2ETest(unittest.TestCase):
    """PhotoMap Explorer エンドツーエンドテスト"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラス全体のセットアップ"""
        print("🚀 PhotoMap Explorer E2E テスト開始")
        cls.test_config = setup_test_environment()
        cls.sample_images = create_sample_images()
        
        # Qtアプリケーション作成
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    @classmethod
    def tearDownClass(cls):
        """テストクラス全体のクリーンアップ"""
        cleanup_test_environment()
        print("✅ PhotoMap Explorer E2E テスト完了")
    
    def setUp(self):
        """各テストのセットアップ"""
        self.start_time = time.time()
    
    def tearDown(self):
        """各テストのクリーンアップ"""
        duration = (time.time() - self.start_time) * 1000  # ms
        test_name = self._testMethodName
        
        if hasattr(self, '_test_passed') and self._test_passed:
            test_reporter.add_result(test_name, 'passed', duration)
        else:
            test_reporter.add_result(test_name, 'failed', duration)
    
    def test_legacy_ui_startup(self):
        """レガシーUI起動テスト"""
        print("\n📱 レガシーUI起動テスト")
        
        try:
            from main_window import MainWindow
            
            window = MainWindow()
            self.assertIsNotNone(window)
            
            # ウィンドウを表示してすぐに閉じる
            window.show()
            QTest.qWait(100)  # 100ms待機
            window.close()
            
            print("✅ レガシーUI起動成功")
            self._test_passed = True
            
        except Exception as e:
            print(f"❌ レガシーUI起動失敗: {e}")
            self._test_passed = False
            raise
    
    def test_new_ui_startup(self):
        """新UI起動テスト"""
        print("\n🆕 新UI起動テスト")
        
        try:
            from presentation.views.simple_main_view import SimpleNewMainWindow
            
            window = SimpleNewMainWindow()
            self.assertIsNotNone(window)
            
            # ウィンドウを表示してすぐに閉じる
            window.show()
            QTest.qWait(100)  # 100ms待機
            window.close()
            
            print("✅ 新UI起動成功")
            self._test_passed = True
            
        except Exception as e:
            print(f"❌ 新UI起動失敗: {e}")
            self._test_passed = False
            raise
    
    def test_hybrid_ui_startup(self):
        """ハイブリッドUI起動テスト"""
        print("\n🔄 ハイブリッドUI起動テスト")
        
        try:
            from test_phase4_final import FinalIntegrationWindow
            
            window = FinalIntegrationWindow()
            self.assertIsNotNone(window)
            
            # ウィンドウを表示してすぐに閉じる
            window.show()
            QTest.qWait(200)  # 200ms待機（ハイブリッドは複雑なので少し長め）
            window.close()
            
            print("✅ ハイブリッドUI起動成功")
            self._test_passed = True
            
        except Exception as e:
            print(f"❌ ハイブリッドUI起動失敗: {e}")
            self._test_passed = False
            raise
    
    def test_domain_services(self):
        """ドメインサービステスト"""
        print("\n🏗️ ドメインサービステスト")
        
        try:
            from domain.services.photo_domain_service import PhotoDomainService
            from infrastructure.repositories import PhotoRepository
            from infrastructure.file_system import FileSystemService
            
            # サービス作成
            file_service = FileSystemService()
            photo_repo = PhotoRepository(file_service)
            domain_service = PhotoDomainService(photo_repo)
            
            self.assertIsNotNone(domain_service)
            
            # サンプル画像でテスト
            if self.sample_images:
                folder_path = os.path.dirname(self.sample_images[0])
                photos = domain_service.load_photos_from_folder(folder_path)
                self.assertIsInstance(photos, list)
                print(f"📁 フォルダから {len(photos)} 枚の画像を読み込み")
            
            print("✅ ドメインサービステスト成功")
            self._test_passed = True
            
        except Exception as e:
            print(f"❌ ドメインサービステスト失敗: {e}")
            self._test_passed = False
            raise
    
    def test_infrastructure_services(self):
        """インフラストラクチャサービステスト"""
        print("\n🔧 インフラストラクチャサービステスト")
        
        try:
            from infrastructure.file_system import FileSystemService
            from infrastructure.exif_reader import ExifReaderService
            from infrastructure.map_generator import MapGeneratorService
            
            # ファイルシステムサービステスト
            file_service = FileSystemService()
            self.assertIsNotNone(file_service)
            
            # EXIFリーダーサービステスト
            exif_service = ExifReaderService()
            self.assertIsNotNone(exif_service)
            
            # マップジェネレーターサービステスト
            map_service = MapGeneratorService()
            self.assertIsNotNone(map_service)
            
            print("✅ インフラストラクチャサービステスト成功")
            self._test_passed = True
            
        except Exception as e:
            print(f"❌ インフラストラクチャサービステスト失敗: {e}")
            self._test_passed = False
            raise
    
    def test_presentation_layer(self):
        """プレゼンテーション層テスト"""
        print("\n🎨 プレゼンテーション層テスト")
        
        try:
            from presentation.controllers.main_controller import MainController
            from presentation.viewmodels.simple_main_viewmodel import SimpleMainViewModel
            
            # ViewModelテスト
            viewmodel = SimpleMainViewModel()
            self.assertIsNotNone(viewmodel)
            
            # Controllerテスト
            controller = MainController()
            self.assertIsNotNone(controller)
            
            print("✅ プレゼンテーション層テスト成功")
            self._test_passed = True
            
        except Exception as e:
            print(f"❌ プレゼンテーション層テスト失敗: {e}")
            self._test_passed = False
            raise

class PerformanceE2ETest(unittest.TestCase):
    """パフォーマンス関連エンドツーエンドテスト"""
    
    @classmethod
    def setUpClass(cls):
        """パフォーマンステストセットアップ"""
        print("⚡ パフォーマンステスト開始")
        cls.test_config = setup_test_environment()
        cls.sample_images = create_sample_images()
        
        if not QApplication.instance():
            cls.app = QApplication(sys.argv)
        else:
            cls.app = QApplication.instance()
    
    def setUp(self):
        """各パフォーマンステストのセットアップ"""
        self.start_time = time.time()
    
    def tearDown(self):
        """各パフォーマンステストのクリーンアップ"""
        duration = (time.time() - self.start_time) * 1000  # ms
        test_name = self._testMethodName
        test_reporter.add_performance_metric(test_name, f"{duration:.2f}", "ms")
    
    def test_startup_performance(self):
        """起動パフォーマンステスト"""
        print("\n⚡ 起動パフォーマンステスト")
        
        # 目標: 3秒以内
        target_time = 3000  # ms
        
        start_time = time.time()
        
        try:
            from presentation.views.simple_main_view import SimpleNewMainWindow
            window = SimpleNewMainWindow()
            window.show()
            QTest.qWait(50)
            window.close()
            
            duration = (time.time() - start_time) * 1000
            
            print(f"起動時間: {duration:.2f}ms (目標: {target_time}ms以内)")
            
            if duration <= target_time:
                print("✅ 起動パフォーマンス目標達成")
            else:
                print("⚠️ 起動パフォーマンス目標未達成")
            
            test_reporter.add_performance_metric("startup_time", f"{duration:.2f}", "ms")
            
        except Exception as e:
            print(f"❌ 起動パフォーマンステスト失敗: {e}")
            raise
    
    def test_image_loading_performance(self):
        """画像読み込みパフォーマンステスト"""
        print("\n📸 画像読み込みパフォーマンステスト")
        
        if not self.sample_images:
            self.skipTest("サンプル画像が見つかりません")
        
        target_time = 1000  # ms (100枚まで)
        
        start_time = time.time()
        
        try:
            from domain.services.photo_domain_service import PhotoDomainService
            from infrastructure.repositories import PhotoRepository
            from infrastructure.file_system import FileSystemService
            
            file_service = FileSystemService()
            photo_repo = PhotoRepository(file_service)
            domain_service = PhotoDomainService(photo_repo)
            
            folder_path = os.path.dirname(self.sample_images[0])
            photos = domain_service.load_photos_from_folder(folder_path)
            
            duration = (time.time() - start_time) * 1000
            
            print(f"画像読み込み時間: {duration:.2f}ms ({len(photos)}枚)")
            
            if duration <= target_time:
                print("✅ 画像読み込みパフォーマンス目標達成")
            else:
                print("⚠️ 画像読み込みパフォーマンス目標未達成")
            
            test_reporter.add_performance_metric("image_loading_time", f"{duration:.2f}", "ms")
            test_reporter.add_performance_metric("images_loaded", str(len(photos)), "枚")
            
        except Exception as e:
            print(f"❌ 画像読み込みパフォーマンステスト失敗: {e}")
            raise

def run_e2e_tests():
    """エンドツーエンドテストを実行"""
    print("🧪 PhotoMap Explorer エンドツーエンドテスト実行")
    print("=" * 60)
    
    # テストスイート作成
    suite = unittest.TestSuite()
    
    # 基本機能テスト追加
    suite.addTest(PhotoMapExplorerE2ETest('test_legacy_ui_startup'))
    suite.addTest(PhotoMapExplorerE2ETest('test_new_ui_startup'))
    suite.addTest(PhotoMapExplorerE2ETest('test_hybrid_ui_startup'))
    suite.addTest(PhotoMapExplorerE2ETest('test_domain_services'))
    suite.addTest(PhotoMapExplorerE2ETest('test_infrastructure_services'))
    suite.addTest(PhotoMapExplorerE2ETest('test_presentation_layer'))
    
    # パフォーマンステスト追加
    suite.addTest(PerformanceE2ETest('test_startup_performance'))
    suite.addTest(PerformanceE2ETest('test_image_loading_performance'))
    
    # テスト実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # レポート生成
    print("\n" + "=" * 60)
    print(test_reporter.generate_report())
    test_reporter.save_report()
    
    return result

if __name__ == '__main__':
    run_e2e_tests()
