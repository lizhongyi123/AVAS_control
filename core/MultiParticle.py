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
    def __init__(self, project_path):  # *arg **kwargs #dllpath写死
        self.project_path = project_path



    def run(self, input_file='InputFile', output_file='OutputFile', field_file = None):
        errorlog = os.path.join(self.project_path, output_file, "ErrorLog.txt")
        if os.path.exists(errorlog):
            os.remove(errorlog)


        inputfilepath = os.path.join(self.project_path, input_file)
        outputfilePath = os.path.join(self.project_path, output_file)

        if field_file == None:
            fielfilepath = os.path.join(self.project_path, input_file)
        else:
            fielfilepath = field_file

        self.multiparticle_engine = MultiParticleEngine()


        res_tmp = self.multiparticle_engine.get_path(inputfilepath, outputfilePath, fielfilepath)



        res = self.multiparticle_engine.main_agent(1)
        if res == 1:
            raise Exception(f'模拟错误，请查询OutputFile中的ErrorLog.txt')

            # raise Exception(f'{error}')
            # error = self.check_error_file(errorlog)
            # raise Exception(f'{error}')
        elif res == 2:
            raise Exception(f'模拟错误，请查询OutputFile中的ErrorLog.txt')
            # error = self.check_error_file(errorlog)
            # raise Exception(f'{error}')
        return res

    def check_error_file(self, ErrorLog):
        with open(ErrorLog, 'r') as file:
            text = file.read()

        # error_parts = re.findall(r'[A-Za-z\s:,.]+', text)[3]
        error_parts = text.split('     ')[1]
        print(42, error_parts)
        return error_parts

    def stop(self):
        self.multiparticle_engine.stop_function()



def basic_mulp(project_path):
    obj = MultiParticle(project_path)

    res = obj.run()


if __name__ == "__main__":
    start = time.time()
    project_path = r"D:\using\test_avas_qt\cafe_avas3"


    obj = MultiParticle(project_path)
    obj.run()

    end = time.time()
    print(f"总时间: {end - start}")

