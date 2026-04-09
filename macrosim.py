#!/usr/bin/env python3

import subprocess
import numpy as np
import matplotlib.pyplot as plt
import re

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QLabel, QPushButton
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QColor, QPen


class XYPad(QWidget):
    def __init__(self, on_change):
        super().__init__()
        self.setMinimumSize(300, 300)

        self.norm_x = 0.5
        self.norm_y = 0.5
        
        self.x_range = 1
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
        
        self.run_button = QPushButton("Run Simulation")
        self.run_button.clicked.connect(self.run_simulation)

        self.xy_pad = XYPad(self.update_xy_labels)
        self.xy_label = QLabel("J_1 = 0.00    D_1 = 0.00")
        self.xy_label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.xy_label)
        layout.addWidget(self.xy_pad)
        
        layout.addWidget(self.run_button)

        self.j0_slider, self.j0_label = self.add_slider("J_0", 5, layout)
        self.jij_slider, self.jij_label = self.add_slider("J_ij", 5, layout)
        self.ratio, self.ratio_label = self.add_slider("Ratio", 1, layout)

        self.setLayout(layout)
        self.setWindowTitle("Macrosimulator")

    def add_slider(self, name, value_range, layout):
        label = QLabel(f"{name} = 0.00")
        label.setAlignment(Qt.AlignCenter)

        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 1000)
        slider.setValue(500)

        def update(value):
            v = value_range * (2 * (value / 1000) - 1)
            label.setText(f"{name} = {v:.2f}")
            setattr(self, name.lower(), v)

        slider.valueChanged.connect(update)

        layout.addWidget(label)
        layout.addWidget(slider)

        update(slider.value())  # initialize value

        return slider, label
    
    def update_xy_labels(self):
        x = self.xy_pad.x
        y = self.xy_pad.y
        self.xy_label.setText(f"J_1 = {x:.2f}    D_1 = {y:.2f}")

    def run_line(self, line):
        comm = line.split(" ")    
        subprocess.run(comm, check=True)
    
    def run_simulation(self):
        x = self.xy_pad.x
        y = self.xy_pad.y
        J_0 = self.j_0
        J_ij = self.j_ij
        r = self.ratio

#        self.run_line("./fieldgen.py --rate 0.01 --range 6")        
#        self.run_line(f"python3 netgen.py --ratio 0 --size 50 --S_0 1 --S_1 2")
        self.run_line(f'./ising_model --J_ij={{{J_0},{x},{J_ij}}} --D_i={{0,{y}}} --out=monitor')
        self.run_line("./fig_plot.py --trim --column 2 --xRange -2.5 2.5 --show")
#        
#        self.run_line(f"python3 netgen.py --ratio 1 --size 50 --S_0 1 --S_1 2")
#        self.run_line(f'./ising_model --J_ij={{3.4,{x},{z}}} --D_i={{0,{y}}} --out=monitor')
#        self.run_line("./fig_plot.py --trim --column 1 --name nitcne_hyst")
#        
#        self.run_line(f"python3 netgen.py --ratio {w*0.53} --size 50 --S_0 1 --S_1 2")
#        self.run_line("./fieldgen.py --rate 0.01 --range 2.5")
#        self.run_line(f'./ising_model --J_ij={{3.4,{x},{z}}} --D_i={{0,{y}}} --out=monitor')
#        self.run_line("./fig_plot.py --trim --column 2 --name fe_hyst")
#        self.run_line("./fig_plot.py --trim --column 1 --name ni_hyst")
#        
#        self.run_line(f"python3 netgen.py --ratio {w} --size 50 --S_0 1 --S_1 2")
#        self.run_line(f'./ising_model --J_ij={{3.4,{x},{z}}} --D_i={{0,{y}}} --out=monitor')
#        self.run_line("./fig_plot.py --trim --column 2 --name nife_fe_04_hyst")
#        self.run_line("./fig_plot.py --trim --column 1 --name nife_04_hyst --normalize 2 --yRange -1.2 1.2")

app = QApplication([])
plt.ion()
plt.show()

panel = ControlPanel()
panel.show()

app.exec()

