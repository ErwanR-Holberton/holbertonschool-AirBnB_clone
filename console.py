#!/usr/bin/python3
"""Defines the HBnB console."""


import cmd
import shlex
from datetime import datetime
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """ hbnb command interpreter """
    prompt = "(hbnb) "
    class_dict = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """ exit the program"""
        return True

    def do_EOF(self, arg):
        """ End of file"""
        return True

    def emptyline(self):
        """don´t execute nothing """
        pass

    def do_create(self, arg):
        """creates an instance of a class"""
        args_list = shlex.split(arg)
        if len(args_list) == 0:
            print("** class name missing **")
        else:
            class_name = args_list[0]
            if class_name not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
            else:
                obj = HBNBCommand.class_dict[class_name]()
                storage.new(obj)
                storage.save()
                print(obj.id)

    def do_show(self, arg):
        """Prints the string representation of an instance
        based on the class name and id"""
        args_list = shlex.split(arg)
        if len(args_list) == 0:
            print("** class name missing **")
        else:
            class_name = args_list[0]
            if class_name not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
            elif len(args_list) < 2:
                print("** instance id missing **")
            else:
                instance_id = args_list[1]
                key = "{}.{}".format(class_name, instance_id)
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    instance = storage.all()[key]
                    print(instance)

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id """
        args_list = shlex.split(arg)
        if len(args_list) == 0:
            print("** class name missing **")
        else:
            class_name = args_list[0]
            if class_name not in HBNBCommand.class_dict:
                print("** class doesn't exist **")
            elif len(args_list) < 2:
                print("** instance id missing **")
            else:
                instance_id = args_list[1]
                key = "{}.{}".format(class_name, instance_id)
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, arg):
        """ Prints all str representation of all instances """
        args_list = shlex.split(arg)
        obj_list = []

        if len(args_list) == 0:
            for obj in storage.all().values():
                obj_list.append(str(obj))
            print(obj_list)
        else:
            class_name = args_list[0]
            if class_name in HBNBCommand.class_dict:
                for obj in storage.all().values():
                    if type(obj).__name__ == class_name:
                        obj_list.append(str(obj))
                print(obj_list)
            else:
                print("** class doesn't exist **")

    def do_update(self, arg):
        """ Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args_list = shlex.split(arg)
        if len(args_list) == 0:
            print("** class name missing **")
            return
        class_name = args_list[0]
        if class_name not in HBNBCommand.class_dict:
            print("** class doesn't exist **")
            return
        elif len(args_list) < 2:
            print("** instance id missing **")
            return
        instance_id = args_list[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in storage.all():
            print("** no instance found **")
            return
        instance = storage.all()[key]
        if len(args_list) < 3:
            print("** attribute name missing **")
            return
        attribute_name = args_list[2]
        if len(args_list) < 4:
            print("** value missing **")
            return
        value = args_list[3]
        try:
            value = eval(value)
        except (NameError, SyntaxError):
            pass
        setattr(instance, attribute_name, value)
        instance.updated_at = datetime.now()
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
