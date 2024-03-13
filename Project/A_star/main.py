import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

import random_map
import a_star
from TimeStop.point import Point

plt.figure(figsize=(5, 5))

map = random_map.RandomMap()

ax = plt.gca()
ax.set_xlim([0, map.size])
ax.set_ylim([0, map.size])

for i in range(map.size):
    for j in range(map.size):
        if map.IsObstacle(i, j):
            rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
        else:
            rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
            ax.add_patch(rec)


plt.axis('equal')
plt.axis('off')
plt.tight_layout()
# plt.show()

start_point = Point(0,0)
end_point = Point(9,9)

a_star = a_star.AStar(map,start_point,end_point,start_point)
a_star.Run(ax, plt)
print(a_star.PathForRobot(a_star.shortest_path,0.00))
# print(a_star.shortest_path)