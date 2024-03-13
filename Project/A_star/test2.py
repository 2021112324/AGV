# from A_star.robot import Robot
#
# a = Robot(1,0,0,0.00)
# print(a)

from EvasionAlgorithm.EAMap import EAMap

#
# a = "{robotID=1,position=(0,1),degree=0.00,pause=True}"
# RobotIDRegular = "robotID=" + "(\d+)"
# RobotPositionRegular = "position=" + "\(" + "(\d+)" + "," + "(\d+)" + "\)"
# RobotDegreeRegular = "degree=" + "(\d+.\d+)"
# RobotPauseRegular = "pause=" + "(False|True)"
# RobotID = re.findall(RobotIDRegular, a)
# Position = re.findall(RobotPositionRegular, a)
# Degree = re.findall(RobotDegreeRegular, a)
# Pause = re.findall(RobotPauseRegular,a)
# print(RobotID)
# print(Position[0].__len__())
# print(Degree)
# print(Pause[0])

# Map = [[0,0,0,0,0,0],
#        [0,0,0,1,1,0],
#        [0,0,0,0,0,0],
#        [0,0,0,0,0,0]]
# a = EAMap()
# a.GenerateMap(Map)
# print(a.width)
# a = EAMap()
# print(a.width)
# a.ShowMap()

# print(Map.__len__())
# print(Map[0].__len__())
import matplotlib.pyplot as plt
import numpy as np
import time
# from sklearn.cluster import KMeans
# from sklearn import datasets
from sklearn.datasets import load_iris


# 随机取得中心点
def rand_center(data, k):
    np.random.seed(2)
    data_rand = np.random.randint(0, 150, size=k)
    return (data[data_rand])


# 计算点到中心的距离,在分类中使用
def point_cent_distan(point, cent):
    dis = np.square(point[0] - cent[0]) + np.square((point[1] - cent[1]))
    return (dis)


# 判断属于哪一个中点的类,k指类数；label_data存储不同类的数据
def belong_cluster(data, center, k):
    label_data = [[] for i in range(k)]

    for i in range(data.shape[0]):
        mini_distan = point_cent_distan(data[i], center[0])
        label_value = 0
        for j in range(1, k):
            mini_distan_coach = point_cent_distan(data[i], center[j])
            if mini_distan_coach < mini_distan:
                label_value = j
                mini_distan = mini_distan_coach
        label_data[label_value].append(data[i])
    return (label_data)


# 修改一个类的中心点,类内的数据data，k表示组数
def change_one_center(data):
    total = [0, 0]
    one_cent = []
    for i in range(len(data)):
        total[0] = total[0] + data[i][0]
        total[1] = total[1] + data[i][1]
    one_cent = [total[0] / len(data), total[1] / len(data)]
    return (one_cent)


def change_all_center(data, k):
    cent = []
    for i in range(k):
        cent.append(change_one_center(data[i]))
    return (cent)


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

iris = load_iris()
X = iris.data[:, 2:4]  ##表示我们只取特征空间中的后两个维度
# 随机初始的中心点
ini_center = rand_center(X, 3)
# 对中心点分类
cluster = belong_cluster(X, ini_center, 3)

plt.ion()  # 使得plt.show()显示后不暂停，交互模式，可以使用plt.ioff()停止

for i in range(20):
    plt.clf()
    center = change_all_center(cluster, 3)
    center = np.array(center)
    c0 = cluster[0]
    c1 = cluster[1]
    c2 = cluster[2]
    # c0=[list(i) for i in c0]
    c0 = np.array(c0)
    c1 = np.array(c1)
    c2 = np.array(c2)

    plt.scatter(c0[:, 0], c0[:, 1], c="red", marker='o', label='label0')
    plt.scatter(c1[:, 0], c1[:, 1], c="green", marker='*', label='label1')
    plt.scatter(c2[:, 0], c2[:, 1], c="blue", marker='+', label='label2')
    plt.scatter(center[:, 0], center[:, 1], c="m", marker='+', label='center', s=300)
    plt.xlabel('sepal length')
    plt.ylabel('sepal width')

    plt.title('第' + str(i + 1) + "次迭代", loc='center')
    plt.legend(loc=2)

    plt.pause(0.5)
    if i == 19:
        plt.ioff()
    plt.show()
    cluster = belong_cluster(X, center, 3)







