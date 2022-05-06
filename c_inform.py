# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Column, Integer

import c_ancestor as anc

class CInformation(anc.CAncestor):
    """Класс справочника событий."""

    __tablename__ = 'tbl_inform'
    fversion = Column(Integer,
                      nullable=False,
                      unique=False)


    def __init__(self, pversion: int):
        """Конструктор"""
        super().__init__()
        self.fversion: int = pversion


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Version:{self.fversion}"""
