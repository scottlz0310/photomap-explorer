from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTreeView, QHeaderView, QFileSystemModel, QAbstractItemView
from PyQt5.QtCore import Qt, QDir, pyqtSignal, QModelIndex

class FolderPanel(QWidget):
    folder_changed = pyqtSignal(str)  # フォルダ移動時にパスを通知

    def __init__(self, on_folder_selected):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.back_button = QPushButton('⬆ 親ディレクトリ/全ドライブへ戻る')
        self.back_button.setFixedHeight(32)
        self.back_button.clicked.connect(self.go_back)
        layout.addWidget(self.back_button)

        self.tree = QTreeView()
        model = QFileSystemModel()
        model.setRootPath("")
        self.tree.setModel(model)
        self._current_path = QDir.rootPath()
        self.tree.setRootIndex(model.index(self._current_path))
        self.tree.setTextElideMode(Qt.ElideNone)
        self.tree.header().setSectionResizeMode(0, QHeaderView.Interactive)
        self.tree.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.tree.header().setSectionResizeMode(2, QHeaderView.Interactive)
        self.tree.setColumnWidth(0, 200)
        self.tree.setColumnWidth(1, 100)
        self.tree.setColumnWidth(2, 150)
        self.tree.clicked.connect(self._on_clicked)
        self.tree.setColumnHidden(1, True)
        self.tree.setColumnHidden(2, True)
        self.tree.setColumnHidden(3, True)
        self.tree.setRootIsDecorated(False)
        self.tree.setItemsExpandable(False)
        self.tree.setHeaderHidden(False)
        self.tree.doubleClicked.connect(self._on_double_clicked)
        self.tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.tree)

    def _on_clicked(self, index):
        path = self.tree.model().filePath(index)
        if self.tree.model().isDir(index):
            self.folder_changed.emit(path)

    def _on_double_clicked(self, index):
        path = self.tree.model().filePath(index)
        if self.tree.model().isDir(index):
            self.set_root(path)
            self.folder_changed.emit(path)
        else:
            # ファイルの場合もemit（プレビュー・地図表示用）
            self.folder_changed.emit(path)

    def go_back(self):
        import os
        # 現在が全ドライブ表示なら何もしない
        if not self._current_path or self._current_path == "":
            return
        # Windows: ドライブ直下なら全ドライブへ
        if os.name == 'nt':
            drive, rest = os.path.splitdrive(self._current_path)
            if drive and rest in ('\\', '/', ''):
                self.set_root("")
                self.folder_changed.emit("")
                return
        # ルートや空パスも全ドライブ
        if not self._current_path or self._current_path in (QDir.rootPath(), "/", "C:/"):
            self.set_root("")
            self.folder_changed.emit("")
            return
        # それ以外は親ディレクトリへ
        parent = QDir(self._current_path)
        if parent.cdUp():
            new_path = parent.absolutePath()
            self.set_root(new_path)
            self.folder_changed.emit(new_path)

    def set_root(self, path):
        # 空文字列なら全ドライブ
        if not path:
            self._current_path = ""
            index = self.tree.model().index("")
        else:
            self._current_path = path
            index = self.tree.model().index(path)
        self.tree.setRootIndex(index)

    def get_path(self, index):
        return self.tree.model().filePath(index)

    def select_file(self, file_path, center=False):
        model = self.tree.model()
        self.tree.sortByColumn(0, Qt.AscendingOrder)
        index = model.index(file_path)
        if index.isValid():
            self.tree.setCurrentIndex(index)