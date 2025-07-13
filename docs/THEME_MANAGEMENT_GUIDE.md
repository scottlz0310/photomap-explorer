# テーマ管理ガイド

## 現在の構成

### 有効なテーマ（3個）
- `dark` - ダークモード（普段使い）
- `light` - ライトモード（普段使い）
- `high_contrast` - ハイコントラスト（アクセシビリティ対応）

### 無効化されたテーマ（13個）
すべて `disabled_themes` セクションに保存済み：
- `blue`, `green`, `purple` - カラーテーマ
- `orange`, `pink`, `red`, `teal`, `yellow`, `gray` - 拡張カラーテーマ
- `sepia`, `cyberpunk`, `forest`, `ocean` - 特殊テーマ

## テーマの再有効化方法

### 1. 単一テーマを有効化
1. `settings/theme_settings.json` を開く
2. `disabled_themes` セクションから使いたいテーマをコピー
3. `available_themes` セクションに貼り付け
4. `disabled_themes` から該当テーマを削除（または残す）

**例：ブルーテーマを有効化**
```json
"available_themes": {
  "dark": { ... },
  "light": { ... },
  "high_contrast": { ... },
  "blue": {
    "name": "blue",
    "display_name": "ブルーモード",
    "description": "プロフェッショナルなブルーベーステーマ",
    // ... 以下すべてのブルーテーマ設定
  }
}
```

### 2. 複数テーマを一括有効化
1. `disabled_themes` から必要なテーマを選択してコピー
2. `available_themes` に一度に貼り付け
3. カンマ区切りに注意

### 3. 全テーマを復活
1. `disabled_themes` セクション全体をコピー
2. `available_themes` に統合
3. 不要なコメント行を削除

## ファイル構造
```
settings/
├── theme_settings.json         # メイン設定ファイル
├── theme_settings_backup.json  # 全テーマ版のバックアップ
```

## バックアップの利用
元の16テーマ構成に戻したい場合：
```bash
cd /home/hiro/Projects/photomap-explorer
cp settings/theme_settings_backup.json settings/theme_settings.json
```

## カスタムテーマの追加
新しいテーマは `available_themes` または `disabled_themes` のどちらにも追加可能：

```json
"my_custom": {
  "name": "my_custom",
  "display_name": "マイカスタム",
  "description": "自分だけのテーマ",
  "primaryColor": "#色コード",
  "accentColor": "#色コード",
  "backgroundColor": "#色コード",
  "textColor": "#色コード",
  "button": {
    "background": "#色コード",
    "text": "#色コード",
    "hover": "#色コード"
  },
  "panel": {
    "background": "#色コード",
    "border": "#色コード"
  }
}
```

## テスト方法
テーマ変更後の動作確認：
```bash
python test_simplified_themes.py
```

## 注意事項
- JSONファイル編集時は構文エラーに注意
- テーマ名は一意である必要がある
- `available_themes` のテーマのみがアプリで利用可能
- `disabled_themes` は単なる保存領域（アプリは読み込まない）
