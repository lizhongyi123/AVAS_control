import sys
import time
import platform
import subprocess
import os
import re
# sys.path.append(r'E:\AVAS_CONTROL\AVAS_control')

from core.MultiParticleEngine import MultiParticleEngine
import multiprocessing
class MultiParticle():
    """
    多粒子模拟
    """
    def __init__(self, item):  # *arg **kwargs #dllpath写死
        self.project_path = item["project_path"]
        self.input_file = item.get("input_file")
        self.output_file = item.get("output_file")
        self.field_file = item.get("field_file")
        self.errorlog_path = item.get("errorlog_path")
        self.multiparticle_engine = item.get("mulp_engine")

        if self.input_file is None:
            self.input_file = os.path.join(self.project_path, "InputFile")
        if self.output_file is None:
            self.output_file = os.path.join(self.project_path, "OutputFile")

        if self.field_file == None:
            self.field_file = self.input_file

        if self.errorlog_path is None:
            self.errorlog_path = os.path.join(self.output_file, "ErrorLog.txt")

        if self.multiparticle_engine is None:
            self.multiparticle_engine = MultiParticleEngine()

    def run(self):
        print(38, self.input_file, self.output_file, self.field_file)
        if os.path.exists(self.errorlog_path):
            os.remove(self.errorlog_path)

        res_tmp = self.multiparticle_engine.get_path(self.input_file, self.output_file, self.field_file)

        res = self.multiparticle_engine.main_agent(1)
        if res == 1:
            # raise Exception(f'模拟错误，请查询OutputFile中的ErrorLog.txt')

            error = self.check_error_file(self.errorlog_path)
            raise Exception(f'{error}')
        elif res == 2:
            # raise Exception(f'模拟错误，请查询OutputFile中的ErrorLog.txt')
            error = self.check_error_file(self.errorlog_path)
            raise Exception(f'{error}')


        return res

    def stop(self):
        res = self.multiparticle_engine.main_agent(2)
        print("停止", res)


    def check_error_file(self, ErrorLog):
        with open(ErrorLog, 'r') as file:
            text = file.read()

        # error_parts = re.findall(r'[A-Za-z\s:,.]+', text)[3]
        error_parts = text.split('     ')[1]
        return error_parts





def basic_mulp(project_path):
    obj = MultiParticle(project_path)

    res = obj.run()


if __name__ == "__main__":


    item = {'project_path': r'C:\Users\anxin\Desktop\test_s59',
            }
    obj = MultiParticle(item)
    obj.run()



