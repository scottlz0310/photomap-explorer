# 📊 レガシーUI削除対象詳細リスト

**作成日**: 2025年7月2日  
**目的**: 削除計画実施前の詳細確認  

## 🎯 削除対象ファイル一覧

### Phase 1: 緊急削除（リスク: 低）

#### 空ファイル・無効ファイル
```
main_hybrid.py                          # 0行（空ファイル）
```

#### アーカイブ・バックアップ
```
archive/backups/backup_phase5_2_20250628/
├── main.py                             # ハイブリッドUI起動スクリプト
├── presentation/views/
│   ├── final_optimized_main_view.py    # 最適化版実装
│   └── extreme_light_view.py           # 軽量版実装
└── README_BACKUP.md                    # バックアップ説明

archive/backups/backup_phase5_2_20250628_020731/
├── main.py                             # ハイブリッドUI起動スクリプト  
├── presentation/views/
│   ├── final_optimized_main_view.py    # 最適化版実装
│   └── extreme_light_view.py           # 軽量版実装
└── その他バックアップファイル群
```

#### 実験的テストファイル群
```
archive/development_tests/
├── test_phase4_final.py                # ハイブリッドUI統合テスト
├── test_phase4_hybrid.py               # ハイブリッドテスト
├── test_phase4_migration.py            # 移行テスト
├── test_phase4_practical.py            # 実用テスト
├── test_phase4_simple.py               # シンプルテスト
├── test_phase4_sync.py                 # 同期テスト
├── test_phase2.py                      # Phase 2テスト
├── test_phase3.py                      # Phase 3テスト
├── simple_test_phase2.py               # シンプル Phase 2テスト
├── simple_test_phase3.py               # シンプル Phase 3テスト
├── test_fixed_map.py                   # マップ修正テスト
├── test_folder_content_fix.py          # フォルダ内容修正テスト
├── test_memory_only.py                 # メモリテスト
├── test_new_ui_standalone.py           # 新UI単体テスト
├── test_thumbnail_gps.py               # サムネイルGPSテスト
├── test_ui_fix.py                      # UI修正テスト
├── test_ui_improvements.py             # UI改善テスト
├── test_updated_memory.py              # 更新メモリテスト
└── 他のテストファイル
```

### Phase 2: 慎重削除（リスク: 中）

#### レガシーMainWindow実装
```
window/main_window.py                   # 266行、レガシーMainWindow
```

**依存関係確認結果**:
- 現在の`main.py`では使用されていない ✅
- `archive/`内のテストファイルでのみ参照 ✅
- 本体機能への影響なし ✅

## 🔍 依存関係分析結果

### 現在のエントリーポイント
```python
# main.py (現在の起動スクリプト)
from presentation.views.functional_new_main_view import FunctionalNewMainWindow
window = FunctionalNewMainWindow()  # 新UIのみ使用
```

### レガシーUI参照箇所
```
1. archive/backups/backup_phase5_2_20250628/main.py:91
   from window.main_window import MainWindow

2. archive/backups/backup_phase5_2_20250628_020731/main.py:91  
   from window.main_window import MainWindow

3. archive/development_tests/test_phase4_final.py:93
   from window.main_window import MainWindow

4. archive/development_tests/test_phase4_final.py:293
   from window.main_window import MainWindow
```

**結論**: レガシーUIはarchiveディレクトリ内でのみ参照され、本体機能に影響なし

## ✅ 削除安全性確認

### 本体機能への影響
- **main.py**: 新UIのみ使用、レガシーUI参照なし ✅
- **presentation層**: Clean Architecture実装、レガシーUI依存なし ✅  
- **ui層**: 新UIコンポーネント、レガシーUI独立 ✅
- **domain層**: ビジネスロジック、UI実装に依存しない ✅
- **infrastructure層**: インフラ層、UI実装に依存しない ✅

### テスト・ビルドへの影響
- **pyinstaller**: 現在のspec設定では新UIのみ対象 ✅
- **requirements.txt**: UI実装に依存しない依存関係 ✅
- **実行ファイル生成**: 新UIベースで正常動作 ✅

## 📋 削除実施手順

### Step 1: Phase 1削除
```bash
# バックアップ作成
git add -A && git commit -m "レガシーUI削除前バックアップ"

# Phase 1削除実行
rm main_hybrid.py
rm -rf archive/backups/
rm -rf archive/development_tests/
```

### Step 2: 動作確認
```bash
# アプリケーション起動テスト
python main.py

# ビルドテスト  
python -m build

# 実行ファイル生成テスト
pyinstaller photomap-explorer.spec
```

### Step 3: Phase 2削除（動作確認後）
```bash
# レガシーMainWindow削除
rm window/main_window.py
rmdir window/  # 空になった場合
```

## 🎉 削除完了後の状態

### プロジェクト構造最適化
```
photomap-explorer/
├── main.py                             # 新UI専用エントリーポイント
├── presentation/                       # Clean Architecture UI層
│   ├── views/
│   │   └── functional_new_main_view.py # メインUI実装（第3回リファクタリング対象）
│   ├── controllers/
│   ├── viewmodels/
│   └── themes/
├── domain/                             # ビジネスロジック層
├── infrastructure/                     # インフラストラクチャ層
├── ui/                                 # UIコンポーネント
└── docs/                              # ドキュメント
```

### 第3回リファクタリング準備完了
- **集中対象**: `functional_new_main_view.py` (1690行)
- **分割計画**: 8-10個の200-300行ファイル群
- **クリーンな開始**: 不要コード削除済み

---

**次のステップ**: レガシーUI削除完了後、直ちに`docs/THIRD_REFACTORING_PLAN.md`に基づく分割作業開始
