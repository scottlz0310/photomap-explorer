# 🗑️ レガシーUI廃止計画

**作成日**: 2025年7月2日  
**ステータス**: 実施準備中  
**対象バージョン**: v2.2.0以降  

## 📋 概要

PhotoMapExplorerは現在、新UI（Clean Architecture）が安定稼働しており、レガシーUIは廃止可能な状態です。第3回コードリファクタリング前に、不要なファイル・コードを削除してプロジェクトを整理します。

## 🎯 削除計画の目標

1. **コードベースの簡素化**: レガシーUIコードの完全削除
2. **メンテナンス負荷軽減**: 重複実装の排除
3. **開発効率向上**: 単一UI実装への集約
4. **プロジェクト構造最適化**: Clean Architecture構造の明確化

## 🔍 現状分析

### ✅ 現在のエントリーポイント
- **`main.py`**: 新UI (`FunctionalNewMainWindow`) のみを起動 - **保持**
- **`main_hybrid.py`**: 空ファイル - **削除対象**

### 🏛️ レガシーUI関連ファイル（削除対象）

#### 1. メインウィンドウ実装
- **`window/main_window.py`** (266行) - レガシーMainWindow実装
- **`main_window.py`** (ルート) - 古いMainWindow（存在確認要）

#### 2. アーカイブディレクトリ
- **`archive/backups/`** - 全バックアップファイル群
  - `backup_phase5_2_20250628/main.py` - ハイブリッドUI起動スクリプト
  - `backup_phase5_2_20250628_020731/main.py` - バックアップ起動スクリプト
  - その他バックアップファイル群

#### 3. 開発テストファイル群
- **`archive/development_tests/`** - フェーズ別テストファイル群
  - `test_phase4_final.py` - ハイブリッドUI統合テスト
  - `test_phase4_hybrid.py` - ハイブリッドテスト
  - `test_phase*.py` - 段階的開発テストファイル群
  - その他実験的テストファイル

### 🚀 新UI関連ファイル（保持・改善対象）

#### 主要ファイル
- **`presentation/views/functional_new_main_view.py`** (1690行) - **第3回リファクタリング対象**
- **`presentation/views/main_view.py`** - Clean Architecture版ビュー
- **`presentation/controllers/main_controller.py`** - メインコントローラー
- **`presentation/viewmodels/main_viewmodel.py`** - ビューモデル

## 📅 削除実施フェーズ

### 🚨 Phase 1: 緊急削除（即座実施可能）
**リスク**: 低 | **工数**: 0.5日

```
削除対象:
├── main_hybrid.py (空ファイル)
├── archive/backups/ (全バックアップ)
│   ├── backup_phase5_2_20250628/
│   ├── backup_phase5_2_20250628_020731/
│   └── backup_phase5_2_20250730/ (あれば)
└── archive/development_tests/ (実験的テストファイル)
    ├── test_phase4_*.py
    ├── test_phase2.py
    ├── test_phase3.py
    └── simple_test_*.py
```

### ⚠️ Phase 2: 慎重削除（要検証）
**リスク**: 中 | **工数**: 1日

```
削除対象:
├── window/main_window.py (レガシーMainWindow)
├── main_window.py (ルート、存在確認要)
└── archive/development_tests/ (残存テストファイル)
    ├── test_*.py (新UI関連以外)
    └── test_ui_*.py (UI修正テスト)
```

**必要作業**:
- `window/main_window.py` の参照チェック
- インポート文の洗い出し
- 依存関係の確認

### 🔧 Phase 3: コード整理（リファクタリング準備）
**リスク**: 低 | **工数**: 0.5日

```
整理対象:
├── 未使用インポート文の削除
├── デッドコードの除去
└── コメントアウトされたレガシーコードの削除
```

## 🛡️ 安全対策

### 事前バックアップ
- 削除前に全体のGitコミット実行
- 重要ファイルの個別バックアップ

### 段階的実施
1. Phase 1実施後の動作確認
2. Phase 2実施後の包括的テスト
3. エラー発生時の即座ロールバック

### 確認手順
```bash
# 1. 現在の動作確認
python main.py

# 2. ビルドテスト
python -m build

# 3. 実行ファイル生成テスト
pyinstaller photomap-explorer.spec
```

## 🔍 削除前チェックリスト

### Phase 1実施前
- [ ] 現在のmain.pyの正常動作確認
- [ ] アーカイブディレクトリの内容確認
- [ ] Gitの現在状態をコミット

### Phase 2実施前
- [ ] `window/main_window.py`の参照箇所検索
- [ ] インポート依存関係の確認
- [ ] レガシーUI使用箇所の有無確認

### Phase 3実施前
- [ ] コードベース全体の静的解析
- [ ] 未使用インポートの特定
- [ ] デッドコードの特定

## 📈 期待効果

### 削除後の改善
- **ファイル数削減**: 約30-40ファイル削除予定
- **コードベースサイズ**: 20-30%削減見込み
- **ビルド時間短縮**: 依存関係簡素化
- **保守性向上**: 単一UI実装への集約

### 第3回リファクタリングへの効果
- **集中対象明確化**: `functional_new_main_view.py`への集中
- **クリーンな開始**: 不要コードのない状態でのリファクタリング
- **テスト環境簡素化**: 新UI専用テストスイート構築

## ⚠️ 注意事項

### 削除禁止ファイル
- **`main.py`** - 現在のエントリーポイント
- **`presentation/views/functional_new_main_view.py`** - 現在のメインUI
- **`ui/`ディレクトリ** - UIコンポーネント群
- **`domain/`ディレクトリ** - Clean Architectureドメイン層
- **`infrastructure/`ディレクトリ** - インフラストラクチャ層

### 削除後の第3回リファクタリング準備
1. **`functional_new_main_view.py`分割計画の詳細化**
2. **テストスイート構築準備**
3. **Clean Architecture準拠度確認**

## 📝 実施ログ

### 実施予定
- **Phase 1**: 2025年7月3日予定
- **Phase 2**: 2025年7月4日予定  
- **Phase 3**: 2025年7月5日予定

### 完了記録
<!-- 実施後に記録 -->

---

**備考**: このドキュメントは第3回コードリファクタリング計画（`docs/THIRD_REFACTORING_PLAN.md`）と連携して実施されます。レガシーUI削除完了後、直ちに`functional_new_main_view.py`の分割作業に移行します。
