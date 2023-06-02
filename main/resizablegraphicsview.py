from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt

class ResizableGraphicsView(QGraphicsView):
    def resizeEvent(self, event):
        self.fitInView(self.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)