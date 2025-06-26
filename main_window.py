from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QSplitter, QWidget, QStatusBar, QHBoxLayout
from ui.folder_panel import FolderPanel
from ui.thumbnail_panel import ThumbnailPanel
from ui.preview_panel import PreviewPanel
from ui.map_panel import MapPanel
from ui.controls import create_controls, create_address_bar_widget
from logic.image_utils import find_images_in_directory, load_pixmap, extract_gps_coords, generate_map_html
from PyQt5.QtCore import Qt, QUrl, QSize, QDir
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QListWidgetItem
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.image_paths = []

        self.folder_panel = FolderPanel(self.on_folder_selected)
        self.thumbnail_panel = ThumbnailPanel(self.on_thumbnail_clicked, self.set_thumbnail_size_and_width)
        self.preview_panel = PreviewPanel()
        self.map_panel = MapPanel()

        # --- 新アドレスバーウィジェットを使用 ---
        self.current_path = QDir.rootPath()  # 初期パスをルートに
        self.address_bar_widget, self.address_bar_edit = create_address_bar_widget(
            self.current_path, self.on_address_part_double_clicked, self.on_address_entered
        )
        self.go_to_parent_button = self.create_go_to_parent_button()
        controls_widget = QWidget()
        controls_layout = QHBoxLayout(controls_widget)
        controls_layout.setContentsMargins(5, 5, 5, 5)
        controls_layout.setSpacing(5)
        controls_layout.addWidget(self.address_bar_widget)
        controls_layout.addWidget(self.go_to_parent_button)
        controls_widget.setFixedHeight(40)
        # --- ここまで ---

        self.middle_splitter = QSplitter(Qt.Vertical)
        self.middle_splitter.addWidget(self.thumbnail_panel)

        self.right_splitter = QSplitter(Qt.Vertical)
        self.right_splitter.addWidget(self.preview_panel)
        self.right_splitter.addWidget(self.map_panel)
        self.right_splitter.setSizes([5000, 5000])

        self.main_splitter = QSplitter()
        self.main_splitter.addWidget(self.folder_panel)
        self.main_splitter.addWidget(self.middle_splitter)
        self.main_splitter.addWidget(self.right_splitter)
        self.main_splitter.setSizes([700, 200, 700])

        layout = QVBoxLayout()
        layout.addWidget(controls_widget)
        layout.addWidget(self.main_splitter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStatusBar(QStatusBar())

        self.set_thumbnail_size_and_width('medium')

    def create_go_to_parent_button(self):
        from PyQt5.QtWidgets import QPushButton, QStyle
        btn = QPushButton()
        btn.setIcon(btn.style().standardIcon(QStyle.SP_FileDialogToParent))
        btn.setToolTip("親フォルダへ移動")
        btn.setFixedSize(30, 30)
        btn.clicked.connect(self.on_go_to_parent)
        return btn

    def set_thumbnail_size_and_width(self, size_label):
        size_map = {
            'small': (QSize(64, 64), 64 + 60),
            'medium': (QSize(128, 128), 128 + 60),
            'large': (QSize(192, 192), 192 + 60)
        }
        size, width = size_map.get(size_label, (QSize(128, 128), 188))
        self.thumbnail_panel.set_icon_size(size)
        self.main_splitter.setSizes([300, width, 900])

    def update_address_bar(self, path):
        # アドレスバーウィジェットを再生成して置き換え
        parent = self.address_bar_widget.parentWidget()
        layout = parent.layout()
        layout.removeWidget(self.address_bar_widget)
        self.address_bar_widget.deleteLater()
        self.address_bar_widget, self.address_bar_edit = create_address_bar_widget(
            path, self.on_address_part_double_clicked, self.on_address_entered
        )
        layout.insertWidget(0, self.address_bar_widget)
        self.current_path = path
        self.address_bar_widget.show()

    def on_address_part_double_clicked(self, path):
        self.update_address_bar(path)
        self.folder_panel.set_root(path)
        self.image_paths = find_images_in_directory(path)
        self.thumbnail_panel.update_list(self.image_paths)
        self.statusBar().showMessage(f"移動: {path}", 3000)

    def on_address_entered(self):
        folder_path = self.address_bar_edit.text()
        if folder_path:
            self.update_address_bar(folder_path)
            self.folder_panel.set_root(folder_path)
            self.image_paths = find_images_in_directory(folder_path)
            self.thumbnail_panel.update_list(self.image_paths)

    def on_folder_selected(self, index):
        path = self.folder_panel.get_path(index)
        if os.path.isdir(path):
            self.update_address_bar(path)
            self.image_paths = find_images_in_directory(path)
            self.thumbnail_panel.update_list(self.image_paths)
            # フォルダ選択時はリスト更新のみ、選択・表示は行わない
        elif os.path.isfile(path):
            dir_path = os.path.dirname(path)
            self.update_address_bar(dir_path)
            self.image_paths = find_images_in_directory(dir_path)
            self.thumbnail_panel.update_list(self.image_paths)
            norm_path = os.path.normcase(os.path.normpath(path))
            norm_image_paths = [os.path.normcase(os.path.normpath(p)) for p in self.image_paths]
            # ファイル選択時は選択画像のみを選択・表示
            if norm_path in norm_image_paths:
                self.thumbnail_panel.select_thumbnail(path, center=True)
                self.show_image_and_map(path)
            else:
                pass

    def on_thumbnail_clicked(self, image_path):
        self.show_image_and_map(image_path)
        self.folder_panel.select_file(image_path, center=True)  # サムネイル選択時のみcenter

    def show_image_and_map(self, image_path):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.preview_panel.set_image(pixmap)

        gps_info = extract_gps_coords(image_path)
        if gps_info:
            lat, lon = gps_info["latitude"], gps_info["longitude"]
        else:
            lat, lon = 0.0, 0.0

        map_file = generate_map_html(lat, lon)
        self.map_panel.load_map(map_file)

    def on_go_to_parent(self):
        current_path = self.current_path
        import os
        # Windows: ドライブ直下（C:\ など）なら全ドライブに戻す
        if os.name == 'nt':
            drive, rest = os.path.splitdrive(current_path)
            if drive and rest in ('\\', '/',''):
                self.folder_panel.set_root("")
                self.statusBar().showMessage("全ドライブに戻りました", 3000)
                self.update_address_bar(QDir.rootPath())
                return
        # ルートや空パスも全ドライブに戻す
        if not current_path or current_path == QDir.rootPath():
            self.folder_panel.set_root("")
            self.statusBar().showMessage("全ドライブに戻りました", 3000)
            self.update_address_bar(QDir.rootPath())
            return
        parent_path = os.path.dirname(os.path.normpath(current_path.rstrip(os.sep)))
        # これ以上上がれない場合も全ドライブ
        if not parent_path or parent_path == current_path:
            self.folder_panel.set_root("")
            self.statusBar().showMessage("全ドライブに戻りました", 3000)
            self.update_address_bar(QDir.rootPath())
            return
        self.update_address_bar(parent_path)
        self.folder_panel.set_root(parent_path)
        self.image_paths = find_images_in_directory(parent_path)
        self.thumbnail_panel.update_list(self.image_paths)
        self.statusBar().showMessage(f"親フォルダへ移動: {parent_path}", 3000)