from utils.readfile import read_txt
import pandas as pd
def is_int(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


file_path = r"C:\Users\shliu\Desktop\mass_1.mas20.txt"

res = read_txt(file_path, out="list", case_sensitive=True)[1:]
for i in res:
    if i[-4] == "*":
        i.insert(-3, "*")
#正常情况，第四个值是A，第五个值是 El，
#异常情况  第3个值是A， 第四个值El，
#如果第四个值可以转换为整数，那就是有0情况，如果不能，那就是无0情况
for i in res:
    v = is_int(i[4])
    if v is True:
        pass
    else:
        i.insert(0, 0)

#处理没有组成的情况
for i in res:
    if len(i) == 16:
        i.insert(6, "**")

#把Am中的#号改变
for i in res:
    if "#" in i[-2]:
        i[-2] = i[-2].replace("#", ".0")
A_lis = []  #核子数
element_lis = []  #同位素名称
Z_lis = []     #质子数
N_lis = []  #中子数
Am_lis = []   #Mq的倍数
for i in res:
        A_lis.append(int(i[4]))
        Z_lis.append(int(i[3]))
        N_lis.append(int(i[2]))
        element_lis.append(i[5])
        am = i[-3] + "." + i[-2].replace(".", "")
        Am_lis.append(float(am))
all_dict = {
    "Element": element_lis,
    "A": A_lis,
    "Z": Z_lis,
     "N":N_lis,
    "Am": Am_lis
}

df = pd.DataFrame(all_dict)
df.to_csv('atomic_masses.csv', index=False)

print(df)

