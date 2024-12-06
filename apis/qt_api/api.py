from aftertreat.dataanalysis.percentemitt import PercentEmit
from utils.readfile import read_dst_fast
import os
import copy
from utils.tool import format_output

def cal_beam_parameter(item):
    dst_path = item["dstPath"]
    kwargs = {}

    try:
        beam_parameter = {}
        if os.path.exists(dst_path):
            dst_res = read_dst_fast(dst_path)
            beam_parameter['particlerestmass'] = dst_res['basemassinmev']
            beam_parameter['current'] = dst_res['ib']
            beam_parameter['particlebumber'] = dst_res['number']
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

    except Exception as e:
        code = -1
        msg = str(e)
        kwargs.update({'beamParams': {}})
        output = format_output(code, msg=msg, **kwargs)
        return output

    beam_parameter["readparticledistribution"] = ""
    beam_parameter["distribution_x"] = ""
    beam_parameter["distribution_y"] = ""
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

if __name__ == '__main__':
    dst_path = "E:\project\MEBT\RFQ_55_73_59_proton.dst"
    item = {"dstPath": dst_path}
    beam_parameter = cal_beam_parameter(item)
    print(beam_parameter)

    path = r"C:\Users\shliu\Desktop\field_ciads"
    item = {"projectPath": path}
    res = get_inputpath(item)
    print(res)