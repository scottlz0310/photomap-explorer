from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar
from ui.folder_panel import FolderPanel
from ui.thumbnail_panel import ThumbnailPanel
from ui.preview_panel import PreviewPanel
from ui.map_panel import MapPanel
from ui.controls import create_controls
from logic.image_utils import find_images_in_directory, load_pixmap, extract_gps_coords, generate_map_html
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.image_paths = []

        self.folder_panel = FolderPanel(self.on_folder_selected)
        self.thumbnail_panel = ThumbnailPanel(self.on_thumbnail_clicked, self.set_thumbnail_size_and_width)
        self.preview_panel = PreviewPanel()
        self.map_panel = MapPanel()

        controls_widget, self.address_bar, self.return_to_root_button = create_controls(
            self.on_address_entered, self.on_return_to_root
        )
        controls_widget.setFixedHeight(40)  # アドレスバー＋ボタンの高さを固定（例: 40px）

        self.middle_splitter = QSplitter(Qt.Vertical)
        self.middle_splitter.addWidget(self.thumbnail_panel)

        self.right_splitter = QSplitter(Qt.Vertical)
        self.right_splitter.addWidget(self.preview_panel)
        self.right_splitter.addWidget(self.map_panel)
        self.right_splitter.setSizes([5000, 5000])  # プレビューと地図ビューを半分ずつに初期化

        self.main_splitter = QSplitter()
        self.main_splitter.addWidget(self.folder_panel)
        self.main_splitter.addWidget(self.middle_splitter)
        self.main_splitter.addWidget(self.right_splitter)
        self.main_splitter.setSizes([300, 200, 900])

        layout = QVBoxLayout()
        layout.addWidget(controls_widget)
        layout.addWidget(self.main_splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStatusBar(QStatusBar())

        self.set_thumbnail_size_and_width('medium')

    def set_thumbnail_size_and_width(self, size_label):
        size_map = {
            'small': (QSize(64, 64), 64 + 60),
            'medium': (QSize(128, 128), 128 + 60),
            'large': (QSize(192, 192), 192 + 60)
        }
        size, width = size_map.get(size_label, (QSize(128, 128), 188))
        self.thumbnail_panel.set_icon_size(size)
        self.main_splitter.setSizes([300, width, 900])

    def on_folder_selected(self, index):
        path = self.folder_panel.get_path(index)
        if os.path.isdir(path):
            self.image_paths = find_images_in_directory(path)
            self.thumbnail_panel.update_list(self.image_paths)
            if self.image_paths:
                self.show_image_and_map(self.image_paths[0])
        elif os.path.isfile(path):
            dir_path = os.path.dirname(path)
            self.image_paths = find_images_in_directory(dir_path)
            self.thumbnail_panel.update_list(self.image_paths)
            if path in self.image_paths:
                self.show_image_and_map(path)

    def on_thumbnail_clicked(self, image_path):
        self.show_image_and_map(image_path)

    def show_image_and_map(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.preview_panel.set_image(pixmap)

        gps_info = extract_gps_coords(image_path)
        if gps_info:
            lat, lon = gps_info["latitude"], gps_info["longitude"]
        else:
            lat, lon = 0.0, 0.0

        map_file = generate_map_html(lat, lon)
        self.map_panel.load_map(map_file)

    def on_address_entered(self):
        folder_path = self.address_bar.text()
        if folder_path:
            self.folder_panel.set_root(folder_path)
            self.image_paths = find_images_in_directory(folder_path)
            self.thumbnail_panel.update_list(self.image_paths)

    def on_return_to_root(self):
        self.folder_panel.set_root("")
        self.statusBar().showMessage("全ドライブに戻りました", 3000)