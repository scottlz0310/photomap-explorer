from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize

class ThumbnailListWidget(QListWidget):
    """サムネイル一覧表示用のウィジェットクラス（レガシーUI互換）"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIconSize(QSize(128, 128))
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setSpacing(10)
    
    def add_thumbnail(self, image_path):
        """サムネイルを追加"""
        try:
            icon = QIcon(image_path)
            filename = image_path.split("/")[-1].split("\\")[-1]  # Windows/Linux両対応
            item = QListWidgetItem(icon, filename)
            self.addItem(item)
            return True
        except Exception as e:
            print(f"サムネイル追加エラー: {e}")
            return False
    
    def set_thumbnail_size(self, size_label):
        """サムネイルサイズを設定"""
        size_map = {
            'small': QSize(64, 64),
            'medium': QSize(128, 128),
            'large': QSize(192, 192)
        }
        size = size_map.get(size_label, QSize(128, 128))
        self.setIconSize(size)
        self.update()
    
    def clear_thumbnails(self):
        """全てのサムネイルをクリア"""
        self.clear()


# 既存の関数は互換性のために残す
def load_pixmap(image_path):
    """画像パスからQPixmapを生成して返すユーティリティ関数"""
    return QPixmap(image_path)

def create_thumbnail_list(thumbnail_clicked_callback):
    """サムネイル一覧のウィジェットを作成して初期化する関数"""
    thumbnail_list = ThumbnailListWidget()
    thumbnail_list.itemClicked.connect(thumbnail_clicked_callback)
    return thumbnail_list
