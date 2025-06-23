# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

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



## 🚧 v1.0.0-beta 予定機能

- [ ] **メニューバーの実装**  
      └ ファイル・表示・設定などを含むベーシックな構成

- [ ] **アドレスバーによる直接フォルダ入力**  
      └ `QLineEdit` 経由でパス入力→ナビゲーション

- [ ] **QFileDialog の代替となる PC/ドライブツリービュー**  
      └ `QFileSystemModel` でローカル/ネットワーク環境へのアクセスを可視化

- [ ] **起動引数からの自動遷移処理**  
      └ ダブルクリックで渡されたファイル→親フォルダを表示

- [ ] **右クリックメニューの実装**  
      └ サムネイル上での操作（例: ファイルを開く・Exifを見る・場所をコピー）

- [ ] **Exif ステータスバー統合表示**  
      └ 解像度、撮影日、位置情報等を一行で可視化 + 設定メニューで項目編集

- [ ] **左右カーソルキーと左右フォームボタンでの画像ビューの切り替え操作
　　　 └ より直感的な操作を可能とし、画像同士の比較を想定