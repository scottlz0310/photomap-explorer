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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer")
        self.setGeometry(100, 100, 1400, 900)
        self.image_paths = []
        self.is_fullscreen = False  # ウィンドウ全体の全画面状態フラグ
        self.is_preview_fullscreen = False  # プレビューのみ全画面状態フラグ
        self._original_central_widget = None  # 元の中央ウィジェット保持用

        self.folder_panel = FolderPanel(None)
        self.folder_panel.folder_changed.connect(self.on_folder_selected)
        self.thumbnail_panel = ThumbnailPanel(self.on_thumbnail_clicked, self.set_thumbnail_size_and_width)
        self.preview_panel = PreviewPanel()
        self.map_panel = MapPanel()

        # --- 新アドレスバーウィジェットを使用 ---
        self.current_path = QDir.rootPath()  # 初期パスをルートに
        self.address_bar_widget, self.address_bar_edit = create_address_bar_widget(
            self.current_path, self.on_address_part_double_clicked, self.on_address_entered
        )
        # 最大化ボタン（画像/地図）
        self.maximize_image_btn = QPushButton("画像最大化")
        self.maximize_image_btn.setFixedWidth(90)
        self.maximize_image_btn.clicked.connect(self.toggle_image_maximize)
        self.maximize_map_btn = QPushButton("地図最大化")
        self.maximize_map_btn.setFixedWidth(90)
        self.maximize_map_btn.clicked.connect(self.toggle_map_maximize)
        self.restore_btn = QPushButton("元に戻す")
        self.restore_btn.setFixedWidth(90)
        self.restore_btn.setFixedHeight(30)  # 高さを30pxに固定
        self.restore_btn.clicked.connect(self.restore_normal_view)
        self.restore_btn.hide()

        self.controls_widget = QWidget()
        controls_layout = QHBoxLayout(self.controls_widget)
        controls_layout.setContentsMargins(5, 5, 5, 5)
        controls_layout.setSpacing(5)
        controls_layout.addWidget(self.address_bar_widget)
        controls_layout.addWidget(self.maximize_image_btn)
        controls_layout.addWidget(self.maximize_map_btn)
        controls_layout.addWidget(self.restore_btn)
        self.controls_widget.setFixedHeight(40)
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

        self._maximize_container = QWidget()  # 最大化用一時コンテナ
        self._maximize_stack = QStackedLayout(self._maximize_container)
        self._maximize_panel = QWidget()
        self._maximize_panel_layout = QVBoxLayout(self._maximize_panel)
        self._maximize_panel_layout.setContentsMargins(0, 0, 0, 0)
        self._maximize_panel_layout.setSpacing(0)
        # 右上に元に戻すボタンを重ねる
        self._maximize_topbar = QWidget()
        self._maximize_topbar.setFixedHeight(30)  # トップバー全体の高さを30pxに固定
        self._maximize_topbar_layout = QHBoxLayout(self._maximize_topbar)
        self._maximize_topbar_layout.setContentsMargins(0, 0, 0, 0)
        self._maximize_topbar_layout.addStretch()
        self._maximize_topbar_layout.addWidget(self.restore_btn)
        self._maximize_panel_layout.addWidget(self._maximize_topbar)
        # self._maximize_panel_layout.addStretch()  # 余白をなくすため削除
        self._maximize_stack.addWidget(self._maximize_panel)
        self._maximize_container.hide()

        layout = QVBoxLayout()
        layout.addWidget(self.controls_widget)
        layout.addWidget(self.main_splitter)
        layout.addWidget(self._maximize_container)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setStatusBar(QStatusBar())

        self.set_thumbnail_size_and_width('medium')
        self._panel_maximized = None  # 'image' or 'map' or None
        self._preview_panel_index_in_splitter = 0
        self._map_panel_index_in_splitter = 1

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
        # GimpStyleAddressBarの場合はset_path()メソッドを使用
        if hasattr(self.address_bar_edit, 'set_path'):
            self.address_bar_edit.set_path(path)
            self.current_path = path
        else:
            # レガシーアドレスバーの場合は従来通り再生成
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
        # GimpStyleAddressBarから現在のパスを取得
        if hasattr(self.address_bar_edit, 'current_path'):
            folder_path = self.address_bar_edit.current_path
        elif hasattr(self.address_bar_edit, 'text'):
            folder_path = self.address_bar_edit.text()
        else:
            folder_path = None
            
        if folder_path:
            self.update_address_bar(folder_path)
            self.folder_panel.set_root(folder_path)
            self.image_paths = find_images_in_directory(folder_path)
            self.thumbnail_panel.update_list(self.image_paths)

    def on_folder_selected(self, path):
        import os
        if os.path.isdir(path):
            self.update_address_bar(path)
            self.image_paths = find_images_in_directory(path)
            self.thumbnail_panel.update_list(self.image_paths)
        elif os.path.isfile(path):
            dir_path = os.path.dirname(path)
            self.update_address_bar(dir_path)
            self.image_paths = find_images_in_directory(dir_path)
            self.thumbnail_panel.update_list(self.image_paths)
            # サムネイルリスト内で該当画像を選択し、プレビュー・地図も更新
            norm_path = os.path.normcase(os.path.normpath(path))
            norm_image_paths = [os.path.normcase(os.path.normpath(p)) for p in self.image_paths]
            if norm_path in norm_image_paths:
                self.thumbnail_panel.select_thumbnail(path, center=True)
                self.show_image_and_map(path)
            else:
                # サムネイルリストに画像がない場合も、プレビュー・地図だけは更新
                self.show_image_and_map(path)

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

        # 画像情報を取得しステータスバーに表示
        info = extract_image_info(image_path)
        status = f"解像度: {info['width']}x{info['height']}  "
        status += f"撮影日時: {info['datetime']}  " if info['datetime'] else ""
        status += f"カメラ: {info['camera']}  " if info['camera'] else ""
        status += f"シャッタースピード: {info['shutter']}" if info['shutter'] else ""
        self.statusBar().showMessage(status, 10000)

    def mouseDoubleClickEvent(self, event):
        self.toggle_image_maximize()
        super().mouseDoubleClickEvent(event)

    def toggle_image_maximize(self):
        if self._panel_maximized == 'image':
            self.restore_normal_view()
            return
        idx = self.right_splitter.indexOf(self.preview_panel)
        if idx != -1:
            self._preview_panel_index_in_splitter = idx
            self.right_splitter.widget(idx).setParent(None)
        # 最大化パネルの中央にpreview_panelを追加
        for i in reversed(range(self._maximize_panel_layout.count())):
            item = self._maximize_panel_layout.itemAt(i)
            widget = item.widget()
            if widget and widget not in [self._maximize_topbar]:
                self._maximize_panel_layout.removeWidget(widget)
                widget.setParent(None)
        self._maximize_panel_layout.addWidget(self.preview_panel)
        self.controls_widget.hide()
        self.main_splitter.hide()
        self._maximize_container.show()
        self.maximize_image_btn.hide()
        self.maximize_map_btn.hide()
        self.restore_btn.show()
        self._panel_maximized = 'image'
        # 画像拡大: 現在選択中の画像を再表示
        if self.image_paths:
            # サムネイルパネルで選択中の画像があればそれを、なければ先頭
            selected = getattr(self.thumbnail_panel, 'current_image_path', None)
            image_path = selected if selected else self.image_paths[0]
            self.show_image_and_map(image_path)

    def toggle_map_maximize(self):
        if self._panel_maximized == 'map':
            self.restore_normal_view()
            return
        idx = self.right_splitter.indexOf(self.map_panel)
        if idx != -1:
            self._map_panel_index_in_splitter = idx
            self.right_splitter.widget(idx).setParent(None)
        # 最大化パネルの中央にmap_panelを追加
        for i in reversed(range(self._maximize_panel_layout.count())):
            item = self._maximize_panel_layout.itemAt(i)
            widget = item.widget()
            if widget and widget not in [self._maximize_topbar]:
                self._maximize_panel_layout.removeWidget(widget)
                widget.setParent(None)
        self._maximize_panel_layout.addWidget(self.map_panel)
        self.controls_widget.hide()
        self.main_splitter.hide()
        self._maximize_container.show()
        self.maximize_image_btn.hide()
        self.maximize_map_btn.hide()
        self.restore_btn.show()
        self._panel_maximized = 'map'

    def restore_normal_view(self):
        layout = self._maximize_panel_layout
        if self._panel_maximized == 'image':
            layout.removeWidget(self.preview_panel)
            self.right_splitter.insertWidget(self._preview_panel_index_in_splitter, self.preview_panel)
        elif self._panel_maximized == 'map':
            layout.removeWidget(self.map_panel)
            self.right_splitter.insertWidget(self._map_panel_index_in_splitter, self.map_panel)
        self.controls_widget.show()
        self.main_splitter.show()
        self._maximize_container.hide()
        self.maximize_image_btn.show()
        self.maximize_map_btn.show()
        self.restore_btn.hide()
        self._panel_maximized = None
