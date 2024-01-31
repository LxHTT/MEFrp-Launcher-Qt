from typing import Union
import sys
from os import path as osp
from PyQt5.QtCore import QFile

from qmaterialwidgets import QConfig, qconfig, Theme, ConfigItem, BoolValidator


class Config(QConfig):
    """MEFrp Launcher Configuration"""

    isLoggedIn = ConfigItem("User", "isLoggedIn", False, BoolValidator())
    userName = ConfigItem("User", "userName", "", "")
    userPassword = ConfigItem("User", "userToken", "", "")
    oldExecuteable = ConfigItem("Other", "oldExecuteable", "", "")


cfg = Config()


def getStyleSheetFromFile(file: Union[str, QFile]):
    """get style sheet from qss file"""
    f = QFile(file)
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding="utf-8")
    f.close()
    return qss


def initMELauncherConfig(loading=False):
    qconfig.load("MEFrp-Launcher-Settings.json", cfg)
    cfg.set(cfg.oldExecuteable, osp.basename(sys.executable))
    if loading:
        return
    cfg.set(cfg.isLoggedIn, False)
    cfg.set(cfg.userName, "")
    cfg.set(cfg.userPassword, "")
    cfg.set(cfg.themeColor, "#6750A4")
    cfg.set(cfg.themeMode, Theme.AUTO)
