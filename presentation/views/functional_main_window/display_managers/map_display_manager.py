"""
マップ表示・GPS処理を担当するマネージャー

このモジュールは functional_new_main_view.py から分離された
マップ表示・GPS関連の機能を担当します。
"""

import os
import logging


class MapDisplayManager:
    """マップ表示・GPS処理を担当するマネージャー"""
    
    def __init__(self, main_window):
        """
        マップ表示マネージャーを初期化
        
        Args:
            main_window: メインウィンドウインスタンス
        """
        self.main_window = main_window
        self.current_location = None
        self.current_image = None
        
        # コンポーネント参照
        self.map_panel = None
        
        # 表示設定
        self.default_zoom = 15
        
    def set_components(self, map_panel):
        """コンポーネントの参照を設定"""
        self.map_panel = map_panel
    
    def update_map(self, image_path):
        """GPS情報を取得してマップを更新"""
        try:
            if not self.map_panel:
                self.main_window.show_status_message("📍 マップパネルが利用できません")
                return False
            
            self.current_image = image_path
            
            # GPS情報抽出
            gps_info = self._extract_gps_info(image_path)
            
            if gps_info and "latitude" in gps_info and "longitude" in gps_info:
                lat, lon = gps_info["latitude"], gps_info["longitude"]
                self.current_location = (lat, lon)
                
                # マップ更新
                success = self._update_map_display(lat, lon, image_path)
                
                if success:
                    self.main_window.show_status_message(f"📍 マップ表示: {lat:.6f}, {lon:.6f}")
                    return True
                else:
                    self.main_window.show_status_message("📍 マップ更新に失敗")
                    return False
            else:
                # GPS情報なしの場合
                self._show_no_gps_display()
                self.main_window.show_status_message("📍 GPS情報が見つかりません")
                return False
                
        except Exception as e:
            logging.error(f"マップ更新エラー: {e}")
            self.main_window.show_status_message(f"❌ マップ更新エラー: {e}")
            return False
    
    def _extract_gps_info(self, image_path):
        """画像からGPS情報を抽出"""
        try:
            from logic.image_utils import extract_gps_coords
            return extract_gps_coords(image_path)
            
        except ImportError:
            logging.warning("GPS抽出モジュールが利用できません")
            return None
        except Exception as e:
            logging.error(f"GPS情報抽出エラー: {e}")
            return None
    
    def _update_map_display(self, lat, lon, image_path):
        """マップ表示を更新"""
        try:
            # マップパネルの update_location メソッドを試行
            if hasattr(self.map_panel, 'update_location'):
                return self.map_panel.update_location(lat, lon)  # type: ignore
            
            # HTMLベースのマップ表示
            elif hasattr(self.map_panel, 'view'):
                return self._show_gps_html(lat, lon, image_path)
            
            # フォールバック: 基本的な情報表示
            else:
                return self._show_basic_gps_info(lat, lon, image_path)
                
        except Exception as e:
            logging.error(f"マップ表示更新エラー: {e}")
            return False
    
    def _show_gps_html(self, lat, lon, image_path):
        """GPS情報のHTML表示"""
        try:
            # 最大化状態の確認
            maximized_state = getattr(self.main_window, 'maximized_state', None)
            status_text = "最大化表示中" if maximized_state == 'map' else "GPS座標が含まれています"
            
            # テーマ色の取得
            theme_colors = self._get_theme_colors()
            
            gps_html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 20px;
                        margin: 0;
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                    }}
                    .gps-container {{
                        background: {theme_colors['panel_bg']};
                        border: 2px solid {theme_colors['accent']};
                        border-radius: 10px;
                        padding: 20px;
                        max-width: 400px;
                        margin: 0 auto;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .gps-title {{
                        color: {theme_colors['accent']};
                        margin-top: 0;
                        font-size: 18px;
                    }}
                    .gps-coord {{
                        margin: 10px 0;
                        font-size: 14px;
                    }}
                    .gps-image {{
                        color: {theme_colors['muted']};
                        margin: 10px 0;
                        font-size: 12px;
                    }}
                    .gps-status {{
                        margin-top: 15px;
                        padding: 10px;
                        background: {theme_colors['secondary']};
                        border-radius: 5px;
                        font-size: 11px;
                    }}
                </style>
            </head>
            <body>
                <div class="gps-container">
                    <h3 class="gps-title">📍 GPS座標情報</h3>
                    <p class="gps-coord"><strong>緯度:</strong> {lat:.6f}</p>
                    <p class="gps-coord"><strong>経度:</strong> {lon:.6f}</p>
                    <p class="gps-image"><strong>画像:</strong> {os.path.basename(image_path)}</p>
                    <div class="gps-status">
                        <small>{status_text}</small>
                    </div>
                </div>
            </body>
            </html>
            """
            
            self.map_panel.view.setHtml(gps_html)  # type: ignore
            self.map_panel.view.update()  # type: ignore
            self.map_panel.view.repaint()  # type: ignore
            
            return True
            
        except Exception as e:
            logging.error(f"GPS HTML表示エラー: {e}")
            return False
    
    def _show_no_gps_display(self):
        """GPS情報なしの表示"""
        try:
            if hasattr(self.map_panel, 'view'):
                return self._show_no_gps_html()
            else:
                return self._show_basic_no_gps_info()
                
        except Exception as e:
            logging.error(f"GPS無し表示エラー: {e}")
            return False
    
    def _show_no_gps_html(self):
        """GPS情報なしのHTML表示"""
        try:
            theme_colors = self._get_theme_colors()
            
            no_gps_html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px;
                        margin: 0;
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                    }}
                    .no-gps-container {{
                        background: {theme_colors['panel_bg']};
                        border: 2px solid {theme_colors['warning']};
                        border-radius: 10px;
                        padding: 30px;
                        max-width: 400px;
                        margin: 0 auto;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .no-gps-title {{
                        color: {theme_colors['warning']};
                        margin-top: 0;
                        font-size: 18px;
                    }}
                    .no-gps-message {{
                        color: {theme_colors['muted']};
                        margin: 15px 0;
                        font-size: 14px;
                    }}
                    .no-gps-hint {{
                        margin-top: 20px;
                        padding: 10px;
                        background: {theme_colors['secondary']};
                        border-radius: 5px;
                        font-size: 11px;
                    }}
                </style>
            </head>
            <body>
                <div class="no-gps-container">
                    <h3 class="no-gps-title">📍 GPS情報なし</h3>
                    <p class="no-gps-message">この画像にはGPS座標が含まれていません。</p>
                    <div class="no-gps-hint">
                        <small>位置情報付きの画像を選択してください</small>
                    </div>
                </div>
            </body>
            </html>
            """
            
            self.map_panel.view.setHtml(no_gps_html)  # type: ignore
            self.map_panel.view.update()  # type: ignore
            self.map_panel.view.repaint()  # type: ignore
            
            return True
            
        except Exception as e:
            logging.error(f"GPS無し HTML表示エラー: {e}")
            return False
    
    def _show_basic_gps_info(self, lat, lon, image_path):
        """基本的なGPS情報表示（フォールバック）"""
        try:
            if hasattr(self.map_panel, 'setText'):
                text = f"📍 GPS座標\n緯度: {lat:.6f}\n経度: {lon:.6f}\n画像: {os.path.basename(image_path)}"
                self.map_panel.setText(text)  # type: ignore
                return True
            return False
            
        except Exception as e:
            logging.error(f"基本GPS情報表示エラー: {e}")
            return False
    
    def _show_basic_no_gps_info(self):
        """基本的なGPS無し情報表示（フォールバック）"""
        try:
            if hasattr(self.map_panel, 'setText'):
                self.map_panel.setText("📍 GPS情報なし\nこの画像には位置情報が含まれていません")  # type: ignore
                return True
            return False
            
        except Exception as e:
            logging.error(f"基本GPS無し情報表示エラー: {e}")
            return False
    
    def _get_theme_colors(self):
        """現在のテーマ色を取得"""
        try:
            # テーママネージャーから色を取得
            if hasattr(self.main_window, 'theme_manager'):
                theme_manager = self.main_window.theme_manager
                if hasattr(theme_manager, 'get_current_theme'):
                    current_theme = theme_manager.get_current_theme()
                    if hasattr(current_theme, 'value') and current_theme.value == "DARK":
                        return self._get_dark_theme_colors()
            
            # デフォルトテーマ色
            return self._get_default_theme_colors()
            
        except Exception as e:
            logging.error(f"テーマ色取得エラー: {e}")
            return self._get_default_theme_colors()
    
    def _get_dark_theme_colors(self):
        """ダークテーマ色"""
        return {
            'background': '#2d2d2d',
            'foreground': '#ffffff',
            'panel_bg': '#3d3d3d',
            'accent': '#007ACC',
            'secondary': '#4d4d4d',
            'muted': '#cccccc',
            'warning': '#ff6b35'
        }
    
    def _get_default_theme_colors(self):
        """デフォルトテーマ色"""
        return {
            'background': '#ffffff',
            'foreground': '#000000',
            'panel_bg': '#f9f9f9',
            'accent': '#007ACC',
            'secondary': '#f0f0f0',
            'muted': '#666666',
            'warning': '#ff6b35'
        }
    
    def show_initial_screen(self):
        """初期画面を表示"""
        try:
            if hasattr(self.map_panel, 'view'):
                return self._show_initial_html()
            else:
                return self._show_basic_initial_info()
                
        except Exception as e:
            logging.error(f"初期画面表示エラー: {e}")
            return False
    
    def _show_initial_html(self):
        """初期画面のHTML表示"""
        try:
            theme_colors = self._get_theme_colors()
            
            initial_html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: Arial, sans-serif;
                        text-align: center;
                        padding: 50px;
                        margin: 0;
                        background-color: {theme_colors['background']};
                        color: {theme_colors['foreground']};
                    }}
                    .initial-container {{
                        background: {theme_colors['panel_bg']};
                        border: 2px solid {theme_colors['accent']};
                        border-radius: 10px;
                        padding: 30px;
                        max-width: 400px;
                        margin: 0 auto;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    .initial-title {{
                        color: {theme_colors['accent']};
                        margin-top: 0;
                        font-size: 18px;
                    }}
                    .initial-message {{
                        color: {theme_colors['muted']};
                        margin: 15px 0;
                        font-size: 14px;
                    }}
                    .initial-hint {{
                        margin-top: 20px;
                        padding: 10px;
                        background: {theme_colors['secondary']};
                        border-radius: 5px;
                        font-size: 11px;
                    }}
                </style>
            </head>
            <body>
                <div class="initial-container">
                    <h3 class="initial-title">🗺️ マップビュー</h3>
                    <p class="initial-message">GPS情報付きの画像を選択すると、ここに地図が表示されます。</p>
                    <div class="initial-hint">
                        <small>位置情報付きの画像を選択してください</small>
                    </div>
                </div>
            </body>
            </html>
            """
            
            self.map_panel.view.setHtml(initial_html)  # type: ignore
            self.map_panel.view.update()  # type: ignore
            self.map_panel.view.repaint()  # type: ignore
            
            return True
            
        except Exception as e:
            logging.error(f"初期HTML表示エラー: {e}")
            return False
    
    def _show_basic_initial_info(self):
        """基本的な初期情報表示（フォールバック）"""
        try:
            if hasattr(self.map_panel, 'setText'):
                self.map_panel.setText("🗺️ マップビュー\nGPS情報付きの画像を選択すると地図が表示されます")  # type: ignore
                return True
            return False
            
        except Exception as e:
            logging.error(f"基本初期情報表示エラー: {e}")
            return False
    
    def clear_map(self):
        """マップ表示をクリア"""
        try:
            self.current_location = None
            self.current_image = None
            
            # 初期画面を表示
            self.show_initial_screen()
            
        except Exception as e:
            logging.error(f"マップクリアエラー: {e}")
    
    def refresh_map(self):
        """現在の画像でマップを再表示"""
        try:
            if self.current_image:
                self.update_map(self.current_image)
                
        except Exception as e:
            logging.error(f"マップ再表示エラー: {e}")
    
    def get_current_location(self):
        """現在の位置情報を取得"""
        return self.current_location
    
    def has_gps_info(self):
        """GPS情報があるかどうか"""
        return self.current_location is not None
    
    def apply_theme(self, theme_name):
        """マップパネルにテーマを適用"""
        try:
            # 現在の画像で再表示（テーマが反映される）
            if self.current_image:
                self.refresh_map()
            else:
                self.show_initial_screen()
                
        except Exception as e:
            logging.error(f"マップテーマ適用エラー: {e}")
