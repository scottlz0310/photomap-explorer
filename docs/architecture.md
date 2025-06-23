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

V1.0時点
photomap_explorer/
├── main.py                # エントリーポイント
├── main_window.py         # MainWindowの統括（最低限）
├── README.md
├── requirements.txt       # 依存ライブラリ一覧
│
├── ui/                    # UI関連モジュール
│   ├── __init__.py
│   ├── image_preview.py   # ImagePreviewView クラス
│   ├── folder_browser.py  # QTreeView/Model の構成や選択処理
│   ├── thumbnail_list.py  # QListWidget サムネイル処理
│   ├── map_view.py        # QWebEngineView の地図ビュー管理
│   └── controls.py        # アドレスバー・ボタンのUI部品
│
├── logic/                 # ロジック関連
│   ├── __init__.py
│   ├── image_loader.py
│   ├── gps_parser.py
│   └── map_generator.py
│
└── assets/                # アセット
    └── pme.ico


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



If you'd like to contribute or suggest improvements, see the repository:  
改善提案・参加にご興味があれば、以下のリポジトリをご覧ください：  
🔗 https://github.com/scottlz0310/photomap-explorer