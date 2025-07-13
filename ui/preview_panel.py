from ui.image_preview import ImagePreviewView
from utils.debug_logger import debug, info, warning, error, verbose

class PreviewPanel(ImagePreviewView):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(200)
