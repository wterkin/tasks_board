#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса селектора тегов."""
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

import c_tag
import c_task
import c_context
import c_database


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

    def __init__(self, pparent, pdatabase, papplication_folder: str, pid: int):
        # *** Конструктор
        # super(CTagSelector, self).__init__(pparent)
        super().__init__()
        # *** Сохраняем параметры
        self.parent = pparent
        self.database = pdatabase
        self.application_folder: str = papplication_folder
        uic_path = self.application_folder / "ui" / "task_edit.ui"
        uic.loadUi(uic_path, self)
        # ***
        self.scroll_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.check_box_list: list = []
        self.lineEdit_Name.setText("")
        self.textEdit_Description.setText("")
        self.comboBox_Contexts.setCurrentIndex(0)
        self.comboBox_Urgency.addItems(c_database.URGENCIES)
        self.toolButton_Ok.clicked.connect(self.button_ok)
        self.fill_context_list()
        self.fill_scrollbox()
        # ***
        self.load_data(pid)
        self.show()

    def fill_context_list(self):
        """Загружает список тэгов из базы."""
        queried_data: object = self.database.get_session().query(c_context.CContext.id,
                                                                 c_context.CContext.fname)
        queried_data = queried_data.filter(c_context.CContext.fstatus > 0)
        context_list: list = queried_data.all()
        self.comboBox_Contexts.clear()
        # self.comboBox_Contexts.addItems()
        for context in context_list:
            self.comboBox_Contexts.addItem(context[1], context[0])


        # self.database.get_session().query(c_tag.CTag.fname).all()

    def load_tag_list(self):
        """Загружает список тэгов из базы."""
        return self.database.get_session().query(c_tag.CTag.fname).all()

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
        query = session.query(c_task.CTask)
        query = query.filter(c_task.CTask.id==pid)
        data: c_task.CTask = query.first()
        # combobox_Contexts
        # combobox_Urgencies
        # lineEdit_Name
        # textEdit_Description
        # self.check_box_list
        print(data)
        self.lineEdit_Name.setText(data.fname)
        self.textEdit_Description.setText(data.fdescription)
        self.comboBox_Contexts.setCurrentIndex(data.fcontext-1)