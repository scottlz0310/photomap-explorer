# PyQt5 GIMP風アドレスバーコンポーネント実装プロンプト

## 要件概要
PyQt5アプリケーション用のGIMP風ブレッドクラムアドレスバーコンポーネントを実装してください。新しいTheme Managerライブラリ（https://github.com/scottlz0310/Theme-Manager）を使用してテーマ管理を行います。

## 機能要件

### 1. ブレッドクラム表示
- パスをボタン形式で表示（例: `[C:]` `[Users]` `[Documents]` `[Photos]`）
- 各ボタンをクリックすることでそのパスに移動可能
- 画面幅が不足する場合は省略記号（`...`）を使用して、末尾側を優先表示
- Windows（ドライブレター）とUnix系パスの両方に対応

### 2. テキスト入力モード
- 編集ボタン（📝）をクリックでテキスト入力モードに切り替え
- テキストボックスでパスを直接編集可能
- Enter キーまたは確定ボタン（✓）で確定
- Escape キーで編集をキャンセル
- テキスト内容に応じて動的に幅を調整

### 3. テーマ対応
- Theme Managerライブラリを使用したテーマ管理
- ダークテーマ、ライトテーマ、その他16種類のテーマに対応
- テーマ変更時の動的スタイル更新

## 技術仕様

### Theme Manager ライブラリの使用
```python
# Theme Manager の基本的な使用方法
from theme_manager.qt.controller import ThemeController

# テーマコントローラーの初期化
controller = ThemeController()

# ウィジェットにテーマを適用
controller.apply_theme_to_widget(widget)

# 利用可能なテーマの取得
themes = controller.get_available_themes()

# テーマの変更
controller.set_theme("dark")
```

### クラス構成
以下の3つのクラスに分割して実装してください：

#### 1. AddressBarCore (メインクラス)
```python
class AddressBarCore(QWidget):
    """
    GIMP風アドレスバーのメイン機能
    """
    path_changed = pyqtSignal(str)  # パス変更シグナル
    
    def __init__(self, parent=None):
        # 初期化処理
        
    def setup_ui(self):
        # UI初期化
        
    def setText(self, path: str):
        # パスを設定
        
    def text(self) -> str:
        # 現在のパスを取得
        
    def apply_theme(self, theme_name: str):
        # テーマを適用
```

#### 2. BreadcrumbManager (ブレッドクラム管理)
```python
class BreadcrumbManager(QObject):
    """
    ブレッドクラムの表示とナビゲーション管理
    """
    navigation_requested = pyqtSignal(str)
    
    def analyze_path(self, path: str) -> List[dict]:
        # パスを分析してブレッドクラム要素を生成
        
    def create_navigation_button(self, element: dict) -> QPushButton:
        # ナビゲーションボタンを作成
        
    def calculate_optimal_display(self, elements: List[dict], available_width: int) -> List[dict]:
        # 省略記号を考慮した最適表示を計算
```

#### 3. TextInputHandler (テキスト入力管理)
```python
class TextInputHandler(QObject):
    """
    テキスト入力モードの管理
    """
    input_confirmed = pyqtSignal(str)
    input_cancelled = pyqtSignal()
    
    def setup_text_input(self, parent: QWidget) -> QLineEdit:
        # テキスト入力フィールドをセットアップ
        
    def enter_edit_mode(self, current_path: str):
        # 編集モードに入る
        
    def exit_edit_mode(self):
        # 編集モードを終了
```

## UI仕様

### レイアウト構成
```
[ブレッドクラムエリア                           ] [📝]
[テキスト入力エリア（編集モード時のみ表示）      ] [✓]
```

### ボタンスタイル
- 通常ボタン: 境界線付き、ホバー時に強調
- カレントボタン: 異なる色で強調表示
- 省略記号ボタン: 小さめサイズ、ツールチップで省略内容を表示

### テキスト入力
- プレースホルダー: "フォルダパスを入力してください"
- フォント: Consolas, Monaco, Courier New (monospace)
- 自動幅調整: 最小300px、最大800px、内容に応じて動的調整

## パス処理仕様

### Windows パス対応
- ドライブレター認識 (`C:\`, `D:\` など)
- UNCパス対応 (`\\server\share`)
- パス区切り文字の正規化

### Unix パス対応  
- ルートパス処理 (`/`)
- 隠しファイル・フォルダの考慮
- シンボリックリンクの処理

### 安全性
以下のシステムフォルダへのアクセスを制限：
- `/proc`, `/sys`, `/dev`, `/run`, `/media`
- `/mnt/wslg`, `/mnt/wsl` (WSL環境)

## イベント処理

### シグナル定義
```python
# AddressBarCore のシグナル
path_changed = pyqtSignal(str)  # パス変更時

# BreadcrumbManager のシグナル  
navigation_requested = pyqtSignal(str)  # ナビゲーション要求

# TextInputHandler のシグナル
input_confirmed = pyqtSignal(str)  # 入力確定
input_cancelled = pyqtSignal()    # 入力キャンセル
```

### キーイベント
- `Enter`: テキスト入力確定
- `Escape`: 編集モードキャンセル
- `Tab`: フォーカス移動

## テーマ設定例

### Theme Manager設定の活用
```python
# テーマ設定からボタンスタイルを取得
theme_data = controller.get_current_theme_data()
button_config = theme_data.get('button', {})

# スタイル適用
button_style = f"""
QPushButton {{
    background-color: {button_config.get('background', '#f0f0f0')};
    color: {button_config.get('text', '#000000')};
    border: 1px solid {button_config.get('border', '#d0d0d0')};
    border-radius: 4px;
    padding: 4px 12px;
    margin: 1px;
}}
QPushButton:hover {{
    background-color: {button_config.get('hover', '#e0e0e0')};
}}
"""
```

## エラーハンドリング

### ログ出力
```python
import logging

# エラーレベルでの出力
logging.error(f"パス設定エラー: {e}")

# デバッグレベルでの出力（開発時のみ）
logging.debug(f"ブレッドクラム更新: path='{path}'")
```

### 例外処理
- ファイルシステムアクセスエラー
- PyQt オブジェクト削除エラー
- テーマ適用エラー

## パフォーマンス要件

### レスポンス性
- パス変更時の応答時間: 100ms以内
- テーマ変更時の更新時間: 200ms以内
- 大量フォルダ（1000+）での動作保証

### メモリ効率
- ボタンの適切な削除と再作成
- イベントリスナーのリーク防止
- テーマリソースの適切な管理

## テスト要件

### 基本機能テスト
```python
def test_path_setting():
    # パス設定の動作確認
    
def test_breadcrumb_navigation():
    # ブレッドクラムナビゲーションの確認
    
def test_text_input_mode():
    # テキスト入力モードの動作確認
    
def test_theme_switching():
    # テーマ切り替えの確認
```

### エッジケーステスト
- 空パス処理
- 存在しないパス処理
- 特殊文字を含むパス処理
- 非常に長いパス処理

## ファイル構成

```
ui/controls/address_bar/
├── __init__.py              # 統合インターフェース
├── address_bar_core.py      # メインクラス
├── breadcrumb_manager.py    # ブレッドクラム管理
├── text_input_handler.py    # テキスト入力管理
└── theme_integration.py     # テーマ統合ヘルパー
```

## 依存関係

### 必須ライブラリ
```python
# PyQt5
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLineEdit, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QFont

# Theme Manager
from theme_manager.qt.controller import ThemeController

# 標準ライブラリ
import os
import logging
from typing import List, Optional, Dict
```

### インストール手順
```bash
# Theme Manager ライブラリのインストール
git clone https://github.com/scottlz0310/Theme-Manager
cd Theme-Manager
pip install -e .
```

## 実装上の注意点

### PyQt オブジェクト管理
- 親ウィジェットの明示的指定
- `deleteLater()` の適切な使用
- C++ オブジェクトの有効性チェック

### Theme Manager 統合
- テーマコントローラーのシングルトン使用
- テーマ変更イベントの購読
- フォールバックスタイルの提供

### クロスプラットフォーム対応
- OS固有のパス処理の分離
- フォント選択の環境別対応
- ファイルシステム権限の考慮

この仕様に従って、保守性が高く、拡張可能なGIMP風アドレスバーコンポーネントを実装してください。Theme Managerライブラリの機能を最大限活用し、16種類のテーマに対応した美しいUIを提供してください。
