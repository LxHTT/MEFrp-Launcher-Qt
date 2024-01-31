from typing import Union
import sys
from os import path as osp
from PyQt5.QtCore import QFile
from PyQt5.QtGui import QColor

from qmaterialwidgets import QConfig, qconfig, Theme, ConfigItem, BoolValidator


class Config(QConfig):
    """MEFrp Launcher Configuration"""

    isLoggedIn = ConfigItem("User", "isLoggedIn", False, BoolValidator())
    userName = ConfigItem("User", "userName", "", "")
    userPassword = ConfigItem("User", "userToken", "", "")
    isFirstGuideFinished = ConfigItem("Launcher", "isFirstGuideFinished", True, BoolValidator())
    oldExecuteable = ConfigItem("Launcher", "oldExecuteable", "", "")


cfg = Config()


def getStyleSheetFromFile(file: Union[str, QFile]):
    """get style sheet from qss file"""
    f = QFile(file)
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding="utf-8")
    f.close()
    return qss


def initMELauncherConfig():
    if osp.exists("MEFrp-Launcher-Settings.json"):
        qconfig.load("MEFrp-Launcher-Settings.json", cfg)
        return
    qconfig.load("MEFrp-Launcher-Settings.json", cfg)
    cfg.set(cfg.isFirstGuideFinished, True)
    cfg.set(cfg.oldExecuteable, osp.basename(sys.executable))
    cfg.set(cfg.isLoggedIn, False)
    cfg.set(cfg.userName, "")
    cfg.set(cfg.userPassword, "")
    cfg.set(cfg.themeColor, QColor("#6750A4"))
    cfg.set(cfg.themeMode, Theme.AUTO)
