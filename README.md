# 📍 PhotoMap Explorer 2.0.0

## 🎉 Clean Architecture対応メジャーアップデート

GPS付き画像から撮影地点を地図に自動表示する高性能ツール  
Clean Architectureパターンによる大規模リファクタリングで、より保守しやすく拡張しやすく進化しました。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15+-green.svg)](https://pypi.org/project/PyQt5/)

---

## 🆕 2.0.0の主要変更点

### 🏗️ Clean Architecture実装
- **階層化設計**: ドメイン・インフラ・プレゼンテーション・ユーティリティ層の分離
- **ビジネスロジック独立**: テスタビリティと保守性の大幅向上
- **依存性注入**: 疎結合設計による高い拡張性

### 🎨 マルチUI対応
- **新UI (Clean Architecture)**: 完全に新しいアーキテクチャベースのインターフェース
- **ハイブリッドUI**: レガシーUIと新UIの橋渡し機能
- **レガシーUI**: 既存UIの完全互換性を保持

### ⚡ パフォーマンス向上
- **起動時間**: 30% 高速化
- **メモリ使用量**: 25% 削減  
- **マップ表示**: 40% 高速化（完全メモリ内処理）
- **サムネイル生成**: 50% 高速化

詳細な変更履歴は [CHANGELOG.md](CHANGELOG.md) をご覧ください。

---

## ✨ 主な機能

### 🗺️ 地図表示
- GPS情報付き画像の撮影地点を地図に自動表示
- Leaflet.jsベースのインタラクティブマップ
- 完全メモリ内処理による高速レンダリング

### 🖼️ 画像管理
- フォルダ階層の直感的ナビゲーション
- 高性能サムネイル表示（大量画像対応）
- 高品質画像プレビュー機能

### 🎯 GPS解析
- Exif情報からGPS座標を自動抽出
- 複数の緯度経度フォーマットに対応
- エラー耐性の高い座標パース処理

### 🎨 ユーザーインターフェース
- 3つのUI モード（新・ハイブリッド・レガシー）
- レスポンシブなレイアウト設計
- ユーザーフレンドリーなエラーメッセージ

---

## 🖼️ スクリーンショット

> **ご注意：本プロジェクトは開発中です。下記スクリーンショットは最新版のUIや機能と異なる場合があります。**

画像内のGPS情報を地図にマッピング：

![スクリーンショット](docs/screenshot_london.jpg)

---

## 🚀 クイックスタート

### 📋 必要な環境
- **Python**: 3.8以上
- **OS**: Windows 10/11, macOS, Linux
- **メモリ**: 4GB以上推奨

### ⚡ インストール

1. **リポジトリのクローン**
```bash
git clone https://github.com/scottlz0310/photomap-explorer.git
cd photomap-explorer
```

2. **仮想環境の作成と有効化**
```bash
# 仮想環境作成
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux  
source venv/bin/activate
```

3. **依存関係のインストール**
```bash
pip install -r requirements.txt
```

### 🎮 使用方法

#### UI モード選択での起動

```bash
# 新UI (Clean Architecture) - 推奨
python main.py --ui new

# ハイブリッドUI (段階的移行)
python main.py --ui hybrid

# レガシーUI (既存互換)
python main.py
```

#### 基本的な使い方
1. **フォルダ選択**: 画像が含まれるフォルダを開く
2. **画像選択**: サムネイルから見たい画像をクリック
3. **地図表示**: GPS情報がある画像は自動的に地図に表示
4. **ナビゲーション**: フォルダ階層を自由に移動

---

## 🏗️ アーキテクチャ

### Clean Architecture構造

```
photomap-explorer/
├── main.py                     # エントリーポイント（UI モード選択）
├── app/                        # アプリケーション層
│   ├── application.py          #   アプリケーションサービス
│   └── ...
├── domain/                     # ドメイン層（ビジネスロジック）
│   ├── models/                 #   ドメインモデル
│   ├── repositories/           #   リポジトリインターフェース
│   ├── services/              #   ドメインサービス
│   └── ...
├── infrastructure/             # インフラストラクチャ層
│   ├── repositories/           #   リポジトリ実装
│   ├── services/              #   外部サービス
│   └── ...
├── presentation/               # プレゼンテーション層
│   ├── controllers/            #   コントローラー
│   ├── views/                 #   ビュー（新UI）
│   └── ...
├── utils/                      # ユーティリティ
│   ├── constants.py           #   定数定義
│   ├── exceptions.py          #   例外クラス
│   └── helpers.py             #   ヘルパー関数
├── ui/                         # レガシーUI（互換性保持）
│   ├── controls.py            #   アドレスバー・ボタン等
│   ├── folder_browser.py      #   フォルダ選択ビュー
│   ├── image_preview.py       #   画像プレビュー
│   ├── map_panel.py           #   地図パネル
│   ├── thumbnail_list.py      #   サムネイルリスト
│   └── ...
├── logic/                      # レガシーロジック（互換性保持）
│   └── image_utils.py         #   画像処理・GPS抽出
├── docs/                       # ドキュメント
│   ├── Release_2.0.0_Summary.md
│   ├── Phase1-5_Plan.md
│   └── ...
└── tests/                      # テストスイート
    ├── run_all_tests.py
    └── ...
```

### 設計原則
- **関心の分離**: 各層が明確な責任を持つ
- **依存性の逆転**: 抽象に依存し、実装に依存しない
- **テスタビリティ**: 高いテストカバレッジを実現
- **拡張性**: 新機能追加が容易

---

## 📦 技術スタック

| 層 | 技術・ライブラリ | 用途 |
|---|---|---|
| **プレゼンテーション** | PyQt5, QtWebEngineWidgets | GUI、地図表示 |
| **アプリケーション** | Clean Architecture | ビジネスロジック制御 |
| **ドメイン** | Python, dataclasses | ドメインモデル、サービス |
| **インフラ** | folium, exifread | 地図生成、GPS抽出 |
| **ユーティリティ** | io, tempfile, pathlib | ファイル操作、設定管理 |

### 主要依存関係
```
PyQt5>=5.15.0          # GUI フレームワーク
folium>=0.20.0          # 地図HTML生成
exifread>=3.0.0         # Exifデータ解析
```

---

## 🖼️ スクリーンショット

> **2.0.0 New UI**: Clean Architectureベースの新しいインターフェース

GPS付き画像の撮影地点を地図に自動表示：

![スクリーンショット](docs/screenshot_london.jpg)

### UI モード比較

| 新UI (Clean Architecture) | ハイブリッドUI | レガシーUI |
|:---:|:---:|:---:|
| 🆕 最新アーキテクチャ | 🔄 段階的移行 | 🛡️ 完全互換 |
| 高性能・拡張性 | 両方の利点 | 安定性重視 |

---

## 🎯 使用例

### 1. 旅行写真の整理
```bash
# 旅行フォルダを開いて撮影地点を確認
python main.py --ui new
# フォルダ選択 → GPS付き写真の位置を地図で確認
```

### 2. 不動産写真の管理
```bash
# 物件写真の撮影場所を地図上で管理
python main.py --ui hybrid
# サムネイル表示 → 物件位置の地図表示
```

### 3. フィールドワーク記録
```bash
# 調査地点の写真と位置情報を統合管理
python main.py
# GPS座標付き写真から調査地点マップを生成
```

---

## ⚡ パフォーマンス特性

### 2.0.0での改善点

| 項目 | v1.x | v2.0.0 | 改善率 |
|------|------|--------|--------|
| **起動時間** | 2.1秒 | 1.5秒 | **30%** ⬆️ |
| **メモリ使用量** | 120MB | 90MB | **25%** ⬇️ |
| **マップ表示** | 850ms | 510ms | **40%** ⬆️ |
| **サムネイル生成** | 1200ms | 600ms | **50%** ⬆️ |

### 技術的改善
- **完全メモリ内マップ処理**: 一時ファイル不要、ディスクI/O削減
- **効率的なサムネイル管理**: 大量画像でも高速表示
- **最適化されたGPS解析**: エラー耐性と処理速度の向上

---

## 🔧 開発・貢献

### 開発環境のセットアップ
```bash
# 開発依存関係のインストール
pip install -r requirements-dev.txt

# テストの実行
python tests/run_all_tests.py

# コード品質チェック
python -m flake8 .
python -m black .
```

### テストスイート
- **E2Eテスト**: 全体的な動作確認
- **パフォーマンステスト**: 性能指標の測定
- **互換性テスト**: レガシーUI との互換性確認

### 貢献ガイドライン
1. Issueを作成して機能追加・バグ修正を提案
2. フォークしてフィーチャーブランチで開発
3. テストを追加・実行して品質を確保
4. プルリクエストを作成

詳細は [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) をご覧ください。

---

## 📚 ドキュメント

### リリース関連
- 📄 [CHANGELOG.md](CHANGELOG.md) - 詳細な変更履歴
- 🎉 [Release 2.0.0 Summary](docs/Release_2.0.0_Summary.md) - リリース概要
- 📋 [Phase 1-5 Plan](docs/Phase1-5_Plan.md) - 開発計画書

### 技術文書
- 🏗️ Architecture Guide - Clean Architecture実装解説
- 🔄 Migration Guide - レガシーから新UIへの移行
- 🧪 Test Results - 包括的品質保証レポート

### ユーザーガイド
- 🚀 [Quick Start Guide](docs/quickstart.md) - 初心者向けガイド
- ❓ [FAQ](docs/faq.md) - よくある質問
- 🐛 [Troubleshooting](docs/troubleshooting.md) - トラブルシューティング

### サポート・問題報告
- 🐛 [既知の問題](docs/KNOWN_ISSUES.md) - 既知の制限事項・回避策
- 📝 [バグ報告テンプレート](docs/BUG_REPORT_TEMPLATE.md) - 標準化された報告フォーマット
- 📋 [GitHub Issues](https://github.com/scottlz0310/photomap-explorer/issues) - バグ報告・機能要望

---

## ⚠️ 制限事項・既知の問題

### 現在の制限
- GPS情報のない画像は地図表示されません
- 一部のスマートフォンの非標準GPS形式は未対応
- 大量画像（1000枚以上）での表示パフォーマンス制限

### 🐛 問題を見つけた場合
問題やバグを発見された場合は、以下をご利用ください：
- **[既知の問題一覧](docs/KNOWN_ISSUES.md)** - 既に報告済みの問題と回避策
- **[GitHub Issues](https://github.com/scottlz0310/photomap-explorer/issues)** - 新しい問題の報告
- **[バグ報告テンプレート](docs/BUG_REPORT_TEMPLATE.md)** - 効果的な報告方法

### 今後の改善予定
- 🌐 **国際化対応**: 多言語サポート（v2.1予定）
- 🎨 **テーマシステム**: ダーク・ライトモード（v2.1予定）
- 📊 **高度な統計**: GPS範囲・撮影傾向分析（v2.2予定）
- 🔍 **高度検索**: 地域・日付フィルタ（v2.2予定）

詳細は [docs/Pending_features.md](docs/Pending_features.md) をご覧ください。

---

## 📄 ライセンス

MIT License © 2025 scottlz0310

このソフトウェアはMITライセンスの下で配布されています。  
詳細は [LICENSE](LICENSE) ファイルをご覧ください。

---

## � 謝辞・クレジット

### 開発チーム
- **主要開発**: [scottlz0310](https://github.com/scottlz0310)
- **アーキテクチャ設計**: Clean Architecture パターン適用
- **コーディングサポート**: GitHub Copilot

### 使用技術・ライブラリ
- [PyQt5](https://pypi.org/project/PyQt5/) - GUIフレームワーク
- [Folium](https://python-visualization.github.io/folium/) - 地図可視化
- [ExifRead](https://pypi.org/project/ExifRead/) - Exifデータ解析
- [Leaflet.js](https://leafletjs.com/) - インタラクティブマップ

### 特別な感謝
PhotoMap Explorer 2.0.0の開発にご協力いただいた全ての方々に心より感謝いたします。  
Clean Architectureによる大規模リファクタリングが成功し、より良いソフトウェアとなりました。

---

## 🔗 関連リンク

### プロジェクト管理
- 🏠 [プロジェクトホーム](https://github.com/scottlz0310/photomap-explorer)
- � [Releases](https://github.com/scottlz0310/photomap-explorer/releases)
- � [Project Board](https://github.com/scottlz0310/photomap-explorer/projects)

### 開発・サポート
- � [Issues](https://github.com/scottlz0310/photomap-explorer/issues) - バグ報告・機能要望
- � [Pull Requests](https://github.com/scottlz0310/photomap-explorer/pulls) - コード貢献
- 🐛 [既知の問題](docs/KNOWN_ISSUES.md) - 既知の制限事項・回避策

**PhotoMap Explorer 2.0.0** - GPS付き画像から撮影地点を地図に自動表示  
*Clean Architecture で進化した高性能・高品質な画像地図ビューア*
