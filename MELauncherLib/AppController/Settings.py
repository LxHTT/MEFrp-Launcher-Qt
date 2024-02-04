from typing import Union
import sys
from os import path as osp
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QColor

from qmaterialwidgets import (
    QConfig,
    qconfig,
    Theme,
    ConfigItem,
    OptionsConfigItem,
    BoolValidator,
    OptionsValidator,
)


class Config(QConfig):
    """MEFrp Launcher Configuration"""

    userName = ConfigItem("User", "userName", "", "")
    userPassword = ConfigItem("User", "userPassword", "", "")
    userAuthorization = ConfigItem("User", "userAuthorization", "", "")

    runFrpcType = OptionsConfigItem("Frpc", "runFrpcType", "EZ", OptionsValidator(["EZ", "INI"]))

    isFirstGuideFinished = ConfigItem("Launcher", "isFirstGuideFinished", False, BoolValidator())
    oldExecuteable = ConfigItem("Launcher", "oldExecuteable", "", "")
    bypassProxy = ConfigItem("Launcher", "bypassProxy", True, BoolValidator())
    navigationPosition = OptionsConfigItem(
        "Launcher", "navigationPosition", "Bottom", OptionsValidator(["Bottom", "Left"])
    )


cfg = Config()


def getStyleSheetFromFile(file: Union[str, QFile]):
    """get style sheet from qss file"""
    f = QFile(file)
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding="utf-8")
    f.close()
    return qss


def initMELauncherConfig():
    qconfig.load("MEFrp-Launcher-Settings.json", cfg)
    if cfg.get(cfg.isFirstGuideFinished):
        return
    cfg.set(cfg.isFirstGuideFinished, False)
    cfg.set(cfg.oldExecuteable, osp.basename(sys.executable))
    cfg.set(cfg.userName, "")
    cfg.set(cfg.userPassword, "")
    cfg.set(cfg.themeColor, QColor("#6750A4"))
    cfg.set(cfg.themeMode, Theme.AUTO)
    cfg.set(cfg.navigationPosition, "Bottom")
