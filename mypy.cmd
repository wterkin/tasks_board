@echo off
if exist mypy.log del mypy.log
call D:\home\bin\mypy.cmd c_main.py
echo Done.
D:\home\bin\PortableApps\PortableApps\AkelPadPortable\AkelPadPortable.exe mypy.log

