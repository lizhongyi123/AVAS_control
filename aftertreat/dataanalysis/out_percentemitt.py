from percentemitt import PercentEmit
import os


def treat_directory(directory_path, ratio):
    file_names = os.listdir(directory_path)
    if os.path.exists('result.txt'):
        os.remove('result.txt')
    with open('result.txt', 'a') as file:
        j = 0
        for file_name in file_names:
            file.write(file_name + '\n')

            file_name_all = os.path.join(directory_path, file_name)
            res = treat_one_file(file_name_all, ratio)

            for i in res:
                file.write(i + '\n')
            j += 1
            file.write('' + '\n')
            print(f'已完成第{j}个文件的计算')


def treat_one_file(dst_path, ratio):
    """
    此函数用来处理单个dst文件
    """
    v = PercentEmit(dst_path)
    res_percent = v.get_percent_emit(ratio)
    res_100 = v.get_100_emit()
    text = [
        'X-X\'',
        f'\u03B5(rms)  = {res_100[0][2]:.5f} π.mm.mrad [ Norm. ]',
        f'\u03B5(rms)[{ratio * 100}%]  = {res_percent[0][2]:.5f} π.mm.mrad [ Norm. ]',
        f'\u03B5[{ratio * 100}%] = {res_percent[0][3]:.5f} π.mm.mrad',
        # f'\u03B5[{ratio * 100}%][{ratio * 100}% twiss] = {res_percent[0][4]:.5f} π.mm.mrad',
        f'β = {res_percent[0][1]:.5f}  mm/π.mrad',
        f'α = {res_percent[0][0]:.5f}  ',
        ' ',
        'Y-Y\'',
        f'\u03B5(rms)  = {res_100[1][2]:.5f} π.mm.mrad [ Norm. ]',
        f'\u03B5(rms)[{ratio * 100}%]  = {res_percent[1][2]:.5f} π.mm.mrad [ Norm. ]',
        f'\u03B5[{ratio * 100}%] = {res_percent[1][3]:.5f} π.mm.mrad',
        # f'\u03B5[{ratio * 100}%][{ratio * 100}% twiss] = {res_percent[1][4]:.5f} π.mm.mrad',
        f'β = {res_percent[1][1]:.5f}  mm/π.mrad',
        f'α = {res_percent[1][0]:.5f}  ',
        ' ',
        'Z-Z\'',
        f'\u03B5(rms)  = {res_100[2][2]:.5f} π.mm.mrad [ Norm. ]',
        f'\u03B5(rms)[{ratio * 100}%]  = {res_percent[2][2]:.5f} π.mm.mrad [ Norm. ]',
        f'\u03B5[{ratio * 100}%] = {res_percent[2][3]:.5f} π.mm.mrad',
        # f'\u03B5[{ratio * 100}%][{ratio * 100}% twiss] = {res_percent[2][4]:.5f} π.mm.mrad',
        f'β = {res_percent[2][1]:.5f}  mm/π.mrad',
        f'α = {res_percent[2][0]:.5f}  ',
        ' ',
        'X-Y',
        f'\u03B5(rms)  = {res_100[3][2]:.5f} mm2',
        f'\u03B5(rms)[{ratio * 100}%]  = {res_percent[3][2]:.5f} mm2]',
        f'\u03B5[{ratio * 100}%] = {res_percent[3][3]:.5f} mm2',
        # f'\u03B5[{ratio * 100}%][{ratio * 100}% twiss] = {res_percent[3][4]:.5f} mm2',
        f'β = {res_percent[3][1]:.5f}  ',
        f'α = {res_percent[3][0]:.5f}  ',
    ]
    return text


if __name__ == "__main__":
    # 计算某一个dst文件的参数
    dst_path = r"E:\E\cafe\AVAS\InputFile\part_rfq.dst"

    res = treat_one_file(dst_path, 0.3)
    for i in res:
        print(i)

    # directory_path = r'C:\Users\anxin\Desktop\te'
    # treat_directory(directory_path, 0.8)