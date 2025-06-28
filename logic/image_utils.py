from PyQt5.QtGui import QPixmap
import os
import folium
import exifread

def load_pixmap(image_path):
    return QPixmap(image_path)

def find_images_in_directory(folder_path, recursive=False):
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    image_paths = []
    if recursive:
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(valid_extensions):
                    image_paths.append(os.path.abspath(os.path.join(root, file)))
    else:
        try:
            for file in os.listdir(folder_path):
                full_path = os.path.join(folder_path, file)
                if os.path.isfile(full_path) and file.lower().endswith(valid_extensions):
                    image_paths.append(os.path.abspath(full_path))
        except Exception:
            pass
    # ファイル名昇順でソートして返す
    return sorted(image_paths, key=lambda x: os.path.basename(x).lower())

def extract_gps_coords(image_path):
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False, strict=True)
        if not tags:
            return None

        def get_if_exist(data, key):
            return data.get(key)

        def convert_to_degrees(value):
            d, m, s = [float(x.num) / float(x.den) for x in value.values]
            return d + (m / 60.0) + (s / 3600.0)

        gps_latitude = get_if_exist(tags, 'GPS GPSLatitude')
        gps_latitude_ref = get_if_exist(tags, 'GPS GPSLatitudeRef')
        gps_longitude = get_if_exist(tags, 'GPS GPSLongitude')
        gps_longitude_ref = get_if_exist(tags, 'GPS GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = convert_to_degrees(gps_latitude)
            if gps_latitude_ref.values[0] != 'N':
                lat = -lat
            lon = convert_to_degrees(gps_longitude)
            if gps_longitude_ref.values[0] != 'E':
                lon = -lon
            return {"latitude": lat, "longitude": lon}
        return None
    except Exception:
        return None

def generate_map_html(lat, lon):
    """指定された緯度経度の地図HTMLを生成"""
    import io
    
    # Foliumマップを作成
    map_obj = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="画像の位置").add_to(map_obj)
    
    # BytesIOを使用してメモリ内でHTMLを生成
    output = io.BytesIO()
    map_obj.save(output, close_file=False)
    html_content = output.getvalue().decode('utf-8')
    output.close()
    
    return html_content

def generate_map_file(lat, lon):
    """指定された緯度経度の地図HTMLファイルを生成（レガシー互換）"""
    map_obj = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="画像の位置").add_to(map_obj)
    output_path = os.path.abspath("map.html")
    map_obj.save(output_path)
    return output_path

def extract_image_info(image_path):
    """
    画像の解像度・撮影日時・カメラ名・シャッタースピード等を辞書で返す
    """
    info = {
        "width": None,
        "height": None,
        "datetime": None,
        "camera": None,
        "shutter": None
    }
    # 解像度
    try:
        pixmap = load_pixmap(image_path)
        if not pixmap.isNull():
            info["width"] = pixmap.width()
            info["height"] = pixmap.height()
    except Exception:
        pass
    # Exif
    try:
        with open(image_path, 'rb') as f:
            tags = exifread.process_file(f, details=False, strict=True)
        if tags:
            info["datetime"] = str(tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime') or "")
            info["camera"] = str(tags.get('Image Model') or "")
            info["shutter"] = str(tags.get('EXIF ExposureTime') or "")
    except Exception:
        pass
    return info
