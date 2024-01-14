from typing import Union

from PyQt5.QtCore import QFile

from qmaterialwidgets import QConfig, ConfigItem


class Config(QConfig):
    """MEFrp Launcher Configuration"""

    oldExecuteable = ConfigItem("Other", "oldExecuteable", "", "")


cfg = Config()


def getStyleSheetFromFile(file: Union[str, QFile]):
    """get style sheet from qss file"""
    f = QFile(file)
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding="utf-8")
    f.close()
    return qss
