"""
フォルダパネルコンポーネント
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QTreeView, 
                            QHeaderView, QFileSystemModel, QAbstractItemView)
from PyQt5.QtCore import Qt, QDir, pyqtSignal, QModelIndex


class FolderTreeView(QTreeView):
    """
    フォルダツリービュー
    Clean Architecture対応版
    """
    # シグナル
    folder_selected = pyqtSignal(str)  # フォルダ選択時
    folder_double_clicked = pyqtSignal(str)  # フォルダダブルクリック時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_path = QDir.rootPath()  # 初期化を最初に移動
        self._setup_model()
        self._setup_ui()
    
    def _setup_model(self):
        """ファイルシステムモデルのセットアップ"""
        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.setModel(self.model)
    
    def _setup_ui(self):
        """UIセットアップ"""
        # 表示設定
        self.setTextElideMode(Qt.ElideNone)
        self.header().setSectionResizeMode(0, QHeaderView.Interactive)
        self.header().setSectionResizeMode(1, QHeaderView.Interactive)
        self.header().setSectionResizeMode(2, QHeaderView.Interactive)
        
        # カラム幅設定
        self.setColumnWidth(0, 200)
        self.setColumnWidth(1, 100)
        self.setColumnWidth(2, 150)
        
        # 不要なカラムを非表示
        self.setColumnHidden(1, True)  # サイズ
        self.setColumnHidden(2, True)  # 種類
        self.setColumnHidden(3, True)  # 更新日時
        
        # ツリー表示設定
        self.setRootIsDecorated(False)
        self.setItemsExpandable(False)
        self.setHeaderHidden(False)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # シグナル接続
        self.clicked.connect(self._on_clicked)
        self.doubleClicked.connect(self._on_double_clicked)
        
        # 初期設定
        self.set_root_path(self._current_path)
    
    def _on_clicked(self, index):
        """アイテムクリック時の処理"""
        path = self.model.filePath(index)
        if self.model.isDir(index):
            self.folder_selected.emit(path)
        else:
            # ファイルの場合もemit（プレビュー・地図表示用）
            self.folder_selected.emit(path)
    
    def _on_double_clicked(self, index):
        """アイテムダブルクリック時の処理"""
        path = self.model.filePath(index)
        if self.model.isDir(index):
            self.folder_double_clicked.emit(path)
    
    def set_root_path(self, path):
        """ルートパスを設定"""
        if not path:
            # 空文字列なら全ドライブ
            self._current_path = ""
            index = self.model.index("")
        else:
            self._current_path = path
            index = self.model.index(path)
        
        self.setRootIndex(index)
    
    def get_current_path(self):
        """現在のパスを取得"""
        return self._current_path
    
    def select_file(self, file_path, center=False):
        """指定されたファイルを選択"""
        self.sortByColumn(0, Qt.AscendingOrder)
        index = self.model.index(file_path)
        if index.isValid():
            self.setCurrentIndex(index)
            if center:
                self.scrollTo(index, QAbstractItemView.PositionAtCenter)


class FolderPanel(QWidget):
    """
    フォルダパネル（ツリービュー + ナビゲーションボタン）
    Clean Architecture対応版
    """
    # シグナル
    folder_changed = pyqtSignal(str)  # フォルダ移動時にパスを通知
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        
        # 戻るボタン
        self.back_button = QPushButton('⬆ 親ディレクトリ/全ドライブへ戻る')
        self.back_button.setFixedHeight(32)
        layout.addWidget(self.back_button)
        
        # フォルダツリー
        self.folder_tree = FolderTreeView()
        layout.addWidget(self.folder_tree)
    
    def _connect_signals(self):
        """シグナル接続"""
        self.back_button.clicked.connect(self._go_back)
        self.folder_tree.folder_selected.connect(self.folder_changed.emit)
        self.folder_tree.folder_double_clicked.connect(self._on_folder_double_clicked)
    
    def _go_back(self):
        """親ディレクトリへ戻る処理"""
        current_path = self.folder_tree.get_current_path()
        
        # 現在が全ドライブ表示なら何もしない
        if not current_path or current_path == "":
            return
        
        # Windows: ドライブ直下なら全ドライブへ
        if os.name == 'nt':
            drive, rest = os.path.splitdrive(current_path)
            if drive and rest in ('\\', '/', ''):
                self.set_root("")
                self.folder_changed.emit("")
                return
        
        # ルートや空パスも全ドライブ
        if not current_path or current_path in (QDir.rootPath(), "/", "C:/"):
            self.set_root("")
            self.folder_changed.emit("")
            return
        
        # それ以外は親ディレクトリへ
        parent = QDir(current_path)
        if parent.cdUp():
            new_path = parent.absolutePath()
            self.set_root(new_path)
            self.folder_changed.emit(new_path)
    
    def _on_folder_double_clicked(self, path):
        """フォルダダブルクリック時の処理"""
        self.set_root(path)
        self.folder_changed.emit(path)
    
    def set_root(self, path):
        """ルートパスを設定"""
        self.folder_tree.set_root_path(path)
    
    def get_path(self, index):
        """指定されたインデックスのパスを取得"""
        return self.folder_tree.model.filePath(index)
    
    def select_file(self, file_path, center=False):
        """指定されたファイルを選択"""
        self.folder_tree.select_file(file_path, center)
    
    def get_current_path(self):
        """現在のパスを取得"""
        return self.folder_tree.get_current_path()


# 後方互換性のための関数（既存コードとの互換性維持）
def create_folder_panel(on_folder_selected):
    """
    レガシー関数：フォルダパネルを作成
    新しいFolderPanelクラスを使用して実装
    """
    panel = FolderPanel()
    panel.folder_changed.connect(on_folder_selected)
    return panel
