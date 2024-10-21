from utils.beamconfig import BeamConfig
from utils.inputconfig import InputConfig
from utils.iniconfig import IniConfig
from utils.latticeconfig import LatticeConfig

import os

class CreatBasicFile():
    def __init__(self, project_path):
        self.project_path = project_path
        self.beam_path = os.path.join(project_path, "InputFile", "beam.txt")
        self.input_path = os.path.join(project_path, "InputFile", "input.txt")
        self.lattice_mulp_path = os.path.join(project_path, "InputFile", "lattice_mulp.txt")
        self.ini_path = os.path.join(project_path, "InputFile", "ini.ini")


    def create_basic_beam_file(self):
        beam_config = BeamConfig()
        basic_info = {
            'readparticledistribution': None, 'numofcharge': 1, 'particlerestmass': 938.272, 'current': 0,
            'particlenumber': 5000, 'frequency': 100, 'kneticenergy': 1,
            "alpha_x": 0, "beta_x": 1, "emit_x": 0.1,
            "alpha_y": 0, "beta_y": 1, "emit_y": 0.1,
            "alpha_z": 0, "beta_z": 1, "emit_z": 0.1,
            "distribution_x": "GS", "distribution_y": "GS"
        }
        beam_config.set_param(**basic_info)
        beam_config.write_to_file(self.beam_path)

    def create_basic_input_file(self):
        input_config = InputConfig()
        input_info = {
            "!sim_type": "mulp", 'scmethod': "FFT", "scanphase": 1, 'spacecharge': 1, 'steppercycle': 100, 'dumpperiodicity': 0,
            "maxthreads": -1
        }
        input_config.set_param(**input_info)
        input_config.write_to_file(self.input_path)

    def create_basic_lattice_mulp_file(self):
        lattice_config = LatticeConfig()
        lattice_config.initialize_lattice()
        lattice_config.write_to_file(self.lattice_mulp_path)

    def create_basic_ini_file(self):
        ini_config = IniConfig()
        ini_info = {"input": {"!sim_type": "mulp"}}

        ini_config.set_param(**ini_info)
        ini_config.write_to_file(self.ini_path)

class CreateBasicProject():
    def __init__(self, project_path):
        self.project_path = project_path

    def create_project(self):
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
        elif os.path.exists(self.project_path):
            raise FileExistsError(f"The directory '{project_path}' already exists.")


        input_file = os.path.join(self.project_path, 'InputFile')
        output_file = os.path.join(self.project_path, 'OutputFile')
        os.makedirs(input_file)
        os.makedirs(output_file)

        obj = CreatBasicFile(self.project_path)
        obj.create_basic_beam_file()
        obj.create_basic_input_file()
        obj.create_basic_lattice_mulp_file()
        obj.create_basic_ini_file()




if __name__ == "__main__":
    project_path = r"C:\Users\shliu\Desktop\eee"
    # CreatBasicFile(project_path).create_basic_beam_file()
    # CreatBasicFile(project_path).create_basic_input_file()
    # CreatBasicFile(project_path).create_basic_lattice_mulp_file()
    # CreatBasicFile(project_path).create_basic_ini_file()

    obj = CreateBasicProject(project_path)
    obj.create_project()

