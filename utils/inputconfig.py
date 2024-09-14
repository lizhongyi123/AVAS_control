from utils.readfile import read_txt
from utils.exception import (TypeError, ValueRangeError, ValueChooseError, ListLengthError,
                             UnknownkeywordError, ValueConvertError)
from utils.tool import write_to_txt, convert_dic2lis
import copy

class InputConfig():
    def __init__(self):
        self.input_parameter_keys = ["scmethod", "scanphase", "spacecharge", "steppercycle", "dumpperiodicity", "maxthreads"]
        self.int_keys = ["scanphase", "spacecharge", "steppercycle", "dumpperiodicity", "maxthreads"]

        self.input_parameter = {'scmethod': None, "scanphase": None, 'spacecharge': None, 'steppercycle': None, 'dumpperiodicity':None,
                                "maxthreads": None}
    # def initialize_input(self):
    #     self.input_parameter = {'scmethod': None, "scanphase": None, 'spacecharge': None, 'steppercycle': None, 'dumpperiodicity':None,
    #                             "maxthreads": None}

    def read_input_txt(self, path):
        #读取beam文件
        input_lis = read_txt(path, out='list', case_sensitive=True)


        for i in input_lis:
            if len(i) == 1:
                i.append(None)

        res = {}
        for i in input_lis:
            if len(i) == 2:
                res[i[0]] = i[1]
            else:
                res[i[0]] = i[1:]
        return res

    def creat_from_file(self, path):
        original_dict = self.read_input_txt(path)
        print(original_dict)

        #验证是否存在未知元素
        for k, v in original_dict.items():
            if k not in self.input_parameter_keys:
                raise UnknownkeywordError(message=None, key=k)

        #如果不存在未知元素, 转换类型
        for k, v in original_dict.items():
            original_dict[k] = self.convert_v(k, v)

        if self.validate_type(original_dict):
            for k, v in original_dict.items():
                self.input_parameter[k] = original_dict[k]

        print(original_dict)
        return self.input_parameter

    def set_param(self, **kwargs):
        self.validate_type(kwargs)
        for k, v in kwargs.items():
            self.input_parameter[k] = v

        print("set", self.input_parameter)
        return True
    def write_to_file(self, path):

        v_dic = copy.deepcopy(self.input_parameter)
        v_lis = convert_dic2lis(v_dic)
        for index, i in enumerate(v_lis):
            v_lis[index] = ["" if v is None else v for v in i]
        print("write", v_lis)

        #检查是否存在未None的情况

        write_to_txt(path, v_lis)
        return True


    def validate_type(self, param):
        #验证关键词的类型
        for k, v in param.items():
            if k == "scmethod" and v is not None:
                if v not in ["FFT", "PICNIC"]:
                    raise ValueChooseError(k, ["FFT", "PICNIC"], v)
            elif k == "scanphase" and v is not None:
                if v not in [0, 1, 2]:
                    raise ValueChooseError(k, [0, 1, 2], v)
            elif k == "spacecharge" and v is not None:
                if v not in [0, 1]:
                    raise ValueChooseError(k, [0, 1], v)
            elif k == "steppercycle" and v is not None:
                if not isinstance(v, int):
                    raise TypeError(k, int, type(v))
                if v <= 0:
                    raise ValueRangeError(k, ["1", "+inf"], v)

            elif k == "dumpperiodicity" and v is not None:
                if not isinstance(v, int):
                    raise TypeError(k, int, type(v))
                if v < 0:
                    raise ValueRangeError(k, ["0", "+inf"], v)

            elif k == "maxthreads" and v is not None:
                if not isinstance(v, int):
                    raise TypeError(k, int, type(v))

            elif k not in self.input_parameter_keys:
                raise UnknownkeywordError(k)

        return True



    def convert_v(self, k, v):
        if v is not None:
            expected_type = None
            try:
                if k in self.int_keys:
                    expected_type = int
                    v = int(v)
            except (ValueError, TypeError):
                raise ValueConvertError(k, expected_type, v)
            return v

        else:
            return v

    def validate_run(self, path):
        self.creat_from_file(path)
        #当所有输入符合
        for k in self.input_parameter_keys:
            if self.input_parameter[k] is None:
                raise Exception(f"missing parameter {k}")

if __name__ == "__main__":
    path = (r"C:\Users\shliu\Desktop\test_new_avas\input1.txt")
    obj = InputConfig(path)
    # obj.read_input()
    # set_param = {'scanphase': 2}
    # obj.set_input(**set_param)
    obj.write_input()