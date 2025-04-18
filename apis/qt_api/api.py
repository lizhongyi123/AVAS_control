import re
import sys

from fontTools.feaLib import location

from aftertreat.dataanalysis.percentemitt import PercentEmit
from utils.readfile import read_dst_fast
import os
import copy
from utils.tool import format_output
from utils.treat_directory import list_files_in_directory

from utils.iniconfig import IniConfig
from utils.inputconfig import InputConfig
import pandas as pd
def cal_beam_parameter(item):
    dst_path = item["dstPath"]
    kwargs = {}

    beam_parameter = {}
    try:
        if os.path.exists(dst_path):
            dst_res = read_dst_fast(dst_path)
            beam_parameter['particlerestmass'] = dst_res['basemassinmev']
            beam_parameter['current'] = dst_res['ib']
            beam_parameter['particlenumber'] = dst_res['number']
            beam_parameter['frequency'] = dst_res['freq']
            beam_parameter['kneticenergy'] = dst_res['kneticenergy']

            obj = PercentEmit(dst_path)
            res = obj.get_percent_emit(1)

            alpha_xx1, beta_xx1, epsi_xx1, _, _ = res[0]
            alpha_yy1, beta_yy1, epsi_yy1, _, _ = res[1]
            alpha_zz1, beta_zz1, epsi_zz1, _, _ = res[2]

            beam_parameter['alpha_x'] = alpha_xx1
            beam_parameter['beta_x'] = beta_xx1
            beam_parameter['emit_x'] = epsi_xx1

            beam_parameter['alpha_y'] = alpha_yy1
            beam_parameter['beta_y'] = beta_yy1
            beam_parameter['emit_y'] = epsi_yy1

            beam_parameter['alpha_z'] = alpha_zz1
            beam_parameter['beta_z'] = beta_zz1
            beam_parameter['emit_z'] = epsi_zz1

            beam_parameter["readparticledistribution"] = ""
            beam_parameter["distribution_x"] = "GS"
            beam_parameter["distribution_y"] = "GS"
            beam_parameter["numofcharge"] = ""
    except Exception as e:
        code = -1
        msg = str(e)
        kwargs.update({'beamParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    kwargs.update({'beamParams': copy.deepcopy(beam_parameter)})
    output = format_output(**kwargs)
    return output

def cal_beam_parameter(item):
    dst_path = item["dstPath"]
    kwargs = {}

    beam_parameter = {}
    try:
        if os.path.exists(dst_path):
            dst_res = read_dst_fast(dst_path)
            beam_parameter['particlerestmass'] = dst_res['basemassinmev']
            beam_parameter['current'] = dst_res['ib']
            beam_parameter['particlenumber'] = dst_res['number']
            beam_parameter['frequency'] = dst_res['freq']
            beam_parameter['kneticenergy'] = dst_res['kneticenergy']

            obj = PercentEmit(dst_path)
            res = obj.get_percent_emit(1)

            alpha_xx1, beta_xx1, epsi_xx1, _, _ = res[0]
            alpha_yy1, beta_yy1, epsi_yy1, _, _ = res[1]
            alpha_zz1, beta_zz1, epsi_zz1, _, _ = res[2]

            beam_parameter['alpha_x'] = alpha_xx1
            beam_parameter['beta_x'] = beta_xx1
            beam_parameter['emit_x'] = epsi_xx1

            beam_parameter['alpha_y'] = alpha_yy1
            beam_parameter['beta_y'] = beta_yy1
            beam_parameter['emit_y'] = epsi_yy1

            beam_parameter['alpha_z'] = alpha_zz1
            beam_parameter['beta_z'] = beta_zz1
            beam_parameter['emit_z'] = epsi_zz1

            beam_parameter["readparticledistribution"] = ""
            beam_parameter["distribution_x"] = ""
            beam_parameter["distribution_y"] = ""
            beam_parameter["numofcharge"] = ""
    except Exception as e:
        code = -1
        msg = str(e)
        kwargs.update({'beamParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    kwargs.update({'beamParams': copy.deepcopy(beam_parameter)})
    output = format_output(**kwargs)
    return output


def get_inputfile_path(item):
    # item = {"projectPath": "fdasf" }
    kwargs = {}
    input_path = os.path.join(item["projectPath"], "InputFile")
    kwargs.update({'inputFilePath': input_path})
    output = format_output(**kwargs)
    return output


# 获取上传位置
def get_upload_path(item):
    # item = {"projectPath": "fdasf", fileType, " "}
    kwargs = {}
    projectPath = item["projectPath"]
    fileType = item["fileType"]
    if fileType == "dst":
        upload_path = os.path.join(projectPath, "InputFile")
    elif fileType == "field":
        upload_path = os.path.join(projectPath, "InputFile", "field")
    kwargs.update({'uploadPath': upload_path})
    output = format_output(**kwargs)
    return output


# 得到模拟进度

def get_fieldname(item):
    #相对路径，没有后缀名， 去重
    kwargs = {}
    fieldPath = item["filePath"]
    if os.path.exists(fieldPath):
        all_files = list_files_in_directory(fieldPath, sort_by="mtime")
        suffix_list = ["edx", "edy", "edz", "bdx", "bdy", "bdz",
                       "bsx", "bsy", "bsz"
                       ]
        all_files = [i for i in all_files if i.split(".")[-1] in suffix_list]
        v = [i.split(r"/")[-1] for i in all_files]
        v = [i.split(".")[0] for i in v]
        field_name = list(set(v))
        kwargs.update({'fieldName': field_name})
        output = format_output(**kwargs)
    else:
        code = -1
        msg = f"FileNotFoundError: {fieldPath}"
        kwargs.update({'fieldName': []})
        output = format_output(code, msg=msg, **kwargs)
    return output


def get_bimap_name(item):
    #相对路径，没有后缀
    kwargs = {}
    bimapPath = item["filePath"] 
    if os.path.exists(bimapPath):
        all_files = list_files_in_directory(bimapPath)
        suffix_list = ["csv"
                       ]
        all_files = [i for i in all_files if i.split(".")[-1] in suffix_list]
        v = [i.split(r"/")[-1] for i in all_files]
        v = [i.split(".")[0] for i in v]
        bimap_name = list(set(v))
        kwargs.update({'bimapName': bimap_name})
        output = format_output(**kwargs)
    else:
        code = -1
        msg = f"FileNotFoundError: {bimapPath}"
        kwargs.update({'bimapName': []})
        output = format_output(code, msg=msg, **kwargs)
    return output


def get_fieldfile(item):
    #相对路径，有后缀
    kwargs = {}
    fieldpath = item["fieldPath"]
    if os.path.exists(fieldpath):
        all_files = list_files_in_directory(fieldpath, sort_by="mtime")
        suffix_list = ["edx", "edy", "edz", "bdx", "bdy", "bdz",
                       "bsx", "bsy", "bsz"
                       ]
        all_files = [i for i in all_files if i.split(".")[-1] in suffix_list]
        v = [i.split(r"/")[-1] for i in all_files]
        kwargs.update({'fieldFile': v})
        output = format_output(**kwargs)
    else:
        code = -1
        msg = f"FileNotFoundError: {fieldpath}"
        kwargs.update({'fieldFile': []})
        output = format_output(code, msg=msg, **kwargs)

    return output


def get_allfile_relative_path(item):
    #带后缀
    kwargs = {}
    fieldpath = item["filePath"]
    if os.path.exists(fieldpath):
        all_files = list_files_in_directory(fieldpath, sort_by="mtime")
        v = [i.split(r"/")[-1] for i in all_files]
        kwargs.update({'allFile': v})
        output = format_output(**kwargs)
    else:
        code = -1
        msg = f"FileNotFoundError: {fieldpath}"
        kwargs.update({'allFile': []})
        output = format_output(code, msg=msg, **kwargs)

    return output


def create_from_file_input_ini(item):
    # item的格式{“projectPath”： “path”}
    kwargs = {}

    input_obj = InputConfig()
    input_res = input_obj.create_from_file(item)
    if input_res["code"] == -1:
        code = -1
        msg = input_res["data"]["message"]
        kwargs.update({'inputiniParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    ini_obj = IniConfig()
    ini_res = ini_obj.create_from_file(item)
    if input_res["code"] == -1:
        code = -1
        msg = input_res["data"]["message"]
        kwargs.update({'inputiniParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    new_dic = {}
    new_dic.update(input_res["data"]["inputParams"])
    fieldSource_dic = {'fieldSource': ini_res["data"]["iniParams"]["project"]["fieldSource"],
                       "device": ini_res["data"]["iniParams"]["input"]["device"]
                       }
    new_dic.update(fieldSource_dic)

    kwargs.update({'inputiniParams': new_dic})
    output = format_output(**kwargs)
    return output


def write_to_file_input_ini(item, param):
    # item的格式{“projectPath”： “path”}
    # {'sim_type': 'mulp', 'scanphase': 1, 'spacecharge': 1, 'steppercycle': 50,
    #  'dumpperiodicity': 1, 'spacechargelong': None, 'spacechargetype': None,
    #  'scmethod': 'SPICNIC', 'fieldSource': ''}
    kwargs = {}
    input_param = copy.deepcopy(param)
    del input_param["fieldSource"]

    if input_param.get("device"):
        del input_param["device"]

    ini_param = {"project": {"fieldSource": param["fieldSource"]},
                 "input": {"sim_type": param["sim_type"], "device": param.get("device")},
                 }

    input_obj = InputConfig()
    input_res = input_obj.set_param(**input_param)
    if input_res["code"] == -1:
        code = -1
        msg = input_res["data"]["message"]
        kwargs.update({'inputiniParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    ini_obj = IniConfig()
    ini_res = ini_obj.set_param(**ini_param)
    if ini_res["code"] == -1:
        code = -1
        msg = ini_res["data"]["message"]
        kwargs.update({'inputiniParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    res1 = input_obj.write_to_file(item)
    res2 = ini_obj.write_to_file(item)
    new_dic = param
    kwargs.update({'inputiniParams': new_dic})
    output = format_output(**kwargs)
    return output


# def set_input_ini(item):
#     project_path =

def cal_mass(item):
    particletype = item["particletype"]
    nucleonnumber = item["nucleonnumber"]
    numofcharge = item["numofcharge"]

    kwargs = {}
    if particletype == "e-":
        kwargs.update({'particlerestmass': 0.511})
        output = format_output(**kwargs)
        return output
    elif particletype == "e+":
        kwargs.update({'particlerestmass': 0.511})
        output = format_output(**kwargs)
        return output

    script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在文件夹的绝对路径
    parent_directory = os.path.dirname(script_directory)  # 获取上级目录的路径
    parent_directory = os.path.dirname(parent_directory)  # 获取上级目录的路径
    mass_csv_path = os.path.join(parent_directory, "staticfile", "atomic_masses.csv")
    df = pd.read_csv(mass_csv_path, index_col=None)

    # 检测错误情况
    if 1:
        Element_lis = df["Element"].tolist()
        unique_lst = list(dict.fromkeys(Element_lis))
        if particletype not in unique_lst:
            code = -1
            msg = "This element doesn't exist"
            kwargs.update({'particlerestmass': ""})
            output = format_output(code, msg=msg, **kwargs)
            return output

        df_all_isotope = df[df["Element"] == particletype]
        all_A = df_all_isotope["A"].tolist()

        if nucleonnumber not in all_A:
            code = -1
            msg = (f"{particletype} does not have such an isotope. Its isotopes "
                   f"only exist with nucleon numbers of {all_A}.")
            kwargs.update({'particlerestmass': ""})
            output = format_output(code, msg=msg, **kwargs)
            return output

    df_filtered = df[(df["Element"] == particletype) & (df["A"] == nucleonnumber)]
    dict_rows = df_filtered.to_dict(orient='records')

    dict_rows = dict_rows[0]
    Mq = 931.4941024
    Me = 0.511

    def get_mass(Am, q):
        mass = Am * Mq - q * Me
        return mass

    Am = dict_rows["Am"]
    q = numofcharge
    particlerestmass = round(get_mass(Am, q), 5)
    kwargs.update({'particlerestmass': particlerestmass})
    output = format_output(**kwargs)
    return output


def get_atom(mode):
    # mode的选项， “common”， “all”
    kwargs = {}
    if mode == "common":
        v = ["H", "Cr", "Ar", "Ca", "Mn", "e+", "e-"]
        kwargs.update({'atomList': v})
        output = format_output(**kwargs)
        return output
    else:
        script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在文件夹的绝对路径
        parent_directory = os.path.dirname(script_directory)  # 获取上级目录的路径
        parent_directory = os.path.dirname(parent_directory)  # 获取上级目录的路径
        mass_csv_path = os.path.join(parent_directory, "staticfile", "atomic_masses.csv")
        df = pd.read_csv(mass_csv_path, index_col=None)

        Element_lis = df["Element"].tolist()
        unique_lst = list(dict.fromkeys(Element_lis))
        unique_lst.append("e+")
        unique_lst.append("e-")
        kwargs.update({'atomList': unique_lst})
        output = format_output(**kwargs)
        return output


def judge_if_is_avas_project(item):
    # item = {"projectPath": }
    # 这是一个初步的判断， 判断是否存在inputfile和outputfile
    project_path = item["projectPath"]
    inputfile_path = os.path.join(project_path, "InputFile")
    outputfile_path = os.path.join(project_path, "OutputFile")

    inputfile_exist = False
    outputfile_exist = False
    if os.path.exists(inputfile_path):
        inputfile_exist = True
    if os.path.exists(outputfile_path):
        outputfile_exist = True

    kwargs = {}
    if all([inputfile_exist, outputfile_exist]):
        kwargs.update({'projectPath': project_path})
        output = format_output(**kwargs)
    else:
        code = -1
        msg = f"{project_path} is not a  AVAS project"
        kwargs.update({'projectPath': project_path})
        output = format_output(code=code, msg=msg, **kwargs)
    return output

def get_file_choose_type(item):
    #item = {"ProjectPath":, "file_type"}
    default_item = {"projectPath": None, "fileType": None, "location": "out", "other_directory": None}
    default_item.update(item)

    file_type = default_item.get("fileType")
    project_path = default_item.get("projectPath")
    location = default_item.get("location")
    other_directory = default_item.get("other_directory")

    if location == "out":
        target_directory = os.path.join(project_path, "OutputFile")
    elif location == "in":
        target_directory = os.path.join(project_path, "InputFile")
    elif location == "other":
        target_directory = other_directory

    all_files = list_files_in_directory(target_directory)

    # print(all_files)
    can_choose_files = []
    if file_type.lower() == "errors_par":
        for i in all_files:
            v1 = re.findall("errors_par.txt", i)
            if len(v1)!= 0:
                can_choose_files.append(i)

    elif file_type.lower() == "density":
        for i in all_files:
            v1 = re.findall("density", i)
            if len(v1)!= 0:
                can_choose_files.append(i)


    elif file_type.lower() == "dst":
        for i in all_files:
            v1 = re.findall("dst", i)
            if len(v1)!= 0:
                can_choose_files.append(i)

    can_choose_files_relative = [i.split(r"/")[-1] for i in can_choose_files]

    kwargs = {}
    kwargs.update({'filesName': can_choose_files_relative})
    output = format_output(**kwargs)
    return output




if __name__ == '__main__':
    pass
    # item = {
    # "particletype": "H",
    # "nucleonnumber": 10,
    # "numofcharge":1
    # }
    # # res = cal_mass(item)
    # # print(res)
    # item = {"projectPath": r"E:\using\test_avas_qt\test_ini"}
    # res = judge_if_is_avas_project(item)
    # print(res)



    # res = get_atom(mode="all")
    # print(res)


    # item = {"fieldPath": r"C:\Users\shliu\Desktop\field"}
    # res = get_fieldname(item)
    # print(res)

    # dst_path = "E:\project\MEBT\RFQ_55_73_59_proton.dst"
    # item = {"dstPath": dst_path}
    # beam_parameter = cal_beam_parameter(item)
    # print(beam_parameter)
    #
    # path = r"E:\using\test_avas_qt\test_ini"
    # item = {"projectPath": path}
    # # res = create_from_file_input_ini(item)
    # param = {'project': {'project_path': '', 'fieldSource': 'E:\\using\\test_avas_qt\\test_ini\\field'},
    #  'lattice': {'length': 0}, 'input': {'sim_type': 'mulp'},
    #  'match': {'cal_input_twiss': 0, 'match_with_twiss': 0, 'use_initial_value': 0},
    #  'error': {'error_type': '', 'seed': 0, 'if_normal': 0}}
    # write_to_file_input_ini(item, param)
    # path = r"E:\using\test_avas_qt\cafe_avas\InputFile"
    # item = {"filePath": path }
    # res = get_bimap_name(item)
    # print(res)
    #
    # #
    # item = {"fieldPath": path }
    # res = get_fieldfile(item)
    # print(res)
    # projectPath = r"D:\using\test_avas_qt\cafe_avas"
    # #
    # # item = {"projectPath": projectPath, "fileType": "errors_par"}
    # # item = {"projectPath": projectPath, "fileType": "density"}
    # item = {"projectPath": projectPath, "fileType": "dst"}
    #
    # res = get_file_choose_type(item)
    # print(res)
    project_path = r"D:\using\test_avas_qt\test_ini"
    item = {
        "projectPath": project_path,
    }
    res = create_from_file_input_ini(item)
    print(res)
    # param = {'sim_type': 'mulp', 'scanphase': 1, 'spacecharge': 1, 'steppercycle': 50,
    #  'dumpperiodicity': 1, 'spacechargelong': None, 'spacechargetype': None,
    #  'scmethod': 'SPICNIC', 'fieldSource': '', "device": "cpu"}
    # res = write_to_file_input_ini(item, param)