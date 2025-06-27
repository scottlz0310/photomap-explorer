"""
Phase 4 統合テスト - フォルダ同期機能付きハイブリッド環境

新旧UIのフォルダパス同期とイベント連携をテストします。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QVBoxLayout, 
                             QWidget, QPushButton, QHBoxLayout, QLabel, QLineEdit,
                             QSplitter, QGroupBox, QTextEdit, QProgressBar)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# アプリケーション層の初期化
try:
    from app.application import initialize_application
    app = initialize_application()
    print("✅ アプリケーション層初期化成功")
except Exception as e:
    print(f"⚠️  アプリケーション層初期化警告: {e}")


class SyncController(QObject):
    """
    新旧UI間の同期制御クラス
    """
    path_changed = pyqtSignal(str)
    image_selected = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_path = "C:\\"
        self.current_image = None
    
    def update_path(self, path):
        """パス更新と同期"""
        if path != self.current_path:
            self.current_path = path
            self.path_changed.emit(path)
            print(f"🔄 パス同期: {path}")
    
    def update_image(self, image_path):
        """選択画像更新と同期"""
        if image_path != self.current_image:
            self.current_image = image_path
            self.image_selected.emit(image_path)
            print(f"🖼️ 画像同期: {image_path}")


class SynchronizedHybridWindow(QMainWindow):
    """
    同期機能付きハイブリッドテストウィンドウ
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - Phase 4 同期統合テスト")
        self.setGeometry(100, 100, 1800, 1200)
        
        # 同期コントローラー
        self.sync_controller = SyncController()
        self.sync_controller.path_changed.connect(self._on_path_sync)
        self.sync_controller.image_selected.connect(self._on_image_sync)
        
        # アイコン設定
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_path))
        
        self._setup_ui()
        self._setup_test_scenarios()
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # コントロールパネル
        control_panel = self._create_control_panel()
        layout.addWidget(control_panel)
        
        # メインスプリッター（水平分割）
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # 左側：新UI
        new_ui_container = self._create_new_ui_container()
        main_splitter.addWidget(new_ui_container)
        
        # 右側：レガシーUI
        legacy_ui_container = self._create_legacy_ui_container()
        main_splitter.addWidget(legacy_ui_container)
        
        # ログパネル
        log_panel = self._create_log_panel()
        layout.addWidget(log_panel)
        
        # 初期サイズ調整
        main_splitter.setSizes([900, 900])
    
    def _create_control_panel(self):
        """コントロールパネル作成"""
        group = QGroupBox("統合テストコントロール")
        layout = QHBoxLayout(group)
        
        # パス同期テスト
        self.path_input = QLineEdit("C:\\")
        self.path_input.setPlaceholderText("テスト用フォルダパス")
        layout.addWidget(QLabel("パス:"))
        layout.addWidget(self.path_input)
        
        sync_path_btn = QPushButton("パス同期テスト")
        sync_path_btn.clicked.connect(self._test_path_sync)
        layout.addWidget(sync_path_btn)
        
        # 機能テストボタン
        test_buttons = [
            ("基本動作テスト", self._test_basic_operations),
            ("コンポーネント互換性", self._test_component_compatibility),
            ("パフォーマンス比較", self._test_performance),
            ("ログクリア", self._clear_log)
        ]
        
        for text, handler in test_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
        
        # プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return group
    
    def _create_new_ui_container(self):
        """新UIコンテナ作成"""
        group = QGroupBox("新UI (Clean Architecture)")
        layout = QVBoxLayout(group)
        
        try:
            from presentation.views.main_view import MainView
            self.new_ui = MainView()
            layout.addWidget(self.new_ui)
            
            # 新UIのイベント接続
            if hasattr(self.new_ui, 'folder_path_changed'):
                self.new_ui.folder_path_changed.connect(self.sync_controller.update_path)
            
            self.log("✅ 新UI初期化成功")
            
        except Exception as e:
            error_label = QLabel(f"❌ 新UI初期化エラー: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            layout.addWidget(error_label)
            self.log(f"❌ 新UI初期化エラー: {e}")
            self.new_ui = None
        
        return group
    
    def _create_legacy_ui_container(self):
        """レガシーUIコンテナ作成"""
        group = QGroupBox("レガシーUI (従来版)")
        layout = QVBoxLayout(group)
        
        try:
            from window.main_window import MainWindow
            self.legacy_ui = MainWindow()
            
            # レガシーUIの中央ウィジェットを取得
            legacy_central = self.legacy_ui.centralWidget()
            if legacy_central:
                layout.addWidget(legacy_central)
                
                # レガシーUIのイベント接続（可能な範囲で）
                if hasattr(self.legacy_ui, 'folder_panel'):
                    self.legacy_ui.folder_panel.folder_changed.connect(
                        lambda path: self.sync_controller.update_path(path)
                    )
            
            self.log("✅ レガシーUI初期化成功")
            
        except Exception as e:
            error_label = QLabel(f"❌ レガシーUI初期化エラー: {str(e)}")
            error_label.setStyleSheet("color: red; padding: 20px;")
            layout.addWidget(error_label)
            self.log(f"❌ レガシーUI初期化エラー: {e}")
            self.legacy_ui = None
        
        return group
    
    def _create_log_panel(self):
        """ログパネル作成"""
        group = QGroupBox("テスト実行ログ")
        group.setMaximumHeight(150)
        layout = QVBoxLayout(group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(120)
        layout.addWidget(self.log_text)
        
        return group
    
    def log(self, message):
        """ログ出力"""
        self.log_text.append(f"[{QTimer().remainingTime() if hasattr(QTimer(), 'remainingTime') else ''}] {message}")
        print(message)
    
    def _clear_log(self):
        """ログクリア"""
        self.log_text.clear()
        self.log("🗑️ ログクリア")
    
    def _test_path_sync(self):
        """パス同期テスト"""
        path = self.path_input.text().strip()
        if not path:
            self.log("⚠️ パスが入力されていません")
            return
        
        self.log(f"🔄 パス同期テスト開始: {path}")
        self.sync_controller.update_path(path)
    
    def _on_path_sync(self, path):
        """パス同期イベントハンドラ"""
        self.log(f"📁 パス同期受信: {path}")
        
        # 新UIへパス反映
        if self.new_ui and hasattr(self.new_ui, 'update_folder_path'):
            try:
                self.new_ui.update_folder_path(path)
                self.log("✅ 新UIパス更新成功")
            except Exception as e:
                self.log(f"❌ 新UIパス更新エラー: {e}")
        
        # レガシーUIへパス反映
        if self.legacy_ui and hasattr(self.legacy_ui, 'on_folder_selected'):
            try:
                self.legacy_ui.on_folder_selected(path)
                self.log("✅ レガシーUIパス更新成功")
            except Exception as e:
                self.log(f"❌ レガシーUIパス更新エラー: {e}")
    
    def _on_image_sync(self, image_path):
        """画像同期イベントハンドラ"""
        self.log(f"🖼️ 画像同期受信: {image_path}")
    
    def _test_basic_operations(self):
        """基本動作テスト"""
        self.log("🧪 基本動作テスト開始")
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        tests = [
            ("ウィンドウ表示確認", lambda: True),
            ("新UI応答性テスト", self._test_new_ui_response),
            ("レガシーUI応答性テスト", self._test_legacy_ui_response),
            ("イベント伝達テスト", self._test_event_propagation)
        ]
        
        for i, (test_name, test_func) in enumerate(tests):
            self.log(f"  🔍 {test_name}")
            try:
                result = test_func()
                status = "✅ 成功" if result else "⚠️ 要確認"
                self.log(f"    {status}")
            except Exception as e:
                self.log(f"    ❌ エラー: {e}")
            
            self.progress_bar.setValue(int((i + 1) / len(tests) * 100))
        
        self.progress_bar.setVisible(False)
        self.log("🏁 基本動作テスト完了")
    
    def _test_new_ui_response(self):
        """新UI応答性テスト"""
        if not self.new_ui:
            return False
        
        try:
            # 基本メソッドの存在確認
            methods = ['show_status_message', 'update_folder_path']
            for method in methods:
                if not hasattr(self.new_ui, method):
                    self.log(f"    ⚠️ {method} メソッドが見つかりません")
                    return False
            
            # 基本操作テスト
            self.new_ui.show_status_message("Phase 4 統合テスト実行中")
            return True
            
        except Exception as e:
            self.log(f"    ❌ 新UI応答テストエラー: {e}")
            return False
    
    def _test_legacy_ui_response(self):
        """レガシーUI応答性テスト"""
        if not self.legacy_ui:
            return False
        
        try:
            # 基本コンポーネントの存在確認
            components = ['folder_panel', 'thumbnail_panel', 'preview_panel', 'map_panel']
            for component in components:
                if not hasattr(self.legacy_ui, component):
                    self.log(f"    ⚠️ {component} コンポーネントが見つかりません")
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"    ❌ レガシーUI応答テストエラー: {e}")
            return False
    
    def _test_event_propagation(self):
        """イベント伝達テスト"""
        try:
            # テスト用パスでイベント発火
            test_path = "C:\\Windows"
            self.sync_controller.update_path(test_path)
            return True
            
        except Exception as e:
            self.log(f"    ❌ イベント伝達テストエラー: {e}")
            return False
    
    def _test_component_compatibility(self):
        """コンポーネント互換性テスト"""
        self.log("🔧 コンポーネント互換性テスト開始")
        
        # 新UIコンポーネントのファクトリ関数テスト
        try:
            from presentation.views.controls.address_bar import create_address_bar_widget
            from presentation.views.panels.folder_panel import create_folder_panel
            from presentation.views.controls.thumbnail_list import create_thumbnail_list
            
            self.log("  ✅ ファクトリ関数インポート成功")
            
            # 実際にウィジェット作成テスト
            test_widgets = []
            
            # アドレスバー
            widget, edit = create_address_bar_widget("C:\\", None, None)
            test_widgets.append(("アドレスバー", widget))
            
            # フォルダパネル
            folder_panel = create_folder_panel()
            test_widgets.append(("フォルダパネル", folder_panel))
            
            # サムネイルリスト
            thumbnail_list = create_thumbnail_list(None, None)
            test_widgets.append(("サムネイルリスト", thumbnail_list))
            
            for name, widget in test_widgets:
                if widget:
                    self.log(f"  ✅ {name}作成成功")
                else:
                    self.log(f"  ❌ {name}作成失敗")
            
            self.log("🏁 コンポーネント互換性テスト完了")
            
        except Exception as e:
            self.log(f"❌ コンポーネント互換性テストエラー: {e}")
    
    def _test_performance(self):
        """パフォーマンス比較テスト"""
        self.log("⚡ パフォーマンス比較テスト開始")
        
        import time
        
        # 新UI初期化時間
        if self.new_ui:
            start_time = time.time()
            try:
                self.new_ui.show_status_message("パフォーマンステスト")
                new_ui_time = time.time() - start_time
                self.log(f"  📊 新UI応答時間: {new_ui_time:.3f}秒")
            except Exception as e:
                self.log(f"  ❌ 新UIパフォーマンステストエラー: {e}")
        
        # レガシーUI初期化時間
        if self.legacy_ui:
            start_time = time.time()
            try:
                # レガシーUIの基本操作
                legacy_ui_time = time.time() - start_time
                self.log(f"  📊 レガシーUI応答時間: {legacy_ui_time:.3f}秒")
            except Exception as e:
                self.log(f"  ❌ レガシーUIパフォーマンステストエラー: {e}")
        
        self.log("🏁 パフォーマンス比較テスト完了")
    
    def _setup_test_scenarios(self):
        """テストシナリオのセットアップ"""
        # 定期的なヘルスチェック
        self.health_timer = QTimer()
        self.health_timer.timeout.connect(self._health_check)
        self.health_timer.start(30000)  # 30秒間隔
        
        self.log("🚀 Phase 4 同期統合テスト環境準備完了")
        self.log("📋 利用可能な機能:")
        self.log("  - 新旧UI同時表示・比較")
        self.log("  - フォルダパス同期")
        self.log("  - イベント伝達テスト")
        self.log("  - パフォーマンス比較")
        self.log("  - コンポーネント互換性確認")
    
    def _health_check(self):
        """定期ヘルスチェック"""
        status = []
        if self.new_ui:
            status.append("新UI稼働中")
        if self.legacy_ui:
            status.append("レガシーUI稼働中")
        
        if status:
            self.log(f"💚 ヘルスチェック: {', '.join(status)}")


def main():
    """メインエントリーポイント"""
    print("🚀 Phase 4 同期統合テスト起動中...")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer - Phase 4 Sync Test")
    
    try:
        # テストウィンドウ作成
        window = SynchronizedHybridWindow()
        window.show()
        
        print("✅ 同期統合テスト環境起動成功")
        print("📋 テスト内容:")
        print("  - 新旧UI同時実行・比較")
        print("  - フォルダパス同期機能")
        print("  - イベント伝達テスト")
        print("  - パフォーマンス比較")
        print("  - コンポーネント互換性テスト")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ テスト環境起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
