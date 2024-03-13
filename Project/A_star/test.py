from matplotlib import pyplot as plt

import random_map
#
test = random_map.RandomMap()
#

import a_star
from TimeStop import point

me = a_star.AStar(test, point.Point(0, 0), point.Point(9, 9), point.Point(0, 0))

a = point.Point(2, 4)
b = point.Point(1, 8)
print(a)
# a = point.Point(2,7)
# b = point.Point(9,9)
xs = []
ys = []
xs.append(a.x + 0.5)
ys.append(a.y + 0.5)
xs.append(b.x + 0.5)
ys.append(b.y + 0.5)
plt.plot(xs, ys, linewidth=1, color='red')
plt.draw()

# test.ShowMap()
# print(me.IsPassedObstacle(a,b,test.obstacle_point))

# c = point.Point(8,11)
# print(me.IsTurnpoint(a,b,c))




print(me.CalculateDegree(a,b,0))