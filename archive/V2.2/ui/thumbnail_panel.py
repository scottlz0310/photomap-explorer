from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QRadioButton, QButtonGroup
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from ui.thumbnail_list import load_pixmap
import os
from utils.debug_logger import debug, info, warning, error, verbose

class ThumbnailPanel(QWidget):
    def __init__(self, on_thumbnail_clicked, on_size_changed):
        super().__init__()
        self.on_thumbnail_clicked = on_thumbnail_clicked
        self._updating = False  # リスト更新中フラグ
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self._item_clicked)
        # 複数列表示のための設定
        self.list_widget.setViewMode(QListWidget.IconMode)
        self.list_widget.setResizeMode(QListWidget.Adjust)
        self.list_widget.setMovement(QListWidget.Static)
        self.list_widget.setFlow(QListWidget.LeftToRight)
        self.list_widget.setSpacing(8)

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
        self._updating = True
        self.list_widget.clear()
        for path in image_paths:
            icon = QIcon(load_pixmap(path))
            item = QListWidgetItem(icon, "")  # ファイル名非表示
            item.setData(Qt.UserRole, path)  # 絶対パスを保持
            self.list_widget.addItem(item)
        self._updating = False

    def _item_clicked(self, item):
        if self._updating:
            return  # 更新中は無視
        image_path = item.data(Qt.UserRole)  # 絶対パスを取得
        self.on_thumbnail_clicked(image_path)

    def set_icon_size(self, size):
        self.list_widget.setIconSize(size)

    def select_thumbnail(self, image_path, center=False):
        if self._updating:
            return  # 更新中は無視
        norm_image_path = os.path.normcase(os.path.normpath(image_path))
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            item_path = os.path.normcase(os.path.normpath(item.data(Qt.UserRole)))
            if item_path == norm_image_path:
                self.list_widget.setCurrentItem(item)
                self.list_widget.setFocus()
                if center:
                    self.list_widget.scrollToItem(item, QListWidget.PositionAtCenter)
                break
