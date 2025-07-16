# PhotoMap Explorer 実装ガイド（責任分離・統合版）

## 概要

PhotoMap Explorerは、写真のEXIF情報から撮影場所を抽出し、地図上に表示するPyQt5ベースの写真管理アプリケーションです。GIMP風のモダンなUI、16種類のテーマ対応（Theme Managerライブラリ利用）、高い保守性・拡張性を重視した責任分離構成を採用します。

---

## ディレクトリ構成（推奨・責任分離型）

```
photomap-explorer/
├── main.py                          # アプリケーションのエントリーポイント
├── core/                            # アプリ全体の基盤・設定
│   ├── app_context.py               # グローバル状態・依存性管理
│   ├── config.py                    # 設定・定数管理
│   └── theme_manager.py             # Theme Managerラッパー/統合
├── presentation/                    # プレゼンテーション層（UIロジック）
│   ├── main_window.py               # メインウィンドウ
│   ├── views/                       # 複数ビュー/パネル
│   │   ├── folder_panel.py          # フォルダ内容パネル
│   │   ├── thumbnail_panel.py       # サムネイルパネル
│   │   ├── preview_panel.py         # 画像プレビューパネル
│   │   ├── map_panel.py             # 地図パネル
│   │   └── status_panel.py          # 詳細情報パネル
│   └── dialogs/                     # ダイアログ群
│       └── folder_dialog.py         # カスタムフォルダ選択ダイアログ
├── ui/                              # UIコンポーネント（再利用可能な部品）
│   ├── controls/                    # コントロール群
│   │   ├── address_bar/             # ブレッドクラム式アドレスバー
│   │   │   ├── address_bar_core.py
│   │   │   ├── breadcrumb_manager.py
│   │   │   ├── text_input_handler.py
│   │   │   └── theme_integration.py
│   │   └── toolbar/                 # ツールバー
│   ├── thumbnail_list.py            # サムネイルリスト部品
│   ├── image_preview.py             # 画像プレビュー部品
│   └── map_widget.py                # 地図表示部品
├── logic/                           # ビジネスロジック・ドメイン層
│   ├── image_utils.py               # 画像処理・EXIF読取
│   ├── folder_utils.py              # フォルダ/ファイル操作
│   └── map_utils.py                 # 地図・位置情報処理
├── services/                        # サービス層（外部連携・永続化等）
│   └── exif_service.py              # EXIF/GPS情報抽出サービス
├── utils/                           # 汎用ユーティリティ
│   ├── debug_logger.py              # ログ出力
│   └── path_utils.py                # パス操作ユーティリティ
├── assets/                          # 静的リソース
│   ├── icons/                       # アイコン類
│   │   └── pme_icon.png
│   └── themes/                      # カスタムテーマファイル
├── tests/                           # テストコード
│   ├── unit/                        # ユニットテスト
│   └── integration/                 # 結合テスト
└── test_images/                     # テスト用画像
```

---

## 実装のポイント

### 1. Theme Manager統合
- `core/theme_manager.py`でTheme Managerのラッパーを用意し、全UIに一元適用。
- 16種類のテーマをサポートし、動的切り替え・コンポーネント単位の適用も可能。

### 2. UI/プレゼンテーション層
- `presentation/main_window.py`がアプリの中心。各種パネル（views/）やダイアログ（dialogs/）を組み合わせて構築。
- UI部品（ui/controls/など）は再利用性を重視し、責務ごとに細分化。
- GIMP風アドレスバーは`ui/controls/address_bar/`配下で分割実装。

### 3. ビジネスロジック・サービス
- 画像・フォルダ・地図処理は`logic/`配下で分離。
- EXIFやGPS抽出など外部依存は`services/`で管理。

### 4. ユーティリティ・リソース
- ログやパス操作などは`utils/`で一元化。
- アイコン・テーマ等の静的リソースは`assets/`に集約。

### 5. テスト
- ユニットテスト・結合テストを`tests/`で明示的に管理。

---

## 主要コンポーネント設計例

### main.py
```python
from core.app_context import AppContext
from presentation.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
import sys

def main():
    app_context = AppContext()
    app = QApplication(sys.argv)
    window = MainWindow(app_context)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
```

### GIMP風アドレスバー（ui/controls/address_bar/）
- `address_bar_core.py` ... メインUI・状態管理
- `breadcrumb_manager.py` ... パス分解・ボタン生成・省略処理
- `text_input_handler.py` ... テキスト入力モード管理
- `theme_integration.py` ... Theme Manager連携

#### シグナル例
```python
# AddressBarCore
path_changed = pyqtSignal(str)
# BreadcrumbManager
navigation_requested = pyqtSignal(str)
# TextInputHandler
input_confirmed = pyqtSignal(str)
input_cancelled = pyqtSignal()
```

---

## 実装ガイドライン

- **責任分離**: UI・ロジック・サービス・ユーティリティを明確に分離。
- **拡張性**: 新機能追加やUI部品の差し替えが容易な構成。
- **テスト容易性**: 各層ごとにテスト可能な設計。
- **クロスプラットフォーム**: Windows/macOS/Linux対応、パス処理やフォントも考慮。
- **パフォーマンス**: サムネイル生成や地図描画は非同期・キャッシュ活用。
- **エラーハンドリング**: 例外処理・ログ出力を徹底。

---

## 依存関係

- PyQt5>=5.15.0
- Pillow>=8.0.0
- exifread>=2.3.0
- Theme Manager（https://github.com/scottlz0310/Theme-Manager）

---

## 開発・実装順序（推奨）

1. **基盤構築**
   - Theme Manager統合、設定・依存性管理
2. **UI骨組み**
   - main_windowと各パネル・ダイアログの配置
3. **コアUI部品実装**
   - GIMP風アドレスバー、サムネイルリスト、プレビュー、地図
4. **ビジネスロジック実装**
   - 画像・EXIF・GPS処理、フォルダ操作
5. **サービス・外部連携**
   - EXIF/GPS抽出サービス
6. **テスト・デバッグ**
   - ユニット・結合テスト、UI/UX調整

---

## 参考: GIMP風アドレスバー仕様要点
- ブレッドクラム表示・テキスト入力切替・省略記号・Windows/Unixパス対応
- Theme Managerによる16テーマ対応・動的切替
- シグナル/イベント設計、エラーハンドリング、パフォーマンス要件

---

このドキュメントに従えば、AIや開発者が責任分離・拡張性・保守性に優れたPhotoMap Explorerを効率的に構築できます。
