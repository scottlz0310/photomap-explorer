📍 GPS付き画像から撮影地点を地図に自動表示する軽量ツール  
Exif情報を解析し、PyQtWebEngineベースの地図にピンを立てて視覚化します。

---

## ✨ 特徴

- Exifに埋め込まれたGPS情報を抽出（緯度・経度）
- PyQtWebEngineによるインタラクティブな地図HTML表示
- PyQt5 GUIで画像＋地図ビューアを直感的に操作
- フォルダ内の画像を自動検出し履歴ナビゲーション
- GPS情報がない画像はNull Islandへスキップ
- シンプルかつ高速な単体画像処理
- コード分割で保守性・拡張性も向上

---

## 🖼️ スクリーンショット

画像内のGPS情報を地図にマッピング：

![スクリーンショット](docs/screenshot_dingle.jpg)

---

## 🚀 セットアップと使い方

### 1. クローン & 仮想環境の作成

```bash
git clone https://github.com/scottlz0310/photomap-explorer.git
cd photomap-explorer
python -m venv venv
```

### 2. 仮想環境を有効化

- Windows:
  ```pwsh
  venv\Scripts\activate
  ```
  ```bash
  source venv\Scripts\activate
  ```
- macOS / Linux:
  ```bash
  source venv/bin/activate
  ```

### 3. 必要なライブラリをインストール

```bash
pip install -r requirements.txt
```

### 4. アプリを起動

```bash
python main.py
```

画像ファイルを選択すると、自動でGPS位置が取得され、地図上にピンが表示されます。

---

## 📦 主な依存ライブラリ

| ライブラリ   | 用途             |
|--------------|------------------|
| PyQt5        | GUI表示          |
| PyQtWebEngine| 地図の描画       |
| folium       | 地図HTML生成     |
| exifread     | Exifデータ抽出   |

---

## 📁 ディレクトリ構成（分割後）

```
photomap-explorer/
├── LICENSE                  #  ライセンスファイル
├── README.md                #  プロジェクト説明・セットアップ手順
├── requirements.txt         #  必要な依存ライブラリ一覧
├── main.py                  #  アプリのエントリーポイント
├── main_window.py           #  メインウィンドウの統括クラス
├── logic/                   #  画像・GPS・地図関連のロジック
│   └── image_utils.py       #  画像処理・GPS抽出・地図生成関数
├── ui/                      #  ユーザーインターフェース部品
│   ├── controls.py          #  アドレスバー・ボタン等のコントロール
│   ├── folder_browser.py    #  フォルダ選択ビュー
│   ├── folder_panel.py      #  フォルダパネル（ツリー表示）
│   ├── image_preview.py     #  画像プレビュー表示
│   ├── map_panel.py         #  地図パネル
│   ├── map_view.py          #  地図ビュー
│   ├── preview_panel.py     #  プレビューパネル
│   ├── thumbnail_panel.py   #  サムネイルパネル
│   └── thumbnail_list.py    #  サムネイルリスト管理
├── assets/                  #  静的ファイル・アイコン等
│   ├── pme.ico              #  アプリ用アイコン
│   └── ...                  #  その他アセット
├── docs/                    #  ドキュメント類
│   ├── architecture.md      #  アーキテクチャ概要
│   ├── CONTRIBUTING.md      #  コントリビュートガイド
│   ├── Pending_features.md  #  開発予定・ToDo
│   └── ...                  #  その他ドキュメント
```

---

## ⚠️ 注意点・今後の開発予定

- GPS情報のない画像は地図に表示されません（アプリは正常動作）
- 一部スマートフォン画像は位置情報が非標準形式で保存されており、読み取れない場合があります
- 現在は1枚ずつの表示に対応（将来的にバッチ処理や複数ピン対応も検討）
- 詳細・進捗は docs/Pending_features.md を参照

---

## 📄 ライセンス

MIT License  
© 2025 scottlz0310

---

## 🙌 クレジット

開発・ドキュメント: scottlz0310（GitHub: [@scottlz0310](https://github.com/scottlz0310))  
コーディングサポート: Microsoft Copilot
