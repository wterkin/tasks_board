# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса справочника событий."""

from sqlalchemy import Column, Integer, String, ForeignKey

import c_ancestor as anc
import c_tag
import c_task

class CTagLink(anc.CAncestor):
    """Класс таблицы связки тэгов к задаче."""

    __tablename__ = 'tbl_taglinks'
    # fname = Column(String,
    #                 nullable=False,
    #                 unique=True)
    ftag = Column(Integer, ForeignKey(c_tag.CTag.id))
    ftask = Column(String, ForeignKey(c_task.CTask.fguid))

    def __init__(self, ptag: int, ptask: str):
        """Конструктор"""
        super().__init__()
        self.ftag = ptag
        self.ftask = ptask


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Tag:{self.ftag},
                   Task{self.ftask}"""
