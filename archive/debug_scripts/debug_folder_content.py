#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新UIフォルダ内容表示問題の診断スクリプト
"""

import sys
import os
from pathlib import Path

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.pat        return False
        
    except Exception as e:
        print(f"❌ FunctionalNewMainWindow テストエラー: {e}")
        traceback.print_exc()
        return Falsert(0, str(project_root))

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QListWidget, QListWidgetItem
from PyQt5.QtCore import Qt
import traceback

def test_folder_content_display():
    """フォルダ内容表示のテスト"""
    print("=== フォルダ内容表示テスト ===")
    
    # テストフォルダパス
    test_folder = os.path.join(os.path.expanduser("~"), "Pictures")
    print(f"テストフォルダ: {test_folder}")
    print(f"フォルダ存在確認: {os.path.exists(test_folder)}")
    
    if not os.path.exists(test_folder):
        print("❌ テストフォルダが存在しません")
        return False
    
    try:
        # フォルダ内容を取得
        folder = Path(test_folder)
        items = []
        
        print(f"フォルダ読み込み開始: {folder}")
        
        # 親フォルダ項目
        if folder.parent != folder:
            print(f"親フォルダ: {folder.parent}")
        
        # フォルダ内容を一覧表示
        item_count = 0
        folder_count = 0
        image_count = 0
        other_count = 0
        
        for item_path in folder.iterdir():
            item_count += 1
            if item_path.is_dir():
                folder_count += 1
                print(f"📁 {item_path.name}")
            elif item_path.is_file():
                file_ext = item_path.suffix.lower()
                if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                    image_count += 1
                    print(f"🖼️ {item_path.name}")
                else:
                    other_count += 1
                    print(f"📄 {item_path.name}")
            
            # 最初の10個まで表示
            if item_count >= 10:
                print("... (最初の10個のみ表示)")
                break
        
        print(f"総計: フォルダ {folder_count}, 画像 {image_count}, その他 {other_count}")
        return True
        
    except PermissionError:
        print("❌ アクセス権限エラー")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        traceback.print_exc()
        return False

def test_qlistwidget():
    """QListWidgetの動作テスト"""
    print("\n=== QListWidget テスト ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        # テストウィンドウ作成
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        label = QLabel("フォルダ内容テスト")
        layout.addWidget(label)
        
        list_widget = QListWidget()
        layout.addWidget(list_widget)
        
        # テストアイテム追加
        test_folder = os.path.join(os.path.expanduser("~"), "Pictures")
        
        if os.path.exists(test_folder):
            folder = Path(test_folder)
            
            # 親フォルダ項目
            if folder.parent != folder:
                parent_item = QListWidgetItem("📁 .. (親フォルダ)")
                parent_item.setData(Qt.UserRole, str(folder.parent))
                list_widget.addItem(parent_item)
            
            # フォルダ内容
            item_count = 0
            for item_path in folder.iterdir():
                if item_count >= 10:  # 最初の10個まで
                    break
                    
                if item_path.is_dir():
                    item = QListWidgetItem(f"📁 {item_path.name}")
                    item.setData(Qt.UserRole, str(item_path))
                    list_widget.addItem(item)
                elif item_path.is_file():
                    file_ext = item_path.suffix.lower()
                    if file_ext in {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}:
                        item = QListWidgetItem(f"🖼️ {item_path.name}")
                        item.setData(Qt.UserRole, str(item_path))
                        list_widget.addItem(item)
                
                item_count += 1
        
        print(f"QListWidget アイテム数: {list_widget.count()}")
        
        # アイテム一覧表示
        for i in range(list_widget.count()):
            item = list_widget.item(i)
            print(f"  {i}: {item.text()}")
        
        # ウィンドウ表示（短時間）
        widget.setWindowTitle("フォルダ内容テスト")
        widget.resize(400, 300)
        widget.show()
        
        # 2秒後に閉じる
        from PyQt5.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(widget.close)
        timer.setSingleShot(True)
        timer.start(2000)
        
        app.processEvents()
        timer.timeout.connect(app.quit)
        app.exec_()
        
        return True
        
    except Exception as e:
        print(f"❌ QListWidget テストエラー: {e}")
        traceback.print_exc()
        return False

def test_functional_new_main_view():
    """FunctionalNewMainWindowの初期化テスト"""
    print("\n=== FunctionalNewMainWindow 初期化テスト ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    try:
        from presentation.views.functional_new_main_view import FunctionalNewMainWindow
        
        print("FunctionalNewMainWindow インポート成功")
        
        # インスタンス作成
        main_view = FunctionalNewMainWindow()
        print("FunctionalNewMainWindow インスタンス作成成功")
        
        # 初期化状態確認
        print(f"current_folder: {main_view.current_folder}")
        print(f"folder_content_list: {main_view.folder_content_list}")
        print(f"folder_content_list アイテム数: {main_view.folder_content_list.count() if main_view.folder_content_list else 'None'}")
        
        if main_view.folder_content_list:
            for i in range(main_view.folder_content_list.count()):
                item = main_view.folder_content_list.item(i)
                print(f"  {i}: {item.text()}")
        
        # ウィンドウ表示（短時間）
        main_view.show()
        
        # 2秒後に閉じる
        from PyQt5.QtCore import QTimer
        timer = QTimer()
        timer.timeout.connect(main_view.close)
        timer.setSingleShot(True)
        timer.start(2000)
        
        app.processEvents()
        timer.timeout.connect(app.quit)
        app.exec_()
        
        return True
        
    except Exception as e:
        print(f"❌ FunctionalNewMainView テストエラー: {e}")
        traceback.print_exc()
        return False

def main():
    """メイン処理"""
    print("新UIフォルダ内容表示問題の診断開始")
    
    # テスト実行
    tests = [
        ("フォルダ内容取得", test_folder_content_display),
        ("QListWidget動作", test_qlistwidget),
        ("FunctionalNewMainWindow初期化", test_functional_new_main_view),
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
