import os.path

from utils.readfile import read_dst, read_txt

from utils.readfile import read_dst, read_txt
from utils.iniconfig import IniConfig
from utils.inputconfig import InputConfig
def get_mass_freq(project_path):
    beam_txt = project_path + r'/InputFile/beam.txt'
    res = read_txt(beam_txt)
    if res.get('readparticledistribution') is None:
        BaseMassInMeV = float(res.get('particlerestmass'))
        freq = float(res.get('frequency'))
    else:
        dstfile = project_path + r'/InputFile' + r"/" + res.get('readparticledistribution')
        dst_res = read_dst(dstfile)
        BaseMassInMeV = float(dst_res.get('basemassinmev'))
        freq = float(dst_res.get('freq'))
    return BaseMassInMeV, freq

def get_timestep(project_path):
    BaseMassInMeV, freq = get_mass_freq(project_path)
    input_path = os.path.join(project_path, 'InputFile', "input.txt")
    input_obj = InputConfig()
    input = input_obj.creat_from_file(input_path)

    steppercycle = input['steppercycle']
    timestep = 1 / freq / steppercycle
    return timestep

if __name__ == '__main__':
    project_path = r'C:\Users\shliu\Desktop\AVAS20240923\test'
    timestep = get_timestep(project_path)
    print(timestep)