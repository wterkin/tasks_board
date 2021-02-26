#! /usr/bin/python3
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
""" Органайзер задач. """
import sys

from pathlib import Path

from PyQt5 import QtWidgets, QtGui
from PyQt5 import uic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_

import c_ancestor as anc
import c_config as cfg

    
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
        # db_folder = Path(Path.home() / ALL_CONFIGS_FOLDER)
        # db_folder_path = Path()
        
        # *** Конфигурация
        self.config = cfg.CConfiguration()
        # *** База данных
        if not self.__db_exists():
        
            self.__db_create()

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


    def __db_connect(self):
        """Устанавливает соединение с БД."""
        self.engine = create_engine('sqlite:///'+self.config.restore_value(c_config.DATABASE_FILE_KEY))
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        anc.Base.metadata.bind = self.engine


    def __db_create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        anc.Base.metadata.create_all()
        #count = self.session.query(c_eventtype.CEventType).count()
        #if count == 0:

            #self.fill_event_types_table()
        #count = self.session.query(c_period.CPeriod).count()
        #if count == 0:

            #self.fill_periods_table()


    def __db_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        db_folder_path = Path(self.config.restore_value(cfg.DATABASE_FILE_KEY))
        return db_folder_path.exists()

        
if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()    
