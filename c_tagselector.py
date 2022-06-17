#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса селектора тегов."""
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5 import uic
import c_tag
from datetime import datetime


# import c_constants as const
# import c_tools as tls

class CTagSelector(QtWidgets.QMainWindow):
    def __init__(self, pparent, pdatabase, papplication_folder):
        # *** Конструктор
        super(CTagSelector, self).__init__(pparent)
        # *** Сохраняем параметры
        self.parent = pparent
        self.database = pdatabase
        self.application_folder = papplication_folder

        uic_path = self.application_folder / "ui" / "tag_selector.ui"
        # print("TS:LTL:path ", uic_path)
        uic.loadUi(uic_path, self)
        self.scroll_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.tag_list: list = self.load_tag_list()
        print("TS:LTL:list ", self.tag_list)
        self.fill_scrollbox()
        self.show()

    def load_tag_list(self):
        """Загружает список тэгов из базы."""
        return self.database.get_session().query(c_tag.CTag.fname).all()
        # query = query.filter(c_tag.CTag.fname.like(f"%{tag_name}%"))

    def fill_scrollbox(self):
        """Заполняет скроллбокс чекбоксами"""
        for tag in self.tag_list:

            checkbox = QtWidgets.QCheckBox(tag[0])
            checkbox.setCheckState(QtCore.Qt.Unchecked)
            self.scroll_layout.addWidget(checkbox)
            print(tag[0])
