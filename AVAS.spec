# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    [ 'main.py', 'api.py', 'global_varible.py',

     './aftertreat/dataanalysis/caltwiss.py',
     './aftertreat/dataanalysis/out_percentemitt.py',
     './aftertreat/dataanalysis/percentemitt.py',

    './aftertreat/picture/initialplot.py',
    './aftertreat/picture/plotdataset.py',
    './aftertreat/picture/plotenvbeamout.py',
    './aftertreat/picture/ploterror.py',
    './aftertreat/picture/plotphase.py',
    './aftertreat/picture/plotpicture.py',

    './apps/basicenv.py',
    './apps/changeNp.py',
    './apps/circlematch.py',
    './apps/erroranalysis.py',
    './apps/LongAccelerator.py',
    './apps/matchtwiss.py',
    './apps/scan.py',
    './apps/tasks.py',

    './core/AVAS.py',
    './core/AVASEngine.py',
    './core/LinacOPTEngine.py',
    './core/LongAcceleratorEngine.py',

    './dataprovision/beamparameter.py',
    './dataprovision/datasetparameter.py',
    './dataprovision/env_beam_out.py',
    './dataprovision/latticeparameter.py',


    './utils/beamconfig.py',
    './utils/exception.py',
    './utils/initilaconfig.py',
    './utils/inputconfig.py',
    './utils/latticeconfig.py',
    './utils/myoptimize.py',
    './utils/readfile.py',
    './utils/smalltool.py',
    './utils/tolattice.py',
    './utils/treat_directory.py',


    './user/user_arg/user_argparse.py',

    './user/user_qt/lattice_file/lattice_ide.py',
    './user/user_qt/page_analysis.py',
    './user/user_qt/page_beam.py',
    './user/user_qt/page_data.py',
    './user/user_qt/page_error.py',
    './user/user_qt/page_function.py',
    './user/user_qt/page_input.py',
    './user/user_qt/page_lattice.py',
    './user/user_qt/page_longdistance.py',
    './user/user_qt/user_defined.py',
    './user/user_qt/user_pyqt.py',
    ],

    pathex=[r'C:\Users\anxin\Desktop\AVAS_control'],
    binaries=[],
    datas=[('./dllfile/AVAS.dll', 'dllfile'),
    ('./dllfile/AVAS.lib', 'dllfile'),
    ('./dllfile/libfftw3-3.dll', 'dllfile'),
    ('./dllfile/libfftw3f-3.dll', 'dllfile'),
    ('./dllfile/libfftw3l-3.dll', 'dllfile'),
    ('./dllfile/MSVCP140.dll', 'dllfile'),
    ('./dllfile/Dll2.dll', 'dllfile'),
    ('./dllfile/LongAccelerator2.dll', 'dllfile'),
    ('./dllfile/LongAccelerator3.dll', 'dllfile'),

    ('./staticfile/ifr.txt','staticfile'),
    ('./staticfile/ifx3d_3.txt','staticfile'),
    ('./staticfile/ifz.txt','staticfile'),
    ('./staticfile/ifz3d_3.txt','staticfile'),

    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AVAS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AVAS',
)
