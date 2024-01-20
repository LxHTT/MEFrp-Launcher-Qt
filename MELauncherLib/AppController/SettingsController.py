from typing import Union

from PyQt5.QtCore import QFile

from qmaterialwidgets import QConfig, ConfigItem, BoolValidator


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
