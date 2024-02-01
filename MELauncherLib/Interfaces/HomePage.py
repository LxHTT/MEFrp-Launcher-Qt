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

from ..APIController.Connections import (
    GetUserInfoThread,
    GetSettingThread,
    RefreshUserTokenThread,
    JSONReturnModel,
)
from ..Resources import *  # noqa: F403 F401
from ..AppController.encrypt import getAuthorization
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
)


class HomeAPI(QObject):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def getUserInfoAPI(self) -> GetUserInfoThread:
        return GetUserInfoThread(getAuthorization(), parent=self)

    def getSysSettingAPI(self) -> GetSettingThread:
        return GetSettingThread(parent=self)

    def refreshUserTokenAPI(self, authorization: str) -> RefreshUserTokenThread:
        return RefreshUserTokenThread(authorization, parent=self)


class HomePage(QWidget, HomeAPI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("HomePage")

        self.gridLayout = QGridLayout(self)
        self.gridLayout.setObjectName("gridLayout")
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
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
        self.announcementContent.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.announcementContent.setObjectName("announcementContent")
        self.verticalLayout.addWidget(self.announcementContent)
        self.gridLayout.addWidget(self.announcementWidget, 2, 1, 1, 1)
        self.userInfoWidget = OutlinedCardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.userInfoWidget.sizePolicy().hasHeightForWidth())
        self.userInfoWidget.setSizePolicy(sizePolicy)
        self.userInfoWidget.setMinimumSize(QSize(270, 0))
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
        self.userInfoSC.setGeometry(QRect(0, 0, 252, 330))
        self.userInfoSC.setObjectName("userInfoSC")
        self.userInfoScrollArea.setWidget(self.userInfoSC)
        self.userInfoWidgetLayout.addWidget(self.userInfoScrollArea)
        self.gridLayout.addWidget(self.userInfoWidget, 2, 0, 2, 1)
        self.frpcStatusWidget = OutlinedCardWidget(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusWidget.sizePolicy().hasHeightForWidth())
        self.frpcStatusWidget.setSizePolicy(sizePolicy)
        self.frpcStatusWidget.setMinimumSize(QSize(0, 100))
        self.frpcStatusWidget.setMaximumSize(QSize(16777215, 100))
        self.frpcStatusWidget.setObjectName("frpcStatusWidget")
        self.horizontalLayout = QHBoxLayout(self.frpcStatusWidget)
        self.horizontalLayout.setContentsMargins(25, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frpcStatusTitle = SubtitleLabel(self.frpcStatusWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusTitle.sizePolicy().hasHeightForWidth())
        self.frpcStatusTitle.setSizePolicy(sizePolicy)
        self.frpcStatusTitle.setObjectName("frpcStatusTitle")
        self.horizontalLayout.addWidget(self.frpcStatusTitle)
        self.frpcStatusContent = BodyLabel(self.frpcStatusWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcStatusContent.sizePolicy().hasHeightForWidth())
        self.frpcStatusContent.setSizePolicy(sizePolicy)
        self.frpcStatusContent.setText("")
        self.frpcStatusContent.setObjectName("frpcStatusContent")
        self.horizontalLayout.addWidget(self.frpcStatusContent)
        self.gridLayout.addWidget(self.frpcStatusWidget, 3, 1, 1, 1)

        self.TitleLabel.setText(" 主页")
        self.announcementTitle.setText(" 公告")
        self.userInfoTitle.setText(" 用户信息")
        self.frpcStatusTitle.setText("Frpc客户端状态")
        self.spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)

    def getUserInfoFunc(self):
        self.getUserInfoThread = self.getUserInfoAPI()
        self.getUserInfoThread.returnSlot.connect(self.getUserInfoAPIParser)
        self.getUserInfoThread.start()

    @pyqtSlot(JSONReturnModel)
    def getUserInfoAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "Success!":
            try:
                self.userInfoWidgetLayout.removeItem(self.spacerItem)
            except Exception:
                pass
            for i in reversed(range(self.userInfoWidgetLayout.count())):
                try:
                    if self.userInfoWidgetLayout.itemAt(i).widget().objectName() != "userInfoTitle":
                        self.userInfoWidgetLayout.itemAt(i).widget().setParent(None)
                    else:
                        pass
                except AttributeError:
                    pass
                try:
                    if self.userInfoWidgetLayout.itemAt(i).widget().objectName() != "userInfoTitle":
                        self.userInfoWidgetLayout.itemAt(i).widget().deleteLater()
                    else:
                        pass
                    del self.userInfoWidgetLayout.itemAt(i).widget
                except AttributeError:
                    pass

            self.userInfoWidgetLayout.addWidget(
                UserInfoAvatarWidget(model.data["username"], self.userInfoSC)
            )
            self.userInfoWidgetLayout.addWidget(
                UserInfoWidget("用户ID", str(model.data["id"]), self.userInfoSC)
            )

            self.userInfoWidgetLayout.addWidget(
                UserInfoWidget("用户组", model.data["group"], self.userInfoSC)
            )
            self.userInfoWidgetLayout.addWidget(
                UserInfoWidget(
                    "出网带宽", str(model.data["outbound"] / 128) + " Mbps", self.userInfoSC
                )
            )
            self.userInfoWidgetLayout.addWidget(
                UserInfoWidget(
                    "剩余流量", str(model.data["traffic"] / 1024) + " GB", self.userInfoSC
                )
            )

            self.userInfoWidgetLayout.addWidget(
                UserInfoWidget("邮箱", model.data["email"], self.userInfoSC)
            )
            self.userInfoWidgetLayout.addWidget(
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
            self.userInfoWidgetLayout.addWidget(
                UserInfoPushWidget(
                    "Token泄露？",
                    "重置",
                    self.refreshUserTokenPreFunc,
                    self.userInfoSC,
                )
            )
            self.userInfoWidgetLayout.addItem(self.spacerItem)
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
        self.refreshUserTokenThread.finished.connect(self.getUserInfoFunc)
        self.refreshUserTokenThread.start()

    def getSysSettingFunc(self):
        self.getSysSettingThread = self.getSysSettingAPI()
        self.getSysSettingThread.returnSlot.connect(self.getSysSettingAPIParser)
        self.getSysSettingThread.start()

    @pyqtSlot(JSONReturnModel)
    def getSysSettingAPIParser(self, model: JSONReturnModel):
        if model.status == 200 or model.message == "成功":
            self.announcementContent.setText(
                "  "
                + TextWrap()
                .wrap(
                    model.data["announce"][0]["content"].replace("，", "，\n"),
                    400,
                    False,
                )[0]
                .replace("\n", "\n  ")
            )
        else:
            InfoBar.error(
                title="错误",
                content=model.message,
                duration=1500,
                position=InfoBarPosition.TOP,
                parent=self,
            )
