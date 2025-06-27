# このファイルは window ディレクトリにウィンドウ関連のモジュールを集約するためのものです。

## 今後の分割・整理方針（案）
- 第2回コードリファクタリング。肥大化したmain_window.pyを分割します。
- 実装は少しずつ、動作確認しながら確実に

### 1. main_window.py
- アプリ全体のウィンドウ統括・レイアウト管理
- 各パネルの生成・配置・イベントのハブ
- 「最大化」「アドレスバー更新」など全体制御

### 2. panel_*
- 各UIパネルごとにクラスを分離
    - `panel_folder.py` … フォルダパネル（FolderPanel）
    - `panel_thumbnail.py` … サムネイルパネル（ThumbnailPanel）
    - `panel_preview.py` … プレビューパネル（PreviewPanel）
    - `panel_map.py` … 地図パネル（MapPanel）

### 3. controls_*
- アドレスバーやコントロールバーの生成・管理
    - `controls_addressbar.py`
    - `controls_toolbar.py`（将来のメニューバーやツールバー用）

### 4. layout_utils.py
- レイアウトや最大化・復元などの共通ヘルパー関数

### 5. event_handlers.py（任意）
- イベントハンドラ（on_xxx系）をまとめて管理（肥大化対策）

### 6. __init__.py
- サブモジュールのエクスポート管理

#### 例: 構成イメージ

```
window/
├── main_window.py
├── panel_folder.py
├── panel_thumbnail.py
├── panel_preview.py
├── panel_map.py
├── controls_addressbar.py
├── controls_toolbar.py
├── layout_utils.py
├── event_handlers.py
└── __init__.py
```

このように分割することで、各パネルや機能ごとの責任範囲を明確にし、保守・拡張の下地とします。
