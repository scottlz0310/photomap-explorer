import os

TEMPLATE_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>PhotoMap</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
</head>
<body>
    <div id="map" style="width: 100%; height: 100vh;"></div>
    <script>
        var map = L.map('map').setView([LATITUDE, LONGITUDE], 13);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {{
            maxZoom: 19,
        }}).addTo(map);
        L.marker([LATITUDE, LONGITUDE]).addTo(map)
            .bindPopup('Location: [LATITUDE, LONGITUDE]')
            .openPopup();
    </script>
</body>
</html>
"""

def generate_map_html(latitude, longitude, output_path="map.html"):
    """
    GPSデータを元に地図HTMLを生成します。

    Args:
        latitude (float): 緯度
        longitude (float): 経度
        output_path (str): 保存先のHTMLファイルパス

    Returns:
        str: 生成されたHTMLファイルのパス
    """
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError("緯度と経度が有効な範囲外です。")

    # HTMLテンプレートのカスタマイズ
    html_content = TEMPLATE_HTML.replace("LATITUDE", str(latitude)).replace("LONGITUDE", str(longitude))

    # HTMLファイルとして保存
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"地図HTMLが生成されました: {os.path.abspath(output_path)}")
    return os.path.abspath(output_path)
