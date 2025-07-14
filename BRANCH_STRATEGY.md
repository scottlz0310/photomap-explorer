# PhotoMap Explorer ブランチ戦略・マージ手順

## 📊 現在のブランチ構成（2025年7月15日時点）

```
main (デフォルトブランチ)
  └── refact3.0 (V2.2リファクタリング作業 - 完了済み)
        └── fullrebld3.0 (V3.0完全再構築 - 作業中) ← 現在位置
```

## 🔄 ブランチの役割と経緯

### main
- **役割**: 安定版のメインブランチ
- **状態**: V2.1.2までの安定実装

### refact3.0  
- **役割**: V2.2のリファクタリング作業
- **内容**: 既存コードの整理、構造改善、バグ修正
- **状態**: 完了済み（アーカイブ扱い）

### fullrebld3.0 ← 現在の作業ブランチ
- **役割**: V3.0の完全再構築
- **内容**: Theme Manager統合、新アーキテクチャでの全面実装
- **状態**: 作業中

## 🗂️ コード整理状況

### V2.2実装のアーカイブ化（完了）
```
archive/V2.2/
├── logic/              # ビジネスロジック
├── presentation/       # プレゼンテーション層
├── ui/                # UIコンポーネント
├── utils/             # ユーティリティ
├── settings/          # 設定ファイル
├── main.py            # エントリーポイント
├── requirements.txt   # 依存関係
├── test/              # テストファイル群
├── debug/             # デバッグスクリプト群
└── README.md          # V2.2説明書
```

### 現在のルート構成（整理後）
```
./
├── docs/                      # ドキュメント
├── assets/                    # リソース
├── test_images/              # テスト用画像
├── archive/                  # 過去バージョン
├── IMPLEMENTATION_PROMPT_*.md # 実装仕様書
├── BRANCH_STRATEGY.md        # このファイル
└── （その他設定ファイル）
```

## 🎯 推奨マージ戦略

### 選択肢1: 直接マージ（推奨）

**手順**:
```bash
# V3.0実装完了後
git checkout main
git merge fullrebld3.0
git tag v3.0.0
git push origin main --tags

# クリーンアップ（オプション）
git branch -d refact3.0
git push origin --delete refact3.0
```

**メリット**:
- mainブランチがクリーンに保たれる
- V3.0が明確にV2.xからの大きな変更として位置づけられる
- 中間のリファクタリング作業を履歴として残しつつ、mainには影響しない

### 選択肢2: 段階的マージ

**手順**:
```bash
# 1段階目: refact3.0をmainにマージ
git checkout main
git merge refact3.0
git tag v2.2.0

# 2段階目: fullrebld3.0をmainにマージ
git merge fullrebld3.0
git tag v3.0.0
git push origin main --tags
```

**メリット**:
- V2.2とV3.0のバージョンが明確に分離される
- 段階的な変更履歴が保持される

## ✅ 推奨アプローチ

**選択肢1（直接マージ）を推奨**

### 理由
1. **V2.2コードは既にアーカイブ済み** - `archive/V2.2/`に保存
2. **V3.0は完全な新アーキテクチャ** - 継続性よりも刷新性を重視
3. **Theme Manager統合** - 外部ライブラリ依存の大きな変更
4. **履歴の明確性** - mainブランチには安定版のみを残す

## 📋 V3.0完成時のチェックリスト

### 実装完了確認
- [ ] Theme Manager統合完了
- [ ] GIMP風アドレスバー実装完了
- [ ] メインアプリケーション実装完了
- [ ] 基本機能テスト完了
- [ ] ドキュメント更新完了

### マージ準備
- [ ] 最終コミットの実行
- [ ] ブランチの状態確認
- [ ] テストの最終実行

### マージ実行
```bash
# 最終確認
git status
git log --oneline -5

# mainブランチに切り替え
git checkout main
git pull origin main  # 最新状態に更新

# マージ実行
git merge fullrebld3.0

# タグ付け
git tag -a v3.0.0 -m "V3.0.0: Complete rebuild with Theme Manager integration"

# プッシュ
git push origin main
git push origin v3.0.0
```

### クリーンアップ（オプション）
```bash
# ローカルブランチ削除
git branch -d refact3.0
git branch -d fullrebld3.0

# リモートブランチ削除
git push origin --delete refact3.0
# fullrebld3.0は作業完了の記録として保持推奨
```

## 🚨 注意事項

### バックアップ
- マージ前に現在の状態をバックアップ
- 重要な変更がある場合は追加のアーカイブを作成

### 依存関係
- Theme Managerライブラリの動作確認
- 新しいrequirements.txtの妥当性確認

### ドキュメント
- README.mdの更新
- 変更履歴の記録
- インストール手順の更新

## 📝 履歴メモ

### 2025年7月15日
- V2.2実装をarchive/V2.2/に移動完了
- ブランチ戦略文書作成
- V3.0実装開始準備完了

### 今後の予定
- [ ] Theme Manager統合
- [ ] 新アーキテクチャ実装
- [ ] テスト・検証
- [ ] mainブランチへのマージ

---

**作成日**: 2025年7月15日  
**作成者**: 開発チーム  
**最終更新**: 2025年7月15日
