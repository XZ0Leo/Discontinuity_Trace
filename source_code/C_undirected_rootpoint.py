import numpy as np
import method.read_save

def root_node_pcd_fracture(num_waypoint_cluster):

    root_node = []
    pcd_fracture =[]
    for num_cluster in range(num_waypoint_cluster):

        undirected_map = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/生成树无向图%s.txt"%(num_cluster))
        waypoint_list = np.loadtxt("D:\项目_py编译器\Lost_polyhedron\db/txt/路点%s.txt"%(num_cluster))

        root_node_pre = []
        for i in range(len(undirected_map)):
            num_node = 0
            for n in undirected_map[i]:
                if n == 1:
                    num_node += 1

            if num_node == 1:
                element_root = [num_cluster,i]
                root_node_pre.append(i)
                root_node.append(element_root)


        for i in root_node_pre:
            pcd_fracture.append(list(waypoint_list[i]))



    return root_node, pcd_fracture

def save(root_node, pcd_fracture):
    x_root_node = []
    y_root_node = []
    for i in range(len(root_node)):
        x_root_node.append(root_node[i][0])
        y_root_node.append(root_node[i][1])
    method.read_save.save_txt2(x_root_node,y_root_node,filename="根节点提示符",savepath="D:\项目_py编译器\Lost_polyhedron\db/txt/")
    x_pcd_fracture = []
    y_pcd_fracture = []
    z_pcd_fracture = []
    for i in range(len(pcd_fracture)):
        x_pcd_fracture.append(pcd_fracture[i][0])
        y_pcd_fracture.append(pcd_fracture[i][1])
        z_pcd_fracture.append(pcd_fracture[i][2])
    method.read_save.save_pcd3(x_pcd_fracture,y_pcd_fracture,z_pcd_fracture,filename="根节点",savepath="D:\项目_py编译器\Lost_polyhedron\db/pcd/")
    return None

if __name__ == '__main__':
    root_node, pcd_fracture = root_node_pcd_fracture(num_waypoint_cluster=14)
    print(root_node)
    print(pcd_fracture)
    # save(root_node, pcd_fracture)