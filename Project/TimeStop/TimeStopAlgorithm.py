import math

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle

from EvasionAlgorithm.EAMap import EAMap


class TimeStopAlgorithm:
    def __init__(self):
        self.map = None
        self.robots = []
        self.min_distance = 30
        self.robot_size = 3

    def UpdateMap(self, map):
        if self.map == None:
            print("生成新地图")
        else:
            print("地图更新")
        self.map = EAMap()
        self.map.GenerateMap(map)
        return

    # def ShowMap(self,pause=True,pause_time=1):
    #     if self.map == None:
    #         return
    #     l = 0.3
    #     x = np.array(range(self.map.width))
    #     y = np.array(range(self.map.height))
    #     a = plt.figure(figsize=(self.map.width*l,self.map.height*l))
    #     mngr = plt.get_current_fig_manager()
    #     mngr.window.wm_geometry("+380+310")
    #     if pause == False:
    #         plt.ion()
    #     plt.xticks(x)
    #     plt.yticks(y)
    #     plt.grid(linestyle='-')
    #     for i in range(self.map.width):
    #         for j in range(self.map.height):
    #             if self.map.IsObstacle(i, j):
    #                 rec = Rectangle((i - 0.5, j - 0.5), width=1, height=1, color='black')
    #                 plt.gca().add_patch(rec)
    #     for i in self.robots:
    #         x = i.point.x
    #         y = i.point.y
    #         draw_circle = plt.Circle((x, y), 0.2)
    #         plt.gcf().gca().add_artist(draw_circle)
    #     if pause == False:
    #         plt.pause(pause_time)
    #         plt.ioff()
    #         plt.close()
    #     plt.show()

    def ShowMap(self,pause=True,pause_time=0.1):
        if self.map == None:
            return
        plt.cla()
        plt.xlim((0,self.map.width))
        plt.ylim((0,self.map.height))
        plt.grid(linestyle='-')
        for i in range(self.map.width):
            for j in range(self.map.height):
                if self.map.IsObstacle(i, j):
                    rec = Rectangle((i - 0.5, j - 0.5), width=1, height=1, color='black')
                    plt.gca().add_patch(rec)
        for i in self.robots:
            x = i.point.x
            y = i.point.y
            draw_circle = plt.Circle((x, y), self.robot_size)
            plt.gcf().gca().add_artist(draw_circle)
        if pause == False:
            plt.pause(pause_time)
            return
        plt.show()

    def UpdateRobot(self, robot):
        for i in self.robots:
            if i.ID == robot.ID:
                i.Update(robot)
                return
        self.robots.append(robot)
        return

    def DeleteRobot(self,robot):
        for i in self.robots:
            if i.ID == robot.ID:
                self.robots.remove(i)
                return
        print("未找到该机器人，删除机器人失败！")
        return None

    def Distance(self,robot1,robot2):
        p1 = robot1.point
        p2 = robot2.point
        return np.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

    # 计算以robot_vertex为顶点，以robot_vertex和robot_edge连线为一边顺时针旋转到以robot_vertex的方向为一边所形成的角
    def CalculateDegree(self,robot_vertex,robot_edge):
        p1 = robot_vertex.point
        p2 = robot_edge.point
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
        # print(angle)
        included_angle = robot_vertex.degree - angle
        if included_angle < 0:
            included_angle = included_angle + 360.00
        return int(included_angle * 100) / 100.00

    def IsPaused(self,robot):
        return robot.pause

    # 基本思想，当距离过近时，自己暂停，别人先走
    # 该算法似乎不能解决两个机器人相向问题
    def EvasionAlgorithm(self,robot):
        Flag = False                                    # 判断是否因规避算法而暂停
        temprobot = None
        for i in self.robots:
            # 当两者距离过近，且都处于运动状态且运动方向相交，则可能相撞
            if i.ID == robot.ID:
                temprobot = i
                continue
            if self.Distance(robot,i) < self.min_distance:
                robot_included_angle = self.CalculateDegree(robot,i)
                i_included_angle = self.CalculateDegree(i,robot)
                if i.pause == False and abs(robot_included_angle - i_included_angle) > 180.00:
                    Flag =True
        if Flag:
            robot.pause = True
            if temprobot != None:
                temprobot.pause = True
        else:
            robot.pause = False
            if temprobot != None:
                temprobot.pause = False






