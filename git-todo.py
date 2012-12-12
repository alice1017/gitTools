#!/usr/bin/env python
#coding: utf-8

import os
import miniparser

from util import core
from util import adjust
from util import objects

from util.git import *
from util.color import *
from util.objects import Todo
from datetime import datetime
from sys import exit as kill

parser = miniparser.parser(
            version="0.1.0b",
            description="You can manage to" \
                    "What you want to do on your git repository")

CACHE_FILE = os.path.join(git_directory(), "gitodo")
CACHE_FILE_PATH = os.path.join(os.getcwd(), CACHE_FILE)

@parser.option(
    "init",
    description="prepare for managing todo")
def initialize():
    # check exist file
    if os.access(CACHE_FILE_PATH, os.F_OK):
        print "In this repository, you already initialized."
        return 
    # create cache file
    core.save_state([], open(CACHE_FILE_PATH,"w"))


@parser.option("new",
    description="create new todo, Please write TODO content at argument.")
def create(content):
    # ------------------------------------------------
    # ToDo object
    #   1. id (str)               - git hash-object
    #   2. content(str)           - todo content string
    #   3. created_at(datetime)   - datetime when open todo
    #   4. status(str)            - open or close
    #   4. correlate_commit(str)  - commit hash when created todo
    #   5. closed_at(datetime)    - datetime when close todo
    #   6. closing_commit(str)    - commit hash when closed todo
    # ------------------------------------------------

    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))

    todo_info = {}
    todo_info["hashid"] = make_hash(content)
    todo_info["content"] = content
    todo_info["created_at"] = datetime.now()
    todo_info["status"] = "OPEN"
    todo_info["correlate_commit"] = adjust.get_latest_commit().commithash
    todo_info["closed_at"] = None
    todo_info["closing_commit"] = None

    todo_obj = Todo(**todo_info)
    todo_container.append(todo_obj)
    core.save_state(todo_container, open(CACHE_FILE_PATH,"w"))

@parser.option("ls","list", description="You can show all todos.")
def showall():
    if os.access(CACHE_FILE_PATH, os.F_OK) != True:
        print "The repository does not todo initialized yet."
        print "Please do 'git todo init'"
        kill(1)

    # get todo container
    todo_container = core.load_state(open(CACHE_FILE_PATH,"r"))
    
    header = "#  "+"Date".ljust(21)+"Stat".ljust(6)+"Hash".ljust(12)+"Content"
    title = "%(index)s  %(created_at)s  %(status)s  %(hashid)s  %(content)s"

    print header
    print "-"*core.terminal_width()
    for index, todo in enumerate(todo_container):
        print title % {
              "index"      : yellow(index),
              "created_at" : todo.created_at.strftime("20%y/%m/%d %H:%M:%S"),
              "status"     : (blue(todo.status) if todo.status == "OPEN"
                                              else red(todo.status)),
              "hashid"     : todo.hashid[:10],
              "content"    : todo.content,
                }

@parser.option("alldelete",
    description="This is Only Development option. You can delete all ToDo data")
def alldeelete():
    # delete cache file
    if os.access(CACHE_FILE_PATH, os.F_OK):
        core.shellrun("rm", "%s" % CACHE_FILE_PATH)

    print "Complete"

if __name__ == "__main__":
    if check_exist_repo() == False:
        print yellow("There is not git repository!")
        miniparser.kill(1)

    parser.parse()
