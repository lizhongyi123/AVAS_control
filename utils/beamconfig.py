from utils.readfile import read_txt
from utils.tool import write_to_txt, convert_dic2lis
import copy
from utils.exception import (TypeError, ValueRangeError, ValueChoosesError, ListLengthError,
                             UnknownkeywordError, ValueConvertError)
class BeamConfig():
    def __init__(self, beam_path):
        self.beam_path = beam_path
        self.beam_parameter = {}

        self.beam_parameter_keys = ['readparticledistribution', 'numofcharge', 'particlerestmass',
                                    'current', 'particlenumber', 'frequency',
                                    'kneticenergy', 'alpha_x', 'beta_x', 'emit_x',
                                    "alpha_y", "beta_y", "emit_y",
                                    "alpha_z", "beta_z", "emit_z",
                                    'distribution_x', 'distribution_y']

        self.with_dst_keys = ['readparticledistribution', 'numofcharge']

        self.no_dst_keys = ['numofcharge', 'particlerestmass',
                             'current', 'particlenumber', 'frequency',
                             'kneticenergy', 'alpha_x', 'beta_x', 'emit_x',
                             'distribution_x', 'distribution_y']

        self.str_keys = ['readparticledistribution', 'distribution_x', "distribution_y"]
        self.int_keys = ['numofcharge', 'particlenumber']
        self.float_keys = ['particlerestmass', 'current', 'frequency', 'kneticenergy'
                            "alpha_x", "beta_x", "emit_x",
                           "alpha_y", "beta_y", "emit_y",
                           "alpha_z", "beta_z", "emit_z",
                           ]
        #其他的  'readparticledistribution'， 'distribution_x', "distribution_y"
        self.twiss_keys = ["twissx", "twissy", "twissz"]



    def initialize_beam(self):
        self.beam_parameter = {'readparticledistribution': None,  'numofcharge': None, 'particlerestmass': None, 'current':None,
                       'particlenumber': None, 'frequency': None, 'kneticenergy': None,
                        "alpha_x": None, "beta_x": None, "emit_x": None,
                        "alpha_y": None, "beta_y": None, "emit_y": None,
                        "alpha_z": None, "beta_z": None, "emit_z": None,
                        "distribution_x": None, "distribution_y": None
                }


    def read_beam(self):
        self.initialize_beam()
        original_dict = read_txt(self.beam_path, out='dict')
        print(original_dict)
        if "twissx" in original_dict.keys():
            original_dict["alpha_x"] = original_dict["twissx"][0]
            original_dict["beta_x"] = original_dict["twissx"][1]
            original_dict["emit_x"] = original_dict["twissx"][2]
            del original_dict["twissx"]
        if "twissy" in original_dict.keys():
            original_dict["alpha_y"] = original_dict["twissy"][0]
            original_dict["beta_y"] = original_dict["twissy"][1]
            original_dict["emit_y"] = original_dict["twissy"][2]
            del original_dict["twissy"]

        if "twissz" in original_dict.keys():
            original_dict["alpha_z"] = original_dict["twissz"][0]
            original_dict["beta_z"] = original_dict["twissz"][1]
            original_dict["emit_z"] = original_dict["twissz"][2]
            del original_dict["twissz"]
        if "distribution" in original_dict.keys():
            original_dict["distribution_x"] = original_dict["distribution"][0]
            original_dict["distribution_y"] = original_dict["distribution"][1]
            del original_dict["distribution"]

        #验证是否存在未知元素
        for k, v in original_dict.items():
            if k not in self.beam_parameter_keys:
                raise UnknownkeywordError(message=None, key=k)

        #如果不存在未知元素, 转换类型
        for k, v in original_dict.items():
            original_dict[k] = self.convert_v(k, v)

        #赋值给self.beam_parameter 
        if self.validate_type(original_dict):
            for k, v in original_dict.items():
                self.beam_parameter[k] = original_dict[k]


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
        self.validate_type(kwargs)
        for k, v in kwargs.items():
            self.beam_parameter[k] = v

        print("set", self.beam_parameter)



    def convert_v(self, k, v):
        expected_type = None
        try:
            if k in self.int_keys:
                expected_type = int
                v = int(v)
            elif k in self.float_keys:
                expected_type = float
                v = float(v)
            elif k in self.str_keys:
                expected_type = str
                v = str(v)
        except (ValueError, TypeError):
            raise ValueConvertError(k, expected_type, v)

        return v

    def validate_type(self, param):
        #验证关键词的类型
        for k, v in param.items():
            if k == "readparticledistribution" and v is not None:
                if not isinstance(v, str):
                    raise TypeError(k, str, type(v))
            elif k in self.int_keys and v is not None:
                if not isinstance(v, int):
                    raise TypeError(k, int, type(v))
            elif k in self.float_keys and v is not None:
                if not isinstance(v, (int, float)):
                    raise TypeError(k, float, type(v))
            elif (k == "distribution_x" or k == "distribution_Y") and v is not None:
                if v.lower not in ["wb", "pb", "gs", "kv"]:
                    raise ValueChoosesError(k, ["wb", "pb", "gs", "kv"], v)

            elif k not in self.beam_parameter_keys:
                raise UnknownkeywordError(k)

        return True

    def validate_run(self, param):
        self.read_beam()
        #当说有输入符合
        if self.beam_parameter["readparticledistribution"] is not None:
            v_dic['readparticledistribution'] = self.beam_parameter['readparticledistribution']
            v_dic['numofcharge'] = self.beam_parameter['numofcharge']
        else:
            v_dic = copy.deepcopy(self.beam_parameter)
            del v_dic['readparticledistribution']


        


if __name__ == "__main__":
    path = r"C:\Users\shliu\Desktop\test_new_avas\av_err_dyn\InputFile\beam.txt"
    obj = BeamConfig(path)
    obj.read_beam()
    obj.set_beam(twissx=[1,2,3])
    # # obj.set_beam(numofcharge=1.5)
    # obj.write_beam()