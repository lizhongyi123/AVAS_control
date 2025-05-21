import sys

from core.MultiParticle import MultiParticle

item = {"project_path": ""}
m1obj = MultiParticle(item)

from utils.beamconfig import BeamConfig
from utils.inputconfig import InputConfig
from utils.iniconfig import IniConfig
from utils.latticeconfig import LatticeConfig
import os
import utils.exception as exce
from apis.basic_api.api import basic_mulp, basic_env, match_twiss, circle_match, \
    err_dyn, err_stat, err_stat_dyn
from utils.tool import format_output
from apis.qt_api.judge_lattice import JudgeLattice

class SimMode():
    def __init__(self, item):
        self.item = item
        self.project_path =item.get('projectPath')
        self.ini_path = os.path.join(self.project_path, "InputFile", "ini.ini")
        self.beam_path = os.path.join(self.project_path, "InputFile", "beam.txt")
        self.input_path = os.path.join(self.project_path, "InputFile", "input.txt")
        self.lattice_mulp_path = os.path.join(self.project_path, "InputFile", "lattice_mulp.txt")
        self.runsignal = os.path.join(self.project_path, "OutputFile", 'runsignal.txt')


    def write_signal(self, info):
        signa_path = os.path.join(self.project_path, "OutputFile", "signal.txt")
        with open(signa_path, 'w') as f:
            f.write(str(info))

    def write_sim_error(self, info):
        tmp_dir = os.path.join(self.project_path, "OutputFile", "tmp")

        os.makedirs(tmp_dir, exist_ok=True)  # 确保 tmp 目录存在

        errordata_path = os.path.join(tmp_dir, "errordata.txt")

        with open(errordata_path, 'w') as f:
            f.write(str(info))

    def run(self):
        #检查
        self.write_signal(1)
        try:

            #判断模拟类型并进行模拟
            ini_obj = IniConfig()
            ini_info = ini_obj.create_from_file(self.item)

            ini_info = ini_info["data"]["iniParams"]
            base_mode = ini_info["input"]["sim_type"]
            device = ini_info["input"]["device"]

            match_mode = [
                ini_info["match"]["cal_input_twiss"],
                ini_info["match"]["match_with_twiss"],
                ini_info["match"]["use_initial_value"],
            ]

            err_mode = ini_info["error"]["error_type"]
            err_seed = ini_info["error"]["seed"]

            #检查类型


            field_path = ini_info["project"]["fieldSource"]

            #如果field_path是空的
            if not field_path:
                field_path = None

            item = {
                "project_path": self.project_path,
                "field_path": field_path,
                "seed": err_seed,
                "device": device,
            }
            # print(item)
            # sys.exit()
            if base_mode == "mulp":
                if err_mode == "stat":
                    err_stat(**item)

                elif err_mode == "dyn":
                    err_dyn(**item)

                elif err_mode == "stat_dyn":
                    err_stat_dyn(**item)
                else:
                    basic_mulp(**item)

            self.write_signal(2)


        except Exception as e:
            self.write_signal(2)
            raise Exception(str(e))
        # elif base_mode == "env":
        #     if ini_info['match']["cal_input_twiss"] == 1:
        #         circle_match(self.project_path)
        #     elif ini_info['match']["match_with_twiss"] == 1 and ini_info['match']["use_initial_value"] == 0:
        #         match_twiss(self.project_path, 0)
        #     elif ini_info['match']["match_with_twiss"] == 1 and ini_info['match']["use_initial_value"] == 1:
        #         match_twiss(self.project_path, 1)
        #     else:
        #         basic_env(self.project_path)


        jobInfo_dict = {
            'jobInfo': {'projectPath': self.project_path,
                    'jobName': '',
                    'jobId': 0}
        }

        kwargs = {}
        kwargs.update(jobInfo_dict)
        output = format_output(**kwargs)
        return output


if __name__ == '__main__':
    # path = r"C:\Users\anxin\Desktop\test_schedule\cafe_avas"
    path = r"C:\Users\anxin\Desktop\gpu_jiqun\cafe_avas"

    item = {"projectPath": path}
    obj = SimMode(item)
    res = obj.run()
    print(res)