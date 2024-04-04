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

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QGridLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QRect, QSize, QObject, pyqtSlot

from ..AppController.Utils import UserGroup, check24HoursPassed
from ..APIController import (
    GetUserInfoThread,
    UserSignThread,
    UserGetSignInfoThread,
    GetSettingThread,
    JSONReturnModel,
)
from ..Resources import *  # noqa: F403 F401
from ..AppController.encrypt import getToken
from .Multiplex.ScollArea import NormalSmoothScrollArea
from .Multiplex.UserInfoWidgets import UserInfoAvatarWidget, UserInfoWidget

from qmaterialwidgets import (
    BodyLabel,
    OutlinedCardWidget,
    SubtitleLabel,
    TitleLabel,
    InfoBarIcon,
    InfoBar,
    InfoBarPosition,
    TextWrap,
    TonalPushButton,
)


class HomeAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def getUserInfoAPI(self) -> GetUserInfoThread:
        return GetUserInfoThread(authorization=getToken(), parent=self)

    def getSysSettingAPI(self) -> GetSettingThread:
        return GetSettingThread(parent=self)

    def userSignAPI(self) -> UserSignThread:
        return UserSignThread(authorization=getToken(), parent=self)

    def userGetSignInfoAPI(self) -> UserGetSignInfoThread:
        return UserGetSignInfoThread(authorization=getToken(), parent=self)


class HomePage(QWidget, HomeAPI):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(8, 8, 8, 8)
        self.setObjectName("HomePage")
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 3)
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 2)
        self.announcementWidget = OutlinedCardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.announcementWidget.sizePolicy().hasHeightForWidth())
        self.announcementWidget.setSizePolicy(sizePolicy)
        self.announcementWidget.setObjectName("announcementWidget")
        self.verticalLayout = QVBoxLayout(self.announcementWidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.announcementTitle = SubtitleLabel(self.announcementWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.announcementTitle.sizePolicy().hasHeightForWidth())
        self.announcementTitle.setSizePolicy(sizePolicy)
        self.announcementTitle.setObjectName("announcementTitle")
        self.verticalLayout.addWidget(self.announcementTitle)
        self.announcementContentSC = NormalSmoothScrollArea(self.announcementWidget)
        self.announcementContentSC.setWidgetResizable(True)
        self.announcementContentSC.setObjectName("announcementContentSC")
        self.announcementContentSCWidget = QWidget()
        self.announcementContentSCWidget.setGeometry(QRect(0, 0, 376, 375))
        self.announcementContentSCWidget.setObjectName("announcementContentSCWidget")
        self.announcementContentLayout = QGridLayout(self.announcementContentSCWidget)
        self.announcementContentLayout.setContentsMargins(6, 6, 6, 6)
        self.announcementContentLayout.setSpacing(4)
        self.announcementContentLayout.setObjectName("announcementContentLayout")
        self.announcementContent = BodyLabel(self.announcementContentSCWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.announcementContent.sizePolicy().hasHeightForWidth())
        self.announcementContent.setSizePolicy(sizePolicy)
        self.announcementContent.setOpenExternalLinks(True)
        self.announcementContent.setTextFormat(Qt.MarkdownText)
        self.announcementContent.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.announcementContent.setObjectName("announcementContent")
        self.announcementContentLayout.addWidget(self.announcementContent, 0, 0, 1, 1)
        self.announcementContentSC.setWidget(self.announcementContentSCWidget)
        self.verticalLayout.addWidget(self.announcementContentSC)
        self.gridLayout.addWidget(self.announcementWidget, 3, 2, 1, 1)
        self.serviceStatusWidget = QWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.serviceStatusWidget.sizePolicy().hasHeightForWidth())
        self.serviceStatusWidget.setSizePolicy(sizePolicy)
        self.serviceStatusWidget.setMinimumSize(QSize(0, 50))
        self.serviceStatusWidget.setObjectName("serviceStatusWidget")
        self.serviceStatusLayout = QVBoxLayout(self.serviceStatusWidget)
        self.serviceStatusLayout.setContentsMargins(0, 0, 0, 0)
        self.serviceStatusLayout.setSpacing(0)
        self.serviceStatusLayout.setObjectName("serviceStatusLayout")
        self.gridLayout.addWidget(self.serviceStatusWidget, 2, 2, 1, 1)
        self.homePageSC = NormalSmoothScrollArea(self)
        self.homePageSC.setMinimumSize(QSize(270, 0))
        self.homePageSC.setWidgetResizable(True)
        self.homePageSC.setObjectName("homePageSC")
        self.homePageSCWidget = QWidget()
        self.homePageSCWidget.setGeometry(QRect(0, 0, 274, 516))
        self.homePageSCWidget.setObjectName("homePageSCWidget")
        self.homePageSCLayout = QGridLayout(self.homePageSCWidget)
        self.homePageSCLayout.setContentsMargins(0, 0, 0, 0)
        self.homePageSCLayout.setHorizontalSpacing(4)
        self.homePageSCLayout.setVerticalSpacing(8)
        self.homePageSCLayout.setObjectName("homePageSCLayout")
        self.userInfoWidget = OutlinedCardWidget(self.homePageSCWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userInfoWidget.sizePolicy().hasHeightForWidth())
        self.userInfoWidget.setSizePolicy(sizePolicy)
        self.userInfoWidget.setFixedSize(QSize(270, 300))
        self.userInfoWidget.setObjectName("userInfoWidget")
        self.userInfoLayout = QVBoxLayout(self.userInfoWidget)
        self.userInfoLayout.setObjectName("userInfoLayout")
        self.userInfoTitle = SubtitleLabel(self.userInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userInfoTitle.sizePolicy().hasHeightForWidth())
        self.userInfoTitle.setSizePolicy(sizePolicy)
        self.userInfoTitle.setObjectName("userInfoTitle")
        self.userInfoLayout.addWidget(self.userInfoTitle)
        self.homePageSCLayout.addWidget(self.userInfoWidget, 2, 0, 2, 2)
        self.userSignWidget = OutlinedCardWidget(self.homePageSCWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userSignWidget.sizePolicy().hasHeightForWidth())
        self.userSignWidget.setSizePolicy(sizePolicy)
        self.userSignWidget.setMinimumSize(QSize(270, 200))
        self.userSignWidget.setMaximumSize(QSize(270, 16777215))
        self.userSignWidget.setObjectName("userSignWidget")
        self.gridLayout_2 = QGridLayout(self.userSignWidget)
        self.gridLayout_2.setContentsMargins(9, -1, -1, 11)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.userSignContent = BodyLabel(self.userSignWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userSignContent.sizePolicy().hasHeightForWidth())
        self.userSignContent.setSizePolicy(sizePolicy)
        self.userSignContent.setObjectName("userSignContent")
        self.gridLayout_2.addWidget(self.userSignContent, 1, 0, 2, 1)
        self.userSignBtn = TonalPushButton(self.userSignWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userSignBtn.sizePolicy().hasHeightForWidth())
        self.userSignBtn.setSizePolicy(sizePolicy)
        self.userSignBtn.setObjectName("userSignBtn")
        self.gridLayout_2.addWidget(self.userSignBtn, 3, 0, 1, 1)
        self.userSignTitle = SubtitleLabel(self.userSignWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userSignTitle.sizePolicy().hasHeightForWidth())
        self.userSignTitle.setSizePolicy(sizePolicy)
        self.userSignTitle.setObjectName("userSignTitle")
        self.gridLayout_2.addWidget(self.userSignTitle, 0, 0, 1, 1)
        self.homePageSCLayout.addWidget(self.userSignWidget, 0, 0, 1, 1)
        self.frpcStatusWidget = OutlinedCardWidget(self.homePageSCWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusWidget.sizePolicy().hasHeightForWidth())
        self.frpcStatusWidget.setSizePolicy(sizePolicy)
        self.frpcStatusWidget.setFixedSize(QSize(270, 100))
        self.frpcStatusWidget.setObjectName("frpcStatusWidget")
        self.frpcStatusLayout = QHBoxLayout(self.frpcStatusWidget)
        self.frpcStatusLayout.setContentsMargins(-1, -1, -1, -1)
        self.frpcStatusLayout.setObjectName("frpcStatusLayout")
        self.frpcStatusTitle = SubtitleLabel(self.frpcStatusWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusTitle.sizePolicy().hasHeightForWidth())
        self.frpcStatusTitle.setSizePolicy(sizePolicy)
        self.frpcStatusTitle.setObjectName("frpcStatusTitle")
        self.frpcStatusLayout.addWidget(self.frpcStatusTitle)
        self.frpcStatusContent = BodyLabel(self.frpcStatusWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusContent.sizePolicy().hasHeightForWidth())
        self.frpcStatusContent.setSizePolicy(sizePolicy)
        self.frpcStatusContent.setText("")
        self.frpcStatusContent.setObjectName("frpcStatusContent")
        self.frpcStatusLayout.addWidget(self.frpcStatusContent)
        self.homePageSCLayout.addWidget(self.frpcStatusWidget, 1, 0, 1, 1)
        self.homePageSC.setWidget(self.homePageSCWidget)
        self.gridLayout.addWidget(self.homePageSC, 2, 0, 2, 2)

        self.frpcStatusContent.setText("")
        self.TitleLabel.setText("主页")
        self.announcementTitle.setText(" 公告")
        self.userInfoTitle.setText(" 用户信息")
        self.frpcStatusTitle.setText(" Frpc")
        self.userSignTitle.setText(" 签到")
        self.userSignBtn.setText("签到")
        self.userSignBtn.setEnabled(False)
        self.userSignBtn.clicked.connect(self.userSignFunc)
        self.announcementContent.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.announcementContent.setWordWrap(True)

    def getUserInfoFunc(self):
        if hasattr(self, "getUserInfoThread"):
            if self.getUserInfoThread.isRunning():
                return
        self.getUserInfoThread = self.getUserInfoAPI()
        self.getUserInfoThread.returnSlot.connect(self.getUserInfoAPIParser)
        self.getUserInfoThread.start()

    @pyqtSlot(JSONReturnModel)
    def getUserInfoAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "Success!":
            for i in reversed(range(self.userInfoLayout.count())):
                try:
                    if self.userInfoLayout.itemAt(i).widget().objectName() != "userInfoTitle":
                        self.userInfoLayout.itemAt(i).widget().setParent(None)
                    else:
                        pass
                except AttributeError:
                    pass
                try:
                    if self.userInfoLayout.itemAt(i).widget().objectName() != "userInfoTitle":
                        self.userInfoLayout.itemAt(i).widget().deleteLater()
                    else:
                        pass
                    del self.userInfoLayout.itemAt(i).widget
                except AttributeError:
                    pass

            self.userInfoLayout.addWidget(
                UserInfoAvatarWidget(model.data["username"], self.userInfoWidget)
            )
            self.userInfoLayout.addWidget(
                UserInfoWidget("用户ID", str(model.data["id"]), self.userInfoWidget)
            )

            self.userInfoLayout.addWidget(
                UserInfoWidget("用户组", UserGroup(model.data["group"]), self.userInfoWidget)
            )
            self.userInfoLayout.addWidget(
                UserInfoWidget(
                    "出网带宽",
                    str(int(model.data["outbound"] / 128)) + " Mbps",
                    self.userInfoWidget,
                )
            )
            self.userInfoLayout.addWidget(
                UserInfoWidget(
                    "剩余流量", str(model.data["traffic"] / 1024) + " GB", self.userInfoWidget
                )
            )

            self.userInfoLayout.addWidget(
                UserInfoWidget("邮箱", model.data["email"], self.userInfoWidget)
            )
        else:
            InfoBar.error(
                title="错误",
                content=model.message,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )

    def getSysSettingFunc(self):
        if hasattr(self, "getSysSettingThread"):
            if self.getSysSettingThread.isRunning():
                return
        self.getSysSettingThread = self.getSysSettingAPI()
        self.getSysSettingThread.returnSlot.connect(self.getSysSettingAPIParser)
        self.getSysSettingThread.start()

    @pyqtSlot(JSONReturnModel)
    def getSysSettingAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "成功":
            for i in reversed(range(self.serviceStatusLayout.count())):
                try:
                    self.serviceStatusLayout.itemAt(i).widget().setParent(None)
                except AttributeError:
                    pass
                try:
                    self.serviceStatusLayout.itemAt(i).widget().deleteLater()
                    del self.serviceStatusLayout.itemAt(i).widget
                except AttributeError:
                    pass
            self.serviceStatusInfoBar = InfoBar(
                icon=InfoBarIcon.SUCCESS
                if model.data["alert"]["error"]["title"] == "null"
                else InfoBarIcon.ERROR,
                title="服务正常" if model.data["alert"]["error"]["title"] == "null" else "服务异常",
                content=model.data["alert"]["info"]["content"]
                if model.data["alert"]["error"]["title"] == "null"
                else model.data["alert"]["error"]["content"],
                orient=Qt.Horizontal,
                isClosable=False,
                duration=-1,
                position=InfoBarPosition.NONE,
                parent=self.serviceStatusWidget,
            )
            sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.serviceStatusInfoBar.sizePolicy().hasHeightForWidth())
            self.serviceStatusInfoBar.setSizePolicy(sizePolicy)
            self.serviceStatusLayout.addWidget(self.serviceStatusInfoBar)
            self.announcementContent.setText(
                "  "
                + TextWrap()
                .wrap(
                    "  \n\n".join([
                        str(content).replace("，", "，\n")
                        for content in (
                            item[1]["content"] for item in model.data["announce"].items()
                        )
                    ]),
                    400,
                    False,
                )[0]
                .replace("\n", "\n  ")
                if model.data["announce"] is not None
                else "  暂无公告"
            )
        else:
            InfoBar.error(
                title="错误",
                content=model.message,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )

    def userGetSignInfoFunc(self, isSigning: bool = False):
        if hasattr(self, "userGetSignInfoThread"):
            if self.userGetSignInfoThread.isRunning():
                return
        self.userGetSignInfoThread = self.userGetSignInfoAPI()
        self.userGetSignInfoThread.returnSlot.connect(
            lambda x: self.userGetSignInfoAPIParser(model=x, isSigning=isSigning)
        )
        self.userGetSignInfoThread.start()

    @pyqtSlot(JSONReturnModel)
    def userGetSignInfoAPIParser(self, model: JSONReturnModel, isSigning: bool = False):
        if model.status == 200 or model.message == "Success!":
            text = "  用户ID：{id}\n  用户名：{username}\n  总签到次数：{totalsign} 次\n  总获得流量：{totaltraffic} GB".format(  # noqa: E501
                id=model.data["id"],
                username=model.data["username"],
                totalsign=model.data["totalsign"],
                totaltraffic=model.data["totaltraffic"],
            )
            if isSigning:
                oldTraffic = int(
                    self.userSignContent.text().split("  总获得流量：")[1].replace(" GB", "")
                )
                InfoBar.success(
                    title="签到成功",
                    content="获得 {traffic}GB 流量".format(
                        traffic=str(int(model.data["totaltraffic"]) - oldTraffic)
                    ),
                    duration=1500,
                    position=InfoBarPosition.TOP,
                    parent=self,
                )
            self.userSignContent.setText(text)
            self.userSignBtn.setEnabled(check24HoursPassed(model.data["signdate"]))
        else:
            InfoBar.error(
                title="错误",
                content=model.message,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )

    def userSignFunc(self):
        if hasattr(self, "userSignThread"):
            if self.userSignThread.isRunning():
                return
        self.userSignThread = self.userSignAPI()
        self.userSignThread.returnSlot.connect(self.userSignAPIParser)
        self.userSignThread.start()

    def userSignAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "Success!":
            self.userGetSignInfoFunc(isSigning=True)
        else:
            InfoBar.warning(
                title="提示",
                content=model.message,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )
