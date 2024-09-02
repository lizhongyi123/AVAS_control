from core.MultiParticle import MultiParticle
import os
import shutil
#将lattice_mulp中复制到lattice中
from utils.readfile import read_txt
from utils.treat_directory import list_files_in_directory


def test_err_dyn831(project_path):
    lattice_mulp_path = os.path.join(project_path, "InputFile", "lattice_mulp.txt")
    lattice_path = os.path.join(project_path, "InputFile", "lattice.txt")

    lattice_mulp = read_txt(lattice_mulp_path, out='list')

    with open(lattice_path, 'w', encoding='utf-8') as f:
        for i in lattice_mulp:
            f.write(' '.join(map(str, i)) + '\n')

    obj = MultiParticle(project_path)
    obj.run()
    print("模拟结束")

    path0 = os.path.join(project_path, "OutputFile", "output_0")
    path1 = os.path.join(project_path, "OutputFile")

    res = list_files_in_directory(path0)
    for i in res:
        shutil.copy(i, path1)

if __name__ == "__main__":
    project = r"C:\Users\anxin\Desktop\teat831"
    test_err_dyn831(project)