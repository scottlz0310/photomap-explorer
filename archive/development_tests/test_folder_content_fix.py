#!/usr/bin/env python3
"""
フォルダ内容表示問題の修正テスト

新UIでフォルダ内容が表示されない問題を調査・修正します。
"""

import os
import sys
from pathlib import Path

# 絶対パスで親ディレクトリを追加
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

def test_folder_content_logic():
    """フォルダ内容表示ロジックのテスト"""
    print("=== フォルダ内容表示ロジックテスト ===")
    
    # テスト用フォルダパス
    test_folder = os.path.expanduser("~")
    print(f"テストフォルダ: {test_folder}")
    
    try:
        folder = Path(test_folder)
        
        # フォルダとファイルを取得
        items = []
        
        # 親フォルダへのリンク（ルートでない場合）
        if folder.parent != folder:
            print(f"親フォルダ: {folder.parent}")
            items.append(("📁 .. (親フォルダ)", str(folder.parent), 0))
        
        # フォルダとファイルを取得
        for item_path in folder.iterdir():
            if item_path.is_dir():
                # フォルダ
                items.append((f"📁 {item_path.name}", str(item_path), 0))
            elif item_path.is_file():
                # ファイル（画像ファイルを優先表示）
                file_ext = item_path.suffix.lower()
                if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                    items.append((f"🖼️ {item_path.name}", str(item_path), 1))
                else:
                    items.append((f"📄 {item_path.name}", str(item_path), 2))
        
        # ソートして表示（フォルダ→画像→その他ファイル）
        items.sort(key=lambda x: (x[2], x[0]))
        
        print(f"取得項目数: {len(items)}")
        for i, (name, path, type_id) in enumerate(items[:10]):  # 最初の10項目のみ表示
            print(f"  {i+1}: {name} -> {path}")
        
        if len(items) > 10:
            print(f"  ... 他{len(items)-10}項目")
        
        # ステータス更新情報
        folder_count = len([i for _, _, t in items if t == 0])
        image_count = len([i for _, _, t in items if t == 1])
        other_count = len([i for _, _, t in items if t == 2])
        
        print(f"📁 フォルダ: {folder_count}, 🖼️ 画像: {image_count}, 📄 その他: {other_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ フォルダ内容取得エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_image_discovery():
    """画像発見ロジックのテスト"""
    print("\n=== 画像発見ロジックテスト ===")
    
    # テスト用フォルダパス
    test_folders = [
        os.path.join(os.path.expanduser("~"), "Pictures"),
        os.path.join(os.path.expanduser("~"), "Desktop"),
        os.path.expanduser("~")
    ]
    
    for test_folder in test_folders:
        if not os.path.exists(test_folder):
            continue
            
        print(f"\nテストフォルダ: {test_folder}")
        
        try:
            # 画像ファイル検索
            image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
            image_files = []
            
            folder = Path(test_folder)
            for file_path in folder.iterdir():
                if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                    image_files.append(str(file_path))
            
            print(f"発見画像数: {len(image_files)}")
            for i, img in enumerate(image_files[:5]):  # 最初の5枚のみ表示
                print(f"  {i+1}: {Path(img).name}")
            
            if len(image_files) > 5:
                print(f"  ... 他{len(image_files)-5}枚")
                
            return True
            
        except Exception as e:
            print(f"❌ 画像発見エラー: {e}")
            continue
    
    return False

def analyze_ui_imports():
    """UI関連のインポートをテスト"""
    print("\n=== UI関連インポートテスト ===")
    
    # サムネイルリストのインポートテスト
    try:
        from ui.thumbnail_list import create_thumbnail_list
        print("✅ create_thumbnail_list インポート成功")
    except Exception as e:
        print(f"❌ create_thumbnail_list インポートエラー: {e}")
    
    # 画像プレビューのインポートテスト
    try:
        from ui.image_preview import create_image_preview
        print("✅ create_image_preview インポート成功")
    except Exception as e:
        print(f"❌ create_image_preview インポートエラー: {e}")
    
    # マップパネルのインポートテスト
    try:
        from ui.map_panel import create_map_panel
        print("✅ create_map_panel インポート成功")
    except Exception as e:
        print(f"❌ create_map_panel インポートエラー: {e}")
    
    # 画像ユーティリティのインポートテスト
    try:
        from logic.image_utils import extract_gps_info
        print("✅ extract_gps_info インポート成功")
    except Exception as e:
        print(f"❌ extract_gps_info インポートエラー: {e}")

def test_functional_ui_creation():
    """機能UIの作成テスト（PyQt5なしでロジック部分のみ）"""
    print("\n=== 機能UI作成テスト（ロジック部分） ===")
    
    try:
        # モッククラスでUIロジックをテスト
        class MockFunctionalUI:
            def __init__(self):
                self.current_folder = None
                self.current_images = []
                self.selected_image = None
                
            def _update_folder_content(self, folder_path):
                """フォルダ内容を更新表示（モック版）"""
                try:
                    if not folder_path or not os.path.exists(folder_path):
                        print("❌ 無効なフォルダパス")
                        return False
                    
                    folder = Path(folder_path)
                    
                    # 親フォルダへのリンク（ルートでない場合）
                    items = []
                    if folder.parent != folder:
                        items.append(("📁 .. (親フォルダ)", str(folder.parent), 0))
                    
                    # フォルダとファイルを取得
                    for item_path in folder.iterdir():
                        if item_path.is_dir():
                            # フォルダ
                            items.append((f"📁 {item_path.name}", str(item_path), 0))
                        elif item_path.is_file():
                            # ファイル（画像ファイルを優先表示）
                            file_ext = item_path.suffix.lower()
                            if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                                items.append((f"🖼️ {item_path.name}", str(item_path), 1))
                            else:
                                items.append((f"📄 {item_path.name}", str(item_path), 2))
                    
                    # ソートして追加（フォルダ→画像→その他ファイル）
                    items.sort(key=lambda x: (x[2], x[0]))
                    
                    # ステータス更新
                    folder_count = len([name for name, _, t in items if t == 0])
                    image_count = len([name for name, _, t in items if t == 1])
                    other_count = len([name for name, _, t in items if t == 2])
                    
                    print(f"✅ フォルダ内容更新成功: フォルダ{folder_count}, 画像{image_count}, その他{other_count}")
                    
                    return True
                    
                except Exception as e:
                    print(f"❌ フォルダ内容更新エラー: {e}")
                    return False
            
            def _load_folder(self, folder_path):
                """フォルダ読み込み（モック版）"""
                try:
                    self.current_folder = folder_path
                    
                    # フォルダ内容表示を更新
                    content_success = self._update_folder_content(folder_path)
                    
                    # 画像ファイル検索
                    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}
                    image_files = []
                    
                    folder = Path(folder_path)
                    for file_path in folder.iterdir():
                        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
                            image_files.append(str(file_path))
                    
                    self.current_images = image_files
                    
                    print(f"✅ フォルダ読み込み成功: {len(image_files)}枚の画像")
                    
                    return content_success and True
                    
                except Exception as e:
                    print(f"❌ フォルダ読み込みエラー: {e}")
                    return False
        
        # テスト実行
        mock_ui = MockFunctionalUI()
        
        # テスト用フォルダでテスト
        test_folder = os.path.expanduser("~")
        result = mock_ui._load_folder(test_folder)
        
        if result:
            print("✅ 機能UI作成テスト成功")
        else:
            print("❌ 機能UI作成テスト失敗")
            
        return result
        
    except Exception as e:
        print(f"❌ 機能UI作成テストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """メインテスト実行"""
    print("フォルダ内容表示問題修正テスト開始")
    print("=" * 50)
    
    # テスト実行
    test1 = test_folder_content_logic()
    test2 = test_image_discovery()
    analyze_ui_imports()
    test3 = test_functional_ui_creation()
    
    print("\n" + "=" * 50)
    print("テスト結果:")
    print(f"  フォルダ内容ロジック: {'✅' if test1 else '❌'}")
    print(f"  画像発見ロジック: {'✅' if test2 else '❌'}")
    print(f"  機能UI作成: {'✅' if test3 else '❌'}")
    
    if all([test1, test2, test3]):
        print("\n✅ 全テスト成功：ロジック部分に問題はありません")
        print("問題はPyQt5の初期化またはUI更新にある可能性があります")
    else:
        print("\n❌ テスト失敗：ロジック部分に問題があります")

if __name__ == "__main__":
    main()
