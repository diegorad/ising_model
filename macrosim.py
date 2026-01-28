import subprocess
import numpy as np
import matplotlib.pyplot as plt

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen


class XYPad(QWidget):
    def __init__(self, on_change):
        super().__init__()
        self.setMinimumSize(300, 300)

        self.norm_x = 0.5
        self.norm_y = 0.5
        
        self.x_range = 0.5
        self.y_range = 3

        self.x = 0.0
        self.y = 0.0

        self.on_change = on_change

    def mousePressEvent(self, event):
        self.update_position(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.update_position(event)

    def update_position(self, event):
        self.norm_x = min(max(event.position().x() / self.width(), 0), 1)
        self.norm_y = min(max(1 - event.position().y() / self.height(), 0), 1)
		
        self.x = self.x_range * (2 * self.norm_x - 1)
        self.y = self.y_range * (2 * self.norm_y - 1)

        self.on_change()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        w, h = self.width(), self.height()

        painter.fillRect(self.rect(), QColor(25, 25, 25))

        axis_pen = QPen(QColor(120, 120, 120), 1)
        painter.setPen(axis_pen)
        painter.drawLine(w / 2, 0, w / 2, h)
        painter.drawLine(0, h / 2, w, h / 2)

        px = self.norm_x * w
        py = (1 - self.norm_y) * h

        dot_pen = QPen(QColor(255, 80, 80), 2)
        painter.setPen(dot_pen)
        painter.setBrush(QColor(255, 80, 80))
        painter.drawEllipse(QPointF(px, py), 5, 5)


class ControlPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.z = 0.0
        self.z_range = 3
        
        self.w = 0.0
        self.w_range = 3

        self.xy_pad = XYPad(self.run_simulation)

        self.z_slider = QSlider(Qt.Horizontal)
        self.z_slider.setRange(0, 1000)
        self.z_slider.setValue(500)
        self.z_slider.valueChanged.connect(self.update_z)
        
        self.w_slider = QSlider(Qt.Horizontal)
        self.w_slider.setRange(0, 1000)
        self.w_slider.setValue(500)
        self.w_slider.valueChanged.connect(self.update_w)

        self.z_label = QLabel("z = 0.00")
        self.z_label.setAlignment(Qt.AlignCenter)
        
        self.w_label = QLabel("w = 0.00")
        self.w_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.xy_pad)
        layout.addWidget(self.z_label)
        layout.addWidget(self.z_slider)
        layout.addWidget(self.w_label)
        layout.addWidget(self.w_slider)

        self.setLayout(layout)
        self.setWindowTitle("XY + Z + W Parameter Control")

    def update_z(self, value):
        self.z = self.z_range * (2 * (value / 1000) - 1)
        self.z_label.setText(f"z = {self.z:.2f}")
#        self.run_simulation()

    def update_w(self, value):
        self.w = self.w_range * (2 * (value / 1000) - 1)
        self.w_label.setText(f"w = {self.w:.2f}")

    def run_simulation(self):
        x = self.xy_pad.x
        y = self.xy_pad.y
        z = self.z
        w = self.w

        print(f"x={x:.3f}, y={y:.3f}, z={z:.3f}, w={w:.3f}")

        subprocess.run(
            [
                "python3",
                "netgen.py",
                "--S_0", "4",
                "--ratio", "0.35",
                "--periodic",
            ],
            check=True
        )
		
        subprocess.run(
            [
                "./ising_model",
                "--out=monitor",
                "--T=6",
                f"--J_ij={{{x}, {y}, {z}}}",
                f"--D_i={{{w}, 0}}",
            ],
            check=True
        )
		
        subprocess.run(
            ["python3", "plot.py"],
            check=True
        )


app = QApplication([])
plt.ion()
plt.show()

panel = ControlPanel()
panel.show()

app.exec()

