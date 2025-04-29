import struct
import sys

import numpy as np
import os

class Exdata():
    def __init__(self, path):
        self.path = path
        pass

    def get_grid_num(self):
        with open(self.path, 'rb') as f:
            tdata = struct.unpack("<c", f.read(1))

            index = struct.unpack("<i", f.read(4))

            grid_num = struct.unpack("<d", f.read(8))

            grid_num = int(grid_num[0])
            return grid_num
    def get_param(self):
        grid_num = self.get_grid_num()
        # print(21, grid_num)

        with open(self.path, 'rb') as f:

            byte_onestep = 1 + 4 + 8 + (grid_num * 4) * 4 + 8 * 12
            file_size = os.path.getsize(self.path)

            self.step = int((file_size) / byte_onestep)
            # print(28, self.step)

            dtype = np.dtype([
                ('char', '<c'),
                ('index', '<i4'),
                ('grid_num', '<f8'),
                ('f', '<i4', (4* grid_num)),  # 一口气读 1200 个 int32
                ('i', '<f8', 12),  # 一口气读   12 个 float64
            ])


            buf = f.read(byte_onestep * self.step)

            data = np.frombuffer(buf, dtype=dtype)

            # print(len(data))
            # print(data[-1])
            ex_list = []
            for i in range(len(data)):
            # for i in range():
                tab = np.array(data[i][3])

                parts = np.array_split(tab, grid_num)
                tab_x, tab_y, tab_r, tab_z = map(list, zip(*parts))

                # tab_x = [j[0] for j in parts]
                # tab_y = [j[1] for j in parts]
                # tab_r = [j[2] for j in parts]
                # tab_z = [j[3] for j in parts]
                # print(np.sum(tab_x), np.sum(tab_y), np.sum(tab_r), np.sum(tab_z))
                ex_list.append({
                    "index": data[i][1],
                    "grid_num": data[i][2],
                    "tab_x": tab_x,
                    "tab_y": tab_y,
                    "tab_r": tab_r,
                    "tab_z": tab_z,
                    "x_min": data[i][4][0],
                    "x_max": data[i][4][1],
                    "x_ave": data[i][4][2],
                    "y_min": data[i][4][3],
                    "y_max": data[i][4][4],
                    "y_ave": data[i][4][5],
                    "r_min": data[i][4][6],
                    "r_max": data[i][4][7],
                    "r_ave": data[i][4][8],
                    "z_min": data[i][4][9],
                    "z_max": data[i][4][10],
                    "z_ave": data[i][4][11],
                    })
        return ex_list
if __name__ == '__main__':
    Exdata_path = r"C:\Users\shliu\Desktop\bug\OutputFile\ExData.edt"
    obj = Exdata(Exdata_path)
    res = obj.get_param()
    print(res[0])
    print(res[-1])
