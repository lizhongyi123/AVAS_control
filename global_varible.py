
c_light = 299792458
Pi = 3.14159265358979323846
long_element = ['drift', 'field', 'quad', 'solenoid', 'bend', 'steer']


error_elemment_command = ['err_quad_ncpl_stat', 'err_quad_ncpl_dyn', 'err_cav_ncpl_stat', 'err_cav_ncpl_dyn', ]
#静态动态
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

mulp_basic_command = long_element + \
               ['start', 'end', 'superpose', 'superposeend', ]

mulp_control_command = ['adjust', 'lattice', 'lattice_end']

greek_letters_upper = {'alpha': '\u0391', 'beta': '\u0392', 'gamma': '\u0393', 'phi': '\u03A6'}

