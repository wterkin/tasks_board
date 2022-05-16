#!/usr/bin/python
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.rufrom PyQt5 import QtCore, QtGui, QtWidgets
"""Модель для таблицы задач."""
from PyQt5 import QtCore
# from PyQt5.QtCore import Qt

import c_task

PAGES_IN_FRAME = 10

class CTaskDataModel(QtCore.QAbstractTableModel):
    """Класс модели таблицы задач."""

    def __init__(self, pdatabase):
        """Конструктор."""
        # super(CTaskDataModel, self).__init__()
        super().__init__()
        # self._data = data
        self.database = pdatabase
        self.page = 0
        self.frame = 0
        self.select_sql = ""

    # def data(self, index, role):
    #     if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            # return self._data[index.row()][index.column()]

    def rowCount(self, index):
        """Возвращает количество строк в наборе данных."""
        return len(self._data)

    def columnCount(self, index):
        """Возвращает количество столбцов в наборе данных."""
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def next_frame(self):
        """Переключаемся на следующий фрейм страниц."""

    def next_page(self):
        """Переключаемся на следующую страницу данных."""

    def prev_frame(self):
        """Переключаемся на предыдущий фрейм страниц."""

    def prev_page(self):
        """Переключаемся на предыдущую страницу данных."""

    def select_data(self, pcontext_id, ptag_id):
        """Делаем выборку для TableView."""

        query = self.database.get_session().query(c_task.CTask).filter_by(fcontext=pcontext_id)
        if ptag_id > 0:

            query = query.filter_by(ftag=ptag_id)
        # if role == Qt.DisplayRole:
