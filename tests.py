from functions import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import json


def test_trajectory_and_sphere_sector():
    point_1 = np.zeros(3)
    point_2 = np.ones(3)
    trajectory = np.array([point_1, point_2])
    print(current_pos(trajectory, 5, 1))

    print(is_on_sphere_sector(point_2, point_1, 3, [0, np.pi/2], [0, np.pi/2]))
    print(is_on_sphere_sector(point_1, point_2, 3, [0, np.pi/2], [0, np.pi/2]))
    print(is_on_sphere_sector(point_1, point_2, 3, [np.pi/2, np.pi], [0, np.pi/2]))

    show_sphere_sector_and_point(point_2, point_1, 3, [0, np.pi/2], [0, np.pi/2])
    show_sphere_sector_and_point(point_1, point_2, 3, [0, np.pi/2], [0, np.pi/2])
    show_sphere_sector_and_point(point_1, point_2, 3, [np.pi/2, np.pi], [0, np.pi/2])
    show_sphere_sector_and_point(point_1, point_2, 3, [0, 2*np.pi], [0, 2*np.pi])
    plt.show()


def test_json_and_plots():
    trajectory = [[np.sin(i), i, np.exp(i)] for i in range(8)]
    json_file = open("test.json", 'w')
    json.dump({"speed": 10, "trajectory": trajectory}, json_file)
    json_file = open("test.json", 'r')
    data = json_handle(json_file)
    trajectory_plot(data)
    XY_projection_plot(data)
    height_distance_plot(data)
    plt.show()


def test_animation_3d():
    trajectory = [[np.sin(i), i, np.exp(i)] for i in range(8)]
    json_file = open("test.json", 'w')
    json.dump({"speed": 10, "trajectory": trajectory}, json_file)
    json_file = open("test.json", 'r')
    data = json_handle(json_file)
    animation_3d(data)


def test_animation_xy():
    trajectory = [[np.sin(i), i, np.exp(i)] for i in range(8)]
    json_file = open("test.json", 'w')
    json.dump({"speed": 10, "trajectory": trajectory}, json_file)
    json_file = open("test.json", 'r')
    data = json_handle(json_file)
    animation_xy(data)

def test_rotating_sphere_sector():
    radius = 50000
    center_cords = [0, 0, 0]
    place_angles = [0, np.deg2rad(40)]
    asimuths = [0, np.deg2rad(40)]
    delta = np.pi/180


    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    ax.disable_mouse_rotation()
    ax.set_xlim3d([-50000, 50000])
    ax.set_ylim3d([-50000, 50000])
    ax.set_zlim3d([-50000, 50000])
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

    ax.plot_surface(x, y, z, color='b', alpha=0.7)

    def update(frame):
        ax.cla()
        ax.set_xlim3d([-50000, 50000])
        ax.set_ylim3d([-50000, 50000])
        ax.set_zlim3d([-50000, 50000])

        place_angles[0] += delta
        place_angles[1] += delta

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

        ax.plot_surface(x, y, z, color='b', alpha=0.7)
        return ax


    ani = FuncAnimation(fig=fig, func=update, frames = 180, interval = 3, blit = False)

    plt.show()

test_rotating_sphere_sector()
