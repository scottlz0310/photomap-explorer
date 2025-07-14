# PhotoMap Explorer 完全実装プロンプト

新しいTheme Managerライブラリ（https://github.com/scottlz0310/Theme-Manager）を使用して、PyQt5ベースの写真管理・地図表示アプリケーション「PhotoMap Explorer」を完全実装してください。

## 📋 プロジェクト概要

**PhotoMap Explorer**は、写真のEXIF情報から撮影場所を抽出し、地図上に表示する写真管理アプリケーションです。GIMP風のモダンなUIと、ダークモード対応の美しいテーマシステムを特徴としています。

### 🎯 主要機能
- **フォルダ・ファイル管理**: 写真フォルダの階層表示とナビゲーション
- **サムネイル表示**: 写真のサムネイル一覧表示
- **画像プレビュー**: 選択した写真の詳細表示
- **地図表示**: EXIF位置情報を基にした撮影場所の地図表示
- **GIMP風アドレスバー**: ブレッドクラム形式のパスナビゲーション
- **テーマシステム**: 16種類のテーマサポート（Theme Managerライブラリ使用）
- **パネル最大化**: 画像・地図パネルの全画面表示

## 🏗️ アーキテクチャ構成

### メインエントリーポイント
```python
# main.py
import sys
import os
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication
from presentation.views.main_view import MainWindow

def setup_qt_environment():
    """Qt環境の設定"""
    # PyQt5環境設定（プラグインパス、WebEngineパスなど）

if __name__ == "__main__":
    setup_qt_environment()
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
```

### アプリケーション構造

```
photomap-explorer/
├── main.py                           # メインエントリーポイント
├── presentation/                     # プレゼンテーション層
│   ├── views/
│   │   └── main_view.py                  # メインウィンドウ
│   └── themes/                       # テーマシステム（Theme Manager統合）
├── ui/                              # UIコンポーネント
│   ├── controls/                    # コントロール群
│   │   ├── address_bar/             # GIMP風アドレスバー
│   │   └── toolbar/                 # ツールバー機能
│   ├── thumbnail_list.py            # サムネイル表示
│   ├── image_preview.py             # 画像プレビュー
│   ├── map_panel.py                 # 地図パネル
│   └── custom_folder_dialog.py      # フォルダダイアログ
├── logic/                           # ビジネスロジック
│   └── image_utils.py               # 画像処理・EXIF読取
├── utils/                           # ユーティリティ
│   └── debug_logger.py              # ログ出力
└── assets/                          # リソース
    ├── pme_icon.png                 # アプリケーションアイコン
    └── (test images)                # テスト用画像
```

## 🎨 Theme Manager統合

### Theme Managerの導入
```python
# Theme Manager ライブラリのインストール
git clone https://github.com/scottlz0310/Theme-Manager
pip install -e ./Theme-Manager

# 基本的な使用方法
from theme_manager.qt.controller import ThemeController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # テーマコントローラーの初期化
        self.theme_controller = ThemeController()
        
        # 利用可能なテーマの取得
        self.available_themes = self.theme_controller.get_available_themes()
        
        # UIセットアップ
        self.setup_ui()
        
        # 初期テーマ適用
        self.theme_controller.apply_theme_to_widget(self)
        
    def switch_theme(self, theme_name):
        """テーマ切り替え"""
        self.theme_controller.set_theme(theme_name)
        self.theme_controller.apply_theme_to_widget(self)
```

### 利用可能なテーマ
Theme Managerライブラリが提供する16種類のテーマを活用：

**コアテーマ**:
- `light` - ライトモード
- `dark` - ダークモード  
- `high_contrast` - 高コントラスト

**カラーテーマ**:
- `blue`, `green`, `purple`, `orange`, `pink`, `red`
- `teal`, `yellow`, `gray`, `sepia`
- `cyberpunk`, `forest`, `ocean`

## 🖼️ UIコンポーネント詳細仕様

### 1. メインウィンドウ (MainWindow)

```python
class MainWindow(QMainWindow):
    """
    アプリケーションのメインウィンドウ
    """
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PhotoMap Explorer - v3.0.0")
        self.setGeometry(100, 100, 1400, 900)
        
        # Theme Manager初期化
        self.theme_controller = ThemeController()
        
        # 状態管理
        self.current_folder = None
        self.current_images = []
        self.selected_image = None
        self.maximized_state = None  # 'image', 'map', None
        
        # UI構築
        self.setup_ui()
        self.load_initial_folder()
        
    def setup_ui(self):
        """UI構築"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # ツールバー＋アドレスバー
        self.create_toolbar_area(layout)
        
        # メインスプリッター（左パネル｜右パネル）
        self.create_main_splitter(layout)
        
        # 最大化用コンテナ
        self.create_maximize_container(layout)
        
        # ステータスバー
        self.statusBar().showMessage("準備完了")
        
    def create_toolbar_area(self, layout):
        """ツールバーエリア作成"""
        # フォルダ選択ボタン
        # GIMP風アドレスバー（ui.controls使用）
        # 親フォルダボタン
        # テーマ切り替えボタン
        
    def create_main_splitter(self, layout):
        """メインスプリッター作成"""
        # 左パネル: フォルダ内容 + サムネイル + 詳細情報
        # 右パネル: 画像プレビュー + 地図表示
        
    def create_maximize_container(self, layout):
        """最大化表示用コンテナ"""
        # 画像・地図の全画面表示用
```

### 2. 左パネル構成

#### フォルダ内容パネル
```python
def create_folder_panel(self):
    """フォルダ内容表示パネル"""
    folder_group = QGroupBox("📁 フォルダ内容")
    folder_layout = QVBoxLayout(folder_group)
    
    # フォルダ内容リスト
    self.folder_list = QListWidget()
    self.folder_list.setMinimumHeight(150)
    self.folder_list.itemClicked.connect(self.on_folder_item_clicked)
    self.folder_list.itemDoubleClicked.connect(self.on_folder_item_double_clicked)
    
    folder_layout.addWidget(self.folder_list)
    return folder_group
```

#### サムネイルパネル
```python
def create_thumbnail_panel(self):
    """サムネイル表示パネル"""
    thumbnail_group = QGroupBox("🖼️ サムネイル")
    thumbnail_layout = QVBoxLayout(thumbnail_group)
    
    # サムネイルリスト（ui.thumbnail_list使用）
    from ui.thumbnail_list import create_thumbnail_list
    self.thumbnail_list = create_thumbnail_list(self.on_thumbnail_clicked)
    thumbnail_layout.addWidget(self.thumbnail_list)
    
    return thumbnail_group
```

#### 詳細情報パネル
```python
def create_status_panel(self):
    """詳細情報表示パネル"""
    status_group = QGroupBox("📋 詳細情報")
    status_layout = QVBoxLayout(status_group)
    
    self.status_info = QLabel("画像を選択すると詳細情報が表示されます")
    self.status_info.setWordWrap(True)
    self.status_info.setMinimumHeight(120)
    
    status_layout.addWidget(self.status_info)
    return status_group
```

### 3. 右パネル構成

#### 画像プレビューパネル
```python
def create_preview_panel(self):
    """画像プレビューパネル"""
    preview_group = QGroupBox("🖼️ プレビュー")
    preview_layout = QVBoxLayout(preview_group)
    
    # ヘッダー（タイトル + 最大化ボタン）
    header_layout = QHBoxLayout()
    header_layout.addWidget(QLabel("画像プレビュー"))
    header_layout.addStretch()
    
    self.maximize_btn = QPushButton("⛶")
    self.maximize_btn.setToolTip("画像を最大化表示")
    self.maximize_btn.clicked.connect(self.toggle_image_maximize)
    header_layout.addWidget(self.maximize_btn)
    
    preview_layout.addLayout(header_layout)
    
    # プレビューパネル本体
    from ui.image_preview import create_image_preview
    self.preview_panel = create_image_preview()
    preview_layout.addWidget(self.preview_panel)
    
    return preview_group
```

#### 地図パネル
```python
def create_map_panel(self):
    """地図表示パネル"""
    map_group = QGroupBox("🗺️ マップ")
    map_layout = QVBoxLayout(map_group)
    
    # ヘッダー（タイトル + 最大化ボタン）
    header_layout = QHBoxLayout()
    header_layout.addWidget(QLabel("撮影場所マップ"))
    header_layout.addStretch()
    
    self.maximize_map_btn = QPushButton("⛶")
    self.maximize_map_btn.setToolTip("マップを最大化表示")
    self.maximize_map_btn.clicked.connect(self.toggle_map_maximize)
    header_layout.addWidget(self.maximize_map_btn)
    
    map_layout.addLayout(header_layout)
    
    # マップパネル本体
    from ui.map_panel import create_map_panel
    self.map_panel = create_map_panel()
    map_layout.addWidget(self.map_panel)
    
    return map_group
```

### 4. GIMP風アドレスバー (ui/controls/)

Theme Managerを使用したGIMP風アドレスバーコンポーネント（別途詳細プロンプト参照）:

```python
# ui/controls/address_bar/
from ui.controls import create_controls

# アドレスバー作成
controls_widget, address_bar, parent_button = create_controls(
    self.on_address_entered,
    self.on_parent_folder_clicked
)
```

### 5. テーマ切り替えUI

```python
def create_theme_toggle_button(self):
    """テーマ切り替えボタン"""
    self.theme_btn = QPushButton("🌙 ダーク")
    self.theme_btn.setMaximumHeight(30)
    self.theme_btn.setMaximumWidth(80)
    self.theme_btn.setToolTip("テーマ切り替え")
    self.theme_btn.clicked.connect(self.toggle_theme)
    
def toggle_theme(self):
    """テーマ切り替え"""
    current_theme = self.theme_controller.get_current_theme_name()
    
    # テーマメニューを表示
    theme_menu = QMenu()
    for theme_name, theme_data in self.available_themes.items():
        action = QAction(theme_data.get('display_name', theme_name), self)
        action.triggered.connect(lambda checked, t=theme_name: self.switch_theme(t))
        if theme_name == current_theme:
            action.setCheckable(True)
            action.setChecked(True)
        theme_menu.addAction(action)
    
    theme_menu.exec_(self.theme_btn.mapToGlobal(self.theme_btn.rect().bottomLeft()))

def switch_theme(self, theme_name):
    """指定テーマに切り替え"""
    self.theme_controller.set_theme(theme_name)
    self.theme_controller.apply_theme_to_widget(self)
    
    # ボタンテキスト更新
    theme_data = self.available_themes.get(theme_name, {})
    display_name = theme_data.get('display_name', theme_name)
    icon = "🌙" if "dark" in theme_name.lower() else "☀️"
    self.theme_btn.setText(f"{icon} {display_name}")
```

## 📁 個別UIコンポーネント実装

### ui/thumbnail_list.py
```python
def create_thumbnail_list(on_thumbnail_clicked_callback):
    """サムネイルリスト作成"""
    class ThumbnailList(QListWidget):
        def __init__(self):
            super().__init__()
            self.setViewMode(QListWidget.IconMode)
            self.setResizeMode(QListWidget.Adjust)
            self.setGridSize(QSize(150, 150))
            self.setIconSize(QSize(128, 128))
            
        def update_thumbnails(self, image_files):
            """サムネイル更新"""
            self.clear()
            for image_file in image_files:
                item = QListWidgetItem()
                # サムネイル生成
                pixmap = self.create_thumbnail(image_file)
                item.setIcon(QIcon(pixmap))
                item.setText(os.path.basename(image_file))
                item.setData(Qt.UserRole, image_file)
                self.addItem(item)
                
        def create_thumbnail(self, image_path):
            """サムネイル画像生成"""
            # PIL/Pillowを使用してサムネイル生成
            pass
    
    thumbnail_list = ThumbnailList()
    if on_thumbnail_clicked_callback:
        thumbnail_list.itemClicked.connect(on_thumbnail_clicked_callback)
    
    return thumbnail_list
```

### ui/image_preview.py
```python
def create_image_preview():
    """画像プレビューパネル作成"""
    class ImagePreview(QLabel):
        def __init__(self):
            super().__init__()
            self.setAlignment(Qt.AlignCenter)
            self.setStyleSheet("border: 1px solid #ccc;")
            self.setText("画像を選択してください")
            self.setMinimumSize(400, 300)
            
        def display_image(self, image_path):
            """画像表示"""
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                # サイズ調整
                scaled_pixmap = pixmap.scaled(
                    self.size(), 
                    Qt.KeepAspectRatio, 
                    Qt.SmoothTransformation
                )
                self.setPixmap(scaled_pixmap)
            else:
                self.setText("画像を読み込めませんでした")
                
        def clear_preview(self):
            """プレビュークリア"""
            self.clear()
            self.setText("画像を選択してください")
    
    return ImagePreview()
```

### ui/map_panel.py
```python
def create_map_panel():
    """地図パネル作成"""
    class MapPanel(QWidget):
        def __init__(self):
            super().__init__()
            self.setup_ui()
            
        def setup_ui(self):
            layout = QVBoxLayout(self)
            
            # 地図表示（QtWebEngineViewまたはシンプルな地図表示）
            self.map_view = self.create_map_view()
            layout.addWidget(self.map_view)
            
        def create_map_view(self):
            """地図ビュー作成"""
            try:
                # QtWebEngineView使用の場合
                from PyQt5.QtWebEngineWidgets import QWebEngineView
                web_view = QWebEngineView()
                # OpenStreetMapまたはLeafletベースの地図
                return web_view
            except ImportError:
                # フォールバック: シンプルな地図表示
                return self.create_simple_map_view()
                
        def create_simple_map_view(self):
            """シンプル地図ビュー"""
            label = QLabel("地図表示エリア")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("border: 1px solid #ccc; background: #f0f0f0;")
            return label
            
        def show_location(self, latitude, longitude):
            """指定座標の地図表示"""
            # 地図の中心を指定座標に移動
            pass
            
        def clear_map(self):
            """地図クリア"""
            pass
    
    return MapPanel()
```

### ui/custom_folder_dialog.py
```python
class CustomFolderDialog(QFileDialog):
    """カスタムフォルダ選択ダイアログ"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFileMode(QFileDialog.Directory)
        self.setOption(QFileDialog.ShowDirsOnly, True)
        
    @staticmethod
    def get_folder(parent=None, caption="フォルダを選択", directory=""):
        """フォルダ選択ダイアログ表示"""
        dialog = CustomFolderDialog(parent)
        dialog.setWindowTitle(caption)
        if directory:
            dialog.setDirectory(directory)
            
        if dialog.exec_() == QFileDialog.Accepted:
            return dialog.selectedFiles()[0]
        return None
```

## 🖼️ 画像処理・EXIF読取 (logic/image_utils.py)

```python
"""画像処理とEXIF情報読取"""

from PIL import Image, ExifTags
import os
from typing import Tuple, Optional, List, Dict


def get_image_files(folder_path: str) -> List[str]:
    """フォルダ内の画像ファイル一覧取得"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
    image_files = []
    
    try:
        for file in os.listdir(folder_path):
            if os.path.splitext(file)[1].lower() in image_extensions:
                image_files.append(os.path.join(folder_path, file))
    except (OSError, PermissionError):
        pass
        
    return sorted(image_files)


def extract_gps_info(image_path: str) -> Optional[Tuple[float, float]]:
    """画像からGPS情報を抽出"""
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            
            if exif is None:
                return None
                
            gps_info = exif.get(34853)  # GPS IFD
            if not gps_info:
                return None
                
            # GPS座標の計算
            latitude = convert_gps_coordinate(gps_info.get(2), gps_info.get(1))
            longitude = convert_gps_coordinate(gps_info.get(4), gps_info.get(3))
            
            if latitude is not None and longitude is not None:
                return latitude, longitude
                
    except Exception as e:
        print(f"GPS情報読取エラー: {e}")
        
    return None


def convert_gps_coordinate(coord_data, ref) -> Optional[float]:
    """GPS座標データを十進数に変換"""
    if not coord_data or not ref:
        return None
        
    try:
        degrees = float(coord_data[0])
        minutes = float(coord_data[1])
        seconds = float(coord_data[2])
        
        coordinate = degrees + (minutes / 60) + (seconds / 3600)
        
        if ref in ['S', 'W']:
            coordinate = -coordinate
            
        return coordinate
    except (IndexError, TypeError, ValueError):
        return None


def get_image_info(image_path: str) -> Dict[str, any]:
    """画像の詳細情報取得"""
    info = {
        'path': image_path,
        'filename': os.path.basename(image_path),
        'size': 0,
        'dimensions': None,
        'creation_date': None,
        'gps_coordinates': None,
        'camera_info': {},
    }
    
    try:
        # ファイルサイズ
        info['size'] = os.path.getsize(image_path)
        
        with Image.open(image_path) as img:
            # 画像サイズ
            info['dimensions'] = img.size
            
            # EXIF情報
            exif = img.getexif()
            if exif:
                # 撮影日時
                datetime_tag = 36867  # DateTimeOriginal
                if datetime_tag in exif:
                    info['creation_date'] = exif[datetime_tag]
                
                # カメラ情報
                camera_make = exif.get(271)  # Make
                camera_model = exif.get(272)  # Model
                if camera_make or camera_model:
                    info['camera_info'] = {
                        'make': camera_make,
                        'model': camera_model
                    }
                
                # GPS情報
                info['gps_coordinates'] = extract_gps_info(image_path)
                
    except Exception as e:
        print(f"画像情報読取エラー: {e}")
        
    return info
```

## 🔧 イベント処理・機能実装

### フォルダ選択・ナビゲーション
```python
def on_folder_selected(self):
    """フォルダ選択ダイアログ"""
    from ui.custom_folder_dialog import CustomFolderDialog
    
    folder = CustomFolderDialog.get_folder(
        self, 
        "写真フォルダを選択", 
        self.current_folder or ""
    )
    
    if folder:
        self.load_folder(folder)

def load_folder(self, folder_path):
    """フォルダ読み込み"""
    try:
        self.current_folder = folder_path
        
        # アドレスバー更新
        if self.address_bar:
            self.address_bar.setText(folder_path)
            
        # フォルダ内容更新
        self.update_folder_contents(folder_path)
        
        # 画像ファイル取得・サムネイル更新
        from logic.image_utils import get_image_files
        self.current_images = get_image_files(folder_path)
        self.update_thumbnails(self.current_images)
        
        # ステータス更新
        self.statusBar().showMessage(f"フォルダ読み込み完了: {len(self.current_images)}件の画像")
        
    except Exception as e:
        self.statusBar().showMessage(f"フォルダ読み込みエラー: {e}")

def update_folder_contents(self, folder_path):
    """フォルダ内容リスト更新"""
    self.folder_list.clear()
    
    try:
        # 親フォルダ項目
        parent_dir = os.path.dirname(folder_path)
        if parent_dir != folder_path:
            parent_item = QListWidgetItem("📁 ..")
            parent_item.setData(Qt.UserRole, parent_dir)
            self.folder_list.addItem(parent_item)
            
        # サブフォルダ
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folder_item = QListWidgetItem(f"📁 {item}")
                folder_item.setData(Qt.UserRole, item_path)
                self.folder_list.addItem(folder_item)
                
    except (OSError, PermissionError) as e:
        self.statusBar().showMessage(f"フォルダアクセスエラー: {e}")

def on_folder_item_double_clicked(self, item):
    """フォルダ項目ダブルクリック"""
    folder_path = item.data(Qt.UserRole)
    if folder_path:
        self.load_folder(folder_path)
```

### 画像選択・プレビュー
```python
def on_thumbnail_clicked(self, item):
    """サムネイルクリック"""
    image_path = item.data(Qt.UserRole)
    if image_path:
        self.selected_image = image_path
        self.display_image_preview(image_path)
        self.display_image_location(image_path)
        self.update_image_details(image_path)

def display_image_preview(self, image_path):
    """画像プレビュー表示"""
    if self.preview_panel:
        self.preview_panel.display_image(image_path)

def display_image_location(self, image_path):
    """画像撮影場所の地図表示"""
    from logic.image_utils import extract_gps_info
    
    gps_coords = extract_gps_info(image_path)
    if gps_coords and self.map_panel:
        latitude, longitude = gps_coords
        self.map_panel.show_location(latitude, longitude)
        self.statusBar().showMessage(f"撮影場所: {latitude:.6f}, {longitude:.6f}")
    else:
        if self.map_panel:
            self.map_panel.clear_map()
        self.statusBar().showMessage("GPS情報なし")

def update_image_details(self, image_path):
    """画像詳細情報更新"""
    from logic.image_utils import get_image_info
    
    info = get_image_info(image_path)
    
    details = [
        f"ファイル名: {info['filename']}",
        f"サイズ: {info['size']:,} bytes",
    ]
    
    if info['dimensions']:
        details.append(f"解像度: {info['dimensions'][0]} x {info['dimensions'][1]}")
        
    if info['creation_date']:
        details.append(f"撮影日時: {info['creation_date']}")
        
    if info['camera_info'].get('make') or info['camera_info'].get('model'):
        camera = f"{info['camera_info'].get('make', '')} {info['camera_info'].get('model', '')}".strip()
        details.append(f"カメラ: {camera}")
        
    if info['gps_coordinates']:
        lat, lon = info['gps_coordinates']
        details.append(f"GPS: {lat:.6f}, {lon:.6f}")
        
    self.status_info.setText("\n".join(details))
```

### パネル最大化機能
```python
def toggle_image_maximize(self):
    """画像パネル最大化切り替え"""
    if self.maximized_state == 'image':
        self.restore_normal_view()
    else:
        self.maximize_image_panel()

def toggle_map_maximize(self):
    """地図パネル最大化切り替え"""
    if self.maximized_state == 'map':
        self.restore_normal_view()
    else:
        self.maximize_map_panel()

def maximize_image_panel(self):
    """画像パネル最大化"""
    self.maximized_state = 'image'
    
    # 通常ビューを非表示
    self.main_splitter.hide()
    
    # 最大化コンテナに画像パネルを移動
    self.maximize_container.layout().addWidget(self.preview_panel)
    self.maximize_container.show()
    
    # 復元ボタン表示
    self.show_restore_button()

def maximize_map_panel(self):
    """地図パネル最大化"""
    self.maximized_state = 'map'
    
    # 通常ビューを非表示
    self.main_splitter.hide()
    
    # 最大化コンテナに地図パネルを移動
    self.maximize_container.layout().addWidget(self.map_panel)
    self.maximize_container.show()
    
    # 復元ボタン表示
    self.show_restore_button()

def restore_normal_view(self):
    """通常ビューに復元"""
    if self.maximized_state == 'image':
        # 画像パネルを元の位置に戻す
        self.restore_panel_to_splitter(self.preview_panel)
    elif self.maximized_state == 'map':
        # 地図パネルを元の位置に戻す
        self.restore_panel_to_splitter(self.map_panel)
        
    self.maximized_state = None
    self.maximize_container.hide()
    self.main_splitter.show()
```

## 🚀 実装順序とガイドライン

### Phase 1: 基盤構築
1. **Theme Manager統合**
   - ライブラリインストール・設定
   - 基本的なテーマ切り替え機能

2. **メインウィンドウ構造**
   - 基本レイアウト構築
   - スプリッター設定

### Phase 2: コアUI実装
1. **GIMP風アドレスバー**（別プロンプト参照）
2. **左パネル**: フォルダ・サムネイル・詳細情報
3. **右パネル**: プレビュー・地図表示

### Phase 3: 機能実装
1. **画像処理**: EXIF・GPS読取
2. **ナビゲーション**: フォルダ移動・履歴
3. **最大化機能**: パネル切り替え

### Phase 4: テーマ・UI完成
1. **16テーマ対応**: Theme Manager活用
2. **UI/UX調整**: アニメーション・レスポンシブ
3. **エラーハンドリング**: 例外処理・ログ

## 📋 必要な依存関係

```txt
# requirements.txt
PyQt5>=5.15.0
Pillow>=8.0.0
exifread>=2.3.0

# Theme Manager (手動インストール)
git+https://github.com/scottlz0310/Theme-Manager.git
```

## 🎯 実装時の重要なポイント

### Theme Manager活用
- 16種類のテーマを適切に活用
- 動的テーマ切り替えの実装
- コンポーネント別のテーマ適用

### パフォーマンス
- 大量画像のサムネイル生成最適化
- 非同期処理での応答性確保
- メモリ効率的な画像表示

### エラーハンドリング
- 画像読み込みエラー対応
- GPS情報なしの場合の処理
- ファイルアクセス権限エラー

### クロスプラットフォーム
- Windows/macOS/Linux対応
- パス処理の統一
- フォント・アイコンの互換性

この仕様に従って、新しいTheme Managerライブラリを活用した美しく機能的なPhotoMap Explorerを実装してください。16種類のテーマサポートにより、ユーザーの好みに応じたカスタマイズ可能な写真管理アプリケーションを提供できます。
