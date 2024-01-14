import enum
import hashlib
from os import makedirs, path as osp
from types import TracebackType
from typing import Type, Optional, Iterable, Callable, Dict, List

import psutil
from PyQt5.QtCore import QUrl, QThread, QThreadPool
from PyQt5.QtGui import QDesktopServices


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


class ExceptionFilterMode(enum.Enum):
    RAISE_AND_PRINT = enum.auto()  # 过滤：弹框提示，也会抛出异常
    RAISE = enum.auto()  # 过滤：不弹框提示，但是会抛出异常
    PASS = enum.auto()  # 过滤：不弹框提示，也不抛出异常，就当做什么都没发生


def exceptionFilter(
    ty: Type[BaseException], value: BaseException, _traceback: TracebackType
) -> ExceptionFilterMode:
    """
    过滤异常
    """
    if isinstance(value, AttributeError) and "MessageBox" in str(value):
        return ExceptionFilterMode.PASS
        return ExceptionFilterMode.RAISE
    if isinstance(value, RuntimeError) and "wrapped C/C++ object of type" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "raise test" in str(value):
        return ExceptionFilterMode.RAISE
    if isinstance(value, Exception) and "pass test" in str(value):
        return ExceptionFilterMode.PASS
    if isinstance(value, Exception) and "print test" in str(value):
        return ExceptionFilterMode.RAISE_AND_PRINT

    return ExceptionFilterMode.RAISE_AND_PRINT


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
