# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [2.1.2] - 2025-06-28

### Release
- **安定版リリース**: PhotoMap Explorer v2.1.2 安定版公開
- **最終テスト完了**: 全主要機能の動作検証完了
- **ドキュメント最新化**: README、CHANGELOG、既知の問題リスト更新
- **リリース準備完了**: パッケージング・配布準備完了

### Summary
- 完全なダークモード・ライトモード対応
- GIMP風アドレスバーによる直感的ナビゲーション
- 詳細なEXIF・GPS情報表示
- 最大化・復元可能な画像・マップビュー
- Clean Architectureによる高い保守性
- 包括的なテーマ適用システム

---

## [2.1.1] - 2025-06-28

### Improved
- **EXIF情報の表示・抽出改善**
  - カメラ情報表示の改善（メーカー名重複を自動排除）
  - シャッタースピード抽出の精度向上（APEX値対応、分数表示改善）
  - 絞り値・ISO感度・焦点距離の複数タグ対応
  - 撮影設定の統合表示（シャッター・絞り・ISO・焦点距離を1行で表示）
  - EXIF情報抽出に表示用キー（camera, shutter, aperture, iso, focal_length）を追加

### Fixed
- **ダークモード・テーマ切り替え不具合修正**
  - プレビューエリア"🖼️プレビュー"タイトル文字の色変更問題を修正
  - マップエリア"🗺️マップ"タイトル文字の色変更問題を修正
  - QGroupBoxタイトル要素にテーマ適用処理を追加
  - ステータスバーとメインエリアのテーマ切り替え強制更新機能を強化
  - 全UI要素の強制リフレッシュ処理を追加
  - 存在しないメソッド呼び出しエラー（_force_thumbnail_area_refresh）を修正

### Technical
- **logic/image_utils.py の extract_image_info() 関数強化**
  - 複数のEXIFタグからの情報取得に対応
  - APEX値（ShutterSpeedValue, ApertureValue等）の計算対応
  - エラー耐性の向上
- **presentation/views/functional_new_main_view.py のEXIF表示改善**
  - 新しい表示用キーに対応
  - 撮影設定の統合表示機能追加
- **presentation/views/functional_new_main_view.py のテーマ適用改善**
  - QGroupBoxタイトルの専用テーマ適用処理を追加
  - _apply_additional_theme_styles() に QGroupBox スタイル設定を実装

---

## [2.1.0] - 2025-06-28

### Added
- **ダークモード・ライトモード切り替え機能**
  - テーマ管理システム (ThemeManager) 実装
  - 全UI要素への動的テーマ適用
  - Windowsシステム設定連動（起動時にOSのダーク/ライトモードを自動反映）
  - テーマ切り替えトグルボタン追加
- **起動時のQt環境設定改善**
  - Qt platform pluginパスの自動設定
  - Qt WebEngine OpenGL警告の解消 (AA_ShareOpenGLContexts)
- **ドキュメント整備**
  - 既知の問題一覧 (KNOWN_ISSUES.md) 作成
  - README.mdの制限事項セクション整理

### Changed
- **GIMP風アドレスバーUI改善**
  - スクロールバー廃止、カレント側優先表示実装
  - 幅制約時の「...」ボタンによる省略表示
  - 区切り文字を完全削除（枠線でパーツを区別）
  - フォントサイズを10ptに最適化、30px高さに適応
  - ボタンと編集フィールドの高さを30pxに統一
  - padding/margin調整（4px 12px, 1px）でコンパクト化
  - テーマ対応スタイル適用（ライト/ダークモード対応）
  - hover/pressed状態のビジュアルフィードバック改善
- **フォルダ選択ダイアログ最適化**
  - 標準的なWindows フォルダ選択ダイアログに統一
  - 複雑な実装を廃止、信頼性とユーザビリティを優先
- **コード品質向上**
  - QLineEditのset_path呼び出しをsetTextに修正
  - PIL依存を廃止し、exifreadのみでEXIF情報抽出
  - UI要素の復旧・再作成（空ファイル問題対応）
- **テーマ対応強化**
  - アドレスバー、サムネイル、プレビュー/マップ背景のテーマ適用
  - GPS画面、最大化ビュー、タイトルバー等への動的テーマ適用
  - レガシーUI(main_window.py)から新UI(functional_new_main_view.py)への切替完了

### Fixed
- 主要なImportError、AttributeError修正
- PILライブラリ依存問題の解決
- Qt起動時のプラットフォームプラグイン問題修正
- **フォルダ選択ダイアログの改善**
  - 「検索条件に一致する項目はありません」エラーの解決
  - ファイルとフォルダ両方を表示するように変更
  - サムネイル処理段階で画像ファイルのみフィルタリング
- **アドレスバーのパス分解処理改善**
  - パス正規化の強化でボタン分解を正しく実行
  - 同一パスクリック時のリフレッシュ機能追加

---

## [2.0.2] - 2025-06-27

### Added
- **Clean Architecture移行完了**
  - モジュール分割とアーキテクチャリファクタリング
  - Legacy/New UI機能パリティ確認
- **画像/マップビューの最大化・復元機能**
  - ダブルクリック/ボタンによる最大化切り替え
  - GIMP風アドレスバー（キーボード・アクセシビリティ対応）実装
- **詳細ステータスパネル（EXIF/GPS情報表示）**

### Fixed
- MapPanel.update_location()引数エラー修正

---

## [1.1.0] - 2025-06-26

### Added
- アドレスバーで直接フォルダパスを入力し、画像リストを即時更新できる機能を追加
- ~~サムネイルのサイズ（大・中・小）を表示メニューから切り替え可能に~~ (v2.0で廃止、新UIで未実装)
- ~~サムネイルサイズ変更時、中央ペイン幅の自動調整機能を追加~~ (v2.0で廃止、新UIで未実装)

### Changed
- `main_window.py` を各UIパネルごとに分割し、可読性・保守性を大幅向上
- 依存関係・ディレクトリ構成・セットアップ手順を `README.md` で最新化
- `requirements.txt` から Pillow を除外し、必要最小限の依存パッケージに整理

### Removed
- `docs/architecture.md` を `README.md` に統合し、単独ファイルを削除

---

## [1.0.0] - 2025-06-22

### Added
- PyQt5 GUI による画像ビューアを実装
- Exif-GPS情報の解析機能（Pillowベース）
- GPS座標のHTMLマップ出力（Leaflet.js）
- フォルダ内の画像履歴切り替え機能
- GPSが無い画像に対する適切なスキップ処理
- README.md、requirements.txt、スクリーンショット（`docs/`）を追加
- `.gitignore` を整備し、`venv` や `__pycache__` を除外対象に

### Changed
- GPSデータが (0.0, 0.0) の場合は無効とみなすように改良
- GPS座標パース関数を堅牢化（tuple, float, Fraction対応）

### Removed
- デバッグ用の `print("[DEBUG] ...")` 出力をすべて削除

### Notes
- このリリースは ver 1.0 の初公開版です
- GitHub Releases にタグ `v1.0.0` を付けて記録推奨

📌 マイルストーン: v1.0.0-alpha（2025-06-22）
🎯 目的
PhotoMap Explorer の初期リリースに向けた「動作可能な最小構成」の完成。 UI設計、EXE生成、基本機能の実装と動作検証までが対象。

✅ 主な達成事項
PyInstallerによる .exe 化に成功
.spec の調整、Qt プラグイン・アイコン同梱
--onefile ビルドは失敗
マルチサイズ対応 .ico アイコン生成と統合
タスクバー・Alt+Tab・タイトルバー反映
setWindowIcon() による明示的指定
GitHub上でプロジェクト構成の整理
dist/, build/ ディレクトリの役割理解と .gitignore 整備
PDFベースのUI案を反映した将来設計の草案作成（未公開）
フォルダ選択ビュー・アドレスバー入力の統合構想
モジュール化に向けたアイデア整理
