# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/)
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [1.1.0] - 2025-06-26

### Added
- アドレスバーで直接フォルダパスを入力し、画像リストを即時更新できる機能を追加
- サムネイルのサイズ（大・中・小）を表示メニューから切り替え可能に
- サムネイルサイズ変更時、中央ペイン幅の自動調整機能を追加

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
