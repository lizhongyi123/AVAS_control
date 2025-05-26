from dataprovision.datasetparameter import DatasetParameter
import matplotlib.pyplot as plt
import numpy as np
path1 = r"C:\Users\shliu\Desktop\4292\OutputFile\DataSet.txt"

obj = DatasetParameter(path1)
obj.get_parameter()
x1 = obj.z
y1 = np.array(obj.x) *1000

# path2 = r"C:\Users\shliu\Desktop\新建文件夹 (3)\dataset4.txt"
# obj = DatasetParameter(path2)
# obj.get_parameter()
# x2 = obj.z
# y2 = obj.beta_z

plt.plot(x1,y1, color='red',linewidth = 8 )
# plt.plot(x2,y2, color='blue')
plt.show()