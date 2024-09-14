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
        beam_config = BeamConfig(self.beam_path)
        beam_config.initialize_beam()
        basic_info = {
            'readparticledistribution': None, 'numofcharge': 1, 'particlerestmass': 938.272, 'current': 0,
            'particlenumber': 5000, 'frequency': 100, 'kneticenergy': 1,
            "alpha_x": 0, "beta_x": 1, "emit_x": 0.1,
            "alpha_y": 0, "beta_y": 1, "emit_y": 0.1,
            "alpha_z": 0, "beta_z": 1, "emit_z": 0.1,
            "distribution_x": "GS", "distribution_y": "GS"
        }
        beam_config.set_beam(**basic_info)
        beam_config.write_beam()

    def create_basic_input_file(self):
        input_config = InputConfig(self.input_path)
        input_config.initialize_input()
        input_info = {
            'scmethod': "FFT", "scanphase": 1, 'spacecharge': 1, 'steppercycle': 100, 'dumpperiodicity': 0,
            "maxthreads": -1
        }
        input_config.set_input(**input_info)
        input_config.write_input()

    def create_basic_lattice_mulp_file(self):
        lattice_config = LatticeConfig(self.lattice_mulp_path)
        lattice_config.initialize_lattice()
        lattice_config.write_lattice()

    def create_basic_ini_file(self):
        ini_config = IniConfig(self.ini_path)
        ini_config.initialize_ini()
        ini_config.write_ini()




if __name__ == "__main__":
    project_path = r"C:\Users\shliu\Desktop\test_new_avas\eee"
    CreatBasicFile(project_path).create_basic_beam_file()
    CreatBasicFile(project_path).create_basic_input_file()
    CreatBasicFile(project_path).create_basic_lattice_mulp_file()
    CreatBasicFile(project_path).create_basic_ini_file()


