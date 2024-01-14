from qmaterialwidgets import SmoothScrollArea
from qmaterialwidgets.components.widgets.scroll_area import SmoothScrollDelegate
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtCore import Qt


class NormalSmoothScrollArea(SmoothScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewport().setStyleSheet("background-color: transparent;")
        self.delegate = SmoothScrollDelegate(self, True)
        self.setFrameShape(QScrollArea.NoFrame)
        self.setAttribute(Qt.WA_StyledBackground)
