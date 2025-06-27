"""
最適化された新UIメインビュー

パフォーマンス最適化された Clean Architecture UI実装
- 遅延初期化
- 非同期処理
- 軽量レンダリング
"""

import os
import asyncio
from typing import Optional
from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QSplitter, QWidget, 
                            QStatusBar, QHBoxLayout, QPushButton, QLabel,
                            QProgressBar, QApplication)
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from PyQt5.QtGui import QIcon

# プロファイラー導入
from utils.profiler import profile_function, ui_profiler


class LazyWidget(QWidget):
    """遅延初期化ウィジェット"""
    
    def __init__(self, widget_factory, *args, **kwargs):
        super().__init__()
        self.widget_factory = widget_factory
        self.factory_args = args
        self.factory_kwargs = kwargs
        self.actual_widget = None
        self.is_initialized = False
        
    def initialize(self):
        """実際のウィジェットを初期化"""
        if not self.is_initialized:
            self.actual_widget = self.widget_factory(*self.factory_args, **self.factory_kwargs)
            layout = QVBoxLayout(self)
            layout.addWidget(self.actual_widget)
            self.is_initialized = True
    
    def showEvent(self, event):
        """表示時に初期化"""
        if not self.is_initialized:
            self.initialize()
        super().showEvent(event)


class AsyncUILoader(QObject):
    """非同期UI読み込み"""
    
    component_loaded = pyqtSignal(str, object)
    loading_progress = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.loaded_components = {}
    
    def load_component_async(self, name: str, factory, *args, **kwargs):
        """コンポーネントを非同期で読み込み"""
        QTimer.singleShot(10, lambda: self._load_component(name, factory, *args, **kwargs))
    
    def _load_component(self, name: str, factory, *args, **kwargs):
        """コンポーネント読み込み実行"""
        try:
            component = factory(*args, **kwargs)
            self.loaded_components[name] = component
            self.component_loaded.emit(name, component)
        except Exception as e:
            print(f"❌ コンポーネント読み込みエラー ({name}): {e}")


class OptimizedMainWindow(QMainWindow):
    """
    最適化されたメインウィンドウ
    
    パフォーマンス最適化技術:
    - 遅延初期化 (Lazy Loading)
    - 非同期UI構築
    - 軽量レンダリング
    - プログレッシブローディング
    """
    
    def __init__(self):
        super().__init__()
        
        # 基本設定（軽量）
        self._setup_basic_properties()
        
        # 非同期ローダー
        self.async_loader = AsyncUILoader()
        self.async_loader.component_loaded.connect(self._on_component_loaded)
        
        # 遅延初期化用コンテナ
        self.lazy_components = {}
        self.initialization_queue = []
        
        # 基本UIを即座に構築（最小限）
        self._setup_minimal_ui()
        
        # 残りのUIを非同期で構築
        self._schedule_async_initialization()
        
        # ステータス表示
        self.show_status_message("[新UI] 最適化されたUI (Clean Architecture) で起動しました")
    
    # @profile_function
    def _setup_basic_properties(self):
        """基本プロパティ設定（高速）"""
        self.setWindowTitle("PhotoMap Explorer - 最適化新UI")
        self.setGeometry(100, 100, 1400, 900)
        
        # アイコン設定（キャッシュ済みの場合のみ）
        self._setup_icon_fast()
    
    def _setup_icon_fast(self):
        """高速アイコン設定"""
        # アイコンパスをキャッシュして高速化
        if not hasattr(self.__class__, '_cached_icon_path'):
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "pme_icon.png")
            if os.path.exists(icon_path):
                self.__class__._cached_icon_path = icon_path
            else:
                self.__class__._cached_icon_path = None
        
        if self.__class__._cached_icon_path:
            self.setWindowIcon(QIcon(self.__class__._cached_icon_path))
    
    # @profile_function
    def _setup_minimal_ui(self):
        """最小限のUI構築（即座に表示）"""
        # 中央ウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # ローディング表示
        self.loading_widget = self._create_loading_widget()
        self.main_layout.addWidget(self.loading_widget)
        
        # ステータスバー（軽量）
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # プログレスバー
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def _create_loading_widget(self) -> QWidget:
        """ローディングウィジェット作成"""
        loading_widget = QWidget()
        layout = QVBoxLayout(loading_widget)
        
        loading_label = QLabel("🚀 PhotoMap Explorer 読み込み中...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("font-size: 18px; padding: 20px;")
        
        layout.addWidget(loading_label)
        return loading_widget
    
    def _schedule_async_initialization(self):
        """非同期初期化をスケジュール"""
        # 初期化タスクを段階的に実行
        self.initialization_queue = [
            ("folder_panel", self._create_folder_panel_lazy),
            ("thumbnail_panel", self._create_thumbnail_panel_lazy),
            ("preview_panel", self._create_preview_panel_lazy),
            ("map_panel", self._create_map_panel_lazy),
        ]
        
        # 最初のタスクを開始
        QTimer.singleShot(50, self._process_next_initialization)
    
    def _process_next_initialization(self):
        """次の初期化タスクを処理"""
        if self.initialization_queue:
            name, factory = self.initialization_queue.pop(0)
            self.async_loader.load_component_async(name, factory)
            
            # プログレスバー更新
            total_tasks = 4
            completed_tasks = total_tasks - len(self.initialization_queue)
            progress = int((completed_tasks / total_tasks) * 100)
            
            if not self.progress_bar.isVisible():
                self.progress_bar.setVisible(True)
            self.progress_bar.setValue(progress)
            
            # 次のタスクをスケジュール
            if self.initialization_queue:
                QTimer.singleShot(30, self._process_next_initialization)
            else:
                # 全て完了
                QTimer.singleShot(100, self._finalize_ui)
    
    def _on_component_loaded(self, name: str, component: QWidget):
        """コンポーネント読み込み完了"""
        self.lazy_components[name] = component
        print(f"✅ コンポーネント読み込み完了: {name}")
    
    def _finalize_ui(self):
        """UI構築完了処理"""
        # ローディング画面を削除
        self.main_layout.removeWidget(self.loading_widget)
        self.loading_widget.deleteLater()
        
        # 実際のUIを構築
        self._build_main_ui()
        
        # プログレスバーを非表示
        self.progress_bar.setVisible(False)
        
        self.show_status_message("[新UI] UI読み込み完了 - 最適化されたClean Architecture")
    
    # @profile_function
    def _build_main_ui(self):
        """メインUI構築"""
        # メインスプリッター
        main_splitter = QSplitter(Qt.Horizontal)
        self.main_layout.addWidget(main_splitter)
        
        # 左側: フォルダパネル（読み込み済みコンポーネントを使用）
        if "folder_panel" in self.lazy_components:
            main_splitter.addWidget(self.lazy_components["folder_panel"])
        
        # 右側スプリッター
        right_splitter = QSplitter(Qt.Vertical)
        main_splitter.addWidget(right_splitter)
        
        # 上部: サムネイル・プレビュー
        top_splitter = QSplitter(Qt.Horizontal)
        right_splitter.addWidget(top_splitter)
        
        if "thumbnail_panel" in self.lazy_components:
            top_splitter.addWidget(self.lazy_components["thumbnail_panel"])
        
        if "preview_panel" in self.lazy_components:
            top_splitter.addWidget(self.lazy_components["preview_panel"])
        
        # 下部: マップ
        if "map_panel" in self.lazy_components:
            right_splitter.addWidget(self.lazy_components["map_panel"])
        
        # スプリッター比率設定
        main_splitter.setSizes([300, 1100])
        right_splitter.setSizes([400, 300])
        top_splitter.setSizes([400, 600])
    
    def _create_folder_panel_lazy(self) -> QWidget:
        """フォルダパネル遅延作成"""
        folder_panel = QWidget()
        layout = QVBoxLayout(folder_panel)
        
        header = QLabel("📁 フォルダ")
        header.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(header)
        
        content = QLabel("フォルダブラウザ\n(遅延読み込み完了)")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("border: 1px solid #ccc; padding: 20px;")
        layout.addWidget(content)
        
        return folder_panel
    
    def _create_thumbnail_panel_lazy(self) -> QWidget:
        """サムネイルパネル遅延作成"""
        thumbnail_panel = QWidget()
        layout = QVBoxLayout(thumbnail_panel)
        
        header = QLabel("🖼️ サムネイル")
        header.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(header)
        
        content = QLabel("サムネイル表示\n(遅延読み込み完了)")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("border: 1px solid #ccc; padding: 20px;")
        layout.addWidget(content)
        
        return thumbnail_panel
    
    def _create_preview_panel_lazy(self) -> QWidget:
        """プレビューパネル遅延作成"""
        preview_panel = QWidget()
        layout = QVBoxLayout(preview_panel)
        
        header = QLabel("👁️ プレビュー")
        header.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(header)
        
        content = QLabel("画像プレビュー\n(遅延読み込み完了)")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("border: 1px solid #ccc; padding: 20px;")
        layout.addWidget(content)
        
        return preview_panel
    
    def _create_map_panel_lazy(self) -> QWidget:
        """マップパネル遅延作成"""
        map_panel = QWidget()
        layout = QVBoxLayout(map_panel)
        
        header = QLabel("🗺️ マップ")
        header.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0;")
        layout.addWidget(header)
        
        content = QLabel("地図表示\n(遅延読み込み完了)")
        content.setAlignment(Qt.AlignCenter)
        content.setStyleSheet("border: 1px solid #ccc; padding: 20px;")
        layout.addWidget(content)
        
        return map_panel
    
    def show_status_message(self, message: str, timeout: int = 0):
        """ステータスメッセージ表示"""
        self.status_bar.showMessage(message, timeout)
        print(message)
    
    def show_folder_selection_dialog(self):
        """フォルダ選択ダイアログ表示"""
        self.show_status_message("[新UI] フォルダ選択: ")
    
    def closeEvent(self, event):
        """ウィンドウクローズ時の処理"""
        # リソースクリーンアップ
        for component in self.lazy_components.values():
            if hasattr(component, 'cleanup'):
                component.cleanup()
        
        event.accept()


# エイリアス（後方互換性）
SimpleNewMainWindow = OptimizedMainWindow
