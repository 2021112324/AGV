from TimeStop.point import Point


class Robot:
    def __init__(self,ID,x,y,degree,pause):
        self.ID = ID
        self.point = Point(x, y)
        self.degree = degree
        self.pause = pause

    # def __str__(self):
    #     return "{robotID=" + str(self.ID) + ",position=" + str(self.point) + \
    #         ",degree=" + str(self.degree) + ",pause=" + str(self.pause) + "}"

    def __repr__(self):
        return "{robotID=" + str(self.ID) + ",position=" + str(self.point) +\
            ",degree=" + str(self.degree) + ",pause=" + str(self.pause) + "}"
        return str([self.ID, self.Point, self.degree])

    def Update(self,robot):
        self.point = robot.point
        self.degree = robot.degree
        self.pause = robot.pause
        return

    def UpdateLocation(self,x,y):
        self.point.x = x
        self.point.y = y