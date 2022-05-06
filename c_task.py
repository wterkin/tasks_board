# @author: Andrey Pakhomenkov pakhomenkov@yandex.ru
"""Модуль класса задач."""
import uuid
from sqlalchemy import Column, ForeignKey, Integer, String

import c_ancestor
import c_context
class CTask(c_ancestor.CAncestor):
    """Класс таблицы задач."""

    __tablename__ = 'tbl_tasks'

    fcontext = Column(Integer, ForeignKey(c_context.CContext.id))
    fdescription = Column(String,
                          nullable=False,
                          unique=True)
    fguid = Column(String,
                   nullable=False,
                   unique=True)
    # fnotice = Column(Text)
    furgency = Column(Integer,
                     nullable=False
                     )


    def __init__(self, pcontext, pdescription, purgency):
        """Конструктор"""
        super().__init__()
        self.guid_generation()
        self.fcontext = pcontext
        self.fdescription = pdescription
        self.furgency = purgency


    def __repr__(self):
        ancestor_repr = super().__repr__()
        return f"""{ancestor_repr},
                   Context:{self.fcontext},
                   Desc:{self.fdescription},
                   GUID:{self.fguid},
                   Notice:{self.furgency}"""


    def get_guid(self):
        """Возвращает сгенерированный GUID."""
        return self.fguid


    def guid_generation(self):
        """Генерирует GUID."""
        guid_string = str(uuid.uuid1())
        guid_list = guid_string.split("-")
        self.fguid = "".join(guid_list)
