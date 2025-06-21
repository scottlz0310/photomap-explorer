# apps/logic/map_generator.py

def generate_map_html(coords):
    """
    Leaflet.js を使った HTML を生成
    :param coords: (lat, lon) または None
    :return: HTML文字列
    """
    if coords is None:
        coords = (0, 0)
        popup_text = "この画像には位置情報が含まれていません。"
    else:
        popup_text = f"撮影地点: 緯度 {coords[0]:.6f}, 経度 {coords[1]:.6f}"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8" />
      <title>Map</title>
      <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
      <style>html, body, #map {{ height: 100%; margin: 0; }}</style>
    </head>
    <body>
      <div id="map"></div>
      <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
      <script>
        const map = L.map('map').setView([{coords[0]}, {coords[1]}], {4 if coords == (0,0) else 14});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
          attribution: '&copy; OpenStreetMap contributors'
        }}).addTo(map);
        L.marker([{coords[0]}, {coords[1]}])
          .addTo(map)
          .bindPopup("{popup_text}")
          .openPopup();
      </script>
    </body>
    </html>
    """
