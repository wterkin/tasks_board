

        # def alembic_setup(self):
        #     """Создает среду алембика."""
        #     migrations_path = Path(Path.home() / ccfg.ALL_CONFIGS_FOLDER)
        #     if not migrations_path.exists():
        #
        #         migrations_path.mkdir()
        #     self.alembic_config = Config()
        #     self.alembic_config.set_main_option("script_location", "migrations")
        #     self.alembic_config.set_main_option("url", 'sqlite:///'+self.config.restore_value(ccfg.DATABASE_FILE_KEY))
        #     self.alembic_script = ScriptDirectory.from_config(alembic_config)
        #     self.alembic_env = EnvironmentContext(alembic_config, self. alembic_script)
        #     self.alembic_env.configure(connection=self.engine.connect(), target_metadata=cancst.Base.metadata, fn=self.upgrade)
        #     self.alembic_context = self.alembic_env.get_context()
        # self.alembic = Alembic()
        # alembic.init_app(app)
        # from alembic.config import Config
        # from alembic import command, autogenerate
        # from alembic.script import ScriptDirectory
        # from alembic.runtime.environment import EnvironmentContext


        # conn = engine.connect()
        # alembic_env.configure(connection=conn, target_metadata=metadata)
        # alembic_context = alembic_env.get_context()

# from alembic.config import Config
# from alembic import command, autogenerate
# from alembic.script import ScriptDirectory
# from alembic.runtime.environment import EnvironmentContext
        # self.alembic_setup()
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy import and_, or_
#
# from alembic.config import Config
# from alembic import command, autogenerate
# from alembic.script import ScriptDirectory
# from alembic.runtime.environment import EnvironmentContext

# import c_ancestor as cancst
# import c_config as ccfg
# import c_context as cctx
# import c_tag as ctag
# import c_task as ctsk  # =)


    #
    # def select_data(self, pcontext_id, ptag_id):
    #    """Делаем выборку для TableView."""
    #    data: list = []
    #    offset = self.page * ROWS_IN_PAGE
    #
    #    return data

        # query = self.database.get_session().query(c_task.CTask).filter_by(fcontext=pcontext_id)
        # if ptag_id > 0:
        #
        #     query = query.filter_by(ftag=ptag_id)
        # if role == Qt.DisplayRole:


    # def data(self, index, role):
        # for row in self.data_pool:
        #
        #     print(row)
        #     self.appendRow(QtGui.QStandardItem(row))
        # if not index.isValid():
        #
        #     return QtCore.QVariant()
        # if role != QtCore.Qt.DisplayRole and role != QtCore.Qt.EditRole:
        #
        #     return QtCore.QVariant()
        # if role == QtCore.Qt.DisplayRole:
        #
        #     """
        #         print("*****", self.data_pool, "!!!!!!!!!!!!!!!")
        #         return QtCore.QVariant(self.data_pool)
        #     """
        #     print(f"2.1 {index.row()} {index.column()} {self.data_pool[index.row()][index.column()]}")
        #     #QtCore.QVariant()
        #     return QtGui.QStandardItem(self.data_pool[index.row()][index.column()])
        #
        # def __repr__(self):
        #     return f"""Model: {self.task_count}"""

        # self.tableView_Main.setHorizontalHeaderSectionResizeMode(0, Stretch);
        # self.tableView_Main.horizontalHeader.setSectionResizeMode(1, QHeaderView::Fixed);        self.tableView_Main.setColumnWidth(0, self.tableView_Main.width()-4)
        # self.tableView_Main.setVerticalHeader(None)
        # self.tableView_Main.horizontalHeader().hide()
        # self.tableView_Main.setColumnWidth(0, self.tableView_Main.geometry.width)
        # self.tableView_Main.horizontalHeader().setStretchFirstSection(True)
        # self.tableView_Main.horizontalHeader().setSectionResizeMode(QtCore.QHeaderView.Stretch)
        # self.tableView_Main.setHorizontalHeadereMode(0, Stretch);


    # def query_current_page(self, pcontext_id: int, ptag_id: int):
    #     """Возвращает данные на текущей странице."""
    #     low_bound: int = self.page * ROWS_IN_PAGE
    #     high_bound: int = (self.page + 1) *ROWS_IN_PAGE
    #     for number in range(low_bound, high_bound):
    #
    #         # print(f"TDM:QCP:2 Чепуха всяческая N {number}")
    #         self.data_pool.append(f"Чепуха всяческая N {number}")
            # self.appendRow(QtGui.QStandardItem("Чепуха всяческая N {number}"))

        # return self.data_pool

        # low_bound: int = self.page * ROWS_IN_PAGE
        # high_bound: int = (self.page + 1) *ROWS_IN_PAGE
        # for number in range(low_bound, high_bound):
        #
        #     item_str = f"Чепуха всяческая N {number}"
        #     self.appendRow(QtGui.QStandardItem(item_str))

        # offset() limit()
        # self.task_model.query_current_page(self.comboBox_Contexts.currentData(), tag_id)
        # tableView_Main
        # query = self.database.get_session().query(c_task.CTask).filter_by(fcontext=self.comboBox_Contexts.currentData())
        # self.task_count: int = self.query_task_count()

        # self.page_count = self.task_count // self.row_count
        # if self.query_task_count() % self.row_count > 0:

            # self.page_count += 1

        # вот это придётся делать при каждом обновлении набора данных
        # task_count = self.query_task_count()
        # self.page_count = task_count // ROWS_IN_PAGE
        # if task_count % ROWS_IN_PAGE > 0:
        # 

        print("!!! ", self.task_model.rowCount())

        # self.task_model.query_current_page(self.comboBox_Contexts.currentData(), tag_id)
        # tableView_Main
        # query = self.database.get_session().query(c_task.CTask).filter_by(fcontext=self.comboBox_Contexts.currentData())
        # if self.lineEdit_Tags.text():
        #
        #     query = query.filter_by(ftag=self.get_tag_id())
        #     self.page_count += 1


            # print(tag_id_list)
            # print(description)
        #context_names:list = []
        #print(f"*** Mn:fcc:contid {self.context_ids}")
        #print(f"*** Mn:fcc:contname {context_names}")
        #self.comboBox_Contexts.addItems(context_names)

        def tag_menu(self, pposition):
                """Выводит меню тэгов"""

                menu = QtWidgets.QMenu()
                actions = []
                tags_line = self.lineEdit_Tags.text()
                # print("[1] ", tags_line)
                if len(tags_line) > 0:

                        if " " in tags_line:

                                tag_list = tags_line.split()
                                # print("[2] ", tag_list)
                                tag_name = tag_list[-1]
                                tag_list.pop(tag_list.index(tag_name))
                                self.lineEdit_Tags.setText(" ".join(tag_list))
                                # print("[e] ", tag_name)

                        else:

                                tag_name = tags_line
                                self.lineEdit_Tags.setText(" ")
                        # print("-----", tag_list, tag_name)

                        query = self.database.get_session().query(c_tag.CTag.fname)
                        query = query.filter(c_tag.CTag.fname.like(f"%{tag_name}%"))
                        tag_list = query.all()
                        print("[4] ", tag_list)
                        for tag in tag_list[0]:
                                # actions.append(menu.addAction(tag))
                                menu_action = QtWidgets.QAction(tag, self)
                                menu_action.setData(tag)
                                menu_action.triggered.connect(self.actionClicked)
                                menu.addAction(menu_action)
                # else:

                menu.exec_(self.lineEdit_Tags.mapToGlobal(pposition))
