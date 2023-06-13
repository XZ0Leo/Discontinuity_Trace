import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import method.read_save

def base_connectlist(orient_first,orient_last,pcd,root_prompt):
    '''
    基础连接列表
    :param orient_first:
    :param orient_last:
    :param pcd:
    :param root_prompt:
    :return:
    '''
    base_first = []
    base_last = []
    for i in range(len(root_prompt)):
        if list(np.asarray(pcd.points[i])) == orient_first:
            base_first = [root_prompt[i][0],orient_first[0],orient_first[1],orient_first[2]]
        if list(np.asarray(pcd.points[i])) == orient_last:
            base_last = [root_prompt[i][0],orient_last[0],orient_last[1],orient_last[2]]
    connectlist = [base_first,base_last]
    return connectlist

def cluster_connect_iteration(connectlist,pcd,pcd_tree,root_prompt,iterationed,search_radius,shrink_angle):

    vector = [connectlist[1][1] - connectlist[0][1], connectlist[1][2] - connectlist[0][2],connectlist[1][3] - connectlist[0][3]]
    # 已查询组列表，结束列表
    print("当前向量",vector)
    print("当前链表",connectlist)



    # 找到查询范围内的初始端点
    for i in range(len(pcd.points)):
        # print(i)
        if list(np.asarray(pcd.points[i])) == [connectlist[-1][1],connectlist[-1][2],connectlist[-1][3]]:
            print("此次迭代列表尾点",list(np.asarray(pcd.points[i])))
            iterationed.append(connectlist[-1][0])
            print("当前对照提示符", iterationed)

            [k1, idx1, _] = pcd_tree.search_radius_vector_3d(pcd.points[i],search_radius)


            # 若此次查找idx对应组有不在iterationed内的点，则继续并最后迭代，若所有组都在iterationed内直接返回connectlist
            couple_idx = []
            for idx in idx1:
                couple_idx.append(root_prompt[idx][0])
            print("此次尾点查询点所属组", couple_idx)
            idx_in_iterationed = [False for element in couple_idx if element not in iterationed]
            if not idx_in_iterationed:
                return connectlist
            else:



                connectlist_pre = []
                for idx in idx1:
                    # 找到一个没成型的端点
                    if root_prompt[idx][0] not in iterationed:
                        print("细分组端点所属", root_prompt[idx][0])

                        # 由此端点找到组与组内其他点
                        cluster_num = root_prompt[idx][0]
                        base_point = list(np.asarray(pcd.points[idx]))
                        compare_pointlist = []
                        for i_compare in range(len(pcd.points)):
                            if root_prompt[i_compare][0] == cluster_num and i_compare != idx:
                                compare_pointlist.append(list(pcd.points[i_compare]))

                        print("对象端点",base_point)
                        print("对象端点组内点",compare_pointlist)

                        # 长度，夹角对照
                        angle_compare = []
                        lenth_compare = []
                        for i_pointlist in range(len(compare_pointlist)):
                            a = np.array([compare_pointlist[i_pointlist][0] - base_point[0],compare_pointlist[i_pointlist][1] - base_point[1],compare_pointlist[i_pointlist][2] - base_point[2]])
                            b = np.array(vector)

                            a_norm = np.sqrt(np.sum(a * a))
                            b_norm = np.sqrt(np.sum(b * b))
                            cos_value = np.dot(a, b) / (a_norm * b_norm)
                            arc_value = np.arccos(cos_value)
                            angle_value = arc_value * 180 / np.pi
                            angle_compare.append(angle_value)


                            base_point_ass = np.array(base_point)
                            compare_pointlist_ass = np.array(compare_pointlist[i_pointlist])
                            distance = np.sqrt(np.sum(np.square(compare_pointlist_ass - base_point_ass)))
                            lenth_compare.append(distance)

                        print("对象端点各组内点夹角",angle_compare)
                        print("对象端点各组内点长度",lenth_compare)

                        # 夹角收缩
                        lenth_select = []
                        for i_angle in range(len(angle_compare)):
                            if angle_compare[i_angle] <= shrink_angle:
                                lenth_select.append(lenth_compare[i_angle])
                            if angle_compare[i_angle] > shrink_angle:
                                lenth_select.append(0)



                        # 分组比较connectlist_pre：组类，长度，起点，终点
                        end_point = []
                        start_point = base_point

                        print("对象端点各组内点收缩长度筛选", lenth_select)
                        for i_lenth in range(len(lenth_compare)):
                            if lenth_compare[i_lenth] == max(lenth_select):
                                end_point = compare_pointlist[i_lenth]
                        connectlist_pre_element = [cluster_num,max(lenth_select),start_point,end_point]
                        connectlist_pre.append(connectlist_pre_element)
                        print("本轮查找所有最大路径统计", connectlist_pre)

                # 此次查找时所有的其他组的点找到最大距离的首尾两点

                select_base = []
                for i_connectlist in range(len(connectlist_pre)):
                    select_base.append(connectlist_pre[i_connectlist][1])

                    print("nnn",connectlist_pre[i_connectlist][1])
                print("ppp",select_base)

                if sum(select_base) == 0:
                    return connectlist

                else:

                    for i_select_base in range(len(select_base)):
                        if connectlist_pre[i_select_base][1] == max(select_base):
                            connectlist.append([connectlist_pre[i_select_base][0],connectlist_pre[i_select_base][2][0],connectlist_pre[i_select_base][2][1],connectlist_pre[i_select_base][2][2]])
                            connectlist.append([connectlist_pre[i_select_base][0],connectlist_pre[i_select_base][3][0],connectlist_pre[i_select_base][3][1],connectlist_pre[i_select_base][3][2]])
                    print("当前输出链表",connectlist)
                    return cluster_connect_iteration(connectlist, pcd, pcd_tree, root_prompt, iterationed,search_radius,shrink_angle)



def cluster_connect(connectlist,pcd,pcd_tree,root_prompt,search_radius,shrink_angle):
    iterationed = []


    # 块连接路径
    blocks_connect = cluster_connect_iteration(connectlist,pcd,pcd_tree,root_prompt,iterationed,search_radius,shrink_angle)

    return blocks_connect

def view(pcd, blocks_connect):
    pcd = np.asarray(pcd.points)
    xlist = []
    ylist = []
    zlist = []
    for i in range(len(pcd)):
        xlist.append(pcd[i][0])
        ylist.append(pcd[i][1])
        zlist.append(pcd[i][2])

    num_connect = (len(blocks_connect))/2 - 1
    num_inner = (len(blocks_connect)) / 2

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("z")
    for i in range(int(num_connect)):
        ax1.plot3D([blocks_connect[2*i+1][1], blocks_connect[2*i+2][1]], [blocks_connect[2*i+1][2], blocks_connect[2*i+2][2]],
                   [blocks_connect[2*i+1][3], blocks_connect[2*i+2][3]], color='r')

    for i in range(int(num_inner)):
        ax1.plot3D([blocks_connect[2*i][1], blocks_connect[2*i+1][1]], [blocks_connect[2*i][2], blocks_connect[2*i+1][2]],
                   [blocks_connect[2*i][3], blocks_connect[2*i+1][3]], color='y')

    ax1.scatter(xlist, ylist, zlist, color='gray', marker='.')  # xlist, ylist, zlist
    plt.show()
    return None

def save_connectlist(blocks_connect,filename,savepath):
    un1 = []
    xlist = []
    ylist = []
    zlist = []
    for i in range(len(blocks_connect)):
        un1.append(blocks_connect[i][0])
        xlist.append(blocks_connect[i][1])
        ylist.append(blocks_connect[i][2])
        zlist.append(blocks_connect[i][3])
    method.read_save.save_txt4(un1,xlist,ylist,zlist,filename,savepath)
    return None

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud("D:\项目_py编译器\Lost_polyhedron\db/pcd/根节点.pcd")
    root_prompt = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/根节点提示符.txt")
    orient_first = [10.28149986, 29.80597305, 5.34687901]
    orient_last = [10.26041031, 29.82031059, 5.48218012]
    search_radius = 0.4
    shrink_angle = 40

    connectlist = base_connectlist(orient_first, orient_last, pcd, root_prompt)
    print(connectlist)

    pcd_tree = o3d.geometry.KDTreeFlann(pcd)
    blocks_connect = cluster_connect(connectlist, pcd, pcd_tree, root_prompt,search_radius, shrink_angle)
    print("最终收敛链表",blocks_connect)

    view(pcd, blocks_connect)

    # 打开此函数前更改保存名称
    # save_connectlist(blocks_connect, filename="收敛链表_2",savepath="D:\项目_py编译器\Lost_polyhedron\db/txt/")