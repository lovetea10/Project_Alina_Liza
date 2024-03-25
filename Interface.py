import sys
import matplotlib
matplotlib.use("Qt5Agg")

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QTableWidget, QDialog, QFileDialog, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtWidgets
from functions import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(720, 515)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(1500, 530, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(20, 10, 1850, 520))
        self.widget.setObjectName("widget")
        self.groupBox = QtWidgets.QGroupBox(self.widget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1850, 520))
        self.groupBox.setObjectName("groupBox")

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "Графическое отображение"))
class MyFigure(FigureCanvas):

    def __init__(self,width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111)

class MyFigurePolar(FigureCanvas):

    def __init__(self,width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigurePolar,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111, projection = 'polar')

class MyFigure3d(FigureCanvas):

    def __init__(self,width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(MyFigure3d,self).__init__(self.fig)
        self.axes = self.fig.add_subplot(111, projection='3d')


class App(QDialog, Ui_Dialog):

    def __init__(self):
        super(App, self).__init__()
        self.anim1 = None
        self.anim2 = None
        self.setupUi(self)
        self.setWindowTitle("Отобразить графику рисования matplotlib")
        self.title = 'PyQt5 project'
        self.left = 0
        self.top = 50
        self.width = 1900
        self.height = 900
        self.Pixmap()
        self.file = dict() #data
        self.anim = None

    def anim_xy(self):
        data = self.file
        F = MyFigurePolar(width=3, height=2, dpi=100)
        F.axes.set_xlabel("X")
        F.axes.set_ylabel("Y")
        F.axes.grid(True)
        F.trajectory = np.array(data['trajectory'])
        F.fig.suptitle("xy")
        points = make_points_between(data['trajectory']).T

        def update(num, points, ln):
            ln.set_data(np.arctan2(points[0, :num], points[1, :num]),
                        np.sqrt(points[0, :num] ** 2 + points[1, :num] ** 2))
            return ln,

        ln, = F.axes.plot(np.arctan2(points[0, 0:1], points[1, 0:1]),
                          np.sqrt(points[0, 0:1] ** 2 + points[1, 0:1] ** 2))

        F.axes.set_ylim([np.min(points[1, :]), np.max(points[1, :])])

        self.anim = FuncAnimation(F.fig, update, len(points[0]), fargs=(points, ln), interval = 10,
                                  blit=True)

        return F

    def anim_3d(self):
        data = self.file
        F1 = MyFigure3d(width=5, height=4, dpi=100)
        F1.axes.grid(True)
        F1.trajectory = np.array(data['trajectory'])
        F1.fig.suptitle("3d-Plot")
        points = make_points_between(data['trajectory']).T

        def update1(num, points, ln):
            ln.set_data(points[:2, :num])
            ln.set_3d_properties(points[2, :num])
            return ln,

        ln, = F1.axes.plot(points[0, 0:1], points[1, 0:1], points[2, :1])
        F1.axes.set_xlim3d([np.min(points[0, :]), np.max(points[0, :])])
        F1.axes.set_xlabel('X')

        F1.axes.set_ylim3d([np.min(points[1, :]), np.max(points[1, :])])
        F1.axes.set_ylabel('Y')

        F1.axes.set_zlim3d([np.min(points[2, :]), np.max(points[2, :])])
        F1.axes.set_zlabel('Z')

        self.anim1 = FuncAnimation(F1.fig, update1, len(points[0]), fargs=(points, ln), interval = 10,
                            blit=True)

        return F1

    def anim_hd(self):
        data = self.file
        F2 = MyFigure(width=7, height=6, dpi=100)
        F2.axes.set_xlabel("X")
        F2.axes.set_ylabel("Y")
        F2.axes.grid(True)
        F2.trajectory = np.array(data['trajectory'])
        F2.fig.suptitle("Height-distance plot")
        points = make_points_between(data['trajectory']).T

        def update2(num, points, ln):
            ln.set_data((points[0, :num] ** 2 + points[1, :num] ** 2) ** 0.5, points[2, :num])
            return ln,

        ln, = F2.axes.plot((points[0, :1] ** 2 + points[1, :1] ** 2) ** 0.5, points[2, :1])
        F2.axes.set_xlim(
            [np.min(points[0, :] ** 2 + points[1, :] ** 2) ** 0.5, np.max(points[0, :] ** 2 + points[1, :] ** 2)])

        F2.axes.set_ylim([np.min(points[2, :]), np.max(points[2, :])])

        self.anim2 = FuncAnimation(F2.fig, update2, len(points[0]), fargs=(points, ln), interval = 10,
                                   blit=True)
        return F2

    def myfunc(self):
        F = self.anim_xy()
        F1 = self.anim_3d()
        F2 = self.anim_hd()

        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(F, 0, 1)
        self.gridlayout.addWidget(F1, 0, 2)
        self.gridlayout.addWidget(F2, 0, 3)
    def Pixmap(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.Buttons()
        self.Presentashion()
        self.DataTable()
        self.show()
    def Label(self):

        label2 = QLabel(self)
        label2.setText("Цель обнаружена!")
        label2.setGeometry(300, 400, 200, 50)
    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "JSON Files (*.json);;All Files (*)")
        try:
            if filename:
                with open(filename, 'r') as file:
                    contents = file.read()
            self.file = json.loads(contents)
        except:
            print("НЕПРАВИЛЬНЫЙ ФОРМАТ JSON!!!")

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", ".", "JSON Files (*.json);;All Files (*)")
        if filename:
            with open(filename, 'w') as file:
                file.write("filename")
    def print_file(self):
        self.myfunc()
        self.Label()
    def Buttons(self):
        pybutton = QPushButton('ОТКРЫТЬ', self)
        pybutton.resize(85, 60)
        pybutton.move(120, 600)
        pybutton.clicked.connect(self.open_file)

        pybutton1 = QPushButton('СТАРТ', self)
        pybutton1.clicked.connect(self.print_file)
        pybutton1.resize(85, 60)
        pybutton1.move(215, 600)

        pybutton2 = QPushButton('ПЕРЕХВАТ', self)
        pybutton2.clicked.connect(self.clickMethod)
        pybutton2.resize(85, 60)
        pybutton2.move(310, 600)

        pybutton3 = QPushButton('МЕТОД: ТТ', self)
        pybutton3.clicked.connect(self.clickMethod)
        pybutton3.resize(85, 60)
        pybutton3.move(405, 600)

        pybutton4 = QPushButton('ПРЕРВАТЬ', self)
        pybutton4.clicked.connect(self.clickMethod)
        pybutton4.resize(85, 60)
        pybutton4.move(500, 600)
    def clickMethod(self):
        print('Button pressed in PyQt application.')
    def DataTable(self):

        table = QTableWidget(self)
        table.verticalScrollBar()
        table.setColumnCount(14)
        table.setRowCount(6)

        # Set the table headers
        table.setHorizontalHeaderLabels(["Number", "X coord_goal", "Y coord_goal", "Z coord_goal", "r coord_goal",
                                         "β coord_goal", "ε coord_goal", "X coord_interceptor", "Y coord_interceptor",
                                         "Z coord_interceptor", "r coord_interceptor", "β coord_interceptor", "ε coord_interceptor", "Distance"])
        table.setGeometry(120, 700, 1730, 100)
        table.resizeColumnsToContents()

    def Presentashion(self):
        dialog = QDialog()
        dialog.setFixedSize(400, 300)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())

