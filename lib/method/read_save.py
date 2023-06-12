import os


def read_txt1(file):     # = open("D:/dotjob/txt/backwall_idx.txt", "r")
    un1 = []

    for line in file.readlines():
        line = line.strip('\n')
        data = [float(i) for i in line.split()]
        un1.append(data[0])

    return un1

def read_txt3(file):     # = open("D:/dotjob/txt/backwall_idx.txt", "r")
    x = []
    y = []
    z = []
    for line in file.readlines():
        line = line.strip('\n')
        data = [float(i) for i in line.split()]
        x.append(data[0])
        y.append(data[1])
        z.append(data[2])

    return x,y,z

def read_txt4(file):    # = open("D:/dotjob/txt/backwall_idx.txt", "r")
    x = []
    y = []
    z = []
    un1 = []
    for line in file.readlines():
        line = line.strip('\n')
        data = [float(i) for i in line.split()]
        x.append(data[0])
        y.append(data[1])
        z.append(data[2])
        un1.append(data[3])
    return x, y, z, un1

def read_txt7(file):    # = open("D:/dotjob/txt/backwall_idx.txt", "r")
    x = []
    y = []
    z = []
    un1 = []
    un2 = []
    un3 = []
    un4 = []
    for line in file.readlines():
        line = line.strip('\n')
        data = [float(i) for i in line.split()]
        x.append(data[0])
        y.append(data[1])
        z.append(data[2])
        un1.append(data[3])
        un1.append(data[4])
        un1.append(data[5])
        un1.append(data[6])
    return x, y, z, un1, un2, un3, un4

def save_pcd3(xlist,ylist,zlist,filename,savepath):
    '''
    存3列pcd 到"D:/dotjob/pcd/"

    :return:
    '''
    savefilename = "%s"%(filename) + ".pcd"
    savefilename = "%s"%(savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        file_to_write.writelines("# .PCD v0.7 - Point Cloud Data file format\n")
        file_to_write.writelines("VERSION 0.7\n")
        file_to_write.writelines("FIELDS x y z\n")
        file_to_write.writelines("SIZE 4 4 4\n")
        file_to_write.writelines("TYPE F F F\n")
        file_to_write.writelines("COUNT 1 1 1\n")
        file_to_write.writelines("WIDTH " + str(len(xlist)) + "\n")
        file_to_write.writelines("HEIGHT 1\n")
        file_to_write.writelines("VIEWPOINT 0 0 0 1 0 0 0\n")
        file_to_write.writelines("POINTS " + str(len(xlist)) + "\n")
        file_to_write.writelines("DATA ascii\n")
        for i in range(len(xlist)):
            file_to_write.writelines(str(xlist[i]) + " " + str(ylist[i]) + " " + str(zlist[i]) + "\n")
    return None

def save_txt1(un1,filename,savepath):
    '''
    存3列txt 到"D:/项目_py编译器/DRI_ResetEdition_v1.1/db/pcd/"

    :return:
    '''
    savefilename = "%s" % (filename) + ".txt"
    savefilename = "%s" % (savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(un1)):
            file_to_write.writelines(str(un1[i]) + "\n")
    return None

def save_txt2(xlist,ylist,filename,savepath):
    '''
    存3列txt 到"D:/项目_py编译器/DRI_ResetEdition_v1.1/db/pcd/"

    :return:
    '''
    savefilename = "%s" % (filename) + ".txt"
    savefilename = "%s" % (savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(xlist)):
            file_to_write.writelines(str(xlist[i]) + " " + str(ylist[i]) + "\n")
    return None

def save_txt3(xlist,ylist,zlist,filename,savepath):
    '''
    存3列txt 到"D:/项目_py编译器/DRI_ResetEdition_v1.1/db/pcd/"

    :return:
    '''
    savefilename = "%s" % (filename) + ".txt"
    savefilename = "%s" % (savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(xlist)):
            file_to_write.writelines(str(xlist[i]) + " " + str(ylist[i]) + " " + str(zlist[i]) + "\n")
    return None


def save_txt4(xlist, ylist, zlist, un1,filename,savepath):
    '''
    存4列txt 到"D:/dotjob/txt/"

    :return:
    '''
    savefilename = "%s" % (filename) + ".txt"
    savefilename = "%s" % (savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(xlist)):
            file_to_write.writelines(str(xlist[i]) + " " + str(ylist[i]) + " " + str(zlist[i]) + " " + str(un1[i])+"\n")
    return None

def save_txt5(un1, un2, un3, un4, un5, filename, savepath):
    '''
    存7列txt 到"D:/dotjob/txt/"

    :return:
    '''
    savefilename = "%s" %(filename) + ".txt"
    savefilename = "%s" %(savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(un1)):
            file_to_write.writelines(str(un1[i]) + " " + str(un2[i]) + " " + str(un3[i]) + " " + str(un4[i])+ " " +
                                     str(un5[i])+ "\n")
    return None

def save_txt8(xlist, ylist, zlist, un1, un2, un3, un4, un5,filename,savepath):
    '''
    存7列txt 到"D:/dotjob/txt/"

    :return:
    '''
    savefilename = "%s" %(filename) + ".txt"
    savefilename = "%s" %(savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(xlist)):
            file_to_write.writelines(str(xlist[i]) + " " + str(ylist[i]) + " " + str(zlist[i]) + " " + str(un1[i])+ " " +
                                     str(un2[i])+ " " + str(un3[i])+ " " + str(un4[i]) + " " + str(un5[i]) + "\n")
    return None

def save_txt9(xlist, ylist, zlist, un1, un2, un3, un4, un5, un6, filename,savepath):
    '''
    存7列txt 到"D:/dotjob/txt/"

    :return:
    '''
    savefilename = "%s" %(filename) + ".txt"
    savefilename = "%s" %(savepath) + savefilename
    if not os.path.exists(savefilename):
        f = open(savefilename, 'w')
        f.close()
    with open(savefilename, 'w') as file_to_write:
        for i in range(len(xlist)):
            file_to_write.writelines(str(xlist[i]) + " " + str(ylist[i]) + " " + str(zlist[i]) + " " + str(un1[i])+ " " +
                                     str(un2[i])+ " " + str(un3[i])+ " " + str(un4[i]) + " " + str(un5[i]) + " " + str(un6[i]) + "\n")
    return None
# if __name__ == '__main__':
#     read_txt3()
#     read_txt4()
#     read_txt7()