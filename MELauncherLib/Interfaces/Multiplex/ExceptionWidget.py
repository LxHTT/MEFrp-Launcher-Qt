#                    Copyright 2024, LxHTT.
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

from PyQt5.QtCore import QRect, Qt, QSize
from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout, QWidget, QFrame
from qmaterialwidgets import BodyLabel

from MELauncherLib.Interfaces.Multiplex.ScollArea import NormalSmoothScrollArea


class ExceptionWidget(QWidget):
    def __init__(self, traceStr):
        super().__init__()
        self.exceptionScrollArea = NormalSmoothScrollArea(self)
        self.exceptionScrollArea.setGeometry(QRect(50, 10, 480, 150))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exceptionScrollArea.sizePolicy().hasHeightForWidth())
        self.exceptionScrollArea.setSizePolicy(sizePolicy)
        self.exceptionScrollArea.setMinimumSize(QSize(480, 0))
        self.exceptionScrollArea.setMaximumSize(QSize(480, 320))
        self.exceptionScrollArea.setFrameShape(QFrame.NoFrame)
        self.exceptionScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.exceptionScrollArea.setWidgetResizable(True)
        self.exceptionScrollAreaWidgetContents = QWidget()
        self.exceptionScrollAreaWidgetContents.setGeometry(QRect(0, 0, 468, 320))
        self.exceptionLayout = QVBoxLayout(self.exceptionScrollAreaWidgetContents)
        self.exceptionLayout.setContentsMargins(0, 0, 0, 0)
        self.exceptionLabel = BodyLabel(self.exceptionScrollAreaWidgetContents)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exceptionLabel.sizePolicy().hasHeightForWidth())
        self.exceptionLabel.setSizePolicy(sizePolicy)
        self.exceptionLabel.setMinimumSize(QSize(450, 200))
        self.exceptionLabel.setMaximumSize(QSize(450, 16777215))
        self.exceptionLabel.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.exceptionLabel.setWordWrap(True)
        self.exceptionLayout.addWidget(self.exceptionLabel)
        self.exceptionScrollArea.setWidget(self.exceptionScrollAreaWidgetContents)
        self.exceptionLabel.setText(traceStr)
