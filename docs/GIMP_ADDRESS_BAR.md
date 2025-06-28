# GIMP風アドレスバー実装ガイド

## 📋 概要

PhotoMap Explorer 2.0.0では、GIMP風のパンくずリストナビゲーションを実装しました。
これにより、フォルダ階層を直感的にナビゲートできるプロフェッショナルなインターフェースを提供します。

## 🎯 特徴

### 視覚的デザイン
- **GIMP 2.10+スタイル**: 正確なGIMPライクなデザイン
- **グラデーション効果**: 洗練されたホバーアニメーション
- **適切なサイズ**: 24px高さでコンパクトなデザイン
- **区切り文字**: 右向き三角形（▶）でパス区切り

### 機能
- **クリック可能パス**: 各フォルダ部分をクリックして移動
- **テキスト編集**: ダブルクリックまたはF2で直接編集
- **キーボードナビゲーション**: 完全なキーボードサポート
- **パス検証**: 無効なパスの自動検出とエラー表示

## 🎮 使用方法

### 基本操作

#### パス移動
```
C: ▶ Users ▶ YourName ▶ Pictures
[クリック可能]  [クリック可能]  [クリック可能]
```
- 各フォルダ部分をクリックしてそのフォルダに移動

#### 編集モード
- **ダブルクリック**: アドレスバーをダブルクリック
- **F2キー**: キーボードからF2を押す
```
編集前: C: ▶ Users ▶ Pictures
編集中: C:\Users\Pictures [テキスト編集可能]
```

### キーボードショートカット

| キー | 機能 |
|------|------|
| `F2` | アドレスバー編集モード |
| `Enter` | 編集確定 |
| `Esc` | 編集キャンセル |
| `Ctrl+Home` | ホームディレクトリへ移動 |
| `Alt+↑` | 親フォルダへ移動 |
| `Tab` | 次のブレッドクラムにフォーカス |
| `Shift+Tab` | 前のブレッドクラムにフォーカス |

### マウス操作

| 操作 | 機能 |
|------|------|
| **左クリック** | そのフォルダに移動 |
| **ダブルクリック** | 編集モード開始 |
| **ホバー** | ハイライト表示 |

## 🛠️ 技術仕様

### アーキテクチャ

```python
# 主要クラス構成
ui/controls.py
├── GimpStyleAddressButton    # 個別フォルダボタン
├── GimpStyleSeparator        # パス区切り文字
├── GimpStyleAddressBar       # メインアドレスバー
└── create_controls()         # ファクトリ関数
```

### 実装ファイル

- **`ui/controls.py`**: GIMP風アドレスバーの実装
- **`presentation/views/functional_new_main_view.py`**: 新UIでの統合
- **`window/main_window.py`**: レガシーUIでの統合

### スタイル定義

```css
/* ボタンスタイル */
QPushButton {
    padding: 4px 8px;
    border: none;
    background: transparent;
    color: #2e3436;
    border-radius: 2px;
}

QPushButton:hover {
    background: qlineargradient(...);
    border: 1px solid #a6a8aa;
}

/* コンテナスタイル */
QFrame {
    background: qlineargradient(...);
    border: 1px solid #a6a8aa;
    border-radius: 3px;
}
```

## 🎨 カスタマイズ

### 色の変更

```python
# ui/controls.py内のスタイル設定を変更
self.setStyleSheet("""
    QPushButton:hover {
        background: #your-color;  # ここを変更
    }
""")
```

### サイズの調整

```python
# ボタンの高さ変更
self.setFixedHeight(24)  # 24px → 他の値に変更

# 区切り文字の幅変更
self.setFixedWidth(12)   # 12px → 他の値に変更
```

## 🔧 トラブルシューティング

### よくある問題

#### Q: アドレスバーが表示されない
**A**: UI統合を確認してください
```python
# 正しいインポート
from ui.controls import create_controls

# 正しい統合
controls_widget, address_bar, parent_button = create_controls(
    self._on_address_changed, 
    self._go_to_parent_folder
)
```

#### Q: キーボードショートカットが効かない
**A**: フォーカス設定を確認してください
```python
# フォーカス設定
self.address_bar.setFocusPolicy(Qt.StrongFocus)
```

#### Q: パス検証でエラーが出る
**A**: パス存在チェックを確認してください
```python
if os.path.exists(new_path) and os.path.isdir(new_path):
    # パス変更処理
```

### ログ確認

```bash
# デバッグモードで起動
python main.py --debug

# ログファイル確認（Windows）
type logs\photomap_explorer.log
```

## 📚 関連ドキュメント

- [README.md](../README.md) - メインドキュメント
- [CHANGELOG.md](../CHANGELOG.md) - 変更履歴
- [CONTRIBUTING.md](../docs/CONTRIBUTING.md) - 開発ガイド

## 🎯 将来の改善予定

### v2.1.x+で予定している機能

- **お気に入りフォルダ**: ブックマーク機能
- **履歴機能**: 最近訪問したフォルダ
- **自動補完**: パス入力時の候補表示
- **ドラッグ&ドロップ**: フォルダのドラッグ操作
- **コンテキストメニュー**: 右クリックメニュー

---

*Last Updated: 2025-06-28*  
*PhotoMap Explorer 2.0.0 - GIMP風アドレスバー実装完了*
