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

from PyQt5.QtWidgets import QSizePolicy, QVBoxLayout

from qmaterialwidgets import (
    BodyLabel,
    CardWidget,
    InfoBadge,
    SubtitleLabel,
    InfoLevel,
    InfoBar,
    InfoBarPosition,
)


class NodeWidget(CardWidget):
    def __init__(self, config, slot, parent=None):
        super().__init__(parent)
        self.setObjectName("NodeWidget")
        self.config = config
        self.clicked.connect(slot)
        self.setUpInterface()
        self.setUpData()

    def setUpInterface(self):
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedHeight(170)
        self.setMinimumWidth(320)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(12, 4, 0, 4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.regionLabel = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.regionLabel.sizePolicy().hasHeightForWidth())
        self.regionLabel.setSizePolicy(sizePolicy)
        self.regionLabel.setObjectName("regionLabel")
        self.verticalLayout.addWidget(self.regionLabel)
        self.bandwidthLabel = SubtitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bandwidthLabel.sizePolicy().hasHeightForWidth())
        self.bandwidthLabel.setSizePolicy(sizePolicy)
        self.bandwidthLabel.setObjectName("bandwidthLabel")
        self.verticalLayout.addWidget(self.bandwidthLabel)
        self.allowPortLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allowPortLabel.sizePolicy().hasHeightForWidth())
        self.allowPortLabel.setSizePolicy(sizePolicy)
        self.allowPortLabel.setObjectName("allowPortLabel")
        self.verticalLayout.addWidget(self.allowPortLabel)
        self.allowPortocolLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allowPortocolLabel.sizePolicy().hasHeightForWidth())
        self.allowPortocolLabel.setSizePolicy(sizePolicy)
        self.allowPortocolLabel.setObjectName("allowPortocolLabel")
        self.verticalLayout.addWidget(self.allowPortocolLabel)
        self.statusBadge = InfoBadge(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.statusBadge.sizePolicy().hasHeightForWidth())
        self.statusBadge.setSizePolicy(sizePolicy)
        self.statusBadge.setObjectName("statusBadge")
        self.verticalLayout.addWidget(self.statusBadge)

    def setUpData(self):
        self.setProperty("id", self.config["id"])
        self.setProperty("name", self.config["name"])
        self.setProperty("group", self.config["group"].split(";"))
        self.setProperty("allow_port", self.config["allow_port"][:-1].strip().split("-"))
        self.setProperty("allow_type", self.config["allow_type"][:-1].strip().split(";"))
        self.setProperty("status", self.config["status"])
        self.bandwidthLabel.setText(
            (bandwidth := self.property("name").replace(" 节点", "").split(" ")[-1])
        )
        self.regionLabel.setText(self.property("name").replace(" 节点", "").replace(bandwidth, ""))
        self.allowPortLabel.setText("端口范围 " + ("-".join(self.property("allow_port"))))
        self.allowPortocolLabel.setText("支持 " + (" | ".join(self.property("allow_type"))))
        self.statusBadge.setText(
            f"{self.property('status')} - "
            + ("正常" if self.property("status") == 200 else "服务器异常")
        )
        if self.property("status") == 200:
            self.statusBadge.setLevel(InfoLevel.SUCCESS)
        else:
            self.statusBadge.setLevel(InfoLevel.ERROR)
        if self.property("status") != 200:
            self.clicked.connect(
                lambda: InfoBar.warning(
                    title="提示",
                    content="此节点当前状态异常，不建议选择",
                    isClosable=True,
                    duration=1500,
                    position=InfoBarPosition.TOP,
                    parent=self.window(),
                )
            )
