# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    [ 'main.py', 'api.py', 'global_varible.py',


D:\AVAS_CONTROL\AVAS_control\venv\Scripts\python.exe D:\AVAS_CONTROL\AVAS_control\otherdemand\listpackagefiles.py
'./aftertreat/picture/initialplot.py',
'./aftertreat/picture/plotacc.py',
'./aftertreat/picture/plotdataset.py',
'./aftertreat/picture/plotdesnsity.py',
'./aftertreat/picture/plotenvbeamout.py',
'./aftertreat/picture/ploterror.py',
'./aftertreat/picture/plotphase.py',
'./aftertreat/picture/plotphaseellipse.py',
'./aftertreat/picture/plotpicture.py',
'./aftertreat/picture/__init__.py',
'./aftertreat/dataanalysis/caltwiss.py',
'./aftertreat/dataanalysis/EAanalysis.py',
'./aftertreat/dataanalysis/extodensity.py',
'./aftertreat/dataanalysis/out_percentemitt.py',
'./aftertreat/dataanalysis/percentemitt.py',
'./aftertreat/dataanalysis/plttodensity.py',
'./aftertreat/dataanalysis/plttodst.py',
'./aftertreat/dataanalysis/__init__.py',
'./apis/basic_api/api.py',
'./apis/qt_api/api.py',
'./apis/qt_api/createbasicfile.py',
'./apis/qt_api/getschedule.py',
'./apis/qt_api/hpc_simmode.py',
'./apis/qt_api/judge_lattice.py',
'./apis/qt_api/SimMode.py',
'./apps/basicenv.py',
'./apps/calacceptance.py',
'./apps/changeNp.py',
'./apps/circlematch.py',
'./apps/diaginfo.py',
'./apps/EA.py',
'./apps/error.py',
'./apps/err_adjust.py',
'./apps/LongAccelerator.py',
'./apps/matchtwiss.py',
'./apps/scan.py',
'./apps/tasks.py',
'./apps/__init__.py',
'./core/LinacOPTEngine.py',
'./core/LongAcceleratorEngine.py',
'./core/MultiParticle.py',
'./core/MultiParticleEngine.py',
'./core/__init__.py',
'./dataprovision/beamparameter.py',
'./dataprovision/beamset.py',
'./dataprovision/datasetparameter.py',
'./dataprovision/densityparameter.py',
'./dataprovision/env_beam_out.py',
'./dataprovision/exdataparameter.py',
'./dataprovision/latticeparameter.py',
'./dataprovision/__init__.py',
'./hpc/get_errordata.py',
'./hpc/get_jobstatus.py',
'./hpc/stop_job.py',
'./hpc/submit_job.py',
'./otherdemand/listpackagefiles.py',
'./otherdemand/zhuanhuan.py',
'./user/user_qt/lattice_file',
'./user/user_qt/page_acc.py',
'./user/user_qt/page_analysis.py',
'./user/user_qt/page_beam.py',
'./user/user_qt/page_data.py',
'./user/user_qt/page_error.py',
'./user/user_qt/page_function.py',
'./user/user_qt/page_input.py',
'./user/user_qt/page_lattice.py',
'./user/user_qt/page_longdistance.py',
'./user/user_qt/page_match.py',
'./user/user_qt/page_others.py',
'./user/user_qt/page_output.py',

'./user/user_qt/user_defined.py',
'./user/user_qt/user_pyqt.py',
'./user/user_qt/lattice_file/latticeideuseclass.py',
'./user/user_qt/lattice_file/lattice_ide.py',
'./user/user_qt/lattice_file/test_lattice.py',
'./user/user_qt/page_utils/phaseellipse_dialog.py',
'./user/user_qt/page_utils/picture_dialog.py',
'./utils/beamconfig.py',
'./utils/change_win_to_linux.py',
'./utils/exception.py',
'./utils/getinfotools.py',
'./utils/griddensity.py',
'./utils/iniconfig.py',
'./utils/initilaconfig.py',
'./utils/inputconfig.py',
'./utils/latticecheck.py',
'./utils/latticeconfig.py',
'./utils/myoptimize.py',
'./utils/readfile.py',
'./utils/tolattice.py',
'./utils/tool.py',
'./utils/treatfile.py',
'./utils/treatlist.py',
'./utils/treat_directory.py',
'./utils/__init__.py',

    ],

    pathex=[r'D:\AVAS_CONTROL\AVAS_control'],
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