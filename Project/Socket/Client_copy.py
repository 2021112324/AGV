import socket

from TimeStop.robot import Robot

# 服务端为TCP方式，客户端也采用TCP方式，默认参数即为TCP
client = socket.socket()
# 访问服务器的IP和端口
ip_port = ('127.0.0.1', 8888)
# 连接主机
client.connect(ip_port)
#
while True:
    # 接收主机信息 每次接收缓冲区1024个字节
    data = client.recv(1024)
    data = data.decode()
    # 打印接收数据
    print(data)
    if data == "updated_map":
        print("地图更新成功")
    elif data == "updated_robot":
        print("机器人信息更新成功")
    msg_input = input("发送文件(1)、发送坐标(2)或结束通讯(bye)：")
    if msg_input == 'bye':
        client.send('bye'.encode())
        break
    elif msg_input == '1':
        client.send('map'.encode())
        with open('F:\WebComp\Project\Socket\TestMap', 'rb') as f:
            # 按每一段分割文件上传
            for i in f:
                client.send(i)
                data = client.recv(1024)
                # 判断是否真正接收完成
                if data != b'success':
                    break
        client.send('success'.encode())
    elif msg_input == '2':
        client.send('ori'.encode())
        x = int(input("x:"))
        y = int(input("y:"))
        robot = Robot(2,x,y,135.00,True)
        client.send(str(robot).encode())

