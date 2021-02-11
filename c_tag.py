# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Table, Column, String

import c_ancestor as anc

class CTag(anc.CAncestor):
    """Класс справочника событий."""

    __tablename__ = 'tbl_tags'
    fname = Column(String,
                    nullable=False,
                    unique=True)


    def __init__(self, pstatus, pname):
        """Конструктор"""
        super().__init__(pstatus)
        self.fname = pname


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname}"""

  
