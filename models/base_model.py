#!/usr/bin/python3
"""Definition of class basemodel"""
import uuid
from datetime import datetime
from models.__init__ import storage


class BaseModel:
    """Definition of class basemodel"""

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        for key, value in kwargs.items():
            if key == "created_at" or key == "updated_at":
                value = datetime.now()
            elif key == "__class__":
                pass
            else:
                setattr(self, key, value)
        if args is None and kwargs is None:
            storage.new(self)

    def __str__(self):
        """return string representation of the object"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """update the time"""
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """returns list of attributes including class name"""
        dict_copy = self.__dict__.copy()
        dict_copy["__class__"] = self.__class__.__name__
        dict_copy["created_at"] = self.created_at.isoformat()
        dict_copy["updated_at"] = self.updated_at.isoformat()
        return dict_copy
