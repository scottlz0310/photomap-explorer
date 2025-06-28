from PyQt5.QtWidgets import (QLineEdit, QPushButton, QHBoxLayout, QWidget, QStyle, 
                             QLabel, QSizePolicy, QApplication, QFrame)
from PyQt5.QtCore import Qt, QEvent, pyqtSignal, QPropertyAnimation, QEasingCurve, QRect
from PyQt5.QtGui import QPainter, QColor, QFont, QPalette, QFontMetrics

class GimpStyleAddressButton(QPushButton):
    """GIMP風のアドレスバーボタン - より正確なGIMPスタイル"""
    
    path_clicked = pyqtSignal(str)
    
    def __init__(self, text, path):
        super().__init__(text)
        self.path = path
        self.setFlat(True)
        self.setCursor(Qt.PointingHandCursor)
        
        # GIMP風のフォント（少し小さめ）
        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.setFont(font)
        
        # より正確なGIMP風のスタイル（グラデーション追加）
        self.setStyleSheet("""
            QPushButton {
                padding: 4px 8px;
                border: none;
                background: transparent;
                color: #2e3436;
                border-radius: 2px;
                min-width: 0px;
                text-align: left;
                margin: 0px;
            }
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #e8eaec, stop: 1 #d6d8da);
                color: #000000;
                border: 1px solid #a6a8aa;
            }
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #c6c8ca, stop: 1 #d6d8da);
                border: 1px solid #969899;
            }
            QPushButton:focus {
                outline: none;
                border: 1px solid #4a90e2;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f0f8ff, stop: 1 #e8f4fd);
            }
        """)
        
        self.setFixedHeight(24)  # GIMPに近いサイズ
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        
        # テキスト幅に基づく最適なサイズ設定
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(text)
        self.setMinimumWidth(text_width + 16)
        
        # アニメーション効果用のプロパティ
        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(150)
        self._animation.setEasingCurve(QEasingCurve.OutCubic)
        
        # クリック時のシグナル接続
        self.clicked.connect(lambda: self.path_clicked.emit(self.path))
        
    def enterEvent(self, event):
        """マウスホバー時のアニメーション"""
        super().enterEvent(event)
        # GIMPライクなホバー効果（軽微なアニメーション）
        
    def leaveEvent(self, event):
        """マウスリーブ時のアニメーション"""
        super().leaveEvent(event)
        
    def keyPressEvent(self, event):
        """キーボードナビゲーション"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.path_clicked.emit(self.path)
        elif event.key() == Qt.Key_Space:
            self.path_clicked.emit(self.path)
        else:
            super().keyPressEvent(event)

class GimpStyleSeparator(QLabel):
    """GIMP風のパス区切り - より正確なGIMPスタイル"""
    
    def __init__(self):
        super().__init__()
        self.setText("▶")  # 右向き三角形（GIMP 2.10+のスタイル）
        self.setStyleSheet("""
            QLabel {
                color: #888a85;
                background: transparent;
                border: none;
                padding: 0px 2px;
                font-size: 10px;
                font-weight: normal;
            }
        """)
        self.setFixedWidth(12)  # より狭く
        self.setFixedHeight(24)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

class GimpStyleAddressBar(QWidget):
    """GIMP風のアドレスバー - より正確なGIMPスタイル"""
    
    path_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.current_path = ""
        self.editing_mode = False
        self._setup_ui()
        
    def _setup_ui(self):
        """UI セットアップ"""
        self.setFixedHeight(32)  # GIMPに近いサイズ
        self.setContentsMargins(0, 0, 0, 0)
        
        # メインレイアウト
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # ブレッドクラムコンテナ（GIMPスタイル + シャドウ効果）
        self.breadcrumb_container = QFrame()
        self.breadcrumb_container.setFrameStyle(QFrame.StyledPanel)
        self.breadcrumb_container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #ffffff, stop: 0.1 #f8f8f8, stop: 1 #f0f0f0);
                border: 1px solid #a6a8aa;
                border-radius: 3px;
                margin: 0px;
            }
            QFrame:focus {
                border: 1px solid #4a90e2;
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 #f0f8ff, stop: 0.1 #e8f4fd, stop: 1 #e0f0fc);
            }
            QFrame:hover {
                border: 1px solid #969899;
            }
        """)
        
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_container)
        self.breadcrumb_layout.setContentsMargins(4, 2, 4, 2)  # GIMPライクなマージン
        self.breadcrumb_layout.setSpacing(0)
        self.breadcrumb_layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        # テキスト編集用LineEdit（GIMPスタイル）
        self.line_edit = QLineEdit()
        self.line_edit.setStyleSheet("""
            QLineEdit {
                border: 1px solid #4a90e2;
                border-radius: 3px;
                padding: 4px 6px;
                background: white;
                font-family: 'Segoe UI';
                font-size: 8pt;
                color: #2e3436;
            }
            QLineEdit:focus {
                border: 2px solid #4a90e2;
                background: #ffffff;
            }
        """)
        self.line_edit.setVisible(False)
        self.line_edit.returnPressed.connect(self._on_edit_finished)
        self.line_edit.editingFinished.connect(self._on_edit_finished)
        
        # レイアウトに追加
        self.main_layout.addWidget(self.breadcrumb_container)
        self.main_layout.addWidget(self.line_edit)
        
        # ダブルクリックで編集モードに切り替え
        self.breadcrumb_container.mouseDoubleClickEvent = self._enter_edit_mode
        
        # キーボードフォーカス対応
        self.setFocusPolicy(Qt.StrongFocus)
        self.breadcrumb_container.setFocusPolicy(Qt.StrongFocus)
        
    def keyPressEvent(self, event):
        """キーボードショートカット"""
        if event.key() == Qt.Key_F2:
            self._enter_edit_mode(None)
        elif event.key() == Qt.Key_Escape and self.editing_mode:
            self._exit_edit_mode()
        elif event.key() == Qt.Key_Tab and not self.editing_mode:
            # タブキーでブレッドクラム間を移動
            self._navigate_breadcrumbs(1)
        elif event.key() == Qt.Key_Backtab and not self.editing_mode:
            # Shift+Tab で逆方向移動
            self._navigate_breadcrumbs(-1)
        elif event.key() == Qt.Key_Home and event.modifiers() == Qt.ControlModifier:
            # Ctrl+Home でホームディレクトリ
            import os
            home_path = os.path.expanduser("~")
            self.path_changed.emit(home_path)
        elif event.key() == Qt.Key_Up and event.modifiers() == Qt.AltModifier:
            # Alt+↑ で親ディレクトリ
            import os
            if self.current_path:
                parent_path = os.path.dirname(self.current_path)
                if parent_path != self.current_path:  # ルートでない場合
                    self.path_changed.emit(parent_path)
        else:
            super().keyPressEvent(event)
            
    def _navigate_breadcrumbs(self, direction):
        """ブレッドクラム間でフォーカス移動"""
        # 現在フォーカスされているブレッドクラムボタンを探す
        focused_widget = self.focusWidget()
        buttons = self.breadcrumb_container.findChildren(GimpStyleAddressButton)
        
        if buttons and focused_widget in buttons:
            current_index = buttons.index(focused_widget)
            next_index = (current_index + direction) % len(buttons)
            buttons[next_index].setFocus()
        
    def set_path(self, path):
        """パスを設定してブレッドクラムを更新"""
        if path == self.current_path:
            return
            
        self.current_path = path
        self._update_breadcrumbs()
        
    def _update_breadcrumbs(self):
        """ブレッドクラムを更新"""
        # 既存のウィジェットを削除
        self._clear_breadcrumbs()
        
        if not self.current_path:
            return
            
        import os
        
        # パス分析
        abs_path = os.path.abspath(self.current_path)
        parts = self._parse_path(abs_path)
        
        # ブレッドクラムボタンを作成
        for i, (display_name, full_path) in enumerate(parts):
            # パス部分のボタン
            button = GimpStyleAddressButton(display_name, full_path)
            button.path_clicked.connect(self.path_changed.emit)
            
            # フォルダアイコンを追加（ルート以外）
            if i > 0:  # ルートディスクではないフォルダの場合
                button.setIcon(button.style().standardIcon(QStyle.SP_DirIcon))
            elif i == 0 and len(parts) > 1:  # ルートディスクの場合
                button.setIcon(button.style().standardIcon(QStyle.SP_DriveHDIcon))
            
            # キーボードナビゲーション用のタブオーダー
            button.setFocusPolicy(Qt.StrongFocus)
            if i == 0:
                button.setObjectName("first_breadcrumb")
            elif i == len(parts) - 1:
                button.setObjectName("last_breadcrumb")
                
            self.breadcrumb_layout.addWidget(button)
            
            # 区切り文字（最後以外）
            if i < len(parts) - 1:
                separator = GimpStyleSeparator()
                self.breadcrumb_layout.addWidget(separator)
        
        # 残りスペースを埋める
        self.breadcrumb_layout.addStretch()
        
        # アクセシビリティ
        self.setAccessibleName(f"アドレスバー: {self.current_path}")
        self.setAccessibleDescription("ダブルクリックで編集、F2キーで編集モード")
        
    def _parse_path(self, path):
        """パスを解析してブレッドクラム用の部品に分割"""
        import os
        parts = []
        
        if not path:
            return parts
            
        # ドライブ文字とパス部分を分離
        drive, rest = os.path.splitdrive(path)
        
        if drive:
            # Windows: C:\ など（GIMPスタイルで表示）
            root_path = drive + os.sep
            display_name = drive if not drive.endswith(':') else drive  # "C:" として表示
            parts.append((display_name, root_path))
            current_path = root_path
        else:
            # Unix系: / から開始
            current_path = os.sep
            parts.append((os.sep, current_path))
            
        # 残りのパス部分を処理
        if rest:
            path_parts = [p for p in rest.split(os.sep) if p]
            for part in path_parts:
                current_path = os.path.join(current_path, part)
                # 長いフォルダ名を短縮表示（GIMPライク）
                display_part = part
                if len(part) > 20:
                    display_part = part[:18] + "…"
                parts.append((display_part, current_path))
                
        return parts
        
    def _clear_breadcrumbs(self):
        """ブレッドクラムをクリア"""
        while self.breadcrumb_layout.count():
            child = self.breadcrumb_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def _enter_edit_mode(self, event):
        """編集モードに入る（F2キーまたはダブルクリック）"""
        self.editing_mode = True
        self.breadcrumb_container.setVisible(False)
        self.line_edit.setVisible(True)
        self.line_edit.setText(self.current_path)
        self.line_edit.selectAll()
        self.line_edit.setFocus()
        
        # GIMPライクなフェードイン効果
        self.line_edit.setProperty("geometry", self.breadcrumb_container.geometry())
        
    def _on_edit_finished(self):
        """編集完了"""
        if self.editing_mode:
            new_path = self.line_edit.text().strip()
            if new_path and new_path != self.current_path:
                # パスの有効性チェック
                import os
                if os.path.exists(new_path):
                    self.path_changed.emit(new_path)
                else:
                    # 無効なパスの場合は元に戻す
                    self.line_edit.setText(self.current_path)
                    # ユーザーに通知（アクセシビリティ対応）
                    self.setAccessibleDescription(f"無効なパス: {new_path}")
            
            self._exit_edit_mode()
            
    def _exit_edit_mode(self):
        """編集モードを終了"""
        self.editing_mode = False
        self.line_edit.setVisible(False)
        self.breadcrumb_container.setVisible(True)
        self.breadcrumb_container.setFocus()  # フォーカスを戻す

class GimpStyleHomeButton(QPushButton):
    """GIMP風のホームボタン"""
    
    def __init__(self, callback):
        super().__init__()
        self.setIcon(self.style().standardIcon(QStyle.SP_DirHomeIcon))
        self.setToolTip("ホームフォルダへ移動 (Ctrl+Home)")
        self.setFixedSize(28, 28)
        self.clicked.connect(callback)
        
        # GIMPライクなスタイル
        self.setStyleSheet("""
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
        """)

class GimpStyleRefreshButton(QPushButton):
    """GIMP風のリフレッシュボタン"""
    
    def __init__(self, callback):
        super().__init__()
        self.setIcon(self.style().standardIcon(QStyle.SP_BrowserReload))
        self.setToolTip("フォルダを更新 (F5)")
        self.setFixedSize(28, 28)
        self.clicked.connect(callback)
        
        # GIMPライクなスタイル
        self.setStyleSheet("""
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
        """)

def create_controls(address_entered_callback, go_to_parent_callback):
    """
    GIMP風アドレスバーと親フォルダボタンを作成する関数

    Args:
        address_entered_callback (function): アドレスバーでパスが変更された時のコールバック。
        go_to_parent_callback (function): 親フォルダボタンが押された時のコールバック。
    
    Returns:
        QWidget: アドレスバーとボタンを含むコンテナウィジェット。
        GimpStyleAddressBar: GIMP風アドレスバーウィジェット。
        QPushButton: 親フォルダボタンウィジェット。
    """
    # GIMP風アドレスバー
    address_bar = GimpStyleAddressBar()
    address_bar.path_changed.connect(address_entered_callback)

    # 親フォルダへ移動ボタン（GIMPスタイル）
    go_to_parent_button = QPushButton()
    go_to_parent_button.setIcon(go_to_parent_button.style().standardIcon(QStyle.SP_FileDialogToParent))
    go_to_parent_button.setToolTip("親フォルダへ移動 (Alt+↑)")
    go_to_parent_button.setFixedSize(28, 28)  # GIMPに合わせてサイズ調整
    go_to_parent_button.clicked.connect(go_to_parent_callback)
    
    # GIMPライクなボタンスタイル
    go_to_parent_button.setStyleSheet("""
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
    """)

    # レイアウト作成
    controls_widget = QWidget()
    layout = QHBoxLayout(controls_widget)
    layout.addWidget(address_bar, 1)  # アドレスバーを拡張
    layout.addWidget(go_to_parent_button)

    # GIMPライクなマージン設定
    layout.setContentsMargins(3, 3, 3, 3)
    layout.setSpacing(4)  # GIMPライクなスペース
    
    return controls_widget, address_bar, go_to_parent_button

def create_address_bar_widget(path, on_part_clicked, address_entered_callback):
    """
    GIMP風アドレスバーウィジェットを作成（レガシー互換性用）
    
    Args:
        path (str): 現在のパス
        on_part_clicked (function): パス部分クリック時のコールバック（引数:パス）
        address_entered_callback (function): テキスト入力でパス変更時のコールバック
    Returns:
        QWidget: アドレスバーウィジェット
        GimpStyleAddressBar: GIMP風アドレスバー
    """
    # GIMP風アドレスバーを作成
    address_bar = GimpStyleAddressBar()
    address_bar.set_path(path)
    
    # コールバック接続
    address_bar.path_changed.connect(address_entered_callback)
    
    # パス部分クリック用の接続（ブレッドクラムボタンのクリック）
    def connect_breadcrumb_clicks():
        """ブレッドクラムボタンのクリックイベントを接続"""
        # GimpStyleAddressButtonのpath_clickedシグナルをon_part_clickedに接続
        buttons = address_bar.breadcrumb_container.findChildren(GimpStyleAddressButton)
        for button in buttons:
            button.path_clicked.connect(on_part_clicked)
    
    # ブレッドクラム更新時にクリックイベントも更新
    original_update = address_bar._update_breadcrumbs
    def enhanced_update():
        original_update()
        connect_breadcrumb_clicks()
    address_bar._update_breadcrumbs = enhanced_update
    
    # 初回のクリックイベント接続
    connect_breadcrumb_clicks()
    
    return address_bar, address_bar

def create_gimp_style_navigation_bar(address_entered_callback, go_to_parent_callback, 
                                   go_to_home_callback=None, refresh_callback=None):
    """
    GIMP風のナビゲーションバーを作成する関数（ホーム・戻る・更新ボタン付き）

    Args:
        address_entered_callback (function): アドレスバーでパスが変更された時のコールバック。
        go_to_parent_callback (function): 親フォルダボタンが押された時のコールバック。
        go_to_home_callback (function): ホームボタンが押された時のコールバック。
        refresh_callback (function): リフレッシュボタンが押された時のコールバック。
    
    Returns:
        QWidget: ナビゲーションバー全体のコンテナウィジェット。
        GimpStyleAddressBar: GIMP風アドレスバーウィジェット。
        dict: 各ボタンウィジェットの辞書 {'parent': QPushButton, 'home': QPushButton, 'refresh': QPushButton}
    """
    # GIMP風アドレスバー
    address_bar = GimpStyleAddressBar()
    address_bar.path_changed.connect(address_entered_callback)

    # ボタン類
    buttons = {}
    
    # 親フォルダボタン
    buttons['parent'] = QPushButton()
    buttons['parent'].setIcon(buttons['parent'].style().standardIcon(QStyle.SP_FileDialogToParent))
    buttons['parent'].setToolTip("親フォルダへ移動 (Alt+↑)")
    buttons['parent'].setFixedSize(28, 28)
    buttons['parent'].clicked.connect(go_to_parent_callback)
    
    # ホームボタン（オプション）
    if go_to_home_callback:
        buttons['home'] = GimpStyleHomeButton(go_to_home_callback)
    
    # リフレッシュボタン（オプション）
    if refresh_callback:
        buttons['refresh'] = GimpStyleRefreshButton(refresh_callback)
    
    # 全ボタンに共通スタイル適用
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
    
    for button in buttons.values():
        button.setStyleSheet(button_style)

    # レイアウト作成
    nav_widget = QWidget()
    nav_widget.setStyleSheet("""
        QWidget {
            background: #ededed;
            border: none;
            margin: 0px;
        }
    """)
    
    layout = QHBoxLayout(nav_widget)
    
    # ボタンを追加（GIMP風の順序）
    if 'home' in buttons:
        layout.addWidget(buttons['home'])
    
    layout.addWidget(buttons['parent'])
    
    if 'refresh' in buttons:
        layout.addWidget(buttons['refresh'])
    
    layout.addWidget(address_bar, 1)  # アドレスバーを拡張

    # GIMPライクなマージン設定
    layout.setContentsMargins(4, 4, 4, 4)
    layout.setSpacing(2)  # GIMPライクな密なスペース
    
    return nav_widget, address_bar, buttons
