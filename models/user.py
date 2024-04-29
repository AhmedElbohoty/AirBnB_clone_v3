#!/usr/bin/python3
""" holds class User"""
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base
import hashlib


class User(BaseModel, Base):
    """Representation of a user """

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, k, v):
        """Add security to user pasword"""
        if k != "password":
            super().__setattr__(k, v)
            return

        secure_password = hashlib.md5(v.encode()).hexdigest()
        super().__setattr__(k, secure_password)

    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
