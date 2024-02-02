from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSpacerItem,
    QSizePolicy,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QApplication,
)
from PyQt5.QtCore import Qt, QRect, QSize, QObject, pyqtSlot

from ..AppController.Utils import check24HoursPassed
from ..AppController.encrypt import updateToken
from ..APIController import (
    GetUserInfoThread,
    UserSignThread,
    UserGetSignInfoThread,
    GetSettingThread,
    RefreshUserTokenThread,
    JSONReturnModel,
)
from ..Resources import *  # noqa: F403 F401
from ..AppController.encrypt import getToken
from .Multiplex.ScollArea import NormalSmoothScrollArea
from .Multiplex.UserInfoWidgets import UserInfoAvatarWidget, UserInfoPushWidget, UserInfoWidget

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
)


class HomeAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def getUserInfoAPI(self) -> GetUserInfoThread:
        return GetUserInfoThread(authorization=getToken(), parent=self)

    def getSysSettingAPI(self) -> GetSettingThread:
        return GetSettingThread(parent=self)

    def refreshUserTokenAPI(self) -> RefreshUserTokenThread:
        return RefreshUserTokenThread(authorization=getToken(), parent=self)

    def userSignAPI(self) -> UserSignThread:
        return UserSignThread(authorization=getToken(), parent=self)

    def userGetSignInfoAPI(self) -> UserGetSignInfoThread:
        return UserGetSignInfoThread(authorization=getToken(), parent=self)


class HomePage(QWidget, HomeAPI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomePage")

        self.setContentsMargins(8, 8, 8, 8)
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
        self.userSignWidget.setMaximumSize(QSize(16777215, 200))
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
        self.userSignContent.setText("")
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

        self.TitleLabel.setText(" 主页")
        self.announcementTitle.setText(" 公告")
        self.userInfoTitle.setText(" 用户信息")
        self.frpcStatusTitle.setText("Frpc客户端状态")
        self.userSignTitle.setText(" 签到")
        self.userSignBtn.setText("签到")
        self.userSignBtn.setEnabled(False)
        self.userSignBtn.clicked.connect(self.userSignFunc)
        self.announcementContent.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def getUserInfoFunc(self):
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
            self.userInfoSCRealLayout.addWidget(
                (
                    w := UserInfoPushWidget(
                        "Token",
                        "复制",
                        lambda: QApplication.clipboard().setText(model.data["token"]),
                        self.userInfoSC,
                    )
                )
            )
            w.actionBtn.clicked.connect(
                lambda: InfoBar.success(
                    title="已复制",
                    content="请妥善保存，切勿泄露。\n已经泄露的请立即重置！",
                    duration=1500,
                    position=InfoBarPosition.TOP,
                    parent=self,
                )
            )
            self.userInfoSCRealLayout.addWidget(
                UserInfoPushWidget(
                    "Token泄露？",
                    "重置",
                    self.refreshUserTokenPreFunc,
                    self.userInfoSC,
                )
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

    def refreshUserTokenPreFunc(self):
        w = MessageBox(
            "确认重置Token？",
            "确认重置 Token 吗？这将使当前 Token 失效并生成新的 Token。",
            parent=self,
        )
        w.yesButton.setText("确定")
        w.yesButton.clicked.connect(self.refreshUserTokenFunc)
        w.cancelButton.setText("取消")
        w.exec_()

    def refreshUserTokenFunc(self):
        self.refreshUserTokenThread = self.refreshUserTokenAPI()
        self.refreshUserTokenThread.returnSlot.connect(self.refreshUserTokenAPIParser)
        self.refreshUserTokenThread.start()

    @pyqtSlot(JSONReturnModel)
    def refreshUserTokenAPIParser(self, model: JSONReturnModel):
        attr = "success"
        if model.status != 200 or model.message != "Token更新成功":
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
            updateToken(model.data["newToken"])
            self.getUserInfoFunc()
            self.userGetSignInfoFunc()

    def getSysSettingFunc(self):
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
                alertText += f"  运行正常\n  {model.data['alert']['success']['content']}\n"
            self.announcementContent.setText(
                "  "
                + TextWrap()
                .wrap(
                    str(model.data["announce"][0]["content"]).replace("，", "，\n"),
                    400,
                    False,
                )[0]
                .replace("\n", "\n  ")
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

    def userGetSignInfoFunc(self):
        self.userGetSignInfoThread = self.userGetSignInfoAPI()
        self.userGetSignInfoThread.returnSlot.connect(self.userGetSignInfoAPIParser)
        self.userGetSignInfoThread.start()

    @pyqtSlot(JSONReturnModel)
    def userGetSignInfoAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "Success!":
            text = "  用户ID：{id}\n  用户名：{username}\n  总签到次数：{totalsign}\n  总获得流量：{totaltraffic}".format(
                id=model.data["id"],
                username=model.data["username"],
                totalsign=model.data["totalsign"],
                totaltraffic=model.data["totaltraffic"],
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
        self.userSignThread = self.userSignAPI()
        self.userSignThread.returnSlot.connect(self.userSignAPIParser)
        self.userSignThread.start()

    def userSignAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "Success!":
            self.userGetSignInfoFunc()
        else:
            InfoBar.warning(
                title="提示",
                content=model.message,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )
