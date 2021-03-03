# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса задач."""

from sqlalchemy import Table, Column, String, Text

import c_ancestor as anc
import uuid

class CTask(anc.CAncestor):
    """Класс справочника событий."""

    __tablename__ = 'tbl_tasks'
    
    fguid = Column(String,
                   nullable=False,
                   unique=True)
    fdescription = Column(String,
                          nullable=False,
                          unique=True)
    fnotice = Column(Text)


    def __init__(self, pdescription, pnotice):
        """Конструктор"""
        super().__init__()
        self.__GUID_generation()
        self.fdescription = pdescription
        self.fnotice = pnotice
        

    def __GUID_generation(self):
        """Генерирует GUID."""
        guid_string = str(uuid.uuid1())
        guid_list = guid_string.split("-")
        self.fguid = "".join(guid_list)

    
    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Desc:{self.fdescription},
                   Notice:{self.fnotice}"""


    def get_GUID(self):
        """Возвращает сгенерированный GUID."""
        return fguid
