import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from TimeStop import point


class EAMap:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.obstacle_point = []

    def GenerateMap(self,map):
        self.height = map.__len__()
        if self.height == 0:
            print("地图大小为0！")
            return None
        self.width = map[0].__len__()
        for i in range(self.height):
            for j in range(self.width):
                if map[i][j] == 1:
                    self.obstacle_point.append(point.Point(j, self.height - i - 1))

    def  IsObstacle(self,i,j):
        for p in self.obstacle_point:
            if i == p.x and j == p.y:
                return True
        return False

    def ShowMap(self):
        x = np.array(range(self.width))
        y = np.array(range(self.height))
        plt.xticks(x)
        plt.yticks(y)
        plt.grid(linestyle='-')
        for i in range(self.width):
            for j in range(self.height):
                if self.IsObstacle(i, j):
                    rec = Rectangle((i-0.5, j-0.5), width=1, height=1, color='black')
                    plt.gca().add_patch(rec)
        plt.show()

    def GetObstaclePoint(self):
        return self.obstacle_point