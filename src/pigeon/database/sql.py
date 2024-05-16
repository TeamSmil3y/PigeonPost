from typing import Any
import sqlalchemy
import sqlalchemy_utils
from sqlalchemy import MetaData
from pigeon.conf.manager import Manager
import pigeon.utils.logger as logger
from alembic.migration import MigrationContext
from alembic.operations import Operations

log = logger.Log('DB', '#2255ee')


class DBManager:
    """
    Handles interaction with databases.
    """
    # metatinfo of db
    dbtype: str
    dbapi: str
    location: str
    # sqlalchemy
    engine: sqlalchemy.Engine
    # list containing all Models
    models: list = list()
    # '_metadata' Model used to keep track of other Models
    _metadata_model = None

    @classmethod
    def __init__(cls):
        cls.dbtype: str = Manager.db_type
        cls.dbapi: str = Manager.db_api
        cls.location: str = Manager.db_location

        # establish connection to database
        cls.connect()

        # get current database schema
        log.debug("LOADING DATABASE SCHEMA")
        cls.metadata = MetaData()
        log.sublog(cls.__str__())

        # generate tables for all models
        log.debug("GENERATING MODELS")
        for model in cls.models:
            model.generate(metadata=cls.metadata)
            log.sublog(model.__repr__())

        # update database schema
        log.debug("MIGRATING DATABASE")
        # get current database schema
        MigrationManager.migrate()

        log.debug("CURRENT DATABASE:")
        log.sublog(cls.__str__(cls.current_metadata))

    @classmethod
    def connect(cls) -> None:
        """
        Checks if database exists and connects to it to check if connection is possible.
        """
        if not cls.location:
            # no location is specified - do not connect to database
            log.error('TRIED CONNECTING TO DATABASE WITHOUT LOCATION - ABORTING!')

        url = f'{cls.dbtype}+{cls.dbapi}://{cls.location}'
        try:
            # check if database exists
            if not sqlalchemy_utils.database_exists(url):
                if not log.ask_user('DATABASE DOES NOT EXIST. CREATE DATABASE? \\[y/n]: '):
                    return
                log.info('CREATING DATABASE')
                sqlalchemy_utils.create_database(url)
            else:
                log.info('DATABASE FOUND')

            # connect to db
            cls.engine = sqlalchemy.create_engine(url, echo=Manager.verbosity >= 5)
            # check if we can connect
            cls.engine.connect()
        except Exception as e:
            log.error(f'FAILED CONNECTING TO DATABASE AT {url}')
            raise e

        log.info(f'ESTABLISHED DATABASE CONNECTION AT {url}')

    @classmethod
    @property
    def current_metadata(cls) -> MetaData:
        _metadata = MetaData()
        _metadata.reflect(cls.engine)
        return _metadata

    @classmethod
    def execute(cls, statement) -> sqlalchemy.CursorResult:
        with cls.engine.connect() as connection:
            return connection.execute(statement)

    @classmethod
    def execute_and_commit(cls, statement) -> sqlalchemy.CursorResult:
        with cls.engine.connect() as connection:
            _return = connection.execute(statement)
            connection.commit()
            return _return

    @classmethod
    def autocommit_execute(cls, statement) -> sqlalchemy.CursorResult:
        autocommit_engine = DBManager.engine.execution_options(isolation_level="AUTOCOMMIT")
        with autocommit_engine.connect() as connection:
            return connection.execute(statement)

    @classmethod
    def __str__(cls, metadata=None) -> str:
        if not metadata: metadata = cls.metadata
        return '\n'.join(f'{str(table.name)}({' | '.join((str(column.name) for column in table.c))})' for table in metadata.tables.values())


class MigrationManager:
    """
    Responsible for migrations in database
    """

    monitored_attributes = {
        'name': str,
        'type': str,
        'autoincrement': str,
        'default': str,
        'nullable': bool,
        'primary_key': bool,
        'server_default': str,
        'server_onupdate': str,
        'unique': bool,
        'system': str,
    }

    @classmethod
    def migrate(cls):
        """
        Migrate database to fit models provided.

        The '_metadata' table is a special table used to keep track of Models, therefore it will be handled differently.
        """

        # create '_metadata' table if missing
        if '_metadata' not in DBManager.current_metadata.tables:
            log.debug(f'TABLE \'_metdata\' NOT FOUND')
            log.verbose(f'CREATING TABLE \'_metadata\'')
            DBManager._metadata_model.generate(DBManager.metadata).create(bind=DBManager.engine)
        else:
            log.debug(f'TABLE \'_metadata\' FOUND')

        # create all tables not already existent in database
        log.info(f'CREATING ALL NOT ALREADY EXISTENT MODELS IN DATABASE')
        for model in DBManager.models:
            if model.__tablename__ not in DBManager.current_metadata.tables:
                if log.ask_user(f'MODEL \'{model.__tablename__}\' HAS BEEN ADDED. CREATE NEW TABLE? \\[y/n]: '):
                    log.info(f'CREATING TABLE \'{model.__tablename__}\'')
                    model.generate(metadata=DBManager.metadata).create(bind=DBManager.engine)
                else:
                    raise ValueError(f'Models not matching database')

        # delete tables not in target
        log.verbose('CHECKING FOR DELETED MODELS')
        for table in DBManager.current_metadata.sorted_tables:
            if table.name not in [model.__tablename__ for model in DBManager.models]:
                if log.ask_user(f'MODEL \'{table.name}\' HAS BEEN REMOVED. DROP TABLE? \\[y/n]: '):
                    log.info(f'DROPPING TABLE \'{table.name}\'')
                    table.drop()
                else:
                    raise ValueError(f'Models not matching database')

        # check for changes in tables
        for current_table in DBManager.current_metadata.sorted_tables:
            target_table, = [table for table in DBManager.metadata.sorted_tables if table.name == current_table.name]
            cls.migrate_table(current=current_table, target=target_table)

        # update '_metadata' table
        cls.update_metadata()


    @classmethod
    def migrate_table(cls, current: sqlalchemy.Table, target: sqlalchemy.Table) -> None:
        """
        Migrates a table from its current state to a target state, asking the user on important changes

        :param current: current table representation (state of database)
        :param target: target table representation
        """

        autocommit_engine = DBManager.engine.execution_options(isolation_level="AUTOCOMMIT")
        with autocommit_engine.connect() as connection:

            # create migration context, etc.
            context: MigrationContext = MigrationContext.configure(connection=connection)
            operations: Operations = Operations(context)

            current_column_names = [column.name for column in current.columns]
            target_column_names = [column.name for column in target.columns]

            # remove columns that no longer exist in models
            for column in current.columns:
                if column.name not in target_column_names:
                    if log.ask_user(f'FIELD \'{current.name}.{column.name}\' HAS BEEN REMOVED. DELETE COLUMN? \\[y/n]: '):
                        log.info(f'REMOVING COLUMN \'{current.name}.{column.name}\'')
                        operations.drop_column(current.name, column.name)
                    else:
                        raise ValueError(f'Model not matching database')

            # add columns that have been added to models
            for column in target.columns:
                if column.name not in current_column_names:
                    if log.ask_user(f'FIELD \'{current.name}.{column.name}\' HAS BEEN ADDED. ADD COLUMN? \\[y/n]: '):
                        log.info(f'ADDING COLUMN \'{current.name}.{column.name}\'')
                        if not column.nullable and not column.server_default:
                            log.error('CANNOT CREATE COLUMN WHICH IS NOT NULLABLE AND HAS NO SERVER_DEFAULT VALUE')
                            raise ValueError(f'Field \'{current.name}.{column.name}\' not migratable')
                        operations.add_column(current.name, column)
                    else:
                        raise ValueError(f'Model not matching database')

        # update already existing columns
        for current_column in current.columns:
            for target_column in target.columns:
                if current_column.name == target_column.name:
                    cls.migrate_column(current=current_column, target=target_column)

    @classmethod
    def migrate_column(cls, current: sqlalchemy.Column, target: sqlalchemy.Column) -> None:
        model = DBManager._metadata_model
        autocommit_engine = DBManager.engine.execution_options(isolation_level="AUTOCOMMIT")
        with autocommit_engine.connect() as connection:
            # create migration context, etc.
            context: MigrationContext = MigrationContext.configure(connection=connection)
            operations: Operations = Operations(context)

            log.debug(f'COMPARING COLUMN \'{current.table.name}.{current}\' WITH \'{target.table.name}.{target}\'')

            query_result = model.select().where(model.table == current.table.name).where(model.name == current.name).execute()
            
            if not query_result:
                log.debug(f'FOUND NO METADATA OBJECT FOR \'{current.table.name}.{current}\' - SKIPPING!')
                return

            previous, = query_result
            log.debug(f'FOUND METADATA OBJECT FOR \'{current.table.name}.{current}\'')
            log.sublog(previous.__repr__())

            target_attributes = cls._get_column_attributes(target)

            for attribute in cls.monitored_attributes:
                if (prev_val := getattr(previous, attribute)) != (new_val := target_attributes.get(attribute)):
                    log.debug(f'MISSMATCH WITH ATTRIBUTE \'{attribute}\'')
                    log.sublog(f'PREVIOUS: {prev_val}')
                    log.sublog(f'TARGET: {new_val}')

                    if log.ask_user(f'PROPERTY \'{attribute}\' HAS CHANGED FOR \'{current.table.name}.{current}\' '
                                    f'(PREVIOUS: {prev_val}, NOW: {new_val}). MIGRATE COLUMN? \\[y/n]: '):
                        log.info(f'MIGRATING PROPERTY \'{attribute}\' FOR \'{current.table.name}.{current}\'')
                        operations.alter_column(table_name=current.table.name, column_name=current.name, **{attribute: new_val})
                    else:
                        raise ValueError(f'Model not matching database')

    @classmethod
    def _compare_column_types(cls, type1, type2) -> bool:
        return type1.python_type == type2.python_type

    @classmethod
    def update_metadata(cls):
        """
        Updates the '_metadata' table used to keep track of table schemas
        """
        # get '_metadata' table
        _metadata_table = DBManager._metadata_model.__table__

        log.debug(f'DELETING DATA FROM TABLE \'_metadata\' FOR REGENERATION')
        with DBManager.engine.connect() as connection:
            connection.execute(sqlalchemy.delete(_metadata_table))
            connection.execute(sqlalchemy.select())
            connection.commit()
            d = connection.execute(sqlalchemy.select(_metadata_table))
            print([dir(row) for row in d])

        log.verbose('UPDATING \'_metadata\' TABLE')
        for table in DBManager.metadata.sorted_tables:
            for column in table.columns:
                attributes = cls._get_column_attributes(column=column)
                log.debug(f'PROPERTIES FOR \'{table}.{column.name}\': {attributes}')
                with DBManager.engine.connect() as connection:
                    connection.execute(sqlalchemy.insert(_metadata_table).values(table=table.name, **attributes))
                    connection.commit()
                log.debug(f'UPDATED METADATA FOR \'{table}.{column.name}\'')

    @classmethod
    def _get_column_attributes(cls, column: sqlalchemy.Column) -> dict[str, str | bool | Any]:
        """
        Gets all attributes listed in cls.monitored_attributes from the column and returns them as a dict.
        Additionally applies type conversion as described in cls.monitored_attributes to the attribute values.

        :param column: Column to get the attributes from
        :returns: Attributes as dict
        """
        for attribute in cls.monitored_attributes:
            if not hasattr(column, attribute):
                raise ValueError(f'COLUMN \'{column.table.name}.{column.name}\' MISSING ATTRIBUTE \'{attribute}\'')

        # gather attributes and do type conversion
        attributes = {}
        for attribute, attribute_type in cls.monitored_attributes.items():
            attributes[attribute] = attribute_type(getattr(column, attribute))

        return attributes
