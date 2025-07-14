"""
カスタムフォルダ選択ダイアログ

理想的なフォルダ選択体験を提供：
- ファイルとフォルダ両方を表示
- フォルダをダブルクリックで移動
- 現在のフォルダを選択ボタンで確定
- アドレスバーで直接パス入力も可能
- サムネイル表示対応
"""

import os
import sys
from typing import Optional, List
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                            QTreeView, QLabel, QLineEdit, QMessageBox,
                            QFileSystemModel, QSplitter, QListWidget,
                            QListWidgetItem, QAbstractItemView, QFrame,
                            QHeaderView, QStyle, QToolButton, QComboBox)
from PyQt5.QtCore import Qt, QDir, QModelIndex, QFileInfo, QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QFont

from logic.image_utils import get_supported_extensions, create_image_preview


class CustomFolderDialog(QDialog):
    """カスタムフォルダ選択ダイアログ"""
    
    def __init__(self, parent=None, start_directory: str = None):
        super().__init__(parent)
        self.setWindowTitle("フォルダを選択")
        self.setModal(True)
        self.resize(800, 600)
        
        # 初期ディレクトリ
        if start_directory and os.path.exists(start_directory):
            self.current_directory = start_directory
        else:
            self.current_directory = os.path.expanduser("~")
        
        # 選択されたフォルダ
        self.selected_folder = None
        
        # サポートされる画像拡張子
        self.supported_extensions = get_supported_extensions()
        
        # UI初期化
        self._setup_ui()
        self._connect_signals()
        
        # 初期ディレクトリを表示
        self._navigate_to_directory(self.current_directory)
    
    def _setup_ui(self):
        """UI要素を設定"""
        layout = QVBoxLayout(self)
        
        # タイトルとアドレスバー
        self._setup_header(layout)
        
        # メインコンテンツエリア
        self._setup_main_content(layout)
        
        # ボタンエリア
        self._setup_buttons(layout)
    
    def _setup_header(self, layout):
        """ヘッダー（タイトルとアドレスバー）を設定"""
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        
        # タイトル
        title_label = QLabel("フォルダを選択してください")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        header_layout.addWidget(title_label)
        
        # アドレスバー
        address_layout = QHBoxLayout()
        
        # 上の階層ボタン
        self.up_button = QToolButton()
        self.up_button.setText("↑")
        self.up_button.setToolTip("上の階層へ")
        address_layout.addWidget(self.up_button)
        
        # アドレス入力
        self.address_edit = QLineEdit()
        self.address_edit.setPlaceholderText("フォルダパスを入力...")
        address_layout.addWidget(self.address_edit)
        
        # 移動ボタン
        self.go_button = QPushButton("移動")
        address_layout.addWidget(self.go_button)
        
        header_layout.addLayout(address_layout)
        layout.addWidget(header_frame)
    
    def _setup_main_content(self, layout):
        """メインコンテンツエリアを設定"""
        splitter = QSplitter(Qt.Horizontal)
        
        # 左パネル：フォルダツリー
        self._setup_folder_tree(splitter)
        
        # 右パネル：ファイル・フォルダリスト
        self._setup_file_list(splitter)
        
        # 分割比率を設定
        splitter.setSizes([250, 550])
        layout.addWidget(splitter)
    
    def _setup_folder_tree(self, splitter):
        """フォルダツリーを設定"""
        # フォルダツリー用のモデル
        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath("")
        self.tree_model.setFilter(QDir.Dirs | QDir.NoDotAndDotDot)
        
        # フォルダツリービュー
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.tree_model)
        self.tree_view.setRootIndex(self.tree_model.index(""))
        
        # 不要な列を非表示
        self.tree_view.hideColumn(1)  # Size
        self.tree_view.hideColumn(2)  # Type
        self.tree_view.hideColumn(3)  # Date Modified
        
        # ヘッダーを非表示
        self.tree_view.header().hide()
        
        splitter.addWidget(self.tree_view)
    
    def _setup_file_list(self, splitter):
        """ファイル・フォルダリストを設定"""
        # リストウィジェット
        self.file_list = QListWidget()
        self.file_list.setViewMode(QListWidget.IconMode)
        self.file_list.setIconSize(QSize(64, 64))
        self.file_list.setResizeMode(QListWidget.Adjust)
        self.file_list.setMovement(QListWidget.Static)
        self.file_list.setSelectionMode(QAbstractItemView.SingleSelection)
        
        splitter.addWidget(self.file_list)
    
    def _setup_buttons(self, layout):
        """ボタンエリアを設定"""
        button_layout = QHBoxLayout()
        
        # 現在のフォルダパス表示
        self.current_path_label = QLabel()
        self.current_path_label.setStyleSheet("color: #666; font-style: italic;")
        button_layout.addWidget(self.current_path_label)
        
        button_layout.addStretch()
        
        # キャンセルボタン
        self.cancel_button = QPushButton("キャンセル")
        button_layout.addWidget(self.cancel_button)
        
        # 現在のフォルダを選択ボタン
        self.select_current_button = QPushButton("このフォルダを選択")
        self.select_current_button.setDefault(True)
        button_layout.addWidget(self.select_current_button)
        
        layout.addLayout(button_layout)
    
    def _connect_signals(self):
        """シグナルを接続"""
        # アドレスバー
        self.up_button.clicked.connect(self._go_up)
        self.go_button.clicked.connect(self._go_to_address)
        self.address_edit.returnPressed.connect(self._go_to_address)
        
        # フォルダツリー
        self.tree_view.clicked.connect(self._on_tree_clicked)
        
        # ファイルリスト
        self.file_list.itemDoubleClicked.connect(self._on_file_double_clicked)
        
        # ボタン
        self.cancel_button.clicked.connect(self.reject)
        self.select_current_button.clicked.connect(self._select_current_folder)
    
    def _navigate_to_directory(self, directory: str):
        """指定されたディレクトリに移動"""
        if not os.path.exists(directory) or not os.path.isdir(directory):
            QMessageBox.warning(self, "エラー", f"ディレクトリが存在しません: {directory}")
            return
        
        try:
            self.current_directory = os.path.normpath(directory)
            
            # アドレスバー更新
            self.address_edit.setText(self.current_directory)
            
            # 現在のパス表示更新
            self.current_path_label.setText(f"現在の場所: {self.current_directory}")
            
            # フォルダツリー選択更新
            tree_index = self.tree_model.index(self.current_directory)
            if tree_index.isValid():
                self.tree_view.setCurrentIndex(tree_index)
                self.tree_view.expand(tree_index)
            
            # ファイルリスト更新
            self._update_file_list()
            
        except Exception as e:
            QMessageBox.warning(self, "エラー", f"ディレクトリの移動に失敗しました: {e}")
    
    def _update_file_list(self):
        """ファイルリストを更新"""
        self.file_list.clear()
        
        try:
            # ディレクトリの内容を取得
            items = []
            for item_name in os.listdir(self.current_directory):
                item_path = os.path.join(self.current_directory, item_name)
                if os.path.exists(item_path):
                    items.append((item_name, item_path))
            
            # ソート（フォルダが先、その後ファイル）
            items.sort(key=lambda x: (not os.path.isdir(x[1]), x[0].lower()))
            
            # リストに追加
            for item_name, item_path in items:
                self._add_item_to_list(item_name, item_path)
                
        except Exception as e:
            print(f"ファイルリスト更新エラー: {e}")
    
    def _add_item_to_list(self, name: str, path: str):
        """リストにアイテムを追加"""
        item = QListWidgetItem()
        item.setText(name)
        item.setData(Qt.UserRole, path)
        
        # アイコンを設定
        if os.path.isdir(path):
            # フォルダアイコン
            icon = self.style().standardIcon(QStyle.SP_DirIcon)
            item.setIcon(icon)
        else:
            # ファイルアイコン（画像の場合はサムネイル）
            if self._is_image_file(path):
                self._set_thumbnail_async(item, path)
            else:
                icon = self.style().standardIcon(QStyle.SP_FileIcon)
                item.setIcon(icon)
        
        self.file_list.addItem(item)
    
    def _is_image_file(self, path: str) -> bool:
        """画像ファイルかどうかを判定"""
        _, ext = os.path.splitext(path)
        return ext.lower() in self.supported_extensions
    
    def _set_thumbnail_async(self, item: QListWidgetItem, path: str):
        """サムネイルを非同期で設定"""
        # まずはデフォルトアイコンを設定
        icon = self.style().standardIcon(QStyle.SP_FileIcon)
        item.setIcon(icon)
        
        # タイマーで少し遅延してサムネイル読み込み
        QTimer.singleShot(100, lambda: self._load_thumbnail(item, path))
    
    def _load_thumbnail(self, item: QListWidgetItem, path: str):
        """サムネイルを読み込み"""
        try:
            pixmap = create_image_preview(path, 64)
            if pixmap and not pixmap.isNull():
                item.setIcon(QIcon(pixmap))
        except Exception as e:
            print(f"サムネイル読み込みエラー ({path}): {e}")
    
    def _go_up(self):
        """上の階層に移動"""
        parent_dir = os.path.dirname(self.current_directory)
        if parent_dir != self.current_directory:  # ルートでない場合
            self._navigate_to_directory(parent_dir)
    
    def _go_to_address(self):
        """アドレスバーのパスに移動"""
        address = self.address_edit.text().strip()
        if address:
            self._navigate_to_directory(address)
    
    def _on_tree_clicked(self, index: QModelIndex):
        """フォルダツリーがクリックされた"""
        if index.isValid():
            path = self.tree_model.filePath(index)
            self._navigate_to_directory(path)
    
    def _on_file_double_clicked(self, item: QListWidgetItem):
        """ファイルリストのアイテムがダブルクリックされた"""
        path = item.data(Qt.UserRole)
        if os.path.isdir(path):
            self._navigate_to_directory(path)
    
    def _select_current_folder(self):
        """現在のフォルダを選択"""
        self.selected_folder = self.current_directory
        self.accept()
    
    def get_selected_folder(self) -> Optional[str]:
        """選択されたフォルダを返す"""
        return self.selected_folder


def show_custom_folder_dialog(parent=None, start_directory: str = None) -> Optional[str]:
    """カスタムフォルダ選択ダイアログを表示"""
    dialog = CustomFolderDialog(parent, start_directory)
    if dialog.exec_() == QDialog.Accepted:
        return dialog.get_selected_folder()
    return None


if __name__ == "__main__":
    # テスト用
    from PyQt5.QtWidgets import QApplication
    import sys
from utils.debug_logger import debug, info, warning, error, verbose
    
    app = QApplication(sys.argv)
    
    folder = show_custom_folder_dialog()
    if folder:
        print(f"選択されたフォルダ: {folder}")
    else:
        print("キャンセルされました")
    
    sys.exit()
