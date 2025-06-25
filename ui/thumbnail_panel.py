from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QRadioButton, QButtonGroup
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from ui.thumbnail_list import load_pixmap
import os

class ThumbnailPanel(QWidget):
    def __init__(self, on_thumbnail_clicked, on_size_changed):
        super().__init__()
        self.on_thumbnail_clicked = on_thumbnail_clicked
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._item_clicked)

        radio_layout = QHBoxLayout()
        self.button_group = QButtonGroup()

        for label, size in [("小", "small"), ("中", "medium"), ("大", "large")]:
            btn = QRadioButton(label)
            self.button_group.addButton(btn)
            radio_layout.addWidget(btn)
            btn.toggled.connect(lambda checked, s=size: checked and on_size_changed(s))

        radio_label = QLabel("サムネイルサイズの変更")
        radio_wrapper = QWidget()
        radio_vlayout = QVBoxLayout(radio_wrapper)
        radio_vlayout.addWidget(radio_label)
        radio_vlayout.addLayout(radio_layout)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addWidget(radio_wrapper)

    def update_list(self, image_paths):
        self.list_widget.clear()
        for path in image_paths:
            icon = QIcon(load_pixmap(path))
            item = QListWidgetItem(icon, os.path.basename(path))
            item.setData(Qt.UserRole, path)  # 絶対パスを保持
            self.list_widget.addItem(item)

    def _item_clicked(self, item):
        image_path = item.data(Qt.UserRole)  # 絶対パスを取得
        self.on_thumbnail_clicked(image_path)

    def set_icon_size(self, size):
        self.list_widget.setIconSize(size)
