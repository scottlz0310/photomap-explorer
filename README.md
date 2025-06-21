# PhotoMap Explorer

PhotoMap Explorer is a lightweight photo viewer that visualizes GPS-tagged images on an interactive map.  
It’s designed for photographers and travelers who want a simple, intuitive way to explore photo locations.

GitHub Repository: [scottlz0310/photomap-explorer](https://github.com/scottlz0310/photomap-explorer)

## ✨ Features
- Browse local folders and preview photos as thumbnails
- Extract GPS metadata (EXIF) from geotagged images
- Display image locations on an interactive map (Leaflet.js)
- Resizable, zoomable map interface
- Clean UI inspired by Windows Photos
- Future support for OneDrive, Fileforce, and external drives

## 🚀 Getting Started
```bash
git clone https://github.com/scottlz0310/photomap-explorer.git
cd photomap-explorer
pip install -r requirements.txt
python main_app.py
🔧 Tech Stack
Python 3.x

PyQt5

Pillow

piexif or ExifTool

Leaflet.js (via QWebEngineView)

🗺️ Roadmap
[ ] Multi-photo clustering on map

[ ] Filtering by date or GPS region

[ ] OneDrive & cloud integration

[ ] Exportable map snapshot with image overlay

📄 License
This project is licensed under the MIT License.

<details> <summary>📘 日本語版（Japanese version）</summary>

PhotoMap Explorer（フォトマップ・エクスプローラー）
PhotoMap Explorer は、GPS メタデータ付きの画像を地図上に表示できる軽量フォトビューアです。 旅行写真の整理や、撮影場所を可視化したい方のために設計されています。

GitHub リポジトリ: scottlz0310/photomap-explorer

✨ 主な機能
ローカルフォルダから写真を一覧表示（サムネイル付き）

Exif メタデータから GPS 情報を抽出

Leaflet.js による地図表示（ピン表示・ズーム対応）

プレビュー付きのシンプルな UI（Windows ライク）

将来的に OneDrive / Fileforce などのクラウド対応も視野に

🚀 セットアップ手順
bash
git clone https://github.com/scottlz0310/photomap-explorer.git
cd photomap-explorer
pip install -r requirements.txt
python main_app.py
🔧 使用技術
Python 3.x

PyQt5

Pillow（画像処理）

piexif または ExifTool（Exif情報）

Leaflet.js（地図表示）

🗺️ 今後のロードマップ
[ ] 地図上での複数写真クラスタリング

[ ] 撮影日・位置によるフィルタリング

[ ] OneDrive対応（API経由）

[ ] 写真付きマップビューのエクスポート機能

📄 ライセンス
本プロジェクトは MIT ライセンスの下で公開されています。

</details>