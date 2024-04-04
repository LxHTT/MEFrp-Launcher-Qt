from PyQt5.QtWidgets import QGridLayout, QSizePolicy, QSpacerItem, QWidget, QDialogButtonBox
from PyQt5.QtCore import QObject, pyqtSlot
from qmaterialwidgets import (
    TitleLabel,
    FlowLayout,
    TonalPushButton,
    FluentIcon as FIF,
    TextEdit,
    MessageBox,
    InfoBarPosition,
    InfoBar,
    TextPushButton,
)
from ..APIController import (
    EditTunnelThread,
    GetTunnelListThread,
    DeleteTunnelThread,
    JSONReturnModel,
)
from .Multiplex.TunnelWidget import TunnelWidget
from .Multiplex.EditTunnelWidget import EditTunnelWidget
from ..AppController.encrypt import getToken
from ..AppController.Settings import cfg
from ..AppController.Utils import FrpcConsoleVariables, readFile, writeFile
from ..FrpcController.processCreator import FrpcLauncher, FrpcLaunchMode
from os import path as osp


class TunnelManagerAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def getTunnelListAPI(self) -> GetTunnelListThread:
        return GetTunnelListThread(authorization=getToken(), parent=self)

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
        self.refreshTunnelListBtn = TonalPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshTunnelListBtn.sizePolicy().hasHeightForWidth())
        self.refreshTunnelListBtn.setSizePolicy(sizePolicy)
        self.refreshTunnelListBtn.setObjectName("refreshTunnelListBtn")
        self.gridLayout.addWidget(self.refreshTunnelListBtn, 2, 0, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 2)
        self.containerWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.containerWidget.sizePolicy().hasHeightForWidth())
        self.containerWidget.setSizePolicy(sizePolicy)
        self.tunnelListFlowLayout = FlowLayout(self.containerWidget)
        self.gridLayout.addWidget(self.containerWidget, 4, 0, 1, 2)
        self.TitleLabel.setText("隧道列表")
        self.refreshTunnelListBtn.setIcon(FIF.UPDATE)
        self.refreshTunnelListBtn.setText("刷新")
        self.tunnelListFlowLayout.setContentsMargins(0, 0, 0, 0)
        self.refreshTunnelListBtn.clicked.connect(self.getTunnelListFunc)

    def getTunnelListFunc(self):
        self.tunnelListFlowLayout.takeAllWidgets()
        if hasattr(self, "getTunnelListThread"):
            if self.getTunnelListThread.isRunning():
                return
        self.getTunnelListThread = self.getTunnelListAPI()
        self.getTunnelListThread.returnSlot.connect(self.getTunnelListAPIParser)
        self.getTunnelListThread.start()

    @pyqtSlot(JSONReturnModel)
    def getTunnelListAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "Success!":
            for config in model.data:
                self.tunnelListFlowLayout.addWidget(
                    TunnelWidget(
                        config=config,
                        runFrpcBtnSlot=self.startTunnel,
                        copyUrlBtnSlot=self.showCopyUrlTip,
                        editBtnSlot=self.editTunnelPreFunc,
                        delBtnSlot=self.deleteTunnelPreFunc,
                    )
                )

    def showCopyUrlTip(self):
        InfoBar.success(
            title="复制成功",
            content="已复制到剪贴板",
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def editTunnelPreFunc(self):
        self.editTunnelMessageBox = MessageBox(
            title="编辑隧道 “{tunnel_name}”".format(
                tunnel_name=self.sender().property("tunnel_name")
            ),
            content="对于HTTP / HTTPS 隧道，我们并不支持直接修改域名。\n此类用户请删除隧道重建。",
            parent=self,
        )
        self.editTunnelWidget = EditTunnelWidget(
            tunnel_id=self.sender().property("id"),
            tunnel_name=self.sender().property("tunnel_name"),
            local_ip=self.sender().property("local_ip"),
            local_port=self.sender().property("local_port"),
        )
        self.editTunnelMessageBox.yesButton.setText("提交")
        try:
            self.editTunnelMessageBox.yesButton.clicked.disconnect()
        except Exception:
            pass
        self.editTunnelMessageBox.yesButton.clicked.connect(self.editTunnelFunc)
        self.editTunnelMessageBox.cancelButton.setText("取消")
        self.editTunnelMessageBox.textLayout.addWidget(self.editTunnelWidget)
        self.editTunnelMessageBox.exec()

    def editTunnelFunc(self):
        self.editTunnelMessageBox.yesButton.setEnabled(False)
        self.editTunnelThread = self.editTunnelAPI(
            tunnel_id=self.editTunnelWidget.property("id"),
            tunnel_name=self.editTunnelWidget.tunnelNameEdit.text(),
            local_port=int(self.editTunnelWidget.localPortEdit.text()),
            local_ip=self.editTunnelWidget.localAddrEdit.text(),
        )
        self.editTunnelThread.returnSlot.connect(self.editTunnelThreadAPIParser)
        self.editTunnelThread.start()

    @pyqtSlot(JSONReturnModel)
    def editTunnelThreadAPIParser(self, model: JSONReturnModel):
        attr = "success"
        if model.status != 200 or model.message != "更新成功!":
            attr = "error"
        else:
            pass

        getattr(InfoBar, attr)(
            title=("错误" if attr == "error" else "成功"),
            content=model.message,
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )
        self.refreshTunnelListBtn.click()

    def deleteTunnelPreFunc(self):
        id = self.sender().property("id")
        w = MessageBox(
            title="确认删除此隧道？",
            content="这将使您不能继续使用该隧道并可能返回 API 404 错误。",
            parent=self,
        )
        w.yesButton.setText("确定")
        w.yesButton.clicked.connect(lambda: self.deleteTunnelFunc(id))
        w.cancelButton.setText("取消")
        w.exec()

    def deleteTunnelFunc(self, id: int):
        if hasattr(self, "deleteTunnelThread"):
            if self.deleteTunnelThread.isRunning():
                return
        self.deleteTunnelThread = self.deleteTunnelAPI(tunnel_id=id)
        self.deleteTunnelThread.returnSlot.connect(self.deleteTunnelAPIParser)
        self.deleteTunnelThread.start()

    @pyqtSlot(JSONReturnModel)
    def deleteTunnelAPIParser(self, model: JSONReturnModel):
        attr = "success"
        if model.status != 200 or model.message != "删除成功":
            attr = "error"
        else:
            pass

        getattr(InfoBar, attr)(
            title=("错误" if attr == "error" else "成功"),
            content=model.message,
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )
        self.refreshTunnelListBtn.click()

    def startTunnel(self):
        tunnelId = self.sender().property("id")
        sd = self.sender()
        if self.sender().isChecked():
            if cfg.get(cfg.runFrpcType) == "Config":
                w = MessageBox(
                    "启动选项", "您当前选用了 frpc.ini 启动方式。\n\n请选择您的操作：", self
                )
                w.yesButton.setText("启动隧道")
                w.cancelButton.setText("更新配置并启动")
                editConfigBtn = TextPushButton("编辑配置")
                editConfigBtn.clicked.connect(w.close)
                editConfigBtn.clicked.connect(
                    lambda: self.editTunnelConfigFile(tunnelId=tunnelId, sender=sd)
                )
                w.buttonGroup.addButton(editConfigBtn, QDialogButtonBox.ActionRole)
                w.yesButton.clicked.connect(
                    lambda: self.runTunnel(tunnelId=tunnelId, isUpdateConfig=False, sender=sd)
                )
                w.cancelButton.clicked.connect(
                    lambda: self.runTunnel(tunnelId=tunnelId, isUpdateConfig=True, sender=sd)
                )
                w.exec()
            else:
                self.runTunnel(tunnelId=tunnelId, isUpdateConfig=False, sender=sd)
        else:
            self.closeTunnel(tunnelId=tunnelId)

    def editTunnelConfigFile(self, tunnelId: int, sender):
        sender.setChecked(False)
        if osp.exists("config/{tunnelId}.ini".format(tunnelId=tunnelId)):
            config = readFile("config/{tunnelId}.ini".format(tunnelId=tunnelId))
            w = MessageBox(
                title="编辑配置",
                content="",
                parent=self,
            )
            w.yesButton.setText("保存")
            w.contentLabel.setParent(None)
            w.textLayout.addWidget(
                t := TextEdit(
                    parent=w,
                )
            )
            t.setFixedWidth(int(self.window().width() * 0.65))
            t.setPlainText(config)
            w.yesButton.clicked.connect(
                lambda: writeFile(
                    "config/{tunnelId}.ini".format(tunnelId=tunnelId), t.toPlainText()
                )
            )
            w.exec()
            del config
        else:
            e = MessageBox(
                title="错误",
                content="配置文件不存在，请先更新配置文件。",
                icon=FIF.QUESTION,
                parent=self,
            )
            e.cancelButton.setParent(None)
            e.exec()

    def runTunnel(self, tunnelId: int, isUpdateConfig: bool, sender):
        launchModeDict = {"Easy": FrpcLaunchMode.EasyMode, "Config": FrpcLaunchMode.ConfigMode}
        bridge = FrpcLauncher(
            launchMode=launchModeDict.get(cfg.get(cfg.runFrpcType)),
            tunnelId=tunnelId,
            isUpdateConfig=isUpdateConfig,
            parent=self,
        ).setup()
        bridge.frpcLogOutput.connect(self.parent().parent().parent().frpcLogPage.colorConsoleText)
        comboBoxView = f"[#{tunnelId}] {sender.property('tunnel_name')}"
        self.parent().parent().parent().frpcLogPage.frpcLogFilterComboBox.addItem(comboBoxView)
        bridge.frpcClosed.connect(
            lambda: self.parent()
            .parent()
            .parent()
            .frpcLogPage.frpcLogFilterComboBox.removeItem(
                self.parent()
                .parent()
                .parent()
                .frpcLogPage.frpcLogFilterComboBox.findText(comboBoxView)
            )
        )
        bridge.frpcClosed.connect(lambda: self.closeTunnel(tunnelId=tunnelId, closed=True))

        FrpcConsoleVariables.bridgeDict.update({str(tunnelId): bridge})

    def closeTunnel(self, tunnelId: int, closed=False):
        try:
            existBridge = FrpcConsoleVariables.bridgeDict[str(tunnelId)]
        except KeyError:
            return
        try:
            existBridge.killFrpc()
        except Exception:
            pass
        if not closed:
            FrpcConsoleVariables.bridgeDict.pop(str(tunnelId))
