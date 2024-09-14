from utils.readfile import read_txt
from utils.tool import write_to_txt, convert_dic2lis

class LatticeConfig():
    def __init__(self, lattice_mulp_path):
        self.lattice_path = lattice_mulp_path

    def initialize_lattice(self):
        self.lattice_parameter = [
            ["start"],
            ["drift", 0.01, 0.02, 0],
            ["drift", 0.01, 0.02, 0],
            ["end"]
        ]
    def read_lattice(self):
        self.input_lis = read_txt(self.input_path, out='list', case_sensitive=False)
        self.lattice_parameter = self.input_lis

    def add_element(self):
        pass
    def write_lattice(self):
        write_to_txt(self.lattice_path, self.lattice_parameter)

