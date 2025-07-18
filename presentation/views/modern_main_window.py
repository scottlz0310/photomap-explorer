"""
New Modern Main Window

qt-theme-manager + Figmaデザインベースの新しいメインウィンドウ
完全リファクタリング版
"""

import os
import sys
import logging
from pathlib import Path
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QSplitter, QGroupBox, QListWidget, QLabel, 
                            QPushButton, QApplication, QStatusBar)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon

# 新しいテーママネージャーのインポート
try:
    from qt_theme_manager import ThemeManager
    HAS_QT_THEME_MANAGER = True
except ImportError:
    HAS_QT_THEME_MANAGER = False
    print("qt-theme-manager not available, using fallback")


class ModernMainWindow(QMainWindow):
    """
    モダンなメインウィンドウ
    
    - qt-theme-manager使用
    - Figmaデザインベース
    - シンプルなトップダウン設計
    """
    
    # シグナル定義
    folder_selected = pyqtSignal(str)
    image_selected = pyqtSignal(str)
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        
        # ログ設定
        self.logger = logging.getLogger(__name__)
        self.logger.info("ModernMainWindow初期化開始")
        
        # 状態管理
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        
        # UI要素の参照
        self.folder_list = None
        self.thumbnail_list = None
        self.preview_panel = None
        self.map_panel = None
        self.status_info = None
        
        # 新しいテーママネージャー
        self._setup_theme_manager()
        
        # UI構築（トップダウン）
        self._setup_window_properties()
        self._setup_main_layout()
        self._apply_figma_styling()
        
        self.logger.info("ModernMainWindow初期化完了")
    
    def _setup_theme_manager(self):
        """新しいテーママネージャーの設定"""
        if HAS_QT_THEME_MANAGER:
            self.theme_manager = ThemeManager()
            self.theme_manager.set_theme("dark")  # デフォルトダークテーマ
            self.logger.info("qt-theme-manager設定完了")
        else:
            self.theme_manager = None
            self.logger.warning("qt-theme-manager利用不可、フォールバック")
    
    def _setup_window_properties(self):
        """ウィンドウ基本プロパティの設定"""
        # ウィンドウサイズ（Figmaデザインベース）
        self.setWindowTitle("PhotoMap Explorer v2.2.0")
        self.setGeometry(100, 100, 1440, 900)  # Figmaデザインサイズ
        
        # アイコン設定
        icon_path = Path(__file__).parent.parent.parent / "assets" / "pme_icon.png"
        if icon_path.exists():
            self.setWindowIcon(QIcon(str(icon_path)))
        
        self.logger.debug("ウィンドウプロパティ設定完了")
    
    def _setup_main_layout(self):
        """メインレイアウトの構築（トップダウン）"""
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # メインレイアウト
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. ツールバー
        self._create_toolbar(main_layout)
        
        # 2. メインコンテンツエリア
        self._create_main_content(main_layout)
        
        # 3. ステータスバー
        self._create_status_bar()
        
        self.logger.debug("メインレイアウト構築完了")
    
    def _create_toolbar(self, parent_layout):
        """ツールバーの作成"""
        toolbar_widget = QWidget()
        toolbar_widget.setMaximumHeight(50)
        toolbar_widget.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                border-bottom: 1px solid #404040;
            }
        """)
        
        toolbar_layout = QHBoxLayout(toolbar_widget)
        toolbar_layout.setContentsMargins(10, 5, 10, 5)
        
        # フォルダ選択ボタン
        self.folder_btn = QPushButton("📁 フォルダ選択")
        self.folder_btn.setMaximumHeight(35)
        self.folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QPushButton:pressed {
                background-color: #303030;
            }
        """)
        toolbar_layout.addWidget(self.folder_btn)
        
        # アドレス表示
        self.address_label = QLabel("📁 フォルダが選択されていません")
        self.address_label.setStyleSheet("""
            QLabel {
                color: #cccccc;
                font-size: 12px;
                padding: 5px;
            }
        """)
        toolbar_layout.addWidget(self.address_label, 1)
        
        # テーマ切り替えボタン
        self.theme_btn = QPushButton("🌙 ダーク")
        self.theme_btn.setMaximumHeight(35)
        self.theme_btn.setMaximumWidth(80)
        self.theme_btn.setStyleSheet("""
            QPushButton {
                background-color: #404040;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
        toolbar_layout.addWidget(self.theme_btn)
        
        parent_layout.addWidget(toolbar_widget)
        
        # イベント接続
        self.folder_btn.clicked.connect(self._on_folder_select)
        self.theme_btn.clicked.connect(self._on_theme_toggle)
        
        self.logger.debug("ツールバー作成完了")
    
    def _create_main_content(self, parent_layout):
        """メインコンテンツエリアの作成"""
        # 水平スプリッター
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #404040;
                width: 2px;
            }
            QSplitter::handle:hover {
                background-color: #606060;
            }
        """)
        
        # 左パネル
        left_panel = self._create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右パネル
        right_panel = self._create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # スプリッター比率（Figmaデザインベース）
        main_splitter.setSizes([400, 1040])  # 左:右 = 28:72
        
        parent_layout.addWidget(main_splitter)
        
        self.logger.debug("メインコンテンツエリア作成完了")
    
    def _create_left_panel(self):
        """左パネルの作成"""
        left_panel = QWidget()
        left_panel.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                border-right: 1px solid #404040;
            }
        """)
        
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(5, 5, 5, 5)
        left_layout.setSpacing(5)
        
        # フォルダ内容
        folder_group = QGroupBox("📁 フォルダ内容")
        folder_group.setStyleSheet("""
            QGroupBox {
                color: #cccccc;
                font-weight: bold;
                border: 1px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        folder_layout = QVBoxLayout(folder_group)
        self.folder_list = QListWidget()
        self.folder_list.setStyleSheet("""
            QListWidget {
                background-color: #2b2b2b;
                color: #cccccc;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-radius: 3px;
            }
            QListWidget::item:selected {
                background-color: #0078d4;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #404040;
            }
        """)
        self.folder_list.setMinimumHeight(120)
        self.folder_list.setMaximumHeight(180)
        folder_layout.addWidget(self.folder_list)
        left_layout.addWidget(folder_group)
        
        # サムネイル
        thumbnail_group = QGroupBox("🖼️ サムネイル")
        thumbnail_group.setStyleSheet(folder_group.styleSheet())
        
        thumbnail_layout = QVBoxLayout(thumbnail_group)
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setStyleSheet(self.folder_list.styleSheet())
        self.thumbnail_list.setMinimumHeight(200)
        thumbnail_layout.addWidget(self.thumbnail_list)
        left_layout.addWidget(thumbnail_group)
        
        # イベント接続
        self.thumbnail_list.itemClicked.connect(self._on_image_select)
        self.thumbnail_list.currentRowChanged.connect(self._on_image_select)
        
        # 詳細情報
        info_group = QGroupBox("📋 詳細情報")
        info_group.setStyleSheet(folder_group.styleSheet())
        
        info_layout = QVBoxLayout(info_group)
        self.status_info = QLabel("画像を選択すると詳細情報が表示されます")
        self.status_info.setStyleSheet("""
            QLabel {
                color: #cccccc;
                background-color: #2b2b2b;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 10px;
                font-size: 11px;
            }
        """)
        self.status_info.setWordWrap(True)
        self.status_info.setMinimumHeight(100)
        self.status_info.setMaximumHeight(150)
        info_layout.addWidget(self.status_info)
        left_layout.addWidget(info_group)
        
        self.logger.debug("左パネル作成完了")
        return left_panel
    
    def _create_right_panel(self):
        """右パネルの作成"""
        right_panel = QWidget()
        right_panel.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
            }
        """)
        
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        right_layout.setSpacing(5)
        
        # 垂直スプリッター
        right_splitter = QSplitter(Qt.Orientation.Vertical)
        right_splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #404040;
                height: 2px;
            }
            QSplitter::handle:hover {
                background-color: #606060;
            }
        """)
        
        # 地図パネル
        map_group = QGroupBox("🗺️ 地図")
        map_group.setStyleSheet("""
            QGroupBox {
                color: #cccccc;
                font-weight: bold;
                border: 1px solid #404040;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        map_layout = QVBoxLayout(map_group)
        self.map_panel = QLabel("地図が表示されます")
        self.map_panel.setStyleSheet("""
            QLabel {
                background-color: #2b2b2b;
                color: #cccccc;
                border: 1px solid #404040;
                border-radius: 3px;
                padding: 20px;
                font-size: 14px;
            }
        """)
        self.map_panel.setMinimumHeight(300)
        self.map_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        map_layout.addWidget(self.map_panel)
        right_splitter.addWidget(map_group)
        
        # プレビューパネル
        preview_group = QGroupBox("🖼️ プレビュー")
        preview_group.setStyleSheet(map_group.styleSheet())
        
        preview_layout = QVBoxLayout(preview_group)
        self.preview_panel = QLabel("画像プレビューが表示されます")
        self.preview_panel.setStyleSheet(self.map_panel.styleSheet())
        self.preview_panel.setMinimumHeight(200)
        self.preview_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.preview_panel)
        right_splitter.addWidget(preview_group)
        
        # 垂直スプリッター比率
        right_splitter.setSizes([400, 300])  # 上:下 = 57:43
        
        right_layout.addWidget(right_splitter)
        
        self.logger.debug("右パネル作成完了")
        return right_panel
    
    def _create_status_bar(self):
        """ステータスバーの作成"""
        status_bar = QStatusBar()
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #2b2b2b;
                color: #cccccc;
                border-top: 1px solid #404040;
            }
        """)
        status_bar.showMessage("PhotoMap Explorer v2.2.0 - 新しいUI設計で起動しました")
        self.setStatusBar(status_bar)
        
        self.logger.debug("ステータスバー作成完了")
    
    def _apply_figma_styling(self):
        """Figmaデザインベースのスタイリング適用"""
        # 新しいテーママネージャーを使用
        if self.theme_manager:
            self.theme_manager.apply_theme(self)
        
        # 全体のベーススタイル
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #cccccc;
            }
        """)
        
        self.logger.debug("Figmaスタイリング適用完了")
    
    def _on_folder_select(self):
        """フォルダ選択イベント"""
        from PyQt5.QtWidgets import QFileDialog
        
        folder = QFileDialog.getExistingDirectory(
            self, "フォルダを選択", 
            self.current_folder or os.path.expanduser("~")
        )
        
        if folder:
            self.current_folder = folder
            self.address_label.setText(f"📁 {folder}")
            self._load_folder_content(folder)
            self.folder_selected.emit(folder)
            self.logger.info(f"フォルダ選択: {folder}")
    
    def _load_folder_content(self, folder_path):
        """フォルダ内容の読み込み"""
        try:
            # フォルダ内容をクリア
            self.folder_list.clear()
            self.thumbnail_list.clear()
            self.current_images = []
            
            # サポートする画像形式
            image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
            
            # フォルダ内容を読み込み
            folder_path = Path(folder_path)
            all_items = []
            image_files = []
            
            # フォルダとファイルを取得
            for item in folder_path.iterdir():
                if item.is_dir():
                    all_items.append(f"📁 {item.name}")
                elif item.suffix.lower() in image_extensions:
                    image_files.append(item)
                    all_items.append(f"🖼️ {item.name}")
                else:
                    all_items.append(f"📄 {item.name}")
            
            # フォルダリストに追加
            for item in sorted(all_items):
                self.folder_list.addItem(item)
            
            # 画像ファイルをサムネイルリストに追加
            for image_file in sorted(image_files):
                self.thumbnail_list.addItem(f"🖼️ {image_file.name}")
                self.current_images.append(str(image_file))
            
            # 情報を更新
            folder_count = len([item for item in all_items if item.startswith("📁")])
            image_count = len(image_files)
            total_count = len(all_items)
            
            self.status_info.setText(f"""
フォルダ: {folder_count}個
画像: {image_count}個
合計: {total_count}個

選択中のフォルダ:
{folder_path.name}
            """.strip())
            
            self.logger.info(f"フォルダ内容読み込み完了: {total_count}個のアイテム（画像{image_count}個）")
            
        except Exception as e:
            self.logger.error(f"フォルダ内容読み込みエラー: {e}")
            self.status_info.setText(f"エラー: フォルダの読み込みに失敗しました\n{str(e)}")
    
    def _on_image_select(self):
        """画像選択イベント"""
        current_row = self.thumbnail_list.currentRow()
        if current_row >= 0 and current_row < len(self.current_images):
            selected_image = self.current_images[current_row]
            self.selected_image = selected_image
            self.image_selected.emit(selected_image)
            self.logger.info(f"画像選択: {selected_image}")
            
            # 詳細情報を更新
            self._update_image_info(selected_image)
    
    def _update_image_info(self, image_path):
        """画像詳細情報の更新（PILLOWを使わない基本版）"""
        try:
            import os
            from datetime import datetime
            
            # 基本情報
            file_path = Path(image_path)
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # ファイル拡張子から形式を推測
            format_name = file_path.suffix.upper().replace('.', '')
            
            # 更新日時
            modification_time = file_path.stat().st_mtime
            modified_date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
            
            # 詳細情報を表示（PILLOWなし版）
            info_text = f"""
📁 ファイル名: {file_path.name}
💾 ファイルサイズ: {file_size_mb:.2f} MB
🎨 形式: {format_name}
� 更新日時: {modified_date}

📂 パス:
{file_path.parent.name}

💡 注意: 画像サイズやEXIF情報を表示するには
PILLOWライブラリが必要です
            """.strip()
            
            self.status_info.setText(info_text)
            
        except Exception as e:
            self.logger.error(f"画像情報取得エラー: {e}")
            self.status_info.setText(f"画像情報の取得に失敗しました\n{str(e)}")
    
    def _update_image_info(self, image_path):
        """画像詳細情報の更新（PILLOW + exifread使用）"""
        try:
            # 新しいImageInfoExtractorを使用
            from logic.image_info_extractor import ImageInfoExtractor
            
            extractor = ImageInfoExtractor()
            formatted_info = extractor.format_info_text(image_path)
            
            self.status_info.setText(formatted_info)
            
        except ImportError:
            # フォールバック: 基本情報のみ
            self._update_image_info_basic(image_path)
        except Exception as e:
            self.logger.error(f"画像情報取得エラー: {e}")
            self.status_info.setText(f"画像情報の取得に失敗しました\n{str(e)}")
    
    def _update_image_info_basic(self, image_path):
        """基本的な画像情報の更新（フォールバック）"""
        try:
            import os
            from datetime import datetime
            
            # 基本情報
            file_path = Path(image_path)
            file_size = file_path.stat().st_size
            file_size_mb = file_size / (1024 * 1024)
            
            # ファイル拡張子から形式を推測
            format_name = file_path.suffix.upper().replace('.', '')
            
            # 更新日時
            modification_time = file_path.stat().st_mtime
            modified_date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d %H:%M:%S')
            
            # 詳細情報を表示（基本版）
            info_text = f"""📁 ファイル名: {file_path.name}
💾 ファイルサイズ: {file_size_mb:.2f} MB
🎨 形式: {format_name}
📅 更新日時: {modified_date}

📂 フォルダ: {file_path.parent.name}
📍 フルパス: {file_path.parent}

💡 注意: 詳細な画像情報やEXIF情報を表示するには
PILLOWとexifreadライブラリが必要です"""
            
            self.status_info.setText(info_text)
            
        except Exception as e:
            self.logger.error(f"基本画像情報取得エラー: {e}")
            self.status_info.setText(f"基本情報の取得に失敗しました\n{str(e)}")
    
    def _on_theme_toggle(self):
        """テーマ切り替えイベント"""
        if self.theme_manager:
            current_theme = self.theme_manager.get_current_theme()
            new_theme = "light" if current_theme == "dark" else "dark"
            self.theme_manager.set_theme(new_theme)
            
            # ボタンテキスト更新
            self.theme_btn.setText("☀️ ライト" if new_theme == "dark" else "🌙 ダーク")
            
            self.theme_changed.emit(new_theme)
            self.logger.info(f"テーマ切り替え: {new_theme}")
        else:
            self.logger.warning("テーママネージャー利用不可")


def main():
    """テスト用のメイン関数"""
    app = QApplication(sys.argv)
    
    # ログ設定
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    window = ModernMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
