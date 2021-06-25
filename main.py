#! /usr/bin/python3
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
""" Органайзер задач. """

import sys

from pathlib import Path

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5 import uic

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_, or_

from alembic.config import Config
from alembic import command, autogenerate
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext

import c_ancestor as canc
import c_config as ccfg
import c_context as cctx
import c_tag as ctag
import c_task as ctsk  # =)
    
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
        self.setWindowTitle(f"Tasks board ver. {PROGRAM_VERSION} : \"{HEADER_TEXT}\"")
        self.setWindowIcon(QtGui.QIcon('ui/tasks_board.ico'))

        # *** Конфигурация
        self.config = ccfg.CConfiguration()

        # *** База данных
        self.__db_connect()
        if not self.__db_exists():
            self.__db_create()
        # *** Компоненты
        # comboBox_Contexts
        # lineEdit_TagsFilter
        # lineEdit_TextFilter
        # checkBox_ShowCompleted
        # checkBox_ShowDeleted
        # lineEdit_Tags
        # spinBox_Urgency
        # lineEdit_Task
        # tableWidget_Tasks
        # statusBar
        # toolButton_TagsFilter
        # toolButton_TextFilter
        # toolButton_Quit
        # toolButton_Apply
        # *** Обработчики
        self.toolButton_Apply.clicked.connect(self.__save_task)
        self.toolButton_TagsFilter.clicked.connect(self.__set_tags_filter)
        self.toolButton_TextFilter.clicked.connect(self.__set_text_filter)
        self.pushButton_EditTask.clicked.connect(self.__edit_task)
        self.pushButton_DeleteTask.clicked.connect(self.__delete_task)

        # self.update()
        self.show()


    def __db_alembic_setup(self):
        """Создает среду алембика."""
        migrations_path = Path(Path.home() / ccfg.ALL_CONFIGS_FOLDER)
        if not migrations_path.exists():

            migrations_path.mkdir()
        alembic_config = Config()
        alembic_config.set_main_option("script_location", "migrations")
        alembic_config.set_main_option("url", 'sqlite:///'+self.config.restore_value(ccfg.DATABASE_FILE_KEY))
        self.alembic_script = ScriptDirectory.from_config(alembic_config)
        self.alembic_env = EnvironmentContext(alembic_config, self. alembic_script)
        self.alembic_env.configure(connection=self.engine.connect(), target_metadata=canc.Base.metadata, fn=self.__db_upgrade)
        self.alembic_context = self.alembic_env.get_context()


    def __db_check(self):
        """Проверяет базу на соответствие ее структуры классам."""


    def __db_connect(self):
        """Устанавливает соединение с БД."""
        self.engine = create_engine('sqlite:///'+self.config.restore_value(ccfg.DATABASE_FILE_KEY), echo=True)
        Session = sessionmaker()
        Session.configure(bind=self.engine)
        self.session = Session()
        canc.Base.metadata.bind = self.engine
        self.__db_alembic_setup()


    def __db_create(self):
        """Создает или изменяет БД в соответствии с описанной в классах структурой."""
        canc.Base.metadata.create_all()


    def __db_disconnect(self):
        """Разрывает соединение с БД."""
        self.session.close()
        self.engine.dispose()


    def __db_exists(self):
        """Проверяет наличие базы данных по пути в конфигурации."""
        db_folder_path = Path(self.config.restore_value(ccfg.DATABASE_FILE_KEY))
        return db_folder_path.exists()


    def __db_upgrade(self, revision, context):
        """Приводит структуру базы в соответствие с классами Alchemy."""
        return self.alembic_script._upgrade_revs(script.get_heads(), revision)


    def __delete_task(self):
        """Удаляет задачу"""
        pass


    def __edit_task(self):
        """Добавляет новую задачу"""
        pass


    def __save_task(self):
        """Сохраняет введённую задачу."""
        # *** Соберём введенные теги
        entered_tags = self.lineEdit_Tags.text()
        tag_name_list = entered_tags.split()
        # *** Поищем введенные теги в базе
        tag_id_list = []
        # *** Переберем полученные теги
        for tag in tag_name_list:
            
            # *** Получим ID тега
            tag_id = self.session.query(ctag.CTag.id).filter_by(fname=tag).first()
            if tag_id is None:
                
                # *** Тега такого еще нет в базе, добавляем
                tag_object = ctag.CTag(tag)
                self.session.add(tag_object)
                # *** И снова ищем. 
                tag_id = self.session.query(ctag.CTag.id).filter_by(fname=tag).first()
            
            # *** Заносим ID тега в список и удаляем его из списка необработанных тегов
            tag_id_list.append(tag_id)
            tag_index = tag_name_list.index(tag)
            del tag_name_list[tag_index]


    def __set_tags_filter(self):
        """Включает или выключает фильтрацию по тегам."""
        pass

    
    def __set_text_filter(self):
        """Включает или выключает фильтрацию по тексту задачи."""
        pass
        

    def keyPressEvent(self, event):
        """Отлавливает нажатие Ctrl-Q."""
        if (event.modifiers() & QtCore.Qt.ControlModifier):
        
            if event.key() == QtCore.Qt.Key_Q:
            
                self.close()


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()    
