from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt

class ImagePreviewView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = QGraphicsPixmapItem()
        self.scene().addItem(self._pixmap_item)

        self._zoom_factor = 1.0
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def set_image(self, pixmap: QPixmap):
        """画像を設定し、表示領域にフィットさせる"""
        self._zoom_factor = 1.0
        self.resetTransform()
        self._pixmap_item.setPixmap(pixmap)
        self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)

    def display_image(self, image_path: str):
        """画像ファイルパスから画像を表示"""
        import os
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.set_image(pixmap)
                return True
        return False

    def wheelEvent(self, event):
        """マウスホイールでズームイン・ズームアウト"""
        if not self._pixmap_item.pixmap().isNull():
            zoom_in = event.angleDelta().y() > 0
            factor = 1.25 if zoom_in else 0.8
            self._zoom_factor *= factor
            self.scale(factor, factor)


def create_image_preview():
    """画像プレビューウィジェットを作成して返す関数"""
    return ImagePreviewView()
