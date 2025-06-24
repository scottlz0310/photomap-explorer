from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar
from ui.image_preview import ImagePreviewView
from ui.folder_browser import create_folder_view
from ui.thumbnail_list import create_thumbnail_list
from ui.map_view import create_map_view
from ui.controls import create_controls
from logic import find_images_in_directory
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QIcon


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
        self.folder_view.setTextElideMode(Qt.ElideNone)  # フォルダ名の省略を防ぐ設定を追加
        self.folder_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.folder_view.header().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.folder_view.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.folder_view.header().setSectionResizeMode(2, QHeaderView.Interactive)
        self.folder_view.setColumnWidth(0, 300)
        self.folder_view.setColumnWidth(1, 100)
        self.folder_view.setColumnWidth(2, 150)
        self.thumbnail_list = create_thumbnail_list(self.on_thumbnail_clicked)
        self.map_view = create_map_view()
        controls_widget, self.address_bar, self.return_to_root_button = create_controls(self.on_address_entered, self.on_return_to_root)

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
        layout.addWidget(controls_widget)  # ここをaddress_barではなくcontrols_widgetにする
        layout.addWidget(top_splitter)
        self.setCentralWidget(main_widget)

        self.setStatusBar(QStatusBar())

    def on_folder_selected(self, index):
        dir_path = self.folder_view.model().filePath(index)
        if dir_path:
            self.image_paths = find_images_in_directory (dir_path)
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
            self.image_paths = find_images_in_directory (folder_path)
            self.update_thumbnail_list()

    def on_return_to_root(self):
        self.folder_view.setRootIndex(self.folder_view.model().index(""))
        self.statusBar().showMessage("全ドライブに戻りました", 3000)

    def update_thumbnail_list(self):
        self.thumbnail_list.clear()  # リストを初期化
        for image_path in self.image_paths:
            icon = QIcon(load_pixmap(image_path))  # アイコンを作成
            item = QListWidgetItem(icon, os.path.basename(image_path))  # リストアイテムを作成
            self.thumbnail_list.addItem(item)  # アイテムを追加