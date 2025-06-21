# 📐 PhotoMap Explorer – Architecture Overview | アーキテクチャ概要

This document outlines the overall structure and modular design of the PhotoMap Explorer project.  
本ドキュメントは、PhotoMap Explorer プロジェクトの全体構成とモジュール設計について説明します。

---

## 🏁 System Goals | システムの目的

- Provide a lightweight image viewer with intuitive folder navigation  
  直感的なフォルダブラウズが可能な軽量な画像ビューアを提供
- Extract and utilize EXIF GPS metadata for map visualization  
  EXIF に含まれる GPS メタデータを抽出し、地図上に写真位置を可視化
- Display interactive maps using Leaflet.js within PyQt  
  PyQt の WebView に Leaflet.js を組み込み、インタラクティブな地図表示を実現
- Ensure modular, extensible architecture for future features  
  今後の機能追加（クラウド連携・クラスタリングなど）に対応できるモジュール設計

---

## 🧱 Module Structure | モジュール構成

photomap-explorer/ ├── main_app.py # App launcher and Qt main window | メインウィンドウ起動部 ├── ui_mainwindow.py # UI layout via Qt Designer or manual setup | UI レイアウト定義 ├── folder_browser.py # Local folder selection | フォルダ選択ダイアログ処理 ├── thumbnail_loader.py # Thumbnail generation & display | サムネイル生成と一覧表示 ├── exif_parser.py # Extract EXIF GPS/Date info | EXIF 情報の抽出（緯度経度・撮影日時） ├── map_embedder.py # Leaflet map HTML generation | Leaflet.js を使った地図HTML生成 ├── image_viewer.py # Full preview + metadata panel | プレビュー表示 + メタ情報パネル ├── utils/ │ └── coordinate_converter.py # DMS → decimal latitude/longitude | 度分秒から十進法への変換処理 ├── resources/ │ └── map_template.html # HTML template for embedded maps | Leaflet埋め込み用テンプレート └── docs/, README.md, requirements.txt


---

## 🔄 Data Flow | データフロー

1. User selects an image folder → loads file paths  
   ユーザーが画像フォルダを選択 → パスを取得  
2. For each image:  
   - Generate thumbnail  
   - Parse EXIF for GPS info  
   各画像に対して：サムネイル生成＋EXIF から GPS 情報抽出  
3. Map HTML is generated with pin(s) via Leaflet  
   取得した位置情報で Leaflet によりピンを配置した地図HTMLを生成  
4. PyQt WebView loads map, UI updates with preview + metadata  
   PyQt WebView で地図を表示し、UI で画像プレビューとメタ情報を同時表示  

---

## 🛠️ Tech Stack | 使用技術スタック

| 機能 / Component | 技術 / Tool |
|------------------|-------------|
| GUI              | PyQt5 or PySide6 |
| Image Processing | Pillow, QPixmap |
| Metadata Parsing | piexif, ExifTool (subprocess) |
| Map Display      | Leaflet.js (with QWebEngineView) |
| File I/O         | OS + Qt wrappers |

---

## 🧩 Design Principles | 設計ポリシー

- **Modularization**: UI / logic / parsing / rendering are independent  
  モジュールごとに責務を分離し、拡張性を確保  
- **Platform-ready**: Designed for Windows UX, cross-platform portability considered  
  Windowsライクな操作感を大切にしつつ、移植性にも配慮  
- **Extendability**: Future cloud support (e.g. OneDrive), clustering, and filtering supported  
  将来的なクラウド対応やクラスタリング、Exif検索拡張にも対応可能な構造  

---

## 🚧 Future Plans | 今後の拡張予定

- Multi-photo clustering on map  
  地図上での複数写真クラスタリング対応  
- Map export with overlays  
  写真付きマップ表示のエクスポート機能  
- Cloud storage integration (e.g. OneDrive, Fileforce)  
  OneDrive や Fileforce との連携処理モジュール化  
- Image filtering by date, tag, location  
  撮影日・タグ・位置情報による絞り込み機能  

---

If you'd like to contribute or suggest improvements, see the repository:  
改善提案・参加にご興味があれば、以下のリポジトリをご覧ください：  
🔗 https://github.com/scottlz0310/photomap-explorer