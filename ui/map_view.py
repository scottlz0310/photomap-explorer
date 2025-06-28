from PyQt5.QtWebEngineWidgets import QWebEngineView

def create_map_view():
    """地図ビューを作成して初期化する関数"""
    map_view = QWebEngineView()
    # 初期表示内容を設定
    initial_html = """
    <html>
    <head>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px; 
                background-color: #f5f5f5; 
                margin: 0;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                max-width: 400px;
                margin: 0 auto;
            }
            h3 { color: #333; margin-bottom: 10px; }
            p { color: #666; font-size: 14px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h3>🗺️ マップビュー</h3>
            <p>GPS情報付きの画像を選択すると、ここに地図が表示されます。</p>
        </div>
    </body>
    </html>
    """
    map_view.setHtml(initial_html)
    map_view.setMinimumSize(400, 400)

    return map_view
