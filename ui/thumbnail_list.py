from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize, Qt
import os
from utils.debug_logger import debug, info, warning, error, verbose

def load_pixmap(image_path):
    """画像パスからQPixmapを生成して返すユーティリティ関数"""
    return QPixmap(image_path)

def create_thumbnail_list(thumbnail_clicked_callback=None):
    """サムネイル一覧のウィジェットを作成して初期化する関数"""
    thumbnail_list = QListWidget()
    thumbnail_list.setIconSize(QSize(128, 128))  # サムネイルサイズを設定
    thumbnail_list.setViewMode(QListWidget.IconMode)  # アイコン表示モード
    thumbnail_list.setResizeMode(QListWidget.Adjust)  # 複数列表示対応
    thumbnail_list.setMovement(QListWidget.Static)
    thumbnail_list.setSpacing(8)  # アイコン間隔を調整
    thumbnail_list.setWordWrap(True)  # テキスト折り返し有効
    thumbnail_list.setUniformItemSizes(True)  # パフォーマンス向上
    
    # コールバック接続は外部で行うように変更（後からset_event_handlersで設定）
    # これにより、適切なイベントハンドラーの上書きが可能になる
    info("🔍 create_thumbnail_list: コールバック接続を外部に委譲")

    return thumbnail_list

def add_thumbnail(thumbnail_list, image_path):
    """サムネイルをサムネイル一覧に追加"""
    try:
        icon = QIcon(image_path)  # 画像をアイコンとして読み込み
        # ファイル名のみを表示（プラットフォーム対応）
        filename = os.path.basename(image_path)
        item = QListWidgetItem(icon, filename)
        # フルパスをQt.UserRoleで保存
        item.setData(Qt.UserRole, image_path)
        thumbnail_list.addItem(item)
        return True
    except Exception as e:
        print(f"サムネイル追加エラー: {e}")
        return False

def set_thumbnail_size(thumbnail_list, size_label):
    """サムネイルサイズを 'small', 'medium', 'large' で切り替え"""
    size_map = {
        'small': QSize(64, 64),
        'medium': QSize(128, 128),
        'large': QSize(192, 192)
    }
    size = size_map.get(size_label, QSize(128, 128))
    thumbnail_list.setIconSize(size)
    # サムネイルリストを再描画
    thumbnail_list.update()
