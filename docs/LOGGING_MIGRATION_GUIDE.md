# ログ移行ガイド

## 概要
このファイルは、`utils.debug_logger`から標準の`logging`モジュールへの移行を簡単にするためのガイドです。

## ログブリッジの使用方法

### 基本的な使い方

```python
from utils.logging_bridge import get_theme_logger

# コンテキスト付きロガーを取得
logger = get_theme_logger("ComponentName")

# ログ出力
logger.debug("デバッグメッセージ")
logger.info("情報メッセージ")
logger.warning("警告メッセージ")
logger.error("エラーメッセージ")
logger.verbose("詳細メッセージ")
```

### 専用ロガーの種類

```python
from utils.logging_bridge import (
    get_theme_logger,    # テーマシステム用
    get_ui_logger,       # UI系用
    get_system_logger    # システム系用
)

theme_logger = get_theme_logger("ThemeManager")
ui_logger = get_ui_logger("MainWindow")
system_logger = get_system_logger("FileHandler")
```

### カスタムロガーの作成

```python
from utils.logging_bridge import create_contextual_logger

# カスタムロガーを作成
custom_logger = create_contextual_logger("photomap.custom", "MyComponent")
custom_logger.info("カスタムログメッセージ")
```

## 移行手順

### 1. 現在の使用方法
```python
# 従来の方法
from utils.debug_logger import debug, info, warning, error, verbose

debug("デバッグメッセージ")
info("情報メッセージ")
```

### 2. ログブリッジ使用への移行
```python
# ログブリッジ使用
from utils.logging_bridge import get_theme_logger

class MyClass:
    def __init__(self):
        self.logger = get_theme_logger("MyClass")
    
    def some_method(self):
        self.logger.debug("デバッグメッセージ")
        self.logger.info("情報メッセージ")
```

### 3. 標準loggingへの最終移行
```python
# 最終的な標準logging使用
import logging

class MyClass:
    def __init__(self):
        self.logger = logging.getLogger("photomap.theme.MyClass")
    
    def some_method(self):
        self.logger.debug("デバッグメッセージ")
        self.logger.info("情報メッセージ")
```

## グローバル設定切り替え

```python
from utils.logging_bridge import set_standard_logging

# 標準loggingに切り替え（アプリケーション全体で有効）
set_standard_logging(True)

# debug_loggerに戻す
set_standard_logging(False)
```

## 利点

1. **段階的移行**: 一度に全てを変更する必要がない
2. **統一インターフェース**: どちらのログシステムでも同じメソッド名を使用
3. **コンテキスト管理**: ログメッセージにコンテキスト情報を自動付与
4. **設定の一元化**: アプリケーション全体のログシステムをワンタッチで切り替え可能

## 更新済みファイル

- `presentation/views/functional_main_window/event_handlers/theme_event_handler.py`
- `presentation/themes/integrated_theme_manager.py`

これらのファイルはログブリッジを使用するように更新済みです。今後標準loggingに完全移行する際は、`set_standard_logging(True)`を呼び出すだけで切り替え可能です。
