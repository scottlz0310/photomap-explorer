from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget, QStyle, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QSizePolicy

class AddressBarButton(QPushButton):
    def __init__(self, text, path, double_click_callback):
        super().__init__(text)
        self.path = path
        self.double_click_callback = double_click_callback
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet('QPushButton { padding: 2px 8px; border: none; background: transparent; min-width: 0px; max-width: 300px; } QPushButton:hover { background: #e0e0e0; }')
        self.setFixedHeight(28)
        self.setMaximumHeight(28)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
    def mouseDoubleClickEvent(self, event):
        self.double_click_callback(self.path)
        event.accept()

def create_controls(address_entered_callback, go_to_parent_callback):
    """
    アドレスバーと親フォルダボタンを作成する関数

    Args:
        address_entered_callback (function): アドレスバーでEnterが押された時のコールバック。
        go_to_parent_callback (function): 親フォルダボタンが押された時のコールバック。
    
    Returns:
        QWidget: アドレスバーとボタンを含むコンテナウィジェット。
        QLineEdit: アドレスバーウィジェット。
        QPushButton: 親フォルダボタンウィジェット。
    """
    # アドレスバー
    address_bar = QLineEdit()
    address_bar.setPlaceholderText("フォルダパスを入力してEnterを押してください")
    address_bar.returnPressed.connect(address_entered_callback)

    # 親フォルダへ移動ボタン（QStyle標準アイコン）
    go_to_parent_button = QPushButton()
    go_to_parent_button.setIcon(go_to_parent_button.style().standardIcon(QStyle.SP_FileDialogToParent))
    go_to_parent_button.setToolTip("親フォルダへ移動")
    go_to_parent_button.setFixedSize(30, 30)  # コンパクトなボタンサイズ
    go_to_parent_button.clicked.connect(go_to_parent_callback)

    # レイアウト作成
    controls_widget = QWidget()
    layout = QHBoxLayout(controls_widget)
    layout.addWidget(address_bar)
    layout.addWidget(go_to_parent_button)

    # マージンを設定
    layout.setContentsMargins(5, 5, 5, 5)  # 余白を調整
    layout.setSpacing(5)  # ウィジェット間のスペースを調整
    
    return controls_widget, address_bar, go_to_parent_button

def create_address_bar_widget(path, on_part_double_clicked, address_entered_callback):
    """
    パスを分割して各部分をボタン/ラベルで表示するアドレスバーウィジェットを作成
    Args:
        path (str): 現在のパス
        on_part_double_clicked (function): パス部分ダブルクリック時のコールバック（引数:パス）
        address_entered_callback (function): テキスト入力でEnter時のコールバック
    Returns:
        QWidget: アドレスバーウィジェット
        QLineEdit: テキスト入力用（編集時用）
    """
    import os
    widget = QWidget()
    widget.setFixedHeight(32)
    widget.setStyleSheet('background: white; border: 1px solid #bbb; border-radius: 5px;')
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(6, 2, 6, 2)
    layout.setSpacing(0)
    layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    # パス分割（Windows/UNIX両対応、各階層の絶対パスを保持）
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
    else:
        parts = []

    for i, (part, full_path) in enumerate(parts):
        btn = AddressBarButton(part, full_path, on_part_double_clicked)
        layout.addWidget(btn)
        if i < len(parts) - 1:
            sep = QLabel(os.sep)
            sep.setStyleSheet('color: gray; background: transparent; border: none;')
            layout.addWidget(sep)

    address_bar = QLineEdit(path)
    address_bar.setPlaceholderText("フォルダパスを入力してEnterを押してください")
    address_bar.returnPressed.connect(address_entered_callback)
    address_bar.setVisible(False)
    layout.addWidget(address_bar)

    return widget, address_bar
