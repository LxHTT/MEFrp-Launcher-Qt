from PyQt5.QtWidgets import QWidget, QGridLayout, QSpacerItem, QSizePolicy, QFileDialog
from PyQt5.QtCore import pyqtSlot, Qt
from qmaterialwidgets import (
    ComboBox,
    TextEdit,
    TitleLabel,
    TonalPushButton,
    ElevatedPushButton,
    InfoBar,
    InfoBarPosition,
    FluentIcon as FIF,
)
from os import getcwd
from ..AppController.encrypt import getToken
from ..AppController.Utils import FrpcConsoleVariables, openLocalFile


class FrpcLogPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(8, 8, 8, 8)
        self.setObjectName("FrpcLogPage")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 4)
        self.frpcLogTextEdit = TextEdit(self)
        self.frpcLogTextEdit.setUndoRedoEnabled(False)
        self.frpcLogTextEdit.setReadOnly(True)
        self.frpcLogTextEdit.setObjectName("frpcLogTextEdit")
        self.gridLayout.addWidget(self.frpcLogTextEdit, 3, 0, 1, 4)
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.clearLogBtn = TonalPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearLogBtn.sizePolicy().hasHeightForWidth())
        self.clearLogBtn.setSizePolicy(sizePolicy)
        self.clearLogBtn.setObjectName("clearLogBtn")
        self.gridLayout.addWidget(self.clearLogBtn, 2, 0, 1, 1)
        self.saveLogBtn = TonalPushButton(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveLogBtn.sizePolicy().hasHeightForWidth())
        self.saveLogBtn.setSizePolicy(sizePolicy)
        self.saveLogBtn.setObjectName("saveLogBtn")
        self.gridLayout.addWidget(self.saveLogBtn, 2, 1, 1, 1)
        self.frpcLogFilterComboBox = ComboBox(self)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcLogFilterComboBox.sizePolicy().hasHeightForWidth())
        self.frpcLogFilterComboBox.setSizePolicy(sizePolicy)
        self.frpcLogFilterComboBox.setObjectName("frpcLogFilterComboBox")
        self.gridLayout.addWidget(self.frpcLogFilterComboBox, 2, 2, 1, 2)
        self.TitleLabel.setText("日志")
        self.clearLogBtn.setText("清空")
        self.saveLogBtn.setText("保存日志")
        self.frpcLogFilterComboBox.addItem("[#0] 所有隧道")
        self.frpcLogFilterComboBox.removeItem
        self.frpcLogFilterComboBox.setCurrentIndex(0)
        self.frpcLogFilterComboBox.currentIndexChanged.connect(self.filterFrpcLog)
        self.clearLogBtn.clicked.connect(self.clearFrpcLog)
        self.saveLogBtn.clicked.connect(self.saveFrpcLog)

    @pyqtSlot(str)
    def colorConsoleText(self, frpcLogOutput: str):
        self.frpcLogTextEdit.append(frpcLogOutput[:-1])
        if "start proxy success" in frpcLogOutput:
            id = frpcLogOutput.split(" ")[0]
            tunnelName = (
                frpcLogOutput.split("] [")[3]
                .replace(getToken(), "")[1:]
                .replace("] start proxy success", "")
            )
            InfoBar.success(
                title=id + " " + tunnelName,
                content="隧道启动成功",
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP,
                duration=3500,
                parent=self.window(),
            )

    def filterFrpcLog(self):
        if not self.sender().currentIndex():
            self.frpcLogTextEdit.setPlainText("".join(FrpcConsoleVariables.totalLogList))
        else:
            self.frpcLogTextEdit.setPlainText(
                "".join(
                    FrpcConsoleVariables.singleLogDict[
                        self.sender().text().split("] ")[0].replace("[#", "")
                    ]
                )
            )

    def clearFrpcLog(self):
        self.frpcLogTextEdit.clear()
        if not self.frpcLogFilterComboBox.currentIndex():
            FrpcConsoleVariables.totalLogList = []
        else:
            FrpcConsoleVariables.singleLogDict[
                self.frpcLogFilterComboBox.text().split("] ")[0].replace("[#", "")
            ] = []

    def saveFrpcLog(self):
        saveLogFileDialog = QFileDialog(self, "MEFrp-Launcher 保存 Frpc 日志", getcwd())
        saveLogFileDialog.setAcceptMode(QFileDialog.AcceptSave)
        saveLogFileDialog.setNameFilter("Log Files (*.log);;Text Files (*.txt)")
        saveLogFileDialog.selectFile("Frpc.log")
        if saveLogFileDialog.exec_() == QFileDialog.Accepted:
            try:
                with open(saveLogFileDialog.selectedFiles()[0], "w+", encoding="utf-8") as f:
                    f.write(self.frpcLogTextEdit.toPlainText())
                finishBtn = ElevatedPushButton(text="打开", parent=self)
                finishBtn.clicked.connect(
                    lambda: openLocalFile(saveLogFileDialog.selectedFiles()[0])
                )
                (
                    i := InfoBar(
                        icon=FIF.LINK,
                        title="成功",
                        content=f"日志已保存至 {saveLogFileDialog.selectedFiles()[0]}",
                        isClosable=True,
                        position=InfoBarPosition.TOP,
                        duration=3500,
                        parent=self,
                    )
                ).addWidget(finishBtn)
                i.show()
            except Exception as e:
                InfoBar.error(
                    title="失败",
                    content=e,
                    isClosable=True,
                    position=InfoBarPosition.TOP,
                    duration=3500,
                    parent=self,
                )
        else:
            return

    def isAnyFrpcRunning(self):
        return bool(self.frpcLogFilterComboBox.count() > 1)
