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
    # def __init__(self, project_path):  # *arg **kwargs #dllpath写死
    #     self.project_path = project_path
    #     self.return_value = -1
    #     self.stop_flag = False
    #     self.process = None


    # def delete_file(self, outputfilePath):
    #     ErrorLog = os.path.join(outputfilePath, "ErrorLog.txt")
    #     if os.path.exists(ErrorLog):
    #         os.remove(ErrorLog)
    #     self.runsignal = os.path.join(outputfilePath, 'runsignal.txt')
    #     if os.path.exists(self.runsignal):
    #         os.remove(self.runsignal)
    #
    # def check_error_file(self, outputfilePath):
    #     ErrorLog = os.path.join(outputfilePath, "ErrorLog.txt")
    #     with open(ErrorLog, 'r') as file:
    #         text = file.read()
    #
    #     error_parts = re.findall(r'[A-Za-z\s:,.]+', text)[3].strip()
    #     return error_parts
    #
    # def basic_run(self, input_file, output_file, shared_return_value):
    #     inputfilepath = os.path.join(self.project_path, input_file)
    #     outputfilePath = os.path.join(self.project_path, output_file)
    #
    #     self.multiparticle_engine = MultiParticleEngine()
    #     self.delete_file(outputfilePath)
    #
    #     res_tmp = self.multiparticle_engine.get_path(inputfilepath, outputfilePath)
    #     # 修改共享值
    #     shared_return_value.value = self.multiparticle_engine.main_agent(1)
    #     print(50, shared_return_value.value)
    #
    # def run(self, input_file='InputFile', output_file='OutputFile'):
    #     self.stop_flag = False
    #     outputfilePath = os.path.join(self.project_path, output_file)
    #     self.delete_file(outputfilePath)
    #
    #     with open(self.runsignal, 'w') as f:
    #         f.write('0')
    #
    #     with multiprocessing.Manager() as manager:
    #         # 创建共享值，用于在进程间共享 return_value
    #         shared_return_value = manager.Value('i', -1)  # 初始化值为 -1
    #
    #         self.process = multiprocessing.Process(target=self.basic_run, args=(input_file, output_file, shared_return_value), )
    #         print(63, self.process, "进程被创建")
    #         self.process.daemon = True  # 设置为守护进程
    #         self.process.start()
    #         self.process.join()
    #
    #         # 获取子进程更新的值
    #         self.return_value = shared_return_value.value
    #
    #     with open(self.runsignal, 'w') as f:
    #         f.write('1')
    #     if self.stop_flag == True:
    #         print(72, "结束")
    #         return 2
    #
    #     print(71, self.return_value)
    #     print(79, self.process, "进程被创建")
    #     if self.return_value == 0:
    #         return 0
    #     elif self.return_value == -1:
    #         res = self.check_error_file(outputfilePath)
    #         raise Exception(res)
    #
    # def stop(self):
    #     print(85)
    #     print(self.process)
    #     # 使用 terminate 强制终止子进程
    #     if self.process and self.process.is_alive():
    #         self.stop_flag = True
    #         self.process.terminate()
    #         self.process.join(timeout=3)  # 使用超时等待最多 5 秒
    #         if self.process.is_alive():
    #             print("Process did not terminate within timeout")


def basic_mulp(project_path):
    obj = MultiParticle(project_path)

    res = obj.run()


if __name__ == "__main__":

    start = time.time()
    project_path = r"C:\Users\shliu\Desktop\test_error\0"
    obj = MultiParticle(project_path)


    obj.run()
    # process = multiprocessing.Process(target=basic_mulp,
    #                               args=(project_path, ))
    #
    # process.start()  # 启动子进程
    # process.join()  # 等待子进程运行结束

    end = time.time()
    print(f"总时间: {end - start}")

    # start = time.time()
    #
    # project_path =r"C:\Users\shliu\Desktop\test1113\test_cafe"
    # #
    # # obj = MultiParticle(project_path)
    #
    # # res = obj.run()
    # # print (res)
    # # # # 运行两次
    # # # for i in range(2):
    # # #     print(f"Running iteration {i + 1}")
    # # #     obj.run()
    # # #

    #
    # import multiprocessing
    #
    # project_path =r"C:\Users\shliu\Desktop\test1113\test_cafe"
    #
    # # for i in range(2):
    # #     process = multiprocessing.Process(target=basic_mulp,
    # #                                   args=( project_path, ))
    # #
    # #     process.start()  # 启动子进程
    # #     process.join()  # 等待子进程运行结束
    #
    # queue = multiprocessing.Queue()  # 创建一个队列对象
    #
    # process = multiprocessing.Process(target=basic_mulp, args=(project_path, queue))
    # process.start()  # 启动子进程
    # process.join()  # 等待子进程运行结束
    #
    # # 获取返回值
    # if not queue.empty():
    #     result = queue.get()  # 从队列中获取结果
    #     print(f"函数返回值: {result}")
    # else:
    #     print("子进程未返回结果")
    #
    # end = time.time()
    # print(f"总时间: {end - start}")

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
