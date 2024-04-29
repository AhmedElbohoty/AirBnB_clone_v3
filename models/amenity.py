#!/usr/bin/python
""" holds class Amenity"""
from sqlalchemy import Column, String
import models
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """Representation of Amenity """

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)

    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""
