#                    Copyright 2024, LxHTT and Aehxy.
#
#     Part of "MEFrp-Launcher-Qt", a frpc launcher for ME Frp.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/LxHTT/MEFrp-Launcher-Qt/raw/master/LICENSE
#
################################################################################

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
