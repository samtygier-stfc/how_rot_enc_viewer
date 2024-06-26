from typing import Any

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QTimer, QEvent, Qt
from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QApplication

import data

INACTIVE_TIMEOUT = 120 * 1000


class MainWindow(QMainWindow):
    datasets: list[dict[str, Any]]
    projections_data: np.ndarray

    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Tomography")
        self.showFullScreen()
        self.central = QWidget()
        self.layout = QHBoxLayout()
        self.central.setLayout(self.layout)
        self.setCentralWidget(self.central)

        self.projections_view, self.projections_img = self._make_view()
        self.sinogram_view, self.sinogram_img = self._make_view()
        self.reconstruction_view, self.reconstruction_img = self._make_view()

        self.projections_img.getViewBox().setAspectLocked(True)
        self.reconstruction_img.getViewBox().setAspectLocked(True)

        self.layout.addWidget(self.projections_view)
        self.layout.addWidget(self.sinogram_view)
        self.layout.addWidget(self.reconstruction_view)

        cm = pg.colormap.getFromMatplotlib("binary")
        self.projections_img.setColorMap(cm)
        self.sinogram_img.setColorMap(cm)

        self.recon_animate_timer = QTimer(self)
        self.recon_animate_timer.setInterval(100)
        self.recon_animate_timer.timeout.connect(self.recon_animate)

        self.message_box = QLabel("Starting")
        self.layout.addWidget(self.message_box)

        self.start_timer = QTimer(self)

        self.inactive_timer = QTimer(self)
        self.inactive_timer.setSingleShot(True)
        self.inactive_timer.start(INACTIVE_TIMEOUT)
        self.inactive_timer.timeout.connect(self.handle_inactive)

    def start(self):
        self.start_timer.singleShot(100, self.do_loads)

    @staticmethod
    def _make_view() -> tuple[pg.GraphicsLayoutWidget, pg.ImageItem]:
        data = np.zeros((200, 200))
        widget = pg.GraphicsLayoutWidget()
        view = pg.ViewBox()
        view.setBackgroundColor((255, 255, 255))
        img_item = pg.ImageItem(data, autolevel=False, axisOrder='row-major')
        view.addItem(img_item)
        widget.addItem(view)
        return widget, img_item

    def do_loads(self) -> None:
        for i in [0, 1, 2, 0]:
            self.message_box.setText(f"Loading {i}")
            QApplication.processEvents()
            try:
                self.select_dataset(i)
            except Exception as e:
                self.message_box.setText(f"Failed to load {i}\n{e}")
                raise

        self.message_box.hide()

    def select_dataset(self, index: int) -> None:
        self.recon_animate_timer.stop()
        projections_dataset = self.datasets[index]['projections']
        self.projections_data = data.load_stack_c(**projections_dataset)
        self.level_min_max = self.projections_data.min(
        ), self.projections_data.max()

        reconstruction_dataset = self.datasets[index]['reconstruction']
        self.reconstruction_data = data.load_stack_c(**reconstruction_dataset)
        self.recon_slice = 0
        self.max_recon_slice = self.reconstruction_data.shape[0]
        self.level_min_max_recon = self.reconstruction_data.min(
        ), self.reconstruction_data.max()

        self.sinogram = np.full(
            (self.projections_data.shape[0], self.projections_data.shape[2]),
            self.level_min_max[0])
        self.angles_done = np.zeros((self.projections_data.shape[0]),
                                    dtype=bool)
        self.angle = 0
        self.max_angle = self.datasets[index]['projections']['stop']
        self.rotate(0)

        self.projections_img.setLevels(self.level_min_max)
        self.sinogram_img.setLevels(self.level_min_max)
        self.reconstruction_img.setLevels(self.level_min_max_recon)
        self.reconstruction_img.setImage(np.full((1, 1), 255))

    def rotate(self, step: int) -> None:
        self.angle += step
        self.angle = self.angle % self.max_angle
        self.projections_img.setImage(self.projections_data[self.angle])
        slice_number = self.projections_data.shape[1] // 2
        self.sinogram[self.angle, :] = self.projections_data[self.angle,
                                                             slice_number, :]
        self.sinogram_img.setImage(self.sinogram)
        self.angles_done[self.angle] = True

        if np.all(self.angles_done):
            if not self.recon_animate_timer.isActive():
                self.recon_animate_timer.start()

    def show_reconstruction(self) -> None:
        self.reconstruction_img.setImage(
            self.reconstruction_data[self.recon_slice])

    def recon_animate(self) -> None:
        self.recon_slice += 1
        self.recon_slice = self.recon_slice % self.max_recon_slice
        self.show_reconstruction()

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
        else:
            if e.key() == Qt.Key.Key_1:
                self.select_dataset(0)
            if e.key() == Qt.Key.Key_2:
                self.select_dataset(1)
            if e.key() == Qt.Key.Key_3:
                self.select_dataset(2)

            if e.key() == Qt.Key.Key_Left:
                self.rotate(1)
            if e.key() == Qt.Key.Key_Right:
                self.rotate(-1)

        self.inactive_timer.start(INACTIVE_TIMEOUT)

    def handle_inactive(self) -> None:
        self.recon_animate_timer.stop()
        self.projections_img.setImage(np.zeros((1, 1)))
        self.sinogram_img.setImage(np.zeros((1, 1)))
        self.reconstruction_img.setImage(np.ones((1, 1)) * 255)
