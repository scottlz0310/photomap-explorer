#!/usr/bin/env python3
"""GPS EXIFデータ確認スクリプト"""

import exifread
import os
import sys

def check_gps_data():
    """GPS EXIFデータを確認"""
    print("🔍 GPS EXIFデータ確認開始")
    
    test_images = [
        'test_images/taiwan-jiufen.jpg',
        'test_images/england-london-bridge.jpg', 
        'test_images/irland-dingle.jpg',
        'test_images/PIC001.jpg'
    ]
    
    for img_path in test_images:
        if os.path.exists(img_path):
            print(f'\n=== {img_path} ===')
            try:
                with open(img_path, 'rb') as f:
                    tags = exifread.process_file(f)
                    gps_keys = [k for k in tags.keys() if 'GPS' in k]
                    if gps_keys:
                        print(f"GPS情報発見: {len(gps_keys)}個")
                        for key in sorted(gps_keys):
                            print(f'  {key}: {tags[key]}')
                    else:
                        print('GPS情報なし')
            except Exception as e:
                print(f"エラー: {e}")
        else:
            print(f'{img_path}: ファイルが見つかりません')
    
    print("\n✅ GPS EXIFデータ確認完了")

if __name__ == '__main__':
    check_gps_data()
