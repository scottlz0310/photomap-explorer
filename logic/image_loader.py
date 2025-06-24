import os
from PyQt5.QtGui import QPixmap

def find_images_in_directory(directory):
    """
    指定されたディレクトリ内の画像ファイルを検索します。
    ファイルの場合、そのファイルの属するディレクトリを使用します。

    Args:
        directory (str): 対象のディレクトリまたはファイルパス。

    Returns:
        list: 画像ファイルのパスリスト。
    """
    try:
        # ファイルの場合は、その親ディレクトリを取得
        if not os.path.isdir(directory):
            directory = os.path.dirname(directory)
        
        valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
        return [
            os.path.join(directory, f)
            for f in os.listdir(directory)
            if f.lower().endswith(valid_extensions)
        ]
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return []  # エラー時は空リストを返します

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
