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

import sys
from platform import system as systemName, version as systemVersion
from traceback import format_exception
from types import TracebackType
from typing import Type

from ..FrpcController.completer import checkFrpc, downloadFrpc

from .Multiplex.ExceptionWidget import ExceptionWidget
from ..AppController.ExceptionHandler import ExceptionFilterMode, exceptionFilter
from ..AppController.Settings import getStyleSheetFromFile, cfg
from ..AppController.encrypt import getUser, getPassword, saveUser, updateToken
from ..APIController import JSONReturnModel

from ..Resources import *  # noqa: F403 F401

from qmaterialwidgets import (
    SplashScreen,
    FluentIcon as FIF,
    MessageBox,
    isDarkTheme,
    setTheme,
    MaterialTitleBar,
    InfoBar,
    InfoBarPosition,
    NavigationItemPosition,
    MaterialStyleSheet,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QThreadPool, pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication

from .. import VERSION
from .HomePage import HomePage
from .CreateTunnelPage import CreateTunnelPage
from .TunnelManagerPage import TunnelManagerPage
from .FrpcLogPage import FrpcLogPage
from .SettingsPage import SettingsPage
from .AboutPage import AboutPage
from .Multiplex.FirstGuide import GuideAPI
from .Multiplex.SystemTray import SystemTrayContainer

if cfg.get(cfg.navigationPosition) == "Bottom":
    from qmaterialwidgets import BottomNavMaterialWindow as BaseWindowClass
else:
    from qmaterialwidgets import MaterialWindow as BaseWindowClass


class METitleBar(MaterialTitleBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.setQss()

    def setQss(self):
        self.setStyleSheet(
            getStyleSheetFromFile(
                f":/built-InQss/title_bar_{'dark' if isDarkTheme() else 'light'}.qss"
            )
        )


class MEMainWindow(BaseWindowClass):
    def __init__(self) -> None:
        super().__init__()

        self.setupSystemTray()
        # self.oldHook = sys.excepthook
        # sys.excepthook = self.catchExceptions
        self.titleBar.setParent(None)
        self.titleBar.deleteLater()

        self.homePage = HomePage(self)
        self.createTunnelPage = CreateTunnelPage(self)
        self.tunnelManagerPage = TunnelManagerPage(self)
        self.frpcLogPage = FrpcLogPage(self)
        self.settingsPage = SettingsPage(self)
        self.aboutPage = AboutPage(self)

        self.setTitleBar(METitleBar(self))
        self.initWindow()
        self.mySetTheme()
        self.initNavigation()
        self.finishSetup()

    def setupSystemTray(self):
        self.systemTrayIcon = SystemTrayContainer(
            showLauncherSlot=self.showLauncher, exitSlot=self.close, parent=self
        ).getTrayIcon()
        self.systemTrayIcon.show()

    def showLauncher(self):
        self.show()
        self.showNormal()
        self.activateWindow()
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.updateFrameless()

    def initWindow(self):
        """初始化窗口"""
        self.setWindowTitle(f"MEFrp-Launcher-Qt v{VERSION}")
        self.setWindowIcon(QIcon(":/built-InIcons/MEFrp.ico"))

        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(int(w // 1.5), int(h // 1.5))
        self.setMinimumSize(int(w // 2.3), int(h // 1.7))
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        cfg.themeChanged.connect(self.titleBar.setQss)
        QApplication.processEvents()

    def closeEvent(self, a0) -> None:
        if self.frpcLogPage.isAnyFrpcRunning():
            a0.ignore()
            box = MessageBox(
                self.tr("无法退出 MEFrp-Launcher-Qt"),
                self.tr("仍有Frpc正在运行，启动器将最小化到系统托盘。"),
                parent=self,
            )
            box.yesButton.setText(self.tr("了解"))
            box.yesButton.clicked.connect(
                lambda: self.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
            )
            box.cancelButton.setParent(None)
            box.cancelButton.deleteLater()
            box.exec()
            return

        # close thread pool
        QThreadPool.globalInstance().clear()
        QThreadPool.globalInstance().waitForDone()
        QThreadPool.globalInstance().deleteLater()
        self.systemTrayIcon.setVisible(False)
        QApplication.quit()
        super().closeEvent(a0)

    def initNavigation(self):
        self.stackedWidget.currentChanged.connect(self.pageChangedEvent)
        self.addSubInterface(
            interface=self.homePage, icon=FIF.HOME, text="主页", selectedIcon=FIF.HOME_FILL
        )
        self.addSubInterface(interface=self.createTunnelPage, icon=FIF.ADD, text="新建隧道")
        self.addSubInterface(
            interface=self.tunnelManagerPage, icon=FIF.LIBRARY_FILL, text="隧道管理"
        )
        self.addSubInterface(interface=self.frpcLogPage, icon=FIF.COMMAND_PROMPT, text="Frpc日志")
        if cfg.get(cfg.navigationPosition) == "Bottom":
            self.addSubInterface(interface=self.settingsPage, icon=FIF.SETTING, text="设置")
            self.addSubInterface(
                interface=self.aboutPage,
                icon=FIF.INFO,
                text="关于",
            )
        else:
            self.addSubInterface(
                interface=self.settingsPage,
                icon=FIF.SETTING,
                text="设置",
                position=NavigationItemPosition.BOTTOM,
            )
            self.addSubInterface(
                interface=self.aboutPage,
                icon=FIF.INFO,
                text="关于",
                position=NavigationItemPosition.BOTTOM,
            )

        self.navigationInterface.setCurrentItem(self.homePage.objectName())

    def mySetTheme(self):
        if "windows" in systemName().lower():
            if int(systemVersion().split(".")[-1]) >= 22000:
                self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
            else:
                pass
        setTheme(cfg.get(cfg.themeMode))
        cfg.themeChanged.connect(lambda: MaterialStyleSheet.MATERIAL_WINDOW.apply(self))

    def finishSetup(self):
        w = False
        if not checkFrpc(False):
            downloadFrpc(self)
        else:
            w = False
        self.splashScreen.finish()
        if w:
            w = MessageBox(
                title="Frpc补全失败",
                content="MEFrp-Launcher 无法获取您对应系统的Frpc。\n请手动下载Frpc并解压到frpc目录。\n",  # noqa: E501
                icon=FIF.APPLICATION,
                parent=self,
            )
            w.cancelButton.setParent(None)
            w.exec()
        else:
            pass
        if not cfg.get(cfg.isFirstGuideFinished):
            self.runFirstGuide()
        else:
            self.runReLogin()
        if cfg.get(cfg.autoCheckUpdate):
            self.settingsPage.checkUpdate(parent=self)
        self.homePage.getSysSettingFunc()
        self.homePage.frpcStatusContent.setText(checkFrpc(True))
        self.settingsPage.frpcVresionLabel.setText(self.homePage.frpcStatusContent.text())

    def pageChangedEvent(self):
        if self.stackedWidget.currentIndex() == 1:
            self.createTunnelPage.refreshNodeBtn.click()
        if self.stackedWidget.currentIndex() == 2:
            self.tunnelManagerPage.getTunnelListFunc()

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
            return

        elif mode == ExceptionFilterMode.RAISE:
            return self.oldHook(ty, value, _traceback)

        elif mode == ExceptionFilterMode.RAISE_AND_PRINT:
            tracebackString = "".join(format_exception(ty, value, _traceback))
            exceptionWidget = ExceptionWidget(tracebackString)
            box = MessageBox(
                title=self.tr("MEFrp-Launcher 出现未经处理的异常"),
                content="",
                icon=FIF.QUESTION,
                parent=self,
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
            box.exec()
            return self.oldHook(ty, value, _traceback)

    def runFirstGuide(self):
        """
        运行首次使用引导
        """
        from .Multiplex.FirstGuide import GuideInterface

        self.guideInterface = GuideInterface(self)
        self.guideInterface.finish.connect(self.settingsPage.updateAccountStatus)
        self.guideInterface.finish.connect(self.homePage.getUserInfoFunc)
        self.guideInterface.finish.connect(self.homePage.userGetSignInfoFunc)
        self.guideInterface.show()
        self.guideInterface.raise_()
        self.resize(self.width() - 1, self.height() - 1)
        self.resize(self.width() + 1, self.height() + 1)
        self.stackedWidget.setCurrentWidget(self.homePage)
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
            self.settingsPage.updateAccountStatus()
            updateToken(model.data["access_token"])
            saveUser(getUser(), getPassword())
            self.homePage.getUserInfoFunc()
            self.homePage.userGetSignInfoFunc()
