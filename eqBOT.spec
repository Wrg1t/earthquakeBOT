# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['eqBOT.py'],
             pathex=['L:\\OneDrive\\Atom\\PYTHON\\eqBOT'],
             binaries=[],
             datas=[],
             hiddenimports=['requests,bs4,re,time,traceback,win32gui,win32con,win32clipboard'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='eqBOT',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
