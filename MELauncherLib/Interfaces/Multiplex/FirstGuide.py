from PyQt5.QtCore import QSize, Qt, QEvent, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import (
    QGridLayout,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QHBoxLayout,
    QLineEdit,
)
from qmaterialwidgets import (
    FilledPushButton,
    FilledToggleToolButton,
    LargeTitleLabel,
    LineEdit,
    SubtitleLabel,
    TextPushButton,
    TonalPushButton,
    isDarkTheme,
    FluentIcon as FIF,
    InfoBar,
    InfoBarPosition,
)

from ...AppController.encrypt import saveUser, refreshToken
from ...APIController.Connections import (
    LoginThread,
    ForgotPasswordThread,
    RegisterThread,
    SendRegisterEmailThread,
    JSONReturnModel,
)
from ...AppController.Settings import cfg
from .StackedWidget import ChildStackedWidget
from typing import List


class GuideAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def loginAPI(self, username: str, password: str) -> LoginThread:
        return LoginThread(username=username, password=password, parent=self)

    def forgotPasswordAPI(self, email: str, username: str) -> ForgotPasswordThread:
        return ForgotPasswordThread(email=email, username=username, parent=self)

    def registerAPI(self, email: str, username: str, password: str, code: str) -> RegisterThread:
        return RegisterThread(
            email=email, username=username, password=password, code=code, parent=self
        )

    def sendRegisterEmailAPI(self, email: str) -> SendRegisterEmailThread:
        return SendRegisterEmailThread(email=email, parent=self)


class GuideInterface(QWidget, GuideAPI):
    finish = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setObjectName("WelcomeWidget")
        self.gridLayout = QGridLayout(self)

        self.stackedWidget = ChildStackedWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.setupInterface()
        self.extraInterfaceSet()
        self.setupText()
        self.connectSlot()
        self.stackedWidget.setCurrentIndex(0)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        if parent:
            parent.installEventFilter(self)
        self.update()

    def setupInterface(self):
        self.welcomePage = QWidget()
        self.welcomePage.setObjectName("welcomePage")
        self.welcomePageLayout = QGridLayout(self.welcomePage)
        self.welcomePageLayout.setObjectName("welcomePageLayout")
        self.welcomeText = LargeTitleLabel(self.welcomePage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.welcomeText.sizePolicy().hasHeightForWidth())
        self.welcomeText.setSizePolicy(sizePolicy)
        self.welcomeText.setObjectName("welcomeText")
        self.welcomePageLayout.addWidget(self.welcomeText, 2, 6, 1, 1)
        self.welcomeGoBtn = FilledPushButton(self.welcomePage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.welcomeGoBtn.sizePolicy().hasHeightForWidth())
        self.welcomeGoBtn.setSizePolicy(sizePolicy)
        self.welcomeGoBtn.setObjectName("welcomeGoBtn")
        self.welcomePageLayout.addWidget(self.welcomeGoBtn, 6, 6, 1, 1)
        self.mefrpText = LargeTitleLabel(self.welcomePage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mefrpText.sizePolicy().hasHeightForWidth())
        self.mefrpText.setSizePolicy(sizePolicy)
        self.mefrpText.setObjectName("mefrpText")
        self.welcomePageLayout.addWidget(self.mefrpText, 3, 6, 1, 1)
        self.introText = SubtitleLabel(self.welcomePage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.introText.sizePolicy().hasHeightForWidth())
        self.introText.setSizePolicy(sizePolicy)
        self.introText.setObjectName("introText")
        self.welcomePageLayout.addWidget(self.introText, 4, 6, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.welcomePageLayout.addItem(spacerItem, 5, 6, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.welcomePageLayout.addItem(spacerItem1, 1, 0, 7, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.welcomePageLayout.addItem(spacerItem2, 1, 7, 7, 1)
        spacerItem3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.welcomePageLayout.addItem(spacerItem3, 1, 6, 1, 1)
        spacerItem4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.welcomePageLayout.addItem(spacerItem4, 7, 6, 1, 1)
        self.stackedWidget.addWidget(self.welcomePage)
        self.accountSetPage = QWidget()
        self.accountSetPage.setObjectName("accountSetPage")
        self.accountSetPageLayout = QGridLayout(self.accountSetPage)
        self.accountSetPageLayout.setObjectName("accountSetPageLayout")
        self.accountTip = SubtitleLabel(self.accountSetPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accountTip.sizePolicy().hasHeightForWidth())
        self.accountTip.setSizePolicy(sizePolicy)
        self.accountTip.setObjectName("accountTip")
        self.accountSetPageLayout.addWidget(self.accountTip, 2, 1, 1, 1)
        spacerItem5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.accountSetPageLayout.addItem(spacerItem5, 0, 1, 1, 1)
        self.noAccountBtn = TonalPushButton(self.accountSetPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.noAccountBtn.sizePolicy().hasHeightForWidth())
        self.noAccountBtn.setSizePolicy(sizePolicy)
        self.noAccountBtn.setMinimumSize(QSize(180, 0))
        self.noAccountBtn.setObjectName("noAccountBtn")
        self.accountSetPageLayout.addWidget(self.noAccountBtn, 5, 1, 1, 1)
        self.hasAccountBtn = FilledPushButton(self.accountSetPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hasAccountBtn.sizePolicy().hasHeightForWidth())
        self.hasAccountBtn.setSizePolicy(sizePolicy)
        self.hasAccountBtn.setMinimumSize(QSize(180, 0))
        self.hasAccountBtn.setObjectName("hasAccountBtn")
        self.accountSetPageLayout.addWidget(self.hasAccountBtn, 4, 1, 1, 1)
        spacerItem6 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.accountSetPageLayout.addItem(spacerItem6, 3, 1, 1, 1)
        self.accountText = LargeTitleLabel(self.accountSetPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.accountText.sizePolicy().hasHeightForWidth())
        self.accountText.setSizePolicy(sizePolicy)
        self.accountText.setObjectName("accountText")
        self.accountSetPageLayout.addWidget(self.accountText, 1, 1, 1, 1)
        spacerItem7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.accountSetPageLayout.addItem(spacerItem7, 6, 1, 1, 1)
        spacerItem8 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.accountSetPageLayout.addItem(spacerItem8, 0, 2, 7, 1)
        spacerItem9 = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.accountSetPageLayout.addItem(spacerItem9, 0, 0, 7, 1)
        self.stackedWidget.addWidget(self.accountSetPage)
        self.loginPage = QWidget()
        self.loginPage.setObjectName("loginPage")
        self.loginPageLayout = QGridLayout(self.loginPage)
        self.loginPageLayout.setObjectName("loginPageLayout")
        spacerItem10 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.loginPageLayout.addItem(spacerItem10, 7, 2, 1, 1)
        spacerItem11 = QSpacerItem(40, 436, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.loginPageLayout.addItem(spacerItem11, 0, 0, 10, 1)
        spacerItem12 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.loginPageLayout.addItem(spacerItem12, 0, 3, 10, 1)
        spacerItem13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.loginPageLayout.addItem(spacerItem13, 9, 2, 1, 1)
        self.loginBtnWidget = QWidget(self.loginPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginBtnWidget.sizePolicy().hasHeightForWidth())
        self.loginBtnWidget.setSizePolicy(sizePolicy)
        self.loginBtnWidget.setMaximumSize(QSize(370, 16777215))
        self.loginBtnWidget.setObjectName("loginBtnWidget")
        self.loginBtnWidgetLayout = QHBoxLayout(self.loginBtnWidget)
        self.loginBtnWidgetLayout.setContentsMargins(0, 0, 0, 0)
        self.loginBtnWidgetLayout.setObjectName("loginBtnWidgetLayout")
        self.loginBtn = FilledPushButton(self.loginBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginBtn.sizePolicy().hasHeightForWidth())
        self.loginBtn.setSizePolicy(sizePolicy)
        self.loginBtn.setMinimumSize(QSize(180, 0))
        self.loginBtn.setObjectName("loginBtn")
        self.loginBtnWidgetLayout.addWidget(self.loginBtn)
        self.forgotPwdBtn = TextPushButton(self.loginBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forgotPwdBtn.sizePolicy().hasHeightForWidth())
        self.forgotPwdBtn.setSizePolicy(sizePolicy)
        self.forgotPwdBtn.setMinimumSize(QSize(180, 0))
        self.forgotPwdBtn.setObjectName("forgotPwdBtn")
        self.loginBtnWidgetLayout.addWidget(self.forgotPwdBtn)
        self.loginPageLayout.addWidget(self.loginBtnWidget, 8, 2, 1, 1)
        self.usernameEdit = LineEdit(self.loginPage)
        self.usernameEdit.setMaximumSize(QSize(370, 56))
        self.usernameEdit.setPlaceholderText("")
        self.usernameEdit.setObjectName("usernameEdit")
        self.loginPageLayout.addWidget(self.usernameEdit, 5, 2, 1, 1)
        self.loginBackBtn = TextPushButton(self.loginPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginBackBtn.sizePolicy().hasHeightForWidth())
        self.loginBackBtn.setSizePolicy(sizePolicy)
        self.loginBackBtn.setObjectName("loginBackBtn")
        self.loginPageLayout.addWidget(self.loginBackBtn, 1, 2, 1, 1)
        spacerItem14 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.loginPageLayout.addItem(spacerItem14, 4, 2, 1, 1)
        spacerItem15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.loginPageLayout.addItem(spacerItem15, 0, 2, 1, 1)
        self.loginPwdWidget = QWidget(self.loginPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginPwdWidget.sizePolicy().hasHeightForWidth())
        self.loginPwdWidget.setSizePolicy(sizePolicy)
        self.loginPwdWidget.setMaximumSize(QSize(370, 70))
        self.loginPwdWidget.setObjectName("loginPwdWidget")
        self.loginPwdLayout = QHBoxLayout(self.loginPwdWidget)
        self.loginPwdLayout.setContentsMargins(0, 0, 0, 0)
        self.loginPwdLayout.setObjectName("loginPwdLayout")
        self.loginPwdEdit = LineEdit(self.loginPwdWidget)
        self.loginPwdEdit.setEchoMode(QLineEdit.Password)
        self.loginPwdEdit.setObjectName("loginPwdEdit")
        self.loginPwdLayout.addWidget(self.loginPwdEdit)
        self.loginShowPwdWidget = QWidget(self.loginPwdWidget)
        self.loginShowPwdWidget.setObjectName("loginShowPwdWidget")
        self.loginShowPwdLayout = QGridLayout(self.loginShowPwdWidget)
        self.loginShowPwdLayout.setContentsMargins(0, -1, 0, 0)
        self.loginShowPwdLayout.setHorizontalSpacing(0)
        self.loginShowPwdLayout.setObjectName("loginShowPwdLayout")
        self.loginShowPwdBtn = FilledToggleToolButton(self.loginShowPwdWidget)
        self.loginShowPwdBtn.setObjectName("loginShowPwdBtn")
        self.loginShowPwdLayout.addWidget(self.loginShowPwdBtn, 0, 0, 1, 1)
        self.loginPwdLayout.addWidget(self.loginShowPwdWidget)
        self.loginPageLayout.addWidget(self.loginPwdWidget, 6, 2, 1, 1)
        spacerItem16 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.loginPageLayout.addItem(spacerItem16, 2, 2, 1, 1)
        self.loginText = LargeTitleLabel(self.loginPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginText.sizePolicy().hasHeightForWidth())
        self.loginText.setSizePolicy(sizePolicy)
        self.loginText.setObjectName("loginText")
        self.loginPageLayout.addWidget(self.loginText, 3, 2, 1, 1)
        self.stackedWidget.addWidget(self.loginPage)
        self.forgotPwdPage = QWidget()
        self.forgotPwdPage.setObjectName("forgotPwdPage")
        self.forgotPwdPageLayout = QGridLayout(self.forgotPwdPage)
        self.forgotPwdPageLayout.setObjectName("forgotPwdPageLayout")
        spacerItem17 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.forgotPwdPageLayout.addItem(spacerItem17, 8, 1, 1, 1)
        self.forgotEmailEdit = LineEdit(self.forgotPwdPage)
        self.forgotEmailEdit.setMaximumSize(QSize(370, 56))
        self.forgotEmailEdit.setEchoMode(QLineEdit.Normal)
        self.forgotEmailEdit.setObjectName("forgotEmailEdit")
        self.forgotPwdPageLayout.addWidget(self.forgotEmailEdit, 7, 1, 1, 1)
        spacerItem18 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.forgotPwdPageLayout.addItem(spacerItem18, 1, 1, 1, 1)
        spacerItem19 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.forgotPwdPageLayout.addItem(spacerItem19, 5, 1, 1, 1)
        self.forgotPwdText = LargeTitleLabel(self.forgotPwdPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.forgotPwdText.sizePolicy().hasHeightForWidth())
        self.forgotPwdText.setSizePolicy(sizePolicy)
        self.forgotPwdText.setObjectName("forgotPwdText")
        self.forgotPwdPageLayout.addWidget(self.forgotPwdText, 4, 1, 1, 1)
        self.forgotUsernameEdit = LineEdit(self.forgotPwdPage)
        self.forgotUsernameEdit.setMaximumSize(QSize(370, 56))
        self.forgotUsernameEdit.setPlaceholderText("")
        self.forgotUsernameEdit.setObjectName("forgotUsernameEdit")
        self.forgotPwdPageLayout.addWidget(self.forgotUsernameEdit, 6, 1, 1, 1)
        spacerItem20 = QSpacerItem(364, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.forgotPwdPageLayout.addItem(spacerItem20, 1, 2, 10, 1)
        spacerItem21 = QSpacerItem(20, 78, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.forgotPwdPageLayout.addItem(spacerItem21, 10, 1, 1, 1)
        self.sendForgotEmailBtn = FilledPushButton(self.forgotPwdPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sendForgotEmailBtn.sizePolicy().hasHeightForWidth())
        self.sendForgotEmailBtn.setSizePolicy(sizePolicy)
        self.sendForgotEmailBtn.setMinimumSize(QSize(180, 0))
        self.sendForgotEmailBtn.setObjectName("sendForgotEmailBtn")
        self.forgotPwdPageLayout.addWidget(self.sendForgotEmailBtn, 9, 1, 1, 1)
        spacerItem22 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.forgotPwdPageLayout.addItem(spacerItem22, 3, 1, 1, 1)
        spacerItem23 = QSpacerItem(40, 387, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.forgotPwdPageLayout.addItem(spacerItem23, 1, 0, 10, 1)
        self.rememberPwdBtn = TextPushButton(self.forgotPwdPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rememberPwdBtn.sizePolicy().hasHeightForWidth())
        self.rememberPwdBtn.setSizePolicy(sizePolicy)
        self.rememberPwdBtn.setMinimumSize(QSize(0, 0))
        self.rememberPwdBtn.setObjectName("rememberPwdBtn")
        self.forgotPwdPageLayout.addWidget(self.rememberPwdBtn, 2, 1, 1, 1)
        self.stackedWidget.addWidget(self.forgotPwdPage)
        self.registerPage = QWidget()
        self.registerPage.setObjectName("registerPage")
        self.registerPageLayout = QGridLayout(self.registerPage)
        self.registerPageLayout.setObjectName("registerPageLayout")
        spacerItem24 = QSpacerItem(40, 479, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.registerPageLayout.addItem(spacerItem24, 0, 1, 13, 1)
        self.registerPwdWidget = QWidget(self.registerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerPwdWidget.sizePolicy().hasHeightForWidth())
        self.registerPwdWidget.setSizePolicy(sizePolicy)
        self.registerPwdWidget.setMaximumSize(QSize(370, 70))
        self.registerPwdWidget.setObjectName("registerPwdWidget")
        self.registerPwdLayout = QHBoxLayout(self.registerPwdWidget)
        self.registerPwdLayout.setContentsMargins(0, 0, 0, 0)
        self.registerPwdLayout.setObjectName("registerPwdLayout")
        self.registerPwdEdit = LineEdit(self.registerPwdWidget)
        self.registerPwdEdit.setEchoMode(QLineEdit.Password)
        self.registerPwdEdit.setObjectName("registerPwdEdit")
        self.registerPwdLayout.addWidget(self.registerPwdEdit)
        self.registerShowPwdWidget = QWidget(self.registerPwdWidget)
        self.registerShowPwdWidget.setObjectName("registerShowPwdWidget")
        self.registerShowPwdLayout = QGridLayout(self.registerShowPwdWidget)
        self.registerShowPwdLayout.setContentsMargins(0, -1, 0, 0)
        self.registerShowPwdLayout.setHorizontalSpacing(0)
        self.registerShowPwdLayout.setObjectName("registerShowPwdLayout")
        self.registerShowPwdBtn = FilledToggleToolButton(self.registerShowPwdWidget)
        self.registerShowPwdBtn.setObjectName("registerShowPwdBtn")
        self.registerShowPwdLayout.addWidget(self.registerShowPwdBtn, 0, 0, 1, 1)
        self.registerPwdLayout.addWidget(self.registerShowPwdWidget)
        self.registerPageLayout.addWidget(self.registerPwdWidget, 7, 2, 1, 1)
        self.registerBtnWidget = QWidget(self.registerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerBtnWidget.sizePolicy().hasHeightForWidth())
        self.registerBtnWidget.setSizePolicy(sizePolicy)
        self.registerBtnWidget.setMaximumSize(QSize(370, 16777215))
        self.registerBtnWidget.setObjectName("registerBtnWidget")
        self.registerBtnLayout = QHBoxLayout(self.registerBtnWidget)
        self.registerBtnLayout.setContentsMargins(0, 0, 0, 0)
        self.registerBtnLayout.setObjectName("registerBtnLayout")
        self.registerBtn = FilledPushButton(self.registerBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerBtn.sizePolicy().hasHeightForWidth())
        self.registerBtn.setSizePolicy(sizePolicy)
        self.registerBtn.setMinimumSize(QSize(180, 0))
        self.registerBtn.setObjectName("registerBtn")
        self.registerBtnLayout.addWidget(self.registerBtn)
        self.registerHasAccountBtn = TextPushButton(self.registerBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerHasAccountBtn.sizePolicy().hasHeightForWidth())
        self.registerHasAccountBtn.setSizePolicy(sizePolicy)
        self.registerHasAccountBtn.setMinimumSize(QSize(180, 0))
        self.registerHasAccountBtn.setObjectName("registerHasAccountBtn")
        self.registerBtnLayout.addWidget(self.registerHasAccountBtn)
        self.registerPageLayout.addWidget(self.registerBtnWidget, 10, 2, 1, 1)
        spacerItem25 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.registerPageLayout.addItem(spacerItem25, 0, 2, 1, 1)
        self.registerUserNameEdit = LineEdit(self.registerPage)
        self.registerUserNameEdit.setMaximumSize(QSize(370, 56))
        self.registerUserNameEdit.setPlaceholderText("")
        self.registerUserNameEdit.setObjectName("registerUserNameEdit")
        self.registerPageLayout.addWidget(self.registerUserNameEdit, 4, 2, 1, 1)
        spacerItem26 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.registerPageLayout.addItem(spacerItem26, 11, 2, 1, 1)
        self.registerBackBtn = TextPushButton(self.registerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerBackBtn.sizePolicy().hasHeightForWidth())
        self.registerBackBtn.setSizePolicy(sizePolicy)
        self.registerBackBtn.setObjectName("registerBackBtn")
        self.registerPageLayout.addWidget(self.registerBackBtn, 1, 2, 1, 1)
        spacerItem27 = QSpacerItem(364, 339, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.registerPageLayout.addItem(spacerItem27, 0, 3, 13, 1)
        self.registerEmailEdit = LineEdit(self.registerPage)
        self.registerEmailEdit.setMaximumSize(QSize(370, 56))
        self.registerEmailEdit.setPlaceholderText("")
        self.registerEmailEdit.setObjectName("registerEmailEdit")
        self.registerPageLayout.addWidget(self.registerEmailEdit, 5, 2, 1, 1)
        self.registerVerificationWidget = QWidget(self.registerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.registerVerificationWidget.sizePolicy().hasHeightForWidth()
        )
        self.registerVerificationWidget.setSizePolicy(sizePolicy)
        self.registerVerificationWidget.setMaximumSize(QSize(370, 16777215))
        self.registerVerificationWidget.setObjectName("registerVerificationWidget")
        self.registerVerificationLayout = QHBoxLayout(self.registerVerificationWidget)
        self.registerVerificationLayout.setContentsMargins(0, 0, 0, 0)
        self.registerVerificationLayout.setObjectName("registerVerificationLayout")
        self.registerVerificationEdit = LineEdit(self.registerVerificationWidget)
        self.registerVerificationEdit.setEchoMode(QLineEdit.Password)
        self.registerVerificationEdit.setObjectName("registerVerificationEdit")
        self.registerVerificationLayout.addWidget(self.registerVerificationEdit)
        self.registerSendVerificationWidget = QWidget(self.registerVerificationWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.registerSendVerificationWidget.sizePolicy().hasHeightForWidth()
        )
        self.registerSendVerificationWidget.setSizePolicy(sizePolicy)
        self.registerSendVerificationWidget.setObjectName("registerSendVerificationWidget")
        self.registerSendVerificationLayout = QGridLayout(self.registerSendVerificationWidget)
        self.registerSendVerificationLayout.setContentsMargins(0, -1, 0, 0)
        self.registerSendVerificationLayout.setHorizontalSpacing(0)
        self.registerSendVerificationLayout.setObjectName("registerSendVerificationLayout")
        self.sendVerificationBtn = TonalPushButton(self.registerSendVerificationWidget)
        self.sendVerificationBtn.setObjectName("sendVerificationBtn")
        self.registerSendVerificationLayout.addWidget(self.sendVerificationBtn, 0, 0, 1, 1)
        self.registerVerificationLayout.addWidget(self.registerSendVerificationWidget)
        self.registerPageLayout.addWidget(self.registerVerificationWidget, 6, 2, 1, 1)
        self.registerText = LargeTitleLabel(self.registerPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.registerText.sizePolicy().hasHeightForWidth())
        self.registerText.setSizePolicy(sizePolicy)
        self.registerText.setObjectName("registerText")
        self.registerPageLayout.addWidget(self.registerText, 3, 2, 1, 1)
        spacerItem28 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.registerPageLayout.addItem(spacerItem28, 9, 2, 1, 1)
        self.stackedWidget.addWidget(self.registerPage)
        self.finishPage = QWidget()
        self.finishPage.setObjectName("finishPage")
        self.finishPageLayout = QGridLayout(self.finishPage)
        self.finishPageLayout.setObjectName("finishPageLayout")
        self.finishText = LargeTitleLabel(self.finishPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finishText.sizePolicy().hasHeightForWidth())
        self.finishText.setSizePolicy(sizePolicy)
        self.finishText.setAlignment(Qt.AlignCenter)
        self.finishText.setObjectName("finishText")
        self.finishPageLayout.addWidget(self.finishText, 1, 0, 1, 1)
        self.finishTip = SubtitleLabel(self.finishPage)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.finishTip.sizePolicy().hasHeightForWidth())
        self.finishTip.setSizePolicy(sizePolicy)
        self.finishTip.setAlignment(Qt.AlignCenter)
        self.finishTip.setObjectName("finishTip")
        self.finishPageLayout.addWidget(self.finishTip, 3, 0, 1, 1)
        self.finishSetupBtn = FilledPushButton(self.finishPage)
        self.finishSetupBtn.setObjectName("finishSetupBtn")
        self.finishPageLayout.addWidget(self.finishSetupBtn, 5, 0, 1, 1)
        spacerItem29 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.finishPageLayout.addItem(spacerItem29, 0, 0, 1, 1)
        spacerItem30 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.finishPageLayout.addItem(spacerItem30, 6, 0, 1, 1)
        spacerItem31 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.finishPageLayout.addItem(spacerItem31, 4, 0, 1, 1)
        self.stackedWidget.addWidget(self.finishPage)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)

    def setupText(self):
        self.welcomeText.setText("欢迎使用")
        self.welcomeGoBtn.setText("让我们开始吧")
        self.mefrpText.setText("ME Frp 镜缘映射 启动器")
        self.introText.setText("免费 公益 好用 低延迟 稳定的Frp内网穿透")
        self.accountTip.setText("使用ME Frp账户登录以使用此启动器的所有功能。")
        self.noAccountBtn.setText("我还没有ME Frp账户")
        self.hasAccountBtn.setText("我已有ME Frp账户")
        self.accountText.setText("ME Frp账户")
        self.loginBtn.setText("登录")
        self.forgotPwdBtn.setText("忘记密码？")
        self.usernameEdit.setLabel("邮箱或用户名")
        self.loginBackBtn.setText("返回上一页")
        self.loginPwdEdit.setLabel("密码")
        self.loginText.setText("登录ME Frp账户")
        self.forgotEmailEdit.setLabel("邮箱地址")
        self.forgotPwdText.setText("找回ME Frp账户")
        self.forgotUsernameEdit.setLabel("用户名")
        self.sendForgotEmailBtn.setText("发送重置链接")
        self.rememberPwdBtn.setText("我想起密码了")
        self.registerPwdEdit.setLabel("密码")
        self.registerBtn.setText("注册")
        self.registerHasAccountBtn.setText("我已有帐户，登录")
        self.registerUserNameEdit.setLabel("用户名")
        self.registerBackBtn.setText("返回上一页")
        self.registerEmailEdit.setLabel("邮箱")
        self.registerVerificationEdit.setLabel("邮箱验证码")
        self.sendVerificationBtn.setText("发送验证码")
        self.registerText.setText("注册ME Frp账户")
        self.finishText.setText("大功告成")
        self.finishTip.setText("欢迎使用 ME Frp 镜缘映射 启动器！")
        self.finishSetupBtn.setText("开始使用")

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() == QEvent.Resize:
                self.resize(e.size())
            elif e.type() == QEvent.ChildAdded:
                self.raise_()

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(Qt.NoPen)

        # draw background
        c = 32 if isDarkTheme() else 255
        painter.setBrush(QColor(c, c, c))
        painter.drawRect(self.rect())

    def extraInterfaceSet(self):
        self.loginBackBtn.setIcon(FIF.PAGE_LEFT)
        self.registerBackBtn.setIcon(FIF.PAGE_LEFT)
        self.rememberPwdBtn.setIcon(FIF.PAGE_LEFT)
        self.loginShowPwdBtn.setIcon(FIF.HIDE)
        self.loginShowPwdBtn.setChecked(True)
        self.registerShowPwdBtn.setIcon(FIF.HIDE)
        self.registerShowPwdBtn.setChecked(True)
        self.sendForgotEmailBtn.setIcon(FIF.SEND)
        self.sendVerificationBtn.setIcon(FIF.SEND)

    def connectSlot(self):
        self.welcomeGoBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.accountSetPage)
        )
        self.hasAccountBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.loginPage)
        )
        self.loginBackBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.accountSetPage)
        )
        self.noAccountBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.registerPage)
        )
        self.registerBackBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.accountSetPage)
        )
        self.forgotPwdBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.forgotPwdPage)
        )
        self.rememberPwdBtn.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.loginPage)
        )
        self.loginShowPwdBtn.clicked.connect(
            lambda: self.loginPwdEdit.setEchoMode(
                QLineEdit.Password if self.loginShowPwdBtn.isChecked() else QLineEdit.Normal
            )
        )
        self.registerShowPwdBtn.clicked.connect(
            lambda: self.registerPwdEdit.setEchoMode(
                QLineEdit.Password if self.registerShowPwdBtn.isChecked() else QLineEdit.Normal
            )
        )
        self.loginBtn.clicked.connect(self.loginFunc)
        self.finishSetupBtn.clicked.connect(self.kill)

    def kill(self):
        try:
            self.close()
        except Exception:
            pass
        try:
            self.setParent(None)
        except Exception:
            pass
        try:
            self.deleteLater()
        except Exception:
            pass
        cfg.set(cfg.isFirstGuideFinished, True)
        self.finish.emit()

    def textInputChecker(self, lineEditList: List[LineEdit]):
        isOk = True
        for lineEdit in lineEditList:
            if lineEdit.text() == "":
                lineEdit.setError(True)
                isOk = False
                lineEdit.textChanged.connect(self.killFocusChecker)
        if not isOk:
            InfoBar.error(
                title="错误",
                content="请完整填写所有信息",
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )
        return isOk

    def killFocusChecker(self):
        try:
            if self.sender().text() != "":
                self.sender().setError(False)
                self.sender().textChanged.disconnect()
            else:
                return
        except Exception:
            pass

    def loginFunc(self):
        if not self.textInputChecker([self.usernameEdit, self.loginPwdEdit]):
            return
        self.loginThread = self.loginAPI(
            username=self.usernameEdit.text(), password=self.loginPwdEdit.text()
        )
        self.loginThread.returnSlot.connect(self.loginAPIParser)
        self.loginThread.start()

    @pyqtSlot(JSONReturnModel)
    def loginAPIParser(self, model: JSONReturnModel):
        attr = "success"
        if model.status != 200 or model.data == 0:
            attr = "error"
        else:
            pass

        getattr(InfoBar, attr)(
            title="错误" if attr == "error" else "成功",
            content=model.message,
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )
        if attr == "success":
            self.stackedWidget.setCurrentWidget(self.finishPage)
            refreshToken(model.data["access_token"])
            saveUser(self.usernameEdit.text(), self.loginPwdEdit.text())
