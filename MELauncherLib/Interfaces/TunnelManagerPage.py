from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QSpacerItem, QWidget
from PyQt5.QtCore import QObject
from qmaterialwidgets import TitleLabel, FlowLayout
from ..APIController import (
    GetTunnelConfigIdThread,
    EditTunnelThread,
    GetTunnelListThread,
    DeleteTunnelThread,
    GetTunnelConfigIdThread,
    JSONReturnModel,
    TextReturnModel,
)
from ..AppController.encrypt import getToken


class TunnelManagerAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def getTunnelListAPI(self) -> GetTunnelListThread:
        return GetTunnelListThread(authorization=getToken(), parent=self)

    def getTunnelConfigIdAPI(self, id: int) -> GetTunnelConfigIdThread:
        return GetTunnelConfigIdThread(authorization=getToken(), id=id, parent=self)

    def editTunnelAPI(
        self, tunnel_id: int, tunnel_name: str, local_port: int, local_ip: str
    ) -> EditTunnelThread:
        return EditTunnelThread(
            authorization=getToken(),
            tunnel_id=tunnel_id,
            tunnel_name=tunnel_name,
            local_port=local_port,
            local_ip=local_ip,
            parent=self,
        )

    def deleteTunnelAPI(self, tunnel_id: int) -> DeleteTunnelThread:
        return DeleteTunnelThread(authorization=getToken(), tunnel_id=tunnel_id, parent=self)


class TunnelManagerPage(QWidget, TunnelManagerAPI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(8, 8, 8, 8)
        self.setObjectName("TunnelManagerPage")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.containerWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.containerWidget.sizePolicy().hasHeightForWidth())
        self.containerWidget.setSizePolicy(sizePolicy)
        self.tunnelListFlowLayout = FlowLayout(self.containerWidget)
        self.gridLayout.addWidget(self.containerWidget, 2, 0, 1, 2)
        self.TitleLabel.setText("隧道列表")

    def getTunnelListFunc(self):
        self.getTunnel