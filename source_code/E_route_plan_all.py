import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import method.read_save


def inner_route_iteration(last_point_num,undirected,iterationed,line_file):

    print("可能路径集合首", line_file)
    # 找到最后一颗点的连接列表，当1的个数等于1且坐标不属于已记录点时，添加1所属的坐标到line_file[i]
    # 当1的个数大于1且坐标不属于已记录点时，复制个数-1个line_file[i]，添加首个1所属的坐标到line_file[i]，其余的1所属的坐标到复制的line_file[i]并添加到line_file
    for i in range(len(line_file)):
        # print(i)
        # 提取第i行无向图
        list_i = undirected[line_file[i][-1]]
        print("当前行的行数，无向图",line_file[i][-1],list_i)
        print("本次查询的对照列表",iterationed)
        print("当前行的无向图路径数目", sum(list_i))
        if sum(list_i) == 1 :
            for i_list_i in range(len(list_i)):
                if list_i[i_list_i] == 1 and i_list_i not in iterationed:
                    line_file[i].append(i_list_i)
        iterationed.append(line_file[i][-1])

        if sum(list_i) > 1 :
            for i_list_i in range(len(list_i)):
                if i_list_i in iterationed:
                    list_i[i_list_i] = 0
            print("去除对照列表的坐标的当前行的无向图",list_i)

            # 创建剩余1的坐标列表
            idx = []
            for i_list_delet in range(len(list_i)):
                if list_i[i_list_delet] == 1:
                    idx.append(i_list_delet)

            copy_line = []
            for i_copy_line in range(len(line_file[i])):
                copy_line.append(line_file[i][i_copy_line])

            for i_list_idx in range(len(idx)):

                if i_list_idx == 0:
                    line_file[i].append(idx[i_list_idx])

                    print("路径集合首行路径",line_file[i_list_idx])
                elif 0 < i_list_idx < len(idx):
                    print(i_list_idx)
                    # 复制此轮迭代提示表
                    copy = copy_line + [idx[i_list_idx]]
                    line_file.append(copy)
                elif i_list_idx == len(idx):
                    copy = copy_line + [idx[i_list_idx]]
                    line_file.append(copy)
                    print("行数,路径集合尾行路径", i_list_idx,line_file[i_list_idx])
                    iterationed.append(line_file[i][-1])

    print("可能路径集合尾",line_file)
    # 迭代收敛列表
    convergence = []
    for i in range(len(line_file)):
        convergence.append(line_file[i][-1])

    if last_point_num in convergence:
        return line_file
    if last_point_num not in convergence:
        return inner_route_iteration(last_point_num,undirected,iterationed,line_file)




def way_detail_fun(connectlist):
    cluster_num = int(len(connectlist)/2)
    way_detail_point = []
    for i in range(cluster_num):

        cluster_num = int(connectlist[i*2][0])
        first_point = [connectlist[i*2][1], connectlist[i*2][2], connectlist[i*2][3]]
        print(first_point)
        last_point = [connectlist[i*2 + 1][1], connectlist[i*2 + 1][2], connectlist[i*2 + 1][3]]
        print(last_point)

        undirected = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/生成树无向图%s.txt"%(cluster_num))
        waypoint = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/路点%s.txt"%(cluster_num))
        first_point_num = 0
        last_point_num = 0
        for i_waypoint in range(len(waypoint)):
            if [waypoint[i_waypoint][0],waypoint[i_waypoint][1], waypoint[i_waypoint][2]] == first_point:
                first_point_num = i_waypoint
            if [waypoint[i_waypoint][0],waypoint[i_waypoint][1], waypoint[i_waypoint][2]] == last_point:
                last_point_num = i_waypoint

        # 迭代提示列表
        iterationed = []
        iterationed.append(first_point_num)

        # 当前查询获得列表
        line_file = []
        line_file.append([first_point_num])
        line_convergence_file = inner_route_iteration(last_point_num, undirected,iterationed,line_file)

        # 抽取符合首尾端点的链表
        first_line_last = []
        for i_convergence in range(len(line_convergence_file)):
            if line_convergence_file[i_convergence][-1] == last_point_num:
                first_line_last = line_convergence_file[i_convergence]

        # 按照链表计点
        for i_first_line_last in range(len(first_line_last)):
            way_detail_point.append(list(waypoint[first_line_last[i_first_line_last ]]))
    return way_detail_point

def view(pcd,way_detail_point):

    pcd = np.asarray(pcd.points)
    xlist = []
    ylist = []
    zlist = []
    for i in range(len(pcd)):
        xlist.append(pcd[i][0])
        ylist.append(pcd[i][1])
        zlist.append(pcd[i][2])

    num_connect = (len(way_detail_point)) - 1


    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")
    for i in range(int(num_connect)):
        ax1.plot3D([way_detail_point[i][0], way_detail_point[i + 1][0]],
                   [way_detail_point[i][1], way_detail_point[i + 1][1]],
                   [way_detail_point[i][2], way_detail_point[i + 1][2]], color='r')



    ax1.scatter(xlist, ylist, zlist, color='gray', marker='.')  # xlist, ylist, zlist
    plt.show()
    return None

def save(way_detail_point,filename, savepath):

    xlist = []
    ylist = []
    zlist = []
    for i in range(len(way_detail_point)):

        xlist.append(way_detail_point[i][0])
        ylist.append(way_detail_point[i][1])
        zlist.append(way_detail_point[i][2])
    method.read_save.save_txt3(xlist, ylist, zlist, filename, savepath)
    return None

if __name__ == '__main__':
    connectlist = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/收敛链表_2.txt")
    pcd = o3d.io.read_point_cloud("D:\项目_py编译器\Lost_polyhedron\db/pcd/section2.2 - Cloud_pcd.pcd")
    way_detail_point = way_detail_fun(connectlist)
    print(way_detail_point)

    view(pcd,way_detail_point)

    # 使用此函数时记得更改链表名称
    # save(way_detail_point, filename="主路径细节链表_2",savepath="D:\项目_py编译器\Lost_polyhedron\db/txt/")