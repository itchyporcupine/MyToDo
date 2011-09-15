import argparse
import os
import json
from todolist import TodoList


folder = os.path.expanduser("~") + "/.mytodo/"
default_listname = "default_todo"
list_extension = ".json"


#Parser stuff
ARG_DESCRIPTION = """Manage todo lists"""
ARG_PROG = """mytodo"""
ARG_EPILOG = """Text following the argument descriptions"""
ARG_ADD_HELP = True

def add_task(task):
    """Adds an item to the default list"""
    list_name = folder + default_listname + list_extension
    
    todo_list = TodoList(list_name)
    todo_list.add(task)
    todo_list.save()
   
    print "Added to '%s' to %s" % (task, default_listname + list_extension)

def mark_task_as_done(task_id):
    """Marks task as done"""
    list_name = folder + default_listname + list_extension
    todo_list = TodoList(list_name)
    removed_text = todo_list.remove(task_id)
    todo_list.save()

    print "Removed '%s' from %s" % (removed_text, default_listname + list_extension)

def print_list():
    """Prints the default list"""
    list_name = folder + default_listname + list_extension
    print TodoList(list_name)

def install():
    """Sets up files for storing todo lists."""
    try:
        os.mkdir(folder)
    except OSError as e:
        if e.errno == 17: # file exists, do nothing
            pass
        else: #something has gone seriously wrong
            raise e

    #Time to create a new list
    try:
        json_file = open(folder + default_listname + list_extension, 'r')
        json.loads(json_file.read())
        print "MyToDo has already been installed"
    except IOError as e:
        if e.errno == 2: #no file, create it
            json_file = open(folder + "default_todo" + ".json", 'w')
            json_file.write("[]")
            print "MyToDo is now installed."


#########################################################
#########################################################

parser = argparse.ArgumentParser()
subparser = parser.add_subparsers()

#add command
parser_add = subparser.add_parser("add")
parser_add.add_argument("add_called", action='store_true')
parser_add.add_argument("msg")

#done command
parser_done = subparser.add_parser("done")
parser_done.add_argument("done_called", action='store_true')
parser_done.add_argument("id", type=int)

#list command
parser_list = subparser.add_parser("list")
parser_list.add_argument("list_called", action='store_true')

#install command
parser_install = subparser.add_parser("install")
parser_install.add_argument("install_called", action='store_true')


args = parser.parse_args()
namespace_dictionary = args.__dict__

if 'list_called' in namespace_dictionary:
    print_list()
elif 'install_called' in namespace_dictionary:
    install() 
elif 'add_called' in namespace_dictionary:
    add_task(args.msg)
elif 'done_called' in namespace_dictionary:
    mark_task_as_done(args.id)



