from random import randint
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QGridLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import QSize, QRect, Qt, QObject, pyqtSlot
from qmaterialwidgets import (
    FilledComboBox,
    FilledLineEdit,
    FilledPushButton,
    OutlinedCardWidget,
    SpinBox,
    SubtitleLabel,
    TitleLabel,
    FluentIcon as FIF,
    InfoBarPosition,
    InfoBar,
    InfoBarIcon,
    TonalPushButton,
    FilterChip,
)

from MELauncherLib.Interfaces.Multiplex.NodeWidget import NodeWidget

from .Multiplex.ScollArea import NormalSmoothScrollArea
from ..APIController import (
    NodeListThread,
    CreateTunnelThread,
    JSONReturnModel,
    GetRealnameStatusThread,
    GetFreePortThread,
)

from ..AppController.encrypt import getToken


class CreateTunnelAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def getNodeListAPI(self) -> NodeListThread:
        return NodeListThread(authorization=getToken(), parent=self)

    def getRealnameStatusAPI(self) -> GetRealnameStatusThread:
        return GetRealnameStatusThread(authorization=getToken(), parent=self)

    def getFreePortAPI(self, id: int, protocol: str) -> GetFreePortThread:
        return GetFreePortThread(authorization=getToken(), id=id, protocol=protocol, parent=self)

    def createTunnelAPI(
        self,
        node: int,
        proxy_type: str,
        local_ip: str,
        local_port: int,
        remote_port: int,
        proxy_name: str,
    ) -> CreateTunnelThread:
        return CreateTunnelThread(
            authorization=getToken(),
            node=node,
            proxy_type=proxy_type,
            local_ip=local_ip,
            local_port=local_port,
            remote_port=remote_port,
            proxy_name=proxy_name,
            parent=self,
        )


class CreateTunnelPage(QWidget, CreateTunnelAPI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CreateTunnelPage")

        self.setContentsMargins(8, 8, 8, 8)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.createTunnelPageScrollArea = NormalSmoothScrollArea(self)
        self.createTunnelPageScrollArea.setWidgetResizable(True)
        self.createTunnelPageScrollArea.setObjectName("createTunnelPageScrollArea")
        self.createTunnelPageSC = QWidget()
        self.createTunnelPageSC.setGeometry(QRect(0, 0, 716, 722))
        self.createTunnelPageSC.setObjectName("createTunnelPageSC")
        self.proxySettingsFakeLayout = QVBoxLayout(self.createTunnelPageSC)
        self.proxySettingsFakeLayout.setContentsMargins(0, 0, 0, 0)
        self.proxySettingsFakeLayout.setObjectName("proxySettingsFakeLayout")
        self.refreshNodeWidget = QWidget(self.createTunnelPageSC)
        self.refreshNodeWidget.setObjectName("refreshNodeWidget")
        self.refreshNodeLayout = QHBoxLayout(self.refreshNodeWidget)
        self.refreshNodeLayout.setContentsMargins(0, 0, 0, -1)
        self.refreshNodeLayout.setObjectName("refreshNodeLayout")
        self.refreshNodeBtn = TonalPushButton(self.refreshNodeWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshNodeBtn.sizePolicy().hasHeightForWidth())
        self.refreshNodeBtn.setSizePolicy(sizePolicy)
        self.refreshNodeBtn.setObjectName("refreshNodeBtn")
        self.refreshNodeLayout.addWidget(self.refreshNodeBtn)
        self.proxySettingsFakeLayout.addWidget(self.refreshNodeWidget)
        self.nodesWidget = OutlinedCardWidget(self.createTunnelPageSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nodesWidget.sizePolicy().hasHeightForWidth())
        self.nodesWidget.setSizePolicy(sizePolicy)
        self.nodesWidget.setMinimumSize(QSize(0, 200))
        self.nodesWidget.setMaximumSize(QSize(16777215, 200))
        self.nodesWidget.setObjectName("nodesWidget")
        self.gridLayout_2 = QGridLayout(self.nodesWidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.nodesScrollArea = NormalSmoothScrollArea(self.nodesWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nodesScrollArea.sizePolicy().hasHeightForWidth())
        self.nodesScrollArea.setSizePolicy(sizePolicy)
        self.nodesScrollArea.setMinimumSize(QSize(250, 190))
        self.nodesScrollArea.setMaximumSize(QSize(16777215, 190))
        self.nodesScrollArea.setFrameShape(QFrame.NoFrame)
        self.nodesScrollArea.setFrameShadow(QFrame.Plain)
        self.nodesScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.nodesScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.nodesScrollArea.setWidgetResizable(True)
        self.nodesScrollArea.setObjectName("nodesScrollArea")
        self.tunnelsSC = QWidget()
        self.tunnelsSC.setGeometry(QRect(0, 0, 680, 185))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunnelsSC.sizePolicy().hasHeightForWidth())
        self.tunnelsSC.setSizePolicy(sizePolicy)
        self.tunnelsSC.setObjectName("tunnelsSC")
        self.horizontalLayout = QHBoxLayout(self.tunnelsSC)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tunnelsRealLayout = QHBoxLayout()
        self.tunnelsRealLayout.setObjectName("tunnelsRealLayout")
        self.horizontalLayout.addLayout(self.tunnelsRealLayout)
        self.nodesScrollArea.setWidget(self.tunnelsSC)
        self.gridLayout_2.addWidget(self.nodesScrollArea, 0, 0, 1, 1)
        self.proxySettingsFakeLayout.addWidget(self.nodesWidget)
        self.tunnelSettingsWidget = OutlinedCardWidget(self.createTunnelPageSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunnelSettingsWidget.sizePolicy().hasHeightForWidth())
        self.tunnelSettingsWidget.setSizePolicy(sizePolicy)
        self.tunnelSettingsWidget.setMinimumSize(QSize(0, 440))
        self.tunnelSettingsWidget.setObjectName("tunnelSettingsWidget")
        self.proxySettingsRealLayout = QGridLayout(self.tunnelSettingsWidget)
        self.proxySettingsRealLayout.setContentsMargins(18, 18, 18, 18)
        self.proxySettingsRealLayout.setVerticalSpacing(18)
        self.proxySettingsRealLayout.setObjectName("proxySettingsRealLayout")
        self.localPortLayout = QVBoxLayout()
        self.localPortLayout.setObjectName("localPortLayout")
        self.localPortLabel = SubtitleLabel(self.tunnelSettingsWidget)
        self.localPortLabel.setObjectName("localPortLabel")
        self.localPortLayout.addWidget(self.localPortLabel)
        self.localPortSpinBox = SpinBox(self.tunnelSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localPortSpinBox.sizePolicy().hasHeightForWidth())
        self.localPortSpinBox.setSizePolicy(sizePolicy)
        self.localPortSpinBox.setMinimumSize(QSize(190, 43))
        self.localPortSpinBox.setMaximumSize(QSize(16777215, 43))
        self.localPortSpinBox.setObjectName("localPortSpinBox")
        self.localPortLayout.addWidget(self.localPortSpinBox)
        self.proxySettingsRealLayout.addLayout(self.localPortLayout, 5, 0, 1, 1)
        self.localAddrEdit = FilledLineEdit(self.tunnelSettingsWidget)
        self.localAddrEdit.setObjectName("localAddrEdit")
        self.proxySettingsRealLayout.addWidget(self.localAddrEdit, 3, 0, 1, 4)
        self.tunnelNameEdit = FilledLineEdit(self.tunnelSettingsWidget)
        self.tunnelNameEdit.setObjectName("tunnelNameEdit")
        self.proxySettingsRealLayout.addWidget(self.tunnelNameEdit, 2, 0, 1, 4)
        self.remotePortLayout = QGridLayout()
        self.remotePortLayout.setHorizontalSpacing(10)
        self.remotePortLayout.setObjectName("remotePortLayout")
        self.remotePortSpinBox = SpinBox(self.tunnelSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remotePortSpinBox.sizePolicy().hasHeightForWidth())
        self.remotePortSpinBox.setSizePolicy(sizePolicy)
        self.remotePortSpinBox.setMinimumSize(QSize(190, 43))
        self.remotePortSpinBox.setMaximumSize(QSize(16777215, 43))
        self.remotePortSpinBox.setObjectName("remotePortSpinBox")
        self.remotePortLayout.addWidget(self.remotePortSpinBox, 1, 0, 1, 1)
        self.remotePortLabel = SubtitleLabel(self.tunnelSettingsWidget)
        self.remotePortLabel.setObjectName("remotePortLabel")
        self.remotePortLayout.addWidget(self.remotePortLabel, 0, 0, 1, 1)
        self.randomRemotePortBtn = TonalPushButton(self.tunnelSettingsWidget)
        self.randomRemotePortBtn.setObjectName("randomRemotePortBtn")
        self.remotePortLayout.addWidget(self.randomRemotePortBtn, 1, 1, 1, 1)
        self.proxySettingsRealLayout.addLayout(self.remotePortLayout, 5, 2, 1, 1)
        self.protocolComboBox = FilledComboBox(self.tunnelSettingsWidget)
        self.proxySettingsRealLayout.addWidget(self.protocolComboBox, 1, 0, 1, 4)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.proxySettingsRealLayout.addItem(spacerItem1, 5, 1, 1, 1)
        self.createTunnelBtn = FilledPushButton(self.tunnelSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.createTunnelBtn.sizePolicy().hasHeightForWidth())
        self.createTunnelBtn.setSizePolicy(sizePolicy)
        self.createTunnelBtn.setMinimumSize(QSize(110, 0))
        self.createTunnelBtn.setMaximumSize(QSize(16777215, 16777215))
        self.createTunnelBtn.setObjectName("createTunnelBtn")
        self.proxySettingsRealLayout.addWidget(self.createTunnelBtn, 6, 0, 1, 3)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.proxySettingsRealLayout.addItem(spacerItem2, 5, 3, 1, 1)
        self.selectedNodeLabel = SubtitleLabel(self.tunnelSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.selectedNodeLabel.sizePolicy().hasHeightForWidth())
        self.selectedNodeLabel.setSizePolicy(sizePolicy)
        self.selectedNodeLabel.setObjectName("selectedNodeLabel")
        self.proxySettingsRealLayout.addWidget(self.selectedNodeLabel, 0, 0, 1, 1)
        self.proxySettingsFakeLayout.addWidget(self.tunnelSettingsWidget)
        spacerItem3 = QSpacerItem(20, 54, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.proxySettingsFakeLayout.addItem(spacerItem3)
        self.createTunnelPageScrollArea.setWidget(self.createTunnelPageSC)
        self.gridLayout.addWidget(self.createTunnelPageScrollArea, 2, 0, 1, 1)
        spacerItem4 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem4, 1, 0, 1, 2)
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)

        self.TitleLabel.setText("创建隧道")
        self.remotePortLabel.setText("远程端口")
        self.createTunnelBtn.setText("创建隧道")
        self.localPortLabel.setText("本地端口")
        self.localAddrEdit.setLabel("本地地址（一般为127.0.0.1）")
        self.tunnelNameEdit.setLabel("隧道名称（支持英文、数字）")
        self.protocolComboBox.setLabel("选择协议")
        self.randomRemotePortBtn.setText("随机端口")
        self.refreshNodeBtn.setText("刷新")
        self.selectedNodeLabel.setText("已选择节点：未选择")
        self.randomRemotePortBtn.setIcon(FIF.ROTATE)
        self.localPortSpinBox.setMaximum(65535)
        self.remotePortSpinBox.setMaximum(65535)
        self.localPortSpinBox.setValue(25565)
        self.localAddrEdit.setText("127.0.0.1")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.protocolComboBox.sizePolicy().hasHeightForWidth())
        self.protocolComboBox.setSizePolicy(sizePolicy)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tunnelNameEdit.sizePolicy().hasHeightForWidth())
        self.tunnelNameEdit.setSizePolicy(sizePolicy)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.localAddrEdit.sizePolicy().hasHeightForWidth())
        self.localAddrEdit.setSizePolicy(sizePolicy)

        self.spacerItem = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.realnameStatusSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.onlyAvailableNodeBtn = FilterChip(self.refreshNodeWidget)
        self.onlyAvailableNodeBtn.setText("仅显示可用节点")
        self.onlyAvailableNodeBtn.clicked.connect(self.toggleVisibleNode)
        self.refreshNodeBtn.clicked.connect(self.getNodeListFunc)
        self.refreshNodeBtn.setIcon(FIF.UPDATE)
        # self.tunnelSettingsWidget.setEnabled(False)
        self.protocolComboBox.addItems(["TCP", "UDP"])
        self.randomRemotePortBtn.clicked.connect(self.getFreePortFunc)
        self.createTunnelBtn.clicked.connect(self.createTunnelFunc)

    def getRealnameStatusFunc(self):
        self.getRealnameStatusThread = self.getRealnameStatusAPI()
        self.getRealnameStatusThread.returnSlot.connect(self.getRealnameStatusAPIParser)
        self.getRealnameStatusThread.start()

    @pyqtSlot(JSONReturnModel)
    def getRealnameStatusAPIParser(self, model: JSONReturnModel):
        try:
            self.refreshNodeLayout.removeItem(self.realnameStatusSpacer)
        except Exception:
            pass
        for i in reversed(range(self.refreshNodeLayout.count())):
            try:
                self.refreshNodeLayout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
            try:
                self.refreshNodeLayout.itemAt(i).widget().deleteLater()
                del self.refreshNodeLayout.itemAt(i).widget
            except AttributeError:
                pass
        self.realnameStatusInfoBar = InfoBar(
            icon=InfoBarIcon.SUCCESS
            if model.data["code"] == 200 or model.data["realname"] == "已实名认证"
            else InfoBarIcon.ERROR,
            title="提示",
            content="您已完成实名认证，可使用所有节点"
            if model.data["realname"] == "已实名认证"
            else "您还未实名认证，将只能使用境外节点\n实名认证后，您将可以使用境内节点带宽限制将提升至30Mbps",  # noqa: E501
            orient=Qt.Horizontal,
            isClosable=False,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self.refreshNodeWidget,
        )
        self.realnameStatusInfoBar.setFixedWidth(
            327 if model.data["realname"] == "已实名认证" else 494
        )
        self.refreshNodeLayout.addWidget(self.realnameStatusInfoBar)
        self.refreshNodeLayout.addItem(self.realnameStatusSpacer)
        self.refreshNodeLayout.addWidget(self.onlyAvailableNodeBtn)
        self.refreshNodeLayout.addWidget(self.refreshNodeBtn)

    def getNodeListFunc(self):
        self.refreshNodeBtn.setEnabled(False)
        try:
            self.tunnelsRealLayout.removeItem(self.spacerItem)
        except Exception:
            pass
        for i in reversed(range(self.tunnelsRealLayout.count())):
            try:
                self.tunnelsRealLayout.itemAt(i).widget().setParent(None)
            except AttributeError:
                pass
            try:
                self.tunnelsRealLayout.itemAt(i).widget().deleteLater()
                del self.tunnelsRealLayout.itemAt(i).widget
            except AttributeError:
                pass

        self.getNodeListThread = self.getNodeListAPI()
        self.getNodeListThread.returnSlot.connect(self.getNodeListAPIParser)
        self.getNodeListThread.start()

    @pyqtSlot(JSONReturnModel)
    def getNodeListAPIParser(self, model: JSONReturnModel):
        self.refreshNodeBtn.setEnabled(True)
        for node in model.data:
            self.tunnelsRealLayout.addWidget(
                NodeWidget(config=node, slot=self.setSelectedNode, parent=self.tunnelsSC)
            )
        self.tunnelsRealLayout.addItem(self.spacerItem)
        self.toggleVisibleNode()
        self.getRealnameStatusFunc()

    def toggleVisibleNode(self):
        for i in reversed(range(self.tunnelsRealLayout.count())):
            try:
                if not isinstance(self.tunnelsRealLayout.itemAt(i), QSpacerItem):
                    if self.tunnelsRealLayout.itemAt(i).widget().property("status") != 200:
                        self.tunnelsRealLayout.itemAt(i).widget().setVisible(
                            not self.onlyAvailableNodeBtn.isChecked()
                        )
                    else:
                        self.tunnelsRealLayout.itemAt(i).widget().setVisible(True)
                else:
                    continue
            except AttributeError:
                pass

    def setSelectedNode(self):
        self.selectedNodeLabel.setText(f"已选择节点：{self.sender().property('name')}")
        self.id = self.sender().property("id")
        self.allow_port = self.sender().property("allow_port")
        self.allow_type = self.sender().property("allow_type")
        self.tunnelSettingsWidget.setEnabled(True)
        self.protocolComboBox.clear()
        self.protocolComboBox.addItems(self.allow_type)
        self.remotePortSpinBox.setMinimum(int(self.allow_port[0]))
        self.remotePortSpinBox.setMaximum(int(self.allow_port[1]))
        self.getFreePortFunc()

    def getFreePortFunc(self):
        self.randomRemotePortBtn.setEnabled(False)
        self.getFreePortThread = self.getFreePortAPI(
            id=self.id, protocol=str(self.allow_type[self.protocolComboBox.currentIndex()])
        )
        self.getFreePortThread.returnSlot.connect(self.getFreePortAPIParser)
        self.getFreePortThread.start()

    @pyqtSlot(JSONReturnModel)
    def getFreePortAPIParser(self, model: JSONReturnModel):
        self.randomRemotePortBtn.setEnabled(True)
        if model.status == 200 or model.message == "获取成功":
            self.remotePortSpinBox.setValue(model.data["free_port"])
        else:
            self.remotePortSpinBox.setValue(
                randint(int(self.allow_port[0]), int(self.allow_port[1]))
            )
            InfoBar.warning(
                title="警告",
                content="API无法返回有效可用端口！\n端口将由MEFrp-Launcher随机抽取，无法保证100%不被占用。\n若有占用请更换端口。",
                orient=Qt.Horizontal,
                isClosable=True,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )

    def createTunnelFunc(self):
        self.createTunnelBtn.setEnabled(False)
        self.createTunnelThread = self.createTunnelAPI(
            node=self.id,
            proxy_type=str(self.allow_type[self.protocolComboBox.currentIndex()]),
            local_ip=self.localAddrEdit.text(),
            local_port=self.localPortSpinBox.value(),
            remote_port=self.remotePortSpinBox.value(),
            proxy_name=self.tunnelNameEdit.text(),
        )
        self.createTunnelThread.returnSlot.connect(self.createTunnelAPIParser)
        self.createTunnelThread.start()

    @pyqtSlot(JSONReturnModel)
    def createTunnelAPIParser(self, model: JSONReturnModel):
        self.createTunnelBtn.setEnabled(True)
        attr = "success"
        if model.status == 200 or model.message == "创建成功":
            attr = "success"
        else:
            attr = "error"
        getattr(InfoBar, attr)(
            title="错误" if attr == "error" else "成功",
            content=model.message,
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )
