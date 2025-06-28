# CONTRIBUTING.md - PhotoMap Explorer 2.0.0

## はじめに
PhotoMap Explorer 2.0.0 へのご関心・ご協力ありがとうございます！
本プロジェクトは Clean Architecture を採用し、拡張性・保守性・テスタビリティを重視しています。

- **バグ報告・機能提案・ドキュメント改善・テスト追加** など、どなたでも歓迎です。
- コントリビュート前に [README.md](../README.md)・[CHANGELOG.md](../CHANGELOG.md)・[docs/Release_2.0.0_Summary.md](Release_2.0.0_Summary.md) をご一読ください。

---

## ブランチ運用・開発フロー

### ブランチ構成
- `main` : 本番リリース用（安定版）
- `dev` : 開発統合ブランチ（新機能・修正の集約）
- `feature/xxx` : 新機能開発（`dev` から派生）
- `bugfix/xxx` : バグ修正（`dev` から派生）
- `refactor/xxx` : リファクタリング
- `docs/xxx` : ドキュメント改善
- `test/xxx` : テスト追加・修正
- `hotfix/xxx` : 緊急修正（`main` から派生）

### 命名規則例
| カテゴリ | 例 |
|----------|--------------------------|
| feature  | feature/map-panel-redesign |
| bugfix   | bugfix/gps-parse-error    |
| refactor | refactor/domain-service   |
| docs     | docs/clean-arch-guide     |
| test     | test/e2e-thumbnail        |
| hotfix   | hotfix/startup-crash      |

---

## コントリビュート手順

1. **Issue作成**
   - バグ報告・機能提案・質問はまず [Issues](https://github.com/scottlz0310/photomap-explorer/issues) へ
2. **フォーク & ブランチ作成**
   - `dev` ブランチから `feature/xxx` などを作成
3. **開発・テスト**
   - Clean Architectureの各層（domain, infrastructure, presentation, app, utils）を意識して実装
   - 必要に応じてテスト（`tests/`）も追加
4. **コミット**
   - 意味のあるコミットメッセージを心がける
   - 例: `fix: GPS座標パースのバグ修正`
5. **プルリクエスト作成**
   - `dev` ブランチ宛にPRを作成
   - PR本文に「目的・変更点・テスト内容・関連Issue」を明記
6. **レビュー・マージ**
   - レビュー後、問題なければマージ

---

## コーディング規約・設計方針

- **Clean Architecture**: 層をまたぐ依存は原則禁止
- **型ヒント・docstring**: 主要関数・クラスには型ヒントと説明を付与
- **絶対インポート推奨**: `from domain.models import ...` など
- **テスト必須**: 新機能・修正にはテスト追加を推奨
- **PEP8/Black/Flake8**: コード整形・静的解析を徹底

---

## テスト・CI

- `tests/` ディレクトリにE2E・ユニット・パフォーマンステストを配置
- テストは `python tests/run_all_tests.py` で一括実行
- PR作成時は必ずテストがパスすることを確認
- CI/CD（GitHub Actions等）導入予定

---

## ドキュメント・翻訳

- ドキュメントは `docs/` 配下にMarkdownで作成
- アーキテクチャ・設計思想・API仕様・移行ガイド等も歓迎
- 多言語対応（i18n）やFAQ追加も歓迎

---

## 貢献のヒント
- **小さなPR歓迎**: typo修正・コメント追加も大歓迎
- **議論を重視**: 大きな設計変更はIssueで事前相談
- **互換性配慮**: レガシーUI/新UI両対応を意識
- **テスト・ドキュメント重視**: 品質向上にご協力ください

---

## ライセンス・著作権

- 本プロジェクトはMITライセンスです
- コントリビュート内容はMITライセンスで公開されます

---

## お問い合わせ・連絡先

- [GitHub Issues](https://github.com/scottlz0310/photomap-explorer/issues)
- 開発者: [scottlz0310](https://github.com/scottlz0310)

---

PhotoMap Explorer 2.0.0 へのご貢献を心よりお待ちしています！

