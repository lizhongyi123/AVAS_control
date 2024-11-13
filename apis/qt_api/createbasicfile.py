from utils.beamconfig import BeamConfig
from utils.inputconfig import InputConfig
from utils.iniconfig import IniConfig
from utils.latticeconfig import LatticeConfig
from utils.tool import format_output
import os

class CreatBasicFile():
    def __init__(self, project_path):
        self.project_path = project_path
        self.beam_path = os.path.join(project_path, "InputFile", "beam.txt")
        self.input_path = os.path.join(project_path, "InputFile", "input.txt")
        self.lattice_mulp_path = os.path.join(project_path, "InputFile", "lattice_mulp.txt")
        self.ini_path = os.path.join(project_path, "InputFile", "ini.ini")
        self.beam_info = {
            'readparticledistribution': None, 'numofcharge': 1, 'particlerestmass': 938.272, 'current': 0,
            'particlenumber': 5000, 'frequency': 100, 'kneticenergy': 1,
            "alpha_x": 0, "beta_x": 1, "emit_x": 0.1,
            "alpha_y": 0, "beta_y": 1, "emit_y": 0.1,
            "alpha_z": 0, "beta_z": 1, "emit_z": 0.1,
            "distribution_x": "GS", "distribution_y": "GS"
        }

        self.input_info = {
            "sim_type": "mulp", 'scmethod': "FFT", "scanphase": 1, 'spacecharge': 1, 'steppercycle': 100, 'dumpperiodicity': 0,
            "maxthreads": -1
        }

    def create_basic_beam_file(self):
        beam_config = BeamConfig()

        beam_config.set_param(**self.beam_info)
        beam_config.write_to_file(self.beam_path)

    def create_basic_input_file(self):
        input_config = InputConfig()

        input_config.set_param(**self.input_info)
        input_config.write_to_file(self.input_path)

    def create_basic_lattice_mulp_file(self):
        lattice_config = LatticeConfig()
        lattice_config.initialize_lattice()
        lattice_config.write_to_file(self.lattice_mulp_path)

    def create_basic_ini_file(self):
        ini_config = IniConfig()
        ini_info = {"input": {"sim_type": "mulp"}}

        ini_config.set_param(**ini_info)
        ini_config.write_to_file(self.ini_path)

class CreateBasicProject():
    def __init__(self, item, platform):
        # item = {"project_path": ,
        #         "beam_keys": [],
        #         "input_keys": [],
        #         ""
        #          }

        self.item = item
        self.project_path = self.item["project_path"]
        self.platform = platform


    def validate_keys(self):
        beam_keys_back = BeamConfig().beam_parameter_keys
        input_keys_back = InputConfig().input_parameter_keys


        beam_keys_front = self.item["beam_keys"]
        input_keys_front = self.item["input_keys"]

        beam_extra_keys = set(beam_keys_front) - set(beam_keys_back)  # 前端多出的键
        beam_missing_keys = set(beam_keys_back) - set(beam_keys_front)  # 前端缺少的键

        input_extra_keys = set(input_keys_front) - set(input_keys_back)  # 前端多出的键
        input_missing_keys = set(input_keys_back) - set(input_keys_front)  # 前端缺少的键


        msg ={
            "beam_extra": list(beam_extra_keys),
            "beam_missing": list(beam_missing_keys),
            "input_extra": list(input_extra_keys),
            "input_missing": list(input_missing_keys)
        }
        return msg

    def create_project(self):
        obj = CreatBasicFile(self.project_path)
        kwargs = {
            "project_path": '',
            "beam_params": obj.beam_info,
            "input_params": obj.input_info,
            "beam_extra": [],
            "beam_missing": [],
            "input_extra": [],
            "input_missing": [],
        }

        if self.platform == "qt":
            pass
        elif self.platform == "web":
            validate_res = self.validate_keys()
            validate_res_values = [v for k, v in validate_res.items()]

            if any(validate_res_values):
                msg = ("The template parameter does not match the"
                       " parameters of the AVAS project, unable to generate the basic configuration directory.")

                error_msg = {k: v for k, v in validate_res.items() if v}
                kwargs.update(error_msg)
                output = format_output(code=-1, msg=msg, **kwargs)
                return output

        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
        elif os.path.exists(self.project_path):
            # raise FileExistsError(f"The directory '{project_path}' already exists.")
            project_path = os.path.normpath(self.project_path)

            code = -1
            msg = f"The directory '{project_path}' already exists."
            res = format_output(code, msg=msg, **kwargs)
            return res


        input_file = os.path.join(self.project_path, 'InputFile')
        output_file = os.path.join(self.project_path, 'OutputFile')


        os.makedirs(input_file)
        os.makedirs(output_file)


        obj.create_basic_beam_file()
        obj.create_basic_input_file()
        obj.create_basic_lattice_mulp_file()
        obj.create_basic_ini_file()


        kwargs = {"project_path": self.project_path,
                  }
        res = format_output(**kwargs)

        return res




if __name__ == "__main__":
    project_path = r"C:\Users\shliu\Desktop\test111\new_project"
    # CreatBasicFile(project_path).create_basic_beam_file()
    # CreatBasicFile(project_path).create_basic_input_file()
    # CreatBasicFile(project_path).create_basic_lattice_mulp_file()
    # CreatBasicFile(project_path).create_basic_ini_file()


    item = {
        "project_path": project_path,

        "beam_keys": ['readparticledistribution', 'numofcharge', 'particlerestmass',
                                    'current', 'particlenumber', 'frequency',
                                    'kneticenergy', 'alpha_x', 'beta_x', 'emit_x',
                                    "alpha_y", "beta_y", "emit_y",
                                    "alpha_z", "beta_z", "emit_z",
                                    'distribution_x', 'aaa'],
        # 'distribution_y', 'aaa'


        "input_keys": ["sim_type", "scmethod", "scanphase", "spacecharge", "steppercycle",
                       "dumpperiodicity", "maxthreads", "spacechargelong", "bbb"]
        #"spacechargetype", 'bbb'
    }
    platform = "web"
    obj = CreateBasicProject(item, platform)
    obj.create_project()

