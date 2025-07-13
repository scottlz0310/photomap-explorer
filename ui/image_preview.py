from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QTimer
from utils.debug_logger import debug, info, warning, error, verbose

class ImagePreviewView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = QGraphicsPixmapItem()
        self.scene().addItem(self._pixmap_item)

        self._zoom_factor = 1.0
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        # 親ウィジェットが設定されている場合は明示的に親を設定
        if parent is not None:
            self.setParent(parent)

    def set_image(self, image_source):
        """画像を設定し、表示領域にフィットさせる"""
        try:
            # 画像ソースの型を判定
            if isinstance(image_source, str):
                # パスが渡された場合
                pixmap = QPixmap(image_source)
                if pixmap.isNull():
                    error("画像読み込み失敗: {image_source}")
                    return
            elif isinstance(image_source, QPixmap):
                # QPixmapが渡された場合
                pixmap = image_source
            else:
                error("不正な画像ソース型: {type(image_source)}")
                return
            
            self._zoom_factor = 1.0
            self.resetTransform()
            self._pixmap_item.setPixmap(pixmap)
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)  # type: ignore
            info("画像設定成功: {image_source}")
            
        except Exception as e:
            error("画像設定エラー: {e}")
    
    def set_image_from_path(self, image_path: str):
        """パスから画像を読み込み（互換性用）"""
        self.set_image(image_path)

    def wheelEvent(self, event):
        """マウスホイールでズームイン・ズームアウト"""
        if not self._pixmap_item.pixmap().isNull():
            zoom_in = event.angleDelta().y() > 0  # type: ignore
            factor = 1.25 if zoom_in else 0.8
            self._zoom_factor *= factor
            self.scale(factor, factor)

    def resizeEvent(self, event):
        """ウィンドウリサイズ時に自動フィット"""
        super().resizeEvent(event)
        
        # 画像が設定されている場合のみフィット実行
        if hasattr(self, '_pixmap_item') and self._pixmap_item and not self._pixmap_item.pixmap().isNull():
            try:
                # 少し遅延してからフィット実行（レイアウト計算完了を待つ）
                QTimer.singleShot(50, self._auto_fit_on_resize)
            except Exception as e:
                warning("リサイズイベントエラー: {e}")
    
    def _auto_fit_on_resize(self):
        """リサイズ後の自動フィット処理"""
        try:
            if hasattr(self, '_pixmap_item') and self._pixmap_item and not self._pixmap_item.pixmap().isNull():
                # ズームファクターを1.0にリセットしてフィット
                self._zoom_factor = 1.0
                self.resetTransform()
                self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)  # type: ignore
                info("リサイズ時自動フィット実行")
        except Exception as e:
            warning("リサイズ時自動フィットエラー: {e}")


def create_image_preview(parent=None):
    """画像プレビューウィジェットを作成して返す関数"""
    return ImagePreviewView(parent)
