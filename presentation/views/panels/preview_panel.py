"""
画像プレビューコンポーネント
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtWidgets import (QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, 
                            QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, pyqtSignal


class ImagePreviewView(QGraphicsView):
    """
    画像プレビュー表示用グラフィックスビュー
    Clean Architecture対応版
    """
    # シグナル
    image_loaded = pyqtSignal(str)  # 画像ロード時（ファイルパス）
    zoom_changed = pyqtSignal(float)  # ズーム変更時（ズーム率）
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_image_path = ""
        self._zoom_factor = 1.0
    
    def _setup_ui(self):
        """UIセットアップ"""
        # シーンとアイテムの設定
        self.setScene(QGraphicsScene(self))
        self._pixmap_item = QGraphicsPixmapItem()
        self.scene().addItem(self._pixmap_item)
        
        # ビュー設定
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        
        # デフォルト表示
        self.show_no_image_message()
    
    def set_image(self, image_path):
        """画像を設定"""
        if not os.path.exists(image_path):
            self.show_error_message("画像ファイルが見つかりません")
            return False
        
        try:
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                self.show_error_message("画像を読み込めませんでした")
                return False
            
            self._current_image_path = image_path
            self._zoom_factor = 1.0
            self.resetTransform()
            self._pixmap_item.setPixmap(pixmap)
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
            
            self.image_loaded.emit(image_path)
            return True
            
        except Exception as e:
            self.show_error_message(f"画像読み込みエラー: {str(e)}")
            return False
    
    def get_current_image_path(self):
        """現在の画像パスを取得"""
        return self._current_image_path
    
    def get_zoom_factor(self):
        """現在のズーム率を取得"""
        return self._zoom_factor
    
    def zoom_in(self):
        """ズームイン"""
        self._apply_zoom(1.25)
    
    def zoom_out(self):
        """ズームアウト"""
        self._apply_zoom(0.8)
    
    def zoom_fit(self):
        """画像をビューにフィット"""
        if not self._pixmap_item.pixmap().isNull():
            self._zoom_factor = 1.0
            self.resetTransform()
            self.fitInView(self._pixmap_item, Qt.KeepAspectRatio)
            self.zoom_changed.emit(self._zoom_factor)
    
    def zoom_actual_size(self):
        """実際のサイズで表示"""
        if not self._pixmap_item.pixmap().isNull():
            self._zoom_factor = 1.0
            self.resetTransform()
            self.zoom_changed.emit(self._zoom_factor)
    
    def _apply_zoom(self, factor):
        """ズームを適用"""
        if not self._pixmap_item.pixmap().isNull():
            self._zoom_factor *= factor
            self.scale(factor, factor)
            self.zoom_changed.emit(self._zoom_factor)
    
    def wheelEvent(self, event):
        """マウスホイールでズームイン・ズームアウト"""
        if not self._pixmap_item.pixmap().isNull():
            zoom_in = event.angleDelta().y() > 0
            factor = 1.25 if zoom_in else 0.8
            self._apply_zoom(factor)
    
    def show_no_image_message(self):
        """画像なしメッセージを表示"""
        placeholder_pixmap = QPixmap(400, 300)
        placeholder_pixmap.fill(Qt.lightGray)
        
        # TODO: テキストを描画してプレースホルダーを作成
        self._pixmap_item.setPixmap(placeholder_pixmap)
        self._current_image_path = ""
        self._zoom_factor = 1.0
    
    def show_error_message(self, message):
        """エラーメッセージを表示"""
        # TODO: エラー用のプレースホルダー画像を作成
        self.show_no_image_message()


class ImagePreviewControls(QWidget):
    """
    画像プレビューコントロール（ズームボタンなど）
    Clean Architecture対応版
    """
    # シグナル
    zoom_in_requested = pyqtSignal()
    zoom_out_requested = pyqtSignal()
    zoom_fit_requested = pyqtSignal()
    zoom_actual_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # ズームボタン
        self.zoom_in_btn = QPushButton("🔍+")
        self.zoom_in_btn.setToolTip("ズームイン")
        self.zoom_in_btn.clicked.connect(self.zoom_in_requested.emit)
        layout.addWidget(self.zoom_in_btn)
        
        self.zoom_out_btn = QPushButton("🔍-")
        self.zoom_out_btn.setToolTip("ズームアウト")
        self.zoom_out_btn.clicked.connect(self.zoom_out_requested.emit)
        layout.addWidget(self.zoom_out_btn)
        
        self.zoom_fit_btn = QPushButton("📐")
        self.zoom_fit_btn.setToolTip("ウィンドウにフィット")
        self.zoom_fit_btn.clicked.connect(self.zoom_fit_requested.emit)
        layout.addWidget(self.zoom_fit_btn)
        
        self.zoom_actual_btn = QPushButton("1:1")
        self.zoom_actual_btn.setToolTip("実際のサイズ")
        self.zoom_actual_btn.clicked.connect(self.zoom_actual_requested.emit)
        layout.addWidget(self.zoom_actual_btn)
        
        # ズーム率表示
        self.zoom_label = QLabel("100%")
        layout.addWidget(self.zoom_label)
        
        layout.addStretch()  # 右側に余白
    
    def update_zoom_label(self, zoom_factor):
        """ズーム率ラベルを更新"""
        percentage = int(zoom_factor * 100)
        self.zoom_label.setText(f"{percentage}%")


class PreviewPanel(QWidget):
    """
    プレビューパネル（画像プレビュー + コントロール）
    Clean Architecture対応版
    """
    # シグナル
    image_loaded = pyqtSignal(str)  # 画像ロード時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # プレビューコントロール
        self.controls = ImagePreviewControls()
        layout.addWidget(self.controls)
        
        # プレビュービュー
        self.preview_view = ImagePreviewView()
        layout.addWidget(self.preview_view)
    
    def _connect_signals(self):
        """シグナル接続"""
        # プレビュービューのシグナル
        self.preview_view.image_loaded.connect(self.image_loaded.emit)
        self.preview_view.zoom_changed.connect(self.controls.update_zoom_label)
        
        # コントロールのシグナル
        self.controls.zoom_in_requested.connect(self.preview_view.zoom_in)
        self.controls.zoom_out_requested.connect(self.preview_view.zoom_out)
        self.controls.zoom_fit_requested.connect(self.preview_view.zoom_fit)
        self.controls.zoom_actual_requested.connect(self.preview_view.zoom_actual_size)
    
    def set_image(self, image_path):
        """画像を設定"""
        return self.preview_view.set_image(image_path)
    
    def clear_image(self):
        """画像をクリア"""
        self.preview_view.show_no_image_message()
    
    def get_current_image_path(self):
        """現在の画像パスを取得"""
        return self.preview_view.get_current_image_path()


# 後方互換性のための関数（既存コードとの互換性維持）
def create_image_preview():
    """
    レガシー関数：画像プレビューを作成
    新しいImagePreviewViewクラスを使用して実装
    """
    return ImagePreviewView()


def create_preview_panel():
    """
    レガシー関数：プレビューパネルを作成
    新しいPreviewPanelクラスを使用して実装
    """
    return PreviewPanel()
