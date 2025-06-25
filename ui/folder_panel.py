from PyQt5.QtWidgets import QTreeView, QHeaderView, QFileSystemModel
from PyQt5.QtCore import Qt, QDir

class FolderPanel(QTreeView):
    def __init__(self, on_folder_selected):
        super().__init__()
        model = QFileSystemModel()
        model.setRootPath("")
        self.setModel(model)
        self.setRootIndex(model.index(QDir.rootPath()))
        self.setTextElideMode(Qt.ElideNone)
        self.header().setSectionResizeMode(0, QHeaderView.Interactive)  # Nameカラムも手動調整可に
        self.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.header().setSectionResizeMode(2, QHeaderView.Interactive)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 150)
        self.clicked.connect(on_folder_selected)

    def get_path(self, index):
        return self.model().filePath(index)

    def set_root(self, path):
        self.setRootIndex(self.model().index(path))