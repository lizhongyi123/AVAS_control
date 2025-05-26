
from utils.beamconfig import BeamConfig
from apis.basic_api.api import basic_mulp

#修改beam文件
item = {"projectPath": r"C:\test1",
}

#读取现在的参数
obj = BeamConfig()
res = obj.create_from_file(item)

#设置参数
param =  {'current': None, "alpha_x": None, "beta_x": None, "emit_x": None,"alpha_y": None, "beta_y": None, "emit_y": None,"alpha_z": None, "beta_z": None, "emit_z": None }
#设置参数

#保存参数
res =  obj.set_param(**param)
#将参数写入文件
res = obj.write_to_file(item)

#修改完参数后进行模拟
item = {"projectPath": r"C:\test1",
}
basic_mulp(item)

#束损可以再输出文件中的dataset.txt，可以每次保存dataset文件，也可每次读取，把结果记录下来
#保存结果