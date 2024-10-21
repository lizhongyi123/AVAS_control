import sys

from dataprovision.beamset import BeamsetParameter
import math
from global_varible import c_light, Pi

import struct
import os
import numpy
from utils.getinfotools import get_mass_freq, get_timestep
import numpy as np
from dataprovision.datasetparameter import DatasetParameter
import time
from multiprocessing import Pool, cpu_count
from dataprovision.densityparameter import DensityParameter
import matplotlib.pyplot as plt

class PlttoDensity():
    def __init__(self, pltpath, dataset_path, target_density_path, normal_density_path=None, project_path=None):
        self.project_path = project_path
        self.plt_path = pltpath
        self.dataset_path = dataset_path
        self.target_density_path = target_density_path
        self.normal_density_path = normal_density_path

        self.bins = 300
    def get_all_step(self):
        obj = BeamsetParameter(self.plt_path)
        all_step =obj.get_step()
        return all_step
    def read_beamset_onestep_worker(self, args):
        dataset_obj, beamset_obj, index = args
        # 这里复制 read_beamset_onestep 的逻辑
        res = {}
        # 读取beasmset中的某一步，并返回结果
        one_dict, one_lis = beamset_obj.get_one_parameter(index)
        # 位置

        zg = one_dict["location"]

        emit = [dataset_obj.emit_x[index], dataset_obj.emit_y[index], dataset_obj.emit_z[index]]
        rms_size = [dataset_obj.rms_x[index], dataset_obj.rms_y[index], dataset_obj.rms_z[index]]

        syn_x = dataset_obj.syn_x[index]
        syn_y = dataset_obj.syn_y[index]



        # t1 = time.time()
        filtered_lis = [i for i in one_lis if i[-1] != 1]
        x = np.array([i[0] for i in filtered_lis]) + syn_x
        y = np.array([i[2] for i in filtered_lis]) + syn_y
        z = np.array([i[4] for i in filtered_lis])
        r = np.sqrt(x ** 2 + y ** 2)




        nownumofp = len(x)
        moy = [np.mean(x), np.mean(y), np.mean(r), 0]

        maxb = [np.max(x), np.max(y), np.max(r), np.max(z)]
        minb = [np.min(x), np.min(y), np.min(r), np.min(z)]

        maxr = maxb
        minr = minb

        tab = []



        for i in range(4):
            if i == 0:
                counts, bin_edges = np.histogram(x, bins=self.bins, range=(minb[0], maxb[0]))
            elif i == 1:
                counts, bin_edges = np.histogram(y, bins=self.bins, range=(minb[1], maxb[1]))

            elif i == 2:
                counts, bin_edges = np.histogram(r, bins=self.bins, range=(minb[2], maxb[2]))
            elif i == 3:
                counts, bin_edges = np.histogram(z, bins=self.bins, range=(minb[3], maxb[3]))


            # print(counts)
            # counts = counts / np.max(counts)
            tab.append(counts)
        # t3 = time.time()
        # dt3 = t3-t2
        # self.dt3 += dt3
        res["zg"] = zg
        res["emit"] = emit
        res["rms_size"] = rms_size
        res["nownumofp"] = nownumofp
        res["moy"] = moy
        res["maxb"] = maxb
        res["minb"] = minb
        res["maxr"] = maxr
        res["minr"] = minr
        res["tab"] = tab

        return res

    def generatet_density_data_onestep(self, isnormal):
        """
        使用多进程并行生成密度数据
        """
        dataset_obj = DatasetParameter(self.dataset_path)
        dataset_obj.get_parameter()
        # print(dataset_obj.x[-1])
        beamset_obj = BeamsetParameter(self.plt_path)
        all_step = beamset_obj.get_step() - 1

        dumpPeriodicity = beamset_obj.dumpPeriodicity
        # print(all_step)

        # breakpoint()
        # 使用进程池并行处理每一步的数据
        num_workers = cpu_count()  # 根据 CPU 核心数动态调整
        with Pool(num_workers) as pool:  # 使用上下文管理器
            # 准备每一步的参数
            args = [(dataset_obj, beamset_obj, i) for i in range(all_step)]

            # 使用进程池并行执行每一步数据处理
            results = pool.map(self.read_beamset_onestep_worker, args)

        # 收集并整理结果
        # self.dt1 =0
        # self.dt2 =0
        # self.dt3 =0
        # results = []
        # for i in range(0, 1000):
        #     args = (dataset_obj, beamset_obj, i)
        #     results.append(self.read_beamset_onestep_worker(args))
        # print(self.dt1)
        # print(self.dt2)
        # print(self.dt3)
        # breakpoint()
        # args = (dataset_obj, beamset_obj, 18036)
        # results.append(self.read_beamset_onestep_worker(args))

        zg_lis = [res["zg"] for res in results]
        emit_lis = [res["emit"] for res in results]
        rms_size_lis = [res["rms_size"] for res in results]
        nownumofp_lis = [res["nownumofp"] for res in results]
        moy_lis = [res["moy"] for res in results]
        maxb_lis = [res["maxb"] for res in results]
        minb_lis = [res["minb"] for res in results]
        maxr_lis = [res["maxr"] for res in results]
        minr_lis = [res["minr"] for res in results]
        tab_lis = [res["tab"] for res in results]

        lost_lis = [0] + [nownumofp_lis[i] - nownumofp_lis[i - 1] for i in range(1, len(nownumofp_lis))]
        lost_lis = lost_lis
        maxlost_lis = lost_lis
        minlost_lis = lost_lis
        # print(zg_lis)
        if isnormal == 0:
            density_normal_obj = DensityParameter(self.normal_density_path)
            normal_data = density_normal_obj.get_parameter()
            normal_zg_lis = np.array(normal_data["zg_lis"])

            normal_step = len(normal_zg_lis)

            if normal_step <= len(zg_lis):
                delta_zg = np.array(zg_lis)[:normal_step] - normal_zg_lis

                emit_lis = emit_lis[0:normal_step]
                rms_size_lis = rms_size_lis[0:normal_step]
                nownumofp_lis = nownumofp_lis[0:normal_step]
                lost_lis = lost_lis[0:normal_step]
                minlost_lis = minlost_lis[0:normal_step]
                maxlost_lis = maxlost_lis[0:normal_step]

                moy_lis = np.array(moy_lis)[0:normal_step]
                moy_lis[:, 3] = delta_zg

                maxb_lis = np.array(maxb_lis)[0:normal_step]
                maxb_lis[:, 3] += delta_zg

                minb_lis = np.array(minb_lis)[0:normal_step]
                minb_lis[:, 3] += delta_zg

                maxr_lis = np.array(maxr_lis)[0:normal_step]
                maxr_lis[:, 3] += delta_zg

                minr_lis = np.array(minr_lis)[0:normal_step]
                minr_lis[:, 3] += delta_zg

                tab_lis = tab_lis[0:normal_step]
                zg_lis = normal_zg_lis


            elif normal_step > len(zg_lis):

                E = dataset_obj.ek[-1]

                BaseMassInMeV, freq = get_mass_freq(self.project_path)
                timestep = get_timestep(self.project_path)

                timestep = timestep * dumpPeriodicity

                gamma = 1 + E / BaseMassInMeV
                beta = np.sqrt(1-1 / (gamma**2))
                v = beta * c_light
                delta_z = v * timestep

                delta_step = normal_step - len(zg_lis)
                for i in range(delta_step):
                    next_z = zg_lis[-1] + delta_z
                    zg_lis.append(next_z)
                    # zg_lis = np.append(zg_lis, next_z)
                # print(len(zg_lis))
                # print(normal_zg_lis[-10:])
                # print(zg_lis[-10:])
                delta_zg = np.array(zg_lis) - normal_zg_lis

                emit_lis = emit_lis + [emit_lis[-1]] * delta_step
                # print(emit_lis)
                rms_size_lis = rms_size_lis + [rms_size_lis[-1]] * delta_step
                nownumofp_lis = nownumofp_lis + [nownumofp_lis[-1]] * delta_step


                moy_lis = np.array(moy_lis + [moy_lis[-1]] * delta_step)

                moy_lis[:, 3] = delta_zg

                maxb_lis = np.array(maxb_lis + [maxb_lis[-1]] * delta_step)
                maxb_lis[:, 3] += delta_zg

                minb_lis = np.array(minb_lis + [minb_lis[-1]] * delta_step)
                minb_lis[:, 3] += delta_zg

                maxr_lis = np.array(maxr_lis + [maxr_lis[-1]] * delta_step)
                maxr_lis[:, 3] += delta_zg

                minr_lis = np.array(minr_lis + [minr_lis[-1]] * delta_step)
                minr_lis[:, 3] += delta_zg

                tab_lis = tab_lis + [tab_lis[-1]] * delta_step

                lost_lis = lost_lis + [0] * delta_step
                minlost_lis = minlost_lis + [0] * delta_step
                maxlost_lis = maxlost_lis + [0] * delta_step
                zg_lis = normal_zg_lis

        res = {}
        res["zg_lis"] = zg_lis
        res["emit_lis"] = emit_lis
        res["rms_size_lis"] = rms_size_lis
        res["nownumofp_lis"] = nownumofp_lis
        res["lost_lis"] = lost_lis
        res["maxlost_lis"] = maxlost_lis
        res["minlost_lis"] = minlost_lis
        res["moy_lis"] = moy_lis
        res["maxb_lis"] = maxb_lis
        res["minb_lis"] = minb_lis
        res["maxr_lis"] = maxr_lis
        res["minr_lis"] = minr_lis
        res["tab_lis"] = tab_lis

        return res
    # def write_file(self, path, data):
    #     binary_data = struct.pack("i", len(data["zg_lis"]))  #该文件共有多少步
    #     binary_data += struct.pack("i", self.bins)   #网格划分步数
    #
    #     for i in range(len(data["zg_lis"])):
    #         print(i)
    #         # 依次打包不同的数据字段
    #         binary_data += struct.pack('f', data["zg_lis"][i])  # 打包 zg_lis
    #         # print(len(data["emit_lis"][i]))
    #         binary_data += struct.pack('f' * 3, *data["emit_lis"][i])  # 打包 emit_lis 3 个 float
    #         binary_data += struct.pack('f' * 3, *data["rms_size_lis"][i])  # 打包 rms_size 3 个 float
    #         binary_data += struct.pack('i', data["nownumofp_lis"][i])  # 打包 nownumofp_lis 为 int
    #         binary_data += struct.pack('i', data["lost_lis"][i])  # 打包 lost_lis 为 int
    #         binary_data += struct.pack('i', data["maxlost_lis"][i])  # 打包 maxlost_lis 为 int
    #         binary_data += struct.pack('i', data["minlost_lis"][i])  # 打包 minlost_lis 为 int
    #
    #         # 打包 4 个 float
    #         binary_data += struct.pack('f' * 4, *data["moy_lis"][i])
    #         binary_data += struct.pack('f' * 4, *data["maxb_lis"][i])
    #         binary_data += struct.pack('f' * 4, *data["minb_lis"][i])
    #         binary_data += struct.pack('f' * 4, *data["maxr_lis"][i])
    #         binary_data += struct.pack('f' * 4, *data["minr_lis"][i])
    #
    #         # 动态处理 self.bins 数量的数据
    #         binary_data += struct.pack('i' * self.bins, *data["tab_lis"][i][0])
    #         binary_data += struct.pack('i' * self.bins, *data["tab_lis"][i][1])
    #         binary_data += struct.pack('i' * self.bins, *data["tab_lis"][i][2])
    #         binary_data += struct.pack('i' * self.bins, *data["tab_lis"][i][3])
    #
    #     # 直接写入二进制数据
    #     with open(path, "wb") as f:
    #         f.write(binary_data)

    # def process_data_chunk(self, data_chunk):
    #     binary_data = []
    #     binary_data.append(struct.pack('f', data_chunk["zg_lis"]))  # 打包 zg_lis
    #     binary_data.append(struct.pack('f' * 3, *data_chunk["emit_lis"]))  # 打包 emit_lis
    #     binary_data.append(struct.pack('f' * 3, *data_chunk["rms_size_lis"]))  # 打包 rms_size
    #     binary_data.append(struct.pack('i', data_chunk["nownumofp_lis"]))  # 打包 nownumofp_lis
    #     binary_data.append(struct.pack('i', data_chunk["lost_lis"]))  # 打包 lost_lis
    #     binary_data.append(struct.pack('i', data_chunk["maxlost_lis"]))  # 打包 maxlost_lis
    #     binary_data.append(struct.pack('i', data_chunk["minlost_lis"]))  # 打包 minlost_lis
    #
    #     # 打包 4 个 float
    #     binary_data.append(struct.pack('f' * 4, *data_chunk["moy_lis"]))
    #     binary_data.append(struct.pack('f' * 4, *data_chunk["maxb_lis"]))
    #     binary_data.append(struct.pack('f' * 4, *data_chunk["minb_lis"]))
    #     binary_data.append(struct.pack('f' * 4, *data_chunk["maxr_lis"]))
    #     binary_data.append(struct.pack('f' * 4, *data_chunk["minr_lis"]))
    #
    #     # 动态处理 bins 数量的数据
    #     binary_data.append(struct.pack('i' * self.bins, *data_chunk["tab_lis"][0]))
    #     binary_data.append(struct.pack('i' * self.bins, *data_chunk["tab_lis"][1]))
    #     binary_data.append(struct.pack('i' * self.bins, *data_chunk["tab_lis"][2]))
    #     binary_data.append(struct.pack('i' * self.bins, *data_chunk["tab_lis"][3]))
    #
    #     return b''.join(binary_data)
    #
    # # 主进程负责调度和写文件
    # def write_file(self, path, data):
    #     # 初始步骤信息：文件共有多少步和网格划分步数
    #     initial_data = []
    #     initial_data.append(struct.pack("i", len(data["zg_lis"])))  # 文件共有多少步
    #     initial_data.append(struct.pack("i", self.bins))  # 网格划分步数
    #
    #     # 将所有数据块打包为元组 (data_chunk, bins) 传递给子进程
    #     data_chunks = [
    #             {
    #                 "zg_lis": data["zg_lis"][i],
    #                 "emit_lis": data["emit_lis"][i],
    #                 "rms_size_lis": data["rms_size_lis"][i],
    #                 "nownumofp_lis": data["nownumofp_lis"][i],
    #                 "lost_lis": data["lost_lis"][i],
    #                 "maxlost_lis": data["maxlost_lis"][i],
    #                 "minlost_lis": data["minlost_lis"][i],
    #                 "moy_lis": data["moy_lis"][i],
    #                 "maxb_lis": data["maxb_lis"][i],
    #                 "minb_lis": data["minb_lis"][i],
    #                 "maxr_lis": data["maxr_lis"][i],
    #                 "minr_lis": data["minr_lis"][i],
    #                 "tab_lis": data["tab_lis"][i]
    #             }
    #         for i in range(len(data["zg_lis"]))
    #     ]
    #
    #     # 使用 Pool 来进行并行处理
    #     num_workers = cpu_count()  # 你可以根据系统的 CPU 核心数量调整这个值
    #     with Pool(num_workers) as pool:
    #         # 利用 map 分发任务并获取结果
    #         results = pool.map(self.process_data_chunk, data_chunks)
    #
    #     # 将处理好的数据写入文件
    #     with open(path, "wb") as f:
    #         f.write(b''.join(initial_data))  # 先写入初始步骤信息
    #         for result in results:
    #             f.write(result)  # 写入每个进程处理的结果

    def write_file(self, path, data):
        binary_data = []  # 使用列表来存储中间结果，减少拼接操作
        binary_data.append(struct.pack("i", len(data["zg_lis"])))  # 文件共有多少步
        binary_data.append(struct.pack("i", self.bins))  # 网格划分步数

        for i in range(len(data["zg_lis"])):
            binary_data.append(struct.pack('f', data["zg_lis"][i]))  # 打包 zg_lis
            binary_data.append(struct.pack('f' * 3, *data["emit_lis"][i]))  # 打包 emit_lis
            binary_data.append(struct.pack('f' * 3, *data["rms_size_lis"][i]))  # 打包 rms_size
            binary_data.append(struct.pack('i', data["nownumofp_lis"][i]))  # 打包 nownumofp_lis
            binary_data.append(struct.pack('i', data["lost_lis"][i]))  # 打包 lost_lis
            binary_data.append(struct.pack('i', data["maxlost_lis"][i]))  # 打包 maxlost_lis
            binary_data.append(struct.pack('i', data["minlost_lis"][i]))  # 打包 minlost_lis

            binary_data.append(struct.pack('f' * 4, *data["moy_lis"][i]))
            binary_data.append(struct.pack('f' * 4, *data["maxb_lis"][i]))
            binary_data.append(struct.pack('f' * 4, *data["minb_lis"][i]))
            binary_data.append(struct.pack('f' * 4, *data["maxr_lis"][i]))
            binary_data.append(struct.pack('f' * 4, *data["minr_lis"][i]))

            binary_data.append(struct.pack('i' * self.bins, *data["tab_lis"][i][0]))
            binary_data.append(struct.pack('i' * self.bins, *data["tab_lis"][i][1]))
            binary_data.append(struct.pack('i' * self.bins, *data["tab_lis"][i][2]))
            binary_data.append(struct.pack('i' * self.bins, *data["tab_lis"][i][3]))

        # 最后统一写入文件
        with open(path, "wb") as f:
            f.write(b''.join(binary_data))  # 使用 join 一次性写入

    def generate_density_file_onestep(self, isnormal):
        data = self.generatet_density_data_onestep(isnormal)
        self.write_file(self.target_density_path, data)


class MergeDensityData(PlttoDensity):
    def __init__(self, source_paths, target_path):
        self.source_paths = source_paths
        self.target_path = target_path
        self.bins = 300

    def generate_data(self):
        all_data = []

        for path in self.source_paths:
            density_obj = DensityParameter(path)
            data = density_obj.get_parameter()
            all_data.append(data)

        res = {}
        zg_lis = all_data[0]["zg_lis"]
        # print(zg_lis)
        data_length = len(all_data)

        all_emit_lis = [all_data[i]["emit_lis"] for i in range(data_length)]

        emit_lis = [[sum(values) / len(values) for values in zip(*rows)]
                              for rows in zip(*all_emit_lis)]

        all_rms_size_lis = [all_data[i]["rms_size_lis"] for i in range(data_length)]
        rms_size_lis = [[sum(values) / len(values) for values in zip(*rows)]
                              for rows in zip(*all_rms_size_lis)]

        all_nownumofp_lis = [all_data[i]["nownumofp_lis"] for i in range(data_length)]
        nownumofp_lis = [int(sum(values) / len(values)) for values in zip(*all_nownumofp_lis)]

        all_lost_lis = [all_data[i]["lost_lis"] for i in range(data_length)]
        lost_lis = [int(sum(values) / len(values)) for values in zip(*all_lost_lis)]

        maxlost_lis = [max(values) for values in zip(*all_lost_lis)]
        minlost_lis = [min(values) for values in zip(*all_lost_lis)]

        all_moy_lis = [all_data[i]["moy_lis"] for i in range(data_length)]
        moy_lis = [[sum(values) / len(values) for values in zip(*rows)]
                              for rows in zip(*all_moy_lis)]

        all_maxb_lis = [all_data[i]["maxb_lis"] for i in range(data_length)]
        maxb_lis = [[np.max(values) for values in zip(*rows)]
                              for rows in zip(*all_maxb_lis)]
        # print(maxb_lis[:3])
        all_minb_lis = [all_data[i]["minb_lis"] for i in range(data_length)]
        minb_lis = [[np.min(values) for values in zip(*rows)]
                              for rows in zip(*all_minb_lis)]
        # print(minb_lis[:3])

        all_maxr_lis = [all_data[i]["maxr_lis"] for i in range(data_length)]
        maxr_lis = [[np.min(values) for values in zip(*rows)]
                    for rows in zip(*all_maxr_lis)]

        all_minr_lis = [all_data[i]["minr_lis"] for i in range(data_length)]
        minr_lis = [[np.max(values) for values in zip(*rows)]
                    for rows in zip(*all_minr_lis)]

        all_tab_lis = [all_data[i]["tab_lis"] for i in range(data_length)]

        combined_counts = []
        # print(len(zg_lis))
        for i in range(len(zg_lis)):
            # print(i)
            combined_x = np.array([0 for i in range(self.bins)])
            combined_y = np.array([0 for i in range(self.bins)])
            combined_r = np.array([0 for i in range(self.bins)])
            combined_z = np.array([0 for i in range(self.bins)])

            new_min_x = minb_lis[i][0]
            new_min_y = minb_lis[i][1]
            new_min_r = minb_lis[i][2]
            new_min_z = minb_lis[i][3]

            new_max_x = maxb_lis[i][0]
            new_max_y = maxb_lis[i][1]
            new_max_r = maxb_lis[i][2]
            new_max_z = maxb_lis[i][3]

            for j in range(data_length):
                ori_min_x = all_minb_lis[j][i][0]
                ori_min_y = all_minb_lis[j][i][1]
                ori_min_r = all_minb_lis[j][i][2]
                ori_min_z = all_minb_lis[j][i][3]

                ori_max_x = all_maxb_lis[j][i][0]
                ori_max_y = all_maxb_lis[j][i][1]
                ori_max_r = all_maxb_lis[j][i][2]
                ori_max_z = all_maxb_lis[j][i][3]

                xbins = np.linspace(new_min_x, new_max_x, self.bins+1)
                # print(xbins)
                countsx_rescaled, _ = np.histogram(np.linspace(ori_min_x, ori_max_x, self.bins), bins=xbins,
                                                    weights=all_tab_lis[j][i][0])


                # print(len(combined_x))
                # print(len(countsx_rescaled))
                combined_x += countsx_rescaled

                ybins = np.linspace(new_min_y, new_max_y, self.bins+1)
                countsy_rescaled, _ = np.histogram(np.linspace(ori_min_y, ori_max_y, self.bins), bins=ybins,
                                                    weights=all_tab_lis[j][i][1])


                combined_y += countsy_rescaled

                rbins = np.linspace(new_min_r, new_max_r, self.bins+1)
                countsr_rescaled, _ = np.histogram(np.linspace(ori_min_r, ori_max_r, self.bins), bins=rbins,
                                                   weights=all_tab_lis[j][i][2])
                combined_r += countsr_rescaled

                zbins = np.linspace(new_min_z, new_max_z, self.bins+1)
                countsz_rescaled, _ = np.histogram(np.linspace(ori_min_z, ori_max_z, self.bins), bins=zbins,
                                                   weights=all_tab_lis[j][i][3])
                combined_z += countsz_rescaled

            v_lis= [combined_x, combined_y, combined_r, combined_z]
            combined_counts.append(v_lis)
        tab_lis = combined_counts

        res["zg_lis"] = zg_lis
        res["emit_lis"] = emit_lis
        res["rms_size_lis"] = rms_size_lis
        res["nownumofp_lis"] = nownumofp_lis
        res["lost_lis"] = lost_lis
        res["maxlost_lis"] = maxlost_lis
        res["minlost_lis"] = minlost_lis
        res["moy_lis"] = moy_lis
        res["maxb_lis"] = maxb_lis
        res["minb_lis"] = minb_lis
        res["maxr_lis"] = maxr_lis
        res["minr_lis"] = minr_lis
        res["tab_lis"] = tab_lis

        return res
    def generate_density_file(self):
        data = self.generate_data()
        self.write_file(self.target_path, data)

if __name__ == "__main__":
    # beamset_path = r"C:\Users\shliu\Desktop\testz\test_density_sudu\BeamSet.plt"
    # dataset_path = r"C:\Users\shliu\Desktop\testz\test_density_sudu\DataSet.txt"
    # target_density_path = r"C:\Users\shliu\Desktop\testz\test_density_sudu\density_0_0.dat"
    # obj = PlttoDensity(beamset_path, dataset_path, target_density_path)
    # obj.generate_density_file_onestep(isnormal=1)
    #
    #
    # # beamset_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_1\BeamSet.plt"
    # # dataset_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_1\DataSet.txt"
    # # target_density_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_1\density_1_1.dat"
    # # normal_density_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_0_0\density_0_0.dat"
    # # project_path = r"C:\Users\shliu\Desktop\testz"
    #
    # # obj = PlttoDensity(beamset_path, dataset_path, target_density_path, normal_density_path, project_path)
    # # obj.generate_density_file_onestep(isnormal=0)
    #
    # # beamset_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_2\BeamSet.plt"
    # # dataset_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_2\DataSet.txt"
    # # target_density_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_2\density_1_2.dat"
    # # normal_density_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_0_0\density_0_0.dat"
    # # project_path = r"C:\Users\shliu\Desktop\testz"
    #
    # # obj = PlttoDensity(beamset_path, dataset_path, target_density_path, normal_density_path, project_path)
    # # obj.generate_density_file_onestep(isnormal=0)

    paths = [
        r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_1\density_1_1.dat",
        r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\output_1_2\density_1_2.dat",
    ]

    target_path = r"C:\Users\shliu\Desktop\testz\OutputFile\error_output\density_tot_1.dat"
    obj = MergeDensityData(paths, target_path)
    obj.generate_density_file()