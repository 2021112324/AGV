import socket

from TimeStop.robot import Robot

# 服务端为TCP方式，客户端也采用TCP方式，默认参数即为TCP
client = socket.socket()
# 访问服务器的IP和端口
ip_port = ('127.0.0.1', 8888)
# 连接主机
client.connect(ip_port)


data = client.recv(1024)
data = data.decode()
print(data)
msg_input = input("开启Map(1)，关闭Map(2)：")
if msg_input == '1':
    client.send('show_map'.encode())
elif msg_input == '2':
    client.send('close_map'.encode())

