"""
簡素化された新UIメインビュー

Clean Architectureのコンポーネントを使用するが、
複雑なMVVMパターンを避けてシンプルに実装します。
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QSplitter, QWidget, 
                            QStatusBar, QHBoxLayout, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class SimpleNewMainWindow(QMainWindow):
    """
    簡素化された新UIメインウィンドウ
    
    Phase 4で作成したコンポーネントを使用しますが、
    複雑な依存関係なしに動作します。
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - 新UI (Clean Architecture)")
        self.setGeometry(100, 100, 1400, 900)
        
        # アイコン設定
        self._setup_icon()
        
        # UI構築
        self._setup_ui()
        
        # ステータス表示
        self.show_status_message("新UI (Clean Architecture) で起動しました")
    
    def _setup_icon(self):
        """アイコン設定"""
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "pme_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
    
    def _setup_ui(self):
        """UIセットアップ"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # ヘッダー情報
        header_layout = QHBoxLayout()
        
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        
        from PyQt5.QtWidgets import QLabel
        title_label = QLabel("🚀 PhotoMap Explorer - Clean Architecture版")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2196F3; margin: 10px;")
        info_layout.addWidget(title_label)
        
        desc_label = QLabel("新しいClean Architectureパターンで実装されたUI")
        desc_label.setStyleSheet("color: #666; margin: 5px 10px;")
        info_layout.addWidget(desc_label)
        
        header_layout.addWidget(info_widget)
        header_layout.addStretch()
        
        # テストボタン
        test_btn = QPushButton("コンポーネントテスト")
        test_btn.clicked.connect(self._run_component_test)
        header_layout.addWidget(test_btn)
        
        layout.addLayout(header_layout)
        
        # メインスプリッター
        main_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(main_splitter)
        
        # 左パネル：ナビゲーション
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右パネル：コンテンツ
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # ステータスバー
        self.statusBar().showMessage("準備完了")
        
        # スプリッターサイズ調整
        main_splitter.setSizes([300, 1100])
    
    def _create_left_panel(self):
        """左パネル作成（ナビゲーション）"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # アドレスバー
        try:
            from presentation.views.controls.address_bar import create_address_bar_widget
            
            def dummy_callback(*args):
                self.show_status_message(f"アドレスバー操作: {args}")
            
            address_widget, address_edit = create_address_bar_widget("C:\\", dummy_callback, dummy_callback)
            
            from PyQt5.QtWidgets import QGroupBox
            address_group = QGroupBox("📍 ナビゲーション")
            address_layout = QVBoxLayout(address_group)
            address_layout.addWidget(address_widget)
            layout.addWidget(address_group)
            
        except Exception as e:
            self._add_error_widget(layout, "アドレスバー", str(e))
        
        # フォルダパネル
        try:
            from presentation.views.panels.folder_panel import create_folder_panel
            
            def folder_selected(path):
                self.show_status_message(f"フォルダ選択: {path}")
            
            folder_panel = create_folder_panel(folder_selected)
            
            folder_group = QGroupBox("📁 フォルダ")
            folder_layout = QVBoxLayout(folder_group)
            folder_layout.addWidget(folder_panel)
            layout.addWidget(folder_group)
            
        except Exception as e:
            self._add_error_widget(layout, "フォルダパネル", str(e))
        
        return panel
    
    def _create_right_panel(self):
        """右パネル作成（メインコンテンツ）"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # 上部：サムネイル
        try:
            from presentation.views.controls.thumbnail_list import create_thumbnail_list
            
            def thumbnail_clicked(image_path):
                self.show_status_message(f"画像選択: {image_path}")
            
            thumbnail_list = create_thumbnail_list(thumbnail_clicked)
            
            from PyQt5.QtWidgets import QGroupBox
            thumbnail_group = QGroupBox("🖼️ サムネイル")
            thumbnail_layout = QVBoxLayout(thumbnail_group)
            thumbnail_layout.addWidget(thumbnail_list)
            layout.addWidget(thumbnail_group)
            
        except Exception as e:
            self._add_error_widget(layout, "サムネイルリスト", str(e))
        
        # 下部スプリッター：プレビューと地図
        bottom_splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(bottom_splitter)
        
        # プレビューパネル
        try:
            from presentation.views.panels.preview_panel import create_preview_panel
            
            preview_panel = create_preview_panel()
            
            preview_group = QGroupBox("👁️ プレビュー")
            preview_layout = QVBoxLayout(preview_group)
            preview_layout.addWidget(preview_panel)
            bottom_splitter.addWidget(preview_group)
            
        except Exception as e:
            self._add_error_widget_to_splitter(bottom_splitter, "プレビューパネル", str(e))
        
        # マップパネル
        try:
            from presentation.views.panels.map_panel import create_map_panel
            
            map_panel = create_map_panel()
            
            map_group = QGroupBox("🗺️ 地図")
            map_layout = QVBoxLayout(map_group)
            map_layout.addWidget(map_panel)
            bottom_splitter.addWidget(map_group)
            
        except Exception as e:
            self._add_error_widget_to_splitter(bottom_splitter, "マップパネル", str(e))
        
        # 下部スプリッターサイズ調整
        bottom_splitter.setSizes([550, 550])
        
        return panel
    
    def _add_error_widget(self, layout, component_name, error_message):
        """エラーウィジェットを追加"""
        from PyQt5.QtWidgets import QLabel, QGroupBox
        
        group = QGroupBox(f"❌ {component_name} (エラー)")
        group_layout = QVBoxLayout(group)
        
        error_label = QLabel(f"エラー: {error_message}")
        error_label.setStyleSheet("color: red; padding: 10px;")
        error_label.setWordWrap(True)
        group_layout.addWidget(error_label)
        
        layout.addWidget(group)
    
    def _add_error_widget_to_splitter(self, splitter, component_name, error_message):
        """スプリッターにエラーウィジェットを追加"""
        from PyQt5.QtWidgets import QLabel, QGroupBox
        
        group = QGroupBox(f"❌ {component_name} (エラー)")
        group_layout = QVBoxLayout(group)
        
        error_label = QLabel(f"エラー: {error_message}")
        error_label.setStyleSheet("color: red; padding: 10px;")
        error_label.setWordWrap(True)
        group_layout.addWidget(error_label)
        
        splitter.addWidget(group)
    
    def _run_component_test(self):
        """コンポーネントテスト実行"""
        from PyQt5.QtWidgets import QMessageBox
        
        test_results = []
        
        # ファクトリ関数テスト
        components = [
            ("アドレスバー", "presentation.views.controls.address_bar", "create_address_bar_widget"),
            ("フォルダパネル", "presentation.views.panels.folder_panel", "create_folder_panel"),
            ("サムネイル", "presentation.views.controls.thumbnail_list", "create_thumbnail_list"),
            ("プレビュー", "presentation.views.panels.preview_panel", "create_preview_panel"),
            ("地図", "presentation.views.panels.map_panel", "create_map_panel")
        ]
        
        for name, module_name, function_name in components:
            try:
                module = __import__(module_name, fromlist=[function_name])
                factory = getattr(module, function_name)
                
                # ダミー引数でテスト
                if name == "アドレスバー":
                    factory("C:\\", lambda x: None, lambda: None)
                elif name == "フォルダパネル":
                    factory(lambda x: None)
                elif name == "サムネイル":
                    factory(lambda x: None)
                else:
                    factory()
                
                test_results.append(f"✅ {name}: OK")
                
            except Exception as e:
                test_results.append(f"❌ {name}: {e}")
        
        result_text = "🧪 コンポーネントテスト結果:\n\n" + "\n".join(test_results)
        QMessageBox.information(self, "テスト結果", result_text)
    
    def show_status_message(self, message):
        """ステータスメッセージを表示"""
        self.statusBar().showMessage(message)
        print(f"[新UI] {message}")
    
    def update_folder_path(self, path):
        """フォルダパス更新（外部から呼び出し可能）"""
        self.show_status_message(f"フォルダパス更新: {path}")
