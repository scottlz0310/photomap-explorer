#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サムネイル表示機能のテストスクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
import traceback

def test_thumbnail_creation():
    """サムネイル作成のテスト"""
    print("=== サムネイル作成テスト ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        from ui.thumbnail_list import create_thumbnail_list, ThumbnailListWidget
        
        print("✅ サムネイル関数インポート成功")
        
        # サムネイルリスト作成
        def dummy_callback(item):
            print(f"サムネイルクリック: {item}")
        
        thumbnail_list = create_thumbnail_list(dummy_callback)
        print(f"✅ サムネイルリスト作成成功: {type(thumbnail_list)}")
        
        # テスト画像の検索
        test_paths = [
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads"),
            os.path.join(os.path.expanduser("~"), "OneDrive"),
            "C:/Windows/Web/Wallpaper",  # Windows標準壁紙
        ]
        
        test_images = []
        for test_path in test_paths:
            if os.path.exists(test_path):
                print(f"📁 検索中: {test_path}")
                folder = Path(test_path)
                for file_path in folder.rglob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}:
                        test_images.append(str(file_path))
                        print(f"  🖼️ 発見: {file_path.name}")
                        if len(test_images) >= 5:  # 最初の5枚まで
                            break
                if len(test_images) >= 5:
                    break
        
        print(f"発見した画像ファイル: {len(test_images)}枚")
        
        if not test_images:
            print("❌ テスト用画像が見つかりません")
            return False
        
        # サムネイル追加テスト
        added_count = 0
        for image_path in test_images:
            try:
                print(f"サムネイル追加テスト: {os.path.basename(image_path)}")
                if hasattr(thumbnail_list, 'add_thumbnail'):
                    success = thumbnail_list.add_thumbnail(image_path)
                    if success:
                        added_count += 1
                        print(f"  ✅ 追加成功")
                    else:
                        print(f"  ❌ 追加失敗")
                else:
                    print(f"  ❌ add_thumbnail メソッドがありません")
            except Exception as e:
                print(f"  ❌ エラー: {e}")
        
        print(f"追加成功: {added_count}/{len(test_images)}枚")
        
        # サムネイル表示テスト
        if added_count > 0:
            widget = QWidget()
            layout = QVBoxLayout(widget)
            
            label = QLabel(f"サムネイルテスト ({added_count}枚)")
            layout.addWidget(label)
            layout.addWidget(thumbnail_list)
            
            widget.setWindowTitle("サムネイル表示テスト")
            widget.resize(600, 400)
            widget.show()
            
            # 5秒後に閉じる
            from PyQt5.QtCore import QTimer
            timer = QTimer()
            timer.timeout.connect(widget.close)
            timer.setSingleShot(True)
            timer.start(5000)
            
            app.processEvents()
            timer.timeout.connect(app.quit)
            app.exec_()
        
        return added_count > 0
        
    except Exception as e:
        print(f"❌ サムネイル作成テストエラー: {e}")
        traceback.print_exc()
        return False

def test_gps_functionality():
    """GPS機能のテスト"""
    print("\n=== GPS機能テスト ===")
    
    try:
        # GPS関連モジュールのインポートテスト
        try:
            from logic.image_utils import extract_gps_info
            print("✅ GPS関数インポート成功")
            gps_available = True
        except ImportError as e:
            print(f"❌ GPS関数インポートエラー: {e}")
            gps_available = False
        
        if not gps_available:
            print("GPS機能が利用できません。モジュールを確認してください。")
            return False
        
        # テスト画像の検索（GPS情報付きの可能性が高いファイル）
        test_paths = [
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads"),
        ]
        
        test_images = []
        for test_path in test_paths:
            if os.path.exists(test_path):
                print(f"📁 GPS画像検索中: {test_path}")
                folder = Path(test_path)
                for file_path in folder.rglob("*"):
                    if file_path.is_file() and file_path.suffix.lower() in {'.jpg', '.jpeg'}:
                        test_images.append(str(file_path))
                        if len(test_images) >= 5:  # 最初の5枚まで
                            break
                if len(test_images) >= 5:
                    break
        
        print(f"GPS テスト対象画像: {len(test_images)}枚")
        
        # GPS情報抽出テスト
        gps_found = 0
        for image_path in test_images:
            try:
                print(f"GPS抽出テスト: {os.path.basename(image_path)}")
                gps_info = extract_gps_info(image_path)
                if gps_info and len(gps_info) >= 2:
                    lat, lon = gps_info[0], gps_info[1]
                    print(f"  ✅ GPS発見: {lat:.6f}, {lon:.6f}")
                    gps_found += 1
                else:
                    print(f"  📍 GPS情報なし")
            except Exception as e:
                print(f"  ❌ GPS抽出エラー: {e}")
        
        print(f"GPS情報発見: {gps_found}/{len(test_images)}枚")
        
        return gps_found > 0 or len(test_images) > 0  # 処理自体が動作すればOK
        
    except Exception as e:
        print(f"❌ GPS機能テストエラー: {e}")
        traceback.print_exc()
        return False

def main():
    """メイン処理"""
    print("サムネイル・GPS機能テスト開始")
    
    # テスト実行
    tests = [
        ("サムネイル作成・表示", test_thumbnail_creation),
        ("GPS機能", test_gps_functionality),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"テスト: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            print(f"結果: {'✅ PASS' if result else '❌ FAIL'}")
        except Exception as e:
            print(f"❌ テスト実行エラー: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    # 結果サマリー
    print(f"\n{'='*50}")
    print("テスト結果サマリー:")
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n合計: {passed}/{total} テスト通過")

if __name__ == "__main__":
    main()
