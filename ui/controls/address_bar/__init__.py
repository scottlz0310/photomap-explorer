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
        
        # デバッグ: 初期化時の状態
        debug(f"🔧 🔧 🔧 🔧 🔧 IntegratedAddressBar初期化開始: parent={parent}")
        
        # コンポーネント初期化（適切な親を指定）
        self.address_bar_core = AddressBarCore(self)  # 明示的にselfを親として指定
        self.breadcrumb_manager = BreadcrumbManager(self)  # 明示的にselfを親として指定  
        self.text_input_handler = TextInputHandler(self)  # 明示的にselfを親として指定
        
        self.current_path = ""
        
        # UI設定
        self._setup_integrated_ui()
        
        # 信号接続
        self._connect_signals()
        
        # 明示的に表示状態を設定
        self.setVisible(True)
        self.show()
        
        # 初期化完了後のvisibility維持処理
        from PyQt5.QtCore import QTimer
        def ensure_initial_visibility():
            """初期化後の表示確保"""
            try:
                # IntegratedAddressBar自体の状態確認
                debug(f"🔧 🔧 🔧 初期化遅延処理: IntegratedAddressBar visible={self.isVisible()}, size={self.size()}")
                
                # 内部コンポーネントの状態確認
                if hasattr(self, 'address_bar_core') and self.address_bar_core:
                    debug(f"🔧 🔧 🔧 AddressBarCore visible={self.address_bar_core.isVisible()}, size={self.address_bar_core.size()}")
                    
                    if hasattr(self.address_bar_core, 'breadcrumb_widget') and self.address_bar_core.breadcrumb_widget:
                        debug(f"🔧 🔧 🔧 breadcrumb_widget visible={self.address_bar_core.breadcrumb_widget.isVisible()}, size={self.address_bar_core.breadcrumb_widget.size()}")
                    
                    if hasattr(self.address_bar_core, 'edit_button') and self.address_bar_core.edit_button:
                        debug(f"🔧 🔧 🔧 edit_button visible={self.address_bar_core.edit_button.isVisible()}, size={self.address_bar_core.edit_button.size()}")
                
                # 強制表示設定
                if not self.isVisible():
                    debug(f"🔧 🔧 🔧 初期化後遅延処理: 非表示になっているため再表示")
                    self.setVisible(True)
                    self.show()
                
                # 内部コンポーネントも強制表示
                if hasattr(self, 'address_bar_core') and self.address_bar_core:
                    self.address_bar_core.setVisible(True)
                    self.address_bar_core.show()
                    
                    if hasattr(self.address_bar_core, 'breadcrumb_widget') and self.address_bar_core.breadcrumb_widget:
                        self.address_bar_core.breadcrumb_widget.setVisible(True)
                        self.address_bar_core.breadcrumb_widget.show()
                
                debug(f"🔧 🔧 🔧 初期化遅延処理完了: visible={self.isVisible()}")
            except Exception as e:
                debug(f"🔧 🔧 🔧 初期化遅延処理エラー: {e}")
        
        QTimer.singleShot(50, ensure_initial_visibility)
        
        debug(f"🔧 🔧 🔧 🔧 IntegratedAddressBar初期化完了: visible={self.isVisible()}, parent={self.parent()}")
        
        # シンプルなスタイルを適用（デバッグ用の派手なスタイルを削除）
        self.setStyleSheet("""
            IntegratedAddressBar {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                min-height: 35px;
                max-height: 40px;
                padding: 2px;
            }
        """)
    
    def setParent(self, parent):
        """親ウィジェット設定時のvisibility追跡"""
        debug(f"🔧 🔧 🔧 IntegratedAddressBar.setParent呼び出し: old_parent={self.parent()}, new_parent={parent}")
        debug(f"🔧 🔧 🔧 setParent前: visible={self.isVisible()}, size={self.size()}")
        
        # スタックトレースを取得して呼び出し元を特定
        import traceback
        debug(f"🔧 🔧 🔧 setParent呼び出しスタック:\n{''.join(traceback.format_stack()[-5:])}")
        
        old_visible = self.isVisible()
        super().setParent(parent)
        new_visible = self.isVisible()
        
        debug(f"🔧 🔧 🔧 setParent後: visible={new_visible}, size={self.size()}, parent={self.parent()}")
        debug(f"🔧 🔧 🔧 IntegratedAddressBar.setParent完了: visible変化 {old_visible} → {new_visible}")
        
        # 親ウィジェットの状態もチェック
        if parent:
            debug(f"🔧 🔧 🔧 新しい親ウィジェットの状態: visible={parent.isVisible()}, type={type(parent)}")
        
        # 強制的に表示状態を維持
        if not new_visible:
            debug(f"🔧 🔧 🔧 setParent後にvisible=Falseになったため強制表示")
            self.setVisible(True)
            self.show()
            debug(f"🔧 🔧 🔧 強制表示後: visible={self.isVisible()}")
        
        return parent
    
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
