import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QWidget, QVBoxLayout
import json

class MyFigurePolar(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100, fig=None, ax=None):
        if fig is None:
            self.fig = Figure(figsize=(width, height), dpi=dpi)
            self.axes = self.fig.add_subplot(111, projection='polar')
        else:
            self.fig = fig
            self.axes = ax
        super(MyFigurePolar, self).__init__(self.fig)

def make_points_between(trajectory):
    res = []
    for i in range(len(trajectory) - 1):
        tmp = np.linspace(trajectory[i], trajectory[i + 1], 50)
        for j in tmp:
            res.append(j)
    return np.array(res)

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Animation Demo')
        layout = QVBoxLayout(self)
        self.figure_canvas = MyFigurePolar()
        layout.addWidget(self.figure_canvas)

        self.anim_2d()
        self.anim_sector()

        self.show()

    def anim_2d(self):
        with open('test.json') as f:
            data = json.load(f)

        points = make_points_between(data['trajectory']).T
        self.ln, = self.figure_canvas.axes.plot(np.arctan2(points[0, 0:1], points[1, 0:1]),
                                                np.sqrt(points[0, 0:1] ** 2 + points[1, 0:1] ** 2))

        def update(num):
            self.ln.set_data(np.arctan2(points[0, :num], points[1, :num]),
                             np.sqrt(points[0, :num] ** 2 + points[1, :num] ** 2))
            self.update_sector(num)
            return self.ln,

        self.anim = FuncAnimation(self.figure_canvas.fig, update, frames=len(points[0]), interval=10000 / len(points[0]))

    def update_sector(self, frame):
        r = 7
        period = np.pi / 64
        self.sector.remove() if hasattr(self, 'sector') else None
        start = frame * np.pi / 180
        end = start - period
        self.sector = self.figure_canvas.axes.fill_between([start, end], 0, r, alpha=0.5, facecolor='red')
        self.figure_canvas.draw()

    def anim_sector(self):
        self.anim0 = FuncAnimation(self.figure_canvas.fig, self.update_sector, frames=360, interval=15)

if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    widget = MyWidget()
    sys.exit(app.exec_())