# 🌿 ブランチ戦略 - PhotoMap Explorer v2.0.0以降

## 📋 ブランチ構成

PhotoMap Explorer 2.0.0リリース後の継続的な開発・改善のためのブランチ戦略

### 🏠 **main** - 本番リリースブランチ
- **用途**: 安定版リリース専用
- **保護**: 直接プッシュ禁止、プルリクエスト必須
- **マージ元**: `develop`, `hotfix/*`
- **タグ**: すべてのリリースバージョン（v2.0.0, v2.0.1, v2.1.0など）

### 🔧 **develop** - 統合開発ブランチ
- **用途**: 新機能・改善の統合・テスト
- **ベース**: `main`ブランチから分岐
- **マージ先**: `main`（リリース時）
- **マージ元**: `feature/*`, `bugfix/*`

### 🚨 **hotfix/v2.0.x** - 緊急修正ブランチ
- **用途**: 本番環境の緊急バグ修正
- **ベース**: `main`ブランチから分岐
- **マージ先**: `main` および `develop`
- **命名**: `hotfix/v{version}` または `hotfix/{issue-description}`
- **例**: `hotfix/v2.0.1`, `hotfix/critical-memory-leak`

### ✨ **feature/v2.1.x-development** - 機能開発ブランチ
- **用途**: v2.1.x の新機能開発
- **ベース**: `develop`ブランチから分岐
- **マージ先**: `develop`
- **機能**: 国際化、テーマシステム、高度検索など

### 🐛 **bugfix/{issue-name}** - バグ修正ブランチ
- **用途**: 非緊急のバグ修正
- **ベース**: `develop`ブランチから分岐
- **マージ先**: `develop`
- **命名**: `bugfix/{issue-description}`
- **例**: `bugfix/thumbnail-display-issue`, `bugfix/map-rendering-slow`

## 🔄 ワークフロー

### 📅 定期リリース（v2.1.0, v2.2.0など）
1. `feature/*` → `develop` にマージ
2. `develop` でテスト・品質確認
3. `develop` → `main` にプルリクエスト
4. `main` でリリースタグ作成

### 🚨 緊急修正（v2.0.1, v2.0.2など）
1. `main` → `hotfix/v2.0.x` 分岐
2. バグ修正・テスト
3. `hotfix/v2.0.x` → `main` プルリクエスト
4. `hotfix/v2.0.x` → `develop` バックポート
5. `main` でリリースタグ作成

### 🔧 日常的な改善
1. `develop` → `bugfix/{issue}` 分岐
2. 問題修正・改善実装
3. `bugfix/{issue}` → `develop` プルリクエスト

## 📋 ブランチ使用ガイドライン

### 🎯 作業開始時
```bash
# 新機能開発の場合
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# バグ修正の場合
git checkout develop  
git pull origin develop
git checkout -b bugfix/issue-description

# 緊急修正の場合
git checkout main
git pull origin main
git checkout hotfix/v2.0.x
```

### 📤 作業完了時
```bash
# コミット・プッシュ
git add .
git commit -m "type: description"
git push origin your-branch-name

# GitHub でプルリクエスト作成
```

### 🏷️ コミットメッセージ規約
- `feat:` - 新機能
- `fix:` - バグ修正
- `docs:` - ドキュメント
- `style:` - コードスタイル
- `refactor:` - リファクタリング
- `test:` - テスト追加
- `chore:` - 雑務

## 🛡️ ブランチ保護設定

### main ブランチ
- ✅ 直接プッシュ禁止
- ✅ プルリクエスト必須
- ✅ レビュー必須（1名以上）
- ✅ ステータスチェック必須
- ✅ 最新状態必須

### develop ブランチ  
- ✅ プルリクエスト推奨
- ✅ 自動テスト必須
- ⚠️ 直接プッシュ許可（小規模修正のみ）

## 📊 リリース戦略

### マイナーバージョン（v2.1.0, v2.2.0）
- **頻度**: 2-3ヶ月間隔
- **内容**: 新機能、大幅な改善
- **ブランチ**: `develop` → `main`

### パッチバージョン（v2.0.1, v2.0.2）
- **頻度**: 必要時（バグ発見時）
- **内容**: バグ修正、セキュリティ修正
- **ブランチ**: `hotfix/*` → `main`

## 🔗 関連ドキュメント

- [CONTRIBUTING.md](../CONTRIBUTING.md) - 貢献ガイドライン
- [Pending_features.md](Pending_features.md) - 今後の機能計画
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md) - 既知の問題

---

*作成日: 2025年6月28日*  
*PhotoMap Explorer v2.0.0 リリース完了に伴うブランチ戦略策定*
