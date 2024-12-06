from utils.readfile import read_txt
from utils.exception import (TypeError, ValueRangeError, ValueChooseError, ListLengthError,
                             UnknownkeywordError, ValueConvertError, MisskeywordError)
from utils.tool import write_to_txt, convert_dic2lis
import copy
from utils.iniconfig import IniConfig
from utils.tool import format_output
import os
class InputConfig():
    def __init__(self):
        self.input_parameter_keys = ["sim_type", "scmethod", "scanphase", "spacecharge", "steppercycle", "dumpperiodicity",
                                     "spacechargelong", "spacechargetype"]
        self.int_keys = ["scanphase", "spacecharge", "steppercycle", "dumpperiodicity",
                         "spacechargelong", "spacechargetype"]

        self.input_parameter = {"sim_type": None, "scanphase": None, 'spacecharge': None, 'steppercycle': None, 'dumpperiodicity':None,
                                "spacechargelong": None, "spacechargetype": None}

        self.mulp_keys = ["sim_type", "scmethod", "scanphase", "spacecharge", "steppercycle", "dumpperiodicity",]
        self.env_keys = ["spacechargelong", "spacechargetype"]
    # def initialize_input(self):
    #     self.input_parameter = {'scmethod': None, "scanphase": None, 'spacecharge': None, 'steppercycle': None, 'dumpperiodicity':None,
    #                             "maxthreads": None}




    def read_input_txt(self, path):
        #读取beam文件
        input_lis = read_txt(path, out='list', readdall=True, case_sensitive=True, )


        for i in input_lis:
            if len(i) == 1:
                i.append(None)
            if i[0] == "!sim_type":
                i[0] = "sim_type"

        res = {}
        for i in input_lis:
            if len(i) == 2:
                res[i[0]] = i[1]
            else:
                res[i[0]] = i[1:]

        return res

    def create_from_file(self, item):
        other_path = item.get("otherPath")
        if other_path is None:
            path = os.path.join(item.get("projectPath"), "InputFile", "input.txt")
        else:
            path = other_path

        kwargs = {}
        try:
            original_dict = self.read_input_txt(path)

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

        except Exception as e:
            code = -1
            msg = str(e)
            kwargs.update({'inputParams': {}})
            output = format_output(code, msg=msg, **kwargs)
            return output

        # print("read", self.beam_parameter)
        kwargs.update({'inputParams': copy.deepcopy(self.input_parameter)})
        output = format_output(**kwargs)
        return output

    def set_param(self, **kwargs):
        kwargs1 = {}
        try:
            # self.validate_type(kwargs)
            for k, v in kwargs.items():
                self.input_parameter[k] = v

        except Exception as e:
            code = -1
            msg = str(e)
            kwargs1.update({'inputParams': {}})
            output = format_output(code, msg=msg, **kwargs1)
            return output

        kwargs1.update({'inputParams': copy.deepcopy(self.input_parameter)})
        output = format_output(**kwargs1)
        return output

    def write_to_file(self, item):
        other_path = item.get("otherPath")
        if other_path is None:
            path = os.path.join(item.get("projectPath"), "InputFile", "input.txt")
        else:
            path = other_path

        kwargs = {}
        try:
            v_dic = {}
            if self.input_parameter["sim_type"] == 'mulp':
                v_dic = copy.deepcopy(self.input_parameter)
                v_dic["!sim_type"] = v_dic["sim_type"]

                del v_dic["spacechargelong"]
                del v_dic["spacechargetype"]
                del v_dic["sim_type"]
            elif self.input_parameter["sim_type"] == 'env':

                v_dic["!sim_mode"] = self.input_parameter["sim_type"]
                v_dic["spacechargelong"] = self.input_parameter["spacechargelong"]
                v_dic["spacechargetype"] = self.input_parameter["spacechargetype"]


            v_lis = convert_dic2lis(v_dic)
            for index, i in enumerate(v_lis):
                v_lis[index] = ["" if v is None else v for v in i]
            #检查是否存在未None的情况

            write_to_txt(path, v_lis)

        except Exception as e:
            code = -1
            msg = str(e)
            kwargs.update({'inputParams': {}})
            output = format_output(code, msg=msg, **kwargs)
            return output

        kwargs.update({'inputParams': copy.deepcopy(self.input_parameter)})
        output = format_output(**kwargs)
        return output


    def validate_type(self, param):
        #验证关键词的类型
        for k, v in param.items():
            if k == "scmethod" and v is not None:
                if v not in ["FFT", "SPICNIC"]:
                    raise ValueChooseError(k, ["FFT", "SPICNIC"], v)
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
        if self.input_parameter["sim_type"] == 'mulp':
            for k in self.mulp_keys:
                if self.input_parameter[k] is None:
                    raise MisskeywordError(f"{k}")

        elif self.input_parameter["sim_type"] == 'env':
            for k in self.env_keys:
                if self.input_parameter[k] is None:
                    raise MisskeywordError(f"{k}")
if __name__ == "__main__":
    import json

    path =r"C:\Users\shliu\Desktop\test1113\test4"
    item = {"projectPath": path}
    obj = InputConfig()
    res = obj.create_from_file(item)
    print(res)

    v = {k: v if v else " " for k, v in res["data"]["inputParams"].items()}
    print(1, v)
    # print(res)
    # for k, v in res["data"]["inputParams"].items():
    #     if v:
    #         print(v)
    v = json.dumps(v)
    print(2, v)
    # set_param = {'scanphase': 2}
    # obj.set_input(**set_param)
    # obj.write_input()
