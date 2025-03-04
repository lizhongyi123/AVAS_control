import global_varible
from utils.readfile import read_txt, read_lattice_mulp
def write_mulp_to_lattice_only_sim(lattice_mulp_path, lattice_path):
    """
    :param lattice_mulp_path:
    :param lattice_path:
    :return: None
    该函数的作用是将lattice_mulp中的内容写的入到lattice, 处理的情况为只进行多粒子模拟，不包含误差，矫正等
    """
    lattice_mulp = read_lattice_mulp(lattice_mulp_path)
    lattice_mulp = [i for i in lattice_mulp if i[0] in global_varible.mulp_basic_command]
    with open(lattice_path, 'w', encoding='utf-8') as f:
        for i in lattice_mulp:
            f.write(' '.join(map(str, i)) + '\n')



