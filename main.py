import sys
import os
from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QApplication
from presentation.views.functional_new_main_view import FunctionalNewMainWindow

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
    # Setup Qt environment
    setup_qt_environment()
    
    # Fix Qt WebEngine OpenGL context sharing warning
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    
    app = QApplication(sys.argv)
    window = FunctionalNewMainWindow()
    window.show()
    sys.exit(app.exec_())