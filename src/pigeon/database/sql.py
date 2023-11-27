from sqlalchemy import create_engine
from pigeon.conf.manager import Manager
import pigeon.utils.logger as logger

log = logger.Log('DB', '#2255ee')

connection = None

class DatabaseManager:
    """
    Handles interaction with databases.
    """
    def __init__(self):
        # metatinfo of db
        self.dbtype: str = Manager.dbtype
        self.dbapi: str = Manager.dbapi
        self.location: str = Manager.db_location
    
        global connection
        connection = self.connect()
    
    def connect(self):
        if not self.location:
            # no location is specified - do not connect to database
            log.error('TRIED CONNECTING TO DATABASE WITHOUT LOCATION - ABORTING!')
    
        url = f'{self.dbtype}+{self.dbapi}://{self.location}'
        self.engine = create_engine(url, echo=Manager.verbosity >= 4)
        try:
            # connect to db
            connection = self.engine.connect()
        except e:
            log.error(f'FAILED CONNECTING TO DATABASE TO {url}')
    
        log.info(f'ESTABLISHED DATABASE CONNECTION TO {url}')
        return connection
        
    def migrate(self, models: tuple[Model, ...]) -> None:
        """
        Migrate database to fit models provided
        """
        
        # first query database for existing configuration
        schema = self.schema()
        
    def schema(self) -> tuple:
        """
        Queries and returns database schema
        """
        ...
        
    def alter_column(self, table_name: str, column_name: str, column_type: str, operation: str='add') -> None:
        # run query to altering a single column in a specific table in the database
        self.engine.execute(f'alter table {table_name} {operation} column {column_name} {column_type}')

        
class Model:
    """
    A database model for the database
    """
    def __new__(cls, *args, **kwargs):
        # get all fields and compare to database, if they do not match, ask
        # if should migrate database
        
        
        return object.__new__(*args, **kwargs)

class Field:
    """
    Singular field in database model
    """
    def __init__(self, field_type, default=None):
        ...