# Custom exceptions for PhotoMap Explorer

class PhotoMapExplorerError(Exception):
    """PhotoMap Explorer のベース例外クラス"""
    pass

class ImageError(PhotoMapExplorerError):
    """画像関連のエラー"""
    pass

class ImageNotFoundError(ImageError):
    """画像ファイルが見つからない場合のエラー"""
    pass

class ImageLoadError(ImageError):
    """画像の読み込みに失敗した場合のエラー"""
    pass

class InvalidImageFormatError(ImageError):
    """サポートされていない画像形式の場合のエラー"""
    pass

class GPSError(PhotoMapExplorerError):
    """GPS関連のエラー"""
    pass

class GPSDataNotFoundError(GPSError):
    """GPS情報が見つからない場合のエラー"""
    pass

class InvalidGPSDataError(GPSError):
    """GPS情報が無効な場合のエラー"""
    pass

class MapError(PhotoMapExplorerError):
    """地図関連のエラー"""
    pass

class MapGenerationError(MapError):
    """地図生成に失敗した場合のエラー"""
    pass

class FileSystemError(PhotoMapExplorerError):
    """ファイルシステム関連のエラー"""
    pass

class DirectoryNotFoundError(FileSystemError):
    """ディレクトリが見つからない場合のエラー"""
    pass

class DirectoryAccessError(FileSystemError):
    """ディレクトリアクセスが拒否された場合のエラー"""
    pass

class ConfigurationError(PhotoMapExplorerError):
    """設定関連のエラー"""
    pass

class InvalidConfigurationError(ConfigurationError):
    """設定値が無効な場合のエラー"""
    pass

class InfrastructureError(PhotoMapExplorerError):
    """インフラストラクチャ層のエラー"""
    pass

class RepositoryError(PhotoMapExplorerError):
    """リポジトリ層のエラー"""
    pass

class DomainError(PhotoMapExplorerError):
    """ドメイン層のエラー"""
    pass

class ValidationError(DomainError):
    """バリデーションエラー"""
    pass

class ApplicationError(PhotoMapExplorerError):
    """アプリケーション層のエラー"""
    pass
