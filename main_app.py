import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFileSystemModel, QTreeView, QListWidget, QLabel, QTextBrowser,
    QSplitter, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1200, 800)
        self.setup_ui()

    def setup_ui(self):
        # === Left: Folder Tree ===
        self.folder_model = QFileSystemModel()
        self.folder_model.setRootPath('')
        self.folder_view = QTreeView()
        self.folder_view.setModel(self.folder_model)
        self.folder_view.setRootIndex(self.folder_model.index(''))
        self.folder_view.setHeaderHidden(True)

        # === Center: Thumbnail Viewer ===
        self.thumbnail_list = QListWidget()
        self.thumbnail_list.setMinimumWidth(300)

        # === Right: Image Preview + EXIF Info ===
        self.image_preview = QLabel("Image Preview")
        self.image_preview.setFrameStyle(QFrame.Box)
        self.image_preview.setAlignment(Qt.AlignCenter)

        self.exif_info = QTextBrowser()
        self.exif_info.setText("Exif Info will appear here.")

        right_panel = QVBoxLayout()
        right_panel.addWidget(self.image_preview, stretch=3)
        right_panel.addWidget(self.exif_info, stretch=1)

        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        # === Horizontal splitter (Top Half) ===
        top_splitter = QSplitter(Qt.Horizontal)
        top_splitter.addWidget(self.folder_view)
        top_splitter.addWidget(self.thumbnail_list)
        top_splitter.addWidget(right_widget)

        # === Bottom: Map View ===
        self.map_view = QWebEngineView()
        self.map_view.setHtml("<h3>Map will appear here (Leaflet)</h3>")

        # === Vertical Layout ===
        main_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(top_splitter)
        main_splitter.addWidget(self.map_view)

        self.setCentralWidget(main_splitter)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
