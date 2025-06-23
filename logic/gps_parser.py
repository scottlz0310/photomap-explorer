from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_gps_coords(image_path):
    """
    画像のEXIFデータからGPS座標を抽出します。

    Args:
        image_path (str): 画像ファイルのパス。

    Returns:
        dict or None: GPS情報（緯度、経度）が含まれる辞書。またはNone（情報が存在しない場合）。
    """
    try:
        # 画像ファイルのEXIFデータを取得
        image = Image.open(image_path)
        exif_data = image._getexif()

        if not exif_data:
            return None

        # GPS情報の抽出
        gps_data = {}
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            if tag_name == "GPSInfo":
                for gps_tag_id, gps_value in value.items():
                    gps_tag_name = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_data[gps_tag_name] = gps_value

        if not gps_data:
            return None

        return _parse_gps_data(gps_data)
    except Exception as e:
        print(f"GPSデータの抽出中にエラーが発生しました: {e}")
        return None

def _parse_gps_data(gps_data):
    """
    GPSデータを解析して緯度・経度に変換します。

    Args:
        gps_data (dict): GPS情報の辞書。

    Returns:
        dict: 緯度と経度を含む辞書。
    """
    def convert_to_decimal(degree, minute, second, direction):
        decimal = degree + (minute / 60.0) + (second / 3600.0)
        if direction in ['S', 'W']:  # 南緯、西経なら負の値に変換
            decimal = -decimal
        return decimal

    try:
        latitude = convert_to_decimal(
            gps_data["GPSLatitude"][0], 
            gps_data["GPSLatitude"][1], 
            gps_data["GPSLatitude"][2], 
            gps_data["GPSLatitudeRef"]
        )
        longitude = convert_to_decimal(
            gps_data["GPSLongitude"][0], 
            gps_data["GPSLongitude"][1], 
            gps_data["GPSLongitude"][2], 
            gps_data["GPSLongitudeRef"]
        )

        return {"latitude": latitude, "longitude": longitude}
    except KeyError as e:
        print(f"GPSデータ解析中にキーエラーが発生しました: {e}")
        return None
