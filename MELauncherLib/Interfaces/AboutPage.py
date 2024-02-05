#                    Copyright 2024, LxHTT and Aehxy.
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

from qmaterialwidgets import BodyLabel, CardWidget, SubtitleLabel, TitleLabel, TonalPushButton

from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtWidgets import QGridLayout, QSpacerItem, QSizePolicy, QWidget, QVBoxLayout, QHBoxLayout

from .. import VERSION
from .Multiplex.ScollArea import NormalSmoothScrollArea
from ..AppController.Utils import openWebUrl


class AboutPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("AboutPage")

        self.setContentsMargins(8, 8, 8, 8)
        self.gridLayout = QGridLayout(self)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 2)
        self.TitleLabel = TitleLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TitleLabel.sizePolicy().hasHeightForWidth())
        self.TitleLabel.setSizePolicy(sizePolicy)
        self.TitleLabel.setObjectName("TitleLabel")
        self.gridLayout.addWidget(self.TitleLabel, 0, 0, 1, 1)
        self.aboutScrollArea = NormalSmoothScrollArea(self)
        self.aboutScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.aboutScrollArea.setWidgetResizable(True)
        self.aboutScrollArea.setObjectName("aboutScrollArea")
        self.aboutSC = QWidget()
        self.aboutSC.setGeometry(QRect(0, 0, 621, 940))
        self.aboutSC.setObjectName("aboutSC")
        self.aboutLayout = QVBoxLayout(self.aboutSC)
        self.aboutLayout.setContentsMargins(0, 0, 0, 0)
        self.aboutLayout.setSpacing(8)
        self.aboutLayout.setObjectName("aboutLayout")
        self.launcherTitle = SubtitleLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherTitle.sizePolicy().hasHeightForWidth())
        self.launcherTitle.setSizePolicy(sizePolicy)
        self.launcherTitle.setObjectName("launcherTitle")
        self.aboutLayout.addWidget(self.launcherTitle)
        self.versionLabel = BodyLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.versionLabel.sizePolicy().hasHeightForWidth())
        self.versionLabel.setSizePolicy(sizePolicy)
        self.versionLabel.setObjectName("versionLabel")
        self.aboutLayout.addWidget(self.versionLabel)
        self.copyrightLabel = BodyLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.copyrightLabel.sizePolicy().hasHeightForWidth())
        self.copyrightLabel.setSizePolicy(sizePolicy)
        self.copyrightLabel.setObjectName("copyrightLabel")
        self.aboutLayout.addWidget(self.copyrightLabel)
        self.aboutBtnWidget = QWidget(self.aboutSC)
        self.aboutBtnWidget.setObjectName("aboutBtnWidget")
        self.aboutBtnLayout = QHBoxLayout(self.aboutBtnWidget)
        self.aboutBtnLayout.setContentsMargins(0, 0, 0, 0)
        self.aboutBtnLayout.setSpacing(8)
        self.aboutBtnLayout.setObjectName("aboutBtnLayout")
        self.openMEFrpWebBtn = TonalPushButton(self.aboutBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openMEFrpWebBtn.sizePolicy().hasHeightForWidth())
        self.openMEFrpWebBtn.setSizePolicy(sizePolicy)
        self.openMEFrpWebBtn.setObjectName("openMEFrpWebBtn")
        self.aboutBtnLayout.addWidget(self.openMEFrpWebBtn)
        self.openLauncherRepoBtn = TonalPushButton(self.aboutBtnWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openLauncherRepoBtn.sizePolicy().hasHeightForWidth())
        self.openLauncherRepoBtn.setSizePolicy(sizePolicy)
        self.openLauncherRepoBtn.setObjectName("openLauncherRepoBtn")
        self.aboutBtnLayout.addWidget(self.openLauncherRepoBtn)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.aboutBtnLayout.addItem(spacerItem1)
        self.aboutLayout.addWidget(self.aboutBtnWidget)
        self.authorTitle = SubtitleLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authorTitle.sizePolicy().hasHeightForWidth())
        self.authorTitle.setSizePolicy(sizePolicy)
        self.authorTitle.setObjectName("authorTitle")
        self.aboutLayout.addWidget(self.authorTitle)
        self.authorLabel = BodyLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authorLabel.sizePolicy().hasHeightForWidth())
        self.authorLabel.setSizePolicy(sizePolicy)
        self.authorLabel.setObjectName("authorLabel")
        self.aboutLayout.addWidget(self.authorLabel)
        spacerItem2 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.aboutLayout.addItem(spacerItem2)
        self.openSourceTitle = SubtitleLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openSourceTitle.sizePolicy().hasHeightForWidth())
        self.openSourceTitle.setSizePolicy(sizePolicy)
        self.openSourceTitle.setObjectName("openSourceTitle")
        self.aboutLayout.addWidget(self.openSourceTitle)
        self.openSourceLabel = BodyLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openSourceLabel.sizePolicy().hasHeightForWidth())
        self.openSourceLabel.setSizePolicy(sizePolicy)
        self.openSourceLabel.setObjectName("openSourceLabel")
        self.aboutLayout.addWidget(self.openSourceLabel)
        spacerItem3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.aboutLayout.addItem(spacerItem3)
        self.openSourceProjectLabel = SubtitleLabel(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openSourceProjectLabel.sizePolicy().hasHeightForWidth())
        self.openSourceProjectLabel.setSizePolicy(sizePolicy)
        self.openSourceProjectLabel.setObjectName("openSourceProjectLabel")
        self.aboutLayout.addWidget(self.openSourceProjectLabel)
        self.pyqt5CopyrightWidget = CardWidget(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt5CopyrightWidget.sizePolicy().hasHeightForWidth())
        self.pyqt5CopyrightWidget.setSizePolicy(sizePolicy)
        self.pyqt5CopyrightWidget.setMinimumSize(QSize(100, 0))
        self.pyqt5CopyrightWidget.setMaximumSize(QSize(16777215, 100))
        self.pyqt5CopyrightWidget.setObjectName("pyqt5CopyrightWidget")
        self.pyqt5CopyrightLayout = QVBoxLayout(self.pyqt5CopyrightWidget)
        self.pyqt5CopyrightLayout.setContentsMargins(16, 12, 0, 12)
        self.pyqt5CopyrightLayout.setSpacing(0)
        self.pyqt5CopyrightLayout.setObjectName("pyqt5CopyrightLayout")
        self.pyqt5Title = SubtitleLabel(self.pyqt5CopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt5Title.sizePolicy().hasHeightForWidth())
        self.pyqt5Title.setSizePolicy(sizePolicy)
        self.pyqt5Title.setObjectName("pyqt5Title")
        self.pyqt5CopyrightLayout.addWidget(self.pyqt5Title)
        self.pyqt5Copyright = BodyLabel(self.pyqt5CopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt5Copyright.sizePolicy().hasHeightForWidth())
        self.pyqt5Copyright.setSizePolicy(sizePolicy)
        self.pyqt5Copyright.setObjectName("pyqt5Copyright")
        self.pyqt5CopyrightLayout.addWidget(self.pyqt5Copyright)
        self.pyqt5License = BodyLabel(self.pyqt5CopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pyqt5License.sizePolicy().hasHeightForWidth())
        self.pyqt5License.setSizePolicy(sizePolicy)
        self.pyqt5License.setObjectName("pyqt5License")
        self.pyqt5CopyrightLayout.addWidget(self.pyqt5License)
        self.aboutLayout.addWidget(self.pyqt5CopyrightWidget)
        self.mefrplibCopyrightWidget = CardWidget(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mefrplibCopyrightWidget.sizePolicy().hasHeightForWidth())
        self.mefrplibCopyrightWidget.setSizePolicy(sizePolicy)
        self.mefrplibCopyrightWidget.setMinimumSize(QSize(100, 0))
        self.mefrplibCopyrightWidget.setMaximumSize(QSize(16777215, 100))
        self.mefrplibCopyrightWidget.setObjectName("mefrplibCopyrightWidget")
        self.mefrplibCopyrightLayout = QVBoxLayout(self.mefrplibCopyrightWidget)
        self.mefrplibCopyrightLayout.setContentsMargins(16, 12, 0, 12)
        self.mefrplibCopyrightLayout.setSpacing(0)
        self.mefrplibCopyrightLayout.setObjectName("mefrplibCopyrightLayout")
        self.mefrplibTitle = SubtitleLabel(self.mefrplibCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mefrplibTitle.sizePolicy().hasHeightForWidth())
        self.mefrplibTitle.setSizePolicy(sizePolicy)
        self.mefrplibTitle.setObjectName("mefrplibTitle")
        self.mefrplibCopyrightLayout.addWidget(self.mefrplibTitle)
        self.mefrplibCopyright = BodyLabel(self.mefrplibCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mefrplibCopyright.sizePolicy().hasHeightForWidth())
        self.mefrplibCopyright.setSizePolicy(sizePolicy)
        self.mefrplibCopyright.setObjectName("mefrplibCopyright")
        self.mefrplibCopyrightLayout.addWidget(self.mefrplibCopyright)
        self.mefrplibLicense = BodyLabel(self.mefrplibCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mefrplibLicense.sizePolicy().hasHeightForWidth())
        self.mefrplibLicense.setSizePolicy(sizePolicy)
        self.mefrplibLicense.setObjectName("mefrplibLicense")
        self.mefrplibCopyrightLayout.addWidget(self.mefrplibLicense)
        self.aboutLayout.addWidget(self.mefrplibCopyrightWidget)
        self.qmaterialwidgetsxCopyrightWidget = CardWidget(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.qmaterialwidgetsxCopyrightWidget.sizePolicy().hasHeightForWidth()
        )
        self.qmaterialwidgetsxCopyrightWidget.setSizePolicy(sizePolicy)
        self.qmaterialwidgetsxCopyrightWidget.setMinimumSize(QSize(0, 80))
        self.qmaterialwidgetsxCopyrightWidget.setMaximumSize(QSize(16777215, 80))
        self.qmaterialwidgetsxCopyrightWidget.setObjectName("qmaterialwidgetsxCopyrightWidget")
        self.qmaterialwidgetsxCopyrightLayout = QVBoxLayout(self.qmaterialwidgetsxCopyrightWidget)
        self.qmaterialwidgetsxCopyrightLayout.setContentsMargins(16, 12, 0, 12)
        self.qmaterialwidgetsxCopyrightLayout.setSpacing(0)
        self.qmaterialwidgetsxCopyrightLayout.setObjectName("qmaterialwidgetsxCopyrightLayout")
        self.qmaterialwidgetsxTitle = SubtitleLabel(self.qmaterialwidgetsxCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.qmaterialwidgetsxTitle.sizePolicy().hasHeightForWidth())
        self.qmaterialwidgetsxTitle.setSizePolicy(sizePolicy)
        self.qmaterialwidgetsxTitle.setObjectName("qmaterialwidgetsxTitle")
        self.qmaterialwidgetsxCopyrightLayout.addWidget(self.qmaterialwidgetsxTitle)
        self.qmaterialwidgetsxCopyright = BodyLabel(self.qmaterialwidgetsxCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.qmaterialwidgetsxCopyright.sizePolicy().hasHeightForWidth()
        )
        self.qmaterialwidgetsxCopyright.setSizePolicy(sizePolicy)
        self.qmaterialwidgetsxCopyright.setObjectName("qmaterialwidgetsxCopyright")
        self.qmaterialwidgetsxCopyrightLayout.addWidget(self.qmaterialwidgetsxCopyright)
        self.aboutLayout.addWidget(self.qmaterialwidgetsxCopyrightWidget)
        self.requestsCopyrightWidget = CardWidget(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsCopyrightWidget.sizePolicy().hasHeightForWidth())
        self.requestsCopyrightWidget.setSizePolicy(sizePolicy)
        self.requestsCopyrightWidget.setMinimumSize(QSize(100, 0))
        self.requestsCopyrightWidget.setMaximumSize(QSize(16777215, 100))
        self.requestsCopyrightWidget.setObjectName("requestsCopyrightWidget")
        self.requestsCopyrightLayout = QVBoxLayout(self.requestsCopyrightWidget)
        self.requestsCopyrightLayout.setContentsMargins(16, 12, 0, 12)
        self.requestsCopyrightLayout.setSpacing(0)
        self.requestsCopyrightLayout.setObjectName("requestsCopyrightLayout")
        self.requestsTitle = SubtitleLabel(self.requestsCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsTitle.sizePolicy().hasHeightForWidth())
        self.requestsTitle.setSizePolicy(sizePolicy)
        self.requestsTitle.setObjectName("requestsTitle")
        self.requestsCopyrightLayout.addWidget(self.requestsTitle)
        self.requestsCopyright = BodyLabel(self.requestsCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsCopyright.sizePolicy().hasHeightForWidth())
        self.requestsCopyright.setSizePolicy(sizePolicy)
        self.requestsCopyright.setObjectName("requestsCopyright")
        self.requestsCopyrightLayout.addWidget(self.requestsCopyright)
        self.requestsLicense = BodyLabel(self.requestsCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.requestsLicense.sizePolicy().hasHeightForWidth())
        self.requestsLicense.setSizePolicy(sizePolicy)
        self.requestsLicense.setObjectName("requestsLicense")
        self.requestsCopyrightLayout.addWidget(self.requestsLicense)
        self.aboutLayout.addWidget(self.requestsCopyrightWidget)
        self.psutilCopyrightWidget = CardWidget(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.psutilCopyrightWidget.sizePolicy().hasHeightForWidth())
        self.psutilCopyrightWidget.setSizePolicy(sizePolicy)
        self.psutilCopyrightWidget.setMinimumSize(QSize(100, 0))
        self.psutilCopyrightWidget.setMaximumSize(QSize(16777215, 100))
        self.psutilCopyrightWidget.setObjectName("psutilCopyrightWidget")
        self.psutilCopyrightLayout = QVBoxLayout(self.psutilCopyrightWidget)
        self.psutilCopyrightLayout.setContentsMargins(16, 12, 0, 12)
        self.psutilCopyrightLayout.setSpacing(0)
        self.psutilCopyrightLayout.setObjectName("psutilCopyrightLayout")
        self.psutilTitle = SubtitleLabel(self.psutilCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.psutilTitle.sizePolicy().hasHeightForWidth())
        self.psutilTitle.setSizePolicy(sizePolicy)
        self.psutilTitle.setObjectName("psutilTitle")
        self.psutilCopyrightLayout.addWidget(self.psutilTitle)
        self.psutilCopyright = BodyLabel(self.psutilCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.psutilCopyright.sizePolicy().hasHeightForWidth())
        self.psutilCopyright.setSizePolicy(sizePolicy)
        self.psutilCopyright.setObjectName("psutilCopyright")
        self.psutilCopyrightLayout.addWidget(self.psutilCopyright)
        self.psutilLicense = BodyLabel(self.psutilCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.psutilLicense.sizePolicy().hasHeightForWidth())
        self.psutilLicense.setSizePolicy(sizePolicy)
        self.psutilLicense.setObjectName("psutilLicense")
        self.psutilCopyrightLayout.addWidget(self.psutilLicense)
        self.aboutLayout.addWidget(self.psutilCopyrightWidget)
        self.pydesCopyrightWidget = CardWidget(self.aboutSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pydesCopyrightWidget.sizePolicy().hasHeightForWidth())
        self.pydesCopyrightWidget.setSizePolicy(sizePolicy)
        self.pydesCopyrightWidget.setMinimumSize(QSize(100, 0))
        self.pydesCopyrightWidget.setMaximumSize(QSize(16777215, 100))
        self.pydesCopyrightWidget.setObjectName("pydesCopyrightWidget")
        self.pydesCopyrightLayout = QVBoxLayout(self.pydesCopyrightWidget)
        self.pydesCopyrightLayout.setContentsMargins(16, 12, 0, 12)
        self.pydesCopyrightLayout.setSpacing(0)
        self.pydesCopyrightLayout.setObjectName("pydesCopyrightLayout")
        self.pydesTitle = SubtitleLabel(self.pydesCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pydesTitle.sizePolicy().hasHeightForWidth())
        self.pydesTitle.setSizePolicy(sizePolicy)
        self.pydesTitle.setObjectName("pydesTitle")
        self.pydesCopyrightLayout.addWidget(self.pydesTitle)
        self.pydesCopyright = BodyLabel(self.pydesCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pydesCopyright.sizePolicy().hasHeightForWidth())
        self.pydesCopyright.setSizePolicy(sizePolicy)
        self.pydesCopyright.setObjectName("pydesCopyright")
        self.pydesCopyrightLayout.addWidget(self.pydesCopyright)
        self.pydesLicense = BodyLabel(self.pydesCopyrightWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pydesLicense.sizePolicy().hasHeightForWidth())
        self.pydesLicense.setSizePolicy(sizePolicy)
        self.pydesLicense.setObjectName("pydesLicense")
        self.pydesCopyrightLayout.addWidget(self.pydesLicense)
        self.aboutLayout.addWidget(self.pydesCopyrightWidget)
        self.aboutScrollArea.setWidget(self.aboutSC)
        self.gridLayout.addWidget(self.aboutScrollArea, 2, 0, 1, 1)

        self.TitleLabel.setText("关于")
        self.launcherTitle.setText("MEFrp-Launcher-Qt")
        self.versionLabel.setText(f"当前版本：{VERSION}")
        self.copyrightLabel.setText("Copyright © 2024 LxHTT and Aehxy.")
        self.openMEFrpWebBtn.setText("打开 ME Frp 官网")
        self.openLauncherRepoBtn.setText("打开 GitHub 仓库")
        self.authorTitle.setText("作者")
        self.authorLabel.setText("落雪无痕LxHTT")
        self.openSourceTitle.setText("开源协议提示")
        self.openSourceLabel.setText(
            "本程序遵循 GPL-3.0 开源协议进行开源。\n您可借鉴并使用本程序源代码及思路，但不可二次分发本程序。"  # noqa: E501
        )
        self.openSourceProjectLabel.setText("开源项目引用列表")
        self.pyqt5Title.setText("PyQt5")
        self.pyqt5Copyright.setText("Copyright © 2023 Riverbank Computing Limited.")
        self.pyqt5License.setText("Licensed under the GPL-3.0 License.")
        self.mefrplibTitle.setText("MEFrpLib")
        self.mefrplibCopyright.setText("Copyright © 2024, LxHTT.")
        self.mefrplibLicense.setText("Licensed under the GPL-3.0 License.")
        self.qmaterialwidgetsxTitle.setText("QMaterialWidgets X")
        self.qmaterialwidgetsxCopyright.setText("Copyright © 2024, zhiyiYo and LxHTT.")
        self.requestsTitle.setText("requests")
        self.requestsCopyright.setText("Copyright © 2017 by Kenneth Reitz.")
        self.requestsLicense.setText("Licensed under the Apache 2.0 License.")
        self.psutilTitle.setText("psutil")
        self.psutilCopyright.setText("Copyright © 2009, Giampaolo Rodola'.")
        self.psutilLicense.setText("Licensed under a BSD 3-Clause License.")
        self.pydesTitle.setText("pyDes")
        self.pydesCopyright.setText("Copyright © 2010, Todd Whiteman.")
        self.pydesLicense.setText("Licensed under the MIT License.")
        self.openMEFrpWebBtn.clicked.connect(lambda: openWebUrl("https://www.mefrp.com"))
        self.openLauncherRepoBtn.clicked.connect(
            lambda: openWebUrl("https://github.com/LxHTT/MEFrp-Launcher-Qt")
        )