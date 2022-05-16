@echo off
if exist mypy.log del mypy.log
rem call D:\home\bin\mypy.cmd c_inform.py
rem call D:\home\bin\mypy.cmd c_config.py
rem call D:\home\bin\mypy.cmd c_ancestor.py
rem call D:\home\bin\mypy.cmd c_tag.py
rem call D:\home\bin\mypy.cmd c_taglink.py
rem call D:\home\bin\mypy.cmd c_task.py
rem call D:\home\bin\mypy.cmd c_context.py
rem call D:\home\bin\mypy.cmd c_database.py
call D:\home\bin\mypy.cmd c_main.py
echo Done.
D:\home\bin\PortableApps\PortableApps\AkelPadPortable\AkelPadPortable.exe mypy.log

