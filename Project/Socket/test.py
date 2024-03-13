# import re
# import string
#
# from TimeStop.TimeStopAlgorithm import TimeStopAlgorithm
# from TimeStop.robot import Robot
#
# # a = "{taskID=11,start=1,end=11,path=[]}"
# #
# # ab = re.findall("taskID=(\d+)", a)
# #
# # print(ab)
# map = []
# with open("TestMap", "r", encoding='UTF-8')as f:
#     res = f.readlines()
#     for i in res:
#         line = []
#         a = re.findall("(0|1)",i)
#         for j in a:
#             line.append(int(j))
#         map.append(line)
# print(map)
# TSA = TimeStopAlgorithm()
# TSA.UpdateMap(map)
# robot1 = Robot(1,1,1,45.00,False)
# robot2 = Robot(2,1,2,90.00,False)
# TSA.UpdateRobot(robot1)
# TSA.UpdateRobot(robot2)
# TSA.ShowMap(pause=False)
# TSA.ShowMap(pause=False)
# TSA.ShowMap(pause=False)
# # TSA.DeleteRobot(robot1)
# print(TSA.robots)

with open('F:\WebComp\Project\Socket\TestMap2', 'ab') as f:
    # 写入文件
    for i in range(100):
        for j in range(100):
            f.write(b"0 ")
        f.write(b"\n")
    # 接受完成标志
