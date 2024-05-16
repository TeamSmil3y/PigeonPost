import sqlalchemy
from sqlalchemy import MetaData, Table, Column, select, delete, insert, update, and_, or_
from pigeon.database.sql import DBManager


class Field:
    """
    Singular field in database model, only used to compute sqlalchemy.Column objects for database schema
    """

    def __init__(self, field_type, **kwargs):
        self.name = None
        self.type = field_type
        self.properties: dict = kwargs

    def generate(self, name: str | None = None):
        """
        Creates a sqlalchemy.Column object using the column name and the data passed to the class upon initialization
        """
        if name:
            self.name = name

        return sqlalchemy.Column(self.name, self.type, **self.properties)

    @property
    def __dict__(self):
        d: dict = dict()
        for key, value in self.generate().__dict__.items():
            if value and not key.startswith('_'):
                d[key] = value
        return d

    def __str__(self):
        return str(self.__dict__)


class Model:
    """
    Relation in the database
    """

    def __new__(cls, **kwargs):
        """
        When creating an instance of a Model class, really we want to return an object of type ObjectModel
        corresponding to the provided Model.

        :param **kwargs: arguments for ObjectModel, i.e. column values
        """
        for column in cls.__table__.columns:
            if column.name not in kwargs:
                kwargs[column.name] = None

        return ModelObject(model=cls, exists=False, **kwargs)

    @classmethod
    def __init_subclass__(cls, **kwargs):
        """
        Get all fields and compare to database, if they do not match, ask if database should be migrated
        """
        cls.__fields: list[Field] = list()

        if not hasattr(cls, '__tablename__'):
            cls.__tablename__ = cls.__name__

        if cls.__tablename__ == '_metadata':
            DBManager._metadata_model = cls
        DBManager.models.append(cls)

        super().__init_subclass__(**kwargs)

    @classmethod
    def generate(cls, metadata: MetaData) -> Table:
        """
        Transforms the fields to sqlalchemy.Columns objects

        :param metadata: sqlalchemy.MetaData object used during table creation
        :returns: sqlalchemy.Table object representing the Model
        """
        attributes = {attr: getattr(cls, attr) for attr in dir(cls) if not attr.startswith('__')}

        # generate sqlalchemy.Column objects from fields
        columns = []
        cls.__fields = []
        for key, value in attributes.items():
            if isinstance(value, Column):
                columns.append(value)
            elif isinstance(value, Field):
                columns.append(value.generate(name=key))
                cls.__fields.append(value)

        cls.__table__ = Table(
            cls.__tablename__,
            metadata,
            *columns,
            extend_existing=True,
        )

        for field in cls.__fields:
            setattr(cls, field.name, cls.column(field.name))

        cls.__column_order__ = [column.name for column in cls.__table__.columns]

        return cls.__table__

    @classmethod
    def __get_primary_keys(cls) -> list:
        """
        Gathers names of all primary key attributes
        """
        primary_keys = []
        for column in cls.columns:
            if column.primary_key:
                primary_keys.append(column.name)
        return primary_keys

    @classmethod
    def column(cls, name: str) -> Column:
        """
        Returns column with the given name.

        :param name: The name of the column
        """
        column, = (column for column in cls.__table__.columns if column.name == name)
        return column

    @classmethod
    def select(cls, columns=None):
        if not columns:
            return Query(query=select(cls.__table__), returns=True, model=cls)
        else:
            return Query(query=select(*columns), returns=False, model=cls)

    @classmethod
    def delete(cls):
        return Query(query=delete(cls.__table__), returns=False, model=cls)

    @classmethod
    def insert(cls):
        return Query(query=insert(cls.__table__).returning(*cls.__table__.columns), returns=True, model=cls)

    @classmethod
    def update(cls):
        return Query(query=update(cls.__table__), returns=False, model=cls)

    @classmethod
    def all(cls) -> list:
        rows = DBManager.execute(select(cls.__table__))
        return ModelObject.from_rows(rows=rows, model=cls)

    @classmethod
    def __repr__(cls) -> str:
        return f'{cls.__tablename__}({', '.join(field.name for field in cls.__fields)})'


class ModelObject:
    """
    Object that represents a row in a table defined by a Model, can be edited and saved back to the database
    """

    def __init__(self, model, exists=True, **kwargs):
        # reference to the original model that the object is derived from
        self.__model: Model = model
        # exists stores whether the object actually exists in the database
        self.__exists: bool = exists

        # original attributes of object used to find it when updating values
        self.__original_attributes: dict = kwargs
        # attributes that correspond to columns in database
        self.__database_attributes: list = kwargs.keys()
        for key, value in kwargs.items():
            self.__setattr__(key, value)

    def __get_database_attributes(self) -> dict:
        """
        Gathers attributes that correspond to columns, useful when saving object to database
        """
        attributes = {}
        for attribute in self.__database_attributes:
            value = self.__getattribute__(attribute)
            if self.__exists or value:
                attributes[attribute] = value
        return attributes

    def __where_in_table(self):
        """
        Returns value that describes a where clause used to find object in table.
        """
        if self.__exists:
            return and_(column == val for column, val in
                        zip(self.__model.__table__.c, self.__original_attributes.values()))
        return and_(column == val for column, val in self.__original_attributes.items())

    def save(self) -> None:
        """
        Saves the object to the database (updates/inserts the row)
        """
        attributes = self.__get_database_attributes()

        if not self.__exists:
            # if object is not already in the database, create a new one
            new_model, = self.__model.insert().values(**attributes).execute()

            attributes = new_model.__get_database_attributes()
            # update all attributes according to database
            for attribute, value in attributes.items():
                setattr(self, attribute, value)

            self.__exists = True
        else:
            # if object already exists, update it
            DBManager.autocommit_execute(self.__model.__table__.update()
                                         .where(self.__where_in_table()).values(**attributes))

            self.__original_attributes = attributes

    def delete(self) -> None:
        """
        Deletes the object from the database (deletes the row)
        """
        if not self.__exists:
            return

        # delete row in database
        print("PDEL:", self.__model.select().where(self.__where_in_table()).execute())
        self.__model.delete().where(self.__where_in_table()).execute()

        self.__exists = False

    @staticmethod
    def from_rows(rows, model):
        return [ModelObject(model=model, **{column: val for column, val in zip(model.__column_order__, row)})
                for row in rows]

    def __repr__(self):
        return f'{self.__model.__tablename__}({", ".join(f"{key}={value}" for
                                                         key, value in self.__get_database_attributes().items())})'


class Query:
    """
    Represents a sql query, can be executed.
    """

    def __init__(self, query, model, returns=False):
        """
        :param query: The original sqlalchemy query, that can be edited further using methods of Query
        :param returns: Whether the Query returns ModelObjects
        :param model: Model that the Query originates from
        """
        self.__returns = returns
        self.__query = query
        self.__model = model

    def execute(self) -> list[ModelObject] | sqlalchemy.CursorResult:
        """
        Runs the query and returns the result. If the query is ought to return valid data for ModelObjects,
        a list of ModelObjects created from the data will be returned instead
        """
        query_result = DBManager.execute_and_commit(self.__query)
        # either create ModelObjects from data or return query result as is
        if self.__returns:
            return ModelObject.from_rows(rows=query_result, model=self.__model)
        return query_result

    def __append(self, new_query, returns=None):
        return Query(query=new_query, model=self.__model, returns=returns or self.__returns)

    def where(self, *args, **kwargs):
        return self.__append(self.__query.where(*args, **kwargs))

    def order_by(self, *args, **kwargs):
        return self.__append(self.__query.order_by(*args, **kwargs))

    def values(self, *args, **kwargs):
        return self.__append(self.__query.values(*args, **kwargs))

    def __repr__(self):
        return ({'model': self.__model,
                 'query': self.__query.__str__(),
                 'returns': 'ModelObject' if self.__returns else 'raw'}
                .__repr__())
