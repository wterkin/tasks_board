# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Column, String

import c_ancestor as anc

class CTag(anc.CAncestor):
    """Класс справочника тэгов."""

    __tablename__ = 'tbl_tags'
    fname = Column(String,
                    nullable=False,
                    unique=True)


    def __init__(self, pname: object) -> object:
        """Конструктор"""
        super().__init__()
        self.fname = pname


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Name:{self.fname}"""
