#!/usr/bin/python
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.rufrom PyQt5 import QtCore, QtGui, QtWidgets
"""Модель для таблицы задач."""
from PyQt5 import QtGui, QtCore
# from PyQt5.QtCore import Qt

# import c_task

ROWS_IN_PAGE = 5 #  25
TOTAL_TASK_COUNT = 250  # $$$$
FIRST_PAGE = 0
# LAST_PAGE = -2

class CTaskDataModel(QtGui.QStandardItemModel):
    """Класс модели таблицы задач."""

    def __init__(self, parent, pdatabase):
        """Конструктор."""
        QtGui.QStandardItemModel.__init__(self)
        self.gui = parent
        self.database = pdatabase
        self.page = 0
        self.row_count = ROWS_IN_PAGE
        self.col_count = 1
        self.task_count = self.query_task_count()
        self.page_count = self.task_count // self.row_count
        self.context_id: int = 0
        self.tag_id: int = 0
        if self.task_count % self.row_count > 0:

            self.page_count += 1

        self.data_pool: list = []  # $$$ Временный источник данных

        # вот это придётся делать при каждом обновлении набора данных
        self.page_count = (self.task_count // ROWS_IN_PAGE)
        if self.task_count % ROWS_IN_PAGE > 0:

            self.page_count += 1
        self.setHorizontalHeaderLabels(["Задачи",""])
        self.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.Qt.AlignJustify, QtCore.Qt.TextAlignmentRole)

    def headerData(self, section, orientation, role):
        """Возвращает заголовок таблицы."""
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return ["Задачи", ] #  [section]
            if orientation == QtCore.Qt.Vertical:
                return f"{section}"
        return ""

    def columnCount(self, index):
        """Возвращает количество столбцов в наборе данных."""
        return self.col_count  # len(self._data[0])

    def first_page(self):
        """Переключаемся на первую страницу данных."""
        self.page = 0
        self.update_table()
        return self.page

    def get_page(self):
        """Возвращает номер текущей страницы набора данных."""
        return self.page

    def get_page_count(self):
        """Возвращает количество страниц в наборе данных."""
        return self.page_count

    def last_page(self):
        """Переключаемся на последнюю страницу данных."""
        self.page = self.page_count - 1
        self.update_table()
        return self.page

    def next_page(self):
        """Переключаемся на следующую страницу данных."""
        if self.page < (self.page_count - 1):

            self.page += 1
        self.update_table()
        return self.page

    def page_number(self):
        """Возвращает номер страницы в наборе данных."""
        return self.page

    def prev_page(self):
        """Переключаемся на предыдущую страницу данных."""
        if self.page > 0:

            self.page -=1
        self.update_table()
        return self.page

    def query_task_count(self):
        """Получает из БД количество задач, удовлетворяющих установленным фильтрам."""
        return TOTAL_TASK_COUNT  # !!!!

    def set_context(self, pcontext_id: int):
        """Устанавливает идентификатор контекста."""
        self.context_id = pcontext_id

    def set_tag(self, ptag_id: int):
        """Устанавливает идентификатор тэга."""
        self.tag_id = ptag_id

    def update_table(self):
        """Обновляет данные в таблице"""
        # offset() limit()
        # self.task_model.query_current_page(self.comboBox_Contexts.currentData(), tag_id)
        # tableView_Main
        # query = self.database.get_session().query(c_task.CTask).filter_by(fcontext=self.comboBox_Contexts.currentData())

        self.clear()
        low_bound: int = self.page * ROWS_IN_PAGE
        high_bound: int = (self.page + 1) *ROWS_IN_PAGE
        for number in range(low_bound, high_bound):

            item_str = f"Чепуха всяческая N {number}"
            self.appendRow(QtGui.QStandardItem(item_str))
