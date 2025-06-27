# PhotoMap Explorer Main Window
# 既存の main_window.py を window ディレクトリに移動

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar, QHBoxLayout, QPushButton, QStackedLayout
from ui.folder_panel import FolderPanel
from ui.thumbnail_panel import ThumbnailPanel
from ui.preview_panel import PreviewPanel
from ui.map_panel import MapPanel
from ui.controls import create_controls, create_address_bar_widget
from logic.image_utils import find_images_in_directory, load_pixmap, extract_gps_coords, generate_map_html, extract_image_info
from PyQt5.QtCore import Qt, QUrl, QSize, QDir
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem
import os

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # Set window title and icon
        self.setWindowTitle("PhotoMap Explorer")
        self.setWindowIcon(QIcon(":/icons/icon.png"))

        # Initialize central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Create splitter for resizable panels
        self.splitter = QSplitter(Qt.Horizontal, self.central_widget)
        self.layout.addWidget(self.splitter)

        # Initialize folder, thumbnail, preview, and map panels
        self.folder_panel = FolderPanel(self.splitter)
        self.thumbnail_panel = ThumbnailPanel(self.splitter)
        self.preview_panel = PreviewPanel(self.splitter)
        self.map_panel = MapPanel(self.splitter)

        # Set minimum sizes for panels
        self.folder_panel.setMinimumWidth(200)
        self.thumbnail_panel.setMinimumWidth(200)
        self.preview_panel.setMinimumWidth(200)
        self.map_panel.setMinimumWidth(200)

        # Create status bar
        self.status_bar = QStatusBar(self)
        self.setStatusBar(self.status_bar)

        # Create and set controls and address bar widget
        self.controls_widget = create_controls(self)
        self.address_bar_widget = create_address_bar_widget(self)
        self.layout.setMenuBar(self.controls_widget)
        self.layout.addWidget(self.address_bar_widget)

        # Connect signals and slots
        self.folder_panel.directory_changed.connect(self.on_directory_changed)
        self.thumbnail_panel.image_selected.connect(self.on_image_selected)
        self.preview_panel.image_changed.connect(self.on_preview_image_changed)
        self.map_panel.location_changed.connect(self.on_map_location_changed)

        # Set initial directory
        self.initial_directory = QDir.homePath()
        self.folder_panel.set_directory(self.initial_directory)

    def on_directory_changed(self, directory):
        # Update status bar and load images from the new directory
        self.status_bar.showMessage(f"Directory changed: {directory}")
        self.thumbnail_panel.clear()
        self.preview_panel.clear()
        self.map_panel.clear()
        self.load_images(directory)

    def on_image_selected(self, image_path):
        # Update preview and map panels when an image is selected
        self.preview_panel.set_image(image_path)
        self.map_panel.set_image(image_path)

    def on_preview_image_changed(self, image_path):
        # Update map panel when preview image changes
        self.map_panel.set_image(image_path)

    def on_map_location_changed(self, location):
        # Update status bar when map location changes
        self.status_bar.showMessage(f"Map location changed: {location}")

    def load_images(self, directory):
        # Find and load images from the specified directory
        image_files = find_images_in_directory(directory)
        for image_file in image_files:
            self.thumbnail_panel.add_image(image_file)
