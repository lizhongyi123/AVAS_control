from aftertreat.dataanalysis.percentemitt import PercentEmit
from utils.readfile import read_dst_fast
import os
import copy
from utils.tool import format_output
from utils.treat_directory import list_files_in_directory

from utils.iniconfig import IniConfig
from utils.inputconfig import InputConfig
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
    #item = {"projectPath": "fdasf" }
    kwargs = {}
    input_path = os.path.join(item["projectPath"], "InputFile")
    kwargs.update({'inputFilePath': input_path})
    output = format_output(**kwargs)
    return output


#获取上传位置
def get_upload_path(item):
    #item = {"projectPath": "fdasf", fileType, " "}
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

#得到模拟进度

def get_fieldname(item):
    kwargs = {}
    fieldpath = item["fieldPath"]
    all_files = list_files_in_directory(fieldpath)
    suffix_list = ["edx", "edy", "edz", "bdx", "bdy", "bdz",
                   "bsx", "bsy", "bsz"
                   ]
    all_files = [i for i in all_files if i.split(".")[-1] in suffix_list]
    v = [i.split("\\")[-1] for i in all_files]
    v= [i.split(".")[0] for i in v]
    field_name = list(set(v))
    kwargs.update({'fieldName': field_name})
    output = format_output(**kwargs)
    return output

def get_bimap_name(item):
    kwargs = {}
    fieldpath = item["filePath"]
    all_files = list_files_in_directory(fieldpath)
    suffix_list = ["csv"
                   ]
    all_files = [i for i in all_files if i.split(".")[-1] in suffix_list]
    v = [i.split("\\")[-1] for i in all_files]
    v = [i.split(".")[0] for i in v]
    bimap_name = list(set(v))
    kwargs.update({'bimapName': bimap_name})
    output = format_output(**kwargs)
    return output

def get_fieldfile(item):
    kwargs = {}
    fieldpath = item["fieldPath"]
    all_files = list_files_in_directory(fieldpath)
    suffix_list = ["edx", "edy", "edz", "bdx", "bdy", "bdz",
                   "bsx", "bsy", "bsz"
                   ]
    all_files = [i for i in all_files if i.split(".")[-1] in suffix_list]
    v = [i.split("\\")[-1] for i in all_files]
    kwargs.update({'fieldFile': v})
    output = format_output(**kwargs)
    return output

def get_allfile_relative_path(item):
    kwargs = {}
    fieldpath = item["filePath"]
    all_files = list_files_in_directory(fieldpath)
    v = [i.split("\\")[-1] for i in all_files]
    kwargs.update({'allFile': v})
    output = format_output(**kwargs)
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
    fieldSource_dic = {'fieldSource': ini_res["data"]["iniParams"]["project"]["fieldSource"]}
    new_dic.update(fieldSource_dic)


    kwargs.update({'inputiniParams': new_dic})
    output = format_output(**kwargs)
    print(output)
    return output

def write_to_file_input_ini(item, param):
    # item的格式{“projectPath”： “path”}
    # {'sim_type': 'mulp', 'scanphase': 1, 'spacecharge': 1, 'steppercycle': 50,
    #  'dumpperiodicity': 1, 'spacechargelong': None, 'spacechargetype': None,
    #  'scmethod': 'SPICNIC', 'fieldSource': ''}
    kwargs = {}

    input_param = copy.deepcopy(param)
    del input_param["fieldSource"]

    ini_param = {"project": {"fieldSource": param["fieldSource"]}}

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

    input_obj.write_to_file(item)
    ini_obj.write_to_file(item)

    new_dic = param
    kwargs.update({'inputiniParams': new_dic})
    output = format_output(**kwargs)
    return output

# def set_input_ini(item):
#     project_path =


if __name__ == '__main__':
    # item = {"fieldPath": r"C:\Users\shliu\Desktop\field"}
    # res = get_fieldname(item)
    # print(res)

    # dst_path = "E:\project\MEBT\RFQ_55_73_59_proton.dst"
    # item = {"dstPath": dst_path}
    # beam_parameter = cal_beam_parameter(item)
    # print(beam_parameter)
    #
    path = r"E:\using\test_avas_qt\test_ini"
    item = {"projectPath": path}
    res = create_from_file_input_ini(item)
    params = {'sim_type': 'mulp', 'scanphase': 1, 'spacecharge': 1, 'steppercycle': 50,
               'dumpperiodicity': 1, 'spacechargelong': None, 'spacechargetype': None,
               'scmethod': 'SPICNIC', 'fieldSource': None}

    write_to_file_input_ini(item, params)