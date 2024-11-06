from aftertreat.dataanalysis.percentemitt import PercentEmit
from utils.readfile import read_dst_fast
import os


def cal_beam_parameter(dst_path):
    if not os.path.exists(dst_path):
        pass
    beam_parameter = {}
    # beam_parameter_keys = ['readparticledistribution', 'numofcharge', 'particlerestmass',
    #                             'current', 'particlenumber', 'frequency',
    #                             'kneticenergy', 'alpha_x', 'beta_x', 'emit_x',
    #                             "alpha_y", "beta_y", "emit_y",
    #                             "alpha_z", "beta_z", "emit_z",
    #                             'distribution_x', 'distribution_y']


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
    return beam_parameter


if __name__ == '__main__':
    dst_path = "E:\project\MEBT\RFQ_55_73_59_proton.dst"
    beam_parameter = cal_beam_parameter(dst_path)
    print(beam_parameter)
