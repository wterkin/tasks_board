#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса селектора тегов."""
from PyQt5 import QtWidgets, QtCore
from PyQt5 import uic

import c_tag
import c_task


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
        self.scroll_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.check_box_list: list = []
        self.toolButton_Ok.clicked.connect(self.button_ok)
        self.fill_scrollbox()
        self.update(pid)
        self.show()

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

    def update(self, pid: int):
        """Обновляет данные в окне."""
        session = self.database.get_session
        query = session.query(c_task.CTask)
        query = query.filter(id=pid)
        data = query.first()


        if pid is not None:

            pass