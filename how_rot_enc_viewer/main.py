#!/usr/bin/env python
import sys
from typing import Any

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout
import numpy as np
import pyqtgraph as pg

import config
import data


class MainWindow(QMainWindow):
    datasets: list[dict[str, Any]]
    projections_data: np.ndarray

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

    def select_dataset(self, index: int) -> None:
        projections_dataset = self.datasets[index]['projections']
        self.projections_data = data.load_stack(**projections_dataset)
        self.sinogram = np.zeros(
            (self.projections_data.shape[1], self.projections_data.shape[0]))
        self.angles_done = np.zeros((self.projections_data.shape[0]),
                                    dtype=bool)
        self.angle = 0
        self.max_angle = self.datasets[index]['projections']['stop']
        self.rotate(0)

    def rotate(self, step: int) -> None:
        self.angle += step
        self.angle = self.angle % self.max_angle
        self.projections_img.setImage(self.projections_data[self.angle])
        self.sinogram[:, self.angle] = self.projections_data[self.angle, :,
                                                             1000]
        self.sinogram_img.setImage(self.sinogram)
        self.angles_done[self.angle] = True

    def keyPressEvent(self, e: QEvent) -> None:
        if e.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if e.key() == Qt.Key.Key_1:
                self.select_dataset(0)
            if e.key() == Qt.Key.Key_2:
                self.select_dataset(1)
            if e.key() == Qt.Key.Key_3:
                self.select_dataset(2)

            if e.key() == Qt.Key.Key_4:
                self.rotate(1)
            if e.key() == Qt.Key.Key_5:
                self.rotate(-1)


class HOWViewer:

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = MainWindow()
        self.window.datasets = config.datasets
        self.window.select_dataset(0)

    def start(self):
        self.window.show()
        self.app.exec()


if __name__ == '__main__':
    app = HOWViewer()
    app.start()
