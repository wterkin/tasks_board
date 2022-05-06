

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
