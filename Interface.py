import os
import sys
import matplotlib
from Ui_Dialog import Ui_Dialog
from MyFigure import MyFigure, MyFigure3d, MyFigurePolar
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QTableWidget, QDialog, QFileDialog, QGridLayout, \
    QMessageBox
from functions import *
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

    def anim_2d(self):
        F = MyFigurePolar(width=3, height=2, dpi=100)
        F.axes.grid(True)
        r = 5
        period = np.pi / 64
        sector = F.axes.fill_between([], [], [], alpha=0.5)

        data = self.file
        F.trajectory = np.array(data['trajectory'])
        points = make_points_between(data['trajectory']).T

        def update(frame):
            F.axes.clear()
            theta = np.linspace(0, 2 * np.pi, 100)
            F.axes.set_theta_zero_location("N")
            F.axes.set_theta_direction(-1)
            F.axes.plot(theta, np.ones(100) * r, linestyle='-', color='black')
            start = frame * np.pi / 180
            end = start - period
            sector = F.axes.fill_between([start, end], 0, r, alpha=0.5)
            F.axes.set_yticklabels([])
            return sector,

        self.anim = FuncAnimation(F.fig, update, frames=360, interval=15, blit=True)


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
        F = self.anim_2d()
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
        self.Buttons_1()
        self.Buttons_2()
        self.Buttons_3()
        self.Buttons_4()
        self.Presentashion()
        self.DataTable()
        self.show()
    def Label(self):

        label2 = QLabel(self)
        label2.setText("Цель обнаружена!")
        label2.setGeometry(300, 400, 200, 50)
    def open_file(self):
        self.file, _ = QFileDialog.getOpenFileName(self, "Open File", ".", "JSON Files (*.json);;All Files (*)")
        self.root = os.path.join(self.file)
        if self.file:
            try:
                with open(self.file, 'r') as self.filename:
                    contents = self.filename.read()
                    self.file = json.loads(contents)
                    self.pybutton1.setEnabled(True)
            except json.JSONDecodeError:
                self.handleButton()

    def save_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", ".", "JSON Files (*.json);;All Files (*)")
        with open(filename, 'w') as file:
            file.write("filename")

    def print_file(self):
        self.pybutton3.setEnabled(True)
        self.myfunc()
        self.Label()
    def handleButton(self):
        QMessageBox.information(None, 'Сообщение от программы', "Неверный формат файла JSON.")
    def Buttons(self):
        self.pybutton = QPushButton('ОТКРЫТЬ', self)
        self.pybutton.resize(85, 60)
        self.pybutton.move(120, 600)
        self.pybutton.clicked.connect(self.open_file)

    def Buttons_1(self):
        self.pybutton1 = QPushButton('СТАРТ', self)
        self.pybutton1.resize(85, 60)
        self.pybutton1.move(215, 600)
        self.pybutton1.setEnabled(False)
        self.pybutton1.clicked.connect(self.print_file)

    def Buttons_2(self):
        self.pybutton2 = QPushButton('ПЕРЕХВАТ', self)
        self.pybutton2.clicked.connect(self.clickMethod)
        self.pybutton2.resize(85, 60)
        self.pybutton2.move(310, 600)

    def Buttons_3(self):
        self.pybutton3 = QPushButton('МЕТОД: ТТ', self)
        self.pybutton3.resize(85, 60)
        self.pybutton3.move(405, 600)
        self.pybutton3.setEnabled(False)
        self.pybutton3.clicked.connect(self.clickMethod)
        self.pybutton3.clicked.connect(self.changeName)

    def changeName(self):
        current_text = self.pybutton3.text()
        if current_text == 'МЕТОД: ТТ':
            self.pybutton3.setText('МЕТОД:\nСПРЯМ')
        if current_text == 'МЕТОД:\nСПРЯМ':
            self.pybutton3.setText('МЕТОД: ТТ')

    def Buttons_4(self):
        self.pybutton4 = QPushButton('ПРЕРВАТЬ', self)
        self.pybutton4.clicked.connect(self.clickMethod)
        self.pybutton4.clicked.connect(self.close_filename)
        self.pybutton4.resize(85, 60)
        self.pybutton4.move(500, 600)

    def close_filename(self):
        try:
            if hasattr(self, 'filename') and self.filename:
                self.filename.close()
                QMessageBox.information(self, "Удаление файла", "Файл JSON успешно удален.")
        except Exception as e:
            QMessageBox.information(self, "Удаление файла", f"Не удалось удалить файл: {str(e)}")

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

