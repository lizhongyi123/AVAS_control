import sys
import time
import platform
import subprocess
import os
import re
from os import device_encoding

# sys.path.append(r'E:\AVAS_CONTROL\AVAS_control')

from core.MultiParticleEngine import MultiParticleEngine
import multiprocessing

from utils.inputconfig import InputConfig
from utils.beamconfig import BeamConfig
from utils.readfile import read_txt
from utils.tool import write_to_txt, convert_dic2lis
from sim_gpu.pic import *

class MultiParticle():
    """
    多粒子模拟
    """
    def __init__(self, item):  # *arg **kwargs #dllpath写死
        self.project_path = item["project_path"]
        self.input_file = item.get("input_file")
        self.output_file = item.get("output_file")
        self.field_path = item.get("field_path")
        self.errorlog_path = item.get("errorlog_path")
        self.multiparticle_engine = item.get("mulp_engine")
        self.device = item.get("device")

        if self.device in [None, ""]:
            self.device = "cpu"

        if self.input_file is None:
            self.input_file = os.path.join(self.project_path, "InputFile")
        if self.output_file is None:
            self.output_file = os.path.join(self.project_path, "OutputFile")

        if self.field_path == None:
            self.field_path = self.input_file

        if self.errorlog_path is None:
            self.errorlog_path = os.path.join(self.output_file, "ErrorLog.txt")

        if self.device  == "cpu":
            if self.multiparticle_engine is None:
                self.multiparticle_engine = MultiParticleEngine()



    def run(self):
        if self.device == "cpu":
            print(38, self.input_file, self.output_file, self.field_path)
            if os.path.exists(self.errorlog_path):
                os.remove(self.errorlog_path)

            res_tmp = self.multiparticle_engine.get_path(self.input_file, self.output_file, self.field_path)

            res = self.multiparticle_engine.main_agent(1)

            if res == 1:
                # raise Exception(f'模拟错误，请查询OutputFile中的ErrorLog.txt')

                error = self.check_error_file(self.errorlog_path)
                raise Exception(f'{error}')
            elif res == 2:
                # raise Exception(f'模拟错误，请查询OutputFile中的ErrorLog.txt')
                error = self.check_error_file(self.errorlog_path)
                raise Exception(f'{error}')
        elif self.device == "gpu":
            #重写beam和input
            generate_input_gpu(self.input_file,  self.output_file, self.field_path)
            generate_beam_gpu(self.input_file, self.output_file, self.field_path)

            input_txt_gpu_path = os.path.join(self.input_file, "input_gpu.txt")
            beam_txt_gpu_path = os.path.join(self.input_file, "beam_gpu.txt")
            lattice_txt_gpu_path = os.path.join(self.input_file, "lattice.txt")

            item  = {"project_path": self.project_path,
                     "input_file": self.input_file,

                     "input_path":input_txt_gpu_path,
                     "beam_path": beam_txt_gpu_path,
                     "lattice_path": lattice_txt_gpu_path,
                     }

            simulator = SimulationRunner(item)
            simulator.run()

            res= 0


        return res

    def stop(self):
        res = self.multiparticle_engine.main_agent(2)
        print("停止", res)


    def check_error_file(self, ErrorLog):
        with open(ErrorLog, 'r') as file:
            text = file.read()

        # error_parts = re.findall(r'[A-Za-z\s:,.]+', text)[3]
        error_parts = text.split('     ')[1]
        return error_parts


def generate_input_gpu(input_file, output_file, field_path):
    input_txt = os.path.join(input_file, "input.txt")
    ori_input_res = read_txt(input_txt, out="list", case_sensitive= True)
    ori_input_res.append(["outputpath", output_file])
    ori_input_res.append(["fieldpath", field_path])

    ori_input_res.append(["numofgrid", 24, 24, 24])
    ori_input_res.append(["MeshRms", 4, 4, 4])
    ori_input_res.append(["statOutputInterval", 1])

    input_txt_gpu = os.path.join(input_file, "input_gpu.txt")
    write_to_txt(input_txt_gpu, ori_input_res)


def generate_beam_gpu(input_file, output_file, field_path):
    beam_txt = os.path.join(input_file, "beam.txt")
    ori_beam_res = read_txt(beam_txt, out="list", case_sensitive= True)

    for i in ori_beam_res:
        if i[0] == "kneticenergy":
            i.append(0)

    beam_txt_gpu = os.path.join(input_file, "beam_gpu.txt")
    write_to_txt(beam_txt_gpu, ori_beam_res)

def basic_mulp(project_path):
    obj = MultiParticle(project_path)

    res = obj.run()


if __name__ == "__main__":
    
    item = {'project_path': r'C:\Users\anxin\Desktop\gpu_jiqun\cafe_avas',
            "device": "gpu"
            }
    obj = MultiParticle(item)
    obj.run()



