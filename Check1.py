import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

r = 7
period = np.pi / 64
sector = ax.fill_between([], [], [], alpha=0.5, facecolor='red')  # Начинать с красного цвета

def update(frame):
    ax.clear()
    theta = np.linspace(0, 2 * np.pi, 100)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(theta, np.ones(100) * r, linestyle='-', color='black')
    start = frame * np.pi / 180
    end = start - period
    sector = ax.fill_between([start, end], 0, r, alpha=0.5, facecolor='red')
    ax.set_yticklabels([5000, 10000, 15000, 20000, 25000])

    return sector,

ani = FuncAnimation(fig, update, frames=360, interval=15, blit=True)
plt.show()

