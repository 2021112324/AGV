import re

RobotIDRegular = "robotID=" + "(\d+)"
RobotPositionRegular = "position=" + "\(" + "(\d+)" + ",\s*" + "(\d+)" + "\)"
RobotDegreeRegular = "degree=" + "(\d+.\d+)"
RobotPauseRegular = "pause=" + "(False|True)"

class GetData:
    def __init__(self):
        return
    def GetRobotID(self,data):
        RobotID = re.findall(RobotIDRegular, data)
        if RobotID.__len__() != 1:
            print("数据有误！")
            return None
        return RobotID[0]

    def GetPosition(self,data):
        Position = re.findall(RobotPositionRegular, data)
        if Position.__len__() != 1:
            print("数据有误！")
            return None,None
        elif Position[0].__len__() != 2:
            print("数据有误！")
            return None,None
        return Position[0][0],Position[0][1]

    def GetDegree(self,data):
        Degree = re.findall(RobotDegreeRegular, data)
        if Degree.__len__() != 1:
            print("数据有误！")
            return None
        return Degree[0]

    def GetPause(self,data):
        Pause = re.findall(RobotPauseRegular, data)
        if Pause.__len__() != 1:
            print("数据有误！")
            return None
        return Pause[0]