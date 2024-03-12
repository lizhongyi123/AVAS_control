import numpy as np
import matplotlib.pyplot as plt
import math
from aftertreat.picture.initialplot import PicturePlot_2D, CompoundShape
from utils.readfile import read_txt, read_dst
from dataprovision.datasetparameter import DatasetParameter
from dataprovision.latticeparameter import LatticeParameter

# [ 'emittance_x', 'emittance_y', 'emittance_z',
# 'longitudinal_phase', ]
class PlotDataSet(PicturePlot_2D):
    """
    dataset文件的可视化
    """
    def __init__(self, project_path, picture_name):
        super().__init__()
        self.picture_name = picture_name
        self.BaseMassInMeV = 0
        self.freq = 0

        self.project_path = project_path
        self.beam_path = self.project_path + r'\InputFile' + r'\beam.txt'
        self.lattice_path = self.project_path + r'\InputFile' + r'\lattice.txt'
        self.input_path = self.project_path + r'\InputFile' + r'\input.txt'
        self.dataset_path = self.project_path + r'\OutputFile' + r'\DataSet.txt'



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

    # def get_mass_freq(self, BaseMassInMeV, freq):
    #     self.BaseMassInMeV = BaseMassInMeV
    #     self.freq = freq
    #     return None

    def get_x_y(self):
        inFileName = self.dataset_path

        C_light = 299792458  # 光速 常数

        BaseMassInMeV, freq = self.get_mass_freq()


        dataset_obj = DatasetParameter(self.dataset_path)
        dataset_obj.get_parameter()

        z = dataset_obj.z  # 束团纵向位置
        ek = dataset_obj.ek  # 束团平均能量

        beta = []

        emit_x = [i * 10**6 for i in dataset_obj.emit_x]
        emit_y = [i * 10**6 for i in dataset_obj.emit_y]
        emit_z = [i * 10**6 for i in dataset_obj.emit_z]

        rms_x = [i *10**3 for i in dataset_obj.rms_x]  #单位变成mm
        rms_xx = [i *10**3 for i in dataset_obj.rms_xx]

        rms_y = [i *10**3 for i in dataset_obj.rms_y]
        rms_yy = [i *10**3 for i in dataset_obj.rms_yy]

        max_x = [i *10**3 for i in dataset_obj.max_x]
        max_xx = [i *10**3 for i in dataset_obj.max_xx]

        max_y = [i *10**3 for i in dataset_obj.rms_y]
        max_yy = [i *10**3 for i in dataset_obj.rms_yy]

        rms_z = []
        rms_zz = []

        beta_x = dataset_obj.beta_x
        beta_y = dataset_obj.beta_y
        beta_z = dataset_obj.beta_z

        loss = dataset_obj.loss

        for i in range(len(dataset_obj.ek)):
            gammaaaa = dataset_obj.ek[i] / BaseMassInMeV + 1
            beta.append(math.sqrt(1 - 1.0 / gammaaaa / gammaaaa))
            rms_z.append(dataset_obj.rms_z[i] / (beta[-1] * C_light) * freq * 360)
            rms_zz.append(-1 * (dataset_obj.rms_z[i] / (beta[-1] * C_light) * 162.5e6 * 360))

        # for i in range(len(data)):
        #     gammaaaa = data[i][0] / BaseMassInMeV + 1
        #     beta.append(math.sqrt(1 - 1.0 / gammaaaa / gammaaaa))
        #     rms_z.append(data[i][20] / (beta[-1] * C_light) * freq * 360)
        #     rms_zz.append(-1 * (data[i][20] / (beta[-1] * C_light) * 162.5e6 * 360))

        obj_compound = CompoundShape()
        patch_list = []

        #获取lattice参数
        lattice_res = LatticeParameter(self.lattice_path)
        lattice_res.get_parameter()
        for i in range(len(lattice_res.v_name)):
            aperture = lattice_res.aperture[i] * 1000


            element = ''
            if lattice_res.v_name[i] == "field" and lattice_res.phi_syn[i]:
                element = "cav"
            elif lattice_res.v_name[i] == "field" and not lattice_res.phi_syn[i]:
                element = "sol"

            if element:

                square_origin = [lattice_res.v_start[i], -0.5 * aperture]
                patch_list.append(obj_compound.create_shapes(square_origin, lattice_res.v_len[i], aperture, element))






        if self.picture_name == 'loss':
            self.x = z
            self.y = loss

            self.xlabel = "z(m)"
            self.ylabel = "loss"
            self.ylim = [-max(loss)-1, max(loss) + 1]


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
            self.patch_list =patch_list

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


        elif self.picture_name == 'rms_z':
            self.x = z
            self.y = rms_z

            self.xlabel = "z(m)"
            self.ylabel = "P(deg)(162.5MHz)"



        elif self.picture_name == 'energy':
            self.x = z
            self.y = ek

            self.xlabel = "z(m)"
            self.ylabel = "Ek(MeV)"

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



if __name__ == "__main__":
    a = PlotDataSet(r'D:\重要程序\程序\画dataset\1',  'rms_xy')
    a.get_x_y()
    a.run(show_=1)

