from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar
from ui.image_preview import ImagePreviewView
from ui.folder_browser import create_folder_view
from ui.thumbnail_list import create_thumbnail_list
from ui.map_view import create_map_view
from ui.controls import create_controls
from logic.image_loader import load_images_from_directory

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
        # UIコンポーネントを各モジュールからインポートして初期化
        self.preview_view = ImagePreviewView()
        self.folder_view = create_folder_view(self.on_folder_selected)
        self.thumbnail_list = create_thumbnail_list(self.on_thumbnail_clicked)
        self.map_view = create_map_view()
        self.address_bar, self.return_to_root_button = create_controls(self.on_address_entered, self.on_return_to_root)

        # レイアウトの組み立て
        right_splitter = QSplitter()
        right_splitter.addWidget(self.preview_view)
        right_splitter.addWidget(self.map_view)

        top_splitter = QSplitter()
        top_splitter.addWidget(self.folder_view)
        top_splitter.addWidget(self.thumbnail_list)
        top_splitter.addWidget(right_splitter)

        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.addWidget(self.address_bar)
        layout.addWidget(top_splitter)
        self.setCentralWidget(main_widget)

        self.setStatusBar(QStatusBar())

    def on_folder_selected(self, index):
        dir_path = self.folder_view.model().filePath(index)
        if dir_path:
            self.image_paths = load_images_from_directory(dir_path)
            self.update_thumbnail_list()

    def on_thumbnail_clicked(self, item):
        index = self.thumbnail_list.row(item)
        if 0 <= index < len(self.image_paths):
            self.current_index = index
            self.preview_view.set_image(self.image_paths[index])

    def on_address_entered(self):
        folder_path = self.address_bar.text()
        if folder_path:
            self.folder_view.setRootIndex(self.folder_view.model().index(folder_path))
            self.image_paths = load_images_from_directory(folder_path)
            self.update_thumbnail_list()

    def on_return_to_root(self):
        self.folder_view.setRootIndex(self.folder_view.model().index(""))
        self.statusBar().showMessage("全ドライブに戻りました", 3000)

    def update_thumbnail_list(self):
        self.thumbnail_list.clear()
        for image_path in self.image_paths:
            self.thumbnail_list.add_thumbnail(image_path)
