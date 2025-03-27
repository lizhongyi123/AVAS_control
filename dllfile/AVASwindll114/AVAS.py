#import ctypes
#avas = ctypes.cdll.LoadLibrary('./AVAS.dll')  # Load Dynamic Link Library
#avas.path(ctypes.c_wchar_p("D:\CodeSolo\solo\AVAS\InputFile"), ctypes.c_wchar_p("D:\CodeSolo\solo\AVAS\OutputFile")) # transmitted parameter
#avas.main_agent(1)  # Start the simulation

import ctypes
avas = ctypes.cdll.LoadLibrary(r"./libAVAS.dll")  # Load Dynamic Link Library
avas.path(ctypes.c_wchar_p(r"./inputFile"), ctypes.c_wchar_p(r"./outputFile"), ctypes.c_wchar_p(r"./fieldmap")) # transmitted parameter
avas.main_agent(1)  # Start the simulation