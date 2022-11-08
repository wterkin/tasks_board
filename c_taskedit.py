#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса селектора тегов."""
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic
from pathlib import Path

from c_tag import CTag
from c_taglink import CTagLink
from c_task import CTask
from c_context import CContext


def create_separator():
    """Возвращает стандартный разделитель."""

    separator = QtWidgets.QFrame()
    separator.setMinimumWidth(1)
    separator.setFixedHeight(20)
    separator.setFrameShape(QtWidgets.QFrame.HLine)
    separator.setFrameShadow(QtWidgets.QFrame.Sunken)
    separator.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
    return separator


class CTaskEdit(QtWidgets.QMainWindow):
    """Реализует окно селектора тегов."""

    def __init__(self, pparent, pdatabase, papplication_folder: Path, pid: int):
        # *** Конструктор
        super().__init__()
        # *** Сохраняем параметры
        self.parent = pparent
        self.database = pdatabase
        self.application_folder: Path = papplication_folder
        # *** Грузим интерфейс
        uic_path: Path = self.application_folder / "ui" / "task_edit.ui"
        uic.loadUi(uic_path, self)
        # *** Создаем прокручиваемый список чекбоксов для меток
        self.scroll_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        # *** Список чекбоксов меток
        self.check_box_list: list = []
        # *** Инициализируем элементы формы
        self.lineEdit_Name.setText("")  # noqa
        self.textEdit_Description.setText("")  # noqa
        self.fill_context_list()
        self.comboBox_Contexts.setCurrentIndex(0)  # noqa
        self.comboBox_Urgencies.setCurrentIndex(0)  # noqa
        self.toolButton_Ok.clicked.connect(self.button_ok)
        self.fill_scrollbox()
        self.load_data(pid)
        self.show()

    def fill_context_list(self):
        """Загружает список тэгов из базы."""
        queried_data: object = self.database.get_session().query(CContext.id,
                                                                 CContext.fname)
        queried_data = queried_data.filter(CContext.fstatus > 0)
        context_list: list = queried_data.all()
        self.comboBox_Contexts.clear()  # noqa
        for context in context_list:

            self.comboBox_Contexts.addItem(context[1], context[0])  # noqa

    def load_tag_list(self):
        """Загружает список меток из базы."""
        return self.database.get_session().query(CTag.fname).all()

    def fill_scrollbox(self):
        """Заполняет скроллбокс чекбоксами"""
        tag_list: list = self.load_tag_list()
        for tag in tag_list:

            check_box = QtWidgets.QCheckBox(tag[0])
            check_box.setCheckState(QtCore.Qt.Unchecked)
            self.scroll_layout.addWidget(check_box)
            self.scroll_layout.addWidget(create_separator())
            self.check_box_list.append(check_box)

    def button_ok(self):
        """Обработчик нажатия кнопки 'Ok'"""
        tag_list: list = []
        for checkbox in self.check_box_list:

            if checkbox.isChecked():

                tag_list.append(checkbox.text())
        self.parent.update_tag_line(" ".join(tag_list))
        self.close()

    def load_data(self, pid: int):
        """Обновляет данные в окне."""
        session = self.database.get_session()
        # query = session.query(CTask, CTag)
        query = session.query(CTask, CTag)
        query = query.filter(CTask.id == pid)
        query = query.join(CTagLink, CTagLink.ftask == CTask.fguid)
        query = query.join(CTag, CTag.id == CTagLink.ftag)
        data = query.all()
        task: CTask = data[0][0]
        # tags: [] = data[1]
        # print(data[0][1])
        # print("-"*20)
        # print(tags)
        # print(task.fstatus)
        # print(task.fcontext)
        # print("="*20)
        # ToDo: вот тут надо узнать, как получить данные
        # print("*** TE:LD:curdat", self.comboBox_Contexts.currentData())
        context_index: int = self.comboBox_Contexts.findData(task.fcontext)  # noqa
        self.comboBox_Contexts.setCurrentIndex(context_index)

        # self.comboBox_Contexts.setCurrentIndex(context_index)  # noqa
        self.lineEdit_Name.setText(task.fname)  # noqa
        self.textEdit_Description.setText(task.fdescription)  # noqa
        self.comboBox_Urgencies.setCurrentIndex(task.furgency)  # noqa
        tags: list = []
        # print("*** TE:LD:dt1 ", data[0][0])
        # print("="*20)
        # print("*** TE:LD:dt2 ", data[0][1])
        # print("="*20)
        # print("*** TE:LD:dt3 ", data[1][0])
        for task in data:

            print("*** TE:LD:task ", task[1])
        #     tags.append(tag.fname)
        # print("*** TE:LD:tgs ", tags)
