import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

fig, ax = plt.subplots(figsize=(6, 3))
x = range(20)
y = [0] * 20

bars = ax.bar(x, y, color="blue")
ax.axis([0, 20, 0, 10])  # x-axis from 0 to 20
                         # y-axis from 0 to 10

def update(frame):
    y[frame] = np.random.randint(0, 10)
    bars[frame].set_height(y[frame])

anim = FuncAnimation(fig, update, frames=20, interval=100)
plt.show()

