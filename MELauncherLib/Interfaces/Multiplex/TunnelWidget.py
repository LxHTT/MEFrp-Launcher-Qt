from PyQt5.QtWidgets import QVBoxLayout, QSizePolicy, QHBoxLayout, QWidget, QApplication
from PyQt5.QtCore import QSize
from qmaterialwidgets import (
    BodyLabel,
    CardWidget,
    SubtitleLabel,
    SwitchButton,
    TonalPushButton,
    FluentIcon as FIF,
)
from ...AppController.Utils import splitNodeName


class TunnelWidget(CardWidget):
    def __init__(self, config, editBtnSlot, delBtnSlot, parent=None):
        self.config = config
        self.editBtnSlot = editBtnSlot
        self.delBtnSlot = delBtnSlot
        super().__init__(parent)
        self.setObjectName("TunnelWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setFixedSize(QSize(315, 180))
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(13, 5, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.titleWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.titleWidget.sizePolicy().hasHeightForWidth())
        self.titleWidget.setSizePolicy(sizePolicy)
        self.titleWidget.setObjectName("titleWidget")
        self.titleLayout = QHBoxLayout(self.titleWidget)
        self.titleLayout.setContentsMargins(0, 0, 10, 0)
        self.titleLayout.setSpacing(0)
        self.titleLayout.setObjectName("titleLayout")
        self.tunnelNameLabel = SubtitleLabel(self.titleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunnelNameLabel.sizePolicy().hasHeightForWidth())
        self.tunnelNameLabel.setSizePolicy(sizePolicy)
        self.tunnelNameLabel.setObjectName("tunnelNameLabel")
        self.titleLayout.addWidget(self.tunnelNameLabel)
        self.runFrpcBtn = SwitchButton(self.titleWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runFrpcBtn.sizePolicy().hasHeightForWidth())
        self.runFrpcBtn.setSizePolicy(sizePolicy)
        self.runFrpcBtn.setObjectName("runFrpcBtn")
        self.titleLayout.addWidget(self.runFrpcBtn)
        self.verticalLayout.addWidget(self.titleWidget)
        self.nodeNameLabel = BodyLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nodeNameLabel.sizePolicy().hasHeightForWidth())
        self.nodeNameLabel.setSizePolicy(sizePolicy)
        self.nodeNameLabel.setObjectName("nodeNameLabel")
        self.verticalLayout.addWidget(self.nodeNameLabel)
        self.tunnelInfoSubWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunnelInfoSubWidget.sizePolicy().hasHeightForWidth())
        self.tunnelInfoSubWidget.setSizePolicy(sizePolicy)
        self.tunnelInfoSubWidget.setObjectName("tunnelInfoSubWidget")
        self.tunnelInfoSubLayout = QHBoxLayout(self.tunnelInfoSubWidget)
        self.tunnelInfoSubLayout.setContentsMargins(0, 0, 0, 0)
        self.tunnelInfoSubLayout.setSpacing(8)
        self.tunnelInfoSubLayout.setObjectName("tunnelInfoSubLayout")
        self.protocolInfoLabel = BodyLabel(self.tunnelInfoSubWidget)
        self.protocolInfoLabel.setObjectName("protocolInfoLabel")
        self.tunnelInfoSubLayout.addWidget(self.protocolInfoLabel)
        self.portForwardInfoLabel = BodyLabel(self.tunnelInfoSubWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portForwardInfoLabel.sizePolicy().hasHeightForWidth())
        self.portForwardInfoLabel.setSizePolicy(sizePolicy)
        self.portForwardInfoLabel.setObjectName("portForwardInfoLabel")
        self.tunnelInfoSubLayout.addWidget(self.portForwardInfoLabel)
        self.verticalLayout.addWidget(self.tunnelInfoSubWidget)
        self.btnWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnWidget.sizePolicy().hasHeightForWidth())
        self.btnWidget.setSizePolicy(sizePolicy)
        self.btnWidget.setObjectName("btnWidget")
        self.btnLayout = QHBoxLayout(self.btnWidget)
        self.btnLayout.setContentsMargins(0, 0, 0, 0)
        self.btnLayout.setSpacing(4)
        self.btnLayout.setObjectName("btnLayout")
        self.copyUrlBtn = TonalPushButton(self.btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyUrlBtn.sizePolicy().hasHeightForWidth())
        self.copyUrlBtn.setSizePolicy(sizePolicy)
        self.copyUrlBtn.setObjectName("copyUrlBtn")
        self.btnLayout.addWidget(self.copyUrlBtn)
        self.editTunnelBtn = TonalPushButton(self.btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.editTunnelBtn.sizePolicy().hasHeightForWidth())
        self.editTunnelBtn.setSizePolicy(sizePolicy)
        self.editTunnelBtn.setObjectName("editTunnelBtn")
        self.btnLayout.addWidget(self.editTunnelBtn)
        self.delTunnelBtn = TonalPushButton(self.btnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delTunnelBtn.sizePolicy().hasHeightForWidth())
        self.delTunnelBtn.setSizePolicy(sizePolicy)
        self.delTunnelBtn.setObjectName("delTunnelBtn")
        self.btnLayout.addWidget(self.delTunnelBtn)
        self.verticalLayout.addWidget(self.btnWidget)
        self.copyUrlBtn.setIcon(FIF.COPY)
        self.editTunnelBtn.setIcon(FIF.LABEL)
        self.delTunnelBtn.setIcon(FIF.DELETE)
        self.copyUrlBtn.setText("复制链接地址")
        self.editTunnelBtn.setText("编辑")
        self.delTunnelBtn.setText("删除")

    def setupInfo(self):
        self.tunnelNameLabel.setText(self.config["proxy_name"])
        self.nodeNameLabel.setText(splitNodeName(self.config["node_name"])[1])
        self.protocolInfoLabel.setText(self.config["proxy_type"].upper())
        if "http" not in self.config["proxy_type"]:
            self.portForwardInfoLabel.setText(
                self.config["local_ip"]
                + ":"
                + self.config["local_port"]
                + " -> "
                + self.config["node_hostname"]
                + ":"
                + self.config["remote_port"]
            )
            self.copyUrlBtn.clicked.connect(
                QApplication.clipboard().setText(
                    str(self.config["node_hostname"] + ":" + self.config["remote_port"])
                )
            )
        else:
            self.portForwardInfoLabel.setText(
                self.config["local_ip"]
                + ":"
                + self.config["local_port"]
                + " -> "
                + self.config["proxy_type"]
                + "://"
                + self.config["domain"]
            )
            self.copyUrlBtn.clicked.connect(
                QApplication.clipboard().setText(
                    str(self.config["proxy_type"] + "://" + self.config["domain"])
                )
            )
        self.editTunnelBtn.clicked.connect(self.editBtnSlot)
        self.delTunnelBtn.clicked.connect(self.delBtnSlot)
