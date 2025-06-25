## 新構成 - ファイルごとの中身（続き）

### logic/image_utils.py
```python
# 省略（前述の通り）
```

### logic/folder_utils.py
```python
# 今回は find_images_in_directory が image_utils に含まれるので不要、分割するならここに移しても良い
```

### ui/controls.py
```python
# 省略（前述の通り）
```

---

## README.md（再編集案）
```markdown
# PhotoMap Explorer（再構成版）

画像に含まれるGPS情報をもとに、写真のマップ表示やサムネイル一覧を提供するPyQtアプリケーションです。

---

## 特徴
- フォルダツリーによる画像選択
- サムネイル一覧とサイズ切り替え
- 画像プレビューと位置マップの連動表示
- 入力バーから任意のフォルダへ直接移動

---

## インストール手順
```bash
# 仮想環境を推奨
python -m venv venv
source venv/bin/activate  # Windowsは venv\Scripts\activate

pip install -r requirements.txt
```

### 必要ライブラリ例（requirements.txt に記載）
```
PyQt5
Pillow
folium
```

---

## 起動方法
```bash
python main.py
```

---

## ディレクトリ構成
```
photomap-explorer/
├── main.py
├── main_window.py
├── logic/
│   ├── image_utils.py
│   └── folder_utils.py（必要なら）
├── ui/
│   ├── controls.py
│   ├── folder_panel.py
│   ├── thumbnail_panel.py
│   ├── preview_panel.py
│   └── map_panel.py
├── docs/
└── requirements.txt
```

---

## 注意
- GPS情報が含まれない画像の場合、マップは初期位置（0,0）に表示されます。
- 地図表示にはfoliumを使用しています。
```

---

## ✅ これでREADMEも整理完了です。

さらに tests や setup.py 整備もご希望あれば追記しますのでご指示ください。
