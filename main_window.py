from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar, QListWidgetItem, QHBoxLayout, QRadioButton, QButtonGroup, QLabel
from ui.image_preview import ImagePreviewView
from ui.folder_browser import create_folder_view
from ui.thumbnail_list import create_thumbnail_list, set_thumbnail_size
from ui.map_view import create_map_view
from ui.controls import create_controls
from logic import find_images_in_directory, load_pixmap, extract_gps_coords, generate_map_html
from PyQt5.QtCore import Qt, QUrl, QSize
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
        self.preview_view = ImagePreviewView()
        self.preview_view.setMinimumHeight(200)

        self.folder_view = create_folder_view(self.on_folder_selected)
        self.folder_view.setTextElideMode(Qt.ElideNone)
        self.folder_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.folder_view.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.folder_view.header().setSectionResizeMode(2, QHeaderView.Interactive)
        self.folder_view.setColumnWidth(0, 300)
        self.folder_view.setColumnWidth(1, 100)
        self.folder_view.setColumnWidth(2, 150)

        self.thumbnail_list = create_thumbnail_list(self.on_thumbnail_clicked)

        # ▼ サムネイルサイズ切替用ラベル＋ラジオボタン ▼
        size_radio_layout = QHBoxLayout()
        size_radio_layout.setContentsMargins(10, 5, 10, 5)
        size_radio_layout.setSpacing(20)

        self.size_button_group = QButtonGroup()
        self.radio_small = QRadioButton("小")
        self.radio_medium = QRadioButton("中")
        self.radio_large = QRadioButton("大")
        self.radio_medium.setChecked(True)  # デフォルト

        self.size_button_group.addButton(self.radio_small)
        self.size_button_group.addButton(self.radio_medium)
        self.size_button_group.addButton(self.radio_large)

        size_radio_layout.addWidget(self.radio_small)
        size_radio_layout.addWidget(self.radio_medium)
        size_radio_layout.addWidget(self.radio_large)

        # ラベルを追加
        size_label = QLabel("サムネイルサイズの変更")
        size_label.setContentsMargins(0, 0, 0, 0)

        size_radio_widget = QWidget()
        size_radio_vlayout = QVBoxLayout(size_radio_widget)
        size_radio_vlayout.setContentsMargins(0, 0, 0, 0)
        size_radio_vlayout.setSpacing(5)
        size_radio_vlayout.addWidget(size_label)
        size_radio_vlayout.addLayout(size_radio_layout)
        size_radio_widget.setFixedHeight(60)

        # middle_splitterをインスタンス変数に
        self.middle_splitter = QSplitter()
        self.middle_splitter.setOrientation(Qt.Vertical)
        self.middle_splitter.addWidget(self.thumbnail_list)
        self.middle_splitter.addWidget(size_radio_widget)  # 下部にラベル＋ラジオボタンを追加

        self.map_view = create_map_view()
        self.map_view.setMinimumHeight(200)

        controls_widget, self.address_bar, self.return_to_root_button = create_controls(
            self.on_address_entered, self.on_return_to_root
        )

        controls_widget_wrapper = QWidget()
        controls_layout = QVBoxLayout(controls_widget_wrapper)
        controls_layout.addWidget(controls_widget)
        controls_layout.setContentsMargins(0, 0, 0, 0)
        controls_layout.setSpacing(0)
        controls_widget_wrapper.setFixedHeight(50)

        self.right_splitter = QSplitter()
        self.right_splitter.setOrientation(Qt.Vertical)
        self.right_splitter.addWidget(self.preview_view)
        self.right_splitter.addWidget(self.map_view)
        self.right_splitter.setStretchFactor(0, 1)
        self.right_splitter.setStretchFactor(1, 1)
        self.right_splitter.setSizes([5000, 5000])

        self.main_splitter = QSplitter()
        self.main_splitter.addWidget(self.folder_view)
        self.main_splitter.addWidget(self.middle_splitter)
        self.main_splitter.addWidget(self.right_splitter)
        self.main_splitter.setSizes([300, 200, 900])

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(controls_widget_wrapper)
        layout.addWidget(self.main_splitter)
        self.setCentralWidget(main_widget)

        self.setStatusBar(QStatusBar())

        # イベント接続（サムネイルサイズ＋中央ペイン幅調整）
        self.radio_small.toggled.connect(lambda checked: checked and self.set_thumbnail_size_and_width('small'))
        self.radio_medium.toggled.connect(lambda checked: checked and self.set_thumbnail_size_and_width('medium'))
        self.radio_large.toggled.connect(lambda checked: checked and self.set_thumbnail_size_and_width('large'))
        # ▲ サムネイルサイズ切替用ラジオボタン ▲

    def set_thumbnail_size_and_width(self, size_label):
        size_map = {
            'small': (QSize(64, 64), 64 + 60),
            'medium': (QSize(128, 128), 128 + 60),
            'large': (QSize(192, 192), 192 + 60)
        }
        size, width = size_map.get(size_label, (QSize(128, 128), 188))
        self.thumbnail_list.setIconSize(size)
        self.thumbnail_list.update()
        # 中央ペイン（サムネイルリスト＋ラジオボタン）の幅を1列分に調整
        # 左: 300, 中央: width, 右: 900
        self.main_splitter.setSizes([300, width, 900])

    def on_folder_selected(self, index):
        file_path = self.folder_view.model().filePath(index)

        if os.path.isdir(file_path):
            self.image_paths = find_images_in_directory(file_path)
            self.update_thumbnail_list()

            if self.image_paths:
                first_item = self.thumbnail_list.item(0)
                self.thumbnail_list.setCurrentItem(first_item)
                self.show_image_and_map(self.image_paths[0])

        elif os.path.isfile(file_path):
            dir_path = os.path.dirname(file_path)
            self.image_paths = find_images_in_directory(dir_path)
            self.update_thumbnail_list()

            if file_path in self.image_paths:
                idx = self.image_paths.index(file_path)
                item = self.thumbnail_list.item(idx)
                self.thumbnail_list.setCurrentItem(item)
                self.show_image_and_map(file_path)

    def on_thumbnail_clicked(self, item):
        index = self.thumbnail_list.row(item)
        image_path = self.image_paths[index]
        self.show_image_and_map(image_path)

    def show_image_and_map(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.preview_view.set_image(pixmap)

        gps_info = extract_gps_coords(image_path)
        if gps_info:
            lat, lon = gps_info["latitude"], gps_info["longitude"]
        else:
            lat, lon = 0.0, 0.0

        map_file = generate_map_html(lat, lon)
        self.map_view.load(QUrl.fromLocalFile(map_file))

    def on_address_entered(self):
        folder_path = self.address_bar.text()
        if folder_path:
            self.folder_view.setRootIndex(self.folder_view.model().index(folder_path))
            self.image_paths = find_images_in_directory(folder_path)
            self.update_thumbnail_list()

    def on_return_to_root(self):
        self.folder_view.setRootIndex(self.folder_view.model().index(""))
        self.statusBar().showMessage("全ドライブに戻りました", 3000)

    def update_thumbnail_list(self):
        self.thumbnail_list.clear()
        for image_path in self.image_paths:
            icon = QIcon(load_pixmap(image_path))
            item = QListWidgetItem(icon, os.path.basename(image_path))