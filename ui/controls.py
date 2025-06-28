from PyQt5.QtWidgets import (QLineEdit, QPushButton, QHBoxLayout, QWidget, 
                            QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from presentation.themes.theme_mixin import ThemeAwareMixin
import os


class GIMPAddressBar(QWidget, ThemeAwareMixin):
    """
    GIMP風ブレッドクラムアドレスバー
    
    パスをボタン形式で表示し、クリックで移動可能
    テキスト入力モードとの切り替えも対応
    """
    
    path_changed = pyqtSignal(str)  # パス変更シグナル
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_path = ""
        self.is_edit_mode = False
        self.setup_ui()
    
    def setup_ui(self):
        """UI初期化"""
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(2)
        
        # ブレッドクラムコンテナ（スクロールエリアなし）
        self.breadcrumb_widget = QWidget()
        self.breadcrumb_widget.setMaximumHeight(34)  # 高さを30pxに合わせて調整
        self.breadcrumb_widget.setMinimumHeight(30)
        self.breadcrumb_layout = QHBoxLayout(self.breadcrumb_widget)
        self.breadcrumb_layout.setContentsMargins(0, 0, 0, 0)
        self.breadcrumb_layout.setSpacing(1)
        
        # テキスト入力フィールド（編集モード用）
        self.text_edit = QLineEdit()
        self.text_edit.setVisible(False)
        self.text_edit.setMinimumHeight(28)  # 30pxに合わせて調整
        self.text_edit.returnPressed.connect(self._on_text_entered)
        self.text_edit.editingFinished.connect(self._exit_edit_mode)
        
        # テキスト入力フィールドのフォント設定
        text_font = QFont()
        text_font.setPointSize(10)  # 30px高さに合わせて調整
        self.text_edit.setFont(text_font)
        
        # 編集ボタン
        self.edit_button = QPushButton("📝")
        self.edit_button.setFixedSize(35, 30)  # 30pxに調整
        self.edit_button.setToolTip("テキスト入力モードに切り替え")
        self.edit_button.clicked.connect(self._toggle_edit_mode)
        
        # 編集ボタンのフォント設定
        edit_font = QFont()
        edit_font.setPointSize(12)  # フォントサイズも調整
        self.edit_button.setFont(edit_font)
        
        # レイアウト追加
        self.layout.addWidget(self.breadcrumb_widget, 1)  # 拡張可能
        self.layout.addWidget(self.text_edit, 1)    # 編集モード時
        self.layout.addWidget(self.edit_button)
        
        # 初期表示
        self.setText("")  # 初期パス
    
    def setText(self, path):
        """パスを設定（外部から呼び出し可能）"""
        self.current_path = path
        if self.is_edit_mode:
            self.text_edit.setText(path)
        else:
            self._update_breadcrumb(path)
    
    def text(self):
        """現在のパスを取得"""
        return self.current_path
    
    def _update_breadcrumb(self, path):
        """ブレッドクラム表示を更新（カレント側優先表示）"""
        # 既存のボタンをクリア
        for i in reversed(range(self.breadcrumb_layout.count())):
            item = self.breadcrumb_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        # 空のパスの場合は全ドライブ表示（Windows）
        if not path:
            if os.name == 'nt':  # Windows
                self._show_all_drives()
            return
        
        # パスを分割（正規化してから処理）
        path = os.path.normpath(path)
        parts = []
        
        if os.name == 'nt':  # Windows
            if ':' in path:
                drive, rest = path.split(':', 1)
                parts.append(drive + ':')
                if rest and rest.strip('\\'):
                    # 各フォルダを個別に分割
                    folders = rest.strip('\\').split('\\')
                    parts.extend([folder for folder in folders if folder])
            else:
                # UNCパスや他の形式への対応
                path_parts = path.strip('\\').split('\\')
                parts = [part for part in path_parts if part]
        else:  # Unix系
            parts = path.strip('/').split('/')
            if path.startswith('/'):
                parts.insert(0, '/')
        
        # ボタンを作成（まずは全て作成）
        all_buttons = []
        current_path = ""
        
        for i, part in enumerate(parts):
            if not part and i != 0:  # 空の部分をスキップ（ルート以外）
                continue
            
            # パス構築
            if os.name == 'nt':
                if i == 0:
                    # ドライブ部分（C:）には末尾に\を追加
                    if part.endswith(':'):
                        current_path = part + '\\'
                    else:
                        current_path = part
                else:
                    current_path = os.path.join(current_path, part)
            else:
                if part == '/':
                    current_path = '/'
                else:
                    current_path = os.path.join(current_path, part)
            
            # ボタン作成
            button = QPushButton(part if part else '/')
            button.setProperty('path', current_path)
            button.clicked.connect(lambda checked, p=current_path: self._on_button_clicked(p))
            
            # フォント設定（30px高さに適したサイズ）
            font = QFont()
            font.setPointSize(10)  # 30px高さに適したサイズ
            font.setWeight(QFont.Medium)
            button.setFont(font)
            
            # スタイル設定（区切り文字なしで枠を強化、統一性重視）
            button.setStyleSheet(self._get_button_style())
            
            all_buttons.append(button)
        
        # 利用可能な幅を計算してボタンを配置
        self._layout_buttons_with_priority(all_buttons)
    
    def _layout_buttons_with_priority(self, all_buttons):
        """
        カレント側（右側）を優先してボタンを配置
        幅が足りない場合はルート側から順次隠す
        """
        if not all_buttons:
            return
        
        # 利用可能な幅を取得
        available_width = self.breadcrumb_widget.width() - 20  # マージン考慮
        if available_width <= 0:
            available_width = 400  # 初期幅として仮定
        
        # 各ボタンの推定幅を計算
        button_widths = []
        total_width = 0
        
        for button in all_buttons:
            # ボタンのテキスト幅を推定
            text = button.text()
            estimated_width = len(text) * 8 + 24 + 2  # 文字幅 + パディング + マージン
            button_widths.append(estimated_width)
            total_width += estimated_width
        
        # 全てのボタンが収まる場合は全て表示
        if total_width <= available_width:
            for button in all_buttons:
                self.breadcrumb_layout.addWidget(button)
            # 右端にスペーサー追加
            self.breadcrumb_layout.addStretch()
            return
        
        # 幅が足りない場合：カレント側から優先して配置
        # 「...」ボタンの幅も考慮
        ellipsis_width = 30
        used_width = 0
        visible_buttons = []
        
        # 後ろ（カレント側）から順に追加していく
        for i in reversed(range(len(all_buttons))):
            button = all_buttons[i]
            button_width = button_widths[i]
            
            # 「...」ボタンが必要な場合の幅も考慮
            needed_width = used_width + button_width
            if i > 0:  # まだルート側にボタンがある場合
                needed_width += ellipsis_width
            
            if needed_width <= available_width:
                visible_buttons.insert(0, button)  # 先頭に挿入（順序維持）
                used_width += button_width
            else:
                break
        
        # 隠されたボタンがある場合は「...」ボタンを追加
        if len(visible_buttons) < len(all_buttons):
            ellipsis_button = QPushButton("...")
            ellipsis_button.setFixedSize(30, 22)
            ellipsis_button.setToolTip("隠されたパス部分をクリックして表示")
            
            # 隠されたボタンの最後のパスにジャンプ
            hidden_buttons = all_buttons[:len(all_buttons) - len(visible_buttons)]
            if hidden_buttons:
                last_hidden_path = hidden_buttons[-1].property('path')
                ellipsis_button.clicked.connect(lambda checked, p=last_hidden_path: self._on_button_clicked(p))
            
            # スタイル設定
            ellipsis_button.setStyleSheet(self._get_button_style())
            self.breadcrumb_layout.addWidget(ellipsis_button)
        
        # 可視ボタンを追加
        for button in visible_buttons:
            self.breadcrumb_layout.addWidget(button)
        
        # 右端にスペーサー追加
        self.breadcrumb_layout.addStretch()

    def _get_button_style(self):
        """テーマに応じたボタンスタイルを取得"""
        try:
            if hasattr(self, 'get_theme_color'):
                # テーマカラーを取得
                bg = self.get_theme_color('button_bg') or '#f0f0f0'
                border = self.get_theme_color('border') or '#cccccc'
                text = self.get_theme_color('foreground') or '#000000'
                hover_bg = self.get_theme_color('hover') or '#e6f3ff'
                selection = self.get_theme_color('selection') or '#cce8ff'
                accent = self.get_theme_color('accent') or '#0078d4'
            else:
                # フォールバック値（ライトテーマ）
                bg = '#f0f0f0'
                border = '#cccccc'
                text = '#000000'
                hover_bg = '#e6f3ff'
                selection = '#cce8ff'
                accent = '#0078d4'
        except:
            # エラー時のフォールバック値
            bg = '#f0f0f0'
            border = '#cccccc'
            text = '#000000'
            hover_bg = '#e6f3ff'
            selection = '#cce8ff'
            accent = '#0078d4'
        
        return f"""
            QPushButton {{
                border: 2px solid {border};
                background-color: {bg};
                color: {text};
                padding: 4px 12px;
                margin: 1px;
                border-radius: 5px;
                min-height: 18px;
                max-height: 22px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {hover_bg};
                border-color: {accent};
            }}
            QPushButton:pressed {{
                background-color: {selection};
                border-color: {accent};
            }}
        """
    
    def _show_all_drives(self):
        """Windows全ドライブ表示"""
        import string
        
        # 利用可能なドライブを検索
        drives = []
        for drive_letter in string.ascii_uppercase:
            drive_path = f"{drive_letter}:\\"
            if os.path.exists(drive_path):
                drives.append(drive_path)
        
        # 各ドライブのボタンを作成
        for drive in drives:
            drive_name = drive.rstrip('\\')  # "C:" の形式
            button = QPushButton(drive_name)
            button.setProperty('path', drive)
            button.clicked.connect(lambda checked, p=drive: self._on_button_clicked(p))
            
            # フォント設定
            font = QFont()
            font.setPointSize(10)
            font.setWeight(QFont.Medium)
            button.setFont(font)
            
            # スタイル設定
            button.setStyleSheet(self._get_button_style())
            
            self.breadcrumb_layout.addWidget(button)
        
        # 右端にスペーサー追加
        self.breadcrumb_layout.addStretch()
    
    def apply_theme(self):
        """テーマ適用"""
        super().apply_theme()
        # 既存のボタンを再作成
        self._update_breadcrumb(self.current_path)
    
    def _on_button_clicked(self, path):
        """ブレッドクラムボタンクリック処理"""
        # パスを正規化
        path = os.path.normpath(path)
        
        # 現在のパスと異なる場合のみ処理
        if path != self.current_path:
            self.current_path = path
            self.path_changed.emit(path)
            self._update_breadcrumb(path)
        else:
            # 同じパスの場合はリフレッシュのみ
            self.path_changed.emit(path)
    
    def _toggle_edit_mode(self):
        """編集モード切り替え"""
        if self.is_edit_mode:
            self._exit_edit_mode()
        else:
            self._enter_edit_mode()
    
    def _enter_edit_mode(self):
        """編集モードに切り替え"""
        self.is_edit_mode = True
        self.breadcrumb_widget.setVisible(False)
        self.text_edit.setVisible(True)
        self.text_edit.setText(self.current_path)
        self.text_edit.setFocus()
        self.text_edit.selectAll()
        self.edit_button.setText("✓")
        self.edit_button.setToolTip("確定")
    
    def _exit_edit_mode(self):
        """編集モード終了"""
        self.is_edit_mode = False
        self.breadcrumb_widget.setVisible(True)
        self.text_edit.setVisible(False)
        self.edit_button.setText("📝")
        self.edit_button.setToolTip("テキスト入力モードに切り替え")
    
    def _on_text_entered(self):
        """テキスト入力確定"""
        path = self.text_edit.text().strip()
        if path and os.path.exists(path):
            self.current_path = path
            self.path_changed.emit(path)
            self._exit_edit_mode()
            self._update_breadcrumb(path)
        else:
            # 無効なパスの場合は元に戻す
            self.text_edit.setText(self.current_path)
    
    def keyPressEvent(self, event):
        """キーボードイベント処理"""
        if event.key() == Qt.Key_Escape:
            if self.is_edit_mode:
                self.text_edit.setText(self.current_path)  # 元に戻す
                self._exit_edit_mode()
        super().keyPressEvent(event)


def create_controls(address_entered_callback, return_to_root_callback):
    """
    GIMP風アドレスバーと親フォルダボタンを作成する関数

    Args:
        address_entered_callback (function): アドレスバーでパスが変更された時のコールバック
        return_to_root_callback (function): 親フォルダボタンが押された時のコールバック
    
    Returns:
        QWidget: アドレスバーとボタンを含むコンテナウィジェット
        GIMPAddressBar: GIMP風アドレスバーウィジェット
        QPushButton: 親フォルダボタンウィジェット
    """
    # GIMP風アドレスバー
    address_bar = GIMPAddressBar()
    address_bar.path_changed.connect(address_entered_callback)

    # 親フォルダに戻るボタン
    parent_button = QPushButton("⬆️")
    parent_button.setFixedSize(38, 30)  # 30pxに統一
    parent_button.setToolTip("親フォルダへ移動")
    parent_button.clicked.connect(return_to_root_callback)
    
    # 親フォルダボタンのフォント設定
    parent_font = QFont()
    parent_font.setPointSize(12)  # サイズに合わせて調整
    parent_button.setFont(parent_font)

    # レイアウト作成
    controls_widget = QWidget()
    layout = QHBoxLayout(controls_widget)
    layout.addWidget(address_bar, 1)  # 拡張可能
    layout.addWidget(parent_button)

    # マージンを設定
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(5)
    
    return controls_widget, address_bar, parent_button
