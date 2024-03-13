import multiprocessing
import re
import socketserver
import time
from concurrent.futures import thread

import matplotlib.pyplot as plt

from EvasionAlgorithm.EATimeStop import EATimeStop
from TimeStop.robot import Robot
from RegularExpression import GetData

EvasionAlgorithm = EATimeStop()
ShowMapFlag = False

class Server(socketserver.BaseRequestHandler):

    def setup(self):
        pass

    def handle(self):
        global ShowMapFlag
        # 定义连接变量
        conn = self.request
        print("接收到来自" + str(self.client_address) + "的连接。")
        msg = "成功连接！"
        # 发送消息
        conn.send(msg.encode())
        # 进入循环，不断接收客户端消息
        while True:
            data = conn.recv(1024)
            if data == b'map':
                map_file = 'F:\WebComp\Project\map\\' + str(int(round(time.time()))) + '.map'
                while True:
                    data = conn.recv(1024)
                    if data == b'success':
                        print("文件接收完成")
                        break
                    with open(map_file, 'ab') as f:
                        # 写入文件
                        f.write(data)
                        # 接受完成标志
                        conn.send('success'.encode())
                # 生成地图
                map = []
                with open("TestMap2", "r", encoding='UTF-8')as f:
                    res = f.readlines()
                    for i in res:
                        line = []
                        a = re.findall("(0|1)", i)
                        for j in a:
                            line.append(int(j))
                        map.append(line)
                EvasionAlgorithm.UpdateMap(map)
                # EvasionAlgorithm.method.ShowMap()
                conn.send('updated_map'.encode())



            elif data == b'ori':
                data = conn.recv(1024)
                data = data.decode()
                # print(data)
                RobotID = GetData().GetRobotID(data)
                Position_x,Position_y = GetData().GetPosition(data)
                Degree = GetData().GetDegree(data)
                Pause = GetData().GetPause(data)
                if RobotID == None or Position_x == None or Position_y == None or Degree == None or Pause == None:
                    conn.send('failed'.encode())
                else:
                    RobotID = int(RobotID)
                    Position_x = int(Position_x)
                    Position_y = int(Position_y)
                    Degree = float(Degree)
                    if Pause == 'False':
                        robot = Robot(RobotID,Position_x,Position_y,Degree, False)
                    elif Pause == 'True':
                        robot = Robot(RobotID, Position_x, Position_y, Degree, True)
                    print(EvasionAlgorithm.method.robots)
                    EvasionAlgorithm.UpdateRobot(robot)

                    EvasionAlgorithm.EvasionAlgorithm(robot)
                    print(robot)
                    conn.send(str(robot.pause).encode())
                    # EvasionAlgorithm.method.ShowMap(pause=False)
            elif data == b'ori_finished':
                print("机器人完成任务")
                conn.send('ori_finished'.encode())


            elif data == b'bye':
                print("断开连接")
                break

            elif data == b'show_map':
                if ShowMapFlag == False:
                    ShowMapFlag = True
                else:
                    return
                print("展示地图")
                while(ShowMapFlag):
                    EvasionAlgorithm.method.ShowMap(pause=False)
                plt.show()
            elif data == b'close_map':
                # global ShowMapFlag
                ShowMapFlag = False

        # 关闭连接
        conn.close()

    def finish(self):
        pass

def ShowMap():
    while(True):
        EvasionAlgorithm.method.ShowMap(pause=False)

if __name__ == "__main__":
    # 提示信息
    print("正在等待接收数据。。。。。。")
    # 创建多线程实例
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 8888), Server)
    # 开启多线程，等待连接
    server.serve_forever()



# # 定义连接的ip和port
# ip_port = ('127.0.0.1', 9999)
# # 绑定端口
# sk.bind(ip_port)
# # 最大连接数
# sk.listen(5)
# # 进入循环接收数据
# conn, address = sk.accept()
# print("文件接收开始")
