#! /usr/bin/python3
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
""" Органайзер задач. """

import sys

from pathlib import Path

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5 import uic
# import PyQt5.QtGui
# from PyQt5.uic.properties import QtCore

import c_database
import c_config
import c_context
import c_tag
import c_task
import c_taglink
import c_taskdatamodel
import c_tagselector
import c_taskedit

PROGRAM_VERSION = "0.0"
MAIN_WINDOW_FORM = "mainwindow.ui"
FORM_FOLDER = "ui/"
HEADER_TEXT = "Ты должен делать то, что должен."

URGENCY_LIST: tuple = ("Не срочно.",
                       "Срочно!",
                       "Очень срочно!!")

# Done: Комбик контекстов маловат. Удлинить и увеличить шрифт
# Done: Вставить разделитель перед фильтром по тэгам, да и вообще натыкать их побольше
# Done: Вместо строки ввода тэга влепить комбик lineEdit_Tags comboBox_Tags
# Done: Фильтровать содержимое комбика в зависимости от введенной строки
# Done: Найти иконку для просмотра выполненных задач
# Done: Найти иконку для корзины
# Done: Сделать серые варианты этих иконок
# Done: При чтении из конфига
# ToDo: Реализовать отметку задачи выполненной
# ToDo: Реализовать удаление
# ToDo: Реализовать редактирование
# ToDo: Обработать установку галочки "Все контексты"
# ToDo: Реализовать фильтр по тэгам
# ToDo: Реализовать фильтр по тексту
# ToDo: Сделать иконки фильтров динамическими
# ToDo: Добавить в грид колонку контекстов, если установлена галочка
# ToDo: Добавить цветовое выделение в зависимости от срочности
# ToDo: Добавить в грид колонки даты и тэгов
# ToDo: В модели навигация хромает

HEADER_STYLE = '''
                   ::section {
                     background-color: lightgray;
                     border-style: flat;
                     padding: 0px 5px;
                    }'''


def formalize_tags(ptags):
    """Приводит теги к нижнему регистру и выкидывает # из названий."""
    clean_tags = ''.join(letter for letter in ptags if letter != "#")
    return clean_tags.lower()


class CMainWindow(QtWidgets.QMainWindow):
    """Класс."""

    def __init__(self):
        """Конструктор класса."""
        # super(CMainWindow, self).__init__()
        super().__init__()
        self.task_edit = None
        self.application_folder: Path = Path.cwd()

        # *** Конфигурация
        self.config: c_config.CConfiguration = c_config.CConfiguration()
        self.context_ids: list = []

        # *** Интерфейс
        uic.loadUi(self.application_folder / FORM_FOLDER / MAIN_WINDOW_FORM, self)
        self.setWindowTitle(f"Tasks board ver. {PROGRAM_VERSION} : \"{HEADER_TEXT}\"")
        self.setWindowIcon(QtGui.QIcon('ui/tasks_board4.ico'))

        # *** База данных
        self.database: c_database.CDataBase = c_database.CDataBase(self.config)
        if not self.database.exists():
            self.database.create()
        # *** Обработчики кнопок
        self.toolButton_CompleteTask.clicked.connect(self.complete_task)
        self.toolButton_DeleteTask.clicked.connect(self.delete_task)
        self.toolButton_EditTask.clicked.connect(self.edit_task)
        self.toolButton_NavBottom.clicked.connect(self.nav_bottom)
        self.toolButton_NavDown.clicked.connect(self.nav_down)
        self.toolButton_NavTop.clicked.connect(self.nav_top)
        self.toolButton_NavUp.clicked.connect(self.nav_up)
        self.toolButton_Quit.clicked.connect(self.quit)
        self.toolButton_SaveTask.clicked.connect(self.save_task)
        self.toolButton_TagsFilter.clicked.connect(self.set_tags_filter)
        self.toolButton_TextFilter.clicked.connect(self.set_text_filter)
        self.toolButton_ViewCompleted.clicked.connect(self.view_completed)
        self.toolButton_ViewDeleted.clicked.connect(self.view_deleted)
        self.toolButton_TagSelector.clicked.connect(self.tag_selector)
        self.fill_contexts_combo()
        self.comboBox_Contexts.currentIndexChanged.connect(self.on_combobox_contexts_changed)
        # *** Показываем окно
        self.task_model = c_taskdatamodel.CTaskDataModel(self.database)
        self.tableView_Main.setColumnHidden(0, True)
        self.tableView_Main.setColumnWidth(0, 1)
        self.tableView_Main.hideColumn(0)
        self.tableView_Main.setModel(self.task_model)
        header = self.tableView_Main.horizontalHeader()
        header.setSectionResizeMode(header.Stretch)
        header.setStyleSheet(HEADER_STYLE)
        self.show()
        self.nav_state(0)
        self.update_grid()
        combo_index = self.config.restore_value(c_config.CONTEXT_COMBO_KEY)
        # print("*** MN:IN:cmbin ", combo_index)
        if combo_index:

            # print("*** MN:IN:cmbind setted")
            self.comboBox_Contexts.setCurrentIndex(combo_index)
        # self.comboBox_Urgency.addItems(c_database.URGENCIES)
        # *** Компоненты
        # lineEdit_TagsFilter
        # lineEdit_TextFilter
        # statusBar
        self.tableView_Main.hideColumn(0)

    def complete_task(self):
        """Завершает задачу"""

    def delete_task(self):
        """Удаляет задачу"""

    def edit_task(self):
        """Изменяет ранее введенную задачу."""
        """Вызывает окно селектора тэгов."""
        # row = self.tableView_Main.selectionModel()
        idx = self.tableView_Main.currentIndex()
        ident = self.tableView_Main.model().data(self.tableView_Main.model().index(idx.row(), 0))
        # QModelIndex
        # currentDiscount = ui->discountsTableView->currentIndex();
        # qDebug() << ui->discountsTableView->model()->data(ui->discountsTableView->model()->
        # index(currentDiscount.row(),
        #                                                                                          1), 0);
        # print(idx, ident)
        self.task_edit = c_taskedit.CTaskEdit(pparent=self,
                                              pdatabase=self.database,
                                              papplication_folder=self.application_folder,
                                              pid=ident)
        # window.show()

    def fill_contexts_combo(self):
        """Заполняет выпадающий список контекстов."""
        queried_data: object = self.database.get_session().query(c_context.CContext.id,
                                                                 c_context.CContext.fname)
        queried_data = queried_data.filter(c_context.CContext.fstatus > 0)
        context_list: list = queried_data.all()
        self.comboBox_Contexts.clear()
        for context in context_list:

            self.comboBox_Contexts.addItem(context[1], context[0])

    def get_tag_id(self):
        """Возвращает ID первого введенного тега."""
        tag: str = self.lineEdit_Tags.text().split()[0]  # comboBox_Tags
        return self.database.get_session().query(c_tag.CTag.id).filter_by(fname=tag).first()

    def nav_state(self, page):
        """Разрешает и запрещает кнопки навигации."""
        print("MN:NST:page ", page)
        if page == 0:

            self.toolButton_NavTop.setEnabled(False)
            self.toolButton_NavUp.setEnabled(False)
            self.toolButton_NavDown.setEnabled(True)
            self.toolButton_NavBottom.setEnabled(True)
        elif page < self.task_model.get_page_count() - 1:

            self.toolButton_NavTop.setEnabled(True)
            self.toolButton_NavUp.setEnabled(True)
            self.toolButton_NavDown.setEnabled(True)
            self.toolButton_NavBottom.setEnabled(True)
        else:

            self.toolButton_NavTop.setEnabled(True)
            self.toolButton_NavUp.setEnabled(True)
            self.toolButton_NavDown.setEnabled(False)
            self.toolButton_NavBottom.setEnabled(False)

    def nav_top(self):
        """Вывести в грид первую страницу данных."""
        page: int = self.task_model.first_page()
        self.nav_state(page)
        self.update_grid()

    def nav_up(self):
        """Вывести в грид предыдущую страницу данных."""
        page: int = self.task_model.prev_page()
        self.nav_state(page)
        self.update_grid()

    def nav_down(self):
        """Вывести в грид следующую страницу данных."""
        page: int = self.task_model.next_page()
        self.nav_state(page)
        self.update_grid()

    def nav_bottom(self):
        """Вывести в грид последнюю страницу данных."""
        page: int = self.task_model.last_page()
        self.nav_state(page)
        self.update_grid()

    def on_combobox_contexts_changed(self):
        """Обработчик события от комбобокса контекстов."""
        self.update_grid()
        self.config.store_value(c_config.CONTEXT_COMBO_KEY, self.comboBox_Contexts.currentIndex())

    def parse_entered_tags(self, ptag_name_list: list) -> list:
        """Парсит список введенных тегов, возвращает список ID тэгов в базе."""
        tag_id_list: list = []
        # tag_object: c_tag.CTag
        # print("*** MN:PET:TNL ", ptag_name_list)
        for tag in ptag_name_list:

            # *** Получим ID тега
            tag_id = self.database.get_session().query(c_tag.CTag.id).filter_by(fname=tag).first()
            # print("*** MN:PET:TID ", tag_id)
            if tag_id is None:
                # *** Тега такого еще нет в базе, добавляем
                tag_object: c_tag.CTag = c_tag.CTag(tag)
                self.database.get_session().add(tag_object)
                self.database.get_session().commit()
                # *** И снова ищем.
                tag_id = self.database.get_session().query(c_tag.CTag.id).filter_by(fname=tag).first()

            # print("*** MN:PET:TID2 ", tag_id)
            # *** Заносим ID тега в список и удаляем его из списка необработанных тегов
            tag_id_list.append(tag_id[0])
            tag_index = ptag_name_list.index(tag)
            # del ptag_name_list[tag_index]
            # print("*** MN:PET: ", tag, tag_id, tag_index)
        return tag_id_list

    def quit(self):
        """Завершает работу программы."""
        self.config.store_value(c_config.CONTEXT_COMBO_KEY, self.comboBox_Contexts.currentIndex())
        self.config.write_config()
        self.close()

    def save_task(self):
        """Сохраняет введённую задачу."""

        task_name: str = self.lineEdit_Task.text()
        if task_name:

            context_id: int = self.comboBox_Contexts.currentData()
            urgency: int = self.comboBox_Urgency.currentIndex()
            task_object: object = c_task.CTask(context_id, task_name, "", urgency)
            task_guid: str = task_object.get_guid()
            self.database.get_session().add(task_object)
            self.database.get_session().commit()
            # *** Соберём введенные теги
            entered_tags: str = formalize_tags(self.lineEdit_Tags.text())  # comboBox_Tags
            if not entered_tags:

                entered_tags = c_database.EMPTY_TAG
            tag_name_list: list = entered_tags.split()
            # print("*** MN:ST:TNL", tag_name_list)
            # *** Поищем введенные теги в базе
            tag_id_list: list = self.parse_entered_tags(tag_name_list)
            # print("*** MN:ST:TIL", tag_id_list)
            # *** По-любому они теперь в базе. Нужно добавлять ссылки в таблицу ссылок
            for tag_id in tag_id_list:

                taglink_object = c_taglink.CTagLink(tag_id, task_guid)
                self.database.get_session().add(taglink_object)
                print(tag_id)
            self.database.get_session().commit()
            self.lineEdit_Task.clear()
            self.lineEdit_Tags.clear()  # comboBox_Tags
            self.update_grid()

    def set_tags_filter(self):
        """Включает или выключает фильтрацию по тегам."""

    def set_text_filter(self):
        """Включает или выключает фильтрацию по тексту задачи."""

    def tag_selector(self):
        """Вызывает окно селектора тэгов."""
        window = c_tagselector.CTagSelector(pparent=self,
                                            pdatabase=self.database,
                                            papplication_folder=self.application_folder)
        window.show()

    def update_grid(self):
        """Обновляет содержимое грида."""
        tag_id = -1
        if self.lineEdit_Tags.text():
            tag_id = self.get_tag_id()
        self.task_model.set_context(self.comboBox_Contexts.currentData())
        self.task_model.set_tag(tag_id)
        self.task_model.update()
        self.task_model.update_model()
        self.tableView_Main.hideColumn(0)

    def update_button_state(self):
        """Управляет состояниями кнопок интерфейса."""

    def update_tag_line(self, ptag_line):
        """Обновляет строку тегов задачи."""
        self.lineEdit_Tags.setText(ptag_line)

    def view_completed(self):
        """Показывает/скрывает завершенные задачи."""

    def view_deleted(self):
        """Показывает/скрывает удалённые задачи."""

    def keyPressEvent(self, event):  # pylint: disable-msg=C0103
        """Отлавливает нажатие Ctrl-Q."""
        if event.modifiers() & Qt.ControlModifier:

            if event.key() == Qt.Key_Q:
                self.close()


if __name__ == '__main__':
    application = QtWidgets.QApplication(sys.argv)
    main_window = CMainWindow()
    application.exec_()
