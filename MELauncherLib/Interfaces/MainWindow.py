import sys
from platform import system as systemName, version as systemVersion
from traceback import format_exception
from types import TracebackType
from typing import Type, Union

from qmaterialwidgets.common.icon import MaterialIconBase
from qmaterialwidgets.components.navigation import NavigationPushButton


from ..FrpcController.completer import checkFrpc, downloadFrpc

from .Multiplex.ExceptionWidget import ExceptionWidget
from ..AppController.ExceptionHandler import ExceptionFilterMode, exceptionFilter
from ..AppController.Utils import WorkingThreads
from ..AppController.Settings import getStyleSheetFromFile, cfg
from ..AppController.encrypt import getUser, getPassword, saveUser, updateToken
from ..APIController import JSONReturnModel

from ..Resources import *  # noqa: F403 F401

from qmaterialwidgets import (
    BottomNavMaterialWindow,
    SplashScreen,
    FluentIcon as FIF,
    MessageBox,
    isDarkTheme,
    setTheme,
    BottomNavMaterialTitleBar,
    InfoBar,
    InfoBarPosition,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QThreadPool, pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget

from .. import VERSION
from .HomePage import HomePage
from .CreateTunnelPage import CreateTunnelPage
from .Multiplex.FirstGuide import GuideAPI


class METitleBar(BottomNavMaterialTitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setQss()

    def setQss(self):
        self.setStyleSheet(
            getStyleSheetFromFile(
                f":/built-InQss/title_bar_{'dark' if isDarkTheme() else 'light'}.qss"
            )
        )


class MEMainWindow(BottomNavMaterialWindow):
    def __init__(self) -> None:
        super().__init__()

        self.oldHook = sys.excepthook
        sys.excepthook = self.catchExceptions
        self.titleBar.setParent(None)
        self.titleBar.deleteLater()
        self.setTitleBar(METitleBar(self))
        self.initWindow()
        self.mySetTheme()
        self.initNavigation()
        self.finishSetup()

    def initWindow(self):
        """初始化窗口"""
        self.setWindowTitle(f"镜缘映射 ME Frp 启动器 {VERSION}")
        self.setWindowIcon(QIcon(":/built-InIcons/MEFrp.ico"))

        # self.splashScreen = SplashScreen(self.windowIcon(), self)
        # self.splashScreen.setIconSize(QSize(106, 106))
        # self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(int(w // 1.5), int(h // 1.5))
        self.setMinimumSize(int(w // 1.5), int(h // 1.7))
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        cfg.themeChanged.connect(self.titleBar.setQss)
        QApplication.processEvents()

    def initNavigation(self):
        self.stackedWidget.currentChanged.connect(self.pageChangedEvent)
        self.homePage = HomePage(self)
        self.createTunnelPage = CreateTunnelPage(self)
        self.addSubInterface(
            interface=self.homePage, icon=FIF.HOME, text="主页", selectedIcon=FIF.HOME_FILL
        )
        self.addSubInterface(interface=self.createTunnelPage, icon=FIF.ADD, text="新建隧道")

        self.navigationInterface.setCurrentItem(self.homePage.objectName())

    def mySetTheme(self):
        if "windows" in systemName().lower():
            if int(systemVersion().split(".")[-1]) >= 22000:
                self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
            else:
                pass
        setTheme(cfg.theme)

    def finishSetup(self):
        from time import sleep

        w = False
        if not checkFrpc(False):
            try:
                downloadFrpc()
            except LookupError:
                w = True
        else:
            w = False
            sleep(1.5)
        del sleep
        # self.splashScreen.finish()
        if w:
            w = MessageBox(
                "Frpc补全失败",
                "MEFrp-Launcher无法获取您对应系统的Frpc。\n请手动下载Frpc并解压到frpc目录。\n",
                self,
            )
            w.cancelButton.setParent(None)
            w.exec_()
        else:
            pass
        if not cfg.get(cfg.isFirstGuideFinished):
            self.runFirstGuide()
        else:
            self.runReLogin()
        self.homePage.getSysSettingFunc()
        self.homePage.frpcStatusContent.setText(checkFrpc(True))

    def pageChangedEvent(self):
        if self.stackedWidget.currentIndex() == 1:
            self.createTunnelPage.refreshNodeBtn.click()

    def closeEvent(self, a0) -> None:
        # close thread pool
        QThreadPool.globalInstance().clear()
        QThreadPool.globalInstance().waitForDone()
        QThreadPool.globalInstance().deleteLater()

        try:
            WorkingThreads.closeAllThreads()
            super().closeEvent(a0)
        finally:
            super().closeEvent(a0)

    def catchExceptions(
        self, ty: Type[BaseException], value: BaseException, _traceback: TracebackType
    ):
        """
        全局捕获异常，并弹窗显示
        :param ty: 异常的类型
        :param value: 异常的对象
        :param _traceback: 异常的traceback
        """
        # 过滤部分异常
        mode = exceptionFilter(ty, value, _traceback)

        if mode == ExceptionFilterMode.PASS:
            # MCSL2Logger.info(f"忽略了异常：{ty} {value} {_traceback}")
            return

        elif mode == ExceptionFilterMode.RAISE:
            # MCSL2Logger.error(msg=f"捕捉到异常：{ty} {value} {_traceback}")
            return self.oldHook(ty, value, _traceback)

        elif mode == ExceptionFilterMode.RAISE_AND_PRINT:
            tracebackString = "".join(format_exception(ty, value, _traceback))
            # MCSL2Logger.error(msg=tracebackString)
            exceptionWidget = ExceptionWidget(tracebackString)
            box = MessageBox(
                title=self.tr("程序出现异常"), content="", parent=self, icon=FIF.QUESTION
            )
            box.yesButton.setText(self.tr("确认并复制到剪切板"))
            box.cancelButton.setText(self.tr("知道了"))
            box.contentLabel.setParent(None)
            box.contentLabel.deleteLater()
            del box.contentLabel
            box.textLayout.addWidget(exceptionWidget.exceptionScrollArea)
            box.yesButton.clicked.connect(lambda: QApplication.clipboard().setText(tracebackString))
            box.yesButton.clicked.connect(box.deleteLater)
            box.cancelButton.clicked.connect(box.deleteLater)
            box.yesButton.clicked.connect(exceptionWidget.deleteLater)
            box.cancelButton.clicked.connect(exceptionWidget.deleteLater)
            box.exec_()
            return self.oldHook(ty, value, _traceback)

    def runFirstGuide(self):
        """
        运行首次使用引导
        """
        from .Multiplex.FirstGuide import GuideInterface

        self.guideInterface = GuideInterface(self)
        self.guideInterface.finish.connect(self.homePage.getUserInfoFunc)
        self.guideInterface.finish.connect(self.homePage.userGetSignInfoFunc)
        self.guideInterface.show()
        self.guideInterface.raise_()
        self.resize(self.width() - 1, self.height() - 1)
        self.resize(self.width() + 1, self.height() + 1)
        self.titleBar.raise_()

    def runReLogin(self):
        self.loginThread = GuideAPI(self).loginAPI(getUser(), getPassword())
        self.loginThread.returnSlot.connect(self.reLoginParser)
        self.loginThread.start()

    @pyqtSlot(JSONReturnModel)
    def reLoginParser(self, model: JSONReturnModel):
        attr = "success"
        if model.status != 200 or model.data == 0:
            attr = "error"
        else:
            pass

        getattr(InfoBar, attr)(
            title="错误" if attr == "error" else "成功",
            content=f"自动登录失败，请在设置页重新登录。\nAPI提示：{model.message}"
            if attr == "error"
            else "已自动登录，欢迎回来。",
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )
        if attr == "success":
            updateToken(model.data["access_token"])
            saveUser(getUser(), getPassword())
            self.homePage.getUserInfoFunc()
            self.homePage.userGetSignInfoFunc()
