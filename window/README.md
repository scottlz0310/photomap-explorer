# 📁 Window ディレクトリ - モジュラー化・リファクタリング管理

## 🎯 第3回リファクタリングの焦点

### 🚨 最重要課題: メガファイル問題
現在、メインアプリケーションは **`presentation/views/functional_new_main_view.py` (1690行、44メソッド)** の巨大な単一ファイルで実装されており、これが最大の技術的負債となっています。

### 📋 現状の問題
- **極度の責任集中**: UI制御、イベント処理、テーマ管理、状態管理が一つのクラスに集約
- **保守性の低下**: 1690行の巨大ファイルで理解・修正が困難
- **テスト困難**: 44メソッドが高度に結合し、単体テストが不可能
- **実装重複**: `window/main_window.py` (266行) との二重実装

## 🏗️ 分割戦略 (第3回リファクタリング)

### 📂 新しい構造設計
```
presentation/views/main_window/
├── main_window_core.py (200-250行)
│   └── 基本ウィンドウ構成、初期化、メイン制御
├── ui_managers/
│   ├── layout_manager.py (150-200行)
│   │   └── スプリッター、レイアウト制御
│   ├── panel_manager.py (200-250行)
│   │   └── 各パネル管理
│   ├── maximize_manager.py (150-200行)
│   │   └── 最大化・復元機能
│   └── theme_manager.py (100-150行)
│       └── テーマ切り替え制御
├── event_handlers/
│   ├── folder_event_handler.py (150-200行)
│   │   └── フォルダ選択・ナビゲーション
│   ├── image_event_handler.py (150-200行)
│   │   └── 画像選択・表示イベント
│   └── navigation_event_handler.py (100-150行)
│       └── アドレスバー・ナビゲーション
└── display_controllers/
    ├── image_display_controller.py (150-200行)
    │   └── 画像表示・プレビュー制御
    └── map_display_controller.py (150-200行)
        └── マップ表示・GPS処理
```

### 🔄 実装フェーズ
1. **Phase 1**: メガファイル分割 (最優先)
   - 1690行 → 8-10個の200-300行ファイル群
2. **Phase 2**: MainWindow実装統一
   - 重複実装の整理・統合
3. **Phase 3**: UI Controls分割
   - `ui/controls.py` (425行) の分解
4. **Phase 4**: テストスイート構築
5. **Phase 5**: パフォーマンス最適化

## 📊 期待される改善効果

### 定量的改善
- **最大ファイルサイズ**: 1690行 → 300行以下
- **理解時間**: 推定70%短縮  
- **修正影響範囲**: 80%削減
- **テストカバレッジ**: 0% → 60%以上

### 定性的改善
- **単一責任原則**: 各クラスが明確な責任を持つ
- **保守性向上**: 影響範囲の限定化
- **拡張性向上**: 新機能追加の容易性
- **開発効率**: 並行開発が可能

## 📚 関連ドキュメント

- `docs/THIRD_REFACTORING_PLAN.md` - 実施計画詳細
- `docs/THIRD_REFACTORING_ANALYSIS.md` - 全体的課題分析
- `docs/MEGAFILE_ANALYSIS.md` - メガファイル詳細分析
- `docs/Pending_features.md` - 機能要件・既知課題

## 🚀 次のアクション

### 即座に取り組むべき項目
1. `functional_new_main_view.py` の詳細依存関係分析
2. `main_window_core.py` のプロトタイプ実装
3. 分割後のテスト戦略策定

---
**更新日:** 2025-01-18  
**状況:** 第3回リファクタリング計画策定完了 → 実装開始予定
