import sys
import os
from ctypes import *
from sim_gpu.structures import *
from sim_gpu.initializer import *
from sim_gpu.run import *
import time

class MPIContext:
    def __init__(self):
        try:
            from mpi4py import MPI  # 延迟导入，确保只有在需要时才触发
            self.comm = MPI.COMM_WORLD
            self.rank = self.comm.Get_rank()
            self.comm_size = self.comm.Get_size()

            self.mpi_obj = MPIObject()
            self.mpi_obj.commSize = self.comm_size
            self.mpi_obj.rank = self.rank
            print(f"[MPI] Init success - rank={self.rank}, size={self.comm_size}")
        except Exception as e:
            print("[MPI] 初始化失败:", e)
            import traceback
            traceback.print_exc()
            self.comm = None
            self.rank = 0
            self.comm_size = 1
            self.mpi_obj = None

class CUB:
    def __init__(self, beam_ptr):
        self.cub_obj = CUBObject()
        InitializeCUB(beam_ptr, pointer(self.cub_obj))

class PICHandler:
    def __init__(self, running_options, cub_handler, mpi_handler):
        self.pic = PIC()
        InitializePIC(pointer(self.pic), running_options, 
                     pointer(cub_handler.cub_obj), pointer(mpi_handler.mpi_obj))

class FFT:
    def __init__(self, pic_handler):
        self.fft_solver = FFTSolver()
        InitializerFFT(pointer(self.fft_solver), pointer(pic_handler.pic))

class Beam:
    def __init__(self, config_path, mpi_handler, lattice_ptr, running_options):
        self.beam_ptr = InitializeBeam(config_path, pointer(mpi_handler.mpi_obj),
                                      lattice_ptr, running_options)
        self.statistics = BeamStatistics()

class SimulationRunner:
    def __init__(self, item):
        self.project_path = item["project_path"]
        self.input_file = item.get("input_file")
        self.input_txt = item["input_path"]
        self.beam_txt = item["beam_path"]
        self.lattice_txt = item["lattice_path"]

        self.mpi_handler = MPIContext()
        self.configs = self._read_configs()
        self.running_options = LoadRunningOptions(self.configs[0])
        self._initialize_components()
        self._setup_streams()

    # def _check_args(self, argv):
    #     argc = len(argv)
    #     c_argv = (c_char_p * argc)()
    #     for i in range(argc):
    #         c_argv[i] = argv[i].encode()
    #     if not CheckCommandLineArguments(c_int(argc), c_argv):
    #         exit()

    def _read_configs(self):
        # 动态生成配置参数
        config_args = [
            "avas",
            f"common={self.input_txt}",
            f"beam={self.beam_txt}",
            f"lattice={self.lattice_txt}"
        ]
        print(75, config_args)
        #print(config_args)
        argc = len(config_args)
        argv_c = (c_char_p * argc)()
        for i, arg in enumerate(config_args):
            argv_c[i] = arg.encode()
        return ReadConfigurations(c_int(argc), argv_c)

    def _initialize_components(self):
        # 初始化晶格
        self.lattice_ptr = InitializeLatticeComponents(self.configs[2], self.running_options)
        print(f"rank={self.mpi_handler.rank}: components={self.lattice_ptr[0].numComponents}, length={self.lattice_ptr[0].latticeLength}")

        # 初始化束流
        self.beam_handler = Beam(self.configs[1], self.mpi_handler, 
                                       self.lattice_ptr, self.running_options)
        print(f"rank={self.mpi_handler.rank}: holding {self.beam_handler.beam_ptr[0].particles_gpu.numParticles} of {self.beam_handler.beam_ptr[0].particles_init.numParticles}")

        # 初始化CUB
        self.cub_handler = CUB(self.beam_handler.beam_ptr)
        
        # 初始化PIC
        self.pic_handler = PICHandler(self.running_options, self.cub_handler, self.mpi_handler)
        
        # 初始化FFT
        self.fft_handler = FFT(self.pic_handler)
        
        # 初始化输出
        self.output_obj = OutputObject()
        InitializeOutputObject(self.configs[3], self.running_options, 
                              self.beam_handler.beam_ptr, self.lattice_ptr,
                              pointer(self.output_obj))

    def _setup_streams(self):
        self.cu_stream = (c_void_p * 2)()
        self.cu_stream[0] = CreateCudaStream()
        self.cu_stream[1] = CreateCudaStream()

    def run(self):
        start_time = time.time()
        InitializePhase(self.lattice_ptr, self.beam_handler.beam_ptr,
                       self.running_options, pointer(self.mpi_handler.mpi_obj))

        if self.running_options[0].spaceChargeFlag:
            if self.running_options[0].spaceChargeMethod == 0:
                itr_cnt = RunSimulationWithSpaceChargeUsingFFT(
                    self.running_options, 
                    self.lattice_ptr, 
                    self.beam_handler.beam_ptr, 
                    pointer(self.beam_handler.statistics),
                    pointer(self.cub_handler.cub_obj), 
                    pointer(self.mpi_handler.mpi_obj),
                    pointer(self.pic_handler.pic), 
                    pointer(self.fft_handler.fft_solver),
                    pointer(self.output_obj), 
                    self.cu_stream
                )
            else:
                itr_cnt = RunSimulationWithSpaceChargeUsingPICNIC(
                    self.running_options,
                    self.lattice_ptr,
                    self.beam_handler.beam_ptr,
                    pointer(self.beam_handler.statistics),
                    pointer(self.cub_handler.cub_obj),
                    pointer(self.mpi_handler.mpi_obj),
                    pointer(self.pic_handler.pic),
                    pointer(self.output_obj),
                    self.cu_stream
                )
        else:    
            itr_cnt = RunSimulationWithoutSpaceCharge(
                self.running_options,
                self.lattice_ptr,
                self.beam_handler.beam_ptr,
                pointer(self.beam_handler.statistics),
                pointer(self.cub_handler.cub_obj),
                pointer(self.mpi_handler.mpi_obj),
                pointer(self.output_obj),
                self.cu_stream
            )

        print(f"rank={self.mpi_handler.rank}: steps={itr_cnt}, time={time.time()-start_time:.2f}s")
        OutputRealParticles(self.beam_handler.beam_ptr, 
                            pointer(self.mpi_handler.mpi_obj), b"real.dat")
        

if __name__ == "__main__":
    project_path = r"/root/GAVAS/"
    item = {
        "project_path": project_path
    }
    
    simulator = SimulationRunner(item)
    simulator.run()