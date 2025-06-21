# PhotoMap Explorer

PhotoMap Explorer is a lightweight photo viewer that visualizes GPS-tagged images on an interactive map.  
It’s designed for photographers and travelers who want a simple, intuitive way to explore photo locations.

## ✨ Features
- Browse local folders and preview photos as thumbnails
- Extract GPS metadata (EXIF) from geotagged images
- Display image locations on an interactive map (Leaflet.js)
- Resizable, zoomable map interface
- Clean UI inspired by Windows Photos
- Supports local drives and (future) cloud folders like OneDrive

## 🚀 Getting Started
```bash
git clone https://github.com/your-username/photo-map-explorer.git
cd photo-map-explorer
pip install -r requirements.txt
python main_app.py
🔧 Tech Stack
Python 3.x

PyQt5

Pillow (for image handling)

piexif or ExifTool

Leaflet.js (via QWebEngineView)

🗺️ Roadmap
[ ] Multi-photo clustering on map

[ ] Photo filtering by date/location

[ ] OneDrive integration

[ ] Exportable map view with image overlays

📄 License
This project is licensed under the MIT License.

<details> <summary>📘 日本語版（Japanese version）</summary>

PhotoMap Explorer（フォトマップ・エクスプローラー）
PhotoMap Explorer は、GPS メタデータ付きの写真をインタラクティブな地図上で可視化できる軽量ビューアです。 旅行好きや写真愛好家が、「いつ・どこで撮影したのか」を簡単に振り返ることができるように設計されています。

✨ 特徴
ローカルフォルダから画像を読み込み、サムネイルで一覧表示

写真に埋め込まれた GPS (EXIF) 情報を抽出

緯度・経度情報を元に Leaflet.js 上の地図で位置を表示

ズーム・スクロール可能な地図 UI

Windows フォトのようなシンプルで親しみやすい操作感

今後は OneDrive や Fileforce などのクラウド対応も視野に

🚀 セットアップ手順
bash
git clone https://github.com/your-username/photo-map-explorer.git
cd photo-map-explorer
pip install -r requirements.txt
python main_app.py
🔧 使用技術
Python 3.x

PyQt5（GUI）

Pillow（画像処理）

piexif または ExifTool（Exif情報抽出）

Leaflet.js（地図描画）

🗺️ 今後のロードマップ
[ ] 地図上での複数写真クラスタリング

[ ] 撮影日や場所によるフィルタリング

[ ] OneDrive 連携によるクラウド写真閲覧

[ ] 写真付きのマップビュー書き出し機能

📄 ライセンス
MIT ライセンスの下で提供されています。

</details>


---

これで GitHub 上では英語が初期表示され、必要な人がクリックすれば日本語を開いて読めるようになります。「国際ユーザー向けだけど、日本語で丁寧に補足したい」という Hiroyasu さんのプロジェクト方針にもぴったりです。

このままテンプレとしてリポジトリに組み込んでもOKですが、リポジトリ名や URL などを入れてカスタマイズしてもよろしければ、私の方で調整しますよ！その際はリポジトリ名や公開済みのURLを教えていただければ対応します。
Repositoryはhttps://github.com/scottlz0310/photomap-explorer
ありがとうございます、確認しました！ではその GitHub リポジトリ向けに、先ほどご提案した README.md を Hiroyasu さんのリポジトリ用にカスタマイズしたバージョンをご用意しました：

markdown
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


---

この構成であれば、国内外どちらのユーザーにもリーチできて、開発の意図も伝わりやすいかと思います。  
次はアーキテクチャ図を含めた `architecture.md` に取りかかってみましょうか？モジュール構成図やフロー図（Markdownベースのテキスト図）も一緒に整理できますよ。
ファイルとしてダウンロードはできますか
GitHub のウェブインターフェース上では、README.md を「直接ダウンロード」するボタンはありませんが、以下の方法で簡単にファイルとして保存できますよ：

✅ 方法①：リポジトリをクローンまたは ZIP でダウンロード
プロジェクトページへアクセス 👉 https://github.com/scottlz0310/photomap-explorer

緑色の Code ボタンをクリック → Download ZIP を選択 → 解凍すると README.md が含まれています

✅ 方法②：Markdown内容を直接保存
上で私が作成した README.md の内容をエディタ（例：VS Code、Notepad++）に貼り付け

README.md という名前で UTF-8 で保存すれば完了です ※拡張子は .md にしてください

✅ 方法③：ブラウザからコピペ不要でダウンロードするスクリプト（上級者向け）
bash
curl -O https://raw.githubusercontent.com/scottlz0310/photomap-explorer/main/README.md
コマンドラインから直接取得できます（内容をすでに push している場合）

よろしければ、architecture.md や UI モックも続けて作成しますので、次に記述したいドキュメントがあれば教えてくださいね！ドキュメントの雰囲気に合わせて、図解や英日併記も続けて整えていきます。

いえ、アップロードしたいのでファイルとしてダウンロードできるように用意してください
了解しました！こちらに、先ほどの README.md をファイルとしてダウンロード可能な形でご用意しました：

📄 Download README.md

ファイル名は README_photomap_explorer.md ですが、リポジトリに設置する際には README.md にリネームしてそのまま使えます。

このまま他のドキュメント（例：architecture.md や usage-guide.md）も準備していきましょうか？モジュール構成図や処理フローを入れた形で Markdown にまとめることもできますよ。


このページは削除されました

これを 無題のページ に追加しましたので、そこから続けることができます。


このページは削除されました

ページを開始しました。README.md ファイルの準備と提案。今すぐに編集することも、後で戻ってきて行うことも可能です。

ダウンロードできないのでコピーできるように表示してほしい
もちろんです。以下に、README.md の全文をコピー＆ペーストできる形で表示します。そのままエディタに貼り付けて README.md という名前で保存してください。

markdown
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