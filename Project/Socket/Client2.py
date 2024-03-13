import socket
import time

from TimeStop.robot import Robot

# 服务端为TCP方式，客户端也采用TCP方式，默认参数即为TCP
client = socket.socket()
# 访问服务器的IP和端口
ip_port = ('127.0.0.1', 8888)
# 连接主机
client.connect(ip_port)
x = 99
y = 0
robot = Robot(2, x, y, 135.00, False)

#
while True:
    # 接收主机信息 每次接收缓冲区1024个字节
    data = client.recv(1024)
    data = data.decode()
    # 打印接收数据
    print(data)
    if data == "updated_map":
        print("地图更新成功")
    elif data == "ori_finished":
        print("机器人完成任务")

    msg_input = input("发送文件(1)、发送坐标(2)或结束通讯(bye)：")
    if msg_input == 'bye':
        client.send('bye'.encode())
        break
    elif msg_input == '1':
        client.send('map'.encode())
        with open('F:\WebComp\Project\Socket\TestMap2', 'rb') as f:
            # 按每一段分割文件上传
            for i in f:
                client.send(i)
                data = client.recv(1024)
                # 判断是否真正接收完成
                if data != b'success':
                    break
        client.send('success'.encode())
    elif msg_input == '2':
        flag = False
        while(True):
            time.sleep(0.2)
            if y == 100:
                break
            client.send('ori'.encode())
            client.send(str(robot).encode())
            data = client.recv(1024)
            data = str(data.decode())
            print(data)
            if data == 'True':
                robot.pause = True
            elif data == 'False':
                robot.pause = False
            if robot.pause == False:
                x = x - 1
                y = y + 1
                robot.UpdateLocation(x,y)
        client.send('ori_finished'.encode())


