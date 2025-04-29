"""该文件定义了读取各种文件的工具函数"""
import struct
import numpy
import numpy as np
import os
from utils.exception import CustomFileNotFoundError
import re
import global_varible
def write_to_txt():
    pass
def read_txt(input, out='dict', readdall=None, case_sensitive=None):
    #目前这个函数无法处理包含重复的情况
    """
    :param input: 需要读取的txt文件
    :out:结果返回的类型，可选参数为dict， list
    :return:{}or[]
    注意：当输出为字典格式的时候，文件中存在相同key会出现覆盖的情况
    """
    if not os.path.exists(input):
        raise CustomFileNotFoundError(input)

    with open(input, encoding='UTF-8') as file_object:
        input_lines = []
        if not readdall:
            for line in file_object:
                line = line.lstrip('\ufeff')
                line = line.strip()
                if '!' in line:
                    # 如果当前行包含感叹号，只保留感叹号之前的内容
                    line = line.split('!', 1)[0]
                    input_lines.append(line)
                    continue  # 跳出循环，停止读取接下来的内容
                else:
                    input_lines.append(line)
        elif readdall:
            for line in file_object:
                line = line.lstrip('\ufeff')
                line = line.strip()
                input_lines.append(line)

    input_lines = [re.sub(":" ," : ", i) for i in input_lines]
    input_lines = [i.split() for i in input_lines if i.strip()]

    if not case_sensitive:
        #如果大小写不敏感，全都变成小写，如果敏感
        input_lines = [[word.lower() for word in line] for line in input_lines]



    if out == 'list':
        return input_lines


    res = {}
    for i in input_lines:

        tmp_dict = {}
        if len(i) == 1:
            res[i[0]] = None
        elif len(i) == 2:
            res[i[0]] = i[1]
        else:
            res[i[0]] = i[1:]
    return res

    # return input_lines
def read_lattice_mulp(lattice_mulp_path):
    res = read_txt(lattice_mulp_path, out='list', readdall=None, case_sensitive=True)

    new_lattice_list = []
    for i in res:
        i[0] = i[0].lower()
        if i[0] == 'bend':
            i[1] =np.abs(float(i[4])/180 * np.pi * float(i[5]))

        new_lattice_list.append(i)
        if i[0] == "end":
            break
    return new_lattice_list

def read_lattice_mulp_with_name(lattice_mulp_path):
    ini_lattice = read_txt(lattice_mulp_path, out='list', readdall=None, case_sensitive=True)

    #为原件添加名字，如没有名字，则添加自定义名字
    for i in ini_lattice:
        if i[0].lower() in global_varible.all_element:
            if ":" not in i:
                i.insert(0, "no_name")
                i.insert(1, ":")


    #构建命令列表和名字列表
    lattice_list = []
    name_list = []
    for i in ini_lattice:
        if ":" in i:
            lattice_list.append(i[2:])
            name_list.append(i[0])
        elif ":" not in i:
            lattice_list.append(i)
            name_list.append(None)

    #将大写变为小写
    new_lattice_list = []
    for i in lattice_list:
        i[0] = i[0].lower()
        if i[0] == 'bend':
            i[1] = np.abs(float(i[4])/180 * np.pi * float(i[5]))

        new_lattice_list.append(i)
        if i[0] == "end":
            break
    new_name_list = name_list[:len(new_lattice_list)]
    return new_lattice_list, new_name_list


def read_dst(input):
    """
    此函数为读取dst文件
    :param input:  dst文件路径
    :return:{'number': _, 'ib': _, 'freq': _, 'phase':[], 'basemassinmev': _ }
    """

    res = {}
    f = open(input, 'rb')
    # f.read(2)

    data = struct.unpack("<cc", f.read(2))


    data = struct.unpack("<i", f.read(4))
    number = int(data[0])
    res['number'] = number

    #流强
    data = struct.unpack("<d", f.read(8))
    Ib = float(data[0])
    res['ib'] = Ib

    data = struct.unpack("<d", f.read(8))
    freq = float(data[0])
    res['freq'] = freq*10**6

    data = f.read(1)
    partran_dist = numpy.arange(6 * number, dtype='float64').reshape(number, 6)

    for i in range(number):
        data = f.read(48)
        data = struct.unpack("<dddddd", data)
        partran_dist[i, 0] = data[0]
        partran_dist[i, 1] = data[1]
        partran_dist[i, 2] = data[2]
        partran_dist[i, 3] = data[3]
        partran_dist[i, 4] = data[4]
        partran_dist[i, 5] = data[5]

    res['phase'] = partran_dist

    data = struct.unpack("<d", f.read(8))
    BaseMassInMeV = data[0]
    res['basemassinmev'] = BaseMassInMeV

    f.close()
    return res

def read_dst_fast(input):
    with open(input, 'rb') as f:
        f.read(2)  # 跳过前2个字节

        # 读取整数和两个双精度浮点数
        number = struct.unpack("<i", f.read(4))[0]
        Ib = struct.unpack("<d", f.read(8))[0]
        freq = struct.unpack("<d", f.read(8))[0]

        f.read(1)  # 跳过1个字节

        # 读取 6 * number 个双精度浮点数 cm mrad
        partran_dist = np.fromfile(f, dtype='<f8', count=6 * number).reshape(number, 6)

        # 读取最后一个双精度浮点数
        BaseMassInMeV = struct.unpack("<d", f.read(8))[0]

    res= {}
    res['number'] = number
    res['ib'] = Ib
    res['freq'] = freq*10**6
    res['partran_dist'] = partran_dist
    res['basemassinmev'] = BaseMassInMeV
    energy_lis = np.array([i[5] for i in partran_dist])
    res['kneticenergy'] = np.mean(energy_lis)
    return res

def read_runsignal(path):
    res = 0
    with open(path, 'r') as file:
        line = file.readline()
        res = int(line)
    return res





#
if __name__ == "__main__":
    # print(read_txt(r'C:\Users\anxin\Desktop\cafe_avas\InputFile\lattice.txt', out='list'))
    # print(read_txt(r"C:\Users\anxin\Desktop\comparison\avas_test\inputFile\lattice_mulp.txt", "list"))
    # path = r"C:\Users\anxin\Desktop\test_acct\InputFile\part_rfq.dst"
    # res = read_dst(path)
    # print(res['phase'][0])
    # read_runsignal(0)
    path = r"C:\Users\shliu\Desktop\test_lattice\lattice_mulp.txt"
    # res = read_lattice_mulp(path)
    # for i in res:
    #     print(i)
    res = read_lattice_mulp_with_name(path)
    print(res)