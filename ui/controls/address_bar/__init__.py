"""
アドレスバーモジュール統合パッケージ

このモジュールは ui/controls.py から分離されたアドレスバー機能を
統合して提供します。

主要コンポーネント:
- AddressBarCore: GIMP風ブレッドクラムアドレスバーのコア機能
- BreadcrumbManager: パス要素管理とナビゲーション機能  
- TextInputHandler: テキスト入力、補完、履歴機能
"""

from .address_bar_core import AddressBarCore
from .breadcrumb_manager import BreadcrumbManager
from .text_input_handler import TextInputHandler

# 統合アドレスバークラス
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import logging
from utils.debug_logger import debug, info, warning, error, verbose


class IntegratedAddressBar(QWidget):
    """
    統合アドレスバークラス
    
    AddressBarCore、BreadcrumbManager、TextInputHandlerを統合し、
    外部からは単一のインターフェースとして利用可能。
    元のGIMPAddressBarクラスと同等の機能を提供。
    """
    
    # シグナル
    path_changed = pyqtSignal(str)  # パス変更
    navigation_requested = pyqtSignal(str)  # ナビゲーション要求
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # コンポーネント初期化
        self.address_bar_core = AddressBarCore(self)
        self.breadcrumb_manager = BreadcrumbManager(self)
        self.text_input_handler = TextInputHandler(self)
        
        self.current_path = ""
        
        # UI設定
        self._setup_integrated_ui()
        
        # 信号接続
        self._connect_signals()
    
    def _setup_integrated_ui(self):
        """統合UIを設定"""
        try:
            # メインレイアウト
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)
            
            # アドレスバーコアを追加
            layout.addWidget(self.address_bar_core)
            
            # テキスト入力ハンドラーをアドレスバーコアに設定
            if self.address_bar_core.text_edit:
                self.text_input_handler.setup_text_input(self.address_bar_core.text_edit)
            
        except Exception as e:
            logging.error(f"統合UI設定エラー: {e}")
    
    def _connect_signals(self):
        """コンポーネント間のシグナルを接続"""
        try:
            # AddressBarCore → 外部
            self.address_bar_core.path_changed.connect(self._on_core_path_changed)
            
            # BreadcrumbManager → 外部  
            self.breadcrumb_manager.navigation_requested.connect(self._on_navigation_requested)
            
            # TextInputHandler → AddressBarCore
            self.text_input_handler.path_entered.connect(self._on_text_path_entered)
            self.text_input_handler.edit_mode_requested.connect(self._on_edit_mode_requested)
            
        except Exception as e:
            logging.error(f"シグナル接続エラー: {e}")
    
    def _on_core_path_changed(self, path: str):
        """コアのパス変更時の処理"""
        try:
            self.current_path = path
            self.path_changed.emit(path)
            
        except Exception as e:
            logging.error(f"コアパス変更処理エラー: {e}")
    
    def _on_navigation_requested(self, path: str):
        """ナビゲーション要求時の処理"""
        try:
            self.setText(path)
            self.navigation_requested.emit(path)
            
        except Exception as e:
            logging.error(f"ナビゲーション要求処理エラー: {e}")
    
    def _on_text_path_entered(self, path: str):
        """テキスト入力確定時の処理"""
        try:
            self.setText(path)
            self.path_changed.emit(path)
            
        except Exception as e:
            logging.error(f"テキストパス入力処理エラー: {e}")
    
    def _on_edit_mode_requested(self, enter_mode: bool):
        """編集モード切り替え要求時の処理"""
        try:
            if enter_mode:
                self.text_input_handler.enter_edit_mode(self.current_path)
            else:
                self.text_input_handler.exit_edit_mode()
                
        except Exception as e:
            logging.error(f"編集モード切り替え処理エラー: {e}")
    
    # 外部インターフェース（元のGIMPAddressBarと互換性）
    
    def setText(self, path: str):
        """パスを設定"""
        try:
            self.current_path = path
            self.address_bar_core.setText(path)
            
        except Exception as e:
            logging.error(f"パス設定エラー: {e}")
    
    def text(self) -> str:
        """現在のパスを取得"""
        return self.current_path
    
    def setVisible(self, visible: bool):
        """表示/非表示を設定"""
        super().setVisible(visible)
    
    def apply_theme(self, theme_name: str):
        """テーマを適用"""
        try:
            self.address_bar_core.apply_theme(theme_name)
            self.text_input_handler.apply_theme_style(theme_name)
            
        except Exception as e:
            logging.error(f"テーマ適用エラー: {e}")


# パッケージレベルのエクスポート
__all__ = [
    'AddressBarCore',
    'BreadcrumbManager', 
    'TextInputHandler',
    'IntegratedAddressBar'
]


# 後方互換性のための別名
GIMPAddressBar = IntegratedAddressBar
