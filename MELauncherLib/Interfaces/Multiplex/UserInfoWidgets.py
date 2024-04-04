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

from PyQt5.QtWidgets import QWidget, QSizePolicy, QHBoxLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap
from qmaterialwidgets import BodyLabel, ImageLabel, StrongBodyLabel
from ...Resources import *  # noqa: F403 F401


class UserInfoWidget(QWidget):
    def __init__(self, typeName, value, parent=None):
        super().__init__(parent)
        self.setObjectName("UserInfoWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(0, 30))
        self.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.titleLabel = StrongBodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
        self.titleLabel.setSizePolicy(sizePolicy)
        self.titleLabel.setObjectName("titleLabel")
        self.horizontalLayout.addWidget(self.titleLabel)
        self.valueLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.valueLabel.sizePolicy().hasHeightForWidth())
        self.valueLabel.setSizePolicy(sizePolicy)
        self.valueLabel.setObjectName("valueLabel")
        self.horizontalLayout.addWidget(self.valueLabel)
        self.horizontalLayout.setContentsMargins(9, 1, 9, 1)
        self.titleLabel.setText(typeName)
        self.valueLabel.setText(value)


class UserInfoAvatarWidget(QWidget):
    def __init__(self, username: str, parent=None):
        super().__init__(parent)
        self.setObjectName("UserInfoWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(0, 60))
        self.setMaximumSize(QSize(16777215, 60))
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.userAvatar = ImageLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userAvatar.sizePolicy().hasHeightForWidth())
        self.userAvatar.setSizePolicy(sizePolicy)
        self.userAvatar.setMinimumSize(QSize(55, 55))
        self.userAvatar.setMaximumSize(QSize(55, 55))
        self.userAvatar.setObjectName("userAvatar")
        self.horizontalLayout.addWidget(self.userAvatar)
        self.userName = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userName.sizePolicy().hasHeightForWidth())
        self.userName.setSizePolicy(sizePolicy)
        self.userName.setText(f"  {username}")
        self.userName.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.userName.setObjectName("userName")
        self.horizontalLayout.addWidget(self.userName)
        self.userAvatar.setPixmap(QPixmap(":/built-InIcons/user.png"))
        self.userAvatar.setFixedSize(QSize(52, 52))
        self.horizontalLayout.setContentsMargins(9, 1, 9, 1)


# class UserInfoPushWidget(QWidget):
#     def __init__(self, type: str, action, slot, parent=None):
#         super().__init__(parent)
#         self.setObjectName("UserInfoWidget")
#         sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
#         self.setSizePolicy(sizePolicy)
#         self.setMinimumSize(QSize(0, 40))
#         self.setMaximumSize(QSize(16777215, 40))
#         self.horizontalLayout = QHBoxLayout(self)
#         self.horizontalLayout.setObjectName("horizontalLayout")
#         self.titleLabel = StrongBodyLabel(self)
#         sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.titleLabel.sizePolicy().hasHeightForWidth())
#         self.titleLabel.setSizePolicy(sizePolicy)
#         self.titleLabel.setObjectName("titleLabel")
#         self.horizontalLayout.addWidget(self.titleLabel)
#         self.actionBtn = TonalPushButton(self)
#         sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#         sizePolicy.setHorizontalStretch(0)
#         sizePolicy.setVerticalStretch(0)
#         sizePolicy.setHeightForWidth(self.actionBtn.sizePolicy().hasHeightForWidth())
#         self.actionBtn.setSizePolicy(sizePolicy)
#         self.actionBtn.setObjectName("actionBtn")
#         self.horizontalLayout.addWidget(self.actionBtn)
#         self.horizontalLayout.setContentsMargins(9, 1, 9, 1)
#         self.titleLabel.setText(type)
#         self.actionBtn.setText(action)
#         self.actionBtn.clicked.connect(slot)
