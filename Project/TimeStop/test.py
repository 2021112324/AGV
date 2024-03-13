from TimeStop.TimeStopAlgorithm import TimeStopAlgorithm
from TimeStop.robot import Robot

map = [[0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0],
       [0,0,0,0,0,0,0,0,0,0]]

TSA = TimeStopAlgorithm()
TSA.UpdateMap(map)
robot1 = Robot(1,4,4,45.00,False)
robot2 = Robot(2,5,4,135.00,False)
TSA.UpdateRobot(robot1)
TSA.UpdateRobot(robot2)
# TSA.DeleteRobot(robot1)
print(TSA.robots)
# TSA.ShowMap()
# print(TSA.CalculateDegree(robot1,robot2))
TSA.EvasionAlgorithm(robot1)
print(robot1)