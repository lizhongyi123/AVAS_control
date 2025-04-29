# -- coding: utf-8 --
AVAS_control_path = r"D:\AVAS_CONTROL\AVAS_control"
import sys
sys.path.append(AVAS_control_path)
from core.MultiParticle import MultiParticle

from aftertreat.picture.plotdataset import PlotDataSet
from aftertreat.picture.plotphase import PlotPhase
from aftertreat.dataanalysis.caltwiss import CalTwiss
from aftertreat.picture.plotenvbeamout import PlotEnvBeamOut

from apps.changeNp import ChangeNp
from aftertreat.picture.plotpicture import PlotCavityVoltage, PlotPhaseAdvance, PlotCavitySynPhase
from apps.matchtwiss import MatchTwiss
from apps.circlematch import CircleMatch
from aftertreat.picture.plotacc import PlotAcc
from apps.calacceptance import Acceptance
import os
from utils.readfile import read_txt
from apps.basicenv import BasicEnvSim
from apps.LongAccelerator import LongAccelerator
from utils.tolattice import write_mulp_to_lattice_only_sim2
from apps.error import Errorstat, ErrorDyn, Errorstatdyn, OnlyAdjust

from aftertreat.picture.ploterror import PlotErrout, PlotErr_emit_loss
from aftertreat.picture.plotdesnsity import PlotDensity, PlotDensityLevel, PlotDensityProcess

########################################################################################################################
import multiprocessing
from apis.qt_api.judge_lattice import JudgeLattice
from aftertreat.picture.plotphaseellipse import PlotPhaseEllipse
from utils.tool import format_output, generate_web_picture_param, generate_web_picture_path
import uuid
from apps.diaginfo import DiagInfo
from aftertreat.dataanalysis.extodensity import  ExtoDensity
from utils.inputconfig import InputConfig
#下列为功能函数
#基础运行
def basic_mulp(**item):
    """
    :param project_path:
    :return:
    多粒子模拟
    """

    # else:
    project_path = item.get('project_path')

    multiparticle_obj = MultiParticle(item)

    lattice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    lattice_path = os.path.join(project_path, 'InputFile', 'lattice.txt')
    write_mulp_to_lattice_only_sim2(lattice_mulp_path, lattice_path)

    res = multiparticle_obj.run()

    #生成束诊文件
    diag_item = {
        "project_path": project_path,
        "input_file": os.path.join(project_path, 'InputFile'),
        "output_file": os.path.join(project_path, 'OutputFile'),
        "diag_file_path": os.path.join(project_path, 'OutputFile', 'par_diag1.txt'),
    }
    obj = DiagInfo(diag_item)
    obj.write_diag_info_to_file()

    #
    item = { "projectPath": project_path,}
    input_info = InputConfig()
    input_info = input_info.create_from_file(item)
    input_info = input_info["data"]["inputParams"]


    if input_info.get("outputcontrol_start") == 1 and input_info.get("outputcontrol_grid") > 0:
    #生成密度文件
        exdata_path = os.path.join(project_path, "OutputFile", "ExData.edt")

        dataset_path = os.path.join(project_path, "OutputFile", "DataSet.txt")
        target_density_path = os.path.join(project_path, "OutputFile", f"density_par.dat")

        density_obj = ExtoDensity(exdata_path, dataset_path, target_density_path)
        density_obj.generate_density_file_onestep(1)

    print('模拟结束')
    return res

#粒子数扩充
def change_particle_number(infile_path, outfile_path, ratio):

    """
    :param infile_path: 输入
    :param outfile_path: 输出
    :param ratio: 扩大的比例
    :return:
    扩充经粒子数
    """
    v = ChangeNp(infile_path, outfile_path, ratio)
    v.run()
    return None

def match_twiss(project_path, use_lattice_initial_value=0):
    """
    twiss参数匹配
    :param project_path:
    :param use_lattice_initial_value:
    :return:
    """
    v = MatchTwiss(project_path)
    res = v.match_twiss(r"lattice_env.txt", use_lattice_initial_value)
    print('匹配结束')

    return res

def circle_match(project_path):
    """
    周期匹配
    :param project_path:
    :return:
    """
    v = CircleMatch(project_path)
    res = v.circle_match(r"lattice_env.txt")
    print('匹配结束')
    return res


def err_dyn(**item):
    """
    p跑动态误差, 静态误差将被注释掉
    :param project_path:
    :return:
    """
    default_item = {
        "project_path": None,
        "seed": 50,
        "if_normal": 1,
        "field_path": None,
        "if_generate_density_file":1
    }
    default_item.update(item)
    v = ErrorDyn(default_item)
    res = v.run()
    print('动态误差结束')

    return res

def err_stat(**item):
    """
    :param project_path:
    :return:
    根据是否有adjust命令判断是否需要优化
    """
    default_item = {
        "project_path": None,
        "seed": 50,
        "if_normal": 1,
        "field_path": None,
        "if_generate_density_file":1
    }
    default_item.update(item)
    v = Errorstat(default_item)
    v.run()
    

def err_stat_dyn(**item):
    """

    :param project_path:
    :return:
    动态误差和静态误差一起跑，
    """
    default_item = {
        "project_path": None,
        "seed": 50,
        "if_normal": 1,
        "field_path": None,
        "if_generate_density_file":1
    }
    default_item.update(item)
    v = Errorstatdyn(default_item)
    v.run()
    return None

def basic_env(project_path, lattice):
    """

    :param project_path:
    :param lattice:
    :return:
    基础包络模拟
    """
    obj = BasicEnvSim(project_path, lattice)
    res = obj.run()
    return res

def longdistance( project_path, kind):
    obj = LongAccelerator(project_path, kind)
    obj.run()
    return None

def cal_acceptance(project_path, kind):
    obj = Acceptance(project_path)
    emit, norm_emit, x_min, xx_min = obj.cal_accptance(kind)
    return emit, norm_emit, x_min, xx_min

def plot_acc(project_path, kind):
    obj = PlotAcc(project_path)
    res = obj.run(kind)
    return res


#下列为画图函数

#画dataset中的数据
# def plot_dataset(project_path, picture_type, show_=1, fig=None, platform = "qt"):
#
#     """
#     :param project_path:
#     :param picture_name:
#     :param show_:
#     :return:
#     dataset文件中数据的可视化
#     """
#     dataset_path = os.path.join(project_path, "OutputFile", "dataset.txt")
#     v = PlotDataSet(dataset_path, picture_type)
#     v.get_x_y()
#     res = v.run(show_, fig)
#     return res


def plot_dataset(**item):
    #item = {project_path: , picture_type: , show_: 1, fig: None, platform: "qt", "sample_interval": 1}
    """
    :param project_path:
    :param picture_name:
    :param show_:
    :return:
    dataset文件中数据的可视化
    """
    default_item = {"projectPath": None, "pictureType": None, "show_": 0, "fig": None, "platform": "qt", "sampleInterval": 1,
                    "needData": False
                    }

    default_item.update(item)

    project_path = default_item.get("projectPath")
    picture_type = default_item.get("pictureType")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    sample_interval = default_item.get("sampleInterval")
    webreturn_type = default_item.get("webreturnType")
    need_data = default_item.get("needData")

    dataset_path = os.path.join(project_path, "OutputFile", "dataset.txt")
    v = PlotDataSet(dataset_path, picture_type, sample_interval)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)

    elif platform == "web":
        #生成文件名
        save_path = generate_web_picture_path(project_path)
        v.run(show_, fig, save_path)

        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            data = generate_web_picture_param(v)
            picture_param["pictureInfo"] = data

        output = format_output(**picture_param)

    return output



#画相图
# def plot_phase(dst_path, show_=1, fig = None, platform = "qt"):
#     v = PlotPhase(dst_path)
#     res = v.run(show_, fig)
#     return res

def plot_phase(**item):

    default_item = {"filePath": None, "pictureType": "xx1", "show_": 0, "fig": None, "platform": "qt",
                    "sampleInterval": 1, "needData": False, "projectPath": None, "location": "out"}

    default_item.update(item)
    platform = default_item.get("platform")
    project_path = default_item.get("projectPath")
    fig = default_item.get("fig")
    sample_interval = default_item.get("sampleInterval")
    location = default_item.get("location")
    show_ = default_item.get("show_")

    if platform == "qt":
        file_path = default_item.get("filePath")
    elif platform == "web":
        if location == "out":
            file_path = os.path.join(project_path, "OutputFile", default_item.get("filePath"))
        elif location == "in":
            file_path = os.path.join(project_path, "InputFile", default_item.get("filePath"))


    v = PlotPhase(file_path)

    if platform == "qt":
        output = v.run(show_, fig)
    elif platform == "web":
        try:
            save_path = generate_web_picture_path(project_path)
            v.run(show_, fig, save_path)
            picture_param = {"picturePath": save_path}
            output = format_output(**picture_param)
        except Exception as e:
            code = -1
            msg = str(e)
            picture_param = {"picturePath": ""}
            output = format_output(code, msg=msg, **picture_param)
    return output

def plot_cavity_voltage(project_path, ratio, show_=1, fig = None, platform = "qt"):

    """
    :param project_path:
    :param ratio: {} 场名：比例
    :param show_:
    :return:
    腔压图
    """

    lattice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    v = PlotCavityVoltage(lattice_mulp_path, ratio)
    v.get_x_y()
    res = v.run(show_, fig)
    return res

# def plot_cavity_syn_phase(project_path, show_=1, fig = None, platform = "qt"):
#     # item = {project_path, show_=1, fig = None, platform = "qt"}
#     """
#
#     :param project_path:
#     :param show_:
#     :return:
#     腔体同步相位图
#     """
#     v = PlotCavitySynPhase(project_path)
#     v.get_x_y()
#     res = v.run(show_, fig)
#     return res
def plot_cavity_syn_phase(**item):
    # item = {project_path, show_=1, fig = None, platform = "qt"}

    """

    :param project_path:
    :param show_:
    :return:
    腔体同步相位图
    """

    default_item = {"projectPath": None, "show_": 0, "fig": None, "platform": "qt", "needData": False}
    default_item.update(item)

    project_path = default_item.get("projectPath")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    need_data = default_item.get("needData")

    lattice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    v = PlotCavitySynPhase(lattice_mulp_path)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)

    elif platform == "web":

        #生成文件名
        save_path = generate_web_picture_path(project_path)

        v.run(show_, fig, save_path)

        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            data = generate_web_picture_param(v)
            picture_param["pictureInfo"] = data

        output = format_output(**picture_param)

    return output



def plot_phase_advance(**item):
    """
    :param project_path:
    :param out_type:
    :param out_type:
    :param show_:
    :return:
    相移图
    """
    # item = {project_path, picture_type, show_ = 1, fig = None, platform = "qt"}
    default_item = {"projectPath": None, "pictureType": "period", "show_": 0, "fig": None,
                    "platform": "qt", "nnedData": False}
    default_item.update(item)

    project_path = default_item.get("projectPath")
    picture_type = default_item.get("pictureType")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    need_data = default_item.get("needData")
    v = PlotPhaseAdvance(project_path, picture_type)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)
    elif platform == "web":
        #生成文件名
        save_path = generate_web_picture_path(project_path)

        v.run(show_, fig, save_path)

        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            data = generate_web_picture_param(v)
            picture_param["pictureInfo"] = data

        output = format_output(**picture_param)
    return output

def plot_error_out(**item):
    """
    :param project_path:
    :param picture_name:
    :param picture_type:
    :param show_:
    :return:
    误差图
    """
    default_item = {"filePath": None,
                    "statMethod": "average",
                    "pictureType": "xy",
                    "show_": 0, "fig": None, "platform": "qt",
                    "needData": False, "projectPath": None}

    default_item.update(item)


    stat_method = default_item.get("statMethod")
    picture_type = default_item.get("pictureType")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    need_data = default_item.get("needData")
    project_path = default_item.get("projectPath")
    if platform == "qt":
        file_path = default_item.get("filePath")
    elif platform == "web":
        file_path = os.path.join(project_path, 'outputFile', default_item.get("filePath"))

    v = PlotErrout(file_path, stat_method, picture_type)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)
    elif platform == "web":
        #生成文件名
        save_path = generate_web_picture_path(project_path)
        output = v.run(show_, fig, save_path)

        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            data = generate_web_picture_param(v)
            picture_param["pictureInfo"] = data

        output = format_output(**picture_param)


    return output


def plot_error_emit_loss(**item):
    """
    :param project_path:
    :param picture_name:
    :param picture_type:
    :param show_:
    :return:
    误差图
    """
    default_item = {"filePath": None, "pictureType": "par", "show_": 0, "fig": None,
                    "platform": "qt", "needData":False, "projectPath": None}
    default_item.update(item)

    picture_type = default_item.get("pictureType")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    need_data = default_item.get("needData")
    project_path = default_item.get("projectPath")

    if platform == "qt":
        file_path = default_item.get("filePath")
    elif platform == "web":
        file_path = os.path.join(project_path, 'outputFile', default_item.get("filePath"))

    v = PlotErr_emit_loss(file_path, picture_type)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)

    elif platform == "web":
        #生成文件名
        save_path = generate_web_picture_path(project_path)
        v.run(show_, fig, save_path)
        
        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}
        if need_data is True:
            pictureInfo = {}
            pictureInfo["labelx"] = v.xlabel
            pictureInfo["labely1"] = v.ylabel1
            pictureInfo["labely2"] = v.ylabel2
    
            pictureInfo["datax1"] = v.xy["ax1_x"]
            pictureInfo["datay1"] = v.xy["ax1_y"]
    
            pictureInfo["datax2"] = v.xy["ax2_x"]
            pictureInfo["datay2"] = v.xy["ax2_y"]
    
            pictureInfo["legends1"] = v.labels1
            pictureInfo["legend2"] = v.labels2
            
            picture_param["pictureInfo"] = pictureInfo

        output = format_output(**picture_param)
        # except Exception as e:
        #     code = -1
        #     msg = str(e)
        #     kwargs.update(pictureParam)
        #     output = format_output(code, msg=msg, **kwargs)
    return output

def plot_density(**item):
    default_item = {"filePath": None, "desnityPlane": "x", "show_": 0, "fig": None, "platform": "qt",
                    "sampleInterval": 1, "needData": False, "projectPath": None}

    default_item.update(item)

    file_path = default_item.get("filePath")
    picture_type = default_item.get("desnityPlane")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    sample_interval = default_item.get("sampleInterval")
    need_data = default_item.get("needData")
    project_path = default_item.get("projectPath")
    
    v = PlotDensity(file_path, picture_type, sample_interval)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)
    elif platform == "web":
        save_path = generate_web_picture_path(project_path)
        output = v.run(show_, fig, save_path)

        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            pictureInfo = {}
            pictureInfo["labelx"] = v.xlabel
            pictureInfo["labely"] = v.ylabel
            pictureInfo["z_m"] = v.z_m.tolist()
            pictureInfo["y_m"] = v.y_m.tolist()
            pictureInfo["density_m"] = v.density_m.tolist()
            pictureInfo["legends"] = [None]
            picture_param["pictureInfo"] = pictureInfo

        output = format_output(**picture_param)


    return output


def plot_density_level(**item):
    default_item = {"filetath": None, "desnityPlane": "x", "show_": 0, "fig": None, "platform": "qt",
                    "sampleInterval": 1, "needData": False, "projectPath": None}

    default_item.update(item)

    file_path = default_item.get("filePath")
    picture_type = default_item.get("desnityPlane")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    sample_interval = default_item.get("sampleInterval")
    need_data = default_item.get("needData")
    project_path = default_item.get("projectPath")

    v = PlotDensityLevel(file_path, picture_type, sample_interval)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)

    elif platform == "web":
        save_path = generate_web_picture_path(project_path)

        #运行并保存图片
        v.run(show_, fig, save_path)

        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            data = generate_web_picture_param(v)
            picture_param["pictureInfo"] = data

        output = format_output(**picture_param)

    return output


def plot_density_process(**item):

    #density_plane = ["x", "y", "r", "z"]
    #picture_type = [
    #"centroid"
    #"emit",
    # rms_size, rms_size_max,
    #lost, maxlost, minlost,
    # ]

    default_item = {"filePath": None, "desnityPlane": "x", "pictureType": "centroid", "show_": 0, "fig": None, "platform": "qt",
                    "sampleInterval": 1, "needData": False, "projectPath": None}

    default_item.update(item)

    file_path = default_item.get("filePath")
    density_plane = default_item.get("desnityPlane")
    picture_type = default_item.get("pictureType")
    show_ = default_item.get("show_")
    fig = default_item.get("fig")
    platform = default_item.get("platform")
    sample_interval = default_item.get("sampleInterval")
    need_data = default_item.get("needData")
    project_path = default_item.get("projectPath")

    v = PlotDensityProcess(file_path, density_plane, picture_type, sample_interval)
    v.get_x_y()

    if platform == "qt":
        output = v.run(show_, fig)
    elif platform == "web":
        #生成文件名
        save_path = generate_web_picture_path(project_path)

        v.run(show_, fig, save_path)

        #生成返回信息
        picture_param = {"picturePath": save_path, "pictureInfo": {}}

        if need_data is True:
            data = generate_web_picture_param(v)
            picture_param["pictureInfo"] = data

        output = format_output(**picture_param)

    return output

    return res

def plot_density_transport(**item):
    default_item = {"filePath": None, "desnityPlane": "x", "pictureType": "density", "show_": 0, "fig": None, "platform": "qt",
                    "sampleInterval": 1, "needData": False, "projectPath": None}

    default_item.update(item)

    project_path = default_item.get("projectPath")
    platform = default_item.get("platform")
    if platform == "qt":
        file_path = default_item.get("filePath")
    elif platform == "web":
        file_path = os.path.join(project_path, 'outputFile', default_item.get("filePath"))

    picture_type = default_item.get("pictureType")
    process_type = ["centroid", "emit", "rms_size", "rms_size_max"]
    if picture_type == "density":
        res = plot_density(**item)

    elif picture_type == "density_level":
        res = plot_density_level(**item)

    elif picture_type in process_type:
        res = plot_density_process(**item)
    return res
def plot_phase_ellipse(parameter_item, picture_type, show_=1, fig = None, platform = "qt"):
    obj = PlotPhaseEllipse()
    obj.get_x_y(picture_type, parameter_item)
    res = obj.run(show_, fig)
    return res




def plot_env_beam_out(project_path, picture_name, show_=1, fig = None):
    v =PlotEnvBeamOut(project_path)
    v.get_x_y(picture_name)
    res = v.run(show_, fig)
    return res


################################################################################`#######################################
#下列为数据分析函数

#计算twiss参数
def cal_twiss(dst_path):
    v = CalTwiss(dst_path)
    res = v.get_emit_xyz()
    return res


def judge_opti(res):

    sign = []
    # 判断是否需要矫正
    for i in res:
        if i[0] == 'adjust':
            sign.append('adjust')
        elif i[0].startswith('diag'):
            sign.append('diag')

    # 如果这两个都包含,
    if 'adjust' in sign and 'diag' in sign:
        return 1
    else:
        return 0

if __name__ == '__main__':

    path = r"C:\Users\shliu\Desktop\11\hebt_avas"
    item = {"project_path": path}
    res = basic_mulp(**item)

    # path = r"D:\using\test_avas_qt\cafe_avas"
    # item = {
    #     "projectPath": path,
    #     "pictureType": "meter",
    #     "platform": "web",
    #     "show_": 0,
    #     "needData": True
    #
    # }
    # res = plot_phase_advance(**item)
    # print(res)

    # item = {
    #     "projectPath": path,
    #     "platform": "web",
    #     # "show_": 1
    #     "needData": True
    # }
    # res = plot_cavity_syn_phase(**item)
    # print(res)



    # item = {
    #     "projectPath": path,
    #     "pictureType": "rms_x",
    #     "platform": "web",
    #     "sampleInterval": 1000,
    #     "show_": 0,
    #     "needData": True,
    # }
    #
    # res = plot_dataset(**item)
    # print(res)


    # item = {
    #     "filePath": r"errors_par.txt",
    #     "platform": "web",
    #     "show_": 0,
    #     "needData": False,
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas"
    # }
    # res = plot_error_emit_loss(**item)
    # print(res)


    # item = {
    #     "filePath": r"errors_par.txt",
    #     "statMethod": "average",
    #     "pictureType": "xy",
    #     "platform": "web",
    #     "show_": 0,
    #     "needData": True,
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas"
    # }
    # res = plot_error_out(**item)
    # print(res)



    # item = {
    #     "filePath": r"D:\using\test_avas_qt\cafe_avas\OutputFile\errors_par.txt",
    #     "platform": "web",
    #     "show_": 0,
    #     "needData": True,
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas"
    # }
    # res = plot_error_emit_loss(**item)
    # print(res)

    # item = {
    #     "filePath": r"D:\using\test_avas_qt\cafe_avas\OutputFile\density_par_0_0.dat",
    #     "pictureType": "x",
    #     "platform": "web",
    #     "show_": 0,
    #     "sampleInterval": 100,
    #     "needData": True,
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas"
    # }

    #
    # res = plot_density(**item)
    # print(res)

    # item = {
    #     "filePath": r"D:\using\test_avas_qt\cafe_avas\OutputFile\density_par_0_0.dat",
    #     "pictureType": "x",
    #     "platform": "web",
    #     "show_": 0,
    #     "sampleInterval": 1000,
    #     "needData": True,
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas"
    # }
    #
    # res = plot_density_level(**item)
    # print(res)

    # item = {
    #     "filePath": r"D:\using\test_avas_qt\cafe_avas\OutputFile\density_par_0_0.dat",
    #     "desnityPlane": "x",
    #     "pictureType": "density_level",
    #     "platform": "web",
    #     "show_": 0,
    #     "sampleInterval": 1,
    #     "needData": False,
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas"
    # }
    #
    #
    # res = plot_density_transport(**item)
    # print(res)
    # "filePath": r"inData.dst",
    #"filePath": r"part_rfq.dst",
    # item = {
    #     "filePath": r"inData.dst",
    #     "platform": "web",
    #     "projectPath": r"D:\using\test_avas_qt\cafe_avas",
    #     "location": "out"
    # }
    #
    #
    # res = plot_phase(**item)
    # print(res)