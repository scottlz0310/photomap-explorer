"""
ブレッドクラムナビゲーション管理モジュール

このモジュールは ui/controls.py から分離された
パス要素の管理とナビゲーション機能を提供します。
"""

from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QFont
import os
import logging
from typing import List, Optional


class BreadcrumbManager(QObject):
    """
    ブレッドクラムナビゲーション管理クラス
    
    パス要素の分解・分析・優先度管理を担当
    アドレスバーコアと連携してナビゲーション機能を提供
    """
    
    # シグナル
    navigation_requested = pyqtSignal(str)  # ナビゲーション要求
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_path = ""
        
    def analyze_path(self, path: str) -> List[dict]:
        """
        パスを分析してブレッドクラム要素リストを作成
        
        Args:
            path: 分析対象パス
            
        Returns:
            ブレッドクラム要素リスト
            各要素は {'text': str, 'path': str, 'priority': int} の辞書
        """
        try:
            if not path:
                return self._get_empty_path_elements()
            
            elements = []
            path_parts = self._split_path_safely(path)
            
            accumulated_path = ""
            
            for i, part in enumerate(path_parts):
                if not part and i != 0:  # 空要素をスキップ（ルート以外）
                    continue
                
                # パス構築
                accumulated_path = self._build_accumulated_path(accumulated_path, part, i)
                
                # 要素作成
                element = {
                    'text': part if part else '/',
                    'path': accumulated_path,
                    'priority': len(path_parts) - i,  # 末尾ほど高優先度
                    'is_current': i == len(path_parts) - 1
                }
                
                elements.append(element)
            
            return elements
            
        except Exception as e:
            logging.error(f"パス分析エラー: {e}")
            return []
    
    def _get_empty_path_elements(self) -> List[dict]:
        """空パス時の要素取得（ドライブ一覧など）"""
        try:
            elements = []
            
            if os.name == 'nt':  # Windows
                elements.extend(self._get_drive_elements())
            else:  # Unix系
                elements.append({
                    'text': 'ルート',
                    'path': '/',
                    'priority': 1,
                    'is_current': True
                })
            
            return elements
            
        except Exception as e:
            logging.error(f"空パス要素取得エラー: {e}")
            return []
    
    def _get_drive_elements(self) -> List[dict]:
        """Windowsドライブ要素を取得"""
        try:
            import string
            from pathlib import Path
from utils.debug_logger import debug, info, warning, error, verbose
            
            elements = []
            
            for drive in string.ascii_uppercase:
                drive_path = f"{drive}:\\\\"
                if Path(drive_path).exists():
                    elements.append({
                        'text': f"{drive}:",
                        'path': drive_path,
                        'priority': 1,
                        'is_current': False
                    })
            
            return elements
            
        except Exception as e:
            logging.error(f"ドライブ要素取得エラー: {e}")
            return []
    
    def _split_path_safely(self, path: str) -> List[str]:
        """パスを安全に分割"""
        try:
            parts = []
            
            # パスを正規化
            normalized = os.path.normpath(path)
            
            if os.name == 'nt':  # Windows
                parts = self._split_windows_path(normalized)
            else:  # Unix系
                parts = self._split_unix_path(normalized)
            
            return parts
            
        except Exception as e:
            logging.error(f"パス分割エラー: {e}")
            return []
    
    def _split_windows_path(self, path: str) -> List[str]:
        """Windowsパスを分割"""
        try:
            parts = []
            
            # ドライブ部分の処理
            if ':' in path:
                drive, rest = path.split(':', 1)
                parts.append(drive + ':')
                
                # 残りの部分を処理
                if rest and rest.strip('\\\\'):
                    folders = rest.strip('\\\\').split('\\\\')
                    parts.extend([folder for folder in folders if folder])
            else:
                # ドライブレター無しの場合
                path_parts = path.strip('\\\\').split('\\\\')
                parts = [part for part in path_parts if part]
            
            return parts
            
        except Exception as e:
            logging.error(f"Windowsパス分割エラー: {e}")
            return []
    
    def _split_unix_path(self, path: str) -> List[str]:
        """Unixパスを分割"""
        try:
            parts = path.strip('/').split('/')
            
            # ルートから始まる場合
            if path.startswith('/'):
                parts.insert(0, '/')
            
            # 空要素を除去
            parts = [part for part in parts if part or part == '/']
            
            return parts
            
        except Exception as e:
            logging.error(f"Unixパス分割エラー: {e}")
            return []
    
    def _build_accumulated_path(self, current: str, part: str, index: int) -> str:
        """累積パスを構築"""
        try:
            if os.name == 'nt':  # Windows
                if index == 0:
                    # ドライブ部分
                    if part.endswith(':'):
                        return part + '\\\\'
                    else:
                        return part
                else:
                    return os.path.join(current, part)
            else:  # Unix系
                if part == '/':
                    return '/'
                elif not current or current == '/':
                    return '/' + part
                else:
                    return os.path.join(current, part)
                    
        except Exception as e:
            logging.error(f"累積パス構築エラー: {e}")
            return current
    
    def calculate_optimal_display(self, elements: List[dict], available_width: int) -> List[dict]:
        """
        利用可能幅に基づいて最適な表示要素を計算
        
        Args:
            elements: ブレッドクラム要素リスト
            available_width: 利用可能幅（ピクセル）
            
        Returns:
            表示すべき要素リスト（省略記号情報を含む）
        """
        try:
            if not elements:
                return []
            
            # 各要素の推定幅を計算
            element_widths = [self._estimate_element_width(elem) for elem in elements]
            total_width = sum(element_widths)
            
            # 全て表示できる場合
            if total_width <= available_width:
                return elements
            
            # 省略が必要な場合
            return self._calculate_with_ellipsis(elements, element_widths, available_width)
            
        except Exception as e:
            logging.error(f"最適表示計算エラー: {e}")
            return elements
    
    def _estimate_element_width(self, element: dict) -> int:
        """要素の推定表示幅を計算"""
        try:
            text = element.get('text', '')
            
            # 基本的な文字幅計算
            char_width = 8  # 平均文字幅
            padding = 16    # ボタンパディング
            margin = 2      # マージン
            
            width = len(text) * char_width + padding + margin
            
            # 最小/最大幅制限
            width = max(30, min(width, 200))
            
            return width
            
        except Exception as e:
            logging.error(f"要素幅推定エラー: {e}")
            return 50
    
    def _calculate_with_ellipsis(self, elements: List[dict], widths: List[int], available_width: int) -> List[dict]:
        """省略記号を考慮した表示要素を計算"""
        try:
            ellipsis_width = 30
            result_elements = []
            used_width = 0
            
            # 高優先度順（通常は末尾から）でソート
            sorted_elements = sorted(
                zip(elements, widths), 
                key=lambda x: x[0].get('priority', 0), 
                reverse=True
            )
            
            # 優先度順に追加
            for element, width in sorted_elements:
                needed_width = used_width + width
                
                # 省略記号が必要かチェック
                if len(result_elements) > 0 and len(result_elements) < len(elements):
                    needed_width += ellipsis_width
                
                if needed_width <= available_width:
                    result_elements.append(element)
                    used_width += width
                else:
                    break
            
            # 元の順序に復元
            result_elements.sort(key=lambda x: elements.index(x))
            
            # 省略記号情報を追加
            if len(result_elements) < len(elements):
                # 省略された要素があることを示す
                ellipsis_element = {
                    'text': '...',
                    'path': '',
                    'priority': 0,
                    'is_ellipsis': True,
                    'ellipsis_count': len(elements) - len(result_elements)
                }
                
                # 適切な位置に挿入
                insert_index = self._find_ellipsis_position(elements, result_elements)
                result_elements.insert(insert_index, ellipsis_element)
            
            return result_elements
            
        except Exception as e:
            logging.error(f"省略記号計算エラー: {e}")
            return elements[:3]  # フォールバック
    
    def _find_ellipsis_position(self, original_elements: List[dict], visible_elements: List[dict]) -> int:
        """省略記号の挿入位置を決定"""
        try:
            if not visible_elements:
                return 0
            
            # 最初の表示要素の前に省略があるかチェック
            first_visible_index = original_elements.index(visible_elements[0])
            if first_visible_index > 0:
                return 0  # 先頭に省略記号
            
            # 末尾の可能性をチェック
            last_visible_index = original_elements.index(visible_elements[-1])
            if last_visible_index < len(original_elements) - 1:
                return len(visible_elements)  # 末尾に省略記号
            
            # 中間の場合（連続していない場合）
            for i in range(len(visible_elements) - 1):
                current_index = original_elements.index(visible_elements[i])
                next_index = original_elements.index(visible_elements[i + 1])
                
                if next_index - current_index > 1:
                    return i + 1  # 中間に省略記号
            
            return len(visible_elements) // 2  # デフォルト位置
            
        except Exception as e:
            logging.error(f"省略記号位置決定エラー: {e}")
            return 0
    
    def create_navigation_button(self, element: dict) -> Optional[QPushButton]:
        """
        ブレッドクラム要素からナビゲーションボタンを作成
        
        Args:
            element: ブレッドクラム要素辞書
            
        Returns:
            作成されたボタン（省略記号の場合はNone）
        """
        try:
            # 省略記号要素の場合はボタンを作らない
            if element.get('is_ellipsis', False):
                return self._create_ellipsis_button(element)
            
            text = element.get('text', '')
            path = element.get('path', '')
            is_current = element.get('is_current', False)
            
            button = QPushButton(text)
            button.setProperty('breadcrumb_path', path)
            
            # スタイル設定
            self._apply_button_style(button, is_current)
            
            # クリックイベント接続
            button.clicked.connect(lambda checked, p=path: self._on_navigation_clicked(p))
            
            return button
            
        except Exception as e:
            logging.error(f"ナビゲーションボタン作成エラー: {e}")
            return None
    
    def _create_ellipsis_button(self, element: dict) -> QPushButton:
        """省略記号ボタンを作成"""
        try:
            ellipsis_count = element.get('ellipsis_count', 0)
            
            button = QPushButton("...")
            button.setFixedSize(30, 30)
            button.setToolTip(f"{ellipsis_count}個のパス要素が省略されています")
            button.setEnabled(False)  # クリック無効
            
            # 省略記号用スタイル
            button.setStyleSheet("""
                QPushButton {
                    background-color: #f8f8f8;
                    border: 1px solid #e0e0e0;
                    border-radius: 3px;
                    color: #888;
                    font-weight: normal;
                }
            """)
            
            return button
            
        except Exception as e:
            logging.error(f"省略記号ボタン作成エラー: {e}")
            return QPushButton("...")
    
    def _apply_button_style(self, button: QPushButton, is_current: bool):
        """ボタンにスタイルを適用"""
        try:
            # フォント設定
            font = QFont()
            font.setPointSize(10)
            font.setWeight(QFont.Medium if is_current else QFont.Normal)
            button.setFont(font)
            
            # スタイルシート
            if is_current:
                style = self._get_current_button_style()
            else:
                style = self._get_normal_button_style()
            
            button.setStyleSheet(style)
            
        except Exception as e:
            logging.error(f"ボタンスタイル適用エラー: {e}")
    
    def _get_normal_button_style(self) -> str:
        """通常ボタンのスタイル"""
        return """
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #d0d0d0;
                border-radius: 3px;
                padding: 4px 12px;
                margin: 1px;
                font-weight: normal;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-color: #b0b0b0;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
            }
        """
    
    def _get_current_button_style(self) -> str:
        """カレントボタンのスタイル"""
        return """
            QPushButton {
                background-color: #e8f4fd;
                border: 1px solid #1ba0e2;
                border-radius: 3px;
                padding: 4px 12px;
                margin: 1px;
                font-weight: 500;
                color: #1ba0e2;
            }
            QPushButton:hover {
                background-color: #d1ebfc;
                border-color: #0e90d2;
            }
            QPushButton:pressed {
                background-color: #b8ddf8;
            }
        """
    
    def _on_navigation_clicked(self, path: str):
        """ナビゲーションクリック時の処理"""
        try:
            if path:
                self.current_path = path
                self.navigation_requested.emit(path)
                
        except Exception as e:
            logging.error(f"ナビゲーションクリック処理エラー: {e}")
    
    def get_parent_path(self, path: str) -> Optional[str]:
        """親パスを取得"""
        try:
            if not path:
                return None
            
            parent = os.path.dirname(path)
            
            # ルートパスの場合は親なし
            if parent == path:
                return None
            
            return parent if parent else None
            
        except Exception as e:
            logging.error(f"親パス取得エラー: {e}")
            return None
    
    def validate_path(self, path: str) -> bool:
        """パスの妥当性を検証"""
        try:
            if not path:
                return False
            
            # パスの存在確認
            return os.path.exists(path)
            
        except Exception as e:
            logging.error(f"パス検証エラー: {e}")
            return False
