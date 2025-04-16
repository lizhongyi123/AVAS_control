path = r"E:\using\test_avas_qt\test_adjust\outputFile\Diag_Datas_1_1.txt"
from utils.readfile import read_txt
res = read_txt(path, out="list", case_sensitive=None)
print(res)