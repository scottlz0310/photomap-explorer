"""
ベースViewModelクラス

MVVMパターンにおけるViewModelの基底クラス
観察可能なプロパティとコマンドの基本機能を提供
"""

from abc import ABC, ABCMeta
from typing import Any, Callable, Dict, List, Optional, Set
from PyQt5.QtCore import QObject, pyqtSignal
import logging


class ObservableProperty:
    """
    観察可能なプロパティ
    
    値の変更時に自動的に通知を発行するプロパティ
    """
    
    def __init__(self, initial_value: Any = None, name: str = ""):
        self._value = initial_value
        self._name = name
        self._observers: Set[Callable] = set()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._value
    
    def __set__(self, instance, value):
        if self._value != value:
            old_value = self._value
            self._value = value
            self._notify_observers(instance, old_value, value)
    
    def _notify_observers(self, instance, old_value, new_value):
        """観察者に変更を通知"""
        for observer in self._observers:
            try:
                observer(instance, self._name, old_value, new_value)
            except Exception as e:
                logging.error(f"Property observer error: {e}")
    
    def add_observer(self, observer: Callable):
        """観察者を追加"""
        self._observers.add(observer)
    
    def remove_observer(self, observer: Callable):
        """観察者を削除"""
        self._observers.discard(observer)


class Command:
    """
    コマンドクラス
    
    UIアクションを表現し、実行可能性の制御を行う
    """
    
    def __init__(self, execute_func: Callable, can_execute_func: Optional[Callable] = None):
        self._execute_func = execute_func
        self._can_execute_func = can_execute_func or (lambda: True)
        self._can_execute_changed_callbacks: List[Callable] = []
    
    def execute(self, *args, **kwargs):
        """コマンドを実行"""
        if self.can_execute():
            try:
                return self._execute_func(*args, **kwargs)
            except Exception as e:
                logging.error(f"Command execution error: {e}")
                raise
        else:
            logging.warning("Command execution attempted but can_execute returned False")
    
    def can_execute(self) -> bool:
        """コマンドが実行可能かを判定"""
        try:
            return self._can_execute_func()
        except Exception as e:
            logging.error(f"Command can_execute error: {e}")
            return False
    
    def add_can_execute_changed_callback(self, callback: Callable):
        """実行可能性変更時のコールバックを追加"""
        self._can_execute_changed_callbacks.append(callback)
    
    def raise_can_execute_changed(self):
        """実行可能性が変更されたことを通知"""
        for callback in self._can_execute_changed_callbacks:
            try:
                callback()
            except Exception as e:
                logging.error(f"Can execute changed callback error: {e}")


class QObjectMeta(type(QObject), ABCMeta):
    """QObjectとABCのメタクラス競合を解決するメタクラス"""
    pass


class BaseViewModel(QObject, ABC, metaclass=QObjectMeta):
    """
    ViewModelの基底クラス
    
    MVVMパターンにおけるViewModelの共通機能を提供:
    - プロパティ変更通知
    - コマンド管理
    - エラーハンドリング
    - ログ出力
    """
    
    # PyQt5シグナル
    property_changed = pyqtSignal(str, object, object)  # property_name, old_value, new_value
    error_occurred = pyqtSignal(str, str)  # error_type, error_message
    busy_state_changed = pyqtSignal(bool)  # is_busy
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._logger = logging.getLogger(self.__class__.__name__)
        self._commands: Dict[str, Command] = {}
        self._is_busy = False
        self._errors: List[str] = []
        
        # プロパティ変更の監視設定
        self._setup_property_observers()
    
    def _setup_property_observers(self):
        """プロパティ観察者を設定"""
        # クラスの全ての ObservableProperty に観察者を追加
        for attr_name in dir(self.__class__):
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, ObservableProperty):
                attr.add_observer(self._on_property_changed)
    
    def _on_property_changed(self, instance, property_name: str, old_value, new_value):
        """プロパティ変更時のハンドラ"""
        if instance is self:
            self._logger.debug(f"Property '{property_name}' changed: {old_value} -> {new_value}")
            self.property_changed.emit(property_name, old_value, new_value)
            
            # コマンドの実行可能性を再評価
            self._refresh_commands()
    
    def add_command(self, name: str, command: Command):
        """コマンドを追加"""
        self._commands[name] = command
        command.add_can_execute_changed_callback(lambda: self._refresh_command(name))
    
    def get_command(self, name: str) -> Optional[Command]:
        """コマンドを取得"""
        return self._commands.get(name)
    
    def _refresh_commands(self):
        """全コマンドの実行可能性を更新"""
        for name in self._commands:
            self._refresh_command(name)
    
    def _refresh_command(self, name: str):
        """指定されたコマンドの実行可能性を更新"""
        command = self._commands.get(name)
        if command:
            command.raise_can_execute_changed()
    
    @property
    def is_busy(self) -> bool:
        """ビジー状態を取得"""
        return self._is_busy
    
    @is_busy.setter
    def is_busy(self, value: bool):
        """ビジー状態を設定"""
        if self._is_busy != value:
            self._is_busy = value
            self.busy_state_changed.emit(value)
            self._refresh_commands()
    
    @property
    def has_errors(self) -> bool:
        """エラーがあるかを確認"""
        return len(self._errors) > 0
    
    @property
    def errors(self) -> List[str]:
        """エラーリストを取得"""
        return self._errors.copy()
    
    def add_error(self, error_message: str, error_type: str = "General"):
        """エラーを追加"""
        self._errors.append(error_message)
        self._logger.error(f"{error_type}: {error_message}")
        self.error_occurred.emit(error_type, error_message)
    
    def clear_errors(self):
        """エラーをクリア"""
        self._errors.clear()
    
    def log_info(self, message: str):
        """情報ログを出力"""
        self._logger.info(message)
    
    def log_debug(self, message: str):
        """デバッグログを出力"""
        self._logger.debug(message)
    
    def log_warning(self, message: str):
        """警告ログを出力"""
        self._logger.warning(message)
    
    def log_error(self, message: str):
        """エラーログを出力"""
        self._logger.error(message)
    
    def handle_exception(self, exception: Exception, context: str = ""):
        """例外を処理"""
        error_message = f"{context}: {str(exception)}" if context else str(exception)
        self.add_error(error_message, "Exception")
        self.log_error(f"Exception in {self.__class__.__name__}: {error_message}")
    
    def validate(self) -> bool:
        """
        ViewModelの状態を検証
        
        サブクラスでオーバーライドして独自の検証ロジックを実装
        """
        return True
    
    def reset(self):
        """
        ViewModelの状態をリセット
        
        サブクラスでオーバーライドして独自のリセットロジックを実装
        """
        self.clear_errors()
        self.is_busy = False
    
    def dispose(self):
        """
        リソースを解放
        
        ViewModelが不要になった際に呼び出し
        """
        self._commands.clear()
        self.clear_errors()
        
        # プロパティ観察者をクリア
        for attr_name in dir(self.__class__):
            attr = getattr(self.__class__, attr_name)
            if isinstance(attr, ObservableProperty):
                attr._observers.clear()


class AsyncCommand(Command):
    """
    非同期コマンドクラス
    
    非同期処理を伴うコマンドの実行を管理
    """
    
    def __init__(self, async_execute_func: Callable, can_execute_func: Optional[Callable] = None):
        self._async_execute_func = async_execute_func
        super().__init__(self._sync_execute, can_execute_func)
        self._is_executing = False
    
    def _sync_execute(self, *args, **kwargs):
        """同期的な実行ラッパー"""
        if self._is_executing:
            return
        
        self._is_executing = True
        try:
            import asyncio
            # 既存のイベントループがある場合はタスクとして追加
            try:
                loop = asyncio.get_running_loop()
                return loop.create_task(self._async_execute_func(*args, **kwargs))
            except RuntimeError:
                # イベントループがない場合は新しく作成
                return asyncio.run(self._async_execute_func(*args, **kwargs))
        finally:
            self._is_executing = False
    
    def can_execute(self) -> bool:
        """実行中でない場合のみ実行可能"""
        return not self._is_executing and super().can_execute()


# 便利なデコレータ
def observable_property(initial_value: Any = None):
    """
    観察可能プロパティのデコレータ
    
    使用例:
    @observable_property("")
    def my_property(self): pass
    """
    def decorator(func):
        prop_name = func.__name__
        return ObservableProperty(initial_value, prop_name)
    return decorator


def command_method(can_execute_func: Optional[Callable] = None):
    """
    コマンドメソッドのデコレータ
    
    使用例:
    @command_method(lambda self: not self.is_busy)
    def my_command(self): pass
    """
    def decorator(func):
        def wrapper(self):
            command_name = func.__name__
            if not hasattr(self, '_commands'):
                self._commands = {}
            
            if command_name not in self._commands:
                can_exec = can_execute_func(self) if can_execute_func else lambda: True
                command = Command(lambda: func(self), can_exec)
                self._commands[command_name] = command
            
            return self._commands[command_name]
        return wrapper
    return decorator
