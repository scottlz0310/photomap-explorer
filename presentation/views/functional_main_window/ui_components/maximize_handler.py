"""
最大化・復元機能を担当するハンドラ

このモジュールは functional_new_main_view.py から分離された
画像・マップの最大化表示機能を担当します。
"""

import os
import logging
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QPixmap, QIcon, QFont
from utils.debug_logger import debug, info, warning, error, verbose


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
        
        # 重複防止フラグの初期化
        self._toggle_in_progress = False
        self._last_image_toggle_time = 0
        self._last_map_toggle_time = 0
        
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
        from utils.debug_logger import debug
        debug(f"🔧 MaximizeHandler: コンポーネント設定")
        debug(f"  main_splitter: {main_splitter}")
        debug(f"  preview_panel: {preview_panel}")
        debug(f"  map_panel: {map_panel}")
        
        self.main_splitter = main_splitter
        self.preview_panel = preview_panel
        self.map_panel = map_panel
        
        debug("✅ MaximizeHandler: コンポーネント参照設定完了")
    
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
        from utils.debug_logger import debug, error, warning
        import time
        try:
            # より強力な重複防止機構
            current_time = time.time()
            if hasattr(self, '_last_image_toggle_time'):
                time_diff = current_time - self._last_image_toggle_time
                if time_diff < 0.5:  # 500ms以内の呼び出しをブロック
                    warning(f"⚠️ 画像最大化切り替えの重複呼び出しを検出 ({time_diff:.3f}s間隔) - 処理をスキップ")
                    return
            
            # 進行中フラグのダブルチェック
            if hasattr(self, '_toggle_in_progress') and self._toggle_in_progress:
                warning("⚠️ 画像最大化切り替えが既に進行中です - 処理をスキップ")
                return
            
            # タイムスタンプと処理フラグを設定
            self._last_image_toggle_time = current_time
            self._toggle_in_progress = True
            
            debug("🖼️ MaximizeHandler: 画像最大化切り替え開始")
            debug(f"🔍 呼び出し前の状態: maximized_state={self.maximized_state}")
            debug(f"プレビューパネル: {bool(self.preview_panel)}")
            debug(f"最大化コンテナ: {bool(self.maximize_container)}")
            
            # 実際の表示状態をチェック
            actually_maximized = (self.maximize_container and 
                                 self.maximize_container.isVisible() and 
                                 self.maximize_container.size().width() > 100)
            debug(f"🔍 実際の最大化表示状態: {actually_maximized}")
            
            # 状態の不整合をチェック
            if self.maximized_state == 'image' and not actually_maximized:
                warning("⚠️ 状態不整合検出: 最大化状態だが実際は表示されていない - 状態をリセット")
                self.maximized_state = None
            elif self.maximized_state != 'image' and actually_maximized:
                warning("⚠️ 状態不整合検出: 通常状態だが実際は最大化表示されている - 状態を修正")
                self.maximized_state = 'image'
            
            logging.info("画像最大化切り替え開始")
            if self.maximized_state == 'image':
                debug("🔄 画像最大化状態から通常表示に復元")
                self.restore_normal_view()
            else:
                debug("🔍 通常表示から画像最大化")
                self.maximize_preview()
                
        except Exception as e:
            error(f"画像最大化切り替えエラー: {e}")
            logging.error(f"画像最大化切り替えエラー: {e}")
            import traceback
            traceback.print_exc()
            self.main_window.show_status_message(f"❌ 画像最大化エラー: {e}")
        finally:
            # 処理フラグをクリア
            self._toggle_in_progress = False
            debug(f"🔍 呼び出し後の状態: maximized_state={self.maximized_state}")

    def toggle_map_maximize(self):
        """マップ最大化の切り替え"""
        from utils.debug_logger import debug, error, warning
        import time
        try:
            # より強力な重複防止機構
            current_time = time.time()
            if hasattr(self, '_last_map_toggle_time'):
                time_diff = current_time - self._last_map_toggle_time
                if time_diff < 0.5:  # 500ms以内の呼び出しをブロック
                    warning(f"⚠️ マップ最大化切り替えの重複呼び出しを検出 ({time_diff:.3f}s間隔) - 処理をスキップ")
                    return
            
            # 進行中フラグのダブルチェック
            if hasattr(self, '_toggle_in_progress') and self._toggle_in_progress:
                warning("⚠️ マップ最大化切り替えが既に進行中です - 処理をスキップ")
                return
            
            # タイムスタンプと処理フラグを設定
            self._last_map_toggle_time = current_time
            self._toggle_in_progress = True
            
            debug("🗺️ MaximizeHandler: マップ最大化切り替え開始")
            debug(f"🔍 呼び出し前の状態: maximized_state={self.maximized_state}")
            debug(f"マップパネル: {bool(self.map_panel)}")
            debug(f"最大化コンテナ: {bool(self.maximize_container)}")
            
            # 実際の表示状態をチェック
            actually_maximized = (self.maximize_container and 
                                 self.maximize_container.isVisible() and 
                                 self.maximize_container.size().width() > 100)
            debug(f"🔍 実際の最大化表示状態: {actually_maximized}")
            
            # 状態の不整合をチェック
            if self.maximized_state == 'map' and not actually_maximized:
                warning("⚠️ 状態不整合検出: 最大化状態だが実際は表示されていない - 状態をリセット")
                self.maximized_state = None
            elif self.maximized_state != 'map' and actually_maximized:
                warning("⚠️ 状態不整合検出: 通常状態だが実際は最大化表示されている - 状態を修正")
                self.maximized_state = 'map'
            
            logging.info("マップ最大化切り替え開始")
            if self.maximized_state == 'map':
                debug("🔄 マップ最大化状態から通常表示に復元")
                self.restore_normal_view()
            else:
                debug("🔍 通常表示からマップ最大化")
                self.maximize_map()
                
        except Exception as e:
            error(f"マップ最大化切り替えエラー: {e}")
            logging.error(f"マップ最大化切り替えエラー: {e}")
            import traceback
            traceback.print_exc()
            self.main_window.show_status_message(f"❌ マップ最大化エラー: {e}")
        finally:
            # 処理フラグをクリア
            self._toggle_in_progress = False
            debug(f"🔍 呼び出し後の状態: maximized_state={self.maximized_state}")
    
    def maximize_preview(self):
        """プレビューを最大化（簡略化アプローチ）"""
        try:
            debug("🔧 maximize_preview 開始")
            
            if not self.preview_panel:
                self.main_window.show_status_message("❌ プレビューパネルが利用できません")
                return
            
            debug("簡略化最大化プレビュー開始")
            
            # 既存のスプリッターを非表示にする
            if self.main_splitter:
                self.main_splitter.hide()
                debug("メインスプリッターを非表示")
            
            # 最大化コンテナを直接メインウィンドウに表示
            if self.maximize_container:
                # 既存のコンテナを再利用（安全版 - 削除しない）
                try:
                    # 既存の子ウィジェットを非表示にして再利用準備
                    self.maximize_container.hide()
                    from PyQt5.QtWidgets import QWidget
                    for child in self.maximize_container.findChildren(QWidget):
                        if hasattr(child, 'hide'):
                            child.hide()
                    # Qt イベント処理を実行
                    from PyQt5.QtCore import QCoreApplication
                    QCoreApplication.processEvents()
                    debug("既存の画像最大化コンテナを再利用準備")
                except Exception as e:
                    warning(f"既存コンテナ再利用準備エラー（無視）: {e}")
            else:
                debug("新しい画像最大化コンテナを作成")
                
            # 新しい最大化コンテナを作成
            from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
            central_widget = self.main_window.centralWidget()
            self.maximize_container = QWidget(central_widget)
            
            # ジオメトリを設定（メインウィンドウ全体をカバー）
            if central_widget:
                central_geometry = central_widget.geometry()
                self.maximize_container.setGeometry(0, 0, central_geometry.width(), central_geometry.height())
            else:
                self.maximize_container.setGeometry(0, 0, 1400, 800)
            
            # 背景色を設定（デバッグ用）
            self.maximize_container.setStyleSheet("background-color: black; border: 2px solid red;")
            
            # メインレイアウトを設定
            self.maximized_content_layout = QVBoxLayout(self.maximize_container)
            self.maximized_content_layout.setContentsMargins(10, 10, 10, 10)
            
            # 戻るボタンを追加
            self.restore_button = QPushButton("✖ 戻る")
            self.restore_button.setFixedSize(80, 30)
            self.restore_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.8);
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    color: black;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 0.9);
                }
            """)
            self.restore_button.clicked.connect(self.restore_normal_view)
            
            # 戻るボタンを右上に配置
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(self.restore_button)
            self.maximized_content_layout.addLayout(button_layout)
            
            # プレビューパネルのクローンを作成してコンテンツを表示
            from ui.image_preview import ImagePreviewView
            self.maximized_preview = ImagePreviewView(self.maximize_container)
            
            # 最大化されたプレビューにテーマを適用
            if hasattr(self.main_window, 'register_theme_component'):
                self.main_window.register_theme_component(self.maximized_preview, "image_preview")
                self.main_window.register_theme_component(self.restore_button, "button")
                self.main_window.register_theme_component(self.maximize_container, "panel")
            
            # 現在のテーマを再適用（遅延実行で確実に適用）
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(50, lambda: self._apply_current_theme_to_maximized_widgets())
            
            self.maximized_content_layout.addWidget(self.maximized_preview, 1)  # ストレッチファクター1で拡大
            
            # 現在の画像を新しいプレビューに設定（ズーム機能付き）
            current_image = None
             # 複数の方法で現在の画像を取得
            if hasattr(self.main_window, 'selected_image') and self.main_window.selected_image:
                current_image = self.main_window.selected_image
                debug(f"メインウィンドウから画像取得: {current_image}")
            elif hasattr(self.main_window, 'thumbnail_list') and self.main_window.thumbnail_list and self.main_window.thumbnail_list.currentRow() >= 0:
                item = self.main_window.thumbnail_list.item(self.main_window.thumbnail_list.currentRow())
                if item:
                    current_image = item.data(256)  # Qt.UserRole = 256
                    debug(f"サムネイルリストから画像取得: {current_image}")
            
            if current_image:
                debug(f"画像ファイル確認: 存在={os.path.exists(current_image)}")
                
                # ImagePreviewViewに直接画像を設定
                self.maximized_preview.set_image(current_image)
                
                # レイアウト確定後に適切にフィットするように遅延実行
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(100, lambda: self._ensure_fit_after_layout(current_image))
                info(f"ズーム機能付き画像表示完了（遅延フィット予約）: {current_image}")
            else:
                error("現在の画像が見つかりません")
            
            # コンテナを表示
            self.maximize_container.show()
            self.maximize_container.raise_()
            self.maximize_container.activateWindow()
            
            debug("新しい最大化コンテナ作成完了:")
            debug(f"  - サイズ: {self.maximize_container.size()}")
            debug(f"  - 位置: {self.maximize_container.pos()}")
            debug(f"  - 親: {self.maximize_container.parent()}")
            debug(f"  - 表示状態: {self.maximize_container.isVisible()}")
            
            # 実際に表示されているかチェック
            display_successful = (self.maximize_container.isVisible() and 
                                self.maximize_container.size().width() > 100 and 
                                self.maximize_container.size().height() > 100)
            debug(f"🔍 画像最大化表示成功チェック: {display_successful}")
            
            if display_successful:
                # 状態設定を確実に実行
                debug(f"🔧 状態設定前: {self.maximized_state}")
                self.maximized_state = 'image'
                debug(f"🔧 状態設定後: {self.maximized_state}")
                self.main_window.show_status_message("🖼️ 画像を最大化表示")
                debug(f"✅ 画像最大化状態設定完了: {self.maximized_state}")
            else:
                warning("❌ 画像最大化表示に失敗、状態をリセット")
                self.maximized_state = None
                self.main_window.show_status_message("❌ 画像最大化に失敗しました")
            
        except Exception as e:
            logging.error(f"プレビュー最大化エラー: {e}")
            self.main_window.show_status_message(f"❌ プレビュー最大化エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def maximize_map(self):
        """マップを最大化（簡略化アプローチ）"""
        try:
            debug("🔧 maximize_map 開始")
            
            if not self.map_panel:
                self.main_window.show_status_message("❌ マップパネルが利用できません")
                return
            
            debug("簡略化最大化マップ開始")
            
            # 既存のスプリッターを非表示にする
            if self.main_splitter:
                self.main_splitter.hide()
                debug("メインスプリッターを非表示")
            
            # 最大化コンテナを直接メインウィンドウに表示
            if self.maximize_container:
                # 既存のコンテナを再利用（安全版 - 削除しない）
                try:
                    # 既存の子ウィジェットを非表示にして再利用準備
                    self.maximize_container.hide()
                    from PyQt5.QtWidgets import QWidget
                    for child in self.maximize_container.findChildren(QWidget):
                        if hasattr(child, 'hide'):
                            child.hide()
                    # Qt イベント処理を実行
                    from PyQt5.QtCore import QCoreApplication
                    QCoreApplication.processEvents()
                    debug("既存の地図最大化コンテナを再利用準備")
                except Exception as e:
                    warning(f"既存コンテナ再利用準備エラー（無視）: {e}")
            else:
                debug("新しい地図最大化コンテナを作成")
                
            # 新しい最大化コンテナを作成
            from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
            central_widget = self.main_window.centralWidget()
            self.maximize_container = QWidget(central_widget)
            
            # ジオメトリを設定（メインウィンドウ全体をカバー）
            if central_widget:
                central_geometry = central_widget.geometry()
                self.maximize_container.setGeometry(0, 0, central_geometry.width(), central_geometry.height())
            else:
                self.maximize_container.setGeometry(0, 0, 1400, 800)
            
            # 背景色を設定
            self.maximize_container.setStyleSheet("background-color: white; border: 2px solid blue;")
            
            # メインレイアウトを設定
            self.maximized_content_layout = QVBoxLayout(self.maximize_container)
            self.maximized_content_layout.setContentsMargins(10, 10, 10, 10)
            
            # 戻るボタンを追加（確実に表示）
            self.restore_button = QPushButton("✖ 戻る")
            self.restore_button.setFixedSize(100, 40)  # 少し大きく
            self.restore_button.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 0.9);
                    border: 2px solid #333;
                    border-radius: 6px;
                    color: black;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: rgba(200, 200, 200, 0.9);
                }
            """)
            self.restore_button.clicked.connect(self.restore_normal_view)
            
            # 戻るボタンを右上に配置（zオーダーを最上位に）
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            button_layout.addWidget(self.restore_button)
            self.maximized_content_layout.addLayout(button_layout)
            
            # 戻るボタンを最前面に表示
            self.restore_button.show()
            self.restore_button.raise_()
            debug("地図最大化の戻るボタン作成: size={}, visible={}".format(self.restore_button.size(), self.restore_button.isVisible()))
            
            # マップパネルのクローンを作成してコンテンツを表示
            from ui.map_panel import MapPanel
            self.maximized_map = MapPanel(self.maximize_container)
            
            # 最大化されたマップにテーマを適用
            if hasattr(self.main_window, 'register_theme_component'):
                self.main_window.register_theme_component(self.maximized_map, "map_panel")
                self.main_window.register_theme_component(self.restore_button, "button")
                self.main_window.register_theme_component(self.maximize_container, "panel")
            
            # 現在のテーマを再適用（遅延実行で確実に適用）
            from PyQt5.QtCore import QTimer
            QTimer.singleShot(50, lambda: self._apply_current_theme_to_maximized_widgets())
            
            self.maximized_content_layout.addWidget(self.maximized_map, 1)  # ストレッチファクター1で拡大
            
            info("最大化マップパネル作成完了")
            
            # 現在の画像のGPS情報を取得してマップに表示
            current_image = None
            # 複数の方法で現在の画像を取得
            if hasattr(self.main_window, 'selected_image') and self.main_window.selected_image:
                current_image = self.main_window.selected_image
                debug(f"メインウィンドウから画像取得: {current_image}")
            elif hasattr(self.main_window, 'thumbnail_list') and self.main_window.thumbnail_list and self.main_window.thumbnail_list.currentRow() >= 0:
                item = self.main_window.thumbnail_list.item(self.main_window.thumbnail_list.currentRow())
                if item:
                    current_image = item.data(256)  # Qt.UserRole = 256
                    debug(f"サムネイルリストから画像取得: {current_image}")
            
            if current_image:
                debug(f"マップ用画像ファイル確認: 存在={os.path.exists(current_image)}")
                
                # GPS情報を取得してマップに表示
                try:
                    from logic.image_utils import extract_gps_coords
                    gps_info = extract_gps_coords(current_image)
                    
                    if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                        lat, lon = gps_info["latitude"], gps_info["longitude"]
                        success = self.maximized_map.update_location(lat, lon)
                        if success:
                            info(f"最大化マップに位置情報表示成功: {lat:.6f}, {lon:.6f}")
                        else:
                            warning("最大化マップ位置情報表示失敗")
                    else:
                        warning("GPS情報なし、デフォルトメッセージ表示")
                        self.maximized_map.show_no_gps_message()
                        
                except Exception as gps_error:
                    warning(f"GPS情報取得エラー: {gps_error}")
                    self.maximized_map.show_no_gps_message()
                    
                # レイアウト確定後にマップを再更新
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(200, lambda: self._ensure_map_display_after_layout(current_image))
                info(f"最大化マップ表示完了（遅延更新予約）: {current_image}")
            else:
                error("現在の画像が見つかりません、デフォルトメッセージ表示")
                self.maximized_map.show_no_gps_message()
            
            # コンテナを表示
            self.maximize_container.show()
            self.maximize_container.raise_()
            self.maximize_container.activateWindow()
            
            debug("新しい最大化マップコンテナ作成完了:")
            debug(f"  - サイズ: {self.maximize_container.size()}")
            debug(f"  - 位置: {self.maximize_container.pos()}")
            debug(f"  - 親: {self.maximize_container.parent()}")
            debug(f"  - 表示状態: {self.maximize_container.isVisible()}")
            
            # 実際に表示されているかチェック
            display_successful = (self.maximize_container.isVisible() and 
                                self.maximize_container.size().width() > 100 and 
                                self.maximize_container.size().height() > 100)
            debug(f"🔍 マップ最大化表示成功チェック: {display_successful}")
            
            if display_successful:
                # 状態設定を確実に実行
                debug(f"🔧 状態設定前: {self.maximized_state}")
                self.maximized_state = 'map'
                debug(f"🔧 状態設定後: {self.maximized_state}")
                self.main_window.show_status_message("🗺️ マップを最大化表示")
                debug(f"✅ マップ最大化状態設定完了: {self.maximized_state}")
            else:
                warning("❌ マップ最大化表示に失敗、状態をリセット")
                self.maximized_state = None
                self.main_window.show_status_message("❌ マップ最大化に失敗しました")
            
        except Exception as e:
            logging.error(f"マップ最大化エラー: {e}")
            self.main_window.show_status_message(f"❌ マップ最大化エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def restore_normal_view(self):
        """通常表示に復元（コンテナ保持版 - Segmentation fault完全回避）"""
        try:
            debug("通常表示に復元開始（コンテナ保持版）")
            
            # 最大化状態を記録してすぐにリセット（重複呼び出し防止）
            previous_state = self.maximized_state
            self.maximized_state = None
            
            # まず、すべてのシグナル接続を安全に切断
            if hasattr(self, 'restore_button') and self.restore_button:
                try:
                    self.restore_button.clicked.disconnect()
                    info("復元ボタンのシグナル切断")
                except:
                    pass
            
            # 最大化コンテナを完全に非表示（削除しない）
            if hasattr(self, 'maximize_container') and self.maximize_container:
                try:
                    self.maximize_container.hide()
                    self.maximize_container.setVisible(False)
                    # Z-orderを最低にして他のウィジェットの下に隠す
                    self.maximize_container.lower()
                    info("最大化コンテナを完全非表示")
                except Exception as e:
                    warning(f"コンテナ非表示エラー: {e}")
            
            # QCoreApplication.processEvents()を実行してUI更新を確実に実行
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            # 子ウィジェットを非表示にするだけ（削除しない）
            safe_hide_widgets = [
                ('maximized_preview', '最大化プレビュー'),
                ('maximized_map', '最大化マップ'),
                ('restore_button', '復元ボタン')
            ]
            
            # 子ウィジェットを安全に非表示
            for attr_name, description in safe_hide_widgets:
                if hasattr(self, attr_name):
                    widget = getattr(self, attr_name)
                    if widget:
                        try:
                            widget.hide()
                            widget.setVisible(False)
                            # 属性はクリアしない（再利用のため保持）
                            info(f"{description}を非表示")
                        except Exception as e:
                            warning(f"{description}非表示エラー（無視）: {e}")
            
            # イベント処理を実行
            QCoreApplication.processEvents()
            
            # レイアウトも削除せずに非表示のみ
            if hasattr(self, 'maximized_content_layout') and self.maximized_content_layout:
                try:
                    # レイアウトの全子ウィジェットを非表示（削除しない）
                    for i in range(self.maximized_content_layout.count()):
                        item = self.maximized_content_layout.itemAt(i)
                        if item:
                            widget = item.widget()
                            if widget and hasattr(widget, 'hide'):
                                widget.hide()
                    info("レイアウト内ウィジェットを非表示")
                except Exception as e:
                    warning(f"レイアウト非表示エラー（無視）: {e}")
            
            # 最終的なイベント処理
            QCoreApplication.processEvents()
            
            # メインスプリッターを確実に再表示
            if hasattr(self, 'main_splitter') and self.main_splitter:
                try:
                    self.main_splitter.show()
                    self.main_splitter.setVisible(True)
                    self.main_splitter.raise_()  # 最前面に
                    self.main_splitter.update()
                    info("メインスプリッターを再表示")
                except Exception as e:
                    warning(f"メインスプリッター再表示エラー: {e}")
            
            # メインウィンドウの完全な再描画
            if hasattr(self.main_window, 'update'):
                self.main_window.update()
                self.main_window.repaint()
            
            # 状態に応じたメッセージ
            if previous_state == 'image':
                self.main_window.show_status_message("↩️ 画像表示を復元しました")
            elif previous_state == 'map':
                self.main_window.show_status_message("↩️ マップ表示を復元しました")
            else:
                self.main_window.show_status_message("↩️ 通常表示に復元しました")
            
            info("通常表示復元完了（コンテナ保持版）")
            
        except Exception as e:
            logging.error(f"復元エラー: {e}")
            self.main_window.show_status_message(f"❌ 復元エラー: {e}")
            import traceback
            traceback.print_exc()
            
            # 緊急復旧処理
            self._emergency_restore()
    
    def _emergency_restore(self):
        """緊急復旧処理（コンテナ保持版）"""
        try:
            error("緊急復旧処理開始（コンテナ保持版）")
            
            # 状態の強制リセット
            self.maximized_state = None
            
            # 最大化コンテナを完全非表示（削除しない）
            if hasattr(self, 'maximize_container') and self.maximize_container:
                try:
                    self.maximize_container.hide()
                    self.maximize_container.setVisible(False)
                    self.maximize_container.lower()
                    info("緊急: 最大化コンテナ非表示")
                except Exception as e:
                    warning(f"緊急: コンテナ非表示エラー: {e}")
            
            # すべての最大化関連ウィジェットを非表示（削除しない）
            emergency_widgets = [
                'restore_button', 'maximized_preview', 'maximized_map'
            ]
            
            for attr in emergency_widgets:
                if hasattr(self, attr):
                    try:
                        widget = getattr(self, attr)
                        if widget and hasattr(widget, 'hide'):
                            widget.hide()
                            widget.setVisible(False)
                        info(f"緊急: {attr}を非表示")
                    except Exception as e:
                        warning(f"緊急: {attr}非表示エラー（無視）: {e}")
            
            # イベント処理を実行
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            # メインスプリッターの強制表示
            if hasattr(self, 'main_splitter') and self.main_splitter:
                try:
                    self.main_splitter.show()
                    self.main_splitter.setVisible(True)
                    self.main_splitter.raise_()
                    info("緊急: メインスプリッター表示")
                except Exception as e:
                    warning(f"緊急: スプリッター表示エラー: {e}")
            
            # 最大化ボタンの状態をリセット
            try:
                self.update_maximize_buttons()
                info("緊急: ボタン状態リセット")
            except Exception as e:
                warning(f"緊急: ボタンリセットエラー: {e}")
            
            info("緊急復旧完了（コンテナ保持版）")
            
        except Exception as recovery_error:
            error(f"緊急復旧も失敗: {recovery_error}")
            # 最後の手段：アプリケーション再起動を提案
            try:
                self.main_window.show_status_message("❌ 復旧に失敗しました。アプリケーションの再起動をお勧めします。")
            except:
                error("最終メッセージ表示も失敗")
    
    def refresh_maximized_content(self):
        """最大化されたコンテンツを強制的に更新（強力な表示強制措置付き）"""
        try:
            container = self.maximize_container
            if container is None:
                error("refresh_maximized_content: コンテナがありません")
                return
            
            # コンテナの詳細情報
            debug("refresh_maximized_content - コンテナ詳細:")
            
            # 選択された画像を複数の方法で取得
            selected_image = None
            
            # 1. メインウィンドウから直接取得
            if hasattr(self.main_window, 'selected_image') and self.main_window.selected_image:
                selected_image = self.main_window.selected_image
            
            # 2. 画像イベントハンドラーから取得
            elif hasattr(self.main_window, 'image_event_handler') and self.main_window.image_event_handler:
                if hasattr(self.main_window.image_event_handler, 'selected_image'):
                    selected_image = self.main_window.image_event_handler.selected_image
            
            # 3. フォルダイベントハンドラーから取得
            elif hasattr(self.main_window, 'folder_event_handler') and self.main_window.folder_event_handler:
                if hasattr(self.main_window.folder_event_handler, 'selected_image'):
                    selected_image = self.main_window.folder_event_handler.selected_image
            
            # 4. サムネイルリストから取得（安全な方法）
            elif hasattr(self.main_window, 'thumbnail_list') and self.main_window.thumbnail_list:
                thumbnail_list = self.main_window.thumbnail_list
                current_row = thumbnail_list.currentRow()
                if current_row >= 0:
                    item = thumbnail_list.item(current_row)
                    if item:
                        # ファイルパスを直接取得（UserRoleの代わり）
                        selected_image = item.text()  # アイテムのテキストを使用
                        info(f"画像データを取得 (thumbnail_list): {selected_image}")
            
            if selected_image:
                debug(f"最大化コンテンツ更新: {selected_image}")
                
                if self.maximized_state == 'image':
                    # 直接画像を設定
                    self._update_maximized_image_direct(selected_image)
                        
                elif self.maximized_state == 'map':
                    # 直接マップを設定
                    self._update_maximized_map_direct(selected_image)
            else:
                error("選択された画像が見つかりません")
            
            # 強力な表示強制措置
            debug("強力な表示強制措置を実行中...")
            
            # 1. 親ウィンドウを最前面に
            main_window = container.window()
            if main_window:
                main_window.raise_()
                main_window.activateWindow()
                info(f"メインウィンドウを最前面に移動: {main_window}")
            
            # 2. コンテナの可視性サイクル（複数回）
            for i in range(3):
                container.hide()
                QCoreApplication.processEvents()
                container.show()
                QCoreApplication.processEvents()
                container.raise_()
                QCoreApplication.processEvents()
                container.activateWindow()
                QCoreApplication.processEvents()
            
            # 3. ジオメトリの強制設定（固定値を使用）
            container.setGeometry(0, 40, 1400, 800)
            info(f"ジオメトリ強制設定: {container.geometry()}")
            
            # 4. ウィンドウフラグの調整（コメントアウト - 問題の可能性）
            # container.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)
            # container.show()
            # info("ウィンドウフラグ調整完了")
            
            # 5. レイアウトの強制更新
            layout = container.layout()
            if layout:
                layout.update()
                layout.activate()
                info("レイアウト強制更新完了")
            
            # 6. 再描画の強制
            container.repaint()
            container.update()
            info("再描画強制完了")
            
            # 最終状態確認
            debug("最終状態確認:")
                        
        except Exception as e:
            logging.error(f"最大化コンテンツ更新エラー: {e}")
            error(f"最大化コンテンツ更新エラー: {e}")
            import traceback
            traceback.print_exc()
    
    def _update_maximized_image_direct(self, image_path):
        """最大化時の画像を直接更新（ズーム機能維持）"""
        try:
            debug(f"最大化画像設定開始: {image_path}")
            
            # 最大化されたプレビューが存在する場合、直接使用
            if hasattr(self, 'maximized_preview') and self.maximized_preview:
                self.maximized_preview.set_image(image_path)
                info(f"最大化画像設定成功 (ズーム機能付き): {image_path}")
                return
            
            # フォールバック: 通常のプレビューパネルを使用
            if self.preview_panel:
                info(f"プレビューパネル検出: {type(self.preview_panel)}")
                
                # set_imageメソッドがある場合（ImagePreviewViewの標準メソッド）- 最優先
                if hasattr(self.preview_panel, 'set_image'):
                    self.preview_panel.set_image(image_path)
                    info(f"最大化画像設定成功 (set_image): {image_path}")
                
                # ImagePreviewViewの場合
                elif hasattr(self.preview_panel, 'image_label'):
                    from PyQt5.QtGui import QPixmap
                    from PyQt5.QtCore import Qt
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        # 最大化コンテナのサイズに合わせてスケール
                        if self.maximize_container:
                            container_size = self.maximize_container.size()
                            max_width = max(800, container_size.width() - 100)
                            max_height = max(600, container_size.height() - 150)
                        else:
                            max_width, max_height = 1200, 800
                            
                        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type: ignore
                        self.preview_panel.image_label.setPixmap(scaled_pixmap)
                        info(f"最大化画像設定成功 (image_label): {image_path}")
                        
                # 通常のQLabel扱いの場合
                elif hasattr(self.preview_panel, 'setPixmap'):
                    from PyQt5.QtGui import QPixmap
                    from PyQt5.QtCore import Qt
                    pixmap = QPixmap(image_path)
                    if not pixmap.isNull():
                        if self.maximize_container:
                            container_size = self.maximize_container.size()
                            max_width = max(800, container_size.width() - 100)
                            max_height = max(600, container_size.height() - 150)
                        else:
                            max_width, max_height = 1200, 800
                            
                        scaled_pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)  # type: ignore
                        self.preview_panel.setPixmap(scaled_pixmap)
                        info(f"最大化画像設定成功 (setPixmap): {image_path}")
                
                # load_image_from_pathメソッドがある場合
                elif hasattr(self.preview_panel, 'load_image_from_path'):
                    self.preview_panel.load_image_from_path(image_path)
                    info(f"最大化画像設定成功 (load_image_from_path): {image_path}")
                
                else:
                    error(f"プレビューパネルに画像設定メソッドが見つかりません: {[attr for attr in dir(self.preview_panel) if not attr.startswith('_')]}")
            else:
                error("プレビューパネルが None です")
                
        except Exception as e:
            error(f"最大化画像直接設定エラー: {e}")
            logging.error(f"最大化画像直接設定エラー: {e}")
    
    def _update_maximized_map_direct(self, image_path):
        """最大化時のマップを直接更新"""
        try:
            import os
            if self.map_panel and hasattr(self.map_panel, 'view'):
                # GPS情報を取得してHTMLで表示
                from logic.image_utils import extract_gps_coords
                gps_info = extract_gps_coords(image_path)
                
                if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                    lat, lon = gps_info["latitude"], gps_info["longitude"]
                    html_content = f"""
                    <html>
                    <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px; margin: 0; background-color: #2d2d2d; color: #ffffff;">
                        <div style="background: #3d3d3d; border: 2px solid #007ACC; border-radius: 10px; padding: 40px; max-width: 600px; margin: 0 auto;">
                            <h2 style="color: #007ACC; margin-top: 0;">📍 GPS座標情報（最大化表示）</h2>
                            <p style="margin: 20px 0; font-size: 18px;"><strong>緯度:</strong> {lat:.6f}</p>
                            <p style="margin: 20px 0; font-size: 18px;"><strong>経度:</strong> {lon:.6f}</p>
                            <p style="margin: 20px 0; color: #cccccc; font-size: 16px;"><strong>画像:</strong> {os.path.basename(image_path)}</p>
                            <div style="margin-top: 30px; padding: 20px; background: #4d4d4d; border-radius: 5px;">
                                <small style="color: #cccccc; font-size: 14px;">最大化表示中 - GPS座標が含まれています</small>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    self.map_panel.view.setHtml(html_content)
                    info(f"最大化マップ直接設定: {lat:.6f}, {lon:.6f}")
        except Exception as e:
            error(f"最大化マップ直接設定エラー: {e}")
    
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
    
    def _ensure_fit_after_layout(self, image_path):
        """レイアウト確定後に画像を適切にフィット表示"""
        try:
            if hasattr(self, 'maximized_preview') and self.maximized_preview:
                # ウィジェットサイズが確定するまで待機
                from PyQt5.QtCore import QCoreApplication
                QCoreApplication.processEvents()
                
                # 現在のサイズを確認
                current_size = self.maximized_preview.size()
                debug(f"レイアウト確定後のサイズ: {current_size}")
                
                # サイズが適切に設定されている場合のみフィット実行
                if current_size.width() > 100 and current_size.height() > 100:
                    # レイアウト確定後に画像を再設定してフィット処理を確実に実行
                    try:
                        debug(f"レイアウト確定後の画像再設定: {image_path}")
                        self.maximized_preview.set_image(image_path)
                        info(f"遅延フィット実行成功: {current_size}")
                    except Exception as fit_error:
                        warning(f"遅延フィットエラー（画像表示は成功）: {fit_error}")
                    
                else:
                    warning(f"ウィジェットサイズが未確定、再試行: {current_size}")
                    # 再度遅延実行
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(200, lambda: self._ensure_fit_after_layout(image_path))
                    
        except Exception as e:
            error(f"遅延フィット処理エラー: {e}")
    
    def _ensure_map_display_after_layout(self, image_path):
        """レイアウト確定後にマップを適切に表示"""
        try:
            if hasattr(self, 'maximized_map') and self.maximized_map:
                # ウィジェットサイズが確定するまで待機
                from PyQt5.QtCore import QCoreApplication
                QCoreApplication.processEvents()
                
                # 現在のサイズを確認
                current_size = self.maximized_map.size()
                debug(f"マップレイアウト確定後のサイズ: {current_size}")
                
                # サイズが適切に設定されている場合のみマップ更新実行
                if current_size.width() > 100 and current_size.height() > 100:
                    # GPS情報を再取得してマップを更新
                    try:
                        from logic.image_utils import extract_gps_coords
                        gps_info = extract_gps_coords(image_path)
                        
                        if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                            lat, lon = gps_info["latitude"], gps_info["longitude"]
                            debug(f"レイアウト確定後のマップ更新: {lat:.6f}, {lon:.6f}")
                            success = self.maximized_map.update_location(lat, lon)
                            if success:
                                info(f"遅延マップ表示成功: {current_size}")
                            else:
                                warning("遅延マップ表示失敗")
                        else:
                            warning("GPS情報なし、メッセージ表示維持")
                            self.maximized_map.show_no_gps_message()
                            
                    except Exception as gps_error:
                        warning(f"遅延GPS取得エラー: {gps_error}")
                        self.maximized_map.show_no_gps_message()
                    
                else:
                    warning(f"マップウィジェットサイズが未確定、再試行: {current_size}")
                    # 再度遅延実行
                    from PyQt5.QtCore import QTimer
                    QTimer.singleShot(300, lambda: self._ensure_map_display_after_layout(image_path))
                    
        except Exception as e:
            error(f"遅延マップ表示処理エラー: {e}")
    
    def _apply_current_theme_to_maximized_widgets(self):
        """最大化されたウィジェットに現在のテーマを適用"""
        try:
            # テーマ情報を統一された方法で取得
            theme_colors = None
            current_theme = None
            
            # 優先順位1: テーマイベントハンドラーから取得（最も信頼性が高い）
            if hasattr(self.main_window, 'theme_event_handler'):
                theme_handler = self.main_window.theme_event_handler
                if hasattr(theme_handler, 'current_theme'):
                    current_theme = theme_handler.current_theme
                    debug(f"テーマハンドラーから現在のテーマ取得: {current_theme}")
                    
                    # 基本的なテーマカラーを設定
                    if current_theme == "dark":
                        theme_colors = {
                            'background': '#2d2d2d',
                            'foreground': '#ffffff',
                            'accent': '#007ACC',
                            'secondary': '#4d4d4d'
                        }
                    else:
                        theme_colors = {
                            'background': '#ffffff',
                            'foreground': '#000000',
                            'accent': '#007ACC',
                            'secondary': '#f0f0f0'
                        }
            
            # 優先順位2: テーママネージャーから取得（フォールバック）
            if not theme_colors and hasattr(self.main_window, 'theme_manager'):
                theme_manager = self.main_window.theme_manager
                if hasattr(theme_manager, 'get_current_theme'):
                    fallback_theme = theme_manager.get_current_theme()
                    debug(f"フォールバック: テーママネージャーから取得: {fallback_theme}")
                    current_theme = fallback_theme  # 統一
                    
                    if fallback_theme == "dark":
                        theme_colors = {
                            'background': '#2d2d2d',
                            'foreground': '#ffffff',
                            'accent': '#007ACC',
                            'secondary': '#4d4d4d'
                        }
                    else:
                        theme_colors = {
                            'background': '#ffffff',
                            'foreground': '#000000',
                            'accent': '#007ACC',
                            'secondary': '#f0f0f0'
                        }
            
            # 優先順位3: デフォルトテーマを使用
            if not theme_colors:
                warning("テーマ情報取得失敗、デフォルトテーマを適用")
                current_theme = "light"  # デフォルト
                theme_colors = {
                    'background': '#ffffff',
                    'foreground': '#000000',
                    'accent': '#007ACC',
                    'secondary': '#f0f0f0'
                }
            
            # テーマカラーを適用
            if theme_colors:
                debug(f"最終的に使用するテーマ: {current_theme}")
                self._apply_theme_colors_to_widgets(theme_colors)
                info(f"最大化ウィジェットにテーマ適用完了: {theme_colors}")
                
        except Exception as e:
            error(f"テーマ適用エラー: {e}")
            logging.error(f"最大化ウィジェットテーマ適用エラー: {e}")
    
    def _apply_theme_colors_to_widgets(self, theme_colors):
        """テーマカラーをウィジェットに適用"""
        try:
            debug(f"テーマカラー適用開始: {theme_colors}")
            
            # 最大化コンテナにテーマ適用
            if self.maximize_container:
                container_style = f"""
                    QWidget {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: none;
                    }}
                """
                self.maximize_container.setStyleSheet(container_style)
                info("最大化コンテナにテーマ適用")
            
            # 復元ボタンにテーマ適用
            if hasattr(self, 'restore_button') and self.restore_button:
                button_style = f"""
                    QPushButton {{
                        background-color: {theme_colors['secondary']};
                        color: {theme_colors['foreground']};
                        border: 2px solid {theme_colors['accent']};
                        border-radius: 6px;
                        padding: 8px 12px;
                        font-weight: bold;
                        font-size: 14px;
                    }}
                    QPushButton:hover {{
                        background-color: {theme_colors['accent']};
                        color: white;
                        border-color: {theme_colors['accent']};
                    }}
                    QPushButton:pressed {{
                        background-color: {theme_colors['foreground']};
                        color: {theme_colors['background']};
                    }}
                """
                self.restore_button.setStyleSheet(button_style)
                info("復元ボタンにテーマ適用")
            
            # 最大化されたプレビューにテーマ適用
            if hasattr(self, 'maximized_preview') and self.maximized_preview:
                preview_style = f"""
                    QWidget {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: 1px solid {theme_colors['secondary']};
                    }}
                    QLabel {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: none;
                    }}
                    QGraphicsView {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: 1px solid {theme_colors['secondary']};
                    }}
                """
                self.maximized_preview.setStyleSheet(preview_style)
                info("最大化プレビューにテーマ適用")
                
                # プレビューパネル内の子ウィジェットにもテーマ適用
                if hasattr(self.maximized_preview, 'image_label'):
                    self.maximized_preview.image_label.setStyleSheet(f"""
                        QLabel {{
                            background-color: {theme_colors['background']};
                            color: {theme_colors['foreground']};
                            border: none;
                        }}
                    """)
                    info("プレビューの画像ラベルにテーマ適用")
            
            # 最大化されたマップにテーマ適用
            if hasattr(self, 'maximized_map') and self.maximized_map:
                map_style = f"""
                    QWidget {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: 1px solid {theme_colors['secondary']};
                    }}
                    QWebEngineView {{
                        background-color: {theme_colors['background']};
                        border: 1px solid {theme_colors['secondary']};
                    }}
                """
                self.maximized_map.setStyleSheet(map_style)
                info("最大化マップにテーマ適用")
                
                # マップパネル内のWebEngineViewにもテーマ適用
                if hasattr(self.maximized_map, 'view') and self.maximized_map.view:
                    try:
                        self.maximized_map.view.setStyleSheet(f"""
                            QWebEngineView {{
                                background-color: {theme_colors['background']};
                                border: 1px solid {theme_colors['secondary']};
                            }}
                        """)
                        info("マップのWebEngineViewにテーマ適用")
                    except Exception as view_error:
                        warning("マップビューテーマ適用エラー（無視）: {view_error}")
            
            # 最大化コンテンツエリアにもテーマ適用
            if hasattr(self, 'maximized_content_area') and self.maximized_content_area:
                content_style = f"""
                    QWidget {{
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                        border: none;
                    }}
                """
                self.maximized_content_area.setStyleSheet(content_style)
                info("最大化コンテンツエリアにテーマ適用")
                
            info("最大化ウィジェットテーマ適用完了")
            
        except Exception as e:
            error(f"テーマカラー適用エラー: {e}")
            logging.error(f"テーマカラー適用エラー: {e}")
    
    def on_theme_changed(self, theme_name):
        """テーマ変更時に最大化されたウィジェットにも反映"""
        try:
            if self.is_maximized():
                debug(f"テーマ変更検出、最大化ウィジェットに反映: {theme_name}")
                # 少し遅延してテーマを適用（確実に新しいテーマが設定された後に実行）
                from PyQt5.QtCore import QTimer
                QTimer.singleShot(100, lambda: self._apply_current_theme_to_maximized_widgets())
        except Exception as e:
            error(f"テーマ変更時のエラー: {e}")
            logging.error(f"テーマ変更時エラー: {e}")
    
    def setup_theme_change_listener(self):
        """テーマ変更の監視設定"""
        try:
            # テーマイベントハンドラーがある場合、テーマ変更シグナルに接続
            if hasattr(self.main_window, 'theme_event_handler'):
                theme_handler = self.main_window.theme_event_handler
                if hasattr(theme_handler, 'theme_changed'):
                    theme_handler.theme_changed.connect(self.on_theme_changed)
                    info("テーマ変更リスナー設定完了")
                    return True
        except Exception as e:
            warning(f"テーマ変更リスナー設定エラー: {e}")
        return False
