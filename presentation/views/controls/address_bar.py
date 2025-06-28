"""
アドレスバーコントロール（GIMP風）
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QStyle, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QSizePolicy

# GIMP風アドレスバーをインポート
from ui.controls import GimpStyleAddressBar, create_controls


class NavigationControls(QWidget):
    """
    GIMP風ナビゲーションコントロール（新UI用）
    Clean Architecture対応版
    """
    # シグナル
    path_changed = pyqtSignal(str)
    parent_folder_requested = pyqtSignal()
    home_folder_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_path = ""
    
    def _setup_ui(self):
        """GIMP風UIをセットアップ"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        
        # GIMP風アドレスバーを作成
        self.address_bar = GimpStyleAddressBar()
        self.address_bar.path_changed.connect(self.path_changed.emit)
        
        # ナビゲーションボタン
        self.parent_button = QPushButton()
        self.parent_button.setIcon(self.parent_button.style().standardIcon(QStyle.SP_FileDialogToParent))
        self.parent_button.setToolTip("親フォルダへ移動 (Alt+↑)")
        self.parent_button.setFixedSize(28, 28)
        self.parent_button.clicked.connect(self.parent_folder_requested.emit)
        
        # ホームボタン
        self.home_button = QPushButton()
        self.home_button.setIcon(self.home_button.style().standardIcon(QStyle.SP_DirHomeIcon))
        self.home_button.setToolTip("ホームフォルダへ移動 (Ctrl+Home)")
        self.home_button.setFixedSize(28, 28)
        self.home_button.clicked.connect(self.home_folder_requested.emit)
        
        # リフレッシュボタン
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(self.refresh_button.style().standardIcon(QStyle.SP_BrowserReload))
        self.refresh_button.setToolTip("フォルダを更新 (F5)")
        self.refresh_button.setFixedSize(28, 28)
        self.refresh_button.clicked.connect(self.refresh_requested.emit)
        
        # GIMP風のボタンスタイル
        button_style = """
            QPushButton {
                border: 1px solid #a6a8aa;
                border-radius: 3px;
                background: #f6f6f6;
                padding: 2px;
            }
            QPushButton:hover {
                background: #d6d8da;
                border-color: #969899;
            }
            QPushButton:pressed {
                background: #c6c8ca;
                border-color: #868889;
            }
            QPushButton:focus {
                border: 1px solid #4a90e2;
                background: #e8f4fd;
            }
        """
        
        self.parent_button.setStyleSheet(button_style)
        self.home_button.setStyleSheet(button_style)
        self.refresh_button.setStyleSheet(button_style)
        
        # レイアウトに追加（GIMP風の順序）
        layout.addWidget(self.home_button)
        layout.addWidget(self.parent_button)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.address_bar, 1)  # アドレスバーを拡張
    
    def set_path(self, path):
        """パスを設定"""
        self._current_path = path
        self.address_bar.set_path(path)
    
    def get_path(self):
        """現在のパスを取得"""
        return self._current_path
    
    def keyPressEvent(self, event):
        """キーボードショートカット"""
        if event.key() == Qt.Key_F5:
            self.refresh_requested.emit()
        elif event.key() == Qt.Key_Home and event.modifiers() == Qt.ControlModifier:
            self.home_folder_requested.emit()
        elif event.key() == Qt.Key_Up and event.modifiers() == Qt.AltModifier:
            self.parent_folder_requested.emit()
        else:
            super().keyPressEvent(event)


class AddressBarWidget(QWidget):
    """
    パスを分割して各部分をボタン/ラベルで表示するアドレスバーウィジェット
    Clean Architecture対応版
    """
    # シグナル
    path_changed = pyqtSignal(str)  # パス変更時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        self._current_path = ""
    
    def _setup_ui(self):
        """UIセットアップ"""
        self.setFixedHeight(32)
        self.setStyleSheet('background: white; border: 1px solid #bbb; border-radius: 5px;')
        
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(6, 2, 6, 2)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # テキスト入力用（編集時用）
        self.address_bar = QLineEdit()
        self.address_bar.setPlaceholderText("フォルダパスを入力してEnterを押してください")
        self.address_bar.returnPressed.connect(self._on_address_entered)
        self.address_bar.setVisible(False)
        self.layout.addWidget(self.address_bar)
    
    def set_path(self, path):
        """パスを設定してボタン表示を更新"""
        self._current_path = path
        self._update_path_display()
    
    def get_path(self):
        """現在のパスを取得"""
        return self._current_path
    
    def _update_path_display(self):
        """パス表示を更新"""
        # 既存のボタン/ラベルをクリア
        while self.layout.count() > 1:  # address_barは残す
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # パス分割（Windows/UNIX両対応、各階層の絶対パスを保持）
        parts = self._split_path(self._current_path)
        
        for i, (part, full_path) in enumerate(parts):
            btn = AddressBarButton(part, full_path, self._on_part_double_clicked)
            self.layout.insertWidget(i * 2, btn)
            
            if i < len(parts) - 1:
                sep = QLabel(os.sep)
                sep.setStyleSheet('color: gray; background: transparent; border: none;')
                self.layout.insertWidget(i * 2 + 1, sep)
    
    def _split_path(self, path):
        """パスを階層ごとに分割"""
        parts = []
        abs_path = os.path.abspath(path) if path else ''
        
        if abs_path:
            drive, rest = os.path.splitdrive(abs_path)
            if drive:
                current = drive + os.sep
                parts.append((drive, current))
            else:
                current = os.sep
                parts.append((os.sep, current))
            
            for p in rest.strip(os.sep).split(os.sep):
                if p:
                    current = os.path.join(current, p)
                    parts.append((p, current))
        
        return parts
    
    def _on_part_double_clicked(self, path):
        """パス部分ダブルクリック時の処理"""
        self.path_changed.emit(path)
    
    def _on_address_entered(self):
        """アドレスバーでEnter押下時の処理"""
        new_path = self.address_bar.text().strip()
        if new_path and os.path.exists(new_path):
            self.path_changed.emit(new_path)


class NavigationControls(QWidget):
    """
    ナビゲーションコントロール（アドレスバー + 親フォルダボタン）
    Clean Architecture対応版
    """
    # シグナル
    path_changed = pyqtSignal(str)  # パス変更時
    parent_requested = pyqtSignal()  # 親フォルダボタン押下時
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
    
    def _setup_ui(self):
        """UIセットアップ"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # アドレスバー
        self.address_bar_widget = AddressBarWidget()
        self.address_bar_widget.path_changed.connect(self.path_changed.emit)
        layout.addWidget(self.address_bar_widget)
        
        # 親フォルダへ移動ボタン
        self.go_to_parent_button = QPushButton()
        self.go_to_parent_button.setIcon(
            self.go_to_parent_button.style().standardIcon(QStyle.SP_FileDialogToParent)
        )
        self.go_to_parent_button.setToolTip("親フォルダへ移動")
        self.go_to_parent_button.setFixedSize(30, 30)
        self.go_to_parent_button.clicked.connect(self.parent_requested.emit)
        layout.addWidget(self.go_to_parent_button)
    
    def set_path(self, path):
        """現在のパスを設定"""
        self.address_bar_widget.set_path(path)
    
    def get_path(self):
        """現在のパスを取得"""
        return self.address_bar_widget.get_path()


# 後方互換性のための関数（既存コードとの互換性維持）
def create_controls(address_entered_callback, go_to_parent_callback):
    """
    レガシー関数：アドレスバーと親フォルダボタンを作成
    新しいNavigationControlsクラスを使用して実装
    """
    controls = NavigationControls()
    
    # コールバック接続
    controls.path_changed.connect(lambda path: address_entered_callback())
    controls.parent_requested.connect(go_to_parent_callback)
    
    # レガシーインターフェースのため、個別コンポーネントも返す
    address_bar = controls.address_bar_widget.address_bar
    go_to_parent_button = controls.go_to_parent_button
    
    return controls, address_bar, go_to_parent_button


def create_address_bar_widget(path, on_part_double_clicked, address_entered_callback):
    """
    レガシー関数：アドレスバーウィジェットを作成
    新しいAddressBarWidgetクラスを使用して実装
    """
    widget = AddressBarWidget()
    widget.set_path(path)
    
    # コールバック接続
    if on_part_double_clicked:
        widget.path_changed.connect(on_part_double_clicked)
    
    # 仮の編集エリア（実際のフィールドがないため、ダミーを返す）
    dummy_edit = QLineEdit()
    if address_entered_callback:
        dummy_edit.returnPressed.connect(address_entered_callback)
    
    return widget, dummy_edit
