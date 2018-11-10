#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

includes = [
    "os", "sys", "PyQt5.QtWidgets", "PyQt5.QtGui", "PyQt5.QtCore", "subprocess",
    "collections", "PIL.Image"
]
buildOption = dict(
    create_shared_zip=False, append_script_to_exe=True, includes=includes)
executables = [
    Executable(
        script='Auto_Watermark.py',
        targetName='Auto_Watermark.exe',
        base="Win32GUI")
]
setup(
    name="ProjectName",
    version="1.0",
    description=" ",
    options=dict(build_exe=buildOption),
    executables=executables)
