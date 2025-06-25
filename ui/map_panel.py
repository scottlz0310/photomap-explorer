from ui.map_view import create_map_view
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class MapPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.view = create_map_view()
        self.view.setMinimumHeight(200)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

    def load_map(self, map_file):
        self.view.load(QUrl.fromLocalFile(map_file))
