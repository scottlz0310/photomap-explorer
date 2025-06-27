"""
アドレスバーコントロール
Clean Architecture - プレゼンテーション層
"""
import os
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QStyle, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QSizePolicy


class AddressBarButton(QPushButton):
    """アドレスバー内のパス部分ボタン"""
    
    def __init__(self, text, path, double_click_callback):
        super().__init__(text)
        self.path = path
        self.double_click_callback = double_click_callback
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(
            'QPushButton { '
            'padding: 2px 8px; border: none; background: transparent; '
            'min-width: 0px; max-width: 300px; } '
            'QPushButton:hover { background: #e0e0e0; }'
        )
        self.setFixedHeight(28)
        self.setMaximumHeight(28)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
    
    def mouseDoubleClickEvent(self, event):
        """パス部分をダブルクリックした際の処理"""
        self.double_click_callback(self.path)
        event.accept()


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
    widget.path_changed.connect(on_part_double_clicked)
    widget.address_bar_widget.address_bar.returnPressed.connect(address_entered_callback)
    
    return widget, widget.address_bar
