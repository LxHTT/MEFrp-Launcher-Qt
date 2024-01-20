import sys
from platform import system as systemName
from platform import version as systemVersion
from traceback import format_exception
from types import TracebackType
from typing import Type

from .Multiplex.ExceptionWidget import ExceptionWidget
from ..AppController.ExceptionHandler import ExceptionFilterMode, WorkingThreads, exceptionFilter
from ..AppController.SettingsController import getStyleSheetFromFile, cfg

from ..Resources import *  # noqa: F403 F401

from qmaterialwidgets import (
    BottomNavMaterialWindow,
    SplashScreen,
    FluentIcon as FIF,
    MessageBox,
    setTheme,
    isDarkTheme,
    BottomNavMaterialTitleBar,
    FilledLineEdit,
    TextPushButton,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QThreadPool, Qt
from PyQt5.QtWidgets import QApplication, QDialogButtonBox

from .. import VERSION
from .HomePage import HomePage


class MEMainWindow(BottomNavMaterialWindow):
    def __init__(self) -> None:
        super().__init__()

        self.oldHook = sys.excepthook
        sys.excepthook = self.catchExceptions
        self.titleBar.deleteLater()
        self.titleBar = BottomNavMaterialTitleBar(self)
        self.initWindow()
        self.mySetTheme()
        self.initNavigation()
        self.finishSetup()

    def initWindow(self):
        """初始化窗口"""

        self.setWindowTitle(f"镜缘映射 MEFrp 启动器 {VERSION} - Qt!")
        self.titleBar.titleLabel.setStyleSheet(
            getStyleSheetFromFile(
                f":/built-InQss/title_bar_{'dark' if isDarkTheme() else 'light'}.qss"
            )
        )
        self.setWindowIcon(QIcon(":/built-InIcons/MEFrp.ico"))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.resize(int(w // 1.5), int(h // 1.5))
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.show()
        QApplication.processEvents()

    def initNavigation(self):
        self.homePage = HomePage(self)
        self.addSubInterface(
            interface=self.homePage, icon=FIF.HOME, text="主页", selectedIcon=FIF.HOME_FILL
        )
        self.navigationInterface.setCurrentItem(self.homePage.objectName())

    def mySetTheme(self):
        if "windows" in systemName().lower():
            if int(systemVersion().split(".")[-1]) >= 22000:
                self.windowEffect.setMicaEffect(self.winId(), isDarkMode=isDarkTheme())
            else:
                pass
        setTheme(cfg.theme)

    def finishSetup(self):
        # from time import sleep
        # sleep(2)
        self.splashScreen.finish()
        self.checkLogin()

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

    def checkLogin(self):
        if not cfg.get(cfg.isLoggedIn):
            w = MessageBox(title="登录到 ME Frp", content="", parent=self, icon=FIF.VPN)

            userNameEdit = FilledLineEdit(w)
            userNameEdit.setLabel("邮箱或用户名")

            pwdEdit = FilledLineEdit(w)
            pwdEdit.setLabel("密码")

            registerBtn = TextPushButton(w)
            registerBtn.setText("注册")
            registerBtn.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)

            forgotPwdBtn = TextPushButton(w)
            forgotPwdBtn.setText("找回密码")
            forgotPwdBtn.setAttribute(Qt.WidgetAttribute.WA_LayoutUsesWidgetRect)

            w.contentLabel.setParent(None)
            w.textLayout.addWidget(userNameEdit)
            w.textLayout.addWidget(pwdEdit)
            w.cancelButton.setText("取消")
            w.yesButton.setText("登录")
            w.buttonGroup.addButton(registerBtn, QDialogButtonBox.ActionRole)
            w.buttonGroup.addButton(forgotPwdBtn, QDialogButtonBox.ActionRole)
            w.exec_()
