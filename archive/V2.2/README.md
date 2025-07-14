# PhotoMap Explorer V2.2 - アーカイブ版

このディレクトリには、PhotoMap Explorer V2.2の実装コードが格納されています。

## アーカイブ日
2025年7月15日

## 含まれるコンポーネント

### メイン実装
- **main.py** - アプリケーションエントリーポイント
- **presentation/** - プレゼンテーション層（メインウィンドウ、ビュー）
- **ui/** - UIコンポーネント（コントロール、パネル）
- **logic/** - ビジネスロジック（画像処理、EXIF読取）
- **utils/** - ユーティリティ（ログ、デバッグ機能）
- **settings/** - 設定ファイル、テーマ設定
- **requirements.txt** - Python依存関係

### テストコード（test/）
- **simple_test.py** - 基本機能テスト
- **test_*.py** - 各種機能テスト
- **function_test_helper.py** - テスト用ヘルパー
- **manual_test_helper.py** - 手動テスト用ヘルパー
- **map.html** - 地図表示テスト用HTML
- **test_map_output.html** - 地図出力テスト結果

### デバッグコード（debug/）
- **debug_theme_validation.py** - テーマ検証用デバッグ
- **debug_ui_test.py** - UI動作デバッグ
- **replace_debug_prints.py** - デバッグプリント置換ツール

## V2.2の特徴
- PyQt5ベースのGUI実装
- GIMP風アドレスバー
- 写真のEXIF/GPS情報表示
- 地図表示機能
- テーマ切り替え対応
- パネル最大化機能

## 移行理由
V3.0での新しいTheme Managerライブラリ統合とコード構造の全面刷新に伴い、V2.2実装をアーカイブ化。

## 注意事項
このアーカイブ版は参考用です。新しい開発にはプロジェクトルートの最新実装を使用してください。
