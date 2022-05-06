@echo off
if exist lint.log del lint.log
call D:\home\bin\pylint.cmd c_inform.py
call D:\home\bin\pylint.cmd c_config.py
call D:\home\bin\pylint.cmd c_ancestor.py
call D:\home\bin\pylint.cmd c_tag.py
call D:\home\bin\pylint.cmd c_taglink.py
call D:\home\bin\pylint.cmd c_task.py
call D:\home\bin\pylint.cmd c_context.py
call D:\home\bin\pylint.cmd c_database.py
call D:\home\bin\pylint.cmd c_main.py
echo Done.
D:\home\bin\PortableApps\PortableApps\AkelPadPortable\AkelPadPortable.exe  lint.log

