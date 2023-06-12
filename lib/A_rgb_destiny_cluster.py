import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import method.read_save


def read_txt3(file):     # = open("D:/dotjob/txt/backwall_idx.txt", "r")
    x = []
    y = []
    z = []
    r = []
    g = []
    b = []
    for line in file.readlines():
        line = line.strip('\n')
        data = [float(i) for i in line.split()]
        x.append(data[0])
        y.append(data[1])
        z.append(data[2])
        r.append(data[3])
        g.append(data[4])
        b.append(data[5])
    return x,y,z,r,g,b



def pcd_rgb(pcd, r , g, b, gray_normal):
    select_index = []
    for i in range(len(pcd.points)):

        np.asarray(pcd.colors)[i] = [r[i]/255, g[i]/255, b[i]/255]
        if r[i]/255 < gray_normal and g[i]/255 < gray_normal and b[i]/255 < gray_normal:
            np.asarray(pcd.colors)[i] = [1,0,1]
            select_index.append(i)
        else:
            np.asarray(pcd.colors)[i] = [1,1,0]
    # o3d.visualization.draw_geometries([pcd])


    pcd_rgb = pcd.select_by_index(select_index)
    return pcd_rgb

def pcd_rgb_des(pcd_rgb, grand, destiny, destiny_radius):
    pcd_tree = o3d.geometry.KDTreeFlann(pcd_rgb)

    k_recordlist = []
    idx1_recordlist = []
    pcd_rgb_destiny = []

    for i in range(len(pcd_rgb.points)):
        [k1, idx1, _] = pcd_tree.search_radius_vector_3d(pcd_rgb.points[i], destiny_radius)  # 半径搜索
        k_recordlist.append(k1)
        idx1_recordlist.append(idx1)

    k_de_recordlist = []
    k_idx1_recordlist = []
    for i in range(len(pcd_rgb.points)):
        k_de_recordlist.clear()
        for id in idx1_recordlist[i]:
            k_de_recordlist.append(k_recordlist[id])
        if max(k_de_recordlist) - k_de_recordlist[0] >= grand and k_recordlist[i] >= destiny:

            pcd_rgb_destiny.append(i)
    pcd_rgb_des = pcd_rgb.select_by_index(pcd_rgb_destiny)
    return pcd_rgb_des

def cluster_view(pcd_rgb_des, eps, min_points):
    with o3d.utility.VerbosityContextManager(o3d.utility.VerbosityLevel.Debug) as cm:
        # -------------------密度聚类--------------------------
        labels = np.array(pcd_rgb_des.cluster_dbscan(eps,  # 邻域距离
                                             min_points,  # 最小点数
                                             print_progress=False))  # 是否在控制台中可视化进度条

    max_label = labels.max()

    # --------------------可视化聚类结果----------------------
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    pcd_rgb_des.colors = o3d.utility.Vector3dVector(colors[:, :3])
    o3d.visualization.draw_geometries([pcd_rgb_des], window_name="点云密度聚类",
                                      height=480, width=600,
                                      mesh_show_back_face=0)
    return max_label,labels

def save_labs(datas_ori, labs, n_cluster, t_name, savepath):
    xlist = []
    ylist = []
    zlist = []
    cur_list = []
    for j in range(0,n_cluster + 1):

        for i in range(len(labs)):
            if labs[i] == j:
                xlist.append(datas_ori[i][0])
                ylist.append(datas_ori[i][1])
                zlist.append(datas_ori[i][2])
                # cur_list.append(curvature[i])
        filename = "%s"%(t_name)+ "_%s"%(j)
        # 下列函数只能开一个！！！！！！！！！！！！！！！！！！！！！！！
        # method.read_save.save_txt1(cur_list,filename)
        method.read_save.save_pcd3(xlist,ylist,zlist,filename, savepath)
        list.clear(xlist)
        list.clear(ylist)
        list.clear(zlist)


    return None

if __name__ == '__main__':
    pcd = o3d.io.read_point_cloud("D:/项目_py编译器/Lost_polyhedron/db/pcd/section2.2 - Cloud_pcd.pcd")
    x, y, z, r, g, b = read_txt3(open("D:/项目_py编译器/Lost_polyhedron/db/txt/section2.2 - Cloud.txt", "r"))

    pcd.paint_uniform_color([0.5, 0.5, 0.5])  # 把所有点渲染为灰色（灰兔子）
    pcd_rgb = pcd_rgb(pcd, r, g, b, gray_normal=0.45)
    pcd_rgb_des = pcd_rgb_des(pcd_rgb, grand=10, destiny=25, destiny_radius=0.2)
    max_label, labels = cluster_view(pcd_rgb_des, eps=0.10, min_points=18)

    datas_ori = np.asarray(pcd_rgb_des.points)
    # save_labs(datas_ori, labels, max_label, t_name ="小结构缝聚类", savepath = "D:\项目_py编译器\Lost_polyhedron\db/")