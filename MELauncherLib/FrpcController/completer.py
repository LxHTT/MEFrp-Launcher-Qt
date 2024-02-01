from ..AppController.Utils import Downloader
from os import path as osp, remove
from platform import system, architecture
from PyQt5.QtCore import QProcess
from zipfile import ZipFile
from .. import FRPC_VERSION


frpcDownloadInfo = {
    "darwin_amd64": f"https://download.mefrp.com/n/axyxe0xdery7/b/mefrp-download/o/MirrorEdgeFrp_{FRPC_VERSION}_darwin_amd64.tar.gz",
    "darwin_arm64": f"https://download.mefrp.com/n/axyxe0xdery7/b/mefrp-download/o/MirrorEdgeFrp_{FRPC_VERSION}_darwin_arm64.tar.gz",
    "linux_amd64": f"https://download.mefrp.com/n/axyxe0xdery7/b/mefrp-download/o/MirrorEdgeFrp_{FRPC_VERSION}_linux_amd64.tar.gz",
    "linux_arm64": f"https://download.mefrp.com/n/axyxe0xdery7/b/mefrp-download/o/MirrorEdgeFrp_{FRPC_VERSION}_linux_arm64.tar.gz",
    "windows_amd64": f"https://download.mefrp.com/n/axyxe0xdery7/b/mefrp-download/o/MirrorEdgeFrp_{FRPC_VERSION}_windows_amd64.zip",
    "windows_arm64": f"https://download.mefrp.com/n/axyxe0xdery7/b/mefrp-download/o/MirrorEdgeFrp_{FRPC_VERSION}_windows_arm64.zip",
}


def downloadFrpc():
    arch = "amd64" if architecture()[0] == "64bit" else "arm64"
    if system().lower() == "macos":
        systemType = "darwin"
    else:
        systemType = system().lower()
    try:
        url = frpcDownloadInfo["{systemType}_{arch}".format(systemType=systemType, arch=arch)]
    except KeyError:
        raise LookupError("Not support this platform!")
    if osp.exists(osp.basename(url)):
        remove(osp.basename(url))
    down = Downloader(url, 16, osp.basename(url))
    down.finishSignal.connect(lambda: extractFrpc(osp.basename(url)))
    down.run()


def extractFrpc(file):
    frpcProcessName = "frpc.exe" if system().lower() == "windows" else "frpc"
    with ZipFile(file, "r") as frpcArchive:
        if osp.exists(f"frpc/{frpcProcessName}"):
            remove(f"frpc/{frpcProcessName}")
        frpcArchive.extract(
            f"{file.replace('.zip', '').replace('.tar.gz', '')}/{frpcProcessName}", "frpc"
        )


def checkFrpc() -> bool:
    if not osp.exists("./Plugins/OpenFRP_Plugin/frpc/frpc.exe"):
        return False
    else:
        frpc = QProcess()
        frpc.setProgram("./Plugins/OpenFRP_Plugin/frpc/frpc.exe")
        frpc.setArguments(["-v"])
        frpc.setWorkingDirectory("./Plugins/OpenFRP_Plugin/frpc")
        frpc.start()
        frpc.waitForFinished()
        return bool(frpc.readAll().data().decode("utf-8").split("_")[1] == FRPC_VERSION)
