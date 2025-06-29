# 🧹 ブランチ整理記録 - PhotoMap Explorer v2.0.0

## 📅 整理実施日
**2025年6月28日** - PhotoMap Explorer v2.0.0 リリース完了後

## 🎯 整理の目的
- v2.0.0 開発完了に伴う不要ブランチの削除
- リポジトリのクリーンアップ
- 今後の開発効率向上

## 🗑️ 削除されたブランチ

### ローカルブランチ
- ✅ `refactor-ui-structure` - v2.0.0開発完了、mainにマージ済み
- ✅ `refact` - 古い作業ブランチ

### リモートブランチ
- ✅ `refactor-ui-structure` - Clean Architecture実装完了
- ✅ `refact` - 古いリファクタリング作業
- ✅ `feature/v1.1.3` - 古いバージョンの機能開発(開発中止➡️v2以降に持ち越し)
- ✅ `dev/feature` - 古い開発ブランチ (自動削除)
- ✅ `dev/split-main-window` - 古いUI分割作業 (自動削除)
- ✅ `feature` - 古い機能開発ブランチ (自動削除)
- ✅ `feature-ui-improvements` - UI改善完了 (自動削除)

## ✅ 保持されたブランチ

### 🏠 本番・リリース
- **`main`** - 本番リリースブランチ (v2.0.0タグ付き)

### 🔧 継続開発
- **`develop`** - 統合開発ブランチ
- **`hotfix/v2.0.x`** - v2.0.x緊急修正用
- **`feature/v2.1.x-development`** - v2.1.x新機能開発用

## 📊 整理効果

### Before (整理前)
```
- 12個のブランチ (ローカル6個 + リモート8個)
- 複数の古い開発ブランチが混在
- ブランチ管理の複雑化
```

### After (整理後)
```
- 4個のブランチ (ローカル4個 + リモート4個)
- 明確な役割分担
- シンプルで管理しやすい構成
```

## 🌿 新しいブランチ戦略

整理後のクリーンな状態から、[BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) で定義された新しいブランチ戦略を運用開始。

### 今後のブランチ運用
- **main**: 安定版リリース専用
- **develop**: 日常的な開発・統合
- **hotfix/v2.0.x**: 緊急修正
- **feature/v2.1.x-development**: 新機能開発

## 🔗 関連ドキュメント
- [BRANCH_STRATEGY.md](BRANCH_STRATEGY.md) - ブランチ戦略ガイド
- [CONTRIBUTING.md](../CONTRIBUTING.md) - 貢献ガイドライン

---

*整理実施者: PhotoMap Explorer Development Team*  
*v2.0.0 リリース完了記念クリーンアップ*
