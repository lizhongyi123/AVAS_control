import sys
import time

sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')

from core.AVASEngine import AVASEngine
import os
from utils.beamconfig import BeamConfig
from utils.inputconfig import InputConfig
from utils.latticeconfig import LatticeConfig
import multiprocessing
class AVAS():
    """
    多粒子模拟
    """
    def __init__(self, project_path):   #*arg **kwargs #dllpath写死
        self.project_path = project_path

        # #该处目前还存在不同选择，即全传输和部分传输
        # self.input = projectpath + r'InputFile\input.txt'
        # self.lattice = projectpath + r'InputFile\lattice.txt'
        # self.beam = projectpath + r'InputFile\beam.txt'
        #
        #将整个问见转换成结构体
        # self.input_config = InputConfig(self.input)
        # self.beam_config = BeamConfig(self.input)
        # self.lattice_config = LatticeConfig(self.input)
        #
        #

        self.AVAS_engine = AVASEngine()

    #该函数，目前的新选择为部分传输，即什么参数改了传什么
    # def run(self, input_change: dict = None, beam_change: dict = None, lattice_change: dict = None):

        #input_change = self.input_config.format_change()
        #beam_change = self.beam_config.format_change()
        #lattice_change = self.lattice_config.format_change()

        # inputfilepath = self.projectpath + r'\InputFile'
        # outputfilePath = self.projectpath + r'\OutputFile'
        # res_tmp = self.AVAS_engine.get_path(inputfilepath, outputfilePath)
        #
    #
    #     res_tmp = self.avas_engine.get_path(inputfilepath, outputfilePath)
    #
    #     res = self.engine.main_agent(input_change, beam_change, lattice_change)
    #
    #     return res

    def run(self, input_file='InputFile', output_file='OutputFile'):

        inputfilepath = os.path.join(self.project_path, input_file)
        outputfilePath = os.path.join(self.project_path, output_file)
        print(inputfilepath)
        print(outputfilePath)

        res_tmp = self.AVAS_engine.get_path(inputfilepath, outputfilePath)

        res = self.AVAS_engine.main_agent(1)
        print(res)
        # if res == 1:
        #     raise Exception('error')

        return res

if __name__ == "__main__":

    project_path = r"C:\Users\anxin\Desktop\test_acct"
    obj = AVAS(project_path)
    obj.run()
    # for i in range(3):
    #     # process = multiprocessing.Process(target=worker,
    #     #                                   args=( project_path, ))
    #     #
    #     # process.start()  # 启动子进程
    #     # process.join()  # 等待子进程运行结束
    #     worker(project_path)
    #     print(i)