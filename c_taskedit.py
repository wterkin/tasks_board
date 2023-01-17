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
        self.id: int = 0
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

    def button_ok(self):
        """Обработчик нажатия кнопки 'Ok'"""
        self.save_data()
        """
        tag_list: list = []
        for checkbox in self.check_box_list:

            if checkbox.isChecked():

                tag_list.append(checkbox.text())
        self.parent.update_tag_line(" ".join(tag_list))
        self.close()
        """

    def fill_context_list(self):
        """Загружает список тэгов из базы."""
        queried_data: object = self.database.get_session().query(CContext.id,
                                                                 CContext.fname)
        queried_data = queried_data.filter(CContext.fstatus > 0)
        context_list: list = queried_data.all()
        self.comboBox_Contexts.clear()  # noqa
        for context in context_list:

            self.comboBox_Contexts.addItem(context[1], context[0])  # noqa

    def get_task_data(self, pid):
        session = self.database.get_session()
        query = session.query(CTask, CTag)
        query = query.filter(CTask.id == pid)
        query = query.join(CTagLink, CTagLink.ftask == CTask.fguid)
        query = query.join(CTag, CTag.id == CTagLink.ftag)
        data = query.all()
        return data

    def fill_scrollbox(self):
        """Заполняет скроллбокс чекбоксами"""
        tag_list: list = self.load_tag_list()
        for tag in tag_list:

            check_box = QtWidgets.QCheckBox(tag[0])
            check_box.setCheckState(QtCore.Qt.Unchecked)
            self.scroll_layout.addWidget(check_box)
            self.scroll_layout.addWidget(create_separator())
            self.check_box_list.append(check_box)

    def load_data(self, pid: int):
        """Обновляет данные в окне."""
        # *** Получим данные этой задачи из БД
        data = self.get_task_data(pid)
        # *** Выведем основные данные
        task: CTask = data[0][0]
        context_index: int = self.comboBox_Contexts.findData(task.fcontext)  # noqa
        self.comboBox_Contexts.setCurrentIndex(context_index)  # noqa
        self.lineEdit_Name.setText(task.fname)  # noqa
        self.textEdit_Description.setText(task.fdescription)  # noqa
        self.comboBox_Urgencies.setCurrentIndex(task.furgency)  # noqa

        # *** Займёмся тэгами. Вытащим их все и занесем в список.
        tags: list = []
        for task in data:

            tags.append(task[1].fname)
            # print("*** TE:LD:task ", task[1])

        # *** Теперь. Переберем все чекбоксы тэгов на форме и выставим галочки в тех,
        # *** на которые ссылается наша задача.
        for check_box in self.check_box_list:

            if check_box.text() in tags:

                check_box.setCheckState(True)

        #     tags.append(tag.fname)
        # print("*** TE:LD:tgs ", tags)
        # print("*** TE:LD:dt1 ", data[0][0])
        # print("="*20)
        # print("*** TE:LD:dt2 ", data[0][1])
        # print("="*20)
        # print("*** TE:LD:dt3 ", data[1][0])

        # tags: [] = data[1]
        # print(data[0][1])
        # print("-"*20)
        # print(tags)
        # print(task.fstatus)
        # print(task.fcontext)
        # print("="*20)

    def load_tag_list(self):
        """Загружает список меток из базы."""
        return self.database.get_session().query(CTag.fname).all()

    def save_data(self):
        """Сохраняет измененные данные в БД."""
        # *** 1. Контекст
        context_index: int = self.comboBox_Contexts.getCurrentIndex()  # noqa
        # *** 2. Срочность
        urgency_index: int = self.comboBox_Urgency.getCurrentIndex()  # noqa
        # *** 3. Название
        name_text: str = self.lineEdit_Name.Text()  # noqa
        # *** 4. Описание
        description_text: str = self.textEdit_Description.Text()  # noqa
        # *** 5. Сохраняем данные в базе
        # *** 6. Теги
        # * 6.1 Получим список ID и названий тэгов, ассоциированных с этой записью из БД. l1
        data = self.get_task_data(self.id)
        tags: list = []
        for task in data:
            tags.append(task[1].fname)

        # * 6.2 Получим список ID и названий тэгов, выбранных в окне редактирования. l2
        # * 6.3 Сравниваем l1 с l2. если чего-то не находим в l2 - удаляем из l1
        # * 6.4 Сравниваем l2 с l1. если чего-то не находим в l1 - добавляем в бд
        # * 6.5 Вуаля, теги синхронизированы.
