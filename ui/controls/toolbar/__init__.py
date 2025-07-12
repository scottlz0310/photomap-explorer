"""
ツールバーモジュール統合パッケージ

このモジュールは ui/controls.py から分離されたツールバー機能を
統合して提供します。

主要コンポーネント:
- NavigationControls: ナビゲーション制御機能（戻る/進む/親フォルダ/ホーム/更新）
- UtilityControls: ユーティリティ機能（表示モード/テーマ/設定/ヘルプ）
"""

from .navigation_controls import NavigationControls
from .utility_controls import UtilityControls

# 統合ツールバークラス
from PyQt5.QtWidgets import QWidget, QHBoxLayout
from PyQt5.QtCore import pyqtSignal
import logging


class IntegratedToolbar(QWidget):
    """
    統合ツールバークラス
    
    NavigationControlsとUtilityControlsを統合し、
    外部からは単一のインターフェースとして利用可能。
    元のcreate_controls関数と同等の機能を提供。
    """
    
    # シグナル - ナビゲーション関連
    parent_folder_requested = pyqtSignal()
    home_folder_requested = pyqtSignal()
    back_requested = pyqtSignal()
    forward_requested = pyqtSignal()
    refresh_requested = pyqtSignal()
    
    # シグナル - ユーティリティ関連
    view_mode_changed = pyqtSignal(str)
    settings_requested = pyqtSignal()
    help_requested = pyqtSignal()
    theme_changed = pyqtSignal(str)
    layout_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # コンポーネント初期化
        self.navigation_controls = NavigationControls(self)
        self.utility_controls = UtilityControls(self)
        
        # 状態管理
        self.current_path = ""
        
        # UI設定
        self._setup_integrated_ui()
        
        # シグナル接続
        self._connect_signals()
    
    def _setup_integrated_ui(self):
        """統合UIを設定"""
        try:
            # メインレイアウト
            layout = QHBoxLayout(self)
            layout.setContentsMargins(4, 2, 4, 2)
            layout.setSpacing(8)
            
            # ナビゲーションコントロールを左側に
            layout.addWidget(self.navigation_controls)
            
            # 中央にスペーサー
            layout.addStretch()
            
            # ユーティリティコントロールを右側に
            layout.addWidget(self.utility_controls)
            
        except Exception as e:
            logging.error(f"統合ツールバーUI設定エラー: {e}")
    
    def _connect_signals(self):
        """コンポーネント間のシグナルを接続"""
        try:
            # NavigationControls → 外部
            self.navigation_controls.parent_folder_requested.connect(self.parent_folder_requested)
            self.navigation_controls.home_folder_requested.connect(self.home_folder_requested)
            self.navigation_controls.back_requested.connect(self.back_requested)
            self.navigation_controls.forward_requested.connect(self.forward_requested)
            self.navigation_controls.refresh_requested.connect(self.refresh_requested)
            
            # UtilityControls → 外部
            self.utility_controls.view_mode_changed.connect(self.view_mode_changed)
            self.utility_controls.settings_requested.connect(self.settings_requested)
            self.utility_controls.help_requested.connect(self.help_requested)
            self.utility_controls.theme_changed.connect(self.theme_changed)
            self.utility_controls.layout_changed.connect(self.layout_changed)
            
        except Exception as e:
            logging.error(f"ツールバーシグナル接続エラー: {e}")
    
    # 外部インターフェース（元のcreate_controls関数の機能）
    
    def set_current_path(self, path: str):
        """現在のパスを設定"""
        try:
            self.current_path = path
            self.navigation_controls.set_current_path(path)
            
        except Exception as e:
            logging.error(f"ツールバーパス設定エラー: {e}")
    
    def set_history_state(self, can_back: bool, can_forward: bool):
        """履歴ボタンの状態を設定"""
        try:
            self.navigation_controls.set_history_state(can_back, can_forward)
            
        except Exception as e:
            logging.error(f"履歴状態設定エラー: {e}")
    
    def set_view_mode(self, mode: str):
        """表示モードを設定"""
        try:
            self.utility_controls.set_view_mode(mode)
            
        except Exception as e:
            logging.error(f"表示モード設定エラー: {e}")
    
    def set_theme(self, theme: str):
        """テーマを設定"""
        try:
            self.utility_controls.set_theme(theme)
            
        except Exception as e:
            logging.error(f"テーマ設定エラー: {e}")
    
    def set_layout(self, layout_type: str):
        """レイアウトを設定"""
        try:
            self.utility_controls.set_layout(layout_type)
            
        except Exception as e:
            logging.error(f"レイアウト設定エラー: {e}")
    
    def apply_theme(self, theme_name: str):
        """テーマを適用"""
        try:
            self.navigation_controls.apply_theme(theme_name)
            self.utility_controls.apply_theme(theme_name)
            
        except Exception as e:
            logging.error(f"ツールバーテーマ適用エラー: {e}")
    
    def get_navigation_controls(self) -> NavigationControls:
        """ナビゲーションコントロールを取得"""
        return self.navigation_controls
    
    def get_utility_controls(self) -> UtilityControls:
        """ユーティリティコントロールを取得"""
        return self.utility_controls


# パッケージレベルのエクスポート
__all__ = [
    'NavigationControls',
    'UtilityControls', 
    'IntegratedToolbar'
]


# 個別の関数として機能を提供（元のcreate_controls関数の代替）
def create_controls(parent=None):
    """
    統合ツールバーを作成
    
    元のcreate_controls関数と同等の機能を提供します。
    後方互換性のためのラッパー関数。
    
    Args:
        parent: 親ウィジェット
        
    Returns:
        IntegratedToolbar: 統合ツールバーインスタンス
    """
    return IntegratedToolbar(parent)
