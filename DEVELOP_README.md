# 🔧 Develop Branch - PhotoMap Explorer

## 📍 ブランチ概要

**develop** ブランチは PhotoMap Explorer の統合開発ブランチです。

### 🎯 用途
- 新機能開発の統合・テスト
- 非緊急バグ修正の統合
- リリース前の品質確認

### 🔄 ワークフロー
1. `feature/*` や `bugfix/*` ブランチからのマージ
2. 統合テスト・品質確認
3. 安定版として `main` にマージ

## 📋 現在の開発状況

### v2.1.x 開発予定機能
- 🌐 国際化・多言語対応
- 🎨 ダークモード・テーマシステム  
- 🔍 高度な検索・フィルタ機能
- 📊 統計・分析機能

### 進行中の改善
- パフォーマンス最適化
- UI/UX改善
- エラーハンドリング強化

## 🛠️ 開発者向け情報

### ブランチ作成
```bash
# 新機能開発
git checkout develop
git checkout -b feature/your-feature-name

# バグ修正  
git checkout develop
git checkout -b bugfix/issue-description
```

### マージ手順
```bash
# 開発完了後
git checkout develop
git merge your-branch-name
git push origin develop
```

## 📚 関連ドキュメント
- [BRANCH_STRATEGY.md](docs/BRANCH_STRATEGY.md) - ブランチ戦略
- [CONTRIBUTING.md](docs/CONTRIBUTING.md) - 貢献ガイドライン

---

*PhotoMap Explorer v2.0.0 以降の継続的な開発ブランチ*
