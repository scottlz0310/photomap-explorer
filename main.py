import sys
import os
import logging
from PyQt5.QtCore import Qt, QCoreApplication, qInstallMessageHandler, QLoggingCategory
from PyQt5.QtWidgets import QApplication
from presentation.views.functional_main_window.refactored_main_window import RefactoredFunctionalMainWindow
from utils.debug_logger import set_level_from_args, debug, info, warning, error, verbose

# Qtのログメッセージハンドラー
def qt_message_handler(mode, context, message):
    """Qtのログメッセージを制御"""
    if '--debug' in sys.argv:
        # デバッグモードの場合はQtメッセージも表示
        print(f"[Qt] {message}")
    # それ以外の場合は無視（静音）

def filter_python_output():
    """Python標準出力のフィルタリング設定"""
    # デバッグモードでない場合、特定のライブラリ警告を抑制
    if '--debug' not in sys.argv:
        import warnings
        
        # 標準的な警告を抑制
        warnings.filterwarnings("ignore", category=UserWarning)
        warnings.filterwarnings("ignore", message=".*libpng warning.*")
        warnings.filterwarnings("ignore", message=".*PNG file does not have exif.*")
        warnings.filterwarnings("ignore", category=FutureWarning)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        
        # C拡張からのlibpng警告を環境変数で抑制
        os.environ['PYTHONWARNINGS'] = 'ignore'
        
        # より強力な標準出力フィルタリング
        class OutputFilter:
            def __init__(self, stream):
                self.stream = stream
                
            def write(self, message):
                # 特定のメッセージをフィルタ
                if any(phrase in message for phrase in [
                    'PNG file does not have exif',
                    'libpng warning',
                    'iCCP: known incorrect sRGB profile'
                ]):
                    return  # 出力しない
                self.stream.write(message)
                
            def flush(self):
                self.stream.flush()
        
        # 標準出力と標準エラー出力にフィルタを適用
        sys.stdout = OutputFilter(sys.stdout)
        sys.stderr = OutputFilter(sys.stderr)

def print_help():
    """ヘルプメッセージを表示"""
    print("""
PhotoMap Explorer v2.2.0

使用法:
    python main.py [オプション]

オプション:
    --help, -h        このヘルプメッセージを表示
    --debug           全てのデバッグ情報を表示（Qtメッセージ含む）
    --verbose, -v     詳細な情報を表示（成功メッセージ含む）
    --normal          基本的な情報を表示（警告・エラー）
    --quiet, --silent エラーのみ表示（デフォルト）

説明:
    GPS情報付き画像から撮影地点を地図上に表示するアプリケーションです。
    EXIF情報の詳細表示、ダーク/ライトテーマの切り替え、
    直感的なフォルダナビゲーション機能を提供します。
    
    デフォルトでは完全に静音モードで起動し、エラー以外は出力しません。
""")
    sys.exit(0)

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
    # ヘルプオプションの確認
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
    
    # Python出力フィルタリングを設定
    filter_python_output()
    
    # コマンドライン引数からログレベルを設定
    set_level_from_args()
    
    # Python標準出力のフィルタリング設定
    filter_python_output()
    
    # Qtのログメッセージハンドラーを設定（デバッグモード以外では静音）
    qInstallMessageHandler(qt_message_handler)
    
    # Setup Qt environment
    setup_qt_environment()
    
    # Fix Qt WebEngine OpenGL context sharing warning
    try:
        QCoreApplication.setAttribute(Qt.ApplicationAttribute.AA_ShareOpenGLContexts)
    except AttributeError:
        # 古いバージョンのPyQt5では利用できない場合があります
        debug("Qt AA_ShareOpenGLContexts 属性が利用できません（古いバージョン）")
    
    debug("PhotoMap Explorer v2.2.0 を起動中...")
    app = QApplication(sys.argv)
    
    # アプリケーションの追加設定
    app.setApplicationName("PhotoMap Explorer")
    app.setApplicationVersion("2.2.0")
    app.setOrganizationName("PhotoMap")
    
    window = RefactoredFunctionalMainWindow()
    verbose("メインウィンドウを作成しました")
    
    window.show()
    verbose("PhotoMap Explorer が起動しました")
    
    sys.exit(app.exec_())