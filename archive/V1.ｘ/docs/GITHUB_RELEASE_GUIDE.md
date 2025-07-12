# GitHub Release v2.1.2 作成ガイド

## 🎯 v2.1.2 GitHub Release作成手順

### 1. GitHub リポジトリへアクセス
1. ブラウザで GitHub リポジトリを開く: `https://github.com/scottlz0310/photomap-explorer`
2. 「Releases」タブをクリック
3. 「Create a new release」ボタンをクリック

### 2. リリース情報を入力

#### 基本情報
- **Tag version**: `v2.1.2`
- **Release title**: `PhotoMap Explorer v2.1.2 - 安定版リリース`
- **Target**: `develop` ブランチを選択

#### リリースノート（コピペ用）

```markdown
# PhotoMap Explorer v2.1.2 - 安定版リリース

## 🌟 主な新機能・改善

### ✨ 新機能
- **完全なダーク・ライトモード対応**: システム設定連動の美しいテーマシステム
- **GIMP風アドレスバー**: 直感的ファイルナビゲーション機能
- **詳細なEXIF・GPS情報表示**: 撮影設定・位置情報の包括的表示
- **画像・マップの最大化表示**: ダブルクリックまたはボタンで全画面表示

### 🔧 技術的改善
- **Clean Architecture移行完了**: 高い保守性とテスト容易性を実現
- **Qt起動時の安定性向上**: 信頼性の高いアプリケーション起動
- **PIL依存廃止**: exifreadベースの軽量EXIF処理システム
- **包括的なテーマ適用システム**: 全UIコンポーネントの統一テーマ

### 🐛 修正された問題
- サムネイル表示の安定性向上
- GPS情報表示の精度改善
- ファイル読み込み時のエラーハンドリング強化
- UI応答性の最適化

## 📥 ダウンロード

### 🖥️ Windows ユーザー（推奨）
- **[PhotoMapExplorer-v2.1.2-Windows.zip](ダウンロードリンク)**
  - スタンドアロン実行ファイル（依存関係なし）
  - 解凍後、`PhotoMapExplorer.exe` を実行

### 🐍 Python開発者
```bash
pip install photomap-explorer==2.1.2
```

または、配布ファイルから：
- **[photomap_explorer-2.1.2.tar.gz](ダウンロードリンク)** - ソース配布
- **[photomap_explorer-2.1.2-py3-none-any.whl](ダウンロードリンク)** - Wheel配布

## 📋 システム要件

| 項目 | 要件 |
|------|------|
| **OS** | Windows 10/11 (x64) |
| **Python** | 3.8+ (Python版の場合) |
| **メモリ** | 最小 512MB、推奨 1GB+ |
| **ディスク** | 200MB以上の空き容量 |

## 🚀 使用方法

### Windows実行ファイル版
1. `PhotoMapExplorer-v2.1.2-Windows.zip` をダウンロード
2. 任意のフォルダに解凍
3. `PhotoMapExplorer.exe` をダブルクリックして起動

### Python版
```bash
# インストール
pip install photomap-explorer==2.1.2

# 実行
photomap-explorer
```

## 🛠️ 新機能詳細

### ダーク・ライトモード
- システム設定に自動連動
- 手動切り替え可能（🌙/☀️ボタン）
- 全UIコンポーネントの統一テーマ

### GIMP風アドレスバー
- パス階層の直感的表示
- クリックによる階層移動
- 手動パス入力対応

### 最大化表示
- 画像・マップのダブルクリック最大化
- 専用最大化ボタン
- ESCキーまたは復元ボタンで通常表示

## 🐛 既知の問題

現在、重大な既知の問題はありません。
問題を発見された場合は [Issues](https://github.com/scottlz0310/photomap-explorer/issues) までご報告ください。

## 📚 ドキュメント

- **[README.md](https://github.com/scottlz0310/photomap-explorer/blob/main/README.md)** - 基本的な使用方法
- **[CHANGELOG.md](https://github.com/scottlz0310/photomap-explorer/blob/main/CHANGELOG.md)** - 変更履歴
- **[CONTRIBUTING.md](https://github.com/scottlz0310/photomap-explorer/blob/main/docs/CONTRIBUTING.md)** - 開発貢献ガイド

## 💬 サポート

- **GitHub Issues**: [問題報告・機能要求](https://github.com/scottlz0310/photomap-explorer/issues)
- **GitHub Discussions**: [質問・議論](https://github.com/scottlz0310/photomap-explorer/discussions)

---

**完全なソースコード**: [v2.1.2 タグ](https://github.com/scottlz0310/photomap-explorer/archive/refs/tags/v2.1.2.zip)

この安定版リリースをお楽しみください！ 🎉
```

### 3. ファイルをアップロード

以下のファイルをドラッグ&ドロップでアップロード：

#### 必須ファイル
1. **`PhotoMapExplorer-v2.1.2-Windows.zip`** 
   - 説明: "Windows用スタンドアロン実行ファイル（推奨）"

2. **`photomap_explorer-2.1.2.tar.gz`**
   - 説明: "Python ソース配布パッケージ"

3. **`photomap_explorer-2.1.2-py3-none-any.whl`**
   - 説明: "Python Wheel配布パッケージ"

#### オプションファイル（推奨）
4. **ソースコードアーカイブ**（GitHubが自動生成）
   - zip形式とtar.gz形式の両方が自動で追加される

### 4. リリース設定

#### リリースオプション
- ☑️ **Set as the latest release** - チェック
- ☑️ **Create a discussion for this release** - チェック（推奨）
- ☐ **Set as a pre-release** - チェックしない（安定版のため）

#### Target Branch
- **Target**: `develop` ブランチを選択

### 5. リリース公開

1. 全情報を確認
2. 「Publish release」ボタンをクリック
3. リリースページが生成される

## 🎯 リリース後の確認事項

### 1. リリースページの確認
- [ ] タグ `v2.1.2` が正しく作成されている
- [ ] 全ファイルがダウンロード可能
- [ ] リリースノートが正しく表示されている

### 2. ダウンロードテスト
- [ ] Windows ZIPファイルがダウンロード・実行可能
- [ ] Python パッケージがインストール可能
- [ ] ソースコードがダウンロード可能

### 3. 公開状態確認
- [ ] 「Latest release」として表示されている
- [ ] リリース通知が適切に送信されている
- [ ] README.mdのバッジが最新バージョンを表示

## 📢 リリース後のアクション

### 1. ソーシャル告知（オプション）
- README.mdの更新
- 関連フォーラム・コミュニティでの告知

### 2. 開発の継続
- `develop` ブランチで次のバージョン開発開始
- フィードバック収集とissue対応

---

**🎉 v2.1.2 リリース完了おめでとうございます！**

このガイドに従ってGitHub Releaseを作成し、PhotoMap Explorer v2.1.2を世界中のユーザーに届けましょう！
