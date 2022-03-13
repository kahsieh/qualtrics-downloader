# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

path = os.getcwd()
folderstoadd = [
         (path +'/SetupFiles/*', "SetupFiles"), 
         (path +'/GUIWindows/*', "GUIWindows"),
         ]
         
a = Analysis(['driveGui_v1.0.py'],
             binaries=[],
             datas=folderstoadd,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='driveGui_v1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='driveGui_v1.0')
