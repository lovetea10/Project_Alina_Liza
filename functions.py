import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import json


def current_pos(trajectory, v, t):
    if t < 0 or v < 0:
        print("Неверные данные: время или скорость отрицательны!")
        return -1

    if v == 0 or len(trajectory) == 1:
        return trajectory[0]

    cur_t = 0
    cur_point = 1

    while cur_point < len(trajectory):
        direction = trajectory[cur_point] - trajectory[cur_point - 1]
        mag = np.linalg.norm(direction)
        if cur_t + mag/v < t and cur_point != len(trajectory) - 1:
            cur_t += mag/v
            cur_point += 1
            continue
        res = trajectory[cur_point - 1] + direction * (v * t / mag)
        return res

    print("Траектория не задана ни одной точкой!")
    return -1


def is_on_sphere_sector(point_cords, center_cords, radius, place_angles, asimuths):
    relative_cords = point_cords - center_cords

    if np.array_equal(relative_cords, np.zeros(3)):
        return True

    point_radius = np.linalg.norm(relative_cords)
    point_psi = np.arcsin(relative_cords[2] / point_radius)
    point_phi = np.arcsin(relative_cords[1] / ((relative_cords[0] ** 2 + relative_cords[1] ** 2)**0.5))
    if point_radius < radius and place_angles[0] < point_psi < place_angles[1] and asimuths[0] < point_phi < asimuths[1]:
        return True
    return False


def show_sphere_side_left_right(center_cords, radius, border_angles, angle, ax):
    rad = np.linspace(0, radius, 10)
    psi = np.linspace(border_angles[0], border_angles[1], 10)
    rad, psi = np.meshgrid(rad, psi)

    x = center_cords[0] + rad * np.cos(psi) * np.cos(angle)
    y = center_cords[1] + rad * np.cos(psi) * np.sin(angle)
    z = center_cords[2] + rad * np.sin(psi)

    ax.plot_surface(x, y, z, color='r', alpha=0.7)


def show_sphere_side_up_down(center_cords, radius, border_angles, angle, ax):
    rad = np.linspace(0, radius, 10)
    psi = np.linspace(border_angles[0], border_angles[1], 10)
    rad, psi = np.meshgrid(rad, psi)

    x = center_cords[0] + rad * np.cos(angle) * np.cos(psi)
    y = center_cords[1] + rad * np.cos(angle) * np.sin(psi)
    z = center_cords[2] + rad * np.sin(angle)

    ax.plot_surface(x, y, z, color='r', alpha=0.7)


def show_sphere_sector_and_point(point_cords, center_cords, radius, place_angles, asimuths):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # Определяем углы theta и phi для создания шарового сектора
    theta = np.linspace(place_angles[0], place_angles[1], 20)
    phi = np.linspace(asimuths[0], asimuths[1], 20)
    #radius = np.linspace(0, max_radius, 100)

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

    ax.scatter(point_cords[0], point_cords[1], point_cords[2], color='r')
    # Настройка осей и масштаба
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')


def validate_json(json_file):
    candidate = json.load(json_file)
    if list(candidate.keys()) != ['speed', 'trajectory']:
        return False

    if not(isinstance(candidate['speed'], float) or isinstance(candidate['speed'], int)):
        return False

    if not(isinstance(candidate['trajectory'], list)):
        return False

    for i in candidate['trajectory']:
        if not isinstance(i, list):
            return False

        if len(i) != 3:
            return False

        for j in i:
            if not (isinstance(j, float) or isinstance(j, int)):
                return False

    return candidate


def error():
    print("НЕПРАВИЛЬНЫЙ ФОРМАТ JSON!!!")
    exit()


def json_handle(json_file):
    data = validate_json(json_file)
    if not data:
        error()

    return data


def trajectory_plot(data):
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, label="3D trajectory plot")
    trajectory = np.array(data['trajectory'])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot(trajectory[:, 0], trajectory[:, 1], trajectory[:, 2])


def XY_projection_plot(data):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, label="XY projection plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    trajectory = np.array(data['trajectory'])
    ax.plot(np.arctan2(trajectory[:, 0], trajectory[:, 1]), np.sqrt(trajectory[:, 0]**2 + trajectory[:, 1]**2))


def height_distance_plot(data):
    plt.figure("Height-distance plot")
    trajectory = np.array(data['trajectory'])
    x = trajectory[:, 0]
    y = trajectory[:, 1]
    z = trajectory[:, 2]
    plt.xlabel("distance")
    plt.ylabel("height")
    plt.grid()
    distance = (x**2 + y**2) ** 0.5
    plt.plot(distance, z)

def make_points_between(trajectory):
    res = []
    for i in range(len(trajectory) - 1):
        tmp = np.linspace(trajectory[i], trajectory[i + 1], 50)
        for j in tmp:
            res.append(j)
    return np.array(res)


def animation_3d(data):

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, label="3D trajectory plot")

    points = make_points_between(data['trajectory']).T

    def update(num, points, ln):
        ln.set_data(points[:2, :num])
        ln.set_3d_properties(points[2, :num])
        return ln,

    ln, = ax.plot(points[0, 0:1], points[1, 0:1], points[2, :1])
    ax.set_xlim3d([np.min(points[0, :]), np.max(points[0, :])])
    ax.set_xlabel('X')

    ax.set_ylim3d([np.min(points[1, :]), np.max(points[1, :])])
    ax.set_ylabel('Y')

    ax.set_zlim3d([np.min(points[2, :]), np.max(points[2, :])])
    ax.set_zlabel('Z')

    ani = FuncAnimation(fig, update, len(points[0]), fargs=(points, ln), interval=10000/len(points[0]), blit=False)
    plt.show()

def animation_xy(data):
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, label="XY projection plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)

    points = make_points_between(data['trajectory']).T

    def update(num, points, ln):
        ln.set_data(np.arctan2(points[0, :num], points[1, :num]), np.sqrt(points[0, :num] ** 2 + points[1, :num] ** 2))
        return ln,

    ln, = ax.plot(np.arctan2(points[0, 0:1], points[1, 0:1]), np.sqrt(points[0, 0:1] ** 2 + points[1, 0:1] ** 2))
    ax.set_xlim([np.min(points[0, :]), np.max(points[0, :])])
    ax.set_xlabel('X')

    ax.set_ylim([np.min(points[1, :]), np.max(points[1, :])])
    ax.set_ylabel('Y')

    ani = FuncAnimation(fig, update, len(points[0]), fargs=(points, ln), interval=10000/len(points[0]), blit=False)
    plt.show()
