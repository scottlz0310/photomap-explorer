# PhotoMap Explorer v2.1.2 - デプロイメントガイド

## 📦 配布・パッケージング方法

PhotoMap Explorer v2.1.2の配布用パッケージを作成する方法を説明します。

### 🏗️ スタンドアロン実行ファイル（推奨）

#### Windows向けビルド

1. **ビルドスクリプトの実行**
   ```bash
   # Bashの場合
   ./build.sh
   
   # Command Promptの場合
   build.bat
   ```

2. **ビルド結果**
   - `dist/PhotoMapExplorer/` フォルダが作成されます
   - `PhotoMapExplorer.exe` が実行ファイルです
   - フォルダ全体をコピーして配布可能です

#### 手動ビルド

```bash
# 仮想環境をアクティベート
source venv/Scripts/activate  # Windows (Bash)
# または
venv\Scripts\activate.bat     # Windows (CMD)

# PyInstallerのインストール
pip install pyinstaller

# ビルド実行
pyinstaller photomap-explorer.spec

# 結果の確認
ls dist/PhotoMapExplorer/
```

### 📋 Python パッケージ（pip配布）

#### 1. 配布用パッケージの作成

```bash
# 必要なツールのインストール
pip install build twine

# パッケージのビルド
python -m build

# 生成されるファイル
# dist/photomap-explorer-2.1.2.tar.gz
# dist/photomap_explorer-2.1.2-py3-none-any.whl
```

#### 2. PyPIへのアップロード（オプション）

```bash
# テスト用PyPI（推奨）
twine upload --repository testpypi dist/*

# 本番PyPI
twine upload dist/*
```

#### 3. インストール方法（エンドユーザー向け）

```bash
# PyPIからのインストール
pip install photomap-explorer

# ローカルパッケージからのインストール
pip install photomap-explorer-2.1.2.tar.gz
```

### 🐙 GitHub Release

#### 1. リリースの作成

1. GitHubリポジトリでタグを作成:
   ```bash
   git tag -a v2.1.2 -m "PhotoMap Explorer v2.1.2 - 安定版リリース"
   git push origin v2.1.2
   ```

2. GitHub上でReleaseを作成
3. 以下のファイルを添付:
   - `dist/PhotoMapExplorer.zip` (Windows実行ファイル)
   - `dist/photomap-explorer-2.1.2.tar.gz` (ソースコード)
   - `dist/photomap_explorer-2.1.2-py3-none-any.whl` (Python wheel)

#### 2. リリースノートのテンプレート

```markdown
# PhotoMap Explorer v2.1.2 - 安定版リリース

## 🌟 新機能・改善

- **完全なダークモード・ライトモード対応**
- **GIMP風アドレスバーによる直感的ナビゲーション**
- **詳細なEXIF・GPS情報表示**
- **Clean Architectureによる高い保守性**

## 📥 ダウンロード

### Windows ユーザー（推奨）
- [PhotoMapExplorer.zip](リンク) - スタンドアロン実行ファイル
- 解凍後、`PhotoMapExplorer.exe` を実行

### Python開発者
```bash
pip install photomap-explorer==2.1.2
```

## 📋 システム要件

- **Windows**: 10/11 (x64)
- **Python**: 3.8+ (Pythonインストール版の場合)
- **メモリ**: 最小 512MB、推奨 1GB+

## 🐛 既知の問題

- 詳細は [KNOWN_ISSUES.md](リンク) を参照

## 📚 ドキュメント

- [README.md](リンク) - セットアップと使用方法
- [CHANGELOG.md](リンク) - 変更履歴
```

### 🔄 継続的インテグレーション（オプション）

GitHub Actionsを使用した自動ビルド設定:

```yaml
# .github/workflows/build.yml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pyinstaller
    - name: Build with PyInstaller
      run: pyinstaller photomap-explorer.spec
    - name: Upload artifact
      uses: actions/upload-artifact@v3
      with:
        name: PhotoMapExplorer-Windows
        path: dist/PhotoMapExplorer/
```

### 📝 配布前チェックリスト

- [ ] 全機能の動作テスト完了
- [ ] ドキュメントの最新化確認
- [ ] バージョン番号の統一確認
- [ ] ライセンス情報の確認
- [ ] セキュリティ脆弱性のチェック
- [ ] 異なる環境での動作確認
- [ ] README.mdの手順確認
- [ ] 依存関係の最新性確認

### 🚀 配布方法の選択指針

| 配布方法 | 対象ユーザー | メリット | デメリット |
|---------|-------------|----------|-----------|
| **スタンドアロン実行ファイル** | 一般ユーザー | 簡単インストール、依存関係なし | ファイルサイズ大 |
| **Python パッケージ** | 開発者 | 軽量、アップデート容易 | Python環境必須 |
| **GitHub Release** | 両方 | 版管理明確、配布経路統一 | GitHub必須 |

### 💡 推奨配布戦略

1. **メイン配布**: スタンドアロン実行ファイル（Windows向け）
2. **サブ配布**: Python パッケージ（開発者・Linux/macOS向け）
3. **管理**: GitHub Releaseで統一管理
