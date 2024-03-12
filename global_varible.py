
c_light = 299792458
long_element = ['drift', 'field', 'quad', 'quad', 'solenoid', 'bend', 'steer']


error_elemment_command = ['err_quad_ncpl_stat', 'err_quad_ncpl_dyn', 'err_cav_ncpl_stat', 'err_cav_ncpl_dyn', ]

error_elemment_command_stat = ['err_quad_ncpl_stat', 'err_cav_ncpl_stat']
error_elemment_command_dyn = ['err_quad_ncpl_dyn', 'err_cav_ncpl_dyn']

error_elemment_command_quad = ['err_quad_ncpl_stat', 'err_quad_ncpl_dyn']
error_elemment_command_cav = ['err_cav_ncpl_stat', 'err_cav_ncpl_dyn', ]

error_beam_command = ['err_beam_stat', 'err_beam_dyn']
error_beam_stat = ['err_beam_stat']
error_beam_dyn = ['err_beam_dyn']

error_elemment_dyn_on = ['err_quad_dyn_on', 'err_cav_dyn_on']
error_elemment_stat_on = ['err_quad_stat_on', 'err_cav_stat_on']

error_beam_dyn_on = ['err_beam_dyn_on']
error_beam_stat_on = ['err_beam_stat_on']

avas_command = long_element + \
               ['start', 'end', 'superpose', 'superposeend', ] \
                + error_elemment_command + error_beam_command  \
                + error_elemment_dyn_on + error_elemment_stat_on + error_beam_dyn_on + error_beam_stat_on

control_command = ['adjust', 'lattice', 'lattice_end']

greek_letters_upper = {'alpha': '\u0391', 'beta': '\u0392', 'gamma': '\u0393', 'phi': '\u03A6'}

