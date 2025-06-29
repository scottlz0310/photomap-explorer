# -*- mode: python ; coding: utf-8 -*-
"""
PhotoMap Explorer v2.1.2 - PyInstaller specification file
Windows用スタンドアロン実行ファイル生成設定
"""

import os
from pathlib import Path

block_cipher = None

# プロジェクトのルートディレクトリ
root_dir = Path.cwd()

# データファイルとリソースファイルの追加
datas = [
    (str(root_dir / 'assets'), 'assets'),
    (str(root_dir / 'docs'), 'docs'),
    (str(root_dir / 'map.html'), '.'),
    (str(root_dir / 'README.md'), '.'),
    (str(root_dir / 'CHANGELOG.md'), '.'),
    (str(root_dir / 'LICENSE'), '.'),
]

# Foliumとその依存関係の追加
hiddenimports = [
    'folium',
    'folium.plugins',
    'branca',
    'jinja2',
    'PyQt5.QtWebEngineWidgets',
    'PyQt5.QtWebEngine',
    'exifread',
    'PIL',
    'PIL.Image',
    'PIL.ExifTags',
]

a = Analysis(
    ['main.py'],
    pathex=[str(root_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='photomap-explorer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Windowsアプリとして実行（コンソールなし）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(root_dir / 'assets' / 'pme.ico'),  # アプリケーションアイコン
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='photomap-explorer',
)
