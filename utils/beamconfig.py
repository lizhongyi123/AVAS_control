from utils.readfile import read_txt
from utils.tool import write_to_txt, convert_dic2lis
import copy
from utils.exception import ValidateDictError, TypeError, ValueError, ListLengthError
class BeamConfig():
    def __init__(self, beam_path):
        self.beam_path = beam_path
        self.beam_parameter = {}


        self.int_keys = ['numofcharge', 'particlenumber']
        self.float_keys = ['particlerestmass', 'current', 'frequency', 'kneticenergy'
                            "alpha_x", "beta_x", "emit_x",
                           "alpha_y", "beta_y", "emit_y",
                           "alpha_z", "beta_z", "emit_z",
                           ]
        self.twiss_keys = ["twissx", "twissy", "twissz"]
        #其他的  'readparticledistribution'， 'distribution_x', "distribution_y"


    def initialize_beam(self):
        self.beam_parameter = {'readparticledistribution': None,  'numofcharge': None, 'particlerestmass': None, 'current':None,
                       'particlenumber': None, 'frequency': None, 'kneticenergy': None,
                        "alpha_x": None, "beta_x": None, "emit_x": None,
                        "alpha_x": None, "beta_x": None, "emit_x": None,
                        "alpha_x": None, "beta_x": None, "emit_x": None,
                        "distribution_x": None, "distribution": None
             }

    # 'twissx': [None, None, None], 'twissy': [None, None, None],
    # 'twissz': [None, None, None], 'distribution': [None, None],

    def read_beam(self):
        self.initialize_beam()
        t_dict = read_txt(self.beam_path, out='dict')

        for k, v in t_dict.items():
            v = self.convert_v(k, v)
            self.beam_parameter[k] = v

        print("read", self.beam_parameter)

    def write_beam(self):
        print("write", self.beam_parameter)
        v_dic = {}
        if self.beam_parameter["readparticledistribution"] is not None:
            v_dic['readparticledistribution'] = self.beam_parameter['readparticledistribution']
            v_dic['numofcharge'] = self.beam_parameter['numofcharge']
        else:
            v_dic = copy.deepcopy(self.beam_parameter)
            del v_dic['readparticledistribution']

        self.validate_write(v_dic)
        print("v_dic", v_dic)
        v_lis = convert_dic2lis(v_dic)
        print("write", v_lis)


        #检查是否存在未None的情况

        # write_to_txt(self.beam_path, v_lis)

    def set_beam(self, **kwargs):
        # self.validate_set(kwargs)
        for k, v in kwargs.items():
            self.beam_parameter[k] = v

        print("set", self.beam_parameter)



    def convert_v(self, k, v):

        if k in self.int_keys:
            v = int(v)
        elif k in self.float_keys:
            v = float(v)
        elif k in self.twiss_keys:
            v = [float(v[0]), float(v[1]), float(v[2])]
        else:
            pass
        return v

    def validate_write(self, param):
        if self.beam_parameter["readparticledistribution"] is not None:
            if not isinstance(param["readparticledistribution"], str):
                raise TypeError("readparticledistribution", str, type(param["readparticledistribution"]))

            if not isinstance(param["numofcharge"], int):
                raise TypeError("numofcharge", int, type(param["numofcharge"]))

        else:


            for k, v in param.items():
                if k in self.int_keys and not isinstance(v, int):
                    raise TypeError(k, int, type(v))
                elif k in self.float_keys and not isinstance(v, (int, float)):
                    raise TypeError(k, float, type(v))
                elif k == "distribution_x" and v.lower not in ["wb", "pb", "gs", "kv"]:
                    raise ValueError(k, ["wb", "pb", "gs", "kv"])





        # for k, v in param.items():

        #检查类型有没有错误
        # pass
    # def validate_set(self, param):
    #     for k, v in param.items():
    #         if k == "is_dstfile" and v not in [0, 1]:
    #             raise ValidateDictError("Value error", f"{k}", [0, 1])
    #

    def validate_read(self, param):
        pass




if __name__ == "__main__":
    path = r"C:\Users\anxin\Desktop\test_830\InputFile\beam.txt"
    obj = BeamConfig(path)
    obj.read_beam()
    obj.set_beam(twissx=[1,2,3])
    # obj.set_beam(numofcharge=1.5)
    obj.write_beam()