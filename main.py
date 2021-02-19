#! /usr/bin/python3
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
""" Органайзер задач. """
import sys
from pathlib import Path
from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic
    
PROGRAM_VERSION = "0.0"
MAIN_WINDOW_FORM = "mainwindow.ui"
FORM_FOLDER = "ui/"
HEADER_TEXT = "Ты должен делать то, что должен."

class CMainWindow(QtWidgets.QMainWindow):
    """Класс."""
    def __init__(self):
        """Конструктор класса."""
        super(CMainWindow, self).__init__()
        self.application_folder = Path.cwd()
        # *** Интерфейс
        ui_folder = self.application_folder / FORM_FOLDER / MAIN_WINDOW_FORM
        uic.loadUi(self.application_folder / FORM_FOLDER / MAIN_WINDOW_FORM, self)

        # *** БД
        db_folder = Path(Path.home() / ALL_CONFIGS_FOLDER)
        db_folder_path = Path()
        return config_folder_path.exists()
        
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
        
        window_title = f"Task organizer ver. {PROGRAM_VERSION} : \"{HEADER_TEXT}\""
        self.setWindowTitle(window_title)
        #self.setWindowIcon(QtGui.QIcon('ui/forget-me-not.ico'))
        self.update()
        self.show()

        
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()    
