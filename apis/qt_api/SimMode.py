
from utils.beamconfig import BeamConfig
from utils.inputconfig import InputConfig
from utils.iniconfig import IniConfig
from utils.latticeconfig import LatticeConfig
import os
import utils.exception as exce
from apis.basic_api.api import basic_mulp, basic_env, match_twiss, circle_match, \
    err_dyn, err_stat, err_stat_dyn
class SimMode():
    def __init__(self, project_path):
        self.project_path = project_path
        self.ini_path = os.path.join(path, "InputFile", "ini.ini")
        self.beam_path = os.path.join(project_path, "InputFile", "beam.txt")
        self.input_path = os.path.join(project_path, "InputFile", "input.txt")
        self.lattice_mulp_path = os.path.join(project_path, "InputFile", "lattice_mulp.txt")

    def file_check(self):
        #检查input文件
        input_config = InputConfig()
        input_config.validate_run(self.input_path)

        #检查beam文件
        beam_config = BeamConfig()
        beam_config.validate_run(self.beam_path)



    def run(self):
        self.file_check()
        #判断模拟类型并进行模拟
        ini_obj = IniConfig()
        ini_info = ini_obj.creat_from_file(self.ini_path)

        base_mode = ini_info["input"]["!sim_type"]
        print(base_mode)

        match_mode = [
            ini_info["match"]["cal_input_twiss"],
            ini_info["match"]["match_with_twiss"],
            ini_info["match"]["use_initial_value"],
        ]

        err_mode = ini_info["error"]["error_type"]
        err_seed = ini_info["error"]["seed"]

        #检查类型
        if base_mode not in ["mulp", "env"]:
            raise exce.ValueRangeError('sim type', ["mulp", "env"], base_mode)

        all_error_type =["stat", "dyn", "stat_dyn", "undefined"]
        if err_mode not in all_error_type:
            raise exce.ValueRangeError('error type', all_error_type, err_mode)


        if base_mode == "mulp":
            if err_mode == "stat":
                err_stat(self.project_path, err_seed, if_normal=1)
            elif err_mode == "dyn":
                err_dyn(self.project_path, err_seed, if_normal=1)
            elif err_mode == "stat_dyn":
                err_stat_dyn(self.project_path, err_seed, if_normal=1)
            else:
                basic_mulp(self.project_path)

        elif base_mode == "env":
            if ini_info['match']["cal_input_twiss"] == 1:
                circle_match(self.project_path)
            elif ini_info['match']["match_with_twiss"] == 1 and ini_info['match']["use_initial_value"] == 0:
                match_twiss(self.project_path, 0)
            elif ini_info['match']["match_with_twiss"] == 1 and ini_info['match']["use_initial_value"] == 1:
                match_twiss(self.project_path, 1)
            else:
                basic_env(self.project_path)

if __name__ == '__main__':
    path = r"C:\Users\shliu\Desktop\eee"
    obj = SimMode(path)
    obj.run()
