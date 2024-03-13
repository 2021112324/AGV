# a_star.py
import math
import os
import sys
import time

import numpy as np

from matplotlib.patches import Rectangle

from TimeStop import point


class AStar:
    def __init__(self, map, start, end, margin_left_down):
        self.map = map
        self.open_set = []
        self.close_set = []
        self.path = './img' + str(int(round(time.time()))) + '/'
        self.start = start
        self.end = end
        # 地图的左下角位置，用于确定地图位置
        self.margin_left_down = margin_left_down
        self.shortest_path = []

    # 距离起点的长度
    def BaseCost(self, p):
        x_dis = p.x - self.start.x
        y_dis = p.y - self.start.y
        return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

    # 距离终点的长度
    def HeuristicCost(self, p):
        x_dis = self.end.x - 1 - p.x
        y_dis = self.end.y - 1 - p.y
        return x_dis + y_dis + (np.sqrt(2) - 2) * min(x_dis, y_dis)

    # 总权重
    def TotalCost(self, p):
        return self.BaseCost(p) + self.HeuristicCost(p)

    # 两点间距离
    def Distance(self, p1, p2):
        return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    # 该点是否可经过
    def IsValidPoint(self, x, y):
        if x < self.margin_left_down.x or y < self.margin_left_down.y:
            return False
        if x >= self.margin_left_down.x + self.map.size or y >= self.margin_left_down.y + self.map.size:
            return False
        return not self.map.IsObstacle(x, y)

    # 点列表中是否有该点
    def IsInPointList(self, p, point_list):
        for point in point_list:
            if point.x == p.x and point.y == p.y:
                return True
        return False

    def IsInOpenList(self, p):
        return self.IsInPointList(p, self.open_set)

    def IsInCloseList(self, p):
        return self.IsInPointList(p, self.close_set)

    def IsStartPoint(self, p):
        return p.x == self.start.x and p.y == self.start.y

    def IsEndPoint(self, p):
        return p.x == self.end.x and p.y == self.end.y

    # 判断两点之间是否通过障碍
    # 待优化：1.每次寻找最短路径都会遍历所有障碍，实际上只要遍历起点终点间的障碍即可
    #        2.判断是否经过障碍物的方法需要调节
    def IsPassedObstacle(self,p1,p2,obstacle_point):
        # 机器人距障碍物最短距离
        min_distance = 1
        flag = False
        for op in obstacle_point:
            # tempop = point.Point(op.x + 0.5,op.y + 0.5)
            disbot = self.Distance(p1,p2)               # 两点间距离
            dis1 = self.Distance(op,p1)
            dis2 = self.Distance(op,p2)
            if dis1 < min_distance or dis2 < min_distance:
                flag = True
                continue
            cos_deg1 = (dis1 ** 2 + disbot ** 2 - dis2 ** 2) / (2 * dis1 * disbot) # 底角余弦
            cos_deg2 = (dis2 ** 2 + disbot ** 2 - dis1 ** 2) / (2 * dis2 * disbot)
            # 当障碍物距离两点中其中一点距离过近，则视为经过障碍
            # 当障碍物在两点之间，且距离俩点直线过近，则视为经过障碍
            if cos_deg1 > 0 and cos_deg2 > 0:
                if np.sqrt(abs(dis1 ** 2 - 1)) + np.sqrt(abs(dis2 ** 2 - 1)) <= disbot:
                    flag = True
        return flag

    def Run(self, ax, plt):

        # plt.show()
        start_time = time.time()

        start_point = point.Point(self.start.x, self.start.y)
        start_point.cost = 0
        self.open_set.append(start_point)

        while True:
            index = self.SelectPointInOpenList()
            if index < 0:
                print('No path found, algorithm failed!!!')
                return
            p = self.open_set[index]
            rec = Rectangle((p.x, p.y), 1, 1, color='c')
            ax.add_patch(rec)
            # self.SaveImage(plt,self.path)

            if self.IsEndPoint(p):
                # self.BuildPath(p, ax, plt, start_time)
                self.OptimizedPath_v1(p, ax, plt, start_time)
                return

            del self.open_set[index]
            self.close_set.append(p)

            # Process all neighbors
            x = p.x
            y = p.y
            if self.IsValidPoint(x-1, y) and self.IsValidPoint(x, y+1):
                self.ProcessPoint(x - 1, y + 1, p)
            self.ProcessPoint(x - 1, y, p)
            if self.IsValidPoint(x - 1, y) and self.IsValidPoint(x, y - 1):
                self.ProcessPoint(x - 1, y - 1, p)
            self.ProcessPoint(x, y - 1, p)
            if self.IsValidPoint(x + 1, y) and self.IsValidPoint(x, y - 1):
                self.ProcessPoint(x + 1, y - 1, p)
            self.ProcessPoint(x + 1, y, p)
            if self.IsValidPoint(x + 1, y) and self.IsValidPoint(x, y + 1):
                self.ProcessPoint(x + 1, y + 1, p)
            self.ProcessPoint(x, y + 1, p)

    def SaveImage(self, plt, path):
        millis = int(round(time.time() * 1000))
        filename = self.path + str(millis) + '.png'
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        plt.savefig(filename)

    def ProcessPoint(self, x, y, parent):
        if not self.IsValidPoint(x, y):
            return  # Do nothing for invalid point
        p = point.Point(x, y)
        if self.IsInCloseList(p):
            return  # Do nothing for visited point
        if not self.IsInOpenList(p):
            p.parent = parent

            self.open_set.append(p)
        p.cost = self.TotalCost(p)
        print('Process Point [', p.x, ',', p.y, ']', ', cost: ', p.cost)

    def SelectPointInOpenList(self):
        index = 0
        selected_index = -1
        min_cost = sys.maxsize
        for p in self.open_set:
            cost = self.TotalCost(p)
            if cost < min_cost:
                min_cost = cost
                selected_index = index
            index += 1
        return selected_index


    # A*改进算法
    def BuildPath(self, p, ax, plt, start_time):
        path = []
        xs = []
        ys = []
        while True:
            path.insert(0, p)  # Insert first
            if self.IsStartPoint(p):
                break
            else:
                p = p.parent
        for p in path:
            xs.append(p.x+0.5)
            ys.append(p.y+0.5)
            rec = Rectangle((p.x, p.y), 1, 1, color='g')
            ax.add_patch(rec)

            plt.draw()
            # plt.show()
            # self.SaveImage(plt,path)
        # plt.plot(xs, ys, 'o')
        plt.plot(xs, ys, linewidth=1, color='red')
        plt.draw()
        # self.SaveImage(plt,self.path)
        self.shortest_path = path

        plt.show()
        end_time = time.time()
        print('===== Algorithm finish in', int(end_time - start_time), ' seconds')

    # 判断拐点
    def IsTurnpoint(self, point, prepoint, postpoint):
       return not (prepoint.x - postpoint.x) * (point.y - postpoint.y) \
                  == (point.x - postpoint.x) * (prepoint.y - postpoint.y)

    # 路径优化算法
    def OptimizedPath_v1(self, p, ax, plt, start_time):
        path = []
        xs = []
        ys = []
        turnpoint = []
        # turnpoint.insert(0,p)
        # 待简化
        if self.IsStartPoint(p):
            # path = self.path
            # print(path)
            # for pss in path:
            #     xs.append(pss.x + 0.5)
            #     ys.append(pss.y + 0.5)
            #     # print(pss.x,pss.y)
            # plt.plot(xs, ys, linewidth=1, color='red')
            # plt.draw()
            return
        if self.IsStartPoint(p.parent):
            # path = self.path
            # print(path)
            # for pss in path:
            #     xs.append(pss.x + 0.5)
            #     ys.append(pss.y + 0.5)
            #     # print(pss.x,pss.y)
            # plt.plot(xs, ys, linewidth=1, color='red')
            # plt.draw()
            return
        postpoint = p
        point = p.parent
        prepoint = p.parent.parent
        turnpoint.insert(0,postpoint)
        # print(turnpoint)
        while True:
            if self.Distance(postpoint,point) != self.Distance(point,prepoint):
                turnpoint.insert(0,point)
            if self.IsStartPoint(prepoint):
                break
            else:
                postpoint = postpoint.parent
                point = point.parent
                prepoint = prepoint.parent
        turnpoint.insert(0,prepoint)
        turnpoint.reverse()
        # path.insert(0, prepoint)
        if turnpoint == None:
            print("错误：拐点为空！")
            return
        for tp in turnpoint:
            temptp = tp
            if not self.IsPassedObstacle(p,tp,self.map.GetObstaclePoint()):
                if not path.__contains__(tp):
                    path.insert(0,tp)
            else:
                Flag = False
                temp = p
                while True:
                    if temp.x == tp.x and temp.y == tp.y:
                        break
                    else:
                        temp = temp.parent
                        if not self.IsPassedObstacle(temp,p,self.map.GetObstaclePoint()):
                            temptp = temp
                            Flag = True
                if Flag:
                    if not path.__contains__(temptp):
                        path.insert(0,temptp)
            p = temptp
        # plt.plot(xs, ys, 'o')
        # path.insert(0, p)
        # path.remove(path[0])
        if not path.__contains__(tp):
            path.insert(0,tp)

        # print(tp)
        # print(temp)
        # print(temptp)
        print(path)

        self.shortest_path = path

        for pss in path:
            xs.append(pss.x + 0.5)
            ys.append(pss.y + 0.5)
            # print(pss.x,pss.y)
        plt.plot(xs, ys, linewidth=1, color='red')
        plt.draw()
        # self.SaveImage(plt, self.path)

        # millis = int(round(time.time() * 1000))
        # filename = self.path + str(millis) + '.png'
        # if not os.path.exists(self.path):
        #     os.makedirs(self.path)
        # plt.savefig(filename)

        plt.show()

        end_time = time.time()
        print('===== Algorithm finish in', int(end_time - start_time), ' seconds')

    def CalculateDegree(self,p1,p2,initial_degree):
        angle = 0.00
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        if p2.x == p1.x:
            angle = 90.00
            if p2.y == p1.y:
                angle = 0.00
            elif p2.y < p1.y:
                angle = 270.00
        elif p2.y == p1.y:
            angle = 0.00
            if p2.x < p1.x:
                angle = 180.00
        elif p2.x > p1.x and p2.y > p1.y:
            angle = math.atan(dy / dx) / math.pi * 180.00
        elif p2.x > p1.x and p2.y < p1.y:
            angle = (math.pi * 3.00 / 2.00 + math.atan(-dx / dy)) / math.pi * 180.00
        elif p2.x < p1.x and p2.y < p1.y:
            angle = (math.pi + math.atan(dy / dx)) / math.pi * 180.00
        elif p2.x < p1.x and p2.y > p1.y:
            angle = (math.pi / 2.00 + math.atan(dx / -dy)) / math.pi * 180.00
        return int(angle * 100) / 100.00

    def PathForRobot(self,path,initial_degree):
        route = []
        angle = initial_degree
        Flag = False
        tp = None
        for p in path:
            if Flag:
                angle = self.CalculateDegree(tp, p, angle)
                turn_angle = angle - initial_degree
                if turn_angle > 180.00:
                    turn_angle = turn_angle - 360.00
                distance = int(self.Distance(tp, p) * 100) / 100.00
                route.append((turn_angle, distance))
            Flag =True
            tp = p
            initial_degree = angle
        return route
