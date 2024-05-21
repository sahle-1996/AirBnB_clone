#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arguments):
    curly = re.search(r"\{(.*?)\}", arguments)
    square = re.search(r"\[(.*?)\]", arguments)
    if curly is None:
        if square is None:
            return [token.strip(",") for token in split(arguments)]
        else:
            lexer = split(arguments[:square.span()[0]])
            result = [token.strip(",") for token in lexer]
            result.append(square.group())
            return result
    else:
        lexer = split(arguments[:curly.span()[0]])
        result = [token.strip(",") for token in lexer]
        result.append(curly.group())
        return result


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, line):
        """Default behavior for cmd module when input is invalid"""
        cmd_dict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", line)
        if match:
            class_name, command = line[:match.span()[0]], line[match.span()[1]:]
            match = re.search(r"\((.*?)\)", command)
            if match:
                action, args = command[:match.span()[0]], match.group(1)
                if action in cmd_dict:
                    return cmd_dict[action](f"{class_name} {args}")
        print(f"*** Unknown syntax: {line}")
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        args = parse(line)
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = eval(args[0])()
            print(new_instance.id)
            storage.save()

    def do_show(self, line):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        args = parse(line)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in obj_dict:
                print("** no instance found **")
            else:
                print(obj_dict[key])

    def do_destroy(self, line):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        args = parse(line)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
        elif args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            key = f"{args[0]}.{args[1]}"
            if key not in obj_dict:
                print("** no instance found **")
            else:
                del obj_dict[key]
                storage.save()

    def do_all(self, line):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        args = parse(line)
        if args and args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if not args or args[0] == obj.__class__.__name__:
                    obj_list.append(str(obj))
            print(obj_list)

    def do_count(self, line):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        args = parse(line)
        count = sum(1 for obj in storage.all().values() if obj.__class__.__name__ == args[0])
        print(count)

    def do_update(self, line):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        args = parse(line)
        obj_dict = storage.all()
        if not args:
            print("** class name missing **")
            return False
        if args[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        key = f"{args[0]}.{args[1]}"
        if key not in obj_dict:
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(args) == 4:
            obj = obj_dict[key]
            if args[2] in obj.__class__.__dict__:
                attr_type = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = attr_type(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        elif isinstance(eval(args[2]), dict):
            obj = obj_dict[key]
            for k, v in eval(args[2]).items():
                if (k in obj.__class__.__dict__ and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    attr_type = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = attr_type(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
