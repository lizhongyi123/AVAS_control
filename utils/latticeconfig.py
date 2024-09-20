from utils.readfile import read_txt
from utils.tool import write_to_txt, convert_dic2lis

class LatticeConfig():
    def __init__(self):
        self.lattice_parameter = [
            ["start"],
            ["drift", 0.01, 0.02, 0],
            ["drift", 0.01, 0.02, 0],
            ["end"]
        ]

    def initialize_lattice(self):
        self.lattice_parameter = [
            ["start"],
            ["drift", 0.01, 0.02, 0],
            ["drift", 0.01, 0.02, 0],
            ["end"]
        ]
    def create_from_file(self, path):
        self.input_lis = read_txt(path, out='list', case_sensitive=False)
        self.lattice_parameter = self.input_lis
        return self.lattice_parameter

    def add_element(self):
        return self.lattice_parameter
    def write_to_file(self, path):
        write_to_txt(path, self.lattice_parameter)

