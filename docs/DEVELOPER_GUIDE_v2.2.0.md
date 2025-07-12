# 🛠️ PhotoMap Explorer 開発者ガイド v2.2.0

**対象**: 開発者・コントリビューター  
**最終更新**: 2025年7月12日  
**対象バージョン**: v2.2.0以降  

---

## 🎯 概要

PhotoMap Explorer v2.2.0 の新しいモジュラーアーキテクチャでの開発方法を説明します。第2回リファクタリング完了後の構造に基づいて、効率的な開発・拡張・テスト方法を提供します。

---

## 🚀 クイックスタート

### 開発環境セットアップ

```bash
# リポジトリクローン
git clone https://github.com/scottlz0310/photomap-explorer.git
cd photomap-explorer

# 仮想環境作成
python -m venv venv
source venv/bin/activate  # Linux/macOS
# または
venv\Scripts\activate     # Windows

# 依存関係インストール
pip install -r requirements.txt

# 開発用テスト実行
python simple_test.py
```

### 基本動作確認

```python
# テーマシステムのテスト
from presentation.themes.definitions.light_theme import create_light_theme
from presentation.themes.definitions.dark_theme import create_dark_theme

light = create_light_theme()
dark = create_dark_theme()
print(f"ライトテーマ: {light['name']}")
print(f"ダークテーマ: {dark['name']}")

# UIコントロールのテスト
from ui.controls.address_bar.address_bar_core import AddressBarCore
from ui.controls.toolbar.navigation_controls import NavigationControls
print("UIコントロール読み込み成功")
```

---

## 🏗️ アーキテクチャ理解

### モジュール構造

```
photomap-explorer/
├── 📂 presentation/themes/    # テーマシステム（Phase 3）
│   ├── core/                  # コア機能
│   ├── system/                # システム連携
│   ├── definitions/           # テーマ定義
│   └── __init__.py           # 統合インターフェース
├── 📂 ui/controls/           # UIコントロール（Phase 2）
│   ├── address_bar/          # アドレスバー機能
│   ├── toolbar/              # ツールバー機能
│   └── __init__.py          # 統合インターフェース
└── 📂 その他のモジュール...
```

### 設計原則
1. **単一責任**: 各モジュールは1つの明確な責任
2. **疎結合**: モジュール間の依存関係を最小限に
3. **高凝集**: 関連する機能を同じモジュールに
4. **テスト容易**: 独立したユニットテスト対応

---

## 🎨 テーマシステム開発

### 新しいテーマの作成

#### 1. テーマ定義ファイル作成

```python
# presentation/themes/definitions/custom_theme.py

def create_custom_theme() -> Dict[str, Any]:
    """カスタムテーマ定義を作成"""
    return {
        "name": "custom",
        "display_name": "カスタムテーマ",
        "description": "独自のカスタムテーマ",
        "version": "1.0.0",
        "colors": {
            "background": "#f0f0f0",
            "foreground": "#333333",
            "primary": "#007acc",
            "secondary": "#e0e0e0",
            "accent": "#ff6b35",
            # 必要なカラーを定義
        },
        "styles": {
            "main_window": """
QMainWindow {{
    background-color: {background};
    color: {foreground};
}}
            """,
            # 必要なスタイルを定義
        }
    }
```

#### 2. テーマファクトリーに登録

```python
# カスタムテーマの登録例
from presentation.themes.core.theme_factory import ThemeFactory
from .definitions.custom_theme import create_custom_theme

factory = ThemeFactory()
factory.register_theme_creator("custom", create_custom_theme)
```

#### 3. テーマの使用

```python
from presentation.themes import ThemeManager

manager = ThemeManager()
manager.set_current_theme("custom")
```

### テーマカスタマイズ

```python
# カラーオーバーライド例
custom_colors = {
    "primary": "#ff0000",
    "accent": "#00ff00"
}

# カスタムテーマ作成
from presentation.themes.core.theme_factory import ThemeFactory
factory = ThemeFactory()

custom_theme = factory.create_theme(
    "light", 
    color_overrides=custom_colors,
    font_scale=1.2
)
```

---

## 🎛️ UIコントロール開発

### 新しいコントロールの作成

#### 1. コントロールクラス作成

```python
# ui/controls/custom/my_control.py

from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout
from PyQt5.QtCore import pyqtSignal

class MyCustomControl(QWidget):
    """カスタムコントロール例"""
    
    # シグナル定義
    action_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()
        
    def _setup_ui(self):
        """UI初期化"""
        layout = QHBoxLayout(self)
        
        self.button = QPushButton("カスタムアクション")
        self.button.clicked.connect(self._on_button_clicked)
        layout.addWidget(self.button)
        
    def _on_button_clicked(self):
        """ボタンクリック時の処理"""
        self.action_requested.emit("custom_action")
        
    def apply_theme(self, theme_name: str):
        """テーマ適用"""
        # テーマに応じたスタイル適用
        pass
```

#### 2. 統合インターフェースに追加

```python
# ui/controls/custom/__init__.py

from .my_control import MyCustomControl

__all__ = ['MyCustomControl']

# ui/controls/__init__.py に追加
from .custom import MyCustomControl
```

### 既存コントロールの拡張

```python
# AddressBarCoreの拡張例
from ui.controls.address_bar.address_bar_core import AddressBarCore

class ExtendedAddressBar(AddressBarCore):
    """拡張アドレスバー"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._add_custom_features()
        
    def _add_custom_features(self):
        """カスタム機能追加"""
        # 新機能実装
        pass
```

---

## 🧪 テスト開発

### ユニットテストの作成

#### テーマシステムのテスト

```python
# tests/unit/themes/test_theme_factory.py

import unittest
from presentation.themes.core.theme_factory import ThemeFactory

class TestThemeFactory(unittest.TestCase):
    
    def setUp(self):
        self.factory = ThemeFactory()
        
    def test_create_light_theme(self):
        """ライトテーマ作成テスト"""
        theme = self.factory.create_theme("light")
        
        self.assertIsNotNone(theme)
        self.assertEqual(theme["name"], "light")
        self.assertIn("colors", theme)
        self.assertIn("styles", theme)
        
    def test_theme_validation(self):
        """テーマバリデーションテスト"""
        valid_theme = {
            "name": "test",
            "colors": {"background": "#ffffff"},
            "styles": {"main_window": "QMainWindow {}"}
        }
        
        self.assertTrue(self.factory.validate_theme(valid_theme))
        
    def test_custom_theme_creation(self):
        """カスタムテーマ作成テスト"""
        custom_theme = self.factory.create_custom_theme(
            "my_theme",
            "light",
            {"color_overrides": {"primary": "#ff0000"}}
        )
        
        self.assertIsNotNone(custom_theme)
        self.assertEqual(custom_theme["name"], "my_theme")

if __name__ == '__main__':
    unittest.main()
```

#### UIコントロールのテスト

```python
# tests/unit/ui/test_address_bar_core.py

import unittest
from PyQt5.QtWidgets import QApplication
from ui.controls.address_bar.address_bar_core import AddressBarCore

class TestAddressBarCore(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        if not QApplication.instance():
            cls.app = QApplication([])
        
    def setUp(self):
        self.address_bar = AddressBarCore()
        
    def test_initialization(self):
        """初期化テスト"""
        self.assertIsNotNone(self.address_bar)
        self.assertEqual(self.address_bar.get_current_path(), "")
        
    def test_path_setting(self):
        """パス設定テスト"""
        test_path = "/home/user/documents"
        self.address_bar.set_path(test_path)
        self.assertEqual(self.address_bar.get_current_path(), test_path)
        
    def test_breadcrumb_creation(self):
        """ブレッドクラム作成テスト"""
        test_path = "/home/user/documents"
        self.address_bar.set_path(test_path)
        
        breadcrumbs = self.address_bar.get_breadcrumbs()
        expected = ["", "home", "user", "documents"]
        self.assertEqual(breadcrumbs, expected)

if __name__ == '__main__':
    unittest.main()
```

### 統合テストの実行

```bash
# 全テスト実行
python -m pytest tests/

# 特定モジュールのテスト
python -m pytest tests/unit/themes/

# カバレッジ付きテスト
python -m pytest --cov=presentation.themes tests/unit/themes/
```

---

## 🔧 デバッグ・トラブルシューティング

### よくある問題と解決方法

#### 1. インポートエラー

```python
# 問題: ModuleNotFoundError
# 解決: Pythonパスの確認
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
```

#### 2. テーママネージャーのエラー

```python
# 問題: テーママネージャーの初期化失敗
# 解決: 段階的初期化
try:
    from presentation.themes import ThemeManager
    manager = ThemeManager()
except Exception as e:
    print(f"テーママネージャーエラー: {e}")
    # フォールバック処理
```

#### 3. UIコントロールの表示問題

```python
# 問題: QApplicationが必要
# 解決: アプリケーション初期化確認
from PyQt5.QtWidgets import QApplication

if not QApplication.instance():
    app = QApplication([])

# その後でUIコントロール作成
```

### ログレベル設定

```python
import logging

# デバッグモード有効化
logging.basicConfig(level=logging.DEBUG)

# 特定モジュールのログレベル設定
logging.getLogger('presentation.themes').setLevel(logging.DEBUG)
logging.getLogger('ui.controls').setLevel(logging.INFO)
```

---

## 📚 ベストプラクティス

### コード品質

#### 1. 命名規則
```python
# クラス名: PascalCase
class ThemeManager:
    pass

# 関数・変数名: snake_case
def create_light_theme():
    current_theme = "light"

# 定数: UPPER_SNAKE_CASE
DEFAULT_THEME = "light"
```

#### 2. ドキュメント
```python
def create_theme(theme_name: str, **kwargs) -> Optional[Dict[str, Any]]:
    """
    テーマを作成
    
    Args:
        theme_name: テーマ名
        **kwargs: カスタマイズパラメータ
        
    Returns:
        Optional[Dict[str, Any]]: テーマ定義、失敗時はNone
        
    Examples:
        >>> factory = ThemeFactory()
        >>> theme = factory.create_theme("light")
        >>> print(theme["name"])
        light
    """
```

#### 3. エラーハンドリング
```python
def safe_operation():
    """安全な操作の例"""
    try:
        # メイン処理
        result = risky_operation()
        return result
    except SpecificException as e:
        logging.error(f"特定エラー: {e}")
        return None
    except Exception as e:
        logging.error(f"予期しないエラー: {e}")
        raise
```

### パフォーマンス

#### 1. 遅延読み込み
```python
class ThemeManager:
    def __init__(self):
        self._theme_data = None
        
    @property
    def theme_data(self):
        """遅延読み込みプロパティ"""
        if self._theme_data is None:
            self._theme_data = self._load_theme_data()
        return self._theme_data
```

#### 2. キャッシュ活用
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_processed_theme(theme_name: str) -> Dict[str, Any]:
    """キャッシュ付きテーマ処理"""
    return process_theme(theme_name)
```

---

## 🚀 高度な開発

### プラグインシステム（将来対応）

```python
# plugin_interface.py
from abc import ABC, abstractmethod

class ThemePlugin(ABC):
    """テーマプラグインインターフェース"""
    
    @abstractmethod
    def get_theme_name(self) -> str:
        pass
        
    @abstractmethod
    def create_theme(self) -> Dict[str, Any]:
        pass

# カスタムプラグイン実装例
class MyThemePlugin(ThemePlugin):
    def get_theme_name(self) -> str:
        return "my_custom_theme"
        
    def create_theme(self) -> Dict[str, Any]:
        return {
            "name": self.get_theme_name(),
            # テーマ定義
        }
```

### 設定システム拡張

```python
# 設定プロバイダーの実装例
class CustomSettingsProvider:
    """カスタム設定プロバイダー"""
    
    def load_settings(self) -> Dict[str, Any]:
        # カスタム設定読み込み
        pass
        
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        # カスタム設定保存
        pass
```

---

## 📋 リリース・デプロイメント

### バージョン管理

```python
# version.py
__version__ = "2.2.0"
__build__ = "20250712"

# アプリケーション内でのバージョン確認
from .version import __version__
print(f"PhotoMap Explorer v{__version__}")
```

### パッケージング

```bash
# 開発版ビルド
python setup.py build

# 配布用パッケージ作成
python setup.py sdist bdist_wheel

# インストール可能パッケージの確認
pip install -e .
```

---

## 🆘 サポート・コミュニティ

### 問題報告
- **GitHub Issues**: バグ報告・機能要求
- **Discussion**: 質問・議論
- **Pull Request**: コード貢献

### 開発参加
1. **Fork** リポジトリ
2. **Feature branch** 作成
3. **Tests** 追加・実行
4. **Pull Request** 作成

### ドキュメント
- `docs/ARCHITECTURE_v2.2.0.md`: アーキテクチャ仕様
- `docs/REFACTORING_COMPLETION_REPORT.md`: リファクタリング報告
- `CHANGELOG.md`: 変更履歴

---

**Happy Coding! 🚀**

**作成者**: PhotoMap Explorer Development Team  
**最終更新**: 2025年7月12日
