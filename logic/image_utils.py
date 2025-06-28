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
    map_obj = folium.Map(location=[lat, lon], zoom_start=15)
    folium.Marker([lat, lon], tooltip="画像の位置").add_to(map_obj)
    output_path = os.path.abspath("map.html")
    map_obj.save(output_path)
    return output_path

def extract_image_info(image_path):
    """
    画像ファイルからEXIF情報を抽出（exifreadライブラリを使用）
    
    Args:
        image_path (str): 画像ファイルのパス
        
    Returns:
        dict: EXIF情報の辞書
    """
    try:
        import os
        
        info = {}
        
        # ファイル基本情報
        stat = os.stat(image_path)
        info['ファイルサイズ'] = f"{stat.st_size / 1024:.1f} KB"
        info['ファイル名'] = os.path.basename(image_path)
        
        # exifreadを使用してEXIF情報を取得
        try:
            with open(image_path, 'rb') as f:
                tags = exifread.process_file(f, details=False, strict=True)
            
            if tags:
                # 撮影日時
                if 'EXIF DateTimeOriginal' in tags:
                    info['datetime'] = str(tags['EXIF DateTimeOriginal'])
                    info['撮影日時'] = str(tags['EXIF DateTimeOriginal'])
                elif 'Image DateTime' in tags:
                    info['datetime'] = str(tags['Image DateTime'])
                    info['撮影日時'] = str(tags['Image DateTime'])
                elif 'EXIF DateTime' in tags:
                    info['datetime'] = str(tags['EXIF DateTime'])
                    info['撮影日時'] = str(tags['EXIF DateTime'])
                
                # カメラ情報（メーカー + 機種を統合）
                make = ""
                model = ""
                if 'Image Make' in tags:
                    make = str(tags['Image Make']).strip()
                    info['メーカー'] = make
                if 'Image Model' in tags:
                    model = str(tags['Image Model']).strip()
                    info['機種'] = model
                
                # カメラ情報を統合（表示用）
                if make and model:
                    # メーカー名が機種名に含まれている場合は重複を避ける
                    if make.lower() in model.lower():
                        info['camera'] = model
                    else:
                        info['camera'] = f"{make} {model}"
                elif model:
                    info['camera'] = model
                elif make:
                    info['camera'] = make
                
                # 画像サイズ
                if 'EXIF ExifImageWidth' in tags and 'EXIF ExifImageLength' in tags:
                    width = int(str(tags['EXIF ExifImageWidth']))
                    height = int(str(tags['EXIF ExifImageLength']))
                    info['width'] = width
                    info['height'] = height
                    info['画像サイズ'] = f"{width} × {height}"
                elif 'Image ImageWidth' in tags and 'Image ImageLength' in tags:
                    width = int(str(tags['Image ImageWidth']))
                    height = int(str(tags['Image ImageLength']))
                    info['width'] = width
                    info['height'] = height
                    info['画像サイズ'] = f"{width} × {height}"
                
                # ISO感度
                if 'EXIF ISOSpeedRatings' in tags:
                    iso_value = str(tags['EXIF ISOSpeedRatings'])
                    info['ISO感度'] = iso_value
                    info['iso'] = iso_value  # 表示用キー
                elif 'EXIF PhotographicSensitivity' in tags:
                    iso_value = str(tags['EXIF PhotographicSensitivity'])
                    info['ISO感度'] = iso_value
                    info['iso'] = iso_value  # 表示用キー
                
                # 絞り値
                if 'EXIF FNumber' in tags:
                    f_number = tags['EXIF FNumber']
                    f_value = float(f_number.values[0].num) / float(f_number.values[0].den)
                    f_str = f"F/{f_value:.1f}"
                    info['絞り値'] = f_str
                    info['aperture'] = f_str  # 表示用キー
                elif 'EXIF ApertureValue' in tags:
                    # ApertureValueからF値を計算（APEX値）
                    aperture_value = tags['EXIF ApertureValue']
                    if hasattr(aperture_value, 'values') and aperture_value.values:
                        apex_value = float(aperture_value.values[0].num) / float(aperture_value.values[0].den)
                        f_value = 2 ** (apex_value / 2)
                        f_str = f"F/{f_value:.1f}"
                        info['絞り値'] = f_str
                        info['aperture'] = f_str  # 表示用キー
                
                # シャッタースピード
                if 'EXIF ExposureTime' in tags:
                    exposure = tags['EXIF ExposureTime']
                    num = exposure.values[0].num
                    den = exposure.values[0].den
                    
                    if den > num and num == 1:
                        # 1/xxx形式の高速シャッター
                        shutter_speed = f"1/{den}"
                    elif den > num:
                        # 分数形式
                        shutter_speed = f"{num}/{den}"
                    else:
                        # 秒単位の低速シャッター
                        seconds = float(num) / float(den)
                        if seconds >= 1:
                            shutter_speed = f"{seconds:.1f}秒"
                        else:
                            shutter_speed = f"1/{int(1/seconds)}"
                    
                    info['shutter'] = shutter_speed  # 表示用キー
                    info['シャッタースピード'] = shutter_speed  # 互換性用キー
                elif 'EXIF ShutterSpeedValue' in tags:
                    # ShutterSpeedValueからシャッタースピードを計算（APEX値）
                    shutter_value = tags['EXIF ShutterSpeedValue']
                    if hasattr(shutter_value, 'values') and shutter_value.values:
                        apex_value = float(shutter_value.values[0].num) / float(shutter_value.values[0].den)
                        exposure_time = 1 / (2 ** apex_value)
                        if exposure_time >= 1:
                            shutter_speed = f"{exposure_time:.1f}秒"
                        else:
                            shutter_speed = f"1/{int(1/exposure_time)}"
                        info['shutter'] = shutter_speed  # 表示用キー
                        info['シャッタースピード'] = shutter_speed  # 互換性用キー
                
                # 焦点距離
                if 'EXIF FocalLength' in tags:
                    focal_length = tags['EXIF FocalLength']
                    focal_mm = float(focal_length.values[0].num) / float(focal_length.values[0].den)
                    focal_str = f"{focal_mm:.0f}mm"
                    info['焦点距離'] = focal_str
                    info['focal_length'] = focal_str  # 表示用キー
                    
            else:
                info['EXIF情報'] = "なし"
                
        except Exception as exif_error:
            info['EXIF'] = f"EXIF読み込みエラー: {exif_error}"
        
        # GPS情報
        gps_info = extract_gps_coords(image_path)
        if gps_info:
            info['GPS緯度'] = f"{gps_info['latitude']:.6f}"
            info['GPS経度'] = f"{gps_info['longitude']:.6f}"
        else:
            info['GPS情報'] = "なし"
            
        return info
        
    except Exception as e:
        return {'エラー': f"情報抽出エラー: {e}"}