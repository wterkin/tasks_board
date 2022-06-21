#!/usr/bin/python
# -*- coding: utf-8 -*-
# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru

# py lint: disable=C0301

"""Модуль конфигурации."""
from sys import platform
from pathlib import Path
import json
from os.path import expanduser

APP_NAME: str = "tasks_board"
HOME_PREFIX: str = expanduser("~")
# if platform == "linux" or platform == "linux2":
if platform in ("linux", "linux2"):
    HOME_PREFIX += "/.config"
    APP_FOLDER: str = f"{HOME_PREFIX}/{APP_NAME}"
else:
    APP_FOLDER: str = f"{HOME_PREFIX}/.{APP_NAME}"
CONFIG_FILE_NAME: str = f"{APP_NAME}.json"
DATABASE_FILE_NAME: str = f"{APP_NAME}.db"
DATABASE_FILE_KEY: str = "database_file_name"
CONTEXT_COMBO_KEY: str = "contexts"


class CConfiguration():
    """Класс конфигурации программы."""

    def __init__(self):
        """Конструктор."""

        # *** Соберём путь к домашнему каталогу программы и создадим каталог, если его нет.
        self.home_folder_path: object = Path(Path.home() / APP_FOLDER)
        # print("CFG:INIT:HFP ", self.home_folder_path)
        if not self.home_folder_path.exists():
            self.home_folder_path.mkdir()
        # *** Конфиг будет лежать в домашнем каталоге. Создадим его, если его нет.
        config_file: object = self.home_folder_path / CONFIG_FILE_NAME
        # print("CFG:INIT:CFL ", config_file)
        if config_file.exists():

            self.read_config()
        else:

            self.config: dict = {}
        # *** Если в конфиге не прописана БД, пропишем её.
        if DATABASE_FILE_KEY not in self.config:
            self.store_value(DATABASE_FILE_KEY,
                             str(self.home_folder_path / DATABASE_FILE_NAME))
            self.write_config()

    def store_value(self, pkey: str, pvalue: str) -> bool:
        """Сохраняет заданное значение по заданному ключу в словарь конфигурации."""
        result = False
        if pkey:

            if pvalue:

                self.config[pkey] = pvalue
                result = True
        return result

    def restore_value(self, pkey):
        """Возвращает значение, сохраненное в словаре конфигурации по заданному ключу."""
        if pkey in self.config:

            return self.config[pkey]
        return None

    def write_config(self):
        """Сохраняет словарь конфигурации в файл в формате json."""
        # config_file = open(Path.home() / CONFIG_FOLDER / CONFIG_FILE_NAME, "w", encoding="utf-8")
        with open(self.home_folder_path / CONFIG_FILE_NAME, "w", encoding="utf-8") as config_file:

            config_file.write(json.dumps(self.config, sort_keys=True, indent=4))
        # config_file.close()

    def read_config(self):
        """Считывает сохраненную конфигурацию из json файла в словарь."""
        # config_file = open(Path.home() / CONFIG_FOLDER / CONFIG_FILE_NAME, "r", encoding="utf-8")
        with open(Path.home() / APP_FOLDER / CONFIG_FILE_NAME, "r", encoding="utf-8") as config_file:

            self.config = json.load(config_file)
        # print("CFG:RCFG:CFG ", self.config)
