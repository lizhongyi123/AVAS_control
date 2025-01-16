﻿import numpy as np
import matplotlib.pyplot as plt
import math
from aftertreat.picture.initialplot import PicturePlot_2D, CompoundShape
from utils.readfile import read_txt, read_dst
from dataprovision.datasetparameter import DatasetParameter
from dataprovision.latticeparameter import LatticeParameter
import os
# [ 'emittance_x', 'emittance_y', 'emittance_z',
# 'longitudinal_phase', ]
class PlotDataSet(PicturePlot_2D):
    """
    dataset文件的可视化
    """
    def __init__(self, dataset_path, picture_name, project_path=None):
        super().__init__()
        self.picture_name = picture_name
        self.BaseMassInMeV = 0
        self.freq = 0

        if project_path:
            self.project_path = project_path
        else:
            self.project_path = None
        self.dataset_path = dataset_path
        # self.beam_path = self.project_path + r'\InputFile' + r'\beam.txt'
        # self.lattice_path = self.project_path + r'\InputFile' + r'\lattice.txt'
        # self.lattice_mulp_path = self.project_path + r'\InputFile' + r'\lattice_mulp.txt'
        # self.input_path = self.project_path + r'\InputFile' + r'\input.txt'
        # self.dataset_path = os.path.join(self.project_path, "OutputFile", "Dataset.txt" )
        # if dataset_path:
        #     self.dataset_path = dataset_path
        # else:


    def get_mass_freq(self):
        beam_txt = self.project_path + r'\InputFile\Beam.txt'
        res = read_txt(beam_txt)
        if res.get('readparticledistribution') is None:
            BaseMassInMeV = float(res.get('particlerestmass'))
            freq = float(res.get('frequency'))
        else:
            dstfile = self.project_path + r'\InputFile' + r"\\" + res.get('readparticledistribution')
            dst_res = read_dst(dstfile)
            BaseMassInMeV = float(dst_res.get('basemassinmev'))
            freq = float(dst_res.get('freq'))
        return BaseMassInMeV, freq

    def get_x_y(self):

        dataset_obj = DatasetParameter(self.dataset_path, self.project_path)
        dataset_obj.get_parameter()
        # end_index = dataset_obj.get_lattice_end_index() + 1
        end_index = -1
        z = dataset_obj.z[:end_index]  # 束团纵向位置

        ek = dataset_obj.ek[:end_index]  # 束团平均能量



        emit_x = [i * 10**6 for i in dataset_obj.emit_x][:end_index]
        emit_y = [i * 10**6 for i in dataset_obj.emit_y][:end_index]
        emit_z = [i * 10**6 for i in dataset_obj.emit_z][:end_index]

        rms_x = [i *10**3 for i in dataset_obj.rms_x][:end_index]#单位变成mm
        rms_xx = [i *10**3 for i in dataset_obj.rms_xx][:end_index]

        rms_y = [i *10**3 for i in dataset_obj.rms_y][:end_index]
        rms_yy = [i *10**3 for i in dataset_obj.rms_yy][:end_index]

        max_x = [i *10**3 for i in dataset_obj.max_x][:end_index]
        max_xx = [i *10**3 for i in dataset_obj.max_xx][:end_index]

        max_y = [i *10**3 for i in dataset_obj.max_y][:end_index]
        max_yy = [i *10**3 for i in dataset_obj.max_yy][:end_index]


        alpha_x = dataset_obj.alpha_x[:end_index]
        alpha_y = dataset_obj.alpha_y[:end_index]
        alpha_z = dataset_obj.alpha_z[:end_index]

        beta_x = dataset_obj.beta_x[:end_index]
        beta_y = dataset_obj.beta_y[:end_index]
        beta_z = dataset_obj.beta_z[:end_index]

        loss = dataset_obj.loss[:end_index]
        # phi = dataset_obj.phi[:end_index]
        # phi_phi = dataset_obj.phi_phi[:end_index]
        # BaseMassInMeV = dataset_obj.BaseMassInMeV
        # freq = dataset_obj.freq
        #
        # # for i in range(len(dataset_obj.ek)):
        # #     gammaaaa = dataset_obj.ek[i] / BaseMassInMeV + 1
        # #     beta.append(math.sqrt(1 - 1.0 / gammaaaa / gammaaaa))
        # #     v = dataset_obj.rms_z[i] / (beta[-1] * C_light) * freq * 360
        # #     # rms_z.append(dataset_obj.rms_z[i] / (beta[-1] * C_light) * freq * 360)
        # #     # rms_zz.append(-1 * (dataset_obj.rms_z[i] / (beta[-1] * C_light) * freq * 360))
        # #     rms_z.append(v)
        # #     rms_zz.append(-1 * v)
        # #
        # # for i in range(len(data)):
        # #     gammaaaa = data[i][0] / BaseMassInMeV + 1
        # #     beta.append(math.sqrt(1 - 1.0 / gammaaaa / gammaaaa))
        # #     rms_z.append(data[i][20] / (beta[-1] * C_light) * freq * 360)
        # #     rms_zz.append(-1 * (data[i][20] / (beta[-1] * C_light) * 162.5e6 * 360))



        if self.picture_name == 'loss':
            self.x = z
            self.y = loss
            self.xlabel = "z(m)"
            self.ylabel = "loss"
            self.ylim = [-max(loss)-100, max(loss) + 100]


        elif self.picture_name == 'emittance_x':
            self.x = z
            self.y = emit_x


            self.xlabel = "z(m)"
            self.ylabel = "Emit_x(pi*mm*mrad)"


        elif self.picture_name == 'emittance_y':
            self.x = z
            self.y = emit_y

            self.xlabel = "z(m)"
            self.ylabel = "Emit_y(pi*mm*mrad)"



        elif self.picture_name == 'emittance_z':
            self.x = z
            self.y = emit_z

            self.xlabel = "z(m)"
            self.ylabel = "Emit_z(pi*mm*mrad)"


        elif self.picture_name == 'rms_x':
            self.x = z
            # print(z)
            # print(rms_x)
            # print(len(rms_x))

            self.y = [rms_x, rms_xx]

            self.xlabel = "z(m)"
            self.ylabel = "RMS_x Size(mm)"

            self.colors = ['r', 'r']
            self.ylim = [ -2 * np.max(np.array(rms_x)),  2 * np.max(np.array(rms_x)) ]
            print(self.ylim)

        elif self.picture_name == 'rms_y':
            self.x = z
            self.y = [rms_y, rms_yy]

            self.xlabel = "z(m)"
            self.ylabel = "RMS_y Size(mm)"
            self.colors = ['b', 'b']


        elif self.picture_name == 'rms_xy':
            self.x = z
            self.y = [rms_x, rms_xx, rms_y, rms_yy]

            self.xlabel = "z(m)"
            self.ylabel = "RMS_xy Size(mm)"

            self.labels = ['x', None, 'y', None]
            self.colors = ['r', 'r', 'b', 'b']
            self.set_legend = 1


        elif self.picture_name == 'max_x':
            self.x = z
            self.y = [max_x, max_xx]

            self.xlabel = "z(m)"
            self.ylabel = "Max_x Size(mm)"

            self.colors = ['r', 'r']


        elif self.picture_name == 'max_y':
            self.x = z
            self.y = [max_y, max_yy]
            self.xlabel = "z(m)"
            self.ylabel = "Max_y Size(mm)"
            self.colors = ['b', 'b']


        elif self.picture_name == 'max_xy':
            self.x = z
            self.y = [max_x, max_xx, max_y, max_yy]

            self.xlabel = "z(m)"
            self.ylabel = "Max_xy Size(mm)"

            self.labels = ['x', None, 'y', None]
            self.colors = ['r', 'r', 'b', 'b']
            self.set_legend = 1


        # elif self.picture_name == 'phi':
        #     self.x = z
        #     self.y = phi
        #
        #     self.xlabel = "z(m)"
        #     v_freq = freq/(10**6)
        #     self.ylabel = f"P(deg)({v_freq}MHz)"



        elif self.picture_name == 'energy':
            self.x = z
            self.y = ek

            self.xlabel = "z(m)"
            self.ylabel = "Ek(MeV)"

        elif self.picture_name == 'alpha_x':
            self.x = z
            self.y = alpha_x

            self.xlabel = "z(m)"
            self.ylabel = r"$\alpha_{x}$"

        elif self.picture_name == 'beta_x':
            self.x = z
            self.y = beta_x

            self.xlabel = "z(m)"
            self.ylabel = r"$\beta_{x}$" + "(mm/" + r"$\pi$ mrad)"

        elif self.picture_name == 'beta_y':
            self.x = z
            self.y = beta_y

            self.xlabel = "z(m)"
            self.ylabel = r"$\beta_{y}$" + "(mm/" + r"$\pi$ mrad)"

        elif self.picture_name == 'beta_z':
            self.x = z
            self.y = beta_z

            self.xlabel = "z(m)"
            self.ylabel = r"$\beta_{z}$" + "(mm/" + r"$\pi$ mrad)"

        elif self.picture_name == 'beta_xyz':
            self.x = z
            self.y = [beta_x, beta_y, beta_z]

            self.xlabel = "z(m)"
            self.ylabel = r"$\beta_{xyz}$" + "(mm/" + r"$\pi$ mrad)"

            self.labels = [r"$\beta_{x}$", r"$\beta_{y}$", r"$\beta_{z}$"]
            self.set_legend = 1

        return self.x, self.y

    def need_element(self, aper=1):

        obj_compound = CompoundShape()
        patch_list = []

        #获取lattice参数
        lattice_res = LatticeParameter(self.lattice_mulp_path)
        lattice_res.get_parameter()

        for i in range(len(lattice_res.v_name)):
            aperture = [i *1000 for i in lattice_res.aperture]


            aperture_fake = 1

            element = ''
            if lattice_res.v_name[i] == "field" and lattice_res.phi_syn[i]:
                element = "cav"
            elif lattice_res.v_name[i] == "field" and not lattice_res.phi_syn[i]:
                element = "sol"

            if element:
                square_origin = [lattice_res.v_start[i], -0.5 * aperture_fake]
                patch_list.append(obj_compound.create_shapes(square_origin, lattice_res.v_len[i], aperture_fake, element))


        aperture_up = [i for i in aperture]
        aperture_up += [aperture_up[-1]]
        print(aperture_up)

        aperture_down = [-i for i in aperture]
        aperture_down += [aperture_down[-1]]

        aper_x = lattice_res.v_start + [lattice_res.v_start[-1] + lattice_res.v_len[-1]]
        print(aper_x)


        self.x = [self.x]*len(self.y) + [aper_x] * 2

        self.y = self.y + [aperture_up] + [aperture_down]

        self.labels = self.labels + [None, None]
        self.colors += ["black", "black"]

        self.patch_list = patch_list
        self.ylim = []

        if aper == 0:
            self.x = self.x[:-2]

            self.y = self.y[:-2]
            self.labels = self.labels[:-2]
            self.colors = self.colors[:-2]

if __name__ == "__main__":
    project_path = r"C:\Users\shliu\Desktop\test_avas_qt\fileld_ciads"
    dataset_path = r"E:\using\test_avas_qt\fileld_ciads\OutputFile\DataSet.txt"
    a = PlotDataSet(project_path=None,  picture_name = 'rms_xy', dataset_path=dataset_path)
    a.get_x_y()
    # a.need_element(aper=1)
    a.run(show_=1)

    # a = PlotDataSet(project_path=None,  picture_name = 'alpha_x', dataset_path=dataset_path)
    # a.get_x_y()
    # # a.need_element(aper=1)
    # a.run(show_=1)
    #
