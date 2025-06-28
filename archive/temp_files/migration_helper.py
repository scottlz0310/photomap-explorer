"""
Phase 4 移行ヘルパー

レガシーUIから新UIへの段階的移行をサポートするユーティリティです。
"""

from typing import Dict, List, Callable, Any, Optional
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget
import inspect


class MigrationHelper(QObject):
    """
    移行ヘルパークラス
    
    レガシーコンポーネントと新コンポーネントの段階的置き換えを管理します。
    """
    
    component_replaced = pyqtSignal(str, object, object)  # name, old_component, new_component
    migration_progress = pyqtSignal(int)  # progress percentage
    
    def __init__(self):
        super().__init__()
        self.component_registry = {}
        self.migration_plan = {}
        self.compatibility_map = {}
        self.replaced_components = {}
    
    def register_legacy_component(self, name: str, component: QWidget, 
                                  new_factory: Callable, 
                                  compatibility_wrapper: Optional[Callable] = None):
        """
        レガシーコンポーネントを登録
        
        Args:
            name: コンポーネント名
            component: レガシーコンポーネント
            new_factory: 新コンポーネントのファクトリ関数
            compatibility_wrapper: 互換性ラッパー関数
        """
        self.component_registry[name] = {
            'legacy': component,
            'new_factory': new_factory,
            'compatibility_wrapper': compatibility_wrapper,
            'replaced': False
        }
        print(f"📝 レガシーコンポーネント登録: {name}")
    
    def create_migration_plan(self, components: List[str]) -> Dict[str, int]:
        """
        移行プランを作成
        
        Args:
            components: 移行対象コンポーネントリスト
            
        Returns:
            移行優先度マップ
        """
        priority_map = {
            'address_bar': 1,      # 低リスク、高価値
            'folder_panel': 2,     # 中リスク、高価値
            'thumbnail_list': 3,   # 中リスク、中価値
            'preview_panel': 4,    # 中リスク、中価値
            'map_panel': 5,        # 高リスク、高価値
        }
        
        plan = {}
        for component in components:
            plan[component] = priority_map.get(component, 99)
        
        self.migration_plan = dict(sorted(plan.items(), key=lambda x: x[1]))
        print(f"📋 移行プラン作成: {list(self.migration_plan.keys())}")
        return self.migration_plan
    
    def replace_component(self, name: str, parent_container=None) -> bool:
        """
        コンポーネントを置き換え
        
        Args:
            name: コンポーネント名
            parent_container: 親コンテナ（レイアウト管理用）
            
        Returns:
            置き換え成功フラグ
        """
        if name not in self.component_registry:
            print(f"❌ 未登録コンポーネント: {name}")
            return False
        
        if self.component_registry[name]['replaced']:
            print(f"⚠️ 既に置き換え済み: {name}")
            return True
        
        try:
            # 新コンポーネント作成
            factory = self.component_registry[name]['new_factory']
            new_component = factory()
            
            # レガシーコンポーネント取得
            legacy_component = self.component_registry[name]['legacy']
            
            # 互換性ラッパー適用
            wrapper = self.component_registry[name]['compatibility_wrapper']
            if wrapper:
                new_component = wrapper(new_component, legacy_component)
            
            # 置き換え実行
            if parent_container:
                self._replace_in_container(legacy_component, new_component, parent_container)
            
            # 状態更新
            self.component_registry[name]['replaced'] = True
            self.replaced_components[name] = {
                'legacy': legacy_component,
                'new': new_component
            }
            
            # シグナル発火
            self.component_replaced.emit(name, legacy_component, new_component)
            self._update_migration_progress()
            
            print(f"✅ コンポーネント置き換え成功: {name}")
            return True
            
        except Exception as e:
            print(f"❌ コンポーネント置き換えエラー ({name}): {e}")
            return False
    
    def revert_component(self, name: str, parent_container=None) -> bool:
        """
        コンポーネントを元に戻す
        
        Args:
            name: コンポーネント名
            parent_container: 親コンテナ
            
        Returns:
            復元成功フラグ
        """
        if name not in self.replaced_components:
            print(f"⚠️ 置き換えられていないコンポーネント: {name}")
            return False
        
        try:
            replaced = self.replaced_components[name]
            legacy_component = replaced['legacy']
            new_component = replaced['new']
            
            # レガシーコンポーネントに戻す
            if parent_container:
                self._replace_in_container(new_component, legacy_component, parent_container)
            
            # 状態更新
            self.component_registry[name]['replaced'] = False
            del self.replaced_components[name]
            
            self._update_migration_progress()
            
            print(f"↩️ コンポーネント復元成功: {name}")
            return True
            
        except Exception as e:
            print(f"❌ コンポーネント復元エラー ({name}): {e}")
            return False
    
    def _replace_in_container(self, old_widget: QWidget, new_widget: QWidget, container):
        """コンテナ内でウィジェットを置き換え"""
        if hasattr(container, 'layout') and container.layout():
            layout = container.layout()
            
            # 古いウィジェットのインデックスを見つける
            for i in range(layout.count()):
                item = layout.itemAt(i)
                if item and item.widget() == old_widget:
                    # 置き換え実行
                    layout.removeWidget(old_widget)
                    layout.insertWidget(i, new_widget)
                    old_widget.hide()
                    new_widget.show()
                    break
    
    def _update_migration_progress(self):
        """移行進捗を更新"""
        total = len(self.component_registry)
        replaced = sum(1 for c in self.component_registry.values() if c['replaced'])
        progress = int((replaced / total) * 100) if total > 0 else 0
        self.migration_progress.emit(progress)
    
    def get_migration_status(self) -> Dict[str, Any]:
        """移行状況を取得"""
        status = {
            'total_components': len(self.component_registry),
            'replaced_components': len(self.replaced_components),
            'remaining_components': len(self.component_registry) - len(self.replaced_components),
            'progress_percentage': len(self.replaced_components) / len(self.component_registry) * 100 if self.component_registry else 0,
            'component_details': {}
        }
        
        for name, info in self.component_registry.items():
            status['component_details'][name] = {
                'replaced': info['replaced'],
                'has_wrapper': info['compatibility_wrapper'] is not None
            }
        
        return status
    
    def validate_compatibility(self, name: str) -> Dict[str, Any]:
        """
        コンポーネント互換性を検証
        
        Args:
            name: コンポーネント名
            
        Returns:
            互換性検証結果
        """
        if name not in self.component_registry:
            return {'valid': False, 'reason': 'Component not registered'}
        
        try:
            legacy = self.component_registry[name]['legacy']
            factory = self.component_registry[name]['new_factory']
            
            # 新コンポーネントを一時作成
            new_component = factory()
            
            # メソッド互換性チェック
            legacy_methods = [method for method in dir(legacy) 
                              if not method.startswith('_') and callable(getattr(legacy, method))]
            new_methods = [method for method in dir(new_component) 
                           if not method.startswith('_') and callable(getattr(new_component, method))]
            
            missing_methods = set(legacy_methods) - set(new_methods)
            extra_methods = set(new_methods) - set(legacy_methods)
            
            # シグナル互換性チェック
            legacy_signals = [attr for attr in dir(legacy) 
                              if hasattr(getattr(legacy, attr), 'emit')]
            new_signals = [attr for attr in dir(new_component) 
                           if hasattr(getattr(new_component, attr), 'emit')]
            
            missing_signals = set(legacy_signals) - set(new_signals)
            
            return {
                'valid': len(missing_methods) == 0 and len(missing_signals) == 0,
                'missing_methods': list(missing_methods),
                'extra_methods': list(extra_methods),
                'missing_signals': list(missing_signals),
                'compatibility_score': 1.0 - (len(missing_methods) + len(missing_signals)) / max(len(legacy_methods) + len(legacy_signals), 1)
            }
            
        except Exception as e:
            return {'valid': False, 'reason': f'Validation error: {e}'}


def create_compatibility_wrapper(legacy_interface: List[str]):
    """
    互換性ラッパーを生成
    
    Args:
        legacy_interface: レガシーインターフェースのメソッド/シグナルリスト
        
    Returns:
        ラッパー関数
    """
    def wrapper(new_component: QWidget, legacy_component: QWidget) -> QWidget:
        """互換性ラッパー"""
        
        # レガシーメソッドの委譲
        for method_name in legacy_interface:
            if hasattr(legacy_component, method_name) and not hasattr(new_component, method_name):
                legacy_method = getattr(legacy_component, method_name)
                setattr(new_component, method_name, legacy_method)
        
        return new_component
    
    return wrapper


class MigrationReporter:
    """移行レポート生成クラス"""
    
    @staticmethod
    def generate_report(helper: MigrationHelper) -> str:
        """移行レポートを生成"""
        status = helper.get_migration_status()
        
        report = []
        report.append("# Phase 4 移行レポート")
        report.append("")
        report.append(f"## 全体進捗")
        report.append(f"- 総コンポーネント数: {status['total_components']}")
        report.append(f"- 置き換え済み: {status['replaced_components']}")
        report.append(f"- 残り: {status['remaining_components']}")
        report.append(f"- 進捗率: {status['progress_percentage']:.1f}%")
        report.append("")
        
        report.append("## コンポーネント詳細")
        for name, details in status['component_details'].items():
            status_icon = "✅" if details['replaced'] else "⏳"
            wrapper_info = "🔧互換性ラッパー有り" if details['has_wrapper'] else ""
            report.append(f"- {status_icon} {name} {wrapper_info}")
        
        return "\n".join(report)
    
    @staticmethod
    def generate_compatibility_report(helper: MigrationHelper) -> str:
        """互換性レポートを生成"""
        report = []
        report.append("# 互換性検証レポート")
        report.append("")
        
        for name in helper.component_registry.keys():
            validation = helper.validate_compatibility(name)
            
            report.append(f"## {name}")
            report.append(f"- 互換性: {'✅' if validation['valid'] else '❌'}")
            
            if 'compatibility_score' in validation:
                report.append(f"- 互換性スコア: {validation['compatibility_score']:.2f}")
            
            if validation.get('missing_methods'):
                report.append(f"- 不足メソッド: {', '.join(validation['missing_methods'])}")
            
            if validation.get('missing_signals'):
                report.append(f"- 不足シグナル: {', '.join(validation['missing_signals'])}")
            
            report.append("")
        
        return "\n".join(report)


# ファクトリ関数とラッパーの定義
def create_address_bar_migration():
    """アドレスバー移行設定"""
    from presentation.views.controls.address_bar import create_address_bar_widget
    
    def factory():
        widget, edit = create_address_bar_widget("", None, None)
        return widget
    
    return factory


def create_folder_panel_migration():
    """フォルダパネル移行設定"""
    from presentation.views.panels.folder_panel import create_folder_panel
    return create_folder_panel


def create_thumbnail_list_migration():
    """サムネイルリスト移行設定"""
    from presentation.views.controls.thumbnail_list import create_thumbnail_list
    
    def factory():
        return create_thumbnail_list(None, None)
    
    return factory


def create_preview_panel_migration():
    """プレビューパネル移行設定"""
    from presentation.views.panels.preview_panel import create_preview_panel
    return create_preview_panel


def create_map_panel_migration():
    """マップパネル移行設定"""
    from presentation.views.panels.map_panel import create_map_panel
    return create_map_panel


# 使用例のための設定関数
def setup_migration_helper(legacy_window) -> MigrationHelper:
    """
    移行ヘルパーのセットアップ例
    
    Args:
        legacy_window: レガシーメインウィンドウ
        
    Returns:
        設定済み移行ヘルパー
    """
    helper = MigrationHelper()
    
    # レガシーコンポーネントと新ファクトリの登録
    if hasattr(legacy_window, 'address_bar_widget'):
        helper.register_legacy_component(
            'address_bar',
            legacy_window.address_bar_widget,
            create_address_bar_migration()
        )
    
    if hasattr(legacy_window, 'folder_panel'):
        helper.register_legacy_component(
            'folder_panel',
            legacy_window.folder_panel,
            create_folder_panel_migration()
        )
    
    if hasattr(legacy_window, 'thumbnail_panel'):
        wrapper = create_compatibility_wrapper(['on_thumbnail_clicked', 'set_thumbnail_size_and_width'])
        helper.register_legacy_component(
            'thumbnail_panel',
            legacy_window.thumbnail_panel,
            create_thumbnail_list_migration(),
            wrapper
        )
    
    if hasattr(legacy_window, 'preview_panel'):
        helper.register_legacy_component(
            'preview_panel',
            legacy_window.preview_panel,
            create_preview_panel_migration()
        )
    
    if hasattr(legacy_window, 'map_panel'):
        helper.register_legacy_component(
            'map_panel',
            legacy_window.map_panel,
            create_map_panel_migration()
        )
    
    # 移行プラン作成
    components = list(helper.component_registry.keys())
    helper.create_migration_plan(components)
    
    return helper
