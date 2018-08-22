#!/usr/bin/python3
'''
    Implementation of the User class which inherits from BaseModel
'''
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from hashlib import md5


class User(BaseModel, Base):
    '''
        Definition of the User class
    '''
    __tablename__ = "users"
    if getenv("HBNB_TYPE_STORAGE", "fs") == "db":
        email = Column(String(128), nullable=False)
        _password = Column("password", String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user",
                              cascade="all, delete, delete-orphan")
        reviews = relationship("Review", backref="user",
                               cascade="all, delete, delete-orphan")
    else:
        email = ""
        _password = ""
        first_name = ""
        last_name = ""

    @property
    def password(self):
        """password getter
        Return:
            password that is set
        """
        return self._password

    @password.setter
    def password(self, pwd):
        """password setter
        Args:
            passwrod: input password
        """
        self._password = md5(pwd.encode()).hexdigest()
