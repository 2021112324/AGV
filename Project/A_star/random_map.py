from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from TimeStop import point


class RandomMap:
    def __init__(self, size=10):
        self.size = size
        self.obstacle = size//8
        self.test_map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                         [0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
                         [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                         ]
        self.GenerateObstacle()



    def GenerateObstacle(self):

        self.obstacle_point = []
        for i in range(self.test_map.__len__()):
            for j in range(self.test_map[0].__len__()):
                if self.test_map[i][j] == 1:
                    self.obstacle_point.append(point.Point(i, j))


        # self.obstacle_point.append(point.Point(self.size//2, self.size//2))
        # self.obstacle_point.append(point.Point(self.size//2, self.size//2 - 1))
        #
        # for i in range(self.size//2-2,self.size//2):
        #     self.obstacle_point.append(point.Point(i, self.size - i))
        #     self.obstacle_point.append(point.Point(i, self.size - i - 1))
        #     self.obstacle_point.append(point.Point(self.size - i, i))
        #     self.obstacle_point.append(point.Point(self.size - i - 1, i))
        #
        # for i in range(self.obstacle-1):
        #     x = np.random.randint(0,self.size)
        #     y = np.random.randint(0,self.size)
        #     self.obstacle_point.append(point.Point(x,y))
        #
        #     if(np.random.rand()>0.5):
        #         for l in range(self.size // 4):
        #             self.obstacle_point.append(point.Point(x, y + l))
        #             pass
        #     else:
        #         for l in range(self.size // 4):
        #             self.obstacle_point.append(point.Point(x + l, y))
        #             pass

    def  IsObstacle(self,i,j):
        for p in self.obstacle_point:
            if i == p.x and j == p.y:
                return True
        return False

    def ShowMap(self):
        ax = plt.gca()
        ax.set_xlim([0, self.size])
        ax.set_ylim([0, self.size])

        for i in range(self.size):
            for j in range(self.size):
                if self.IsObstacle(i, j):
                    rec = Rectangle((i, j), width=1, height=1, color='gray')
                    ax.add_patch(rec)
                else:
                    rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
                    ax.add_patch(rec)

        rec = Rectangle((0, 0), width=1, height=1, facecolor='b')
        ax.add_patch(rec)

        rec = Rectangle((self.size - 1, self.size - 1), width=1, height=1, facecolor='r')
        ax.add_patch(rec)

        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    def GetObstaclePoint(self):
        return self.obstacle_point