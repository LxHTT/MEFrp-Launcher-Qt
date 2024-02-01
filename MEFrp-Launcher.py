import sys
from PyQt5.QtCore import Qt, QLocale, QObject, QEvent
from PyQt5.QtWidgets import QApplication


class MEApplication(QApplication):
    def __init__(self, argv):
        super().__init__(argv)

    def notify(self, a0: QObject, a1: QEvent) -> bool:
        try:
            done = super().notify(a0, a1)
            return done
        except Exception:
            return False


if __name__ == "__main__":
    # fmt: off
    from MELauncherLib.AppController.Utils import initMELauncher
    initMELauncher()
    del initMELauncher

    from MELauncherLib.AppController.Settings import initMELauncherConfig
    initMELauncherConfig()
    del initMELauncherConfig

    MEApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    MEApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    MEApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    MEApplication.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    app = MEApplication(sys.argv)

    from qmaterialwidgets import MaterialTranslator
    fluentTranslator = MaterialTranslator(QLocale(QLocale.Chinese))
    app.installTranslator(fluentTranslator)

    from MELauncherLib.Interfaces.MainWindow import MEMainWindow
    w = MEMainWindow()

    app.exec_()
    sys.exit()
    # fmt: on
