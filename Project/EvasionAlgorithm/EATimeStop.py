from EvasionAlgorithm.EA_Interface import EA_Interface
from TimeStop.TimeStopAlgorithm import TimeStopAlgorithm


class EATimeStop(EA_Interface):
    def __init__(self):
        self.method = TimeStopAlgorithm()

    def UpdateMap(self, map):
        self.method.UpdateMap(map)

    def UpdateRobot(self, robot):
        self.method.UpdateRobot(robot)

    def DeleteRobot(self,robot):
        self.method.DeleteRobot(robot)

    def EvasionAlgorithm(self, robot):
        self.method.EvasionAlgorithm(robot)
