import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileSystemModel, QTreeView, QListWidget, QListWidgetItem, QLabel,
    QPushButton, QSplitter, QFrame, QStatusBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.image_paths = []      # 全画像パス
        self.current_index = -1    # 現在選択インデックス

        self.setup_ui()
        self.load_images_from_directory(self.get_home_dir())  # 初期ディレクトリからロード

    def get_home_dir(self):
        return os.path.expanduser("~")

    def setup_ui(self):
        # フォルダビュー
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath('')

        # フォルダビュー（QTreeView）初期化
        self.folder_view = QTreeView()
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setRootIndex(self.folder_model.index(self.get_home_dir()))
        self.folder_view.setHeaderHidden(True)
        # 横スクロールバーを必要に応じて表示（長いパスに対応）
        self.folder_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 横スクロール有効化
        self.folder_view.setTextElideMode(Qt.ElideNone)  # 「...」省略を防ぐ
        self.folder_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)  # 列幅を内容に自動調整
        self.folder_view.header().setStretchLastSection(False)  # 最終列の不必要な引き伸ばしを防止
        self.folder_view.setMinimumWidth(280)  # 📌 ペインが極端に狭くならないように制限
        self.folder_view.clicked.connect(self.on_folder_selected)

        # サムネイル一覧
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setIconSize(QSize(80, 80))
        self.thumbnail_list.itemClicked.connect(self.on_thumbnail_clicked)

        # プレビューパネルとナビゲーション
        self.preview_label = QLabel("🖼 Preview")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setFrameStyle(QFrame.Box)

        prev_button = QPushButton("◀")
        next_button = QPushButton("▶")
        prev_button.clicked.connect(self.show_previous_image)
        next_button.clicked.connect(self.show_next_image)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(next_button)

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_label, stretch=9)
        preview_layout.addLayout(nav_layout, stretch=1)

        preview_container = QWidget()
        preview_container.setLayout(preview_layout)

        # 地図ビュー（仮置き）
        self.map_view = QWebEngineView()
        self.map_view.setHtml("<h3>🌍 Leaflet map placeholder</h3>")

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(preview_container)
        right_splitter.addWidget(self.map_view)
        right_splitter.setSizes([600, 300])

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(right_splitter)
        right_widget.setLayout(right_layout)

        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.addWidget(self.folder_view)
        top_splitter.addWidget(self.thumbnail_list)
        top_splitter.addWidget(right_widget)
        top_splitter.setSizes([250, 400, 750])

        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_splitter)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("📸 Ready")

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def load_images_from_directory(self, directory):
        self.image_paths = []
        self.thumbnail_list.clear()
        supported_exts = ('.jpg', '.jpeg', '.png')

        for entry in os.listdir(directory):
            if entry.lower().endswith(supported_exts):
                full_path = os.path.join(directory, entry)
                self.image_paths.append(full_path)

                icon = QIcon(full_path)
                item = QListWidgetItem(icon, os.path.basename(entry))
                self.thumbnail_list.addItem(item)

        if self.image_paths:
            self.current_index = 0
            self.display_image_by_index(self.current_index)

    def display_image_by_index(self, index):
        if 0 <= index < len(self.image_paths):
            pixmap = QPixmap(self.image_paths[index])
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.status_bar.showMessage(f"{os.path.basename(self.image_paths[index])}")
            self.current_index = index

    def on_thumbnail_clicked(self, item):
        index = self.thumbnail_list.row(item)
        self.display_image_by_index(index)

    def on_folder_selected(self, index):
        dir_path = self.folder_model.filePath(index)
        if os.path.isdir(dir_path):
            self.load_images_from_directory(dir_path)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.display_image_by_index(self.current_index)

    def show_previous_image(self):
        if self.current_index > 0:
            self.display_image_by_index(self.current_index - 1)

    def show_next_image(self):
        if self.current_index < len(self.image_paths) - 1:
            self.display_image_by_index(self.current_index + 1)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
