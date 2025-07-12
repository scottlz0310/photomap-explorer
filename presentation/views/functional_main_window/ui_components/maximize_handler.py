"""
最大化・復元機能を担当するハンドラ

このモジュールは functional_new_main_view.py から分離された
画像・マップの最大化表示機能を担当します。
"""

import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton


class MaximizeHandler:
    """最大化・復元機能を担当するハンドラ"""
    
    def __init__(self, main_window):
        """
        最大化ハンドラを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.maximized_state = None  # 'image', 'map', None
        
        # コンポーネント参照
        self.main_splitter = None
        self.preview_panel = None
        self.map_panel = None
        self.maximize_container = None
        self.maximized_content_area = None
        self.maximized_content_layout = None
        self.restore_btn = None
        
        # 元の親保存用
        self.original_preview_parent = None
        self.original_map_parent = None
        
    def set_components(self, main_splitter, preview_panel, map_panel):
        """コンポーネントの参照を設定"""
        self.main_splitter = main_splitter
        self.preview_panel = preview_panel
        self.map_panel = map_panel
    
    def create_maximize_container(self):
        """最大化表示用のコンテナ作成"""
        try:
            self.maximize_container = QWidget()
            maximize_layout = QVBoxLayout(self.maximize_container)
            
            # 最大化時のトップバー
            topbar = QHBoxLayout()
            
            # 復元ボタン（サイズを大きくしてフォントが潰れないようにする）
            self.restore_btn = QPushButton("◱ 通常表示に戻る")
            self.restore_btn.setToolTip("通常表示に戻る")
            self.restore_btn.setMinimumSize(120, 35)  # 最小サイズを指定
            self.restore_btn.setMaximumHeight(35)
            self.restore_btn.clicked.connect(self.restore_normal_view)
            
            topbar.addStretch()
            topbar.addWidget(self.restore_btn)
            
            topbar_widget = QWidget()
            topbar_widget.setLayout(topbar)
            topbar_widget.setMaximumHeight(40)  # 高さを少し増やす
            
            maximize_layout.addWidget(topbar_widget)
            
            # 最大化されたコンテンツエリア
            self.maximized_content_area = QWidget()
            self.maximized_content_layout = QVBoxLayout(self.maximized_content_area)
            maximize_layout.addWidget(self.maximized_content_area)
            
            # テーマコンポーネント登録（メインウィンドウにメソッドがあれば）
            if hasattr(self.main_window, 'register_theme_component'):
                self.main_window.register_theme_component(self.restore_btn, "button")
                self.main_window.register_theme_component(self.maximize_container, "panel")
                self.main_window.register_theme_component(topbar_widget, "panel")
                self.main_window.register_theme_component(self.maximized_content_area, "panel")
            
            # 初期状態では非表示
            self.maximize_container.hide()
            
            return self.maximize_container
            
        except Exception as e:
            logging.error(f"最大化コンテナ作成エラー: {e}")
            return None
    
    def toggle_image_maximize(self):
        """画像最大化の切り替え"""
        try:
            if self.maximized_state == 'image':
                self.restore_normal_view()
            else:
                self.maximize_preview()
                
        except Exception as e:
            logging.error(f"画像最大化切り替えエラー: {e}")
            self.main_window.show_status_message(f"❌ 画像最大化エラー: {e}")
    
    def toggle_map_maximize(self):
        """マップ最大化の切り替え"""
        try:
            if self.maximized_state == 'map':
                self.restore_normal_view()
            else:
                self.maximize_map()
                
        except Exception as e:
            logging.error(f"マップ最大化切り替えエラー: {e}")
            self.main_window.show_status_message(f"❌ マップ最大化エラー: {e}")
    
    def maximize_preview(self):
        """プレビューを最大化"""
        try:
            if not self.preview_panel:
                self.main_window.show_status_message("❌ プレビューパネルが利用できません")
                return
            
            # 現在の親を記録
            self.original_preview_parent = self.preview_panel.parent()
            
            # プレビューパネルを最大化エリアに移動
            self.preview_panel.setParent(None)
            if self.maximized_content_layout:
                self.maximized_content_layout.addWidget(self.preview_panel)
            
            # UIの切り替え
            if self.main_splitter:
                self.main_splitter.hide()
            if self.maximize_container:
                self.maximize_container.show()
            
            self.maximized_state = 'image'
            
            # 最大化状態での画像表示更新
            self.refresh_maximized_content()
            
            self.main_window.show_status_message("🖼️ 画像を最大化表示")
            
        except Exception as e:
            logging.error(f"プレビュー最大化エラー: {e}")
            self.main_window.show_status_message(f"❌ プレビュー最大化エラー: {e}")
    
    def maximize_map(self):
        """マップを最大化"""
        try:
            if not self.map_panel:
                self.main_window.show_status_message("❌ マップパネルが利用できません")
                return
            
            # 現在の親を記録
            self.original_map_parent = self.map_panel.parent()
            
            # マップパネルを最大化エリアに移動
            self.map_panel.setParent(None)
            if self.maximized_content_layout:
                self.maximized_content_layout.addWidget(self.map_panel)
            
            # UIの切り替え
            if self.main_splitter:
                self.main_splitter.hide()
            if self.maximize_container:
                self.maximize_container.show()
            
            self.maximized_state = 'map'
            
            # 最大化状態での表示更新
            self.refresh_maximized_content()
            
            self.main_window.show_status_message("🗺️ マップを最大化表示")
            
        except Exception as e:
            logging.error(f"マップ最大化エラー: {e}")
            self.main_window.show_status_message(f"❌ マップ最大化エラー: {e}")
    
    def restore_normal_view(self):
        """通常表示に復元"""
        try:
            if self.maximized_state == 'image' and self.preview_panel:
                # プレビューパネルを元の場所に戻す
                if self.maximized_content_layout:
                    self.maximized_content_layout.removeWidget(self.preview_panel)
                if self.original_preview_parent and hasattr(self.original_preview_parent, 'layout'):
                    parent_layout = self.original_preview_parent.layout()
                    if parent_layout:
                        parent_layout.addWidget(self.preview_panel)
                
            elif self.maximized_state == 'map' and self.map_panel:
                # マップパネルを元の場所に戻す
                if self.maximized_content_layout:
                    self.maximized_content_layout.removeWidget(self.map_panel)
                if self.original_map_parent and hasattr(self.original_map_parent, 'layout'):
                    parent_layout = self.original_map_parent.layout()
                    if parent_layout:
                        parent_layout.addWidget(self.map_panel)
            
            # UIの切り替え
            if self.maximize_container:
                self.maximize_container.hide()
            if self.main_splitter:
                self.main_splitter.show()
            
            previous_state = self.maximized_state
            self.maximized_state = None
            
            # 通常表示での内容更新
            self.refresh_normal_content()
            
            if previous_state == 'image':
                self.main_window.show_status_message("🖼️ 通常表示に復元")
            elif previous_state == 'map':
                self.main_window.show_status_message("🗺️ 通常表示に復元")
            
        except Exception as e:
            logging.error(f"通常表示復元エラー: {e}")
            self.main_window.show_status_message(f"❌ 復元エラー: {e}")
    
    def refresh_maximized_content(self):
        """最大化状態でのコンテンツ更新"""
        try:
            selected_image = getattr(self.main_window, 'selected_image', None)
            
            if selected_image:
                if self.maximized_state == 'image':
                    # 画像表示の更新
                    if hasattr(self.main_window, 'update_preview_display'):
                        self.main_window.update_preview_display(selected_image)
                    elif hasattr(self.main_window, '_update_preview_display'):
                        self.main_window._update_preview_display(selected_image)
                        
                elif self.maximized_state == 'map':
                    # マップ表示の更新
                    if hasattr(self.main_window, 'update_map_display'):
                        self.main_window.update_map_display(selected_image)
                    elif hasattr(self.main_window, '_update_map_display'):
                        self.main_window._update_map_display(selected_image)
                        
        except Exception as e:
            logging.error(f"最大化コンテンツ更新エラー: {e}")
    
    def refresh_normal_content(self):
        """通常表示でのコンテンツ更新"""
        try:
            selected_image = getattr(self.main_window, 'selected_image', None)
            
            if selected_image:
                # 画像表示の更新
                if hasattr(self.main_window, 'update_preview_display'):
                    self.main_window.update_preview_display(selected_image)
                elif hasattr(self.main_window, '_update_preview_display'):
                    self.main_window._update_preview_display(selected_image)
                
                # マップ表示の更新
                if hasattr(self.main_window, 'update_map_display'):
                    self.main_window.update_map_display(selected_image)
                elif hasattr(self.main_window, '_update_map_display'):
                    self.main_window._update_map_display(selected_image)
                    
        except Exception as e:
            logging.error(f"通常コンテンツ更新エラー: {e}")
    
    def on_preview_double_click(self, event):
        """プレビューエリアのダブルクリックイベント"""
        try:
            self.toggle_image_maximize()
        except Exception as e:
            logging.error(f"プレビューダブルクリックエラー: {e}")
    
    def on_map_double_click(self, event):
        """マップエリアのダブルクリックイベント"""
        try:
            self.toggle_map_maximize()
        except Exception as e:
            logging.error(f"マップダブルクリックエラー: {e}")
    
    def is_maximized(self):
        """最大化状態かどうかを確認"""
        return self.maximized_state is not None
    
    def get_maximized_state(self):
        """現在の最大化状態を取得"""
        return self.maximized_state
    
    def force_restore(self):
        """強制的に通常表示に復元"""
        try:
            if self.is_maximized():
                self.restore_normal_view()
                
        except Exception as e:
            logging.error(f"強制復元エラー: {e}")
    
    def update_maximize_buttons(self):
        """最大化ボタンの状態を更新"""
        try:
            # 画像最大化ボタン
            if hasattr(self.main_window, 'maximize_image_btn'):
                btn = self.main_window.maximize_image_btn
                if self.maximized_state == 'image':
                    btn.setText("◱")
                    btn.setToolTip("通常表示に戻る")
                else:
                    btn.setText("⛶")
                    btn.setToolTip("画像を最大化表示（ダブルクリックでも可能）")
            
            # マップ最大化ボタン
            if hasattr(self.main_window, 'maximize_map_btn'):
                btn = self.main_window.maximize_map_btn
                if self.maximized_state == 'map':
                    btn.setText("◱")
                    btn.setToolTip("通常表示に戻る")
                else:
                    btn.setText("⛶")
                    btn.setToolTip("マップを最大化表示（ダブルクリックでも可能）")
                    
        except Exception as e:
            logging.error(f"最大化ボタン更新エラー: {e}")
    
    def apply_theme(self, theme_name):
        """最大化コンテナにテーマを適用"""
        try:
            if not self.maximize_container:
                return
            
            # テーマに応じたスタイル適用
            if theme_name == "dark":
                style = """
                    QWidget {
                        background-color: #2d2d2d;
                        color: #ffffff;
                    }
                    QPushButton {
                        background-color: #4d4d4d;
                        color: #ffffff;
                        border: 1px solid #666666;
                        border-radius: 4px;
                        padding: 8px;
                    }
                    QPushButton:hover {
                        background-color: #5d5d5d;
                        border-color: #007ACC;
                    }
                """
            else:
                style = """
                    QWidget {
                        background-color: #ffffff;
                        color: #000000;
                    }
                    QPushButton {
                        background-color: #f0f0f0;
                        color: #000000;
                        border: 1px solid #cccccc;
                        border-radius: 4px;
                        padding: 8px;
                    }
                    QPushButton:hover {
                        background-color: #e0e0e0;
                        border-color: #007ACC;
                    }
                """
            
            self.maximize_container.setStyleSheet(style)
            
        except Exception as e:
            logging.error(f"最大化テーマ適用エラー: {e}")
    
    def get_available_size(self):
        """最大化時の利用可能サイズを取得"""
        try:
            if self.maximize_container:
                return self.maximize_container.size()
            return None
            
        except Exception as e:
            logging.error(f"利用可能サイズ取得エラー: {e}")
            return None
