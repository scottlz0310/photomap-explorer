from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize

def create_thumbnail_list(thumbnail_clicked_callback):
    """サムネイル一覧のウィジェットを作成して初期化する関数"""
    thumbnail_list = QListWidget()
    thumbnail_list.setIconSize(QSize(128, 128))  # サムネイルサイズを設定
    thumbnail_list.setViewMode(QListWidget.IconMode)  # アイコン表示モード
    thumbnail_list.setResizeMode(QListWidget.Adjust)
    thumbnail_list.setMovement(QListWidget.Static)
    thumbnail_list.setSpacing(10)  # アイコン間隔
    thumbnail_list.itemClicked.connect(thumbnail_clicked_callback)  # クリック時のコールバックを接続

    return thumbnail_list

def add_thumbnail(thumbnail_list, image_path):
    """サムネイルをサムネイル一覧に追加"""
    icon = QIcon(image_path)  # 画像をアイコンとして読み込み
    item = QListWidgetItem(icon, image_path.split("/")[-1])  # ファイル名を表示
    thumbnail_list.addItem(item)
