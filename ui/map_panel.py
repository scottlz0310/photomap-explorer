from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import os
from utils.debug_logger import debug, info, warning, error, verbose


class MapPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.view = None
        self.setup_view()
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)
    
    def setup_view(self):
        """マップビューのセットアップ（フォールバック対応）"""
        try:
            # 最初にQtWebEngineベースを試行
            info("QtWebEngineベースの地図ビューを試行中...")
            from ui.map_view import create_map_view
            self.view = create_map_view()
            self.view.setMinimumHeight(250)  # 最小高さを確保
            self.view.setMinimumWidth(300)   # 最小幅を確保
            
            # QtWebEngineViewの追加設定
            if hasattr(self.view, 'setVisible'):
                self.view.setVisible(True)
            if hasattr(self.view, 'show'):
                self.view.show()
            if hasattr(self.view, 'setAttribute'):
                # Qt.WA_AlwaysShowToolTipsを設定（可視性向上）
                from PyQt5.QtCore import Qt
                self.view.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)
            
            self.use_webengine = True
            info("✅ QtWebEngineベースの地図ビュー作成成功")
        except Exception as e:
            # QtWebEngineが利用できない場合はシンプルビューを使用
            warning(f"QtWebEngine利用不可、シンプルビューを使用: {e}")
            try:
                from ui.simple_map_view import create_simple_map_view
                self.view = create_simple_map_view()
                self.view.setMinimumHeight(250)
                self.view.setMinimumWidth(300)
                self.use_webengine = False
                info("✅ シンプル地図ビュー作成成功")
            except Exception as simple_e:
                error(f"シンプル地図ビューの作成にも失敗: {simple_e}")
                # 最後の手段として基本ウィジェット
                self.view = QLabel("🗺️ 地図ビューの初期化に失敗しました")
                self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.view.setMinimumHeight(250)
                self.view.setMinimumWidth(300)
                self.use_webengine = False

    def load_map(self, map_file):
        """地図ファイルを読み込み"""
        if self.use_webengine and hasattr(self.view, 'load') and self.view:
            debug(f"地図ファイルを読み込み: {map_file}")
            
            # ファイル存在確認
            if not os.path.exists(map_file):
                error(f"地図ファイルが存在しません: {map_file}")
                return False
            
            # ファイルサイズ確認
            file_size = os.path.getsize(map_file)
            info(f"地図ファイルサイズ: {file_size} bytes")
            
            if file_size < 1000:
                warning(f"地図ファイルが小さすぎます: {file_size} bytes")
                return False
            
            # 絶対パスでURLを作成
            abs_path = os.path.abspath(map_file)
            file_url = QUrl.fromLocalFile(abs_path)
            info(f"地図URL: {file_url.toString()}")
            
            # ロード実行
            try:
                info("🔍 QtWebEngineView地図ロード処理開始")
                # QtWebEngineViewのloadFinishedシグナルに接続
                def on_load_finished(success):
                    try:
                        info(f"🔍 地図ロード完了: success={success}")
                        if success:
                            # レンダリング完了後の強制表示処理
                            if self.view and hasattr(self.view, 'show'):
                                self.view.show()
                                info("🔍 地図ビュー再表示完了")
                            if self.view and hasattr(self.view, 'setVisible'):
                                self.view.setVisible(True)
                                info("🔍 地図ビュー可視化完了")
                            if self.view and hasattr(self.view, 'update'):
                                self.view.update()
                                info("🔍 地図ビュー更新完了")
                            
                            # さらに500ms後に追加の強制表示
                            from PyQt5.QtCore import QTimer
                            def final_force_show():
                                try:
                                    if self.view:
                                        if hasattr(self.view, 'raise_'):
                                            self.view.raise_()
                                        if hasattr(self.view, 'activateWindow'):
                                            self.view.activateWindow()
                                        if hasattr(self.view, 'repaint'):
                                            self.view.repaint()
                                        info("🔍 地図最終強制表示完了")
                                except Exception as e:
                                    warning(f"地図最終強制表示エラー: {e}")
                            
                            QTimer.singleShot(500, final_force_show)
                        else:
                            error("🔍 地図ロード失敗")
                    except Exception as e:
                        error(f"地図ロード完了処理エラー: {e}")
                
                # loadFinishedシグナルに接続
                info("🔍 loadFinishedシグナル接続処理開始")
                try:
                    if hasattr(self.view, 'loadFinished'):
                        info("🔍 loadFinishedシグナル存在確認成功")
                        self.view.loadFinished.connect(on_load_finished)
                        info("🔍 loadFinishedシグナル接続完了")
                    else:
                        error("🔍 QtWebEngineView.loadFinishedシグナルが存在しません")
                        return False
                except Exception as e:
                    error(f"🔍 loadFinishedシグナル接続エラー: {e}")
                    error(f"🔍 エラータイプ: {type(e)}")
                    import traceback
                    error(f"🔍 スタックトレース: {traceback.format_exc()}")
                    return False
                
                info("🔍 QtWebEngineView.load()実行開始チェック")
                info(f"🔍 QtWebEngineView.load()実行直前: URL={file_url.toString()}")
                info(f"🔍 self.view型: {type(self.view)}")
                info(f"🔍 self.viewアドレス: {id(self.view)}")
                info(f"🔍 self.view存在確認: {self.view is not None}")
                
                try:
                    if hasattr(self.view, 'load'):
                        info("🔍 QtWebEngineView.load()メソッド存在確認成功")
                        self.view.load(file_url)
                        info("🔍 QtWebEngineView.load()呼び出し直後")
                    else:
                        error("🔍 QtWebEngineView.load()メソッドが存在しません")
                        return False
                except Exception as e:
                    error(f"🔍 QtWebEngineView.load()実行エラー: {e}")
                    error(f"🔍 load実行エラータイプ: {type(e)}")
                    import traceback
                    error(f"🔍 load実行スタックトレース: {traceback.format_exc()}")
                    return False
                
                info("✅ 地図ファイル読み込み完了")
                info("🔍 QtWebEngineView.load()実行完了")
                
                # 地図表示後に強制的にサイズ更新とリフレッシュ
                from PyQt5.QtCore import QTimer
                from PyQt5.QtWidgets import QWidget
                def delayed_update():
                    try:
                        if self.view and hasattr(self.view, 'show'):
                            self.view.show()
                        if self.view and hasattr(self.view, 'update'):
                            self.view.update()
                        
                        # 親ウィジェットも強制表示（安全な型チェック）
                        if self.view and hasattr(self.view, 'parent'):
                            parent = self.view.parent()
                            while parent:
                                if isinstance(parent, QWidget):
                                    parent.show()
                                    parent.update()
                                parent = parent.parent() if hasattr(parent, 'parent') else None
                        info("🔍 地図表示強制更新完了")
                    except Exception as e:
                        warning(f"地図強制更新エラー: {e}")
                
                # 100ms後に強制更新実行
                QTimer.singleShot(100, delayed_update)
                return True
            except Exception as e:
                error(f"地図ファイル読み込みエラー: {e}")
                return False
        else:
            warning("WebEngineが利用できないか、Viewが存在しません")
            return False
    
    def update_location(self, latitude, longitude):
        """
        指定された緯度・経度で地図を更新
        
        Args:
            latitude (float): 緯度
            longitude (float): 経度
            
        Returns:
            bool: 成功した場合True
        """
        try:
            if self.use_webengine:
                # QtWebEngineベースの処理
                from logic.image_utils import generate_map_html
                
                # 地図HTMLファイルを生成
                map_file = generate_map_html(latitude, longitude)
                
                # 地図を読み込み
                if os.path.exists(map_file):
                    self.load_map(map_file)
                    return True
                else:
                    self._show_error_message("地図ファイルの生成に失敗しました")
                    return False
            else:
                # シンプルビューの処理
                if hasattr(self.view, 'update_location') and self.view:
                    debug(f"シンプルビューで位置更新: 緯度={latitude}, 経度={longitude}")
                    return self.view.update_location(latitude, longitude)
                else:
                    warning("シンプルビューにupdate_locationメソッドがありません")
                    return False
                    
        except Exception as e:
            self._show_error_message(f"地図更新エラー: {str(e)}")
            return False
    
    def _show_error_message(self, message):
        """エラーメッセージを表示"""
        error(f"地図エラー: {message}")
        if self.use_webengine and hasattr(self.view, 'setHtml') and self.view:
            error_html = f"""
            <html>
            <body style="background-color: #f8f8f8; font-family: Arial, sans-serif; padding: 20px;">
                <div style="color: #d32f2f; font-size: 14px;">
                    <strong>🚨 地図表示エラー</strong><br>
                    {message}
                </div>
            </body>
            </html>
            """
            self.view.setHtml(error_html)
        elif hasattr(self.view, 'show_error') and self.view:
            self.view.show_error(message)
        else:
            warning(f"エラーメッセージの表示に失敗: {message}")
    
    def show_no_gps_message(self):
        """GPS情報がない場合のメッセージを表示"""
        info("GPS情報がない場合のメッセージを表示")
        if self.use_webengine and hasattr(self.view, 'setHtml') and self.view:
            no_gps_html = """
            <html>
            <body style="background-color: #f5f5f5; font-family: Arial, sans-serif; padding: 20px; text-align: center;">
                <div style="color: #666; font-size: 16px;">
                    <strong>📍 GPS情報がありません</strong><br><br>
                    この画像にはGPS位置情報が含まれていません。<br>
                    GPS付きカメラやスマートフォンで撮影された画像を選択してください。
                </div>
            </body>
            </html>
            """
            self.view.setHtml(no_gps_html)
        elif hasattr(self.view, 'show_no_gps') and self.view:
            self.view.show_no_gps()
        else:
            warning("GPS情報なしメッセージの表示に失敗")


def create_map_panel():
    """マップパネルを作成して返す関数"""
    return MapPanel()
