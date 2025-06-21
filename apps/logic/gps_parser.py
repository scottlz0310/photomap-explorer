from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_gps_coords(path):
    """
    画像ファイルからGPS情報（緯度・経度）を抽出する。
    取得できない場合は None を返す。
    """

    def _convert_to_degrees(value):
        try:
            if len(value) != 3:
                return None

            def as_float(x):
                if isinstance(x, tuple):
                    return x[0] / x[1] if x[1] != 0 else 0
                elif hasattr(x, 'numerator') and hasattr(x, 'denominator'):
                    return x.numerator / x.denominator
                else:
                    return float(x)

            d = as_float(value[0])
            m = as_float(value[1])
            s = as_float(value[2])
            return d + (m / 60.0) + (s / 3600.0)

        except Exception:
            return None

    try:
        img = Image.open(path)
        exif_data = img._getexif()
        if not exif_data:
            return None

        gps_data = None
        for tag, val in exif_data.items():
            if TAGS.get(tag) == "GPSInfo":
                gps_data = {GPSTAGS.get(k, k): v for k, v in val.items()}
                break

        if not gps_data:
            return None

        required = ["GPSLatitude", "GPSLatitudeRef", "GPSLongitude", "GPSLongitudeRef"]
        if not all(k in gps_data for k in required):
            return None

        lat = _convert_to_degrees(gps_data["GPSLatitude"])
        lon = _convert_to_degrees(gps_data["GPSLongitude"])
        if lat is None or lon is None:
            return None

        if gps_data["GPSLatitudeRef"] == "S":
            lat = -lat
        if gps_data["GPSLongitudeRef"] == "W":
            lon = -lon

        if (lat, lon) == (0.0, 0.0):
            return None

        return (lat, lon)

    except Exception:
        return None
