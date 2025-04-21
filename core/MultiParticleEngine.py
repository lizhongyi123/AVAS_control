import ctypes
import sys
import os
from ctypes import POINTER, c_char_p, cdll
import platform

class MultiParticleEngine():
    def __init__(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在文件夹的绝对路径
        parent_directory = os.path.dirname(script_directory)  # 获取上级目录的路径
        self.dll_path = os.path.join(parent_directory, 'dllfile', 'AVAS.dll')  # 使用绝对路径连接得到完整的路径
        self.so_path = os.path.join(parent_directory, 'dllfile', 'libAVAS.so')  # 使用绝对路径连接得到完整的路径
        try:
            if platform.system() == 'Windows':
                # 尝试加载DLL文件
                self.library = ctypes.CDLL(self.dll_path)
            elif platform.system() == "Linux":
                self.AVAS_cdll = cdll.LoadLibrary(self.so_path)  # Load Dynamic Link Library

        except OSError as e:
            if platform.system() == 'Windows':
                # 尝试加载DLL文件
                raise ValueError(f"Failed to load DLL '{self.dll_path}'. Reason: {e}")
            elif platform.system() == "Linux":
                raise ValueError(f"Failed to load so '{self.so_path}'. Reason: {e}")


    def get_path(self, inputfilepath, outputfilePath, fieldfilePath):
        if platform.system() == 'Windows':
            inputfilepath = ctypes.c_wchar_p(inputfilepath)
            outputfilePath = ctypes.c_wchar_p(outputfilePath)
            fieldfilePath = ctypes.c_wchar_p(fieldfilePath)
            res = self.library.path(inputfilepath, outputfilePath, fieldfilePath)
        elif platform.system() == "Linux":
            inputfilepath = ctypes.c_char_p(inputfilepath.encode('utf-8'))  # 转为字节并包装为 c_char_p
            outputfilePath = ctypes.c_char_p(outputfilePath.encode('utf-8'))
            res = self.AVAS_cdll.path(inputfilepath, outputfilePath)
        return res

    #input, beam, lattice都应该为自定义的结构体
    def main_agent(self, value):
        value = ctypes.c_int(1)
        value = ctypes.pointer(value)
        if platform.system() == 'Windows':
            res = self.library.main_agent(value)
        elif platform.system() == "Linux":
            res = self.AVAS_cdll.main_agent(value)

        return res

    def stop(self):
        pass

if __name__ == '__main__':
    project_path = r"E:\using\test_avas_qt\cafe_avas"
    inputfile = os.path.join(project_path, "InputFile")
    outputfile = os.path.join(project_path, "OutputFile")
    fieldfile = os.path.join(project_path, "InputFile")

    # 创建一个停止标志，用于停止执行
    stop_event = threading.Event()


    def run_main_agent():
        """在新的线程中运行 main_agent 函数"""
        multiparticle_engine.main_agent(1)


    # 启动一个线程运行 `main_agent`
    agent_thread = threading.Thread(target=run_main_agent)
    agent_thread.start()

    # 等待一段时间后停止运行
    time.sleep(3)  # 假设我们等待 3 秒后想停止任务
    print("Stopping the engine...")

    # 设置停止事件标志
    stop_event.set()

    # 等待线程执行完成
    agent_thread.join()

    print("Engine stopped.")
