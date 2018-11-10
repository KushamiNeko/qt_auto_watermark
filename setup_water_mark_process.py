#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cx_Freeze import setup, Executable

includes = [
    "os", "sys", "PIL.Image", "PIL.ImageChops", "shutil", "encodings.utf_8"
]
packages = [
    "os", "sys", "PIL.Image", "PIL.ImageChops", "shutil", "encodings.utf_8"
]
buildOption = dict(
    create_shared_zip=False, includes=includes, packages=packages)
executables = [
    Executable(
        script='water_mark_process.py',
        targetName='water_mark_process.exe',
        compress=True,
        copyDependentFiles=True,
        appendScriptToExe=True,
        appendScriptToLibrary=False,
        base="Win32GUI")
]
setup(
    name="ProjectName",
    version="1.0",
    description=" ",
    options=dict(build_exe=buildOption),
    executables=executables)
