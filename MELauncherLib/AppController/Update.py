from PyQt5.QtCore import QThread, pyqtSignal, QObject
from .. import VERSION
import os
import sys
from platform import architecture
from qmaterialwidgets import InfoBar, InfoBarPosition
from .Settings import devMode


def checkUpdate():
    from MEFrpLib.models import APISession

    updateInfo = sorted(
        APISession(True).get("https://api.mefrp.com/api/v4/public/client/update").json()["data"],
        key=lambda x: x["id"],
    )  # type: list[dict[str,str]]
    updateInfo[-1]["log"] = updateInfo[-1]["log"].replace("\\n", "\n")
    updateInfo[-1].pop("id")
    arch = architecture()[0]
    if arch == "64bit":
        arch = "x64"
    elif arch == "32bit":
        arch = "x86"
    else:
        arch = "arm64"
    updateInfo[-1]["url"] = str(updateInfo[-1]["url"]).format(arch=arch)
    return updateInfo[-1]


class CheckUpdateThread(QThread):
    """
    检查更新的网络连接线程\n
    使用多线程防止假死
    """

    isUpdate = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("CheckUpdateThread")

    def run(self):
        try:
            latestVerInfo = checkUpdate()
            self.isUpdate.emit(latestVerInfo)
        except Exception:
            self.isUpdate.emit({"version": "", "log": "", "url": ""})


class Updater(QObject):
    def __init__(self, updateInfo, parent=None):
        super().__init__(parent)
        self.url = updateInfo["url"]  # type: str

    def downloadUpdate(self, showInfoBar: bool = True):
        """下载"""
        if devMode:
            return
        else:
            if showInfoBar:
                InfoBar.info(
                    title=self.tr("正在下载更新"),
                    content=self.tr("MEFrp-Launcher 稍后将自动重启"),
                    position=InfoBarPosition.BOTTOM_RIGHT,
                    duration=-1,
                    parent=self.parent().window(),
                )
        os.system(f"aria2c.exe -d update {self.url}")
        os.system(f".\\update\\{os.path.basename(self.url)}")
        sys.exit()


def compareVersion(newVer: str) -> bool:
    """比较版本号"""
    return bool(int("".join(VERSION.split("."))) < int("".join(newVer.split("."))))
