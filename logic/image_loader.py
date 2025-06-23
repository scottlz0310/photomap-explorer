import os
from PyQt5.QtGui import QPixmap

def find_images_in_directory(directory):
    """
    指定されたディレクトリ内の画像ファイルを検索します。

    Args:
        directory (str): 対象のディレクトリパス。

    Returns:
        list: 画像ファイルのパスリスト。
    """
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.lower().endswith(valid_extensions)
    ]

def load_pixmap(image_path):
    """
    画像ファイルを読み込み、QPixmap形式で返します。

    Args:
        image_path (str): 画像ファイルのパス。

    Returns:
        QPixmap: 読み込まれた画像のピクスマップ。
    """
    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        print(f"画像の読み込みに失敗しました: {image_path}")
    return pixmap
