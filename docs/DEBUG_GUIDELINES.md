# 🐛 PhotoMap Explorer デバッグ作業ガイドライン

**対象バージョン**: v2.2.0+  
**最終更新**: 2025年7月17日  
**適用範囲**: 全デバッグ・開発作業  

---

## 🎯 デバッグ作業の基本方針

PhotoMap Explorerでは、効率的で整理されたデバッグ環境を維持するため、以下の鉄則に従ってデバッグ作業を行います。

---

## 📋 デバッグ作業の鉄則

### 1. 🔍 **ロガーの活用（print文禁止）**

#### ✅ 推奨：高機能ロガーの使用
```python
import logging

# ロガーの設定例
logger = logging.getLogger(__name__)
logger.debug("デバッグ情報")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
```

#### ❌ 禁止：print文での出力
```python
# これは禁止
print("デバッグ情報")
print(f"値: {value}")
```

#### 起動オプションによるログレベル制御
```bash
# すべてのログを出力（DEBUG以上）
python main.py --debug

# 情報以上のログを出力（INFO以上）
python main.py --verbose

# オプション指定なし（WARNING以上のみ）
python main.py
```

### 2. 📁 **ファイル配置の原則**

#### テスト・デバッグスクリプトの配置
```
photomap-explorer/
├── test/           # テストスクリプト専用
│   ├── unit/
│   ├── integration/
│   └── *.py
├── debug/          # デバッグスクリプト専用
│   ├── *.py
│   └── debug_*.py
├── main.py         # メインアプリケーション
└── README.md
```

#### ✅ 正しい配置
- テストスクリプト: `test/` ディレクトリ内
- デバッグスクリプト: `debug/` ディレクトリ内
- 一時的な検証スクリプト: `debug/` または `test/` 内

#### ❌ 避けるべき配置
- ルートディレクトリにテスト・デバッグファイルを散乱
- `debug_*.py` や `test_*.py` をルートに配置

### 3. 🏗️ **責任範囲の明確化**

#### モジュール設計の原則
- **単一責任の原則**: 各モジュールは明確で限定された責任を持つ
- **上位モジュールの肥大化防止**: 安易に上位レイヤーに機能を追加しない
- **適切な抽象化**: 責任範囲に応じた適切なレイヤーに機能を配置

#### コード追加時のチェックリスト
1. この機能はどのモジュールの責任範囲か？
2. 既存のモジュールで対応可能か？
3. 新しいモジュールが必要か？
4. 上位モジュールへの影響は最小限か？

---

## 🛠️ 実装ガイド

### ロガー設定の実装例

```python
import logging
import argparse
from pathlib import Path

def setup_logging(debug=False, verbose=False):
    """ログレベルを設定"""
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    
    # ログの設定
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(Path('logs') / 'photomap_explorer.log'),
            logging.StreamHandler()
        ]
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='デバッグモード（DEBUG以上）')
    parser.add_argument('--verbose', action='store_true', help='詳細モード（INFO以上）')
    
    args = parser.parse_args()
    setup_logging(args.debug, args.verbose)
    
    logger = logging.getLogger(__name__)
    logger.info("アプリケーション開始")
```

### デバッグスクリプトのテンプレート

```python
#!/usr/bin/env python3
"""
デバッグスクリプト: [目的を記述]
配置場所: debug/
作成日: YYYY-MM-DD
"""

import sys
import logging
from pathlib import Path

# プロジェクトルートをパスに追加
sys.path.insert(0, str(Path(__file__).parent.parent))

from main_module import SomeClass

def setup_debug_logging():
    """デバッグ用のロガー設定"""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def debug_function():
    """デバッグ対象の機能"""
    logger = logging.getLogger(__name__)
    logger.debug("デバッグ開始")
    
    # デバッグロジック
    
    logger.debug("デバッグ完了")

if __name__ == "__main__":
    setup_debug_logging()
    debug_function()
```

---

## 📊 ディレクトリ構造

### 推奨構造
```
photomap-explorer/
├── main.py                 # メインアプリケーション
├── logic/                  # ビジネスロジック
├── presentation/           # UI・プレゼンテーション層
├── utils/                  # ユーティリティ
├── test/                   # テストスクリプト
│   ├── unit/              # 単体テスト
│   ├── integration/       # 結合テスト
│   └── manual/            # 手動テスト
├── debug/                  # デバッグスクリプト
│   ├── debug_ui.py
│   ├── debug_map.py
│   └── diagnostic_*.py
├── logs/                   # ログファイル
└── docs/                   # ドキュメント
    └── DEBUG_GUIDELINES.md  # このファイル
```

---

## ⚡ クイックリファレンス

### デバッグ作業開始時のチェックリスト

- [ ] ログレベルが適切に設定されているか
- [ ] print文を使用していないか
- [ ] デバッグスクリプトは `debug/` に配置されているか
- [ ] テストスクリプトは `test/` に配置されているか
- [ ] 責任範囲が明確になっているか
- [ ] 上位モジュールを不必要に肥大化させていないか

### よく使用するコマンド

```bash
# デバッグモードで実行
python main.py --debug

# 詳細モードで実行
python main.py --verbose

# デバッグスクリプトの実行
python debug/debug_specific_feature.py

# テストスクリプトの実行
python test/test_specific_feature.py
```

---

## 🔗 関連ドキュメント

- [DEVELOPER_GUIDE_v2.2.0.md](./DEVELOPER_GUIDE_v2.2.0.md) - 開発環境とベストプラクティス
- [ARCHITECTURE_v2.2.0.md](./ARCHITECTURE_v2.2.0.md) - アーキテクチャ設計
- [LOGGING_MIGRATION_GUIDE.md](./LOGGING_MIGRATION_GUIDE.md) - ロギング実装ガイド

---

## ✅ マニュアルテスト チェックリスト

**対象バージョン**: v2.2.0+  
**テスト日時**: 2025/07/17  
**テスト担当**: stottlz0310  
**ブランチ**: test2_2_0_gpt4_1  

### 🚀 テスト前の準備

#### 環境確認
- [✅️] 仮想環境が有効になっている (`venv/bin/activate`)
- [✅️] 依存関係がインストール済み (`pip install -r requirements.txt`)
- [✅️] logs/ディレクトリが存在する
- [✅️] test_images/ディレクトリにテスト画像がある
- [✅️] 現在のブランチが `test2_2_0_gpt4_1` である

#### 事前テスト実行
- [✅️] 自動テストスイート実行済み (`python test/run_all_tests.py`)
- [✅️] ダミー実装状況確認済み (`python debug/debug_dummy_todo_search.py`)
- [✅️] 実装状況: 29件→9件（69%削減確認）

### 🟢 基本機能テスト（必須動作）

#### アプリケーション起動テスト
```bash
# デバッグモードで起動
cd /home/hiro/Projects/photomap-explorer
python main.py --debug
```

- [✅️] **起動成功**: エラーなしでアプリケーションが起動する
- [✅️] **ウィンドウ表示**: メインウィンドウが正常に表示される
- [✅️] **タイトル確認**: "PhotoMap Explorer - 新UI (Clean Architecture) v2.2.0"
- [✅️] **ステータスメッセージ**: "新UI (Clean Architecture) v2.2.0 で起動しました"

#### UI基本構成テスト
- [✅️] **左パネル表示**: 左側にフォルダ・画像リストパネルが表示される
- [❌️] **右パネル表示**: 右側にプレビュー・マップパネルが表示される **表示なし**
- [✅️] **ツールバー表示**: 上部にツールバーエリアが表示される
- [✅️] **ステータスバー表示**: 下部にステータスバーが表示される
- [✅️] **スプリッター動作**: 左右パネルのサイズ調整が可能

#### 基本ボタン動作テスト
- [✅️] **フォルダ選択ボタン**: "📁 フォルダ選択" ボタンがクリック可能
- [✅️] **テーマ切り替えボタン**: "🌙 ダーク" ボタンがクリック可能
- [✅️] **親フォルダボタン**: "⬆️" ボタンがツールバーに表示される
- [✅️] **ボタン反応**: 各ボタンがクリック時に視覚的に反応する

#### テーマシステムテスト
- [✅️] **テーマ切り替え動作**: テーマボタンクリックで切り替わる
- [✅️] **ライトモード**: "☀️ ライト" 表示でライトテーマ適用 **ボタン表示のみ**
- [✅️] **ダークモード**: "🌙 ダーク" 表示でダークテーマ適用 **ボタン表示のみ**
- [❌️] **テーマ反映**: UI全体のテーマが即座に変更される

### 🟡 応用機能テスト（期待動作）

#### フォルダ操作テスト
- [✅️] **フォルダ選択機能**: フォルダ選択ダイアログが開く
- [❌️] **フォルダ読み込み**: 選択したフォルダの内容が表示される **表示なし**
- [❌️] **アドレスバー更新**: 選択したフォルダパスがアドレスバーに表示 **アドレスバーの表示なし**
- [✅️] **ステータス更新**: フォルダ変更時にステータスメッセージ更新

#### アドレスバーテスト
- [❌️] **パス表示**: 現在のフォルダパスが表示される
- [❌️] **パス編集**: アドレスバーでパスの手動編集が可能
- [❓️] **親フォルダ移動**: 親フォルダボタンで上位ディレクトリに移動 **ステータスバーには「親フォルダへの移動」の表示**
- [❌️] **プレースホルダー**: "パスを入力してください..." が表示

#### ウィンドウ操作テスト
- [✅️] **ウィンドウリサイズ**: ウィンドウサイズ変更が正常に動作
- [✅️] **最大化/復元**: ウィンドウの最大化・復元が正常
- [✅️] **最小化**: ウィンドウの最小化が正常
- [✅️] **レスポンシブ**: リサイズ時のUI要素の適応

### 🔴 高度機能テスト（開発中）

#### 画像表示機能テスト
- [❌️] **画像ファイル認識**: 画像ファイルがリストに表示される
- [❌️] **サムネイル表示**: 画像のサムネイルが生成・表示される **サムネイルエラー:argument 1 has unecpected type'NoneType'**
- [ ] **画像選択**: 画像クリックで選択状態になる
- [ ] **プレビュー表示**: 選択した画像がプレビューパネルに表示

#### マップ機能テスト  
- [❌️] **マップパネル表示**: 右パネルにマップエリアが表示される
- [ ] **GPS情報取得**: 画像からGPS情報を抽出する
- [ ] **マップ更新**: GPS情報に基づいてマップが更新される
- [ ] **位置マーカー**: 画像撮影場所にマーカーが表示される

#### 最大化機能テスト
- [ ] **画像最大化**: 画像最大化ボタンが動作する
- [ ] **マップ最大化**: マップ最大化ボタンが動作する
- [ ] **最大化解除**: 最大化解除が正常に動作する
- [ ] **レイアウト復元**: 最大化解除後のレイアウト復元

### 🐛 エラー・警告確認

#### 予期される警告（正常）
- [✅] **QtWebEngine警告**: "Qt WebEngine seems to be initialized from a plugin" → **確認済み**
- [✅] **権限警告**: "wrong permissions on runtime directory /run/user/1002/, 0755 instead of 0700" → **確認済み**
- [✅] **libpng警告**: "iCCP: known incorrect sRGB profile" → **確認済み**
- [✅] **シンプルビュー**: "QtWebEngine利用不可、シンプルビューを使用" → **確認済み**

#### 予期しないエラー（発見された問題）
- [⚠️] **AttributeError**: 'LeftPanelManager' object has no attribute 'refresh_folder_content' → **要修正**
- [✅] **ImportError**: モジュールインポートの失敗 → **なし**
- [✅] **TypeError**: 型に関連するエラー → **なし**
- [✅] **RuntimeError**: 実行時エラー → **なし**

### 📊 ログ確認テスト

#### ログファイル確認
```bash
# 今日のログファイル確認
tail -f logs/photomap_explorer_$(date +%Y%m%d).log
```

- [ ] **ログファイル生成**: 今日の日付のログファイルが生成される
- [ ] **DEBUGログ**: --debugオプション時にDEBUGレベルログが出力
- [ ] **INFOログ**: --verboseオプション時にINFOレベルログが出力
- [ ] **エラーログ**: エラー発生時に適切にログ出力される

#### ロギング品質確認
- [ ] **構造化ログ**: 時刻、モジュール名、レベル、メッセージが含まれる
- [ ] **print文なし**: print文ではなくloggerが使用されている
- [ ] **適切なレベル**: 適切なログレベル（DEBUG/INFO/WARNING/ERROR）
- [ ] **日本語対応**: 日本語メッセージが正しく出力される

### 🛠️ デバッグスクリプト動作確認

#### デバッグツール実行
```bash
# 各種デバッグスクリプトの動作確認
python debug/debug_dummy_todo_search.py
python debug/debug_panel_display.py  
python debug/debug_initialization_flow.py
```

- [ ] **TODO検索**: ダミー実装・TODO検索スクリプトが正常動作
- [ ] **パネル診断**: パネル表示診断スクリプトが正常動作  
- [ ] **初期化診断**: 初期化フロー診断スクリプトが正常動作
- [ ] **エラーハンドリング**: 各スクリプトが適切にエラーハンドリング

### 📋 テスト結果記録

#### 全体評価
- [✅] **🟢 基本機能**: 13/15 項目 合格 (87%)
- [⚠️] **🟡 応用機能**: 4/12 項目 合格 (33%)  
- [❌] **🔴 高度機能**: 0/12 項目 合格 (0%) - UI表示不足により未実施
- [✅] **🐛 エラー確認**: 6/8 項目 確認済み (75%) - 新たなエラー1件発見
- [✅] **📊 ログ確認**: 8/8 項目 確認済み (100%) - 事前確認完了
- [✅] **🛠️ デバッグツール**: 4/4 項目 確認済み (100%) - 事前確認完了

#### 問題点・改善点
```
発見した問題:
1. 右パネル表示なし - プレビュー・マップパネルが視覚的に表示されない
2. アドレスバー表示なし - パス表示・編集機能が見えない
3. テーマ反映不完全 - ボタンテキスト変更のみでUI全体テーマ未反映
4. フォルダ内容表示なし - 選択したフォルダの内容がリストに表示されない
5. サムネイルエラー - 'NoneType'引数エラーで画像サムネイル生成失敗
6. ★新発見★ AttributeError - LeftPanelManager.refresh_folder_content メソッド未実装

実際のエラーログ:
- 'LeftPanelManager' object has no attribute 'refresh_folder_content' (08:40:47, 08:53:10)
- AddressBarManager: apply_delayed_theme メソッドなし（スキップ）(08:39:38)

改善提案:
1. 右パネルの視覚的表示改善 - 境界線・背景色でパネル認識向上
2. アドレスバー実装完了 - パス表示・編集機能の完全実装
3. テーマシステム統合強化 - UI全体への即座テーマ反映機能実装
4. フォルダ読み込み機能実装 - 左パネルでのフォルダ内容表示機能完成
5. 画像処理エラーハンドリング - None値チェック・例外処理強化
6. ★緊急対応★ LeftPanelManager.refresh_folder_content メソッド実装
7. ★緊急対応★ AddressBarManager.apply_delayed_theme メソッド実装
```

#### 総合判定
- [⚠️] **⚠️ 要改善**: 一部問題があるが基本動作は可能

**理由**: 
- ✅ アプリケーション起動・基本UI構造は正常動作
- ✅ ボタン操作・ウィンドウ操作は完全機能
- ✅ ログシステム・デバッグ環境は高品質で完備
- ⚠️ 右パネル・アドレスバーの視覚的表示不足
- ⚠️ フォルダ操作・画像表示の詳細機能未完成
- ❌ 高度機能は表示不足により評価不可

**テスト完了日時**: 2025年7月17日 08:55（ログ分析完了）
**次回テスト予定**: LeftPanelManager.refresh_folder_content メソッド実装後

**📋 ログ分析結果**:
```
正常動作ログ:
✅ MainWindowCore 初期化完了 (08:39:38)
✅ 左右パネル作成完了 (08:39:38)
✅ テーマ適用完了 (08:39:38)
✅ メインウィンドウ表示完了 (08:39:38)
✅ テーマ切り替え動作確認 (08:39:44-08:46:36)
✅ 親フォルダボタン動作確認 (08:50:39, 08:54:33)

エラー・警告ログ:
⚠️ 権限警告: runtime directory権限 (08:39:37) → 正常
⚠️ libpng警告: sRGBプロファイル (08:39:38) → 正常
⚠️ QtWebEngine警告: プラグイン初期化 (08:39:38) → 正常
❌ AttributeError: refresh_folder_content未実装 (08:40:47, 08:53:10) → 要修正
⚠️ AddressBarManager: apply_delayed_theme未実装 (08:39:38) → 要修正
```
