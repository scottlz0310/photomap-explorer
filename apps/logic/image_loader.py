# apps/logic/image_loader.py

import os
from PyQt5.QtGui import QPixmap, QImageReader

# サポートする画像ファイル拡張子
SUPPORTED_EXTS = ('.jpg', '.jpeg', '.png', '.bmp', '.gif')


def find_images_in_directory(directory: str) -> list:
    """
    指定されたディレクトリ配下の画像ファイルを抽出して、フルパスのリストを返す。

    :param directory: 対象となるディレクトリのパス
    :return: 画像ファイルの絶対パス一覧（拡張子フィルタ済）
    """
    if not os.path.isdir(directory):
        return []

    files = sorted(os.listdir(directory))  # アルファベット順で統一表示
    image_files = [
        os.path.join(directory, f)
        for f in files
        if os.path.splitext(f)[1].lower() in SUPPORTED_EXTS
    ]
    return image_files


def load_pixmap(path: str, max_size=(256, 256)) -> QPixmap:
    """
    指定された画像ファイルを読み込んで、サムネイル用に縮小した QPixmap を返す。

    :param path: 画像ファイルの絶対パス
    :param max_size: 最大サイズ（幅, 高さ）タプル
    :return: QPixmap オブジェクト（読み込み失敗時は Null pixmap）
    """
    pixmap = QPixmap(path)
    if pixmap.isNull():
        return QPixmap()  # 読み込めない画像は空で返す
    return pixmap.scaled(*max_size, aspectRatioMode=1, transformMode=1)  # Qt.KeepAspectRatio, SmoothTransformation
