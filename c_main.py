#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
""" Органайзер задач. """

import sys

from pathlib import Path

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5 import uic

import c_database
import c_config
import c_context
import c_tag
import c_task
import c_taglink

PROGRAM_VERSION = "0.0"
MAIN_WINDOW_FORM = "mainwindow.ui"
FORM_FOLDER = "ui/"
HEADER_TEXT = "Ты должен делать то, что должен."


class CMainWindow(QtWidgets.QMainWindow):
    """Класс."""

    def __init__(self):
        """Конструктор класса."""
        # super(CMainWindow, self).__init__()
        super().__init__()
        self.application_folder: Path = Path.cwd()

        # *** Конфигурация
        self.config: CConfiguration = c_config.CConfiguration()
        self.context_ids: list = []

        # *** Интерфейс
        uic.loadUi(self.application_folder / FORM_FOLDER / MAIN_WINDOW_FORM, self)
        self.setWindowTitle(f"Tasks board ver. {PROGRAM_VERSION} : \"{HEADER_TEXT}\"")
        self.setWindowIcon(QtGui.QIcon('ui/tasks_board.ico'))

        # *** База данных
        self.database: CDataBase = CDataBase(self.config)
        if not self.database.exists():

            self.database.create()

        # *** Обработчики
        self.toolButton_Apply.clicked.connect(self.save_task)
        self.toolButton_TagsFilter.clicked.connect(self.set_tags_filter)
        self.toolButton_TextFilter.clicked.connect(self.set_text_filter)
        self.pushButton_EditTask.clicked.connect(self.edit_task)
        self.pushButton_DeleteTask.clicked.connect(self.delete_task)

        self.fill_contexts_combo()
        # *** Показываем окно
        self.show()
        # self.update()
        # *** Компоненты
        # lineEdit_TagsFilter
        # lineEdit_TextFilter
        # checkBox_ShowCompleted
        # checkBox_ShowDeleted
        # tableWidget_Tasks
        # statusBar
        # toolButton_TagsFilter
        # toolButton_TextFilter
        # toolButton_Quit
        # toolButton_Apply

    def delete_task(self):
        """Удаляет задачу"""
        pass

    def edit_task(self):
        """Добавляет новую задачу"""
        pass

    def fill_contexts_combo(self):
        """Заполняет выпадающий список контекстов."""
        queried_data: object = self.database.get_session().query(c_context.CContext.id,
                                                                 c_context.CContext.fname)
        queried_data = queried_data.filter(c_context.CContext.fstatus > 0)
        context_list: list = queried_data.all()
        #context_names:list = []
        self.comboBox_Contexts.clear()
        for context in context_list:

            self.comboBox_Contexts.addItem(context[1], context[0])
        #print(f"*** Mn:fcc:contid {self.context_ids}")
        #print(f"*** Mn:fcc:contname {context_names}")
        #self.comboBox_Contexts.addItems(context_names)

    def parse_entered_tags(self, ptag_name_list: list)-> list:
        """Парсит список введенных тегов, возвращает список ID тэгов в базе."""

        tag_id_list: list = []
        for tag in ptag_name_list:

            # *** Получим ID тега
            tag_id = self.database.get_session().query(c_tag.CTag.id).filter_by(fname=tag).first()
            if tag_id is None:

                # *** Тега такого еще нет в базе, добавляем
                tag_object = c_tag.CTag(tag)
                self.database.get_session().add(tag_object)
                self.database.get_session().commit()
                # *** И снова ищем.
                tag_id = self.database.get_session().query(c_tag.CTag.id).filter_by(fname=tag).first()

            # *** Заносим ID тега в список и удаляем его из списка необработанных тегов
            tag_id_list.append(tag_id[0])
            tag_index = ptag_name_list.index(tag)
            del ptag_name_list[tag_index]
        return tag_id_list

    def save_task(self):
        """Сохраняет введённую задачу."""

        context_id: int = self.comboBox_Contexts.currentData()
        urgency: int = self.comboBox_Urgency.currentIndex()
        description: str = self.lineEdit_Task.text()
        task_object: object = c_task.CTask(context_id, description, urgency)
        task_guid: str = task_object.get_guid()
        self.database.get_session().add(task_object)
        self.database.get_session().commit()
        # *** Соберём введенные теги
        entered_tags: str = self.lineEdit_Tags.text()
        tag_name_list: list = entered_tags.split()
        # *** Поищем введенные теги в базе
        tag_id_list: list = self.parse_entered_tags(tag_name_list)
        # *** По-любому они теперь в базе. Нужно добавлять ссылки в таблицу ссылок
        # print(tag_id_list)
        for tag_id in tag_id_list:

            taglink_object = c_taglink.CTagLink(tag_id, task_guid)
            self.database.get_session().add(taglink_object)
        self.database.get_session().commit()
        self.lineEdit_Task.clear()
        self.lineEdit_Tags.clear()

    def set_tags_filter(self):
        """Включает или выключает фильтрацию по тегам."""
        pass

    def set_text_filter(self):
        """Включает или выключает фильтрацию по тексту задачи."""
        pass

    def keyPressEvent(self, event):  # pylint: disable-msg=C0103
        """Отлавливает нажатие Ctrl-Q."""
        if event.modifiers() & Qt.ControlModifier:

            if event.key() == Qt.Key_Q:

                self.close()


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()
