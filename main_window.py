from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar, QListWidgetItem
from ui.image_preview import ImagePreviewView
from ui.folder_browser import create_folder_view
from ui.thumbnail_list import create_thumbnail_list
from ui.map_view import create_map_view
from ui.controls import create_controls
from logic import find_images_in_directory, load_pixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QIcon, QPixmap

import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.image_paths = []
        self.current_index = -1

        self.setup_ui()
        self.statusBar().showMessage("アプリが起動しました！", 3000)

    def setup_ui(self):
        # UIコンポーネントを各モジュールからインポートして初期化
        self.preview_view = ImagePreviewView()
        self.folder_view = create_folder_view(self.on_folder_selected)
        self.folder_view.setTextElideMode(Qt.ElideNone)  # フォルダ名の省略を防ぐ設定を追加
        self.folder_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.folder_view.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.folder_view.header().setSectionResizeMode(2, QHeaderView.Interactive)
        self.folder_view.setColumnWidth(0, 300)
        self.folder_view.setColumnWidth(1, 100)
        self.folder_view.setColumnWidth(2, 150)
        self.thumbnail_list = create_thumbnail_list(self.on_thumbnail_clicked)
        self.map_view = create_map_view()
        controls_widget, self.address_bar, self.return_to_root_button = create_controls(self.on_address_entered, self.on_return_to_root)

        # アドレスバー部分を固定高さに設定
        controls_widget_wrapper = QWidget()
        controls_layout = QVBoxLayout(controls_widget_wrapper)
        controls_layout.addWidget(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(0)
        controls_widget_wrapper.setFixedHeight(50)  # 固定高さを設定

        # 右ペイン（画像＋地図）を縦方向に分割
        right_splitter = QSplitter()
        right_splitter.setOrientation(Qt.Vertical)
        right_splitter.addWidget(self.preview_view)  # 上：画像プレビュー
        right_splitter.addWidget(self.map_view)      # 下：地図ビュー

        # 両ビューが等しいスペースを取るように設定
        right_splitter.setStretchFactor(0, 1)  # プレビュー
        right_splitter.setStretchFactor(1, 1)  # 地図ビュー
        right_splitter.setSizes([100, 100])    # 初期状態で等分割# 右ペイン（画像＋地図）を縦方向に分割
        
        # 中央ペイン（サムネイルビュー）
        middle_splitter = QSplitter()
        middle_splitter.addWidget(self.thumbnail_list)

        # 全体レイアウト：左（フォルダビュー）、中央（サムネイルビュー）、右（画像＋地図）を水平分割
        main_splitter = QSplitter()
        main_splitter.addWidget(self.folder_view)    # 左：フォルダビュー
        main_splitter.addWidget(middle_splitter)     # 中央：サムネイルビュー
        main_splitter.addWidget(right_splitter)      # 右：画像＋地図

        # メインウィジェットのセットアップ
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(controls_widget_wrapper)    # アドレスバー部分
        layout.addWidget(main_splitter)              # 全体スプリッターを配置
        self.setCentralWidget(main_widget)
         
        self.setStatusBar(QStatusBar())

    def on_folder_selected(self, index):
        dir_path = self.folder_view.model().filePath(index)
        if dir_path:
            self.image_paths = find_images_in_directory (dir_path)
            self.update_thumbnail_list()

    def on_thumbnail_clicked(self, item):
        """
        サムネイルがクリックされたときに画像をプレビュー表示
        """
        # クリックされたアイテムのインデックスを取得
        index = self.thumbnail_list.row(item)  # QListWidgetから行番号を取得
        image_path = self.image_paths[index]  # 正しいインデックスで画像パスを取得
        
        # QPixmapを生成しプレビューに設定
        pixmap = QPixmap(image_path)  # 画像パスからQPixmapを生成
        if not pixmap.isNull():
            self.preview_view.set_image(pixmap)
        else:
            print(f"画像の読み込みに失敗しました: {image_path}")

    def on_address_entered(self):
        folder_path = self.address_bar.text()
        if folder_path:
            self.folder_view.setRootIndex(self.folder_view.model().index(folder_path))
            self.image_paths = find_images_in_directory (folder_path)
            self.update_thumbnail_list()

    def on_return_to_root(self):
        self.folder_view.setRootIndex(self.folder_view.model().index(""))
        self.statusBar().showMessage("全ドライブに戻りました", 3000)

    def update_thumbnail_list(self):
        self.thumbnail_list.clear()  # リストを初期化
        for image_path in self.image_paths:
            icon = QIcon(load_pixmap(image_path))  # アイコンを作成
            item = QListWidgetItem(icon, os.path.basename(image_path))  # リストアイテムを作成
            self.thumbnail_list.addItem(item)  # アイテムを追加