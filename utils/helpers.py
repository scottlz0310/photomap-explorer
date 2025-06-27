# Helper functions for PhotoMap Explorer
import os
from typing import List, Optional, Tuple
from PyQt5.QtCore import QSize
from utils.constants import SUPPORTED_IMAGE_EXTENSIONS, THUMBNAIL_SIZES
from utils.exceptions import DirectoryNotFoundError, InvalidImageFormatError

def is_image_file(file_path: str) -> bool:
    """
    ファイルが画像ファイルかどうかチェックする
    
    Args:
        file_path: ファイルパス
        
    Returns:
        画像ファイルの場合True
    """
    if not file_path:
        return False
    
    _, ext = os.path.splitext(file_path.lower())
    return ext in SUPPORTED_IMAGE_EXTENSIONS

def validate_directory(directory_path: str) -> bool:
    """
    ディレクトリが存在し、アクセス可能かチェックする
    
    Args:
        directory_path: ディレクトリパス
        
    Returns:
        有効なディレクトリの場合True
        
    Raises:
        DirectoryNotFoundError: ディレクトリが存在しない場合
    """
    if not directory_path:
        return False
        
    if not os.path.exists(directory_path):
        raise DirectoryNotFoundError(f"Directory not found: {directory_path}")
        
    if not os.path.isdir(directory_path):
        return False
        
    if not os.access(directory_path, os.R_OK):
        return False
        
    return True

def get_thumbnail_size_config(size_label: str) -> Tuple[QSize, int]:
    """
    サムネイルサイズの設定を取得する
    
    Args:
        size_label: サイズラベル ("small", "medium", "large")
        
    Returns:
        (QSize, panel_width) のタプル
    """
    config = THUMBNAIL_SIZES.get(size_label, THUMBNAIL_SIZES["medium"])
    size = QSize(config["width"], config["height"])
    panel_width = config["panel_width"]
    return size, panel_width

def normalize_path(path: str) -> str:
    """
    パスを正規化する
    
    Args:
        path: ファイル/ディレクトリパス
        
    Returns:
        正規化されたパス
    """
    if not path:
        return ""
    
    return os.path.normcase(os.path.normpath(path))

def get_file_extension(file_path: str) -> str:
    """
    ファイルの拡張子を取得する
    
    Args:
        file_path: ファイルパス
        
    Returns:
        拡張子（小文字、ドット付き）
    """
    if not file_path:
        return ""
    
    _, ext = os.path.splitext(file_path.lower())
    return ext

def validate_gps_coordinates(latitude: float, longitude: float) -> bool:
    """
    GPS座標が有効範囲内かチェックする
    
    Args:
        latitude: 緯度
        longitude: 経度
        
    Returns:
        有効な座標の場合True
    """
    if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
        return False
        
    # 緯度の範囲チェック (-90 ≤ lat ≤ 90)
    if latitude < -90.0 or latitude > 90.0:
        return False
        
    # 経度の範囲チェック (-180 ≤ lon ≤ 180)  
    if longitude < -180.0 or longitude > 180.0:
        return False
        
    # (0, 0) は無効な座標とみなす
    if latitude == 0.0 and longitude == 0.0:
        return False
        
    return True

def format_file_size(size_bytes: int) -> str:
    """
    ファイルサイズを人間が読みやすい形式でフォーマットする
    
    Args:
        size_bytes: バイト数
        
    Returns:
        フォーマットされたサイズ文字列
    """
    if size_bytes == 0:
        return "0 B"
        
    size_units = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    size = float(size_bytes)
    
    while size >= 1024.0 and i < len(size_units) - 1:
        size /= 1024.0
        i += 1
        
    return f"{size:.1f} {size_units[i]}"

def safe_get_attr(obj, attr_name: str, default=None):
    """
    安全に属性を取得する
    
    Args:
        obj: オブジェクト
        attr_name: 属性名
        default: デフォルト値
        
    Returns:
        属性値またはデフォルト値
    """
    try:
        return getattr(obj, attr_name, default)
    except (AttributeError, TypeError):
        return default
