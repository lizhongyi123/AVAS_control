"""该文件定义了读取各种文件的工具函数"""
import struct
import numpy

def write_to_txt():
    pass
def read_txt(input, out='dict', readdall=None):
    """
    :param input: 需要读取的txt文件
    :out:结果返回的类型，可选参数为dict， list
    :return:{}or[]
    注意：当输出为字典格式的时候，文件中存在相同key会出现覆盖的情况
    """
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


    input_lines = [i.split() for i in input_lines if i.strip()]
    input_lines = [[word.lower() for word in line] for line in input_lines]

    for i in input_lines:
        if i[0] == 'bend':
            i[1] == float(i[4]/180) * float(i[5])

    if out == 'list':
        return input_lines


    res = {}
    for i in input_lines:
        tmp_dict = {}
        if len(i) == 1:
            pass
        elif len(i) == 2:
            res[i[0]] = i[1]
        else:
            res[i[0]] = i[1:]
    return res

    # return input_lines

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




#
if __name__ == "__main__":
    # print(read_txt(r'C:\Users\anxin\Desktop\cafe_avas\InputFile\lattice.txt', out='list'))
    # print(read_txt(r"C:\Users\anxin\Desktop\comparison\avas_test\inputFile\lattice_mulp.txt", "list"))
    path = r"C:\Users\anxin\Desktop\test_acct\InputFile\part_rfq.dst"
    res = read_dst(path)
    print(res['phase'][0])