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
from PyQt5.QtCore import Qt, QRect, QObject, pyqtSlot

from ..Resources import *  # noqa: F403 F401

from qmaterialwidgets import (
    BodyLabel,
    CardWidget,
    ComboBox,
    FilledPushButton,
    OutlinedCardWidget,
    RadioButton,
    StrongBodyLabel,
    SubtitleLabel,
    SwitchButton,
    TitleLabel,
    FluentIcon as FIF,
    Theme,
    setTheme,
    InfoBar,
    InfoBarPosition,
    MessageBox,
)
from .Multiplex.ScollArea import NormalSmoothScrollArea
from ..AppController.Settings import cfg, devMode
from ..AppController.Update import CheckUpdateThread, Updater, compareVersion


class SettingsController(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    def runFrpcTypeControl(self):
        cfg.set(cfg.runFrpcType, self.sender().property("runFrpcType"), save=True)

    def bypassSystemProxyControl(self):
        cfg.set(cfg.bypassProxy, self.sender().isChecked(), save=True)

    def launcherThemeControl(self):
        themeList = [Theme.AUTO, Theme.DARK, Theme.LIGHT]
        cfg.set(cfg.themeMode, themeList[self.sender().currentIndex()], save=True)
        setTheme(themeList[self.sender().currentIndex()])

    def navigationPositionControl(self):
        navigationPositionList = ["Bottom", "Left"]
        cfg.appRestartSig.emit()
        cfg.set(
            cfg.navigationPosition, navigationPositionList[self.sender().currentIndex()], save=True
        )

    def autoCheckUpdateControl(self):
        cfg.set(cfg.autoCheckUpdate, self.sender().isChecked(), save=True)


class SettingsPage(QWidget, SettingsController):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setContentsMargins(8, 8, 8, 8)
        self.setObjectName("SettingsPage")
        self.gridLayout = QGridLayout(self)
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
        self.settingsScrollArea = NormalSmoothScrollArea(self)
        self.settingsScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.settingsScrollArea.setWidgetResizable(True)
        self.settingsScrollArea.setObjectName("settingsScrollArea")
        self.settingsSC = QWidget()
        self.settingsSC.setGeometry(QRect(0, -144, 676, 629))
        self.settingsSC.setObjectName("settingsSC")
        self.settingsLayout = QVBoxLayout(self.settingsSC)
        self.settingsLayout.setContentsMargins(0, 0, 0, 0)
        self.settingsLayout.setSpacing(10)
        self.settingsLayout.setObjectName("settingsLayout")
        self.frpcSettingsTitle = SubtitleLabel(self.settingsSC)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcSettingsTitle.sizePolicy().hasHeightForWidth())
        self.frpcSettingsTitle.setSizePolicy(sizePolicy)
        self.frpcSettingsTitle.setObjectName("frpcSettingsTitle")
        self.settingsLayout.addWidget(self.frpcSettingsTitle)
        self.frpcSettingsWidget = OutlinedCardWidget(self.settingsSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcSettingsWidget.sizePolicy().hasHeightForWidth())
        self.frpcSettingsWidget.setSizePolicy(sizePolicy)
        self.frpcSettingsWidget.setFixedHeight(175)
        self.frpcSettingsWidget.setObjectName("frpcSettingsWidget")
        self.frpcSettingsLayout = QVBoxLayout(self.frpcSettingsWidget)
        self.frpcSettingsLayout.setObjectName("frpcSettingsLayout")
        self.runFrpcWidget = CardWidget(self.frpcSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runFrpcWidget.sizePolicy().hasHeightForWidth())
        self.runFrpcWidget.setSizePolicy(sizePolicy)
        self.runFrpcWidget.setFixedHeight(70)
        self.runFrpcWidget.setObjectName("runFrpcWidget")
        self.runFrpcLayout = QGridLayout(self.runFrpcWidget)
        self.runFrpcLayout.setContentsMargins(16, 16, 16, 16)
        self.runFrpcLayout.setObjectName("runFrpcLayout")
        self.runFrpcTitle = StrongBodyLabel(self.runFrpcWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runFrpcTitle.sizePolicy().hasHeightForWidth())
        self.runFrpcTitle.setSizePolicy(sizePolicy)
        self.runFrpcTitle.setObjectName("runFrpcTitle")
        self.runFrpcLayout.addWidget(self.runFrpcTitle, 0, 0, 1, 1)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.runFrpcLayout.addItem(spacerItem1, 0, 1, 2, 1)
        self.runFrpcTip = BodyLabel(self.runFrpcWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runFrpcTip.sizePolicy().hasHeightForWidth())
        self.runFrpcTip.setSizePolicy(sizePolicy)
        self.runFrpcTip.setObjectName("runFrpcTip")
        self.runFrpcLayout.addWidget(self.runFrpcTip, 1, 0, 1, 1)
        self.runFrpcRadioWidget = QWidget(self.runFrpcWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.runFrpcRadioWidget.sizePolicy().hasHeightForWidth())
        self.runFrpcRadioWidget.setSizePolicy(sizePolicy)
        self.runFrpcRadioWidget.setObjectName("runFrpcRadioWidget")
        self.runFrpcRadioLayout = QHBoxLayout(self.runFrpcRadioWidget)
        self.runFrpcRadioLayout.setContentsMargins(0, 0, 0, 0)
        self.runFrpcRadioLayout.setSpacing(8)
        self.runFrpcRadioLayout.setObjectName("runFrpcRadioLayout")
        self.runFrpcEZRadioBtn = RadioButton(self.runFrpcRadioWidget)
        self.runFrpcEZRadioBtn.setChecked(True)
        self.runFrpcEZRadioBtn.setObjectName("runFrpcEZRadioBtn")
        self.runFrpcRadioLayout.addWidget(self.runFrpcEZRadioBtn)
        self.runFrpcConfigRadioBtn = RadioButton(self.runFrpcRadioWidget)
        self.runFrpcConfigRadioBtn.setObjectName("runFrpcConfigRadioBtn")
        self.runFrpcRadioLayout.addWidget(self.runFrpcConfigRadioBtn)
        self.runFrpcLayout.addWidget(self.runFrpcRadioWidget, 0, 2, 2, 1)
        self.frpcSettingsLayout.addWidget(self.runFrpcWidget)
        self.frpcVersionWidget = CardWidget(self.frpcSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcVersionWidget.sizePolicy().hasHeightForWidth())
        self.frpcVersionWidget.setSizePolicy(sizePolicy)
        self.frpcVersionWidget.setFixedHeight(70)
        self.frpcVersionWidget.setObjectName("frpcVersionWidget")
        self.frpcVersionLayout = QGridLayout(self.frpcVersionWidget)
        self.frpcVersionLayout.setContentsMargins(16, 16, 16, 16)
        self.frpcVersionLayout.setObjectName("frpcVersionLayout")
        self.frpcVersionTip = BodyLabel(self.frpcVersionWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcVersionTip.sizePolicy().hasHeightForWidth())
        self.frpcVersionTip.setSizePolicy(sizePolicy)
        self.frpcVersionTip.setObjectName("frpcVersionTip")
        self.frpcVersionLayout.addWidget(self.frpcVersionTip, 1, 0, 1, 1)
        self.frpcVersionTitle = StrongBodyLabel(self.frpcVersionWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcVersionTitle.sizePolicy().hasHeightForWidth())
        self.frpcVersionTitle.setSizePolicy(sizePolicy)
        self.frpcVersionTitle.setObjectName("frpcVersionTitle")
        self.frpcVersionLayout.addWidget(self.frpcVersionTitle, 0, 0, 1, 1)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.frpcVersionLayout.addItem(spacerItem2, 0, 1, 2, 1)
        self.frpcVresionLabel = BodyLabel(self.frpcVersionWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frpcVresionLabel.sizePolicy().hasHeightForWidth())
        self.frpcVresionLabel.setSizePolicy(sizePolicy)
        self.frpcVresionLabel.setObjectName("frpcVresionLabel")
        self.frpcVersionLayout.addWidget(self.frpcVresionLabel, 0, 2, 2, 1)
        self.frpcSettingsLayout.addWidget(self.frpcVersionWidget)
        self.settingsLayout.addWidget(self.frpcSettingsWidget)
        self.launcherSettingsTitle = SubtitleLabel(self.settingsSC)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherSettingsTitle.sizePolicy().hasHeightForWidth())
        self.launcherSettingsTitle.setSizePolicy(sizePolicy)
        self.launcherSettingsTitle.setObjectName("launcherSettingsTitle")
        self.settingsLayout.addWidget(self.launcherSettingsTitle)
        self.launcherSettingsWidget = OutlinedCardWidget(self.settingsSC)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherSettingsWidget.sizePolicy().hasHeightForWidth())
        self.launcherSettingsWidget.setSizePolicy(sizePolicy)
        self.launcherSettingsWidget.setFixedHeight(430)
        self.launcherSettingsWidget.setObjectName("launcherSettingsWidget")
        self.launcherSettingsLayout = QVBoxLayout(self.launcherSettingsWidget)
        self.launcherSettingsLayout.setObjectName("launcherSettingsLayout")
        self.bypassSystemProxyWidget = CardWidget(self.launcherSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bypassSystemProxyWidget.sizePolicy().hasHeightForWidth())
        self.bypassSystemProxyWidget.setSizePolicy(sizePolicy)
        self.bypassSystemProxyWidget.setFixedHeight(75)
        self.bypassSystemProxyWidget.setObjectName("bypassSystemProxyWidget")
        self.bypassSystemProxyLayout = QGridLayout(self.bypassSystemProxyWidget)
        self.bypassSystemProxyLayout.setContentsMargins(16, 16, 16, 16)
        self.bypassSystemProxyLayout.setObjectName("bypassSystemProxyLayout")
        self.bypassSystemProxySwitchWidget = QWidget(self.bypassSystemProxyWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bypassSystemProxySwitchWidget.sizePolicy().hasHeightForWidth()
        )
        self.bypassSystemProxySwitchWidget.setSizePolicy(sizePolicy)
        self.bypassSystemProxySwitchWidget.setObjectName("bypassSystemProxySwitchWidget")
        self.bypassSystemProxySwitchLayout = QHBoxLayout(self.bypassSystemProxySwitchWidget)
        self.bypassSystemProxySwitchLayout.setContentsMargins(0, 0, 0, 0)
        self.bypassSystemProxySwitchLayout.setSpacing(0)
        self.bypassSystemProxySwitchLayout.setObjectName("bypassSystemProxySwitchLayout")
        self.bypassSystemProxySwitchBtn = SwitchButton(self.bypassSystemProxySwitchWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.bypassSystemProxySwitchBtn.sizePolicy().hasHeightForWidth()
        )
        self.bypassSystemProxySwitchBtn.setSizePolicy(sizePolicy)
        self.bypassSystemProxySwitchBtn.setObjectName("bypassSystemProxySwitchBtn")
        self.bypassSystemProxySwitchLayout.addWidget(self.bypassSystemProxySwitchBtn)
        self.bypassSystemProxyLayout.addWidget(self.bypassSystemProxySwitchWidget, 0, 2, 2, 1)
        self.bypassSystemProxyTitle = StrongBodyLabel(self.bypassSystemProxyWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bypassSystemProxyTitle.sizePolicy().hasHeightForWidth())
        self.bypassSystemProxyTitle.setSizePolicy(sizePolicy)
        self.bypassSystemProxyTitle.setObjectName("bypassSystemProxyTitle")
        self.bypassSystemProxyLayout.addWidget(self.bypassSystemProxyTitle, 0, 0, 1, 1)
        spacerItem3 = QSpacerItem(171, 50, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.bypassSystemProxyLayout.addItem(spacerItem3, 0, 1, 2, 1)
        self.bypassSystemProxyTip = BodyLabel(self.bypassSystemProxyWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bypassSystemProxyTip.sizePolicy().hasHeightForWidth())
        self.bypassSystemProxyTip.setSizePolicy(sizePolicy)
        self.bypassSystemProxyTip.setObjectName("bypassSystemProxyTip")
        self.bypassSystemProxyLayout.addWidget(self.bypassSystemProxyTip, 1, 0, 1, 1)
        self.launcherSettingsLayout.addWidget(self.bypassSystemProxyWidget)
        self.launcherThemeWidget = CardWidget(self.launcherSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherThemeWidget.sizePolicy().hasHeightForWidth())
        self.launcherThemeWidget.setSizePolicy(sizePolicy)
        self.launcherThemeWidget.setFixedHeight(75)
        self.launcherThemeWidget.setObjectName("launcherThemeWidget")
        self.programThemeLayout = QGridLayout(self.launcherThemeWidget)
        self.programThemeLayout.setContentsMargins(16, 16, 16, 16)
        self.programThemeLayout.setObjectName("programThemeLayout")
        self.launcherThemeTitle = StrongBodyLabel(self.launcherThemeWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherThemeTitle.sizePolicy().hasHeightForWidth())
        self.launcherThemeTitle.setSizePolicy(sizePolicy)
        self.launcherThemeTitle.setObjectName("launcherThemeTitle")
        self.programThemeLayout.addWidget(self.launcherThemeTitle, 1, 0, 1, 1)
        spacerItem4 = QSpacerItem(107, 50, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.programThemeLayout.addItem(spacerItem4, 1, 2, 3, 1)
        self.launcherThemeComboWidget = QWidget(self.launcherThemeWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherThemeComboWidget.sizePolicy().hasHeightForWidth())
        self.launcherThemeComboWidget.setSizePolicy(sizePolicy)
        self.launcherThemeComboWidget.setObjectName("launcherThemeComboWidget")
        self.launcherThemeComboLayout = QHBoxLayout(self.launcherThemeComboWidget)
        self.launcherThemeComboLayout.setContentsMargins(0, 0, 0, 0)
        self.launcherThemeComboLayout.setSpacing(0)
        self.launcherThemeComboLayout.setObjectName("launcherThemeComboLayout")
        self.launcherThemeComboBox = ComboBox(self.launcherThemeComboWidget)
        self.launcherThemeComboBox.setObjectName("launcherThemeComboBox")
        self.launcherThemeComboLayout.addWidget(self.launcherThemeComboBox)
        self.programThemeLayout.addWidget(self.launcherThemeComboWidget, 1, 3, 3, 1)
        self.launcherThemeTip = BodyLabel(self.launcherThemeWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.launcherThemeTip.sizePolicy().hasHeightForWidth())
        self.launcherThemeTip.setSizePolicy(sizePolicy)
        self.launcherThemeTip.setObjectName("launcherThemeTip")
        self.programThemeLayout.addWidget(self.launcherThemeTip, 2, 0, 2, 1)
        self.launcherSettingsLayout.addWidget(self.launcherThemeWidget)
        self.navigationPositionWidget = CardWidget(self.launcherSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navigationPositionWidget.sizePolicy().hasHeightForWidth())
        self.navigationPositionWidget.setSizePolicy(sizePolicy)
        self.navigationPositionWidget.setFixedHeight(75)
        self.navigationPositionWidget.setObjectName("navigationPositionWidget")
        self.navigationPositionLayout = QGridLayout(self.navigationPositionWidget)
        self.navigationPositionLayout.setContentsMargins(16, 16, 16, 16)
        self.navigationPositionLayout.setObjectName("navigationPositionLayout")
        spacerItem5 = QSpacerItem(107, 50, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.navigationPositionLayout.addItem(spacerItem5, 1, 2, 3, 1)
        self.navigationPositionTip = BodyLabel(self.navigationPositionWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navigationPositionTip.sizePolicy().hasHeightForWidth())
        self.navigationPositionTip.setSizePolicy(sizePolicy)
        self.navigationPositionTip.setObjectName("navigationPositionTip")
        self.navigationPositionLayout.addWidget(self.navigationPositionTip, 2, 0, 2, 1)
        self.navigationPositionTitle = StrongBodyLabel(self.navigationPositionWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.navigationPositionTitle.sizePolicy().hasHeightForWidth())
        self.navigationPositionTitle.setSizePolicy(sizePolicy)
        self.navigationPositionTitle.setObjectName("navigationPositionTitle")
        self.navigationPositionLayout.addWidget(self.navigationPositionTitle, 1, 0, 1, 2)
        self.navigationPositionComboWidget = QWidget(self.navigationPositionWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.navigationPositionComboWidget.sizePolicy().hasHeightForWidth()
        )
        self.navigationPositionComboWidget.setSizePolicy(sizePolicy)
        self.navigationPositionComboWidget.setObjectName("navigationPositionComboWidget")
        self.navigationPositionComboLayout = QHBoxLayout(self.navigationPositionComboWidget)
        self.navigationPositionComboLayout.setContentsMargins(0, 0, 0, 0)
        self.navigationPositionComboLayout.setSpacing(0)
        self.navigationPositionComboLayout.setObjectName("navigationPositionComboLayout")
        self.navigationPositionComboBox = ComboBox(self.navigationPositionComboWidget)
        self.navigationPositionComboBox.setObjectName("navigationPositionComboBox")
        self.navigationPositionComboLayout.addWidget(self.navigationPositionComboBox)
        self.navigationPositionLayout.addWidget(self.navigationPositionComboWidget, 1, 3, 3, 1)
        self.launcherSettingsLayout.addWidget(self.navigationPositionWidget)
        self.autoCheckUpdateWidget = CardWidget(self.launcherSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoCheckUpdateWidget.sizePolicy().hasHeightForWidth())
        self.autoCheckUpdateWidget.setSizePolicy(sizePolicy)
        self.autoCheckUpdateWidget.setFixedHeight(75)
        self.autoCheckUpdateWidget.setObjectName("autoCheckUpdateWidget")
        self.autoCheckUpdateLayout = QGridLayout(self.autoCheckUpdateWidget)
        self.autoCheckUpdateLayout.setContentsMargins(16, 16, 16, 16)
        self.autoCheckUpdateLayout.setObjectName("autoCheckUpdateLayout")
        spacerItem5 = QSpacerItem(171, 50, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.autoCheckUpdateLayout.addItem(spacerItem5, 0, 1, 2, 1)
        self.autoCheckUpdateSwitchWidget = QWidget(self.autoCheckUpdateWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.autoCheckUpdateSwitchWidget.sizePolicy().hasHeightForWidth()
        )
        self.autoCheckUpdateSwitchWidget.setSizePolicy(sizePolicy)
        self.autoCheckUpdateSwitchWidget.setObjectName("autoCheckUpdateSwitchWidget")
        self.autoCheckUpdateSwitchLayout = QHBoxLayout(self.autoCheckUpdateSwitchWidget)
        self.autoCheckUpdateSwitchLayout.setContentsMargins(0, 0, 0, 0)
        self.autoCheckUpdateSwitchLayout.setSpacing(0)
        self.autoCheckUpdateSwitchLayout.setObjectName("autoCheckUpdateSwitchLayout")
        self.autoCheckUpdateSwitchBtn = SwitchButton(self.autoCheckUpdateSwitchWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoCheckUpdateSwitchBtn.sizePolicy().hasHeightForWidth())
        self.autoCheckUpdateSwitchBtn.setSizePolicy(sizePolicy)
        self.autoCheckUpdateSwitchBtn.setObjectName("autoCheckUpdateSwitchBtn")
        self.autoCheckUpdateSwitchLayout.addWidget(self.autoCheckUpdateSwitchBtn)
        self.autoCheckUpdateLayout.addWidget(self.autoCheckUpdateSwitchWidget, 0, 2, 2, 1)
        self.autoCheckUpdateTip = BodyLabel(self.autoCheckUpdateWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoCheckUpdateTip.sizePolicy().hasHeightForWidth())
        self.autoCheckUpdateTip.setSizePolicy(sizePolicy)
        self.autoCheckUpdateTip.setObjectName("autoCheckUpdateTip")
        self.autoCheckUpdateLayout.addWidget(self.autoCheckUpdateTip, 1, 0, 1, 1)
        self.autoCheckUpdateTitle = StrongBodyLabel(self.autoCheckUpdateWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autoCheckUpdateTitle.sizePolicy().hasHeightForWidth())
        self.autoCheckUpdateTitle.setSizePolicy(sizePolicy)
        self.autoCheckUpdateTitle.setObjectName("autoCheckUpdateTitle")
        self.autoCheckUpdateLayout.addWidget(self.autoCheckUpdateTitle, 0, 0, 1, 1)
        self.launcherSettingsLayout.addWidget(self.autoCheckUpdateWidget)
        self.manualCheckUpdateWidget = CardWidget(self.launcherSettingsWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manualCheckUpdateWidget.sizePolicy().hasHeightForWidth())
        self.manualCheckUpdateWidget.setSizePolicy(sizePolicy)
        self.manualCheckUpdateWidget.setFixedHeight(75)
        self.manualCheckUpdateWidget.setObjectName("manualCheckUpdateWidget")
        self.manualCheckUpdateLayout = QGridLayout(self.manualCheckUpdateWidget)
        self.manualCheckUpdateLayout.setContentsMargins(16, 16, 16, 16)
        self.manualCheckUpdateLayout.setObjectName("manualCheckUpdateLayout")
        spacerItem6 = QSpacerItem(107, 50, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.manualCheckUpdateLayout.addItem(spacerItem6, 1, 2, 3, 1)
        self.manualCheckUpdateTip = BodyLabel(self.manualCheckUpdateWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manualCheckUpdateTip.sizePolicy().hasHeightForWidth())
        self.manualCheckUpdateTip.setSizePolicy(sizePolicy)
        self.manualCheckUpdateTip.setObjectName("manualCheckUpdateTip")
        self.manualCheckUpdateLayout.addWidget(self.manualCheckUpdateTip, 2, 0, 2, 1)
        self.manualCheckUpdateBtn = FilledPushButton(self.manualCheckUpdateWidget)
        self.manualCheckUpdateBtn.setObjectName("manualCheckUpdateBtn")
        self.manualCheckUpdateLayout.addWidget(self.manualCheckUpdateBtn, 1, 3, 3, 1)
        self.manualCheckUpdateTitle = StrongBodyLabel(self.manualCheckUpdateWidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manualCheckUpdateTitle.sizePolicy().hasHeightForWidth())
        self.manualCheckUpdateTitle.setSizePolicy(sizePolicy)
        self.manualCheckUpdateTitle.setObjectName("manualCheckUpdateTitle")
        self.manualCheckUpdateLayout.addWidget(self.manualCheckUpdateTitle, 1, 0, 1, 2)
        self.launcherSettingsLayout.addWidget(self.manualCheckUpdateWidget)
        self.settingsLayout.addWidget(self.launcherSettingsWidget)
        spacerItem7 = QSpacerItem(20, 80, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.settingsLayout.addItem(spacerItem7)
        self.settingsScrollArea.setWidget(self.settingsSC)
        self.gridLayout.addWidget(self.settingsScrollArea, 2, 0, 1, 1)

        self.bypassSystemProxySwitchBtn.setChecked(True)
        self.manualCheckUpdateBtn.setIcon(FIF.UPDATE)
        self.TitleLabel.setText("设置")
        self.frpcSettingsTitle.setText("Frpc 设置")
        self.runFrpcTitle.setText("Frpc 启动方式")
        self.runFrpcTip.setText("注意：选择 frpc.ini 启动时，高级配置选项才会生效。")

        self.runFrpcEZRadioBtn.setText("使用快捷参数启动")
        self.runFrpcConfigRadioBtn.setText("使用 frpc.ini 启动")
        self.frpcVersionTip.setText(
            "MEFrp-Launcher 会在每次启动时自动检查并更新 Frpc，您无需操心。"
        )
        self.frpcVersionTitle.setText("Frpc 版本")
        self.launcherSettingsTitle.setText("启动器设置")
        self.bypassSystemProxyTitle.setText("绕过系统代理")
        self.bypassSystemProxyTip.setText(
            "当开启系统代理，MEFrp-Launcher 无法正常连接网络时请尝试开启此项。"
        )

        self.launcherThemeTitle.setText("主题")
        self.launcherThemeTip.setText("随你所好。")
        self.autoCheckUpdateTip.setText("开启后，MEFrp-Launcher 将在每次启动时检查更新。")
        self.autoCheckUpdateTitle.setText("自动检查更新")
        self.manualCheckUpdateTip.setText("尚未完成，点了也不为所动。")
        self.manualCheckUpdateBtn.setText("检查更新")
        self.manualCheckUpdateTitle.setText("检查更新")
        self.navigationPositionTip.setText("遥遥领先 遥遥领先！")
        self.navigationPositionTitle.setText("导航栏位置")
        self.launcherThemeComboBox.addItems(["跟随系统", "深色模式", "浅色模式"])
        self.navigationPositionComboBox.addItems(["底部", "左侧"])
        self.launcherThemeComboBox.setCurrentIndex(0)

        self.runFrpcEZRadioBtn.setProperty("runFrpcType", "Easy")
        self.runFrpcConfigRadioBtn.setProperty("runFrpcType", "Config")
        self.runFrpcConfigRadioBtn.setEnabled(False)
        cfg.appRestartSig.connect(self.showRestartTip)
        self.initSettingsInterface()

    def showRestartTip(self):
        InfoBar.success(
            title="成功",
            content="此设置将在重启 MEFrp-Launcher 后生效",
            duration=1500,
            position=InfoBarPosition.TOP,
            parent=self,
        )

    def initSettingsInterface(self):
        self.runFrpcEZRadioBtn.setProperty("runFrpcType", "Easy")
        self.runFrpcEZRadioBtn.setChecked(bool(cfg.get(cfg.runFrpcType) == "Easy"))

        self.runFrpcConfigRadioBtn.setProperty("runFrpcType", "Config")
        self.runFrpcConfigRadioBtn.setChecked(bool(not cfg.get(cfg.runFrpcType) == "Easy"))

        self.bypassSystemProxySwitchBtn.setChecked(cfg.get(cfg.bypassProxy))

        themeList = [Theme.AUTO, Theme.DARK, Theme.LIGHT]
        self.launcherThemeComboBox.setCurrentIndex(themeList.index(cfg.get(cfg.themeMode)))
        del themeList

        navigationPositionList = ["Bottom", "Left"]
        self.navigationPositionComboBox.setCurrentIndex(
            navigationPositionList.index(cfg.get(cfg.navigationPosition))
        )
        del navigationPositionList

        self.autoCheckUpdateSwitchBtn.setChecked(cfg.get(cfg.autoCheckUpdate))
        self.connectSettingsSlot()

    def connectSettingsSlot(self):
        self.runFrpcEZRadioBtn.clicked.connect(self.runFrpcTypeControl)
        self.runFrpcConfigRadioBtn.clicked.connect(self.runFrpcTypeControl)
        self.bypassSystemProxySwitchBtn.checkedChanged.connect(self.bypassSystemProxyControl)
        self.launcherThemeComboBox.currentIndexChanged.connect(self.launcherThemeControl)
        self.navigationPositionComboBox.currentIndexChanged.connect(self.navigationPositionControl)
        self.autoCheckUpdateSwitchBtn.checkedChanged.connect(self.autoCheckUpdateControl)
        self.bypassSystemProxyWidget.clicked.connect(
            lambda: self.bypassSystemProxySwitchBtn.setChecked(
                bool(not self.bypassSystemProxySwitchBtn.isChecked())
            )
        )
        self.launcherThemeWidget.clicked.connect(self.launcherThemeComboBox._toggleComboMenu)
        self.navigationPositionWidget.clicked.connect(
            self.navigationPositionComboBox._toggleComboMenu
        )
        self.autoCheckUpdateWidget.clicked.connect(
            lambda: self.autoCheckUpdateSwitchBtn.setChecked(
                bool(not self.autoCheckUpdateSwitchBtn.isChecked())
            )
        )
        self.manualCheckUpdateBtn.clicked.connect(lambda: self.checkUpdate(parent=self))

    def checkUpdate(self, parent):
        """
        检查更新触发器\n
        返回：\n
        1.是否需要更新\n
            1为需要\n
            0为不需要\n
            -1出错\n
        2.新版更新链接\n
        3.新版更新介绍\n
        """
        self.manualCheckUpdateBtn.setEnabled(False)  # 防止爆炸
        self.tmpParent = parent
        self.thread_checkUpdate = CheckUpdateThread(self)
        self.thread_checkUpdate.isUpdate.connect(self.showUpdateMsg)
        self.thread_checkUpdate.start()

    @pyqtSlot(dict)
    def showUpdateMsg(self, latestVerInfo):
        """如果需要更新，显示弹窗；不需要则弹出提示"""
        if not len(latestVerInfo["version"]):
            InfoBar.error(
                title=self.tr("检查更新失败"),
                content=self.tr("尝试自己检查一下网络？"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self.tmpParent,
            )
            self.manualCheckUpdateBtn.setEnabled(True)
            return
        if compareVersion(latestVerInfo["version"]):
            title = self.tr("发现新版本：") + latestVerInfo["version"]
            w = MessageBox(title, latestVerInfo["log"], parent=self.tmpParent)
            w.contentLabel.setTextFormat(Qt.MarkdownText)
            w.yesButton.setText(self.tr("  更新  "))
            w.cancelButton.setText(self.tr("  关闭  "))
            if not devMode:
                w.yesButton.clicked.connect(lambda: self.window().switchTo(self))
                w.yesButton.clicked.connect(
                    Updater(updateInfo=latestVerInfo, parent=self).downloadUpdate
                )
            else:
                w.yesButton.clicked.connect(
                    lambda: InfoBar.error(
                        title=self.tr("不行"),
                        content=self.tr("开发模式下更新会把Python删掉的"),
                        orient=Qt.Horizontal,
                        isClosable=True,
                        position=InfoBarPosition.TOP_RIGHT,
                        duration=2500,
                        parent=self.tmpParent,
                    )
                )
            w.exec()
        else:
            InfoBar.success(
                title=self.tr("无需更新"),
                content=self.tr("已是最新版本"),
                orient=Qt.Horizontal,
                isClosable=True,
                position=InfoBarPosition.TOP_RIGHT,
                duration=2500,
                parent=self.tmpParent,
            )

        self.manualCheckUpdateBtn.setEnabled(True)
