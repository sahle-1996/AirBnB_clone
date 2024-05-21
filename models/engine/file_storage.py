#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Represents an abstract storage engine.
    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Dictionary to store objects.
    """
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects."""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects obj with key <obj_class_name>.id"""
        obj_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(obj_name, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file __file_path."""
        obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(obj_dict, f)

    def reload(self):
        """Deserializes the JSON file __file_path to __objects, if it exists."""
        try:
            with open(FileStorage.__file_path, "r") as f:
                obj_dict = json.load(f)
                for obj_data in obj_dict.values():
                    cls_name = obj_data.pop("__class__")
                    self.new(eval(cls_name)(**obj_data))
        except FileNotFoundError:
            pass
