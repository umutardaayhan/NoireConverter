# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [
    ('App.ico', '.'),
    ('config.json', '.'),
]
binaries = []
hiddenimports = [
    'comtypes', 'comtypes.client', 'comtypes.stream',
    'deep_translator', 'deep_translator.google',
    'PIL', 'PIL.Image', 'PIL.ImageTk',
]

tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('tkinterdnd2')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['noire_converter.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'cv2', 'opencv', 'numpy', 'scipy', 'matplotlib',
        'pandas', 'sklearn', 'torch', 'tensorflow',
        'notebook', 'IPython', 'jupyter',
        'pytest', 'unittest', 'setuptools',
    ],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NoireConverter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['App.ico'],
)
