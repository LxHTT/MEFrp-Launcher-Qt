from PyQt5.QtWidgets import QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from ...Resources import *  # noqa: F403 F401


class SystemTrayContainer:
    def __init__(self, showLauncherSlot, exitSlot, parent=None):
        self.trayIcon = QSystemTrayIcon(parent)
        self.trayMenu = QMenu(parent)
        self.trayIcon.setIcon(QIcon(":/built-InIcons/MEFrp.ico"))
        self.showLauncherAction = QAction("显示主界面", self.trayIcon)
        self.showLauncherAction.triggered.connect(showLauncherSlot)
        self.trayIcon.setToolTip("MEFrp-Launcher-Qt")
        self.exitProcessAction = QAction("退出", self.trayIcon)
        self.exitProcessAction.triggered.connect(exitSlot)
        self.trayMenu.addAction(self.showLauncherAction)
        self.trayMenu.addAction(self.exitProcessAction)
        self.trayIcon.setContextMenu(self.trayMenu)

    def getTrayIcon(self):
        return self.trayIcon
