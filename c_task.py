# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса задач."""

from sqlalchemy import Table, Column, String, Text

import c_ancestor as anc

class CTask(anc.CAncestor):
    """Класс справочника событий."""

    __tablename__ = 'tbl_tasks'
    fdescription = Column(String,
                          nullable=False,
                          unique=True)
    fnotice = Column(Text)


    def __init__(self, pdescription, pnotice):
        """Конструктор"""
        super().__init__()
        self.fdescription = pdescription
        self.fnotice = pnotice


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Desc:{self.fdescription},
                   Notice:{self.fnotice}"""
