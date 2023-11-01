#!/usr/bin/python3
"""definition of class used to store objects"""
import json
from models.base_model import BaseModel


class FileStorage:
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns a dictionaty '__objects'"""
        return self.__objects

    def new(self, obj):
        """Sets in '__objects' the object with the key """
        index = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[index] = obj

    def save(self):
        """Serializes '__objects' dictionary to a JSON file"""
        dict_to_save = {}
        for key, obj in self.__objects.items():
            dict_to_save[key] = obj.to_dict()
        with open(self.__file_path, "w") as file:
            json.dump(dict_to_save, file)

    def reload(self):
        """Deserializes the JSON file to __objects' dictionary'"""
        from models.base_model import BaseModel
        try:
            with open(self.__file_path, encoding='utf-8') as File:
                cls = '__class__'
                for key, value in json.load(File).items():
                    self.__objects[key] = eval(value[cls] + '(**value)')
        except FileNotFoundError:
            pass
