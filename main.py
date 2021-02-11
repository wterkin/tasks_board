#! /usr/bin/python3
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Qt оболочка для forget-me-not."""
import sys
from pathlib import Path
# import shutil
# from datetime import datetime
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic

# import c_config as cfg
# import c_constants as const
# import c_database as db
# import c_eventslist as evlst
# import c_eventtypeslist as evtypelst
# import c_tools as tls
    
PROGRAM_VERSION = "0.0"
MAIN_WINDOW_FORM = "mainwindow.ui"
FORM_FOLDER = "ui/"

class CMainWindow(QtWidgets.QMainWindow):
    """Класс."""
    def __init__(self):
        """Конструктор класса."""
        super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        ui_folder = self.application_folder / FORM_FOLDER / MAIN_WINDOW_FORM
        print("*** MW:IN:fold", ui_folder)
        uic.loadUi(self.application_folder / FORM_FOLDER / MAIN_WINDOW_FORM, self)
        # text_font = QtGui.QFont()
        # text_font.setPointSize(text_font.pointSize()+3)
        # self.textBrowser.setFont(text_font)
        # self.actionEventsList.triggered.connect(self.__event_list_show)
        # self.actionOpenDatabase.triggered.connect(self.__open_database)
        # self.actionEventTypesList.triggered.connect(self.__event_type_list_sho
        # self.config = cfg.CConfiguration()

        #self.database = db.CDatabase(self.config)
        #if not self.__is_database_exists():

            #self.database.create_database()
        #self.database.cleanup()
        #self.backup_need = False
        #PROGRAM_VERSION
        
        window_title = self.windowTitle() + f" ver. {PROGRAM_VERSION}"
        self.setWindowTitle(window_title)
        #self.setWindowIcon(QtGui.QIcon('ui/forget-me-not.ico'))
        self.update()
        self.show()

        
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()    
