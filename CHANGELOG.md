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
