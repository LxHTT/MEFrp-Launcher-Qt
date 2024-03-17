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
    QFrame,
    QGridLayout,
    QHBoxLayout,
)
from PyQt5.QtCore import Qt, QRect, QSize, QObject, pyqtSlot

from ..AppController.Utils import check24HoursPassed
from ..AppController.encrypt import updateToken
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
    MessageBox,
    InfoBar,
    InfoBarPosition,
    TextWrap,
    TonalPushButton,
    FluentIcon as FIF,
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
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.frpcStatusWidget = OutlinedCardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusWidget.sizePolicy().hasHeightForWidth())
        self.frpcStatusWidget.setSizePolicy(sizePolicy)
        self.frpcStatusWidget.setMinimumSize(QSize(0, 100))
        self.frpcStatusWidget.setMaximumSize(QSize(16777215, 100))
        self.frpcStatusWidget.setObjectName("frpcStatusWidget")
        self.frpcStatusLayout = QHBoxLayout(self.frpcStatusWidget)
        self.frpcStatusLayout.setContentsMargins(25, -1, -1, -1)
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
        self.gridLayout.addWidget(self.frpcStatusWidget, 7, 1, 1, 1)
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.userSignWidget = OutlinedCardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userSignWidget.sizePolicy().hasHeightForWidth())
        self.userSignWidget.setSizePolicy(sizePolicy)
        self.userSignWidget.setMinimumSize(QSize(270, 200))
        self.userSignWidget.setMaximumSize(QSize(270, 200))
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
        self.gridLayout.addWidget(self.userSignWidget, 2, 0, 1, 1)
        self.userInfoWidget = OutlinedCardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userInfoWidget.sizePolicy().hasHeightForWidth())
        self.userInfoWidget.setSizePolicy(sizePolicy)
        self.userInfoWidget.setMinimumSize(QSize(270, 0))
        self.userInfoWidget.setMaximumSize(QSize(270, 16777215))
        self.userInfoWidget.setObjectName("userInfoWidget")
        self.userInfoWidgetLayout = QVBoxLayout(self.userInfoWidget)
        self.userInfoWidgetLayout.setObjectName("userInfoWidgetLayout")
        self.userInfoTitle = SubtitleLabel(self.userInfoWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userInfoTitle.sizePolicy().hasHeightForWidth())
        self.userInfoTitle.setSizePolicy(sizePolicy)
        self.userInfoTitle.setObjectName("userInfoTitle")
        self.userInfoWidgetLayout.addWidget(self.userInfoTitle)
        self.userInfoScrollArea = NormalSmoothScrollArea(self.userInfoWidget)
        self.userInfoScrollArea.setFrameShape(QFrame.NoFrame)
        self.userInfoScrollArea.setFrameShadow(QFrame.Plain)
        self.userInfoScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.userInfoScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.userInfoScrollArea.setWidgetResizable(True)
        self.userInfoScrollArea.setAlignment(Qt.AlignCenter)
        self.userInfoScrollArea.setObjectName("userInfoScrollArea")
        self.userInfoSC = QWidget()
        self.userInfoSC.setGeometry(QRect(0, 0, 252, 217))
        self.userInfoSC.setObjectName("userInfoSC")
        self.userInfoSCFakeLayout = QVBoxLayout(self.userInfoSC)
        self.userInfoSCFakeLayout.setContentsMargins(0, 0, 0, 0)
        self.userInfoSCFakeLayout.setObjectName("userInfoSCFakeLayout")
        self.userInfoSCRealLayout = QVBoxLayout()
        self.userInfoSCRealLayout.setObjectName("userInfoSCRealLayout")
        self.userInfoSCFakeLayout.addLayout(self.userInfoSCRealLayout)
        self.userInfoScrollArea.setWidget(self.userInfoSC)
        self.userInfoWidgetLayout.addWidget(self.userInfoScrollArea)
        self.gridLayout.addWidget(self.userInfoWidget, 3, 0, 5, 1)
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
        self.announcementContent = BodyLabel(self.announcementWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.announcementContent.sizePolicy().hasHeightForWidth())
        self.announcementContent.setSizePolicy(sizePolicy)
        self.announcementContent.setText("")
        self.announcementContent.setObjectName("announcementContent")
        self.verticalLayout.addWidget(self.announcementContent)
        self.gridLayout.addWidget(self.announcementWidget, 2, 1, 5, 1)

        self.TitleLabel.setText("主页")
        self.announcementTitle.setText(" 公告")
        self.userInfoTitle.setText(" 用户信息")
        self.frpcStatusTitle.setText("Frpc客户端状态")
        self.userSignTitle.setText(" 签到")
        self.userSignBtn.setText("签到")
        self.userSignBtn.setEnabled(False)
        self.userSignBtn.clicked.connect(self.userSignFunc)
        self.announcementContent.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.spacerItem = QSpacerItem(20, 10, QSizePolicy.Fixed, QSizePolicy.Expanding)

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
            try:
                self.userInfoSCRealLayout.removeItem(self.spacerItem)
            except Exception:
                pass
            for i in reversed(range(self.userInfoSCRealLayout.count())):
                try:
                    if self.userInfoSCRealLayout.itemAt(i).widget().objectName() != "userInfoTitle":
                        self.userInfoSCRealLayout.itemAt(i).widget().setParent(None)
                    else:
                        pass
                except AttributeError:
                    pass
                try:
                    if self.userInfoSCRealLayout.itemAt(i).widget().objectName() != "userInfoTitle":
                        self.userInfoSCRealLayout.itemAt(i).widget().deleteLater()
                    else:
                        pass
                    del self.userInfoSCRealLayout.itemAt(i).widget
                except AttributeError:
                    pass

            self.userInfoSCRealLayout.addWidget(
                UserInfoAvatarWidget(model.data["username"], self.userInfoSC)
            )
            self.userInfoSCRealLayout.addWidget(
                UserInfoWidget("用户ID", str(model.data["id"]), self.userInfoSC)
            )

            self.userInfoSCRealLayout.addWidget(
                UserInfoWidget("用户组", model.data["group"], self.userInfoSC)
            )
            self.userInfoSCRealLayout.addWidget(
                UserInfoWidget(
                    "出网带宽", str(model.data["outbound"] / 128) + " Mbps", self.userInfoSC
                )
            )
            self.userInfoSCRealLayout.addWidget(
                UserInfoWidget(
                    "剩余流量", str(model.data["traffic"] / 1024) + " GB", self.userInfoSC
                )
            )

            self.userInfoSCRealLayout.addWidget(
                UserInfoWidget("邮箱", model.data["email"], self.userInfoSC)
            )
            self.userInfoSCRealLayout.addItem(self.spacerItem)
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
            alertText = "\n\n\n"
            if model.data["alert"]["error"]["title"] != "null":
                alertText += f"  运行异常！\n  {model.data['alert']['error']['content']}\n"
            else:
                alertText += f"  运行正常\n  {model.data['alert']['info']['content']}\n"
            self.announcementContent.setText(
                (
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
                + alertText
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
