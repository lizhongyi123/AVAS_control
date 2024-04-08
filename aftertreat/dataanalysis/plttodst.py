
from dataprovision.beamset import BeamsetParameter
import math
from global_varible import c_light, Pi
from utils.readfile import read_dst
import struct
import os

class Plttodst():
    def __init__(self, pltpath):
        self.plt_path = pltpath

    def to_dst_variable_z(self, num):
        obj = BeamsetParameter(self.plt_path)
        obj.get_one_parameter(num)

        np = obj.numofp
        Ib = obj.Ib
        freq = obj.freq *10**6 #变成Hz
        print(freq)
        BaseMassInMeV = obj.BaseMassInMeV

        part_dict = obj.one_step_dict
        part_list = obj.one_step_list

        part_dstform = []
        for particle in part_list:
            if particle[5] > 0 and (particle[6] ==0 or particle[6]==2):

                p2 = particle[1]**2 + particle[3]**2 + particle[5]**2
                beta = math.sqrt(p2/(1 + p2))
                v = beta * c_light
                gamma = 1/math.sqrt(1-beta**2)

                beta_z = math.sqrt(particle[5]**2/(1 + particle[5]**2))
                v_z = beta_z * c_light

                v_x = (particle[1]/ particle[5]) * v_z
                v_y = (particle[3]/ particle[5]) * v_z


                t = -(particle[4] / v_z)

                x = (particle[0] + v_x * t) * 100
                xx = particle[1] / particle[5]
                y = (particle[2] + v_y * t) * 100
                yy = particle[3] / particle[5]
                phi = t * 2 * Pi * freq
                E = (gamma - 1) * BaseMassInMeV

                tlist = [x, xx, y, yy, phi, E]

                part_dstform.append(tlist)

        outputfile = os.path.dirname(self.plt_path)
        dst_name = "plt_step_" + str(part_dict["index"]) + ".dst"
        outputfile_one_step = os.path.join(outputfile, dst_name)
        print(outputfile_one_step)

        with open(outputfile_one_step, 'wb') as data0utFile:
            try:
                data0utFile.write(struct.pack('c', b'\x7D'))  # skip1
                data0utFile.write(struct.pack('c', b'\x64'))  # skip2

                data0utFile.write(struct.pack('i', np))
                data0utFile.write(struct.pack('d', Ib))  # mA
                data0utFile.write(struct.pack('d', freq/10**6))  # MHz

                data0utFile.write(struct.pack('c', b'\x7D'))

                for i in range(np):
                    for j in range(6):
                        data0utFile.write(struct.pack('d', part_dstform[i][j]))

                data0utFile.write(struct.pack('d', BaseMassInMeV))  # Mev

            except IOError:
                print("输出错误")



    def to_dst_variable_t(self, num):
        pass
if __name__ == "__main__":

    project_path = r"C:\Users\anxin\Desktop\example3"
    beamset_path = os.path.join(project_path, "OutputFile", "BeamSet.plt")

    obj = Plttodst(beamset_path)
    obj.to_dst_variable_z(610)


