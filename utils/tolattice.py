import global_varible
from utils.readfile import read_txt
def write_mulp_to_lattice(lattice_mulp_path, lattice_path):
    """

    :param lattice_mulp_path:
    :param lattice_path:
    :return: None
    该函数的作用是将lattice_mulp中的内容写的入到lattice
    """
    lattice_mulp = read_txt(lattice_mulp_path, out='list')
    lattice_mulp = [i for i in lattice_mulp if i[0] in global_varible.avas_command]
    with open(lattice_path, 'w', encoding='utf-8') as f:
        for i in lattice_mulp:
            f.write(' '.join(map(str, i)) + '\n')



