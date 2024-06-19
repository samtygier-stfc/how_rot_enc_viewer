#!/usr/bin/env python
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
import numpy as np
import pyqtgraph as pg


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Tomography")
        self.central = QWidget()
        self.layout = QHBoxLayout()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

        self.projections_view, self.projections_img = self._make_view()
        self.sinogram_view, self.sinogram_img = self._make_view()
        self.reconstruction_view, self.reconstruction_img = self._make_view()

        self.layout.addWidget(self.projections_view)
        self.layout.addWidget(self.sinogram_view)
        self.layout.addWidget(self.reconstruction_view)

    @staticmethod
    def _make_view() -> tuple[pg.GraphicsLayoutWidget, pg.ImageItem]:
        data = np.random.default_rng().random((200, 200))
        widget = pg.GraphicsLayoutWidget()
        view = pg.ViewBox()
        img_item = pg.ImageItem(data)
        view.addItem(img_item)
        widget.addItem(view)
        return widget, img_item


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
