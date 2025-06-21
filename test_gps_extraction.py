import os
from apps.logic.gps_parser import extract_gps_coords
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

# 対象画像ファイル
image_path = os.path.abspath("PIC001.jpg")
print(f"🧪 検査中ファイル: {image_path}")

# 存在チェック
if not os.path.exists(image_path):
    print("❌ ファイルが見つかりません")
    exit()

# 🔍 元の extract 関数とは別に、Exif内容を直接覗いてみる
try:
    img = Image.open(image_path)
    exif_data = img._getexif()
    if not exif_data:
        print("⚠️ Exif 情報がありません")
        exit()

    # GPS 情報抽出
    gps_info_raw = None
    for tag, val in exif_data.items():
        decoded = TAGS.get(tag, tag)
        if decoded == "GPSInfo":
            gps_info_raw = {GPSTAGS.get(k, k): v for k, v in val.items()}
            break

    if not gps_info_raw:
        print("⚠️ GPS 情報が見つかりません")
    else:
        print("📦 GPS 生データ:")
        for key, val in gps_info_raw.items():
            print(f"   {key}: {val}")

        # 緯度/経度を抽出できるか確認
        lat = gps_info_raw.get("GPSLatitude")
        lon = gps_info_raw.get("GPSLongitude")
        ref_lat = gps_info_raw.get("GPSLatitudeRef")
        ref_lon = gps_info_raw.get("GPSLongitudeRef")

        print(f"\n🔍 座標候補:")
        print(f"   緯度: {lat} {ref_lat}")
        print(f"   経度: {lon} {ref_lon}")

except Exception as e:
    print(f"❌ 解析中にエラーが発生しました: {e}")
