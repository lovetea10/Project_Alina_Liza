import os
import sys
import matplotlib
from Ui_Dialog import Ui_Dialog
from MyFigure import MyFigure, MyFigure3d, MyFigurePolar
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QTableWidget, QDialog, QFileDialog, QGridLayout, \
    QMessageBox, QVBoxLayout
from functions import *
class App(QDialog, Ui_Dialog):

    def __init__(self):
        super(App, self).__init__()
        self.anim = None
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
    def initUI_anim(self):
        self.figure_canvas = MyFigurePolar()
        self.anim_2d()
        self.anim_sector()
        self.show()
        return self.figure_canvas

    def anim_2d(self):
        data = self.file
        points = make_points_between(data['trajectory']).T
        self.ln, = self.figure_canvas.axes.plot(np.arctan2(points[0, 0:1], points[1, 0:1]),
                                                np.sqrt(points[0, 0:1] ** 2 + points[1, 0:1] ** 2))

        def update(num):
            self.ln.set_data(np.arctan2(points[0, :num], points[1, :num]),
                             np.sqrt(points[0, :num] ** 2 + points[1, :num] ** 2))
            self.update_sector(num)
            return self.ln,

        self.anim = FuncAnimation(self.figure_canvas.fig, update, frames=len(points[0]),
                                  interval=10000 / len(points[0]))

    def update_sector(self, frame):
        r = 6
        period = np.pi / 32
        self.sector.remove() if hasattr(self, 'sector') else None
        self.figure_canvas.axes.set_theta_zero_location("N")
        self.figure_canvas.axes.set_theta_direction(-1)
        start = frame * np.pi / 180
        end = start - period
        self.figure_canvas.axes.set_yticklabels([5000, 10000, 15000, 20000, 25000])
        self.sector = self.figure_canvas.axes.fill_between([start, end], 0, r, alpha=0.5, facecolor='red')
        self.figure_canvas.draw()

    def anim_sector(self):
        self.anim0 = FuncAnimation(self.figure_canvas.fig, self.update_sector, frames=360, interval=15)

    def anim_3d(self):
        data = self.file
        radius = 1000
        center_cords = [0, 0, 0]
        place_angles = [0, np.deg2rad(40)]
        asimuths = [0, np.deg2rad(40)]
        delta = np.pi / 180

        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        fig.suptitle("3d-Plot")

        points = make_points_between(data['trajectory']).T

        ax.disable_mouse_rotation()
        ax.set_xlim3d([-radius, radius])
        ax.set_ylim3d([-radius, radius])
        ax.set_zlim3d([-radius, radius])
        # Определяем углы theta и phi для создания шарового сектора
        theta = np.linspace(place_angles[0], place_angles[1], 20)
        phi = np.linspace(asimuths[0], asimuths[1], 20)
        # radius = np.linspace(0, max_radius, 100)

        # Создаем сетку из углов для шарового сектора
        T, P = np.meshgrid(theta, phi)

        # Вычисляем координаты точек на поверхности шарового сектора
        x = center_cords[0] + radius * np.cos(P) * np.cos(T)
        y = center_cords[1] + radius * np.cos(P) * np.sin(T)
        z = center_cords[2] + radius * np.sin(P)

        show_sphere_side_left_right(center_cords, radius, asimuths, place_angles[0], ax)

        show_sphere_side_left_right(center_cords, radius, asimuths, place_angles[1], ax)

        show_sphere_side_up_down(center_cords, radius, place_angles, asimuths[0], ax)

        show_sphere_side_up_down(center_cords, radius, place_angles, asimuths[1], ax)

        ax.plot_surface(x, y, z, color='r', alpha=0.7)

        def update(frame, points, max_frame):
            ax.cla()
            ax.set_xlim3d([-radius, radius])
            ax.set_ylim3d([-radius, radius])
            ax.set_zlim3d([0, radius])

            ax.plot(points[0, :frame], points[1, :frame], points[2, :frame])

            place_angles[0] += delta
            place_angles[1] += delta

            # Определяем углы theta и phi для создания шарового сектора
            theta = np.linspace(place_angles[0], place_angles[1], 20)
            phi = np.linspace(asimuths[0], asimuths[1], 20)
            # radius = np.linspace(0, max_radius, 100)

            # Создаем сетку из углов для шарового сектора
            T, P = np.meshgrid(theta, phi)

            # Вычисля   ем координаты точек на поверхности шарового сектора
            x = center_cords[0] + radius * np.cos(P) * np.cos(T)
            y = center_cords[1] + radius * np.cos(P) * np.sin(T)
            z = center_cords[2] + radius * np.sin(P)

            show_sphere_side_left_right(center_cords, radius, asimuths, place_angles[0], ax)

            show_sphere_side_left_right(center_cords, radius, asimuths, place_angles[1], ax)

            show_sphere_side_up_down(center_cords, radius, place_angles, asimuths[0], ax)

            show_sphere_side_up_down(center_cords, radius, place_angles, asimuths[1], ax)

            ax.plot_surface(x, y, z, color='r', alpha=0.7)
            return ax

        self.anim1 = FuncAnimation(fig=fig, func=update, frames=len(points[0]), fargs=(points, 180), interval=10,
                                   blit=False)
        return MyFigure3d(fig=fig, ax=ax)

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
        F0 = self.initUI_anim()
        F1 = self.anim_3d()
        F2 = self.anim_hd()


        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.addWidget(F0, 0, 1)
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

