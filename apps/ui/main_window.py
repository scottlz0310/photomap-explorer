import os
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFileSystemModel, QTreeView,
    QListWidget, QListWidgetItem, QGraphicsView, QGraphicsScene,
    QGraphicsPixmapItem, QPushButton, QSplitter, QStatusBar, QHeaderView,
    QLineEdit, QFileDialog
)
from PyQt5.QtCore import Qt, QSize, QDir
from PyQt5.QtGui import QPixmap, QIcon, QPainter
from PyQt5.QtWebEngineWidgets import QWebEngineView

from apps.logic.image_loader import find_images_in_directory, load_pixmap
from apps.logic.gps_parser import extract_gps_coords
from apps.logic.map_generator import generate_map_html


class ImagePreviewView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = QGraphicsPixmapItem()
        self.scene().addItem(self._pixmap_item)
        self._zoom_factor = 1.0
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
    def set_image(self, pixmap):
        self._zoom_factor = 1.0
        self.resetTransform()
        self._pixmap_item.setPixmap(pixmap)
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        if not self._pixmap_item.pixmap().isNull():
            zoom_in = event.angleDelta().y() > 0
            factor = 1.25 if zoom_in else 0.8
            self._zoom_factor *= factor
            self.scale(factor, factor)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setWindowIcon(QIcon("assets/pme.ico"))
        self.setGeometry(100, 100, 1400, 900)

        self.image_paths = []
        self.current_index = -1

        self.setup_ui()
        self.load_images_from_directory(self.get_home_dir())

    def get_home_dir(self):
        return os.path.expanduser("~")

    def setup_ui(self):
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath("")  # 全ドライブのルートを設定

        self.folder_view = QTreeView()
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setHeaderHidden(True)
        self.folder_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.setTextElideMode(Qt.ElideNone)
        self.folder_view.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.folder_view.header().setStretchLastSection(False)
        self.folder_view.setMinimumWidth(280)
        self.folder_view.clicked.connect(self.on_folder_selected)

        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setIconSize(QSize(128, 128))
        self.thumbnail_list.setViewMode(QListWidget.IconMode)
        self.thumbnail_list.setResizeMode(QListWidget.Adjust)
        self.thumbnail_list.setMovement(QListWidget.Static)
        self.thumbnail_list.setSpacing(10)
        self.thumbnail_list.setMinimumWidth(300)
        self.thumbnail_list.itemClicked.connect(self.on_thumbnail_clicked)

        self.preview_view = ImagePreviewView()
        self.preview_view.setMinimumSize(400, 400)

        self.map_view = QWebEngineView()
        self.map_view.setHtml("<html><body><p>🗺️ 地図ビュー</p></body></html>")
        self.map_view.setMinimumSize(400, 400)

        # アドレスバーの追加
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("フォルダパスを入力してEnterを押してください")
        self.address_bar.returnPressed.connect(self.on_address_entered)

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(self.preview_view)
        right_splitter.addWidget(self.map_view)

        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.addWidget(self.folder_view)
        top_splitter.addWidget(self.thumbnail_list)
        top_splitter.addWidget(right_splitter)
        top_splitter.setSizes([300, 400, 700])

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.address_bar)  # アドレスバーをUIに追加
        layout.addWidget(top_splitter)
        self.setCentralWidget(main_widget)

        self.setStatusBar(QStatusBar())

    def on_address_entered(self):
        folder_path = self.address_bar.text()
        if os.path.isdir(folder_path):
            self.folder_view.setRootIndex(self.folder_model.index(folder_path))
            self.load_images_from_directory(folder_path)
            self.statusBar().showMessage(f"移動しました: {folder_path}", 3000)
        else:
            self.statusBar().showMessage("❌ フォルダが見つかりません", 3000)

    def on_folder_selected(self, index):
        dir_path = self.folder_model.filePath(index)
        if os.path.isdir(dir_path):
            self.load_images_from_directory(dir_path)
            self.folder_view.resizeColumnToContents(0)

    def load_images_from_directory(self, directory):
        self.image_paths = find_images_in_directory(directory)
        self.thumbnail_list.clear()
        for path in self.image_paths:
            icon = QIcon(load_pixmap(path))
            item = QListWidgetItem(icon, os.path.basename(path))
            self.thumbnail_list.addItem(item)
        if self.image_paths:
            self.current_index = 0
            self.display_image_by_index(self.current_index)

    def on_thumbnail_clicked(self, item):
        index = self.thumbnail_list.row(item)
        self.display_image_by_index(index)

    def display_image_by_index(self, index):
        if 0 <= index < len(self.image_paths):
            self.current_index = index
            pixmap = QPixmap(self.image_paths[index])
            if not pixmap.isNull():
                self.preview_view.set_image(pixmap)

                coords = extract_gps_coords(self.image_paths[index])
                html = generate_map_html(coords)
                self.map_view.setHtml(html)
            else:
                self.preview_view.scene().clear()
                self.statusBar().showMessage("❌ 画像の読み込みに失敗", 3000)

    def open_image_via_dialog(self):
        default_dir = QDir.rootPath()

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "画像ファイルを選択",
            default_dir,
            "Images (*.jpg *.jpeg *.png)"
        )

        if not file_path:
            return

        self.image_paths = [file_path]
        self.current_index = 0
        self.thumbnail_list.clear()

        icon = QIcon(load_pixmap(file_path))
        item = QListWidgetItem(icon, os.path.basename(file_path))
        self.thumbnail_list.addItem(item)

        self.display_image_by_index(0)
