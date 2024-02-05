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
from typing import Optional, Iterable, Callable, Dict, List
from time import sleep, time
from datetime import datetime
from requests import get, head
from concurrent.futures import ThreadPoolExecutor, wait


import psutil
from PyQt5.QtCore import QUrl, QThread, QThreadPool, QObject, pyqtSignal
from PyQt5.QtGui import QDesktopServices

from .. import VERSION


def initMELauncher():
    """
    初始化程序
    """

    folders = [
        "frpc",
    ]
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
            with open(file, "rb") as f:
                fileSha1 = hashlib.sha1(f.read()).hexdigest()
            rv.append({"file": file, "result": fileSha1 == sha1})
        else:
            rv.append({"file": file, "result": True})
    return rv

def unixTimeStampToTime(timeStamp):
    return datetime.fromtimestamp(timeStamp)

def check24HoursPassed(timeStamp):
    current_timestamp = int(time())
    if current_timestamp > (timeStamp + 86400):
        return True
    else:
        return False

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


class Downloader(QObject):
    msg = pyqtSignal(str)
    finishSignal = pyqtSignal()

    def __init__(self, url, threadCnt, fileName, parent=None):
        super().__init__(parent)
        self.url = url
        self.threadCnt = threadCnt
        self.fileName = fileName
        self.getSize = 0
        self.info = {
            "main": {"progress": 0, "speed": ""},
            "sub": {
                "progress": [0 for i in range(threadCnt)],  # 子线程状态
                "stat": [1 for i in range(threadCnt)],  # 下载状态
            },
        }
        r = head(
            self.url,
            headers={
                "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47 MEFrpLauncher/{VERSION}",  # noqa
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",  # noqa
            },
        )
        # 状态码显示302则迭代寻找文件
        while r.status_code == 302:
            self.url = r.headers["Location"]
            r = head(self.url)
        self.size = int(r.headers["Content-Length"])
        # self.msg.emit("该文件大小为: {} B".format(self.size))

    def down(self, start, end, threadId, chunkSize=10240):
        rawStart = start
        for _ in range(10):
            try:
                headers = {
                    "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36 Edg/93.0.961.47 MEFrpLauncher/{VERSION}",  # noqa
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",  # noqa
                    "Range": "bytes={}-{}".format(start, end),
                }
                r = get(self.url, headers=headers, timeout=10, stream=True)
                size = 0
                with open(self.fileName, "rb+") as fp:
                    fp.seek(start)
                    for chunk in r.iter_content(chunk_size=chunkSize):
                        if chunk:
                            self.getSize += chunkSize
                            fp.write(chunk)
                            start += chunkSize
                            size += chunkSize
                            progress = round(size / (end - rawStart) * 100, 2)
                            self.info["sub"]["progress"][threadId - 1] = progress
                            self.info["sub"]["stat"][threadId - 1] = 1
                return
            except Exception:
                self.down(start, end, threadId)
        # self.msg.emit(f"{start}-{end} 下载失败")
        self.info["sub"]["start"][threadId - 1] = 0

    def show(self):
        self.t = DownloaderThread(self.getSize, self.size, self.info, self.parent())
        self.t.msg.connect(self.msg.emit)
        self.t.start()

    def run(self):
        fp = open(self.fileName, "wb")
        # self.msg.emit(f"正在初始化下载文件: {self.fileName}")
        fp.truncate(self.size)
        fp.close()
        part = self.size // self.threadCnt
        pool = ThreadPoolExecutor(max_workers=self.threadCnt + 1)
        futures = []
        for i in range(self.threadCnt):
            start = part * i
            if i == self.threadCnt - 1:
                end = self.size
            else:
                end = start + part - 1
            futures.append(pool.submit(self.down, start, end, i + 1))
        futures.append(pool.submit(self.show))
        # print(f"正在使用{self.threadCnt}个线程进行下载...")
        wait(futures)
        self.finishSignal.emit()
        self.deleteLater()
        # print(f"{self.fileName} 下载完成")


class DownloaderThread(QThread):
    msg = pyqtSignal(str)

    def __init__(self, getSize, size, info, parent=None):
        super().__init__(parent)
        self.getSize = getSize
        self.size = size
        self.info = info

    def run(self):
        speed = self.getSize
        sleep(0.5)
        speed = int((self.getSize - speed) * 2 / 1024)
        if speed > 1024:
            speed = f"{round(speed / 1024, 2)} M/s"
        else:
            speed = f"{speed} KB/s"
        progress = round(self.getSize / self.size * 100, 2)
        self.info["main"]["progress"] = progress
        self.info["main"]["speed"] = speed
        # self.msg.emit("下载进度: {}% 速度: {}".format(progress, speed))
        if progress >= 100:
            self.terminate()
