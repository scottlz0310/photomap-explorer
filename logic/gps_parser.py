import exifread

def extract_gps_coords(image_path):
    """
    画像のEXIFデータからGPS座標を抽出します。

    Args:
        image_path (str): 画像ファイルのパス。

    Returns:
        dict or None: GPS情報（緯度、経度）が含まれる辞書。またはNone（情報が存在しない場合）。
    """
    try:
        # ファイルを開いてタグを解析
        with open(image_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)
        
        # GPS情報の取得
        gps_latitude = tags.get('GPS GPSLatitude')
        gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
        gps_longitude = tags.get('GPS GPSLongitude')
        gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

        if not all([gps_latitude, gps_latitude_ref, gps_longitude, gps_longitude_ref]):
            return None

        # 緯度と経度を変換
        latitude = _convert_to_decimal(gps_latitude, gps_latitude_ref)
        longitude = _convert_to_decimal(gps_longitude, gps_longitude_ref)
        
        return {"latitude": latitude, "longitude": longitude}
    except Exception as e:
        print(f"GPSデータの抽出中にエラーが発生しました: {e}")
        return None

def _convert_to_decimal(coord, ref):
    """
    緯度・経度を10進法に変換します。

    Args:
        coord: 度分秒形式の座標。
        ref: N/S または E/W。

    Returns:
        float: 10進法の座標。
    """
    degrees, minutes, seconds = [float(x.num) / float(x.den) for x in coord.values]
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref.values[0] in ['S', 'W']:
        decimal = -decimal
    return decimal