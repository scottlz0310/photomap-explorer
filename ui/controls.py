from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout, QWidget

def create_controls(address_entered_callback, return_to_root_callback):
    """
    アドレスバーと全ドライブボタンを作成する関数

    Args:
        address_entered_callback (function): アドレスバーでEnterが押された時のコールバック。
        return_to_root_callback (function): 全ドライブボタンが押された時のコールバック。
    
    Returns:
        QWidget: アドレスバーとボタンを含むコンテナウィジェット。
        QLineEdit: アドレスバーウィジェット。
        QPushButton: 全ドライブボタンウィジェット。
    """
    # アドレスバー
    address_bar = QLineEdit()
    address_bar.setPlaceholderText("フォルダパスを入力してEnterを押してください")
    address_bar.returnPressed.connect(address_entered_callback)

    # 全ドライブに戻るボタン
    return_to_root_button = QPushButton("⤴")
    return_to_root_button.setFixedSize(30, 30)  # コンパクトなボタンサイズ
    return_to_root_button.clicked.connect(return_to_root_callback)

    # レイアウト作成
    controls_widget = QWidget()
    layout = QHBoxLayout(controls_widget)
    layout.addWidget(address_bar)
    layout.addWidget(return_to_root_button)
    layout.setContentsMargins(0, 0, 0, 0)  # マージンを省略してスッキリと表示

    return controls_widget, address_bar, return_to_root_button
