#!/usr/bin/env python
import sys

from PyQt6.QtWidgets import QApplication

import config
from main_window import MainWindow


class HOWViewer:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.window.datasets = config.datasets
        self.window.start()

    def start(self):
        self.window.show()
        self.app.exec()


if __name__ == '__main__':
    app = HOWViewer()
    app.start()
