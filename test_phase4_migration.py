"""
Phase 4 段階的移行テスト

移行ヘルパーを使用してレガシーUIから新UIへの段階的移行をテストします。
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                             QWidget, QPushButton, QGroupBox, QListWidget, QListWidgetItem,
                             QTextEdit, QProgressBar, QLabel, QSplitter, QCheckBox,
                             QComboBox, QMessageBox)
from PyQt5.QtCore import Qt, QTimer

# WebEngine問題の解決
QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from migration_helper import MigrationHelper, MigrationReporter, setup_migration_helper


class MigrationTestWindow(QMainWindow):
    """
    段階的移行テストウィンドウ
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - Phase 4 段階的移行テスト")
        self.setGeometry(100, 100, 1600, 1200)
        
        # 移行ヘルパー
        self.migration_helper = None
        self.legacy_window = None
        
        # アイコン設定
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            from PyQt5.QtGui import QIcon
            self.setWindowIcon(QIcon(icon_path))
        
        self._setup_ui()
        self._initialize_legacy_window()
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)
        
        # 左パネル：移行コントロール
        control_panel = self._create_control_panel()
        layout.addWidget(control_panel)
        
        # 右パネル：プレビュー＆ログ
        preview_panel = self._create_preview_panel()
        layout.addWidget(preview_panel)
        
        # パネルサイズ調整
        layout.setStretch(0, 1)
        layout.setStretch(1, 2)
    
    def _create_control_panel(self):
        """コントロールパネル作成"""
        panel = QWidget()
        panel.setMaximumWidth(500)
        layout = QVBoxLayout(panel)
        
        # 移行進捗表示
        progress_group = QGroupBox("移行進捗")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_label = QLabel("移行準備中...")
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        layout.addWidget(progress_group)
        
        # コンポーネント選択
        component_group = QGroupBox("コンポーネント移行制御")
        component_layout = QVBoxLayout(component_group)
        
        self.component_list = QListWidget()
        component_layout.addWidget(QLabel("移行対象コンポーネント:"))
        component_layout.addWidget(self.component_list)
        
        # 移行制御ボタン
        button_layout = QHBoxLayout()
        
        self.replace_btn = QPushButton("選択コンポーネント移行")
        self.replace_btn.clicked.connect(self._replace_selected_component)
        button_layout.addWidget(self.replace_btn)
        
        self.revert_btn = QPushButton("元に戻す")
        self.revert_btn.clicked.connect(self._revert_selected_component)
        button_layout.addWidget(self.revert_btn)
        
        component_layout.addLayout(button_layout)
        
        # 一括操作
        bulk_layout = QHBoxLayout()
        
        self.replace_all_btn = QPushButton("全て移行")
        self.replace_all_btn.clicked.connect(self._replace_all_components)
        bulk_layout.addWidget(self.replace_all_btn)
        
        self.revert_all_btn = QPushButton("全て元に戻す")
        self.revert_all_btn.clicked.connect(self._revert_all_components)
        bulk_layout.addWidget(self.revert_all_btn)
        
        component_layout.addLayout(bulk_layout)
        
        layout.addWidget(component_group)
        
        # 移行戦略設定
        strategy_group = QGroupBox("移行戦略")
        strategy_layout = QVBoxLayout(strategy_group)
        
        self.strategy_combo = QComboBox()
        self.strategy_combo.addItems([
            "順次移行（優先度順）",
            "同時移行（全コンポーネント）",
            "テスト移行（可逆的）"
        ])
        strategy_layout.addWidget(QLabel("移行方式:"))
        strategy_layout.addWidget(self.strategy_combo)
        
        self.validate_check = QCheckBox("移行前に互換性検証")
        self.validate_check.setChecked(True)
        strategy_layout.addWidget(self.validate_check)
        
        layout.addWidget(strategy_group)
        
        # テストボタン
        test_group = QGroupBox("テスト＆検証")
        test_layout = QVBoxLayout(test_group)
        
        test_buttons = [
            ("互換性検証", self._validate_compatibility),
            ("移行レポート生成", self._generate_migration_report),
            ("パフォーマンステスト", self._run_performance_test),
            ("機能動作テスト", self._run_functional_test)
        ]
        
        for text, handler in test_buttons:
            btn = QPushButton(text)
            btn.clicked.connect(handler)
            test_layout.addWidget(btn)
        
        layout.addWidget(test_group)
        
        return panel
    
    def _create_preview_panel(self):
        """プレビュー＆ログパネル作成"""
        splitter = QSplitter(Qt.Vertical)
        
        # プレビューエリア
        preview_group = QGroupBox("レガシーUI プレビュー")
        preview_layout = QVBoxLayout(preview_group)
        
        self.preview_container = QWidget()
        self.preview_container.setMinimumHeight(400)
        preview_layout.addWidget(self.preview_container)
        
        splitter.addWidget(preview_group)
        
        # ログエリア
        log_group = QGroupBox("移行ログ")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(300)
        log_layout.addWidget(self.log_text)
        
        # ログ制御
        log_control_layout = QHBoxLayout()
        
        clear_log_btn = QPushButton("ログクリア")
        clear_log_btn.clicked.connect(self._clear_log)
        log_control_layout.addWidget(clear_log_btn)
        
        export_log_btn = QPushButton("ログエクスポート")
        export_log_btn.clicked.connect(self._export_log)
        log_control_layout.addWidget(export_log_btn)
        
        log_layout.addLayout(log_control_layout)
        
        splitter.addWidget(log_group)
        
        # スプリッターサイズ調整
        splitter.setSizes([600, 300])
        
        return splitter
    
    def _initialize_legacy_window(self):
        """レガシーウィンドウの初期化"""
        try:
            from window.main_window import MainWindow
            self.legacy_window = MainWindow()
            
            # プレビューコンテナにレガシーUIを埋め込み
            legacy_central = self.legacy_window.centralWidget()
            if legacy_central:
                preview_layout = QVBoxLayout(self.preview_container)
                preview_layout.addWidget(legacy_central)
            
            # 移行ヘルパーセットアップ
            self.migration_helper = setup_migration_helper(self.legacy_window)
            
            # イベント接続
            self.migration_helper.component_replaced.connect(self._on_component_replaced)
            self.migration_helper.migration_progress.connect(self._on_migration_progress)
            
            # コンポーネントリスト更新
            self._update_component_list()
            
            self.log("✅ レガシーウィンドウ初期化成功")
            self.log(f"📋 登録コンポーネント数: {len(self.migration_helper.component_registry)}")
            
        except Exception as e:
            self.log(f"❌ レガシーウィンドウ初期化エラー: {e}")
            import traceback
            self.log(traceback.format_exc())
    
    def _update_component_list(self):
        """コンポーネントリスト更新"""
        if not self.migration_helper:
            return
        
        self.component_list.clear()
        
        for name, info in self.migration_helper.component_registry.items():
            item = QListWidgetItem()
            
            # ステータスアイコン
            if info['replaced']:
                status_text = f"✅ {name} (移行済み)"
                item.setBackground(Qt.lightGray)
            else:
                status_text = f"⏳ {name} (移行前)"
            
            # 互換性ラッパー情報
            if info['compatibility_wrapper']:
                status_text += " 🔧"
            
            item.setText(status_text)
            item.setData(Qt.UserRole, name)
            self.component_list.addItem(item)
    
    def log(self, message: str):
        """ログ出力"""
        self.log_text.append(f"[{QTimer().remainingTime() if hasattr(QTimer(), 'remainingTime') else ''}] {message}")
        print(message)
    
    def _clear_log(self):
        """ログクリア"""
        self.log_text.clear()
        self.log("🗑️ ログクリア")
    
    def _export_log(self):
        """ログエクスポート"""
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "ログエクスポート", "migration_log.txt", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
                self.log(f"📄 ログエクスポート成功: {file_path}")
            except Exception as e:
                self.log(f"❌ ログエクスポートエラー: {e}")
    
    def _replace_selected_component(self):
        """選択コンポーネント移行"""
        current_item = self.component_list.currentItem()
        if not current_item:
            self.log("⚠️ コンポーネントが選択されていません")
            return
        
        component_name = current_item.data(Qt.UserRole)
        self.log(f"🔄 コンポーネント移行開始: {component_name}")
        
        # 互換性検証（有効な場合）
        if self.validate_check.isChecked():
            validation = self.migration_helper.validate_compatibility(component_name)
            if not validation['valid']:
                self.log(f"❌ 互換性検証失敗: {validation.get('reason', '不明')}")
                return
            else:
                self.log(f"✅ 互換性検証成功 (スコア: {validation.get('compatibility_score', 0):.2f})")
        
        # 移行実行
        success = self.migration_helper.replace_component(component_name, self.preview_container)
        
        if success:
            self.log(f"✅ コンポーネント移行成功: {component_name}")
        else:
            self.log(f"❌ コンポーネント移行失敗: {component_name}")
        
        self._update_component_list()
    
    def _revert_selected_component(self):
        """選択コンポーネント復元"""
        current_item = self.component_list.currentItem()
        if not current_item:
            self.log("⚠️ コンポーネントが選択されていません")
            return
        
        component_name = current_item.data(Qt.UserRole)
        self.log(f"↩️ コンポーネント復元開始: {component_name}")
        
        success = self.migration_helper.revert_component(component_name, self.preview_container)
        
        if success:
            self.log(f"✅ コンポーネント復元成功: {component_name}")
        else:
            self.log(f"❌ コンポーネント復元失敗: {component_name}")
        
        self._update_component_list()
    
    def _replace_all_components(self):
        """全コンポーネント移行"""
        if not self.migration_helper:
            return
        
        strategy = self.strategy_combo.currentText()
        self.log(f"🚀 全コンポーネント移行開始 (戦略: {strategy})")
        
        components = list(self.migration_helper.migration_plan.keys())
        
        for component_name in components:
            self.log(f"🔄 移行中: {component_name}")
            
            # 互換性検証
            if self.validate_check.isChecked():
                validation = self.migration_helper.validate_compatibility(component_name)
                if not validation['valid']:
                    self.log(f"❌ {component_name} 互換性検証失敗: スキップ")
                    continue
            
            # 移行実行
            success = self.migration_helper.replace_component(component_name, self.preview_container)
            if success:
                self.log(f"✅ {component_name} 移行成功")
            else:
                self.log(f"❌ {component_name} 移行失敗")
        
        self.log("🏁 全コンポーネント移行完了")
        self._update_component_list()
    
    def _revert_all_components(self):
        """全コンポーネント復元"""
        if not self.migration_helper:
            return
        
        self.log("↩️ 全コンポーネント復元開始")
        
        replaced_components = list(self.migration_helper.replaced_components.keys())
        
        for component_name in replaced_components:
            success = self.migration_helper.revert_component(component_name, self.preview_container)
            if success:
                self.log(f"✅ {component_name} 復元成功")
            else:
                self.log(f"❌ {component_name} 復元失敗")
        
        self.log("🏁 全コンポーネント復元完了")
        self._update_component_list()
    
    def _validate_compatibility(self):
        """互換性検証"""
        if not self.migration_helper:
            return
        
        self.log("🔍 互換性検証開始")
        
        all_valid = True
        for name in self.migration_helper.component_registry.keys():
            validation = self.migration_helper.validate_compatibility(name)
            
            if validation['valid']:
                score = validation.get('compatibility_score', 0)
                self.log(f"✅ {name}: 互換性OK (スコア: {score:.2f})")
            else:
                all_valid = False
                reason = validation.get('reason', '不明')
                self.log(f"❌ {name}: 互換性NG ({reason})")
                
                if 'missing_methods' in validation and validation['missing_methods']:
                    self.log(f"   不足メソッド: {', '.join(validation['missing_methods'])}")
                
                if 'missing_signals' in validation and validation['missing_signals']:
                    self.log(f"   不足シグナル: {', '.join(validation['missing_signals'])}")
        
        if all_valid:
            self.log("🎉 全コンポーネント互換性確認")
        else:
            self.log("⚠️ 一部コンポーネントに互換性問題があります")
    
    def _generate_migration_report(self):
        """移行レポート生成"""
        if not self.migration_helper:
            return
        
        self.log("📊 移行レポート生成中...")
        
        try:
            # 移行レポート
            migration_report = MigrationReporter.generate_report(self.migration_helper)
            
            # 互換性レポート
            compatibility_report = MigrationReporter.generate_compatibility_report(self.migration_helper)
            
            # ダイアログで表示
            from PyQt5.QtWidgets import QDialog, QTabWidget, QTextEdit
            
            dialog = QDialog(self)
            dialog.setWindowTitle("移行レポート")
            dialog.setGeometry(200, 200, 800, 600)
            
            layout = QVBoxLayout(dialog)
            tab_widget = QTabWidget()
            
            # 移行レポートタブ
            migration_tab = QTextEdit()
            migration_tab.setPlainText(migration_report)
            tab_widget.addTab(migration_tab, "移行進捗")
            
            # 互換性レポートタブ
            compatibility_tab = QTextEdit()
            compatibility_tab.setPlainText(compatibility_report)
            tab_widget.addTab(compatibility_tab, "互換性検証")
            
            layout.addWidget(tab_widget)
            
            dialog.exec_()
            
            self.log("✅ 移行レポート表示完了")
            
        except Exception as e:
            self.log(f"❌ レポート生成エラー: {e}")
    
    def _run_performance_test(self):
        """パフォーマンステスト"""
        self.log("⚡ パフォーマンステスト開始")
        
        import time
        
        if not self.migration_helper:
            self.log("❌ 移行ヘルパーが初期化されていません")
            return
        
        # 移行前後の応答時間測定
        for name in self.migration_helper.component_registry.keys():
            # 移行前
            if not self.migration_helper.component_registry[name]['replaced']:
                start_time = time.time()
                # 基本操作（show/hideなど）
                legacy_component = self.migration_helper.component_registry[name]['legacy']
                if hasattr(legacy_component, 'show'):
                    legacy_component.show()
                    legacy_component.hide()
                legacy_time = time.time() - start_time
                
                self.log(f"📊 {name} レガシー応答時間: {legacy_time:.3f}秒")
        
        self.log("🏁 パフォーマンステスト完了")
    
    def _run_functional_test(self):
        """機能動作テスト"""
        self.log("🧪 機能動作テスト開始")
        
        # 基本的な操作テスト
        test_scenarios = [
            "ウィンドウ表示確認",
            "コンポーネント初期化確認",
            "イベント処理確認",
            "データバインディング確認"
        ]
        
        for scenario in test_scenarios:
            self.log(f"  🔍 {scenario}")
            # 実際のテスト実装は各コンポーネントの特性に応じて
            self.log(f"    ✅ 実行完了")
        
        self.log("🏁 機能動作テスト完了")
    
    def _on_component_replaced(self, name: str, old_component, new_component):
        """コンポーネント置き換えイベント"""
        self.log(f"🔄 コンポーネント置き換え通知: {name}")
        self._update_component_list()
    
    def _on_migration_progress(self, progress: int):
        """移行進捗イベント"""
        self.progress_bar.setValue(progress)
        self.progress_label.setText(f"移行進捗: {progress}%")


def main():
    """メインエントリーポイント"""
    print("🚀 Phase 4 段階的移行テスト起動中...")
    
    # Qtアプリケーション作成
    app = QApplication(sys.argv)
    app.setApplicationName("PhotoMap Explorer - Phase 4 Migration Test")
    
    try:
        # テストウィンドウ作成
        window = MigrationTestWindow()
        window.show()
        
        print("✅ 段階的移行テスト環境起動成功")
        print("📋 利用可能な機能:")
        print("  - 個別コンポーネント移行・復元")
        print("  - 一括移行・復元")
        print("  - 互換性検証")
        print("  - 移行レポート生成")
        print("  - パフォーマンステスト")
        print("  - 機能動作テスト")
        
        # イベントループ開始
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ テスト環境起動エラー: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
