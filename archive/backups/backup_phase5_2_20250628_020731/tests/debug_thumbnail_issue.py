"""
サムネイル生成問題診断ツール

ハイブリッドモードでのサムネイル生成問題を調査します
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# プロジェクトルートをパスに追加
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

def test_thumbnail_generation():
    """サムネイル生成テスト"""
    print("🔍 サムネイル生成診断開始")
    print("=" * 50)
    
    # 1. レガシーUIのサムネイル機能テスト
    print("\n📊 テスト1: レガシーUIサムネイル機能")
    try:
        from ui.thumbnail_list import ThumbnailListWidget as LegacyThumbnailList
        print("✅ レガシーサムネイルクラス: 利用可能")
        
        # 実際にインスタンス作成
        legacy_widget = LegacyThumbnailList()
        print("✅ レガシーサムネイルウィジェット: 作成成功")
        
    except Exception as e:
        print(f"❌ レガシーサムネイル: エラー - {e}")
    
    # 2. 新UIのサムネイル機能テスト
    print("\n📊 テスト2: 新UIサムネイル機能")
    try:
        from presentation.views.controls.thumbnail_list import ThumbnailListWidget
        print("✅ 新サムネイルクラス: 利用可能")
        
        # 実際にインスタンス作成
        new_widget = ThumbnailListWidget()
        print("✅ 新サムネイルウィジェット: 作成成功")
        
    except Exception as e:
        print(f"❌ 新サムネイル: エラー - {e}")
    
    # 3. ファクトリ関数テスト
    print("\n📊 テスト3: ファクトリ関数")
    try:
        from presentation.views.controls.thumbnail_list import create_thumbnail_list
        
        def dummy_callback(path):
            print(f"サムネイルクリック: {path}")
        
        factory_widget = create_thumbnail_list(dummy_callback)
        print("✅ ファクトリ関数: 作成成功")
        
    except Exception as e:
        print(f"❌ ファクトリ関数: エラー - {e}")
    
    # 4. 画像読み込みテスト
    print("\n📊 テスト4: 画像読み込み機能")
    try:
        from presentation.views.controls.thumbnail_list import load_pixmap
        
        # ダミー画像パスでテスト
        test_path = "test_image.jpg"
        pixmap = load_pixmap(test_path)
        print(f"✅ 画像読み込み関数: 利用可能 (QPixmap作成: {not pixmap.isNull()})")
        
    except Exception as e:
        print(f"❌ 画像読み込み: エラー - {e}")
    
    # 5. サムネイル表示テスト（実画像）
    print("\n📊 テスト5: 実画像でのテスト")
    
    # プロジェクト内のアイコン画像を使用
    icon_path = PROJECT_ROOT / "assets" / "pme_icon.png"
    
    if icon_path.exists():
        try:
            pixmap = QPixmap(str(icon_path))
            if not pixmap.isNull():
                print(f"✅ 実画像読み込み成功: {icon_path}")
                print(f"   サイズ: {pixmap.width()}x{pixmap.height()}")
            else:
                print(f"❌ 実画像読み込み失敗: {icon_path}")
                
        except Exception as e:
            print(f"❌ 実画像テストエラー: {e}")
    else:
        print(f"⚠️ テスト画像が見つかりません: {icon_path}")
    
    # 6. ハイブリッドUIでのサムネイル統合テスト
    print("\n📊 テスト6: ハイブリッドUI統合テスト")
    try:
        from test_phase4_final import FinalIntegrationWindow
        
        print("✅ ハイブリッドUIクラス: 利用可能")
        
        # ハイブリッドUIのサムネイルコンポーネント作成をテスト
        hybrid_window = FinalIntegrationWindow()
        test_result = hybrid_window._test_thumbnail_component()
        
        if test_result[1]:  # 成功フラグ
            print("✅ ハイブリッドUIサムネイルコンポーネント: 正常")
        else:
            print("❌ ハイブリッドUIサムネイルコンポーネント: 異常")
        
    except Exception as e:
        print(f"❌ ハイブリッドUI統合テスト: エラー - {e}")
    
    print("\n" + "=" * 50)
    print("🎯 診断完了")
    
    return True

class ThumbnailDiagnosticWindow(QMainWindow):
    """サムネイル診断ウィンドウ"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("サムネイル生成診断")
        self.setGeometry(200, 200, 600, 400)
        self._setup_ui()
        
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # 情報表示
        info_label = QLabel("サムネイル生成問題の診断ツール")
        info_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(info_label)
        
        # ステータス表示
        self.status_label = QLabel("診断準備完了")
        self.status_label.setStyleSheet("padding: 10px; background: #f0f0f0;")
        layout.addWidget(self.status_label)
        
        # テストボタン
        test_btn = QPushButton("サムネイル診断実行")
        test_btn.clicked.connect(self._run_diagnostic)
        layout.addWidget(test_btn)
        
        # サムネイルテスト表示エリア
        self.test_widget = QWidget()
        test_layout = QVBoxLayout(self.test_widget)
        
        # 実際のサムネイルウィジェットをテスト
        try:
            from presentation.views.controls.thumbnail_list import create_thumbnail_list
            
            def test_callback(path):
                self.status_label.setText(f"サムネイルクリック: {path}")
            
            self.thumbnail_widget = create_thumbnail_list(test_callback)
            test_layout.addWidget(QLabel("新UIサムネイルコンポーネント:"))
            test_layout.addWidget(self.thumbnail_widget)
            
            # テスト画像を追加
            self._load_test_images()
            
        except Exception as e:
            error_label = QLabel(f"サムネイルコンポーネント作成エラー: {e}")
            error_label.setStyleSheet("color: red;")
            test_layout.addWidget(error_label)
        
        layout.addWidget(self.test_widget)
        
    def _load_test_images(self):
        """テスト画像を読み込み"""
        # プロジェクト内の画像を検索
        test_images = []
        
        # assetsディレクトリの画像
        assets_dir = PROJECT_ROOT / "assets"
        if assets_dir.exists():
            for ext in ['*.png', '*.jpg', '*.jpeg']:
                test_images.extend(assets_dir.glob(ext))
        
        if test_images:
            # サムネイルウィジェットに画像を追加
            image_paths = [str(img) for img in test_images[:5]]  # 最大5枚
            self.thumbnail_widget.update_thumbnails(image_paths)
            self.status_label.setText(f"テスト画像 {len(image_paths)} 枚を読み込み")
        else:
            self.status_label.setText("テスト画像が見つかりません")
        
    def _run_diagnostic(self):
        """診断実行"""
        self.status_label.setText("診断実行中...")
        try:
            test_thumbnail_generation()
            self.status_label.setText("診断完了 - コンソールを確認してください")
        except Exception as e:
            self.status_label.setText(f"診断エラー: {e}")

def main():
    """メイン実行"""
    app = QApplication(sys.argv)
    
    # コンソールでの診断実行
    print("🚀 サムネイル生成診断ツール")
    test_thumbnail_generation()
    
    # GUI診断ウィンドウ表示
    window = ThumbnailDiagnosticWindow()
    window.show()
    
    return app.exec_()

if __name__ == "__main__":
    main()
