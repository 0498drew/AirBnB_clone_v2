#!/usr/bin/python3
"""Defines the DBStorage engine."""
from os import getenv
from models.base_model import Base
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


if getenv('HBNB_TYPE_STORAGE') == 'db':
    from models.place import place_amenity

class DBStorage:
    """Represents a database storage engine.
    Attributes:
        __engine (sqlalchemy.Engine): The working SQLAlchemy engine.
        __session (sqlalchemy.Session): The working SQLAlchemy session.
    """

    __engine = None
    __session = None
     __classes = {
                 'User': User, 'Place': Place,
                 'State': State, 'City': City, 'Amenity': Amenity,
                 'Review': Review
                }

    def __init__(self):
        """Initialize a new DBStorage instance."""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query on the curret database session all objects of the given class.
        If cls is None, queries all types of objects.
        Return:
            Dict of queried classes in the format <class name>.<obj id> = obj.
        """
        objs = {}
        if cls is None:
            for table in DBStorage.__classes.values():
                for row in self.__session.query(table).all():
                    key = type(row).__name__ + '.' + row.id
                    objs.update({key: row})
        else:
            if type(cls).__name__ == str:
                cls = eval(cls)
             for row in self.__session.query(cls).all():
                key = type(cls).__name__ + '.' + row.id
                objs.update({key: row})

        return objs

    def new(self, obj):
        """Add obj to the current database session."""
        if obj is not None:
            self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session."""
        if obj is not None:
            # self.__session.query(type(obj)).filter(type(obj).id == obj.id)
            #               .delete()
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.remove()
