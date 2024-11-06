import sys
import time
import platform
import subprocess
import os

sys.path.append(r'C:\Users\anxin\Desktop\AVAS_control')

from core.MultiParticleEngine import MultiParticleEngine

class MultiParticle():
    """
    多粒子模拟
    """

    def __init__(self, project_path):  # *arg **kwargs #dllpath写死
        self.project_path = project_path

    def run(self, input_file='InputFile', output_file='OutputFile'):
        inputfilepath = os.path.join(self.project_path, input_file)
        outputfilePath = os.path.join(self.project_path, output_file)

        self.multiparticle_engine = MultiParticleEngine()
        self.runsignal = os.path.join(outputfilePath, 'runsignal.txt')

        res_tmp = self.multiparticle_engine.get_path(inputfilepath, outputfilePath)

        # try:
        #     res = self.multiparticle_engine.main_agent(1)
        # except:
        #     raise Exception("底层代码发生错误")

        res = self.multiparticle_engine.main_agent(1)
        if res == 1:
            raise Exception('非正常结束')

        # with open(self.runsignal, 'w') as f:
        #     f.write('2')

        return res
        #
        # if platform.system() == 'Windows':
        #     self.multiparticle_engine = MultiParticleEngine()
        #     self.runsignal = os.path.join(outputfilePath, 'runsignal.txt')
        #
        #     # with open(self.runsignal, 'w') as f:
        #     #     f.write('1')
        #
        #     res_tmp = self.multiparticle_engine.get_path(inputfilepath, outputfilePath)
        #
        #     # try:
        #     #     res = self.multiparticle_engine.main_agent(1)
        #     # except:
        #     #     raise Exception("底层代码发生错误")
        #
        #     res = self.multiparticle_engine.main_agent(1)
        #     if res == 1:
        #         raise Exception('非正常结束')
        #
        #     # with open(self.runsignal, 'w') as f:
        #     #     f.write('2')
        #
        #     return res

        # if platform.system() == "Linux":
        #     try:
        #         work_dir = self.project_path
        #         command = f"/ShareData1/AVAS/build/AVAS {inputfilepath} {outputfilePath}"
        #         print(f"Running command: {command} in directory: {work_dir}")
        #
        #         # 使用 Popen 运行命令并捕获输出
        #         process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        #                                     cwd=work_dir, text=True)
        #
        #         detected = False  # 标记是否检测到目标输出
        #
        #         # 逐行读取标准输出和标准错误
        #         while True:
        #             output = process.stdout.readline()
        #             if output == '' and process.poll() is not None:
        #                 break
        #             if output:
        #                 print(output.strip())
        #
        #     except Exception as e:
        #         print(f"An error occurred: {e}")  # 打印错误信息



if __name__ == "__main__":
    start = time.time()
    project_path = r"C:\Users\shliu\Desktop\jiqunshiyong\test_err_dyn"
    project_path =r"C:\Users\shliu\Desktop\test_so\cafe_project"
    obj = MultiParticle(project_path)

    obj.run()
    # # 运行两次
    # for i in range(2):
    #     print(f"Running iteration {i + 1}")
    #     obj.run()
    #
    end = time.time()
    print(f"Total time: {end - start}")


