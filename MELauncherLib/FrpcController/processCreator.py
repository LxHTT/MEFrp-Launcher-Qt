# -*- coding: utf-8 -*-
#     Copyright 2024, MCSL Team, mailto:services@mcsl.com.cn
#
#     Part of "MCSL2", a simple and multifunctional Minecraft server launcher.
#
#     Licensed under the GNU General Public License, Version 3.0, with our
#     additional agreements. (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#        https://github.com/MCSLTeam/MCSL2/raw/master/LICENSE
#
################################################################################
"""
Communicate with Minecraft servers.
"""

from os import path as osp
from typing import Optional, List
from enum import Enum
from platform import system
from PyQt5.QtCore import QProcess, QObject, pyqtSignal, pyqtSlot
from ..APIController import (
    GetTunnelConfigIdThread,
    TextReturnModel,
)
from ..AppController.encrypt import getToken
from ..AppController.Utils import FrpcConsoleVariables, writeFile


class FrpcLaunchMode(Enum):
    """启动模式"""

    EasyMode = 0
    ConfigMode = 1


class FrpcProcess:
    """进程"""

    def __init__(self):
        self.process: Optional[QProcess] = None
        self.lastOutputSize = 0


class FrpcProcessBridge(QObject):
    """进程操控器"""

    # 当输出日志时发出的信号(发送一个字符串)
    frpcLogOutput = pyqtSignal(str)

    # 当关闭时发出的信号(发送一个整数exit code)
    frpcClosed = pyqtSignal(int)

    def __init__(self, tunnelId: int, argList: List[str]):
        """
        初始化一个服务器处理器
        """
        super().__init__()
        self.tunnelId = tunnelId
        self.argList = argList
        self.workingDirectory: str = osp.abspath("frpc")
        self.partialData: str = b""
        self.handledFrpc = None
        self.frpcProcess = self.createProcess()

    def createProcess(self) -> FrpcProcess:
        """
        创建进程对象
        """
        self.handledFrpc = FrpcProcess()
        self.handledFrpc.process = QProcess()
        self.handledFrpc.process.setProgram(
            "frpc/frpc.exe" if "windows" in system().lower() else "frpc/frpc"
        )
        self.handledFrpc.process.setArguments(self.argList)
        self.handledFrpc.process.setWorkingDirectory(self.workingDirectory)
        self.handledFrpc.process.readyReadStandardOutput.connect(self.frpcLogOutputHandler)
        self.handledFrpc.process.finished.connect(
            lambda: self.frpcClosed.emit(self.handledFrpc.process.exitCode())
        )
        return self.handledFrpc

    def frpcLogOutputHandler(self):
        """
        When the frpc outputs change, emit a signal with the updated output.
        """
        newData = self.frpcProcess.process.readAllStandardOutput().data()
        self.partialData += newData  # Append the incoming data to the buffer
        lines = self.partialData.split(b"\n")  # Split the buffer into lines
        self.partialData = (
            lines.pop()
        )  # The last element might be incomplete, so keep it in the buffer

        for line in lines:
            newOutput = line.decode("utf-8", errors="replace")
            self.frpcLogOutput.emit(f"[#{self.tunnelId}] " + newOutput + "\n")

    def startFrpc(self):
        self.frpcProcess = self.createProcess()
        self.frpcProcess.process.start()

    def killFrpc(self):
        if self.isFrpcRunning():
            self.frpcProcess.process.kill()
            self.frpcProcess.process.waitForFinished()

    def isFrpcRunning(self):
        if self.frpcProcess.process is None:
            return False
        return self.frpcProcess.process.state() == QProcess.Running


class FrpcLauncher(QObject):
    def __init__(
        self, launchMode: FrpcLaunchMode,
        tunnelId: int,
        isUpdateConfig: bool = False,
        parent=None
    ):
        super().__init__(parent=parent)
        self.launchMode = launchMode
        self.tunnelId = str(tunnelId)
        self.isUpdateConfig = isUpdateConfig
        self.argList = []

    def _constructArgs(self):
        if self.launchMode == FrpcLaunchMode.ConfigMode:
            self.argList = ["-c", osp.abspath("config/{id}.ini".format(id=self.tunnelId))]
        else:
            self.argList = ["-t", getToken(), "-i", self.tunnelId]

    def setup(self):
        self._constructArgs()
        FrpcConsoleVariables.singleLogDict[str(self.tunnelId)] = []
        if self.launchMode == FrpcLaunchMode.ConfigMode:
            if not self.isUpdateConfig:
                if osp.exists("config/{id}.ini".format(id=self.tunnelId)):
                    return self._launch()
                else:
                    return self._getTunnelConfigFunc()
            else:
                return self._getTunnelConfigFunc()
        else:
            return self._launch()

    def _launch(self) -> FrpcProcessBridge:
        """启动进程"""
        (bridge := FrpcProcessBridge(tunnelId=self.tunnelId, argList=self.argList)).startFrpc()
        bridge.frpcLogOutput.connect(FrpcConsoleVariables.totalLogList.append)
        bridge.frpcLogOutput.connect(FrpcConsoleVariables.singleLogDict[str(self.tunnelId)].append)
        bridge.frpcClosed.connect(
            lambda: FrpcConsoleVariables.singleLogDict.pop(str(self.tunnelId))
        )
        return bridge

    def _getTunnelConfigFunc(self) -> FrpcProcessBridge:
        self.getTunnelConfigThread = GetTunnelConfigIdThread(
            authorization=getToken(), id=self.tunnelId, parent=self
        )
        self.getTunnelConfigThread.returnSlot.connect(self.getTunnelConfigAPIParser)
        self.getTunnelConfigThread.start()
        self.getTunnelConfigThread.wait()
        return self._launch()

    @pyqtSlot(TextReturnModel)
    def getTunnelConfigAPIParser(self, model: TextReturnModel):
        writeFile(file="config/{id}.ini".format(id=self.tunnelId), content=model.data)
