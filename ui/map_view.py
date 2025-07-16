from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer
from utils.debug_logger import info, error, debug

def create_map_view():
    """地図ビューを作成して初期化する関数"""
    map_view = QWebEngineView()
    
    # QtWebEngineViewの強制表示設定
    map_view.setVisible(True)
    map_view.show()
    
    # ロード完了イベントを処理
    def on_load_finished(success):
        if success:
            info("🔍 ✅ QtWebEngineView地図読み込み成功")
            # ロード完了後に再度表示強制
            map_view.show()
            map_view.setVisible(True)
            map_view.update()
            map_view.repaint()
            # 親ウィジェットも強制表示
            parent = map_view.parent()
            if parent and hasattr(parent, 'show'):
                parent.show()
                parent.setVisible(True)
                parent.update()
                info(f"🔍 親ウィジェットも強制表示: {type(parent).__name__}")
            info("🔍 QtWebEngineView表示強制完了")
        else:
            error("🔍 ❌ QtWebEngineView地図読み込み失敗")
    
    # ロード開始イベントを処理
    def on_load_started():
        info("� �🔄 QtWebEngineView地図読み込み開始")
        # ロード開始時にも表示確保
        map_view.show()
        map_view.setVisible(True)
    
    # ロード進捗イベントを処理
    def on_load_progress(progress):
        debug(f"🔍 📊 QtWebEngineView読み込み進捗: {progress}%")
    
    # ページタイトル変更イベントを処理
    def on_title_changed(title):
        info(f"🔍 📄 QtWebEngineViewタイトル変更: {title}")
    
    # URL変更イベントを処理
    def on_url_changed(url):
        info(f"🔍 🔗 QtWebEngineView URL変更: {url.toString()}")
    
    # イベント接続
    map_view.loadFinished.connect(on_load_finished)
    map_view.loadStarted.connect(on_load_started)
    map_view.loadProgress.connect(on_load_progress)
    map_view.titleChanged.connect(on_title_changed)
    map_view.urlChanged.connect(on_url_changed)
    
    info("🔍 QtWebEngineViewイベントハンドラー設定完了")
    
    # 初期表示内容を設定
    initial_html = """
    <html>
    <head>
        <style>
            body { 
                text-align: center; 
                padding: 50px; 
                font-family: Arial;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }
            .message { 
                font-size: 24px; 
                margin-bottom: 20px; 
                text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            }
            .subtitle { 
                color: #ddd; 
                font-size: 14px; 
            }
        </style>
    </head>
    <body>
        <div class="message">🗺️ 地図ビュー初期化完了</div>
        <div class="subtitle">GPS付きの画像を選択してください</div>
        <div class="subtitle">QtWebEngineView動作中...</div>
    </body>
    </html>
    """
    map_view.setHtml(initial_html)
    info("🔍 QtWebEngineView初期HTML設定完了")
    
    # 遅延初期化でより確実な表示
    def delayed_initialization():
        map_view.show()
        map_view.setVisible(True)
        map_view.update()
        map_view.repaint()
        info(f"🔍 遅延初期化完了: size={map_view.size()}, visible={map_view.isVisible()}")
    
    # 100ms後に遅延初期化を実行
    QTimer.singleShot(100, delayed_initialization)
    
    # QtWebEngineViewの強制初期化
    map_view.setMinimumSize(400, 400)
    map_view.resize(400, 400)
    
    # 初期表示の確実な実行
    map_view.show()
    map_view.setVisible(True)
    map_view.update()
    map_view.repaint()
    
    info(f"🔍 QtWebEngineView最終設定完了: size={map_view.size()}, visible={map_view.isVisible()}")

    return map_view
