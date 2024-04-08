# -- coding: utf-8 --
from core.AVAS import AVAS

from aftertreat.picture.plotdataset import PlotDataSet
from aftertreat.picture.plotphase import PlotPhase
from aftertreat.dataanalysis.caltwiss import CalTwiss
from aftertreat.picture.ploterror import PlotError
from aftertreat.picture.plotenvbeamout import PlotEnvBeamOut

from apps.changeNp import ChangeNp
from aftertreat.picture.plotpicture import PlotCavityVoltage, PlotPhaseAdvance, PlotCavitySynPhase
from apps.matchtwiss import MatchTwiss
from apps.circlematch import CircleMatch
from apps.erroranalysis import ErrorAnalysis
import os
from utils.readfile import read_txt
from apps.basicenv import BasicEnvSim
from apps.LongAccelerator import LongAccelerator
from utils.tolattice import write_mulp_to_lattice_only_sim
########################################################################################################################

#下列为功能函数
#基础运行
def basic_mulp(project_path):
    """
    :param project_path:
    :return:
    多粒子模拟
    """
    latice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    res = read_txt(latice_mulp_path, out = 'list')

    sign = ''
    #判断是否需要矫正
    for i in res:
        if i[0] == 'adjust':
            sign = 'adjust'
            break

    if sign == 'adjust':
        v = ErrorAnalysis(project_path)
        res = v.only_adjust()

    #如果不需要矫正，则进行简单模拟
    else:
        AVAS_obj = AVAS(project_path)

        lattice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
        lattice_path = os.path.join(project_path, 'InputFile', 'lattice.txt')
        write_mulp_to_lattice_only_sim(lattice_mulp_path, lattice_path)
        res = AVAS_obj.run()
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


def err_dyn(project_path):
    """
    p跑动态误差, 静态误差将被注释掉
    :param project_path:
    :return:
    """
    v = ErrorAnalysis(project_path)
    res = v.run_err_dyn_all_group()
    print('动态误差结束')

    return res

def err_stat(project_path):
    """
    :param project_path:
    :return:
    根据是否有adjust命令判断是否需要优化
    """
    v = ErrorAnalysis(project_path)
    laatice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    res = read_txt(laatice_mulp_path, out = 'list')
    opti = False
    for i in res:
        if i[0] == 'adjust':
            opti = True
            break
    if opti:
        res = v.optimize_all_group()
        return res

    #不需要优化
    else:
        res = v.run_err_stat_all_group()
    print('静态误差结束')
    

def err_stat_dyn(project_path):
    """

    :param project_path:
    :return:
    动态误差和静态误差一起跑，
    """
    v = ErrorAnalysis(project_path)
    laatice_mulp_path = os.path.join(project_path, 'InputFile', 'lattice_mulp.txt')
    res = read_txt(laatice_mulp_path, out = 'list')
    opti = False
    for i in res:
        if i[0] == 'adjust':
            opti = True

    res = v.run_err_stat_dyn_all_group(opti)
    print('动态静态误差结束')

    return res

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
    return res


# #扫描
# def AVAS_scan(projectpath, scan_parameter, scan_start, scan_end, scan_step, scan_parameter_place):
#     AVAS_scan = Scan(projectpath, scan_parameter, scan_start, scan_end, scan_step, scan_parameter_place)
#     AVAS_scan_res = Scan.scan()
#     return avas_scan_res
#
# #误差分析
# def avas_error_analysis(error, dllpath, projectpath):
#     error_analysis = ErrorAnalysis(error, dllpath, projectpath)
#     error_analysis_res = error_analysis.run()
#     return error_analysis_res

########################################################################################################################

#下列为画图函数

#画dataset中的数据
def plot_dataset(project_path, picture_name, show_=1):
    """

    :param project_path:
    :param picture_name:
    :param show_:
    :return:
    dataset文件中数据的可视化
    """
    v = PlotDataSet(project_path, picture_name)
    v.get_x_y()
    res = v.run(show_)
    return res

#画相图
def plot_phase(dst_path, show_=1):
    v = PlotPhase(dst_path)
    res = v.run(show_)
    return res

def plot_cavity_voltage(project_path, ratio, show_=1):
    """

    :param project_path:
    :param ratio: {} 场名：比例
    :param show_:
    :return:
    腔压图
    """
    v = PlotCavityVoltage(project_path, ratio)
    v.get_x_y()
    res = v.run(show_)
    return res

def plot_cavity_syn_phase(project_path, show_=1):
    """

    :param project_path:
    :param show_:
    :return:
    腔体同步相位图
    """
    v = PlotCavitySynPhase(project_path)
    v.get_x_y()
    res = v.run(show_)
    return res

def plot_phase_advance(project_path, out_type, show_=1):
    """

    :param project_path:
    :param out_type:
    :param show_:
    :return:
    相移图
    """
    v = PlotPhaseAdvance(project_path)
    v.get_x_y(out_type)
    res = v.run(show_)
    return res

def plot_error(project_path, picture_name, picture_type, show_=1):
    """

    :param project_path:
    :param picture_name:
    :param picture_type:
    :param show_:
    :return:
    误差图
    """
    v = PlotError(project_path)
    v.get_x_y(picture_name, picture_type)
    res = v.run(show_)
    return res

def plot_env_beam_out(project_path, picture_name, show_=1):
    v =PlotEnvBeamOut(project_path)
    v.get_x_y(picture_name)
    res = v.run(show_)
    return res


################################################################################`#######################################
#下列为数据分析函数

#计算twiss参数
def cal_twiss(dst_path):
    v = CalTwiss(dst_path)
    res = v.get_emit_xyz()
    return res

if __name__ == '__main__':
    project_path = r'C:\Users\anxin\Desktop\tu_env'
    res = basic_env(project_path, 'InputFile\lattice_env.txt')
    # res = match_twiss(project_path)
    print(res)
