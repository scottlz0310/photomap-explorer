"""
Phase 2の動作確認テスト

新しく作成したインフラ層とドメイン層の基本的な動作をテストします。
"""

import asyncio
import sys
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 絶対インポートで修正
try:
    from infrastructure.exif_reader import ExifReader
    from infrastructure.file_system import FileSystemService
    from infrastructure.map_generator import MapGenerator
    from infrastructure.repositories import FileSystemPhotoRepository
    from domain.models.photo import Photo, GPSCoordinates
    from domain.models.photo_collection import PhotoCollection
    from app.application import initialize_application, shutdown_application
    from utils.constants import APPLICATION_NAME, APPLICATION_VERSION
    
    IMPORTS_OK = True
except ImportError as e:
    print(f"⚠️  インポートエラー: {e}")
    print("📝 これは相対インポートの問題です。個別テストで動作確認します。")
    IMPORTS_OK = False


async def test_exif_reader():
    """EXIF読み取りテスト"""
    print("=== EXIF読み取りテスト ===")
    
    exif_reader = ExifReader()
    
    # テスト用画像ファイルを探す
    test_dirs = [
        Path("."),
        Path("assets"),
        Path("docs")
    ]
    
    test_files = []
    for test_dir in test_dirs:
        if test_dir.exists():
            for ext in ['.jpg', '.jpeg', '.png', '.tiff']:
                test_files.extend(list(test_dir.glob(f"*{ext}")))
                test_files.extend(list(test_dir.glob(f"*{ext.upper()}")))
    
    if not test_files:
        print("  ❌ テスト用画像ファイルが見つかりません")
        return False
    
    success_count = 0
    for file_path in test_files[:3]:  # 最初の3ファイルのみテスト
        print(f"  📁 テスト: {file_path.name}")
        
        try:
            # メタデータ抽出
            metadata = exif_reader.extract_metadata(file_path)
            if metadata:
                print(f"    ✅ メタデータ: {metadata.file_size} bytes")
                success_count += 1
            else:
                print(f"    ⚠️  メタデータ抽出失敗")
            
            # GPS座標抽出
            gps_coords = exif_reader.extract_gps_coordinates(file_path)
            if gps_coords:
                print(f"    ✅ GPS座標: {gps_coords}")
            else:
                print(f"    ℹ️  GPS情報なし")
            
            # 撮影日時抽出
            taken_date = exif_reader.extract_taken_date(file_path)
            if taken_date:
                print(f"    ✅ 撮影日時: {taken_date}")
            else:
                print(f"    ℹ️  撮影日時なし")
                
        except Exception as e:
            print(f"    ❌ エラー: {e}")
    
    print(f"  結果: {success_count}/{len(test_files[:3])} ファイル処理成功")
    return success_count > 0


async def test_file_system():
    """ファイルシステムテスト"""
    print("\n=== ファイルシステムテスト ===")
    
    fs_service = FileSystemService()
    
    # 現在のディレクトリで画像ファイルを検索
    current_dir = Path(".")
    
    try:
        images = await fs_service.find_images_in_directory(current_dir, recursive=True)
        print(f"  ✅ 見つかった画像: {len(images)} 個")
        
        for i, image_path in enumerate(images[:5]):  # 最初の5個のみ表示
            print(f"    {i+1}. {image_path.name}")
        
        if len(images) > 5:
            print(f"    ... その他 {len(images) - 5} 個")
        
        # 画像数をカウント
        count = await fs_service.count_images_in_directory(current_dir, recursive=True)
        print(f"  ✅ 画像カウント: {count} 個")
        
        return len(images) > 0
        
    except Exception as e:
        print(f"  ❌ エラー: {e}")
        return False


async def test_photo_repository():
    """写真リポジトリテスト"""
    print("\n=== 写真リポジトリテスト ===")
    
    repo = FileSystemPhotoRepository()
    
    try:
        # 現在のディレクトリで写真を検索
        current_dir = Path(".")
        photos = await repo.find_by_directory(current_dir, recursive=True)
        
        print(f"  ✅ 読み込んだ写真: {len(photos)} 個")
        
        gps_photos = [p for p in photos if p.has_gps_data]
        print(f"  ✅ GPS情報付き写真: {len(gps_photos)} 個")
        
        # キャッシュサイズを確認
        cache_size = repo.get_cache_size()
        print(f"  ✅ キャッシュサイズ: {cache_size} 個")
        
        # 最初の写真の詳細を表示
        if photos:
            first_photo = photos[0]
            print(f"  📸 サンプル写真:")
            print(f"    ファイル名: {first_photo.file_name}")
            print(f"    GPS情報: {'あり' if first_photo.has_gps_data else 'なし'}")
            print(f"    撮影日時: {first_photo.taken_date or '不明'}")
        
        return len(photos) > 0
        
    except Exception as e:
        print(f"  ❌ エラー: {e}")
        return False


async def test_photo_models():
    """写真モデルテスト"""
    print("\n=== 写真モデルテスト ===")
    
    try:
        # GPS座標のテスト
        try:
            gps_coords = GPSCoordinates(latitude=35.6762, longitude=139.6503)  # 東京駅
            print(f"  ✅ GPS座標作成: {gps_coords}")
            
            # 距離計算のテスト
            other_coords = GPSCoordinates(latitude=35.6586, longitude=139.7454)  # 東京タワー
            distance = gps_coords.distance_to(other_coords)
            print(f"  ✅ 距離計算: {distance:.2f} km")
            
        except Exception as e:
            print(f"  ❌ GPS座標テストエラー: {e}")
            return False
        
        # 写真コレクションのテスト
        try:
            collection = PhotoCollection(name="テストコレクション")
            print(f"  ✅ コレクション作成: {collection.name}")
            print(f"  ✅ 写真数: {len(collection)} 個")
            
            # 統計情報のテスト
            stats = collection.get_statistics()
            print(f"  ✅ 統計情報: {stats['total_photos']} 写真")
            
        except Exception as e:
            print(f"  ❌ コレクションテストエラー: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ モデルテストエラー: {e}")
        return False


async def test_application_lifecycle():
    """アプリケーションライフサイクルテスト"""
    print("\n=== アプリケーションライフサイクルテスト ===")
    
    try:
        # アプリケーション初期化
        app = initialize_application()
        print(f"  ✅ アプリケーション初期化成功")
        print(f"  ✅ アプリケーション名: {APPLICATION_NAME}")
        print(f"  ✅ バージョン: {APPLICATION_VERSION}")
        
        # 設定取得
        config = app.get_config()
        print(f"  ✅ 設定読み込み: 環境={config.environment.value}")
        
        # ロガー取得
        logger = app.get_logger()
        logger.info("テストログメッセージ")
        print(f"  ✅ ロガー動作確認")
        
        # アプリケーション終了
        shutdown_application()
        print(f"  ✅ アプリケーション終了成功")
        
        return True
        
    except Exception as e:
        print(f"  ❌ アプリケーションテストエラー: {e}")
        return False


async def main():
    """メインテスト関数"""
    print(f"🚀 {APPLICATION_NAME} Phase 2 動作確認テスト")
    print(f"📅 実行日時: {Path(__file__).stat().st_mtime}")
    print("=" * 50)
    
    test_results = []
    
    # 各テストを実行
    test_results.append(("EXIF読み取り", await test_exif_reader()))
    test_results.append(("ファイルシステム", await test_file_system()))
    test_results.append(("写真リポジトリ", await test_photo_repository()))
    test_results.append(("写真モデル", await test_photo_models()))
    test_results.append(("アプリケーション", await test_application_lifecycle()))
    
    # 結果サマリー
    print("\n" + "=" * 50)
    print("📊 テスト結果サマリー")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name:<20}: {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n🎯 総合結果: {passed} 成功, {failed} 失敗")
    
    if failed == 0:
        print("🎉 すべてのテストが成功しました！")
        print("✅ Phase 2の新しいアーキテクチャは正常に動作しています。")
    else:
        print("⚠️  一部のテストが失敗しました。")
        print("ℹ️  これは開発段階では正常です。")
    
    print("\n💡 次のステップ:")
    print("  - Phase 3: プレゼンテーション層のリファクタリング")
    print("  - 既存UIコードとの統合")
    print("  - 新機能の追加")


if __name__ == "__main__":
    asyncio.run(main())
