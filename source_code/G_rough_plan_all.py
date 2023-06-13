import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt

def read_txt(file):    # = open("D:/dotjob/txt/backwall_idx.txt", "r")
    blocks_connect = []
    for line in file.readlines():
        line = line.strip('\n')
        data = [float(i) for i in line.split()]
        blocks_connect.append(data)
    return blocks_connect

def sum_length(blocks_connect):
    connect_length = []
    for i in range(len(blocks_connect)-1):
        p_length = np.sqrt((blocks_connect[i+1][1] - blocks_connect[i][1])**2 +
                           (blocks_connect[i+1][2] - blocks_connect[i][2])**2 +
                           (blocks_connect[i+1][3] - blocks_connect[i][3])**2)
        connect_length.append(p_length)
    blocks_connect_length = sum(connect_length)
    print(blocks_connect_length)
    return None

def view(pcd, blocks_connect0, blocks_connect1, blocks_connect2):
    pcd = np.asarray(pcd.points)
    xlist = []
    ylist = []
    zlist = []
    for i in range(len(pcd)):
        xlist.append(pcd[i][0])
        ylist.append(pcd[i][1])
        zlist.append(pcd[i][2])

    num_connect0 = (len(blocks_connect0))/2 - 1
    num_inner0 = (len(blocks_connect0)) / 2
    num_connect1 = (len(blocks_connect1))/2 - 1
    num_inner1 = (len(blocks_connect1)) / 2
    num_connect2 = (len(blocks_connect2))/2 - 1
    num_inner2 = (len(blocks_connect2)) / 2

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")
    for i in range(int(num_connect0)):
        ax1.plot3D([blocks_connect0[2*i+1][1], blocks_connect0[2*i+2][1]], [blocks_connect0[2*i+1][2], blocks_connect0[2*i+2][2]],
                   [blocks_connect0[2*i+1][3], blocks_connect0[2*i+2][3]], color='r')

    for i in range(int(num_inner0)):
        ax1.plot3D([blocks_connect0[2*i][1], blocks_connect0[2*i+1][1]], [blocks_connect0[2*i][2], blocks_connect0[2*i+1][2]],
                   [blocks_connect0[2*i][3], blocks_connect0[2*i+1][3]], color='b')

    for i in range(int(num_connect1)):
        ax1.plot3D([blocks_connect1[2*i+1][1], blocks_connect1[2*i+2][1]], [blocks_connect1[2*i+1][2], blocks_connect1[2*i+2][2]],
                   [blocks_connect1[2*i+1][3], blocks_connect1[2*i+2][3]], color='r')

    for i in range(int(num_inner1)):
        ax1.plot3D([blocks_connect1[2*i][1], blocks_connect1[2*i+1][1]], [blocks_connect1[2*i][2], blocks_connect1[2*i+1][2]],
                   [blocks_connect1[2*i][3], blocks_connect1[2*i+1][3]], color='b')

    for i in range(int(num_connect2)):
        ax1.plot3D([blocks_connect2[2*i+1][1], blocks_connect2[2*i+2][1]], [blocks_connect2[2*i+1][2], blocks_connect2[2*i+2][2]],
                   [blocks_connect2[2*i+1][3], blocks_connect2[2*i+2][3]], color='r')

    for i in range(int(num_inner2)):
        ax1.plot3D([blocks_connect2[2*i][1], blocks_connect2[2*i+1][1]], [blocks_connect2[2*i][2], blocks_connect2[2*i+1][2]],
                   [blocks_connect2[2*i][3], blocks_connect2[2*i+1][3]], color='b')

    ax1.scatter(xlist, ylist, zlist, color='gray', marker='.')  # xlist, ylist, zlist
    plt.show()
    return None

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud("D:\项目_py编译器\Lost_polyhedron\db/pcd/section2.2 - Cloud_pcd.pcd")
    blocks_connect0 = read_txt(open("D:\项目_py编译器\Lost_polyhedron\db\敏感性分析/0.4_45/收敛链表_0.txt", "r"))
    blocks_connect1 = read_txt(open("D:\项目_py编译器\Lost_polyhedron\db\敏感性分析/0.4_45/收敛链表_1.txt", "r"))
    blocks_connect2 = read_txt(open("D:\项目_py编译器\Lost_polyhedron\db\敏感性分析/0.4_45/收敛链表_2.txt", "r"))
    sum_length(blocks_connect0)
    sum_length(blocks_connect1)
    sum_length(blocks_connect2)
    view(pcd, blocks_connect0, blocks_connect1, blocks_connect2)
