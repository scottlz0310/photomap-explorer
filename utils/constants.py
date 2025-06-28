# Constants for PhotoMap Explorer

# アプリケーション情報
APP_NAME = "PhotoMap Explorer"
APP_VERSION = "2.0.0"
APP_AUTHOR = "scottlz0310"

# Clean Architecture用の定数
APPLICATION_NAME = APP_NAME
APPLICATION_VERSION = APP_VERSION

# ファイル関連定数
SUPPORTED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
MAP_OUTPUT_FILE = "map.html"

# UI関連定数
DEFAULT_WINDOW_WIDTH = 1400
DEFAULT_WINDOW_HEIGHT = 900
DEFAULT_THUMBNAIL_SIZE = "medium"

# サムネイルサイズ設定
THUMBNAIL_SIZES = {
    "small": {"width": 64, "height": 64, "panel_width": 124},
    "medium": {"width": 128, "height": 128, "panel_width": 188}, 
    "large": {"width": 192, "height": 192, "panel_width": 252}
}

# スプリッター初期サイズ
DEFAULT_SPLITTER_SIZES = [700, 200, 700]
RIGHT_SPLITTER_SIZES = [5000, 5000]

# 地図関連定数
DEFAULT_MAP_ZOOM = 15
DEFAULT_LATITUDE = 0.0
DEFAULT_LONGITUDE = 0.0
MAP_MARKER_TOOLTIP = "画像の位置"

# GPS座標の妥当性チェック用定数
MIN_LATITUDE = -90.0
MAX_LATITUDE = 90.0
MIN_LONGITUDE = -180.0
MAX_LONGITUDE = 180.0

# メッセージ表示時間（ミリ秒）
STATUS_MESSAGE_TIMEOUT = 3000
LONG_STATUS_MESSAGE_TIMEOUT = 10000

# ウィンドウ状態
WINDOW_STATE_NORMAL = "normal"
WINDOW_STATE_MAXIMIZED_IMAGE = "maximized_image"
WINDOW_STATE_MAXIMIZED_MAP = "maximized_map"
