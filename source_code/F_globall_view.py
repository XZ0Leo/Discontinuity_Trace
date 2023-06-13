import numpy as np
import matplotlib.pyplot as plt
import open3d as o3d

def main_line(mainline_num = 3):
    mainline_file = []

    for i in range(mainline_num):

        line_detail = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/主路径细节链表_%s.txt"%(i))
        line_detail = [list(n) for n in line_detail]
        mainline_file.append(list(line_detail))


    return mainline_file

def cobweb(cobweb_num = 14):
    first_point_line = []
    last_point_line = []

    for i in range(cobweb_num):
        cobweb_undirected = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/生成树无向图%s.txt" % (i))
        cobweb_waypoint = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/路点%s.txt" % (i))
        for i_row in range(len(cobweb_undirected)):
            for i_column in range(len(cobweb_undirected)):
                if i_row < i_column and cobweb_undirected[i_row][i_column]:
                    first_point_line.append(list(cobweb_waypoint[i_row]))
                    last_point_line.append(list(cobweb_waypoint[i_column]))

    return first_point_line,last_point_line

def view_global(pcd,mainline_file,first_point_line,last_point_line):
    pcd = np.asarray(pcd.points)
    xlist = []
    ylist = []
    zlist = []
    for i in range(len(pcd)):
        xlist.append(pcd[i][0])
        ylist.append(pcd[i][1])
        zlist.append(pcd[i][2])



    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")

    for i in range(len(first_point_line)):

        ax1.plot3D([first_point_line[i][0], last_point_line[i][0]],
                   [first_point_line[i][1], last_point_line[i][1]],
                   [first_point_line[i][2], last_point_line[i][2]], color='b')

    for i in range(len(mainline_file)):
        num_connect = (len(mainline_file[i])) - 1
        for i_connect in range(int(num_connect)):
            ax1.plot3D([mainline_file[i][i_connect][0], mainline_file[i][i_connect + 1][0]],
                       [mainline_file[i][i_connect][1], mainline_file[i][i_connect + 1][1]],
                       [mainline_file[i][i_connect][2], mainline_file[i][i_connect + 1][2]], color='r')



    ax1.scatter(xlist, ylist, zlist, color='gray', marker='.')  # xlist, ylist, zlist
    plt.show()

    return None


if __name__ == '__main__':
    # 主路径细节链表 文件数目
    mainline_num = 3
    # 生成树无向图 文件数目
    cobweb_num = 14
    mainline_file = main_line(mainline_num)
    first_point_line,last_point_line = cobweb(cobweb_num)
    print(mainline_file)
    print(first_point_line)
    print(last_point_line)

    pcd = o3d.io.read_point_cloud("D:\项目_py编译器\Lost_polyhedron\db/pcd/section2.2 - Cloud_pcd.pcd")
    view_global(pcd,mainline_file,first_point_line,last_point_line)