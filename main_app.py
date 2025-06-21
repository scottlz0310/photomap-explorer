import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileSystemModel, QTreeView, QListWidget, QLabel, QPushButton,
    QTextBrowser, QSplitter, QFrame, QStatusBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.setup_ui()

    def setup_ui(self):
        # === Left: Folder Tree ===
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath('')
        self.folder_view = QTreeView()
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setRootIndex(self.folder_model.index(''))
        self.folder_view.setHeaderHidden(True)
        self.folder_view.setMinimumWidth(200)

        # === Center: Thumbnail List ===
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setMinimumWidth(300)

        # === Right: Preview + Map View (Vertical Splitter) ===
        self.preview_label = QLabel("🖼 Preview")
        self.preview_label.setFrameStyle(QFrame.Box)
        self.preview_label.setAlignment(Qt.AlignCenter)

        # ◀▶ Navigation Buttons
        prev_button = QPushButton("◀")
        next_button = QPushButton("▶")
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(next_button)

        preview_layout = QVBoxLayout()
        preview_layout.addWidget(self.preview_label, stretch=9)
        preview_layout.addLayout(nav_layout, stretch=1)

        preview_container = QWidget()
        preview_container.setLayout(preview_layout)

        self.map_view = QWebEngineView()
        self.map_view.setHtml("<h3>🌍 Map View (Leaflet Placeholder)</h3>")

        right_splitter = QSplitter(Qt.Vertical)
        right_splitter.addWidget(preview_container)
        right_splitter.addWidget(self.map_view)
        right_splitter.setSizes([600, 300])

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_layout.addWidget(right_splitter)
        right_widget.setLayout(right_layout)

        # === Top Splitter (Folder | Thumbnails | Right Panel) ===
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.addWidget(self.folder_view)
        top_splitter.addWidget(self.thumbnail_list)
        top_splitter.addWidget(right_widget)
        top_splitter.setSizes([250, 400, 750])

        # === Main Splitter (Top Panel + StatusBar Placeholder) ===
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_splitter)

        # === Status Bar ===
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("📸 Ready")

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
