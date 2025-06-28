"""
サムネイルリストコンポーネント
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtWidgets import (QListWidget, QListWidgetItem, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QRadioButton, QButtonGroup)
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt, pyqtSignal


def load_pixmap(image_path):
    """画像パスからQPixmapを生成して返すユーティリティ関数"""
    return QPixmap(image_path)


class ThumbnailListWidget(QListWidget):
    """
    サムネイル表示用リストウィジェット
    Clean Architecture対応版
    """
    # シグナル
    thumbnail_clicked = pyqtSignal(str)  # サムネイルクリック時（画像パス）
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._updating = False  # リスト更新中フラグ
    
    def _setup_ui(self):
        """UIセットアップ"""
        # 複数列表示のための設定
        self.setViewMode(QListWidget.IconMode)
        self.setResizeMode(QListWidget.Adjust)
        self.setMovement(QListWidget.Static)
        self.setFlow(QListWidget.LeftToRight)
        self.setSpacing(8)
        
        # デフォルトアイコンサイズ
        self.setIconSize(QSize(128, 128))
        
        # シグナル接続
        self.itemClicked.connect(self._on_item_clicked)
    
    def _on_item_clicked(self, item):
        """アイテムクリック時の処理"""
        if self._updating:
            return  # 更新中は無視
        
        image_path = item.data(Qt.UserRole)  # 絶対パスを取得
        if image_path:
            self.thumbnail_clicked.emit(image_path)
    
    def update_thumbnails(self, image_paths):
        """サムネイル一覧を更新"""
        self._updating = True
        self.clear()
        
        for path in image_paths:
            icon = QIcon(load_pixmap(path))
            item = QListWidgetItem(icon, "")  # ファイル名非表示
            item.setData(Qt.UserRole, path)  # 絶対パスを保持
            self.addItem(item)
        
        self._updating = False
    
    def set_thumbnail_size(self, size):
        """サムネイルサイズを設定"""
        if isinstance(size, str):
            # 文字列指定の場合
            size_map = {
                'small': QSize(64, 64),
                'medium': QSize(128, 128),
                'large': QSize(192, 192)
            }
            size = size_map.get(size, QSize(128, 128))
        
        self.setIconSize(size)
        self.update()  # 再描画
    
    def select_thumbnail(self, image_path, center=False):
        """指定された画像のサムネイルを選択"""
        if self._updating:
            return  # 更新中は無視
        
        norm_image_path = os.path.normcase(os.path.normpath(image_path))
        
        for i in range(self.count()):
            item = self.item(i)
            item_path = os.path.normcase(os.path.normpath(item.data(Qt.UserRole)))
            
            if item_path == norm_image_path:
                self.setCurrentItem(item)
                self.setFocus()
                
                if center:
                    self.scrollToItem(item, QListWidget.PositionAtCenter)
                break


class ThumbnailSizeControl(QWidget):
    """
    サムネイルサイズ変更コントロール
    Clean Architecture対応版
    """
    # シグナル
    size_changed = pyqtSignal(str)  # サイズ変更時（サイズラベル）
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        
        # ラベル
        label = QLabel("サムネイルサイズの変更")
        layout.addWidget(label)
        
        # ラジオボタン
        radio_layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        
        # サイズオプション
        size_options = [
            ("小", "small"),
            ("中", "medium"),
            ("大", "large")
        ]
        
        for label_text, size_value in size_options:
            btn = QRadioButton(label_text)
            self.button_group.addButton(btn)
            radio_layout.addWidget(btn)
            
            # シグナル接続
            btn.toggled.connect(
                lambda checked, s=size_value: checked and self.size_changed.emit(s)
            )
        
        layout.addLayout(radio_layout)
        
        # デフォルトで中サイズを選択
        self.set_size("medium")
    
    def set_size(self, size):
        """サイズを設定"""
        size_to_index = {"small": 0, "medium": 1, "large": 2}
        index = size_to_index.get(size, 1)  # デフォルトは中
        
        button = self.button_group.buttons()[index]
        button.setChecked(True)


class ThumbnailPanel(QWidget):
    """
    サムネイルパネル（サムネイルリスト + サイズコントロール）
    Clean Architecture対応版
    """
    # シグナル
    thumbnail_clicked = pyqtSignal(str)  # サムネイルクリック時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        
        # サムネイルリスト
        self.thumbnail_list = ThumbnailListWidget()
        layout.addWidget(self.thumbnail_list)
        
        # サイズコントロール
        self.size_control = ThumbnailSizeControl()
        layout.addWidget(self.size_control)
    
    def _connect_signals(self):
        """シグナル接続"""
        self.thumbnail_list.thumbnail_clicked.connect(self.thumbnail_clicked.emit)
        self.size_control.size_changed.connect(self.thumbnail_list.set_thumbnail_size)
    
    def update_thumbnails(self, image_paths):
        """サムネイル一覧を更新"""
        self.thumbnail_list.update_thumbnails(image_paths)
    
    def select_thumbnail(self, image_path, center=False):
        """指定された画像のサムネイルを選択"""
        self.thumbnail_list.select_thumbnail(image_path, center)
    
    def set_thumbnail_size(self, size):
        """サムネイルサイズを設定"""
        self.size_control.set_size(size)


# 後方互換性のための関数（既存コードとの互換性維持）
def create_thumbnail_list(thumbnail_clicked_callback):
    """
    レガシー関数：サムネイル一覧のウィジェットを作成
    新しいThumbnailListWidgetクラスを使用して実装
    """
    thumbnail_list = ThumbnailListWidget()
    thumbnail_list.thumbnail_clicked.connect(thumbnail_clicked_callback)
    return thumbnail_list


def add_thumbnail(thumbnail_list, image_path):
    """
    レガシー関数：サムネイルをサムネイル一覧に追加
    新しいAPIに合わせて更新
    """
    # 単一画像の追加は新しいAPIでは update_thumbnails を使用
    current_paths = []
    
    # 既存のアイテムを取得
    for i in range(thumbnail_list.count()):
        item = thumbnail_list.item(i)
        path = item.data(Qt.UserRole)
        if path:
            current_paths.append(path)
    
    # 新しいパスを追加
    current_paths.append(image_path)
    
    # リストを更新
    thumbnail_list.update_thumbnails(current_paths)


def set_thumbnail_size(thumbnail_list, size_label):
    """
    レガシー関数：サムネイルサイズを設定
    新しいAPIに転送
    """
    thumbnail_list.set_thumbnail_size(size_label)
