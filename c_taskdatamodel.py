#!/usr/bin/python
## -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.rufrom PyQt5 import QtCore, QtGui, QtWidgets
"""Модель для таблицы задач."""
from PyQt5 import QtGui, QtCore
# from PyQt5.QtCore import Qt

import c_task
import c_tag
import c_context

ROWS_IN_PAGE = 5 #  25
FIRST_PAGE = 0

class CTaskDataModel(QtGui.QStandardItemModel):
    """Класс модели таблицы задач."""

    def __init__(self, parent, pdatabase):
        """Конструктор."""
        QtGui.QStandardItemModel.__init__(self)
        self.gui = parent
        self.database = pdatabase
        self.page: int = 0
        self.row_count: int = ROWS_IN_PAGE
        self.col_count: int = 1
        self.context_id: int = 0
        self.tag_id: int = 0
        self.data_pool: list = []  # $$$ Временный источник данных
        self.update_model()
        self.setHorizontalHeaderLabels(["Задачи",""])
        self.setHeaderData(0, QtCore.Qt.Horizontal, QtCore.Qt.AlignJustify, QtCore.Qt.TextAlignmentRole)

    def columnCount(self, index):
        """Возвращает количество столбцов в наборе данных."""
        return self.col_count

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

    def headerData(self, section, orientation, role):
        """Возвращает заголовок таблицы."""
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return ["Задачи", ] #  [section]
            if orientation == QtCore.Qt.Vertical:
                return f"{section}"
        return ""

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

    def get_query(self):
        """Возвращает подготовленный объект запроса для разных операций."""
        query = self.database.get_session().query(c_task.CTask)
        if self.context_id > 0:

            query = query.filter_by(fcontext=self.context_id)
        if self.tag_id > 0:

            query = query.filter_by(ftag=self.tag_id)
        return query

    def query_task_count(self):
        """Получает из БД количество задач, удовлетворяющих установленным фильтрам."""
        return self.get_query().count()

    def set_context(self, pcontext_id: int):
        """Устанавливает идентификатор контекста."""
        self.context_id = pcontext_id

    def set_tag(self, ptag_id: int):
        """Устанавливает идентификатор тэга."""
        self.tag_id = ptag_id

    def update_model(self):
        """Обновляет настройки модели в соотвествии с состоянием базы."""
        task_count = self.query_task_count()
        self.page_count = task_count // ROWS_IN_PAGE
        if task_count % ROWS_IN_PAGE > 0:

            self.page_count += 1

    def update_table(self):
        """Обновляет данные в таблице"""
        query = self.get_query().offset(self.page * ROWS_IN_PAGE)
        query = query.limit(ROWS_IN_PAGE)
        data = query.all()
        self.clear()
        for item in data:

            self.appendRow(QtGui.QStandardItem(item.fdescription))
