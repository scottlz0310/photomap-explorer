# PhotoMap Explorer v2.1.2 リリースノート

## 🚀 リリース概要

**PhotoMap Explorer v2.1.2** は、プライバシー保護を重視した安定版リリースです。
すべての個人情報を削除し、統一された開発者名「scottlz0310」での公開版として完成しました。

本リリースは安定性と信頼性を重視し、次期v2.2.0での大規模リファクタリングに向けた
強固な基盤を提供します。継続的な開発とコミュニティフィードバックにより、
さらなる機能拡張と品質向上を進めていきます。

---

## 🆕 v2.1.2 の変更点

### 🔒 プライバシー保護対応
- **個人情報の完全除去**: すべてのソースコード、メタデータ、配布物から個人情報を削除
- **開発者名統一**: 「scottlz0310」に統一（GitHub: [@scottlz0310](https://github.com/scottlz0310)）
- **プロジェクト名統一**: 「photomap-explorer」に統一
- **安全な配布物**: プライバシーセーフなEXE・パッケージファイルを生成

### 📚 ドキュメント更新
- **新しいスクリーンショット**: GPS付きサンプル画像を使用した美しいデモ画像
- **README.md更新**: 現在の実装状況を正確に反映
- **既知の問題**: KNOWN_ISSUES.mdで制限事項を明確化
- **Pending_features.md**: 未実装機能を正確に記載

### 🧹 プロジェクトクリーンアップ
- **Gitタグ整理**: プライバシー関連の古いタグを削除
- **ブランチ整理**: clean stateでのmain/developブランチ
- **配布物クリーンアップ**: 古い.egg-info、.whl、.tar.gzファイルを削除
- **.gitignore強化**: 配布物の誤コミットを防止

---

## ✨ 主要機能（v2.1系の完全機能）

### 🌙 ダークモード・ライトモード対応
- **テーマ切り替え機能**: ツールバーのトグルボタンでワンクリック切り替え
- **システム連動**: Windows設定と連動し、起動時に自動でダーク/ライトモードを反映
- **全UI対応**: アドレスバー、サムネイル、プレビュー、マップ等すべての要素がテーマに対応

### 🏗️ Clean Architecture移行完了
- **新UI実装**: 機能的で保守性の高い新しいメインビュー
- **最大化・復元**: 画像/マップビューのダブルクリック最大化機能
- **GIMP風アドレスバー**: キーボードアクセシビリティ対応の直感的ナビゲーション
- **詳細ステータス**: EXIF/GPS情報の統合表示パネル

### 🔧 技術的改善
- **Qt起動時の安定性向上**: プラットフォームプラグイン自動設定
- **PIL依存廃止**: exifreadベースの軽量EXIF処理
- **コード品質向上**: エラー修正とパフォーマンス最適化
- **リファクタリング準備**: 肥大化ファイルの分析と分割計画策定（[REFACTORING_PLAN_v2.2.0.md](docs/REFACTORING_PLAN_v2.2.0.md)）

---

## ⚠️ 注意点・制限事項

### 📋 既知の問題
詳細は [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) を参照：
- **GIMP風アドレスバー**: 長いパスでの幅制約による表示制限
- **フォルダ選択ダイアログ**: Windows標準ダイアログの仕様制限

### 🔄 今後の開発予定
詳細・進捗は [docs/Pending_features.md](docs/Pending_features.md) を参照：
- **サムネイルサイズ変更**: v2.0で失われた機能、再実装予定
- **複数選択機能**: CTRLクリックによる複数画像選択
- **ドラッグ&ドロップ**: ファイル操作の簡素化

---

## 🛣️ 開発ロードマップ

### v2.2.0 (第2回リファクタリング)
**予定時期**: 2025年7月以降  
**主な改善点**:
- **コード構造最適化**: 肥大化ファイルの分割（1689行→300行以下）
- **保守性向上**: 単一責任原則に基づく再設計
- **開発効率改善**: テスト容易性とチーム開発対応

詳細計画: [docs/REFACTORING_PLAN_v2.2.0.md](docs/REFACTORING_PLAN_v2.2.0.md)

### v2.3.0以降 (新機能拡張)
- サムネイルサイズ変更機能の復活
- 複数選択・一括操作機能
- パフォーマンス最適化

---

## 🚀 セットアップ方法

### 1. リポジトリのクローン
```bash
git clone https://github.com/scottlz0310/photomap-explorer.git
cd photomap-explorer
```

### 2. 仮想環境のセットアップ
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 依存関係のインストール
```bash
pip install -r requirements.txt
```

### 4. アプリケーションの起動
```bash
python main.py
```

---

## 📦 依存ライブラリ

| ライブラリ   | 用途             |
|--------------|------------------|
| PyQt5        | GUI表示          |
| PyQtWebEngine| 地図の描画       |
| folium       | 地図HTML生成     |
| exifread     | Exifデータ抽出   |

---

## 🎯 動作確認

### 基本機能確認
1. **起動確認**: `python main.py` でアプリが正常起動
2. **テーマ切り替え**: 🌙/☀️ボタンでダーク・ライトモード切り替え
3. **フォルダ選択**: 📁ボタンで画像フォルダを選択
4. **画像表示**: サムネイルクリックで画像プレビュー
5. **GPS機能**: GPS付き画像でマップ表示

### 詳細検証
詳しい検証手順は [docs/VERIFICATION_GUIDE_v2.1.2.md](docs/VERIFICATION_GUIDE_v2.1.2.md) を参照

---

## 🌍 サンプル画像について

リリースのスクリーンショットには、[GeoImgr Sample Photos](https://www.geoimgr.com/sample-photos.html)から提供された台湾・九份の美しい風景写真を使用しています。
GPS情報付きのサンプル画像を使用することで、PhotoMap Explorerの機能をわかりやすくデモンストレーションしています。

---

## 📄 ライセンス

MIT License  
© 2025 scottlz0310

---

## 🙌 クレジット

- **開発・ドキュメント**: scottlz0310（GitHub: [@scottlz0310](https://github.com/scottlz0310))
- **コーディングサポート**: Microsoft Copilot
- **スクリーンショット画像**: [GeoImgr Sample Photos](https://www.geoimgr.com/sample-photos.html) 提供

---

## 📞 サポート

- **GitHub Issues**: [photomap-explorer/issues](https://github.com/scottlz0310/photomap-explorer/issues)
- **プロジェクトページ**: [github.com/scottlz0310/photomap-explorer](https://github.com/scottlz0310/photomap-explorer)

---

## 🎯 次のステップ (v2.1.2リリース後)

### 即座に実施
1. **リリース検証**: [VERIFICATION_GUIDE_v2.1.2.md](docs/VERIFICATION_GUIDE_v2.1.2.md)による全機能テスト
2. **配布物確認**: privacy-safeなEXE・パッケージファイルの最終確認
3. **GitHub Release作成**: v2.1.2の正式リリース公開

### 短期計画（1-2週間）
1. **フィードバック収集**: 初期ユーザーからの問題報告・改善提案
2. **バグフィックス**: 発見された軽微な問題の修正
3. **ドキュメント微調整**: 実際の使用状況に基づく改善

### 中期計画（1-2ヶ月）
1. **第2回リファクタリング開始**: [REFACTORING_PLAN_v2.2.0.md](docs/REFACTORING_PLAN_v2.2.0.md)実施
2. **新機能の設計・実装**: Pending_features.mdの優先機能
3. **テストカバレッジ向上**: 自動テスト体制の強化

PhotoMap Explorer v2.1.2をお楽しみください！
