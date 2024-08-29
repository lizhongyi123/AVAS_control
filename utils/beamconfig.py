from utils.readfile import read_txt
class BeamConfig():
    def __init__(self, beam_path):
        self.beam_path = beam_path

    def initialize_beam(self):
        beam_dict = {'numOfcharge': 0, 'particlerestmass': 0, 'current': 0,
                      'particlenumber': 0, 'frequency': 0, 'kneticenergy': 0,
                      'twissx': [0, 0, 0], 'twissy': [0,0,0], 'twissz': [0,0,0], 'distribution': [" ", " "], }
        return beam_dict
    def read_beam(self):
        beam_dict = read_txt(input, out='dict')
        45

    def write_beam(self):

    def set_beam