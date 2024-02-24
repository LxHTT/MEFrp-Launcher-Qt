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

import os
from os import path as osp, remove
from shutil import move, rmtree
from platform import system, architecture
from PyQt5.QtCore import QProcess
from zipfile import ZipFile
from .. import FRPC_VERSION

frpcDownloadInfo = {
    "darwin_amd64": f"https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_{FRPC_VERSION}_darwin_amd64.tar.gz",
    "darwin_arm64": f"https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_{FRPC_VERSION}_darwin_arm64.tar.gz",
    "linux_amd64": f"https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_{FRPC_VERSION}_linux_amd64.tar.gz",
    "linux_arm64": f"https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_{FRPC_VERSION}_linux_arm64.tar.gz",
    "windows_amd64": f"https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_{FRPC_VERSION}_windows_amd64.zip",
    "windows_arm64": f"https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_{FRPC_VERSION}_windows_arm64.zip",
    "windows_386": "https://jn.sv.ztsin.cn:5244/d/alistfile/MEFrp/MirrorEdgeFrp_0.51.3_windows_386.zip",
}


def downloadFrpc(parent):
    arch = architecture()[0]
    if arch == "64bit":
        arch = "amd64"
    elif arch == "32bit":
        arch = "386"
    else:
        arch = "arm64"
    if system().lower() == "macos":
        systemType = "darwin"
    else:
        systemType = system().lower()
    try:
        url = frpcDownloadInfo["{systemType}_{arch}".format(systemType=systemType, arch=arch)]
    except KeyError:
        raise LookupError("Not support this platform!")
    parent.systemTrayIcon.showMessage("MEFrp Launcher", "正在补全Frpc，请耐心等待...", 5)
    if osp.exists(f"frpc/{osp.basename(url)}"):
        remove(f"frpc/{osp.basename(url)}")
    os.system(f"aria2c.exe -d frpc {url}")
    extractFrpc(file_name=osp.basename(url))
    parent.systemTrayIcon.showMessage("MEFrp Launcher", "Frpc补全完毕", 5)


def extractFrpc(file_name):
    frpcProcessName = "frpc.exe" if system().lower() == "windows" else "frpc"
    if osp.exists(f"frpc/{frpcProcessName}"):
        remove(f"frpc/{frpcProcessName}")
    with ZipFile(f"frpc/{file_name}", "r") as frpcArchive:
        frpcArchive.extract(
            f"{file_name.replace('.zip', '').replace('.tar.gz', '')}/{frpcProcessName}", "frpc"
        )
    move(
        f"frpc/{file_name.replace('.zip', '').replace('.tar.gz', '')}/{frpcProcessName}",
        f"frpc/{frpcProcessName}",
    )
    remove(f"frpc/{file_name}")
    rmtree(f"frpc/{file_name.replace('.zip', '').replace('.tar.gz', '')}")


def checkFrpc(getVersion):
    frpcProcessName = "frpc.exe" if system().lower() == "windows" else "frpc"
    if not osp.exists(f"frpc/{frpcProcessName}"):
        return "未安装" if getVersion else False
    else:
        frpc = QProcess()
        frpc.setProgram(f"frpc/{frpcProcessName}")
        frpc.setArguments(["-v"])
        frpc.setWorkingDirectory("frpc")
        frpc.start()
        frpc.waitForFinished()
        frpcVersion = (
            frpc.readAll().data().decode("utf-8").replace("MirrorEdgeFrp_", "").replace("\n", "")
        )
        return (
            "已安装，版本 {frpcVersion}".format(frpcVersion=frpcVersion)
            if getVersion
            else bool(frpcVersion == FRPC_VERSION)
        )
