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

import hashlib
from os import makedirs, path as osp
from typing import Optional, Iterable, Callable, Dict, List, Tuple
from time import time, strftime, localtime


import psutil
from PyQt5.QtCore import QUrl, QThread, QThreadPool, QFile
from PyQt5.QtGui import QDesktopServices


def Singleton(cls):
    """单例化装饰器"""
    Instances = {}

    def GetInstance(*args, **kwargs):
        if cls not in Instances:
            Instances[cls] = cls(*args, **kwargs)
        return Instances[cls]

    return GetInstance


def initMELauncher():
    """
    初始化程序
    """

    folders = ["frpc", "config"]
    for folder in folders:
        if not osp.exists(folder):
            makedirs(folder, exist_ok=True)
    # set global thread pool
    QThreadPool.globalInstance().setMaxThreadCount(
        psutil.cpu_count(logical=True)
    )  # IO-Bound = 2*N, CPU-Bound = N + 1


def openWebUrl(Url):
    """打开网址"""
    QDesktopServices.openUrl(QUrl(Url))


def openLocalFile(FilePath):
    """打开本地文件(夹)"""
    QDesktopServices.openUrl(QUrl.fromLocalFile(FilePath))


def readFile(file: str):
    f = QFile(file)
    f.open(QFile.ReadOnly)
    content = str(f.readAll(), encoding="utf-8")
    f.close()
    return content


def writeFile(file: str, content: str):
    f = QFile(file)
    f.open(QFile.WriteOnly)
    f.write(content.encode("utf-8"))
    f.close()


def readBytesFile(file: str):
    f = QFile(file)
    f.open(QFile.ReadOnly)
    content = f.readAll()
    f.close()
    return content


def writeBytesFile(file: str, content: bytes):
    f = QFile(file)
    f.open(QFile.WriteOnly)
    f.write(content)
    f.close()


def checkSHA1(fileAndSha1: Iterable, _filter: Callable[[str, str], bool] = None) -> List[Dict]:
    """
    检查文件的SHA1值是否正确
    """
    rv = []
    if _filter is None:

        def _filter(a, b):
            return True

    for file, sha1 in fileAndSha1:
        if not osp.exists(file):
            rv.append({"file": file, "result": False})
            continue
        if _filter(file, sha1):
            # check sha1
            f = readBytesFile(file)
            fileSha1 = hashlib.sha1(f).hexdigest()
            del f
            rv.append({"file": file, "result": fileSha1 == sha1})
        else:
            rv.append({"file": file, "result": True})
    return rv


def unixTimeStampToTime(timeStamp):
    return strftime("%Y-%m-%d %H:%M:%S", localtime(timeStamp))


def check24HoursPassed(timeStamp):
    current_timestamp = int(time())
    if current_timestamp > (timeStamp + 86400):
        return True
    else:
        return False


def splitNodeName(name) -> Tuple[str, str]:
    return (bandwidth := name.replace(" 节点", "").split(" ")[-1]), name.replace(
        " 节点", ""
    ).replace(bandwidth, "")


class WorkingThreads:
    threads = {}

    @classmethod
    def register(cls, name) -> None:
        """
        注册一个线程,并启动它
        """
        if cls.hasThread(name):
            raise RuntimeError("This thread has already been registered.")
        thread = QThread()
        thread.start()
        cls.threads[name] = thread

    @classmethod
    def getThread(cls, name) -> Optional[QThread]:
        """
        获取一个正在运行的线程
        """
        if cls.hasThread(name):
            return cls.threads[name]
        else:
            raise RuntimeError("This thread is not running or not exists.")

    @classmethod
    def closeThread(cls, name) -> bool:
        """
        关闭一个正在运行的线程
        """
        if cls.hasThread(name):
            th = cls.threads.pop(name)
            th.quit()
            th.wait()
            th.deleteLater()
            return True
        else:
            return False

    @classmethod
    def closeAllThreads(cls) -> None:
        """
        关闭所有正在运行的线程
        """
        for th in cls.threads.values():
            th.quit()
            th.wait()
            th.deleteLater()
        cls.threads.clear()

    @classmethod
    def hasThread(cls, name) -> bool:
        rv = cls.threads.get(name, None)
        if rv is None:
            return False
        if not rv.isRunning():
            return False
        return True

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("This class is not allowed to be instantiated.")

    def __call__(self, *args, **kwargs):
        raise RuntimeError("This class is not allowed to be instantiated.")


class FrpcConsoleVariables:
    totalLogList = []
    singleLogDict = {}
    bridgeDict = {}
