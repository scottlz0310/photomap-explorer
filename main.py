import sys
import os
import argparse
import logging
from pathlib import Path
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication
from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow

def setup_logging(debug=False, verbose=False):
    """
    ログレベルを設定
    
    Args:
        debug (bool): --debug フラグ（DEBUG以上のログを出力）
        verbose (bool): --verbose フラグ（INFO以上のログを出力）
    """
    # ログレベル決定
    if debug:
        level = logging.DEBUG
    elif verbose:
        level = logging.INFO
    else:
        level = logging.WARNING
    
    # logsディレクトリの作成
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    # ログファイル名（日付付き）
    from datetime import datetime
    log_filename = f"photomap_explorer_{datetime.now().strftime('%Y%m%d')}.log"
    log_filepath = log_dir / log_filename
    
    # ロガーの設定
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filepath, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    # アプリケーション開始ログ
    logger = logging.getLogger(__name__)
    logger.info(f"PhotoMap Explorer 開始 - ログレベル: {logging.getLevelName(level)}")
    
    return logger

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
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='PhotoMap Explorer - 写真とGPS位置のマッピングツール')
    parser.add_argument('--debug', action='store_true', help='デバッグモード（DEBUG以上のログを出力）')
    parser.add_argument('--verbose', action='store_true', help='詳細モード（INFO以上のログを出力）')
    
    args = parser.parse_args()
    
    # ログの設定
    logger = setup_logging(args.debug, args.verbose)
    
    try:
        # Setup Qt environment
        setup_qt_environment()
        
        # Fix Qt WebEngine OpenGL context sharing warning
        QApplication.setAttribute(Qt.ApplicationAttribute(13))  # Qt.AA_ShareOpenGLContexts
        
        logger.debug("Qt環境設定完了")
        
        app = QApplication(sys.argv)
        logger.info("QApplicationインスタンス作成完了")
        
        window = RefactoredFunctionalMainWindow()
        logger.info("メインウィンドウ作成完了")
        
        window.show()
        logger.info("メインウィンドウ表示完了")
        
        sys.exit(app.exec_())
        
    except Exception as e:
        logger.error(f"アプリケーション実行中にエラーが発生: {e}", exc_info=True)
        sys.exit(1)