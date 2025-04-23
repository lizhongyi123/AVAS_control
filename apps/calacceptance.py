
import numpy as np
import os
import pandas as pd
import numpy
from dataprovision.beamset import BeamsetParameter
import math
from global_varible import c_light, Pi
from dataprovision.latticeparameter import LatticeParameter
import matplotlib.pyplot as plt


class Acceptance():
    def __init__(self, project_path = None):
        self.project_path = project_path
        self.plt_path = os.path.join(project_path, "OutputFile", "BeamSet.plt")
        if project_path:
            self.latttice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')

    def get_para(self, num):
        obj = BeamsetParameter(self.plt_path)
        obj.get_one_parameter(num)

        self.np = obj.numofp
        self.Ib = obj.Ib
        self.freq = obj.freq *10**6 #单位Hz
        self.BaseMassInMeV = obj.BaseMassInMeV

        part_dict = obj.one_step_dict
        part_list = obj.one_step_list

        exist_part = []
        all_part = []

        all_vz = []

        #计算平均速度
        if num == 0:
            for particle in part_list:
                beta_z = math.sqrt(particle[5] ** 2 / (1 + particle[5] ** 2))
                v_z = beta_z * c_light
                if num == 0:
                    particle[4] = (0 + particle[4])
                all_vz.append(v_z)



        lattice_obj = LatticeParameter(self.latttice_mulp_path)
        lattice_obj.get_parameter()
        lattice_total_length = lattice_obj.total_length

        if num == -1:
            for particle in part_list:
                particle[4] = (part_dict['location'] + particle[4])

                if (particle[6] == 0 or particle[6] == 2) and particle[4] >= lattice_total_length:
                    beta_z = math.sqrt(particle[5] ** 2 / (1 + particle[5] ** 2))
                    v_z = beta_z * c_light
                    all_vz.append(v_z)




        average_z = np.mean(all_vz)


        # for i in part_list:
        #     print(i)



        if part_dict["tpye"] == 0:
            if num == 0:
                for particle in part_list:
                # if particle[6] == 0 or particle[6] == 2:
                    p2 = particle[1]**2 + particle[3]**2 + particle[5]**2
                    beta = math.sqrt(p2/(1 + p2))
                    v = beta * c_light
                    gamma = 1/math.sqrt(1-beta**2)

                    beta_z = math.sqrt(particle[5]**2/(1 + particle[5]**2))
                    v_z = beta_z * c_light


                    v_x = (particle[1]/ particle[5]) * v_z
                    v_y = (particle[3]/ particle[5]) * v_z


                    t = -(particle[4] / v_z)

                    x = (particle[0] + v_x * t) * 1000  #mm
                    xx = particle[1] / particle[5] * 1000
                    y = (particle[2] + v_y * t)* 1000
                    yy = particle[3] / particle[5]* 1000

                    # z = (part_dict['location'] + particle[4])* 1000
                    z = particle[4]* 1000

                    zz = (v_z - average_z)/v_z * 1000

                    phi = t * 2 * Pi * self.freq /Pi * 180  #度
                    E = (gamma - 1) * self.BaseMassInMeV  #MeV


                    tlist = [x, xx, y, yy, z, zz, phi, E, 0]

                    # exist_part.append(tlist)
                    all_part.append(tlist)


            if num == -1:
                for particle in part_list:
                    if (particle[6] == 0 or particle[6] == 2) and particle[4] >= lattice_total_length:
                        p2 = particle[1] ** 2 + particle[3] ** 2 + particle[5] ** 2
                        beta = math.sqrt(p2 / (1 + p2))
                        v = beta * c_light
                        gamma = 1 / math.sqrt(1 - beta ** 2)

                        beta_z = math.sqrt(particle[5] ** 2 / (1 + particle[5] ** 2))
                        v_z = beta_z * c_light

                        v_x = (particle[1] / particle[5]) * v_z
                        v_y = (particle[3] / particle[5]) * v_z

                        t = -(particle[4] / v_z)

                        x = (particle[0] + v_x * t) * 1000  # mm
                        xx = particle[1] / particle[5] * 1000
                        y = (particle[2] + v_y * t) * 1000
                        yy = particle[3] / particle[5] * 1000

                        # z = (part_dict['location'] + particle[4])* 1000
                        z = particle[4] * 1000

                        zz = (v_z - average_z) / v_z * 1000

                        phi = t * 2 * Pi * self.freq / Pi * 180
                        E = (gamma - 1) * self.BaseMassInMeV  # MeV

                        tlist = [x, xx, y, yy, z, zz, phi, E, 0]

                        # exist_part.append(tlist)
                        all_part.append(tlist)
                    else:
                        all_part.append([1] * 9)



        return all_part


    def cal_accptance(self, kind):

        in_dis = self.get_para(0)
        out_dis = self.get_para(-1)


        # pd.set_option('display.max_columns', None)
        in_dis = pd.DataFrame(in_dis, columns=['x', 'xx', 'y', 'yy', 'z', 'zz', 'phi', 'E', 'loss'])
        out_dis = pd.DataFrame(out_dis, columns=['x', 'xx', 'y', 'yy', 'z', 'zz', 'phi', 'E', 'loss'])

        w = in_dis["E"].mean()

        m = self.BaseMassInMeV

        gamma = w / m + 1
        beta = (1 - 1 / gamma ** 2) ** 0.5
        btgm = gamma * beta

        in_dis["E"] -= w
        # print(in_dis)


        #丢失的粒子
        loss_particles = in_dis[out_dis["loss"] == 1].copy()
        print(loss_particles)
        breakpoint()
        loss_particles_rows, _ = loss_particles.shape

        if loss_particles_rows == 0:
            raise Exception("All particels passed  through the lattice, avas can not calculate acceptance.")

        if kind == 0:
            #x方向
            emit_norm, t_alpha, t_beta, t_gamma = self.twiss(in_dis["x"], in_dis["xx"], btgm)



            loss_particles.loc[:,'ellipse'] = (t_gamma * loss_particles["x"] ** 2 +
                             2 * t_alpha * loss_particles["x"] * loss_particles["xx"] +
                             t_beta * loss_particles["xx"] ** 2)

            loss_min_emit = loss_particles['ellipse'].min()

            min_loss_index = loss_particles['ellipse'].idxmin()

            # 找到对应的 z 和 zz
            x_min = loss_particles.loc[min_loss_index, 'x']
            xx_min = loss_particles.loc[min_loss_index, 'xx']

            norm_emit = loss_min_emit * btgm

            self.t_alpha = t_alpha
            self.t_beta = t_beta
            self.t_gamma = t_gamma
            self.loss_particles = loss_particles
            return loss_min_emit, norm_emit, x_min, xx_min

        elif kind == 1:
            #y方向
            emit_norm, t_alpha, t_beta, t_gamma = self.twiss(in_dis["y"], in_dis["yy"], btgm)

            print(emit_norm, t_alpha, t_beta, t_gamma )

            loss_particles.loc[:,'ellipse'] = (t_gamma * loss_particles["y"] ** 2 +
                             2 * t_alpha * loss_particles["y"] * loss_particles["yy"] +
                             t_beta * loss_particles["yy"] ** 2)

            loss_min_emit = loss_particles['ellipse'].min()

            min_loss_index = loss_particles['ellipse'].idxmin()

            # 找到对应的 z 和 zz
            y_min = loss_particles.loc[min_loss_index, 'y']
            yy_min = loss_particles.loc[min_loss_index, 'yy']

            norm_emit = loss_min_emit * btgm

            self.t_alpha = t_alpha
            self.t_beta = t_beta
            self.t_gamma = t_gamma
            self.loss_particles = loss_particles

            return loss_min_emit, norm_emit, y_min, yy_min



        elif kind == 2:
            zbtgm = gamma**3 * beta
            emit_norm, t_alpha, t_beta, t_gamma = self.twiss(in_dis["z"], in_dis["zz"], zbtgm)
            print(emit_norm, t_alpha, t_beta, t_gamma)


            loss_particles.loc[:,'ellipse'] = (t_gamma * loss_particles["z"] ** 2 +
                             2 * t_alpha * loss_particles["z"] * loss_particles["zz"] +
                             t_beta * loss_particles["zz"] ** 2)

            loss_min_emit = loss_particles['ellipse'].min()

            min_loss_index = loss_particles['ellipse'].idxmin()

            # 找到对应的 z 和 zz
            z_min = loss_particles.loc[min_loss_index, 'z']
            zz_min = loss_particles.loc[min_loss_index, 'zz']

            norm_emit = loss_min_emit * btgm

            self.t_alpha = t_alpha
            self.t_beta = t_beta
            self.t_gamma = t_gamma
            self.loss_particles = loss_particles

            return loss_min_emit, norm_emit, z_min, zz_min

        elif kind == 3:
            _, t_alpha, t_beta, t_gamma = self.twiss(in_dis["phi"], in_dis["E"] , btgm)

            print(t_alpha, t_beta, t_gamma)

            loss_particles.loc[:,'ellipse'] = (t_gamma * loss_particles["phi"] ** 2 +
                             2 * t_alpha * loss_particles["phi"] * loss_particles["E"] +
                             t_beta * loss_particles["E"] ** 2)

            loss_min_emit = loss_particles['ellipse'].min()


            min_loss_index = loss_particles['ellipse'].idxmin()

            # 找到对应的 z 和 zz
            phi_min = loss_particles.loc[min_loss_index, 'phi']
            E_min = loss_particles.loc[min_loss_index, 'E'] + w

            self.t_alpha = t_alpha
            self.t_beta = t_beta
            self.t_gamma = t_gamma
            self.loss_particles = loss_particles

            return loss_min_emit, None, phi_min, E_min,

    def twiss(self, x, y, btgm, ):
        x_sigma = numpy.average(x ** 2)
        y_sigma = numpy.average(y ** 2)
        x_y_corr = numpy.average(x * y)
        emit = (x_sigma * y_sigma - x_y_corr ** 2) ** 0.5
        print("emit", emit)
        beta = x_sigma / emit
        gamma = y_sigma / emit
        alpha = - x_y_corr / emit
        emit_norm = btgm * emit
        return emit_norm, alpha, beta, gamma


if __name__ == "__main__":
    project_path = r"C:\Users\shliu\Desktop\chu\chu2"
    obj = Acceptance(project_path)
    obj.cal_accptance(3)