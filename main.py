import sys
import os
import argparse
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication
from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow

def setup_qt_environment():
    """Qt環境の設定"""
    # Get virtual environment path
    venv_path = os.path.dirname(os.path.dirname(sys.executable))
    
    # Set Qt platform plugin path
    plugin_path = os.path.join(venv_path, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    
    # Set QtWebEngine process path
    qt5_bin_path = os.path.join(venv_path, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'bin')
    if os.path.exists(qt5_bin_path):
        current_path = os.environ.get('PATH', '')
        os.environ['PATH'] = qt5_bin_path + os.pathsep + current_path
    
    # Set QtWebEngine resources path
    qt5_resources_path = os.path.join(venv_path, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'resources')
    if os.path.exists(qt5_resources_path):
        os.environ['QTWEBENGINE_RESOURCES_PATH'] = qt5_resources_path
    
    # Set QtWebEngine locales path
    qt5_locales_path = os.path.join(venv_path, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'translations', 'qtwebengine_locales')
    if os.path.exists(qt5_locales_path):
        os.environ['QTWEBENGINE_LOCALES_PATH'] = qt5_locales_path

if __name__ == "__main__":
    # デバッグオプションの処理
    import argparse
    parser = argparse.ArgumentParser(description='PhotoMap Explorer v2.2.0')
    parser.add_argument('--debug', action='store_true', help='デバッグモードで実行')
    args = parser.parse_args()
    
    # デバッグモード設定
    if args.debug:
        import logging
        from utils.debug_logger import set_debug_mode, debug, info
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        set_debug_mode(True)
        debug("デバッグモードで起動中...")
    
    # Setup Qt environment
    setup_qt_environment()
    
    # Fix Qt WebEngine OpenGL context sharing warning
    QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    
    app = QApplication(sys.argv)
    window = RefactoredFunctionalMainWindow()
    
    # フォルダ選択機能を追加
    def add_folder_selection_button():
        """フォルダ選択ボタンをメインウィンドウに追加"""
        from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
        
        def select_folder():
            folder_path = QFileDialog.getExistingDirectory(window, "📁 画像フォルダを選択", os.path.expanduser("~"))
            if folder_path and hasattr(window, 'left_panel_manager') and window.left_panel_manager:
                # フォルダ内容を更新
                window.left_panel_manager.update_folder_content(folder_path)
                
                # サムネイル更新
                image_files = window.left_panel_manager._get_image_files_from_folder(folder_path)
                window.left_panel_manager.update_thumbnails(image_files)
                
                # アドレスバー更新
                if hasattr(window, 'address_bar_manager') and window.address_bar_manager:
                    if hasattr(window.address_bar_manager, 'set_path'):
                        window.address_bar_manager.set_path(folder_path)
                    elif hasattr(window.address_bar_manager, 'address_bar'):
                        window.address_bar_manager.address_bar.setText(folder_path)
        
        # ボタンを作成
        folder_btn = QPushButton("📁 フォルダ選択")
        folder_btn.setToolTip("画像が含まれているフォルダを選択してください")
        folder_btn.clicked.connect(select_folder)
        
        # ツールバーに追加（ツールバーがある場合）
        if hasattr(window, 'toolbar') and window.toolbar:
            window.toolbar.addWidget(folder_btn)
        else:
            # ツールバーがない場合は、ウィンドウ上部に配置
            folder_btn.setParent(window)
            folder_btn.setGeometry(10, 10, 120, 30)
            folder_btn.show()
    
    # ウィンドウ表示後にボタンを追加
    from PyQt5.QtCore import QTimer
    QTimer.singleShot(100, add_folder_selection_button)
    
    if args.debug:
        from utils.debug_logger import debug, info, verbose
        
        info("メインウィンドウの状態:")
        verbose(f"ウィンドウタイトル: {window.windowTitle()}")
        verbose(f"ウィンドウサイズ: {window.size()}")
        verbose(f"現在のフォルダ: {window.current_folder}")
        
        debug("管理クラス状態:")
        verbose(f"left_panel_manager: {window.left_panel_manager is not None}")
        verbose(f"right_panel_manager: {window.right_panel_manager is not None}")
        verbose(f"address_bar_manager: {window.address_bar_manager is not None}")
        verbose(f"theme_event_handler: {window.theme_event_handler is not None}")
        
        # 追加詳細情報
        debug("UIコンポーネント状態:")
        if hasattr(window, 'main_splitter'):
            verbose(f"main_splitter: {window.main_splitter is not None}")
            if window.main_splitter:
                verbose(f"main_splitter子要素数: {window.main_splitter.count()}")
                # 各子要素の詳細
                for i in range(window.main_splitter.count()):
                    widget = window.main_splitter.widget(i)
                    verbose(f"子要素{i}: {type(widget).__name__}")
        
        if hasattr(window, 'folder_content_list'):
            verbose(f"folder_content_list: {window.folder_content_list is not None}")
        if hasattr(window, 'thumbnail_list'):
            verbose(f"thumbnail_list: {window.thumbnail_list is not None}")
        if hasattr(window, 'preview_panel'):
            verbose(f"preview_panel: {window.preview_panel is not None}")
        if hasattr(window, 'map_panel'):
            verbose(f"map_panel: {window.map_panel is not None}")
            
        # スプリッターの詳細
        if hasattr(window, 'right_splitter'):
            verbose(f"right_splitter: {window.right_splitter is not None}")
            if window.right_splitter:
                verbose(f"right_splitter子要素数: {window.right_splitter.count()}")
                
        # 管理クラスの詳細状態
        debug("パネル作成状態:")
        if window.left_panel_manager:
            verbose(f"left_panel_manager.panel: {window.left_panel_manager.panel is not None}")
        if window.right_panel_manager:
            verbose(f"right_panel_manager.panel: {window.right_panel_manager.panel is not None}")
            verbose(f"right_panel_manager.right_splitter: {window.right_panel_manager.right_splitter is not None}")
    
    window.show()
    
    # ウィンドウ表示後に強制的にパネルを再表示
    if args.debug:
        from utils.debug_logger import debug, info
        import time
        time.sleep(0.1)  # 少し待つ
        app.processEvents()  # イベント処理
        
        debug("ウィンドウ表示後の状態確認...")
        debug(f"ウィンドウ表示後の可視性: {window.isVisible()}")
        
        if hasattr(window, 'main_splitter') and window.main_splitter:
            debug(f"ウィンドウ表示後メインスプリッター可視性: {window.main_splitter.isVisible()}")
            window.main_splitter.show()  # 再度強制表示
            debug(f"再強制表示後メインスプリッター可視性: {window.main_splitter.isVisible()}")
            
            for i in range(window.main_splitter.count()):
                widget = window.main_splitter.widget(i)
                if widget:
                    debug(f"ウィンドウ表示後子ウィジェット{i}可視性: {widget.isVisible()}")
                    widget.show()  # 子ウィジェットも強制表示
                    debug(f"再強制表示後子ウィジェット{i}可視性: {widget.isVisible()}")
        
        # 右パネルの個別確認
        if hasattr(window, 'right_panel_manager') and window.right_panel_manager:
            if hasattr(window.right_panel_manager, 'panel'):
                debug(f"ウィンドウ表示後右パネル可視性: {window.right_panel_manager.panel.isVisible()}")
                window.right_panel_manager.panel.show()
                debug(f"再強制表示後右パネル可視性: {window.right_panel_manager.panel.isVisible()}")
            
            if hasattr(window.right_panel_manager, 'right_splitter'):
                debug(f"ウィンドウ表示後右スプリッター可視性: {window.right_panel_manager.right_splitter.isVisible()}")
                window.right_panel_manager.right_splitter.show()
                debug(f"再強制表示後右スプリッター可視性: {window.right_panel_manager.right_splitter.isVisible()}")
    
    sys.exit(app.exec_())