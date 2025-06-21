# test_map_input.py

import os
from apps.logic.gps_parser import extract_gps_coords
from apps.logic.map_generator import generate_map_html

image_path = os.path.abspath("PIC001.jpg")
print(f"🧭 検査ファイル: {image_path}")

# 存在確認
if not os.path.exists(image_path):
    print("❌ 画像ファイルが存在しません。")
    exit()

# GPS抽出
coords = extract_gps_coords(image_path)
if coords:
    print(f"✅ 取得されたGPS座標: 緯度={coords[0]:.6f}, 経度={coords[1]:.6f}")
else:
    print("ℹ️ GPS情報が取得できませんでした。（generate_map_htmlには None が渡されます）")

# HTML出力の一部を表示
html = generate_map_html(coords)
print("\n📄 地図HTMLプレビュー（先頭500文字）:")
print(html[:500])
