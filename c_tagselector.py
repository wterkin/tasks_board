#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса селектора тегов."""
from PyQt5 import QtWidgets, QtCore
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
        print("TS:LTL:path ", uic_path)
        uic.loadUi(uic_path, self)

        tag_list = self.load_tag_list()
        print("TS:LTL:list ", tag_list)
        self.show()

    def load_tag_list(self):
        """Загружает список тэгов из базы."""
        return self.database.get_session().query(c_tag.CTag.fname).all()
        # query = query.filter(c_tag.CTag.fname.like(f"%{tag_name}%"))
""" 
for tag in tag_list[0]:
    # actions.append(menu.addAction(tag))
    menu_action = QtWidgets.QAction(tag, self)
    menu_action.setData(tag)
    menu_action.triggered.connect(self.actionClicked)
    menu.addAction(menu_action)
"""