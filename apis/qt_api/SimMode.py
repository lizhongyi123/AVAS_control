
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

    def file_check(self):
        #检查input文件
        input_config = InputConfig()
        input_config.validate_run(self.item)

        #检查beam文件
        beam_config = BeamConfig()
        beam_config.validate_run(self.item)



    def run(self):
        #检查
        self.file_check()

        #判断模拟类型并进行模拟
        ini_obj = IniConfig()
        ini_info = ini_obj.create_from_file(self.item)
        if ini_info["code"] == -1:
            raise Exception(ini_info["data"]['msg'])
        ini_info = ini_info["data"]["iniParams"]
        base_mode = ini_info["input"]["sim_type"]


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

        all_error_type =["stat", "dyn", "stat_dyn", ""]
        if err_mode not in all_error_type:
            raise exce.ValueRangeError('error type', all_error_type, err_mode)


        field_path = ini_info["project"]["fieldSource"]

        #如果field_path是空的
        if not field_path:
            field_path = None

        obj = JudgeLattice(self.lattice_mulp_path)

        if base_mode == "mulp":
            if err_mode == "stat":
                obj.judge_lattice("stat_error")
                err_stat(self.project_path, err_seed, if_normal=1, field_path=field_path)

            elif err_mode == "dyn":
                obj.judge_lattice("dyn_error")
                err_dyn(self.project_path, err_seed, if_normal=1, field_path=field_path)

            elif err_mode == "stat_dyn":
                obj.judge_lattice("stat_dyn_error")
                err_stat_dyn(self.project_path, err_seed, if_normal=1, field_path=field_path)
            else:
                obj.judge_lattice("basic_mulp")
                basic_mulp(self.project_path, field_path=field_path)

        elif base_mode == "env":
            if ini_info['match']["cal_input_twiss"] == 1:
                circle_match(self.project_path)
            elif ini_info['match']["match_with_twiss"] == 1 and ini_info['match']["use_initial_value"] == 0:
                match_twiss(self.project_path, 0)
            elif ini_info['match']["match_with_twiss"] == 1 and ini_info['match']["use_initial_value"] == 1:
                match_twiss(self.project_path, 1)
            else:
                basic_env(self.project_path)

        output = format_output()
        return output


if __name__ == '__main__':
    pass
