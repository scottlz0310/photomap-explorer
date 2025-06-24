from PyQt5.QtWidgets import QTreeView
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5.QtCore import Qt


def create_folder_view(folder_selected_callback):
    """フォルダビューを作成して初期化する関数"""
    folder_model = QFileSystemModel()
    folder_model.setRootPath("")  # 全ドライブを表示

    folder_view = QTreeView()
    folder_view.setModel(folder_model)
    folder_view.setRootIndex(folder_model.index(QDir.rootPath()))  # ルートパスを設定
    folder_view.setHeaderHidden(True)
    folder_view.clicked.connect(folder_selected_callback)  # フォルダ選択時のコールバックを接続
    folder_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    return folder_view
