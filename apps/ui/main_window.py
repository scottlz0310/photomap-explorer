# apps/ui/main_window.py
import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QFileSystemModel, QTreeView,
    QListWidget, QListWidgetItem, QLabel, QPushButton, QSplitter, QFrame,
    QStatusBar, QHeaderView
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView

from apps.logic.image_loader import find_images_in_directory, load_pixmap  # ← これも忘れず！

# ...（中略）...

def load_images_from_directory(self, directory):
    """
    指定フォルダ内の画像ファイルを読み込み、サムネイル一覧に展開して初期画像をプレビュー表示
    """
    self.image_paths = find_images_in_directory(directory)  # image_loader から取得
    self.thumbnail_list.clear()

    for path in self.image_paths:
        icon = QIcon(load_pixmap(path))  # image_loader でサムネイル生成
        item = QListWidgetItem(icon, os.path.basename(path))
        self.thumbnail_list.addItem(item)

    # 最初の画像を自動でプレビュー表示（あれば）
    if self.image_paths:
        self.current_index = 0
        self.display_image_by_index(self.current_index)
