# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса задач."""
import uuid
from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime

import c_ancestor
import c_context


class CTask(c_ancestor.CAncestor):
    """Класс таблицы задач."""

    __tablename__ = 'tbl_tasks'

    fcontext = Column(Integer, ForeignKey(c_context.CContext.id))
    fname = Column(String,
                   nullable=False,
                   unique=False)
    fdescription = Column(Text, nullable=True)
    fguid = Column(String,
                   nullable=False,
                   unique=True)
    furgency = Column(Integer,
                      nullable=False
                      )
    fdatetime = Column(DateTime,
                       nullable=False
                       )

    def __init__(self, pcontext, pname, pdescription, purgency):
        """Конструктор"""
        super().__init__()
        self.guid_generation()
        self.fcontext = pcontext
        self.fname = pname
        self.fdescription = pdescription
        self.furgency = purgency
        self.fdatetime = datetime.now()

    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Context:{self.fcontext},
                   Name:{self.fname},
                   Desc:{self.fdescription},
                   GUID:{self.fguid},
                   Notice:{self.furgency},
                   Datetime:{self.fdatetime}"""

    def get_guid(self):
        """Возвращает сгенерированный GUID."""
        return self.fguid

    def guid_generation(self):
        """Генерирует GUID."""
        guid_string = str(uuid.uuid1())
        guid_list = guid_string.split("-")
        self.fguid = "".join(guid_list)
