from ui.image_preview import ImagePreviewView

class PreviewPanel(ImagePreviewView):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(200)
