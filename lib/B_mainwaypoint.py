import open3d as o3d
import numpy as np
import scipy.spatial as T
import method.read_save


def shrink_fracture(pcd ,shrink_radius, shrink_points):
    pcd.paint_uniform_color([0.5, 0.5, 0.5])
    pcd_tree = o3d.geometry.KDTreeFlann(pcd)

    k_recordlist = []
    idx1_recordlist = []

    for i in range(len(pcd.points)):
        [k1, idx1, _] = pcd_tree.search_radius_vector_3d(pcd.points[i], shrink_radius)  # 半径搜索
        k_recordlist.append(k1)


        if k_recordlist[i] >= shrink_points:  # max(k_de_recordlist) - k_de_recordlist[0] > 15 or
            # np.asarray(pcd.colors)[i] = [0, 0, 1]
            idx1_recordlist.append(i)

    # o3d.visualization.draw_geometries([pcd])

    pcd_shrink = pcd.select_by_index(idx1_recordlist)
    return pcd_shrink

def waypoints(pcd, pcd_shrink, sample_radius):
    p_list = np.asarray(pcd.points)
    matrix_p_list = T.distance.cdist(p_list, p_list, metric='euclidean')
    r, c = np.where(matrix_p_list == np.max(matrix_p_list))
    max = np.max(matrix_p_list)

    pcd_tree_shrink = o3d.geometry.KDTreeFlann(pcd)
    compare_list = []
    waypoint_list = []
    for i in range(len(r)):
        np.asarray(pcd.colors)[r[i]] = [1, 0, 0]
        waypoint_list.append(list(np.asarray(pcd.points[r[i]])))


    for i in range(len(pcd_shrink.points)):

        if i not in compare_list:
            [k, idx, _] = pcd_tree_shrink.search_radius_vector_3d(pcd_shrink.points[i], sample_radius)  # 半径搜索

            for j in range(len(idx)):
                compare_list.append(j)

            np.asarray(pcd_shrink.colors)[i] = [1, 0, 0]
            waypoint_list.append(list(pcd_shrink.points[i]))


    waypoint_list_unic = []
    for element in waypoint_list:
        if element not in waypoint_list_unic:
            waypoint_list_unic.append(element)
    print(waypoint_list_unic)
    o3d.visualization.draw_geometries([pcd_shrink, pcd])
    return waypoint_list_unic

def save_waypoints(waypoint_list_unic,filename,savepath):
    # waypoint_list_unic = np.asarray(pcd_shrink.points)
    xlist = []
    ylist = []
    zlist = []
    for i in range(len(waypoint_list_unic)):
        xlist.append(waypoint_list_unic[i][0])
        ylist.append(waypoint_list_unic[i][1])
        zlist.append(waypoint_list_unic[i][2])
    method.read_save.save_txt3(xlist, ylist, zlist, filename, savepath)
    return None

if __name__ == '__main__':

    # 记得该文件排序
    waypoint_file = 1

    shrink_radius = 0.3
    shrink_points = 90
    sample_radius = 0.4
    pcd = o3d.io.read_point_cloud("D:\项目_py编译器\Lost_polyhedron\db/pcd/小结构缝聚类_%s.pcd"%(waypoint_file))
    # 控制收缩集中度
    pcd_shrink = shrink_fracture(pcd, shrink_radius, shrink_points)
    print(pcd_shrink)
    # 控制稀疏度
    waypoint_list_unic = waypoints(pcd, pcd_shrink, sample_radius)
    print(waypoint_list_unic)

    # 选择保存：pcd_shrink（稀疏前），waypoint_list_unic（稀疏后）
    # save_waypoints(waypoint_list_unic, filename ="路点%s"%(waypoint_file), savepath = "D:\项目_py编译器\Lost_polyhedron\db/txt/")