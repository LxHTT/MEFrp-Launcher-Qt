import sys
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtWidgets import QApplication
from qmaterialwidgets import MaterialTranslator

from MELauncherLib.AppController.ExceptionHandler import initMELauncher
from MELauncherLib.Interfaces.MainWindow import MEMainWindow

if __name__ == "__main__":
    initMELauncher()
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    QApplication.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    app = QApplication(sys.argv)
    fluentTranslator = MaterialTranslator(QLocale(QLocale.Chinese))
    app.installTranslator(fluentTranslator)

    w = MEMainWindow()
    w.show()
    app.exec_()
    sys.exit()
