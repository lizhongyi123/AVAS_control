
from utils.beamconfig import BeamConfig
from apis.basic_api.api import basic_mulp

#�޸�beam�ļ�
item = {"projectPath": r"C:\test1",
}

#��ȡ���ڵĲ���
obj = BeamConfig()
res = obj.create_from_file(item)

#���ò���
param =  {'current': None, "alpha_x": None, "beta_x": None, "emit_x": None,"alpha_y": None, "beta_y": None, "emit_y": None,"alpha_z": None, "beta_z": None, "emit_z": None }
#���ò���

#�������
res =  obj.set_param(**param)
#������д���ļ�
res = obj.write_to_file(item)

#�޸�����������ģ��
item = {"projectPath": r"C:\test1",
}
basic_mulp(item)

#�������������ļ��е�dataset.txt������ÿ�α���dataset�ļ���Ҳ��ÿ�ζ�ȡ���ѽ����¼����
#������