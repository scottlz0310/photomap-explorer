from PyQt5.QtWidgets import QTreeView, QHeaderView, QFileSystemModel
from PyQt5.QtCore import Qt, QDir

class FolderPanel(QTreeView):
    def __init__(self, on_folder_selected):
        super().__init__()
        model = QFileSystemModel()
        model.setRootPath("")
        self.setModel(model)
        # 起動時は全ドライブ（QDir.rootPath()）をルートに
        self.setRootIndex(model.index(QDir.rootPath()))
        self.setTextElideMode(Qt.ElideNone)
        self.header().setSectionResizeMode(0, QHeaderView.Interactive)
        self.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.header().setSectionResizeMode(2, QHeaderView.Interactive)
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 150)
        self.clicked.connect(on_folder_selected)
        self.setColumnHidden(1, True)
        self.setColumnHidden(2, True)
        self.setColumnHidden(3, True)
        # --- ここからリスト風設定 ---
        self.setRootIsDecorated(False)  # ツリー線・展開アイコン非表示
        self.setItemsExpandable(False)  # 展開禁止
        self.setHeaderHidden(False)     # ヘッダーは表示（お好みでTrueも可）

    def get_path(self, index):
        return self.model().filePath(index)
    
    def set_root(self, path):
        index = self.model().index(path)
        self.setRootIndex(index)
        # 1階層リスト風なので、setRootIndexで直下のみ表示
    
    def select_file(self, file_path, center=False):
        model = self.model()
        self.sortByColumn(0, Qt.AscendingOrder)
        index = model.index(file_path)
        if index.isValid():
            self.setCurrentIndex(index)