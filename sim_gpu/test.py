import sys
from ctypes import *
from mpi4py import MPI
from sim_gpu.structures import *
from sim_gpu.initializer import *
from sim_gpu.output import *
import time

class MPIContext:
    def __init__(self):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
        self.mpi_obj = MPIObject()
        self.mpi_obj.commSize = self.size
        self.mpi_obj.rank = self.rank
        SetDeviceForProcessors(pointer(self.mpi_obj))

class ConfigurationLoader:
    def __init__(self, argv):
        argc = len(argv)
        c_argv = (c_char_p * argc)()
        for i in range(argc):
            c_argv[i] = argv[i].encode()
        
        if not CheckCommandLineArguments(c_int(argc), c_argv):
            raise RuntimeError("Invalid command line arguments")
        
        self.configs = ReadConfigurations(c_int(argc), c_argv)

class LatticeManager:
    def __init__(self, config, running_options):
        self.ptr = InitializeLatticeComponents(config, running_options)
        if not self.ptr:
            raise RuntimeError("Lattice initialization failed")
        
    def print_info(self, rank):
        print(f"rank = {rank} : lattice components number = {self.ptr[0].numComponents}, "
              f"lattice length = {self.ptr[0].latticeLength}")

class BeamManager:
    def __init__(self, config, mpi_context, lattice, running_options):
        self.ptr = InitializeBeam(config, pointer(mpi_context.mpi_obj), lattice.ptr, running_options)
        if not self.ptr:
            raise RuntimeError("Beam initialization failed")
    
    def print_info(self, rank):
        print(f"rank = {rank} : holding {self.ptr[0].particles_gpu.numParticles} "
              f"particles of total {self.ptr[0].particles_init.numParticles}")

class SimulationCore:
    def __init__(self, mpi_context):
        self.mpi = mpi_context
        self.argv = sys.argv
        
        # 初始化配置
        self.config_loader = ConfigurationLoader(self.argv)
        self.running_options = LoadRunningOptions(self.config_loader.configs[0])
        
        # 初始化组件
        self.lattice = LatticeManager(self.config_loader.configs[2], self.running_options)
        self.beam = BeamManager(self.config_loader.configs[1], self.mpi, self.lattice, self.running_options)
        
        # 打印初始化信息
        self.lattice.print_info(self.mpi.rank)
        self.beam.print_info(self.mpi.rank)
        
        # 初始化计算资源
        self._init_compute_resources()

    def _init_compute_resources(self):
        self.cub = CUBObject()
        InitializeCUB(self.beam.ptr, pointer(self.cub))
        
        self.pic = PIC()
        InitializePIC(pointer(self.pic), self.running_options, pointer(self.cub), pointer(self.mpi.mpi_obj))
        
        self.fft = FFTSolver()
        InitializerFFT(pointer(self.fft), pointer(self.pic))
        
        self.cu_streams = (c_void_p * 2)()
        self.cu_streams[0] = CreateCudaStream()
        self.cu_streams[1] = CreateCudaStream()

    def run(self):
        InitializePhase(self.lattice.ptr, self.beam.ptr, self.running_options)
        OutputScanPhaseResult(self.lattice.ptr, pointer(self.mpi.mpi_obj))
        
        start_time = time.time()
        itrCnt = RunSimulationWithSpaceChargeUsingPICNICSolver(
            self.running_options,
            self.lattice.ptr,
            self.beam.ptr,
            pointer(BeamStatistics()),
            pointer(self.cub),
            pointer(self.mpi.mpi_obj),
            pointer(self.pic),
            self.cu_streams
        )
        
        print(f"rank = {self.mpi.rank} : iterate steps = {itrCnt}, "
              f"time cost = {time.time()-start_time} s")
        
        OutputRealParticles(self.beam.ptr, pointer(self.mpi.mpi_obj), "real.dat".encode())

if __name__ == "__main__":
    try:
        mpi_ctx = MPIContext()
        simulator = SimulationCore(mpi_ctx)
        simulator.run()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)