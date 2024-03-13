import time

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

xpoints = 1
ypoints = 1

# plt.figure(figsize=(2,8))
# plt.scatter(xpoints, ypoints, s=100)
rec = Rectangle((xpoints - 0.5, ypoints - 0.5), width=1, height=1, color='black')
plt.gca().add_patch(rec)
plt.xlim((0,10))
plt.ylim((0,10))
plt.grid(True)
# plt.show()
# time.sleep(1)

plt.pause(1)
plt.cla()
plt.xlim(0,100)
plt.ylim(0,100)
plt.grid(True)
xpoints = np.array([10, 60])
ypoints = np.array([5, 72])
# plt.figure(figsize=(2,8))
plt.plot(xpoints, ypoints, 'o')


plt.draw()
plt.show()